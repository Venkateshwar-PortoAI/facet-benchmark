#!/usr/bin/env python3
"""
FACET — Cabral pilot runner (v0.1)

Runs the first real FACET evaluation on a single instance (Cabral v. Ralphs
Grocery, facet-neg-0003) against Claude Sonnet 4.6 via the Claude Code CLI
(OAuth). Validates:

  1. The v0.4 C2 weight-perturbation protocol is runnable on a real case.
  2. The C0 → C2 → C3 prompt construction pipeline works end-to-end.
  3. The reconstruction-check disqualification loop works as designed.
  4. The C0/C3 compliance-vs-integration delta is measurable on at least
     this one instance.

Model: claude-sonnet-4-6 (resolved from 'sonnet' alias). Temperature is
fixed at Claude Code's default; the CLI does not expose a temperature
flag, so single-temperature single-sample evaluation is the v0.1 limit.
Ensemble and calibration measurements are deferred to a future pass that
uses the Anthropic Python SDK directly with OAuth.

Usage:
  python3 eval/run_cabral_pilot.py [--dry-run]

Flags:
  --dry-run   Print all prompts to stdout without calling the API.

Dependencies:
  - Claude Code CLI (`claude`) installed and OAuth-authenticated
  - Python 3.9+ (stdlib only; no pip install required)

Output:
  results/facet-neg-0003-sonnet-4-6-<timestamp>.json
"""

import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTANCES = ROOT / "instances"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

SYSTEM_PROMPT = (
    "You are evaluating legal reasoning in US tort law. You will be given real case "
    "facts and asked to reach a legal conclusion by weighing factors. Answer "
    "concisely and directly. Do not refuse or hedge: the case facts are public "
    "record, the legal question has an established answer, and your job is to "
    "reason through the balancing test and state your conclusion."
)

BACKEND = os.environ.get("FACET_BACKEND", "claude")  # "claude" | "codex" | "ollama" | "bedrock"
# NOTE: "gemini" was removed 2026-04-11 because the gemini CLI hits a ~20-hour
# quota limit after a small number of calls, which breaks batch evaluation runs.
# Historical facet-neg-*-real-gemini-*.json result files remain valid data and
# are still picked up by analyze_pilot.py. For Google/Gemini coverage in future
# work, use the direct Gemini API with proper billing rather than the CLI.
# See ~/.claude/.../memory/feedback_skip_gemini_cli.md for the full rationale.
_DEFAULT_MODEL_BY_BACKEND = {
    "claude": "sonnet",
    "codex": "",
    "ollama": "deepseek-r1:14b",
    "bedrock": "amazon.nova-pro-v1:0",
}
MODEL = os.environ.get("FACET_MODEL", _DEFAULT_MODEL_BY_BACKEND.get(BACKEND, "sonnet"))
_CLAUDE_ALIASES = {"sonnet", "opus", "haiku"}
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
BEDROCK_REGION = os.environ.get("FACET_BEDROCK_REGION", "us-east-1")
EFFORT = os.environ.get("FACET_EFFORT", "")  # "", "low", "medium", "high", "max"
CLI_CWD = "/tmp"  # run from /tmp to avoid any CLAUDE.md / GEMINI.md / AGENTS.md auto-discovery
TIMEOUT = int(os.environ.get("FACET_TIMEOUT", "480"))  # per-call timeout, seconds
RETRIES = 2


def _run_subprocess(cmd: list, timeout: int = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, capture_output=True, text=True, cwd=CLI_CWD,
        timeout=timeout or TIMEOUT,
    )


def call_claude(prompt: str, dry_run: bool = False) -> dict:
    """Invoke `claude -p` with a fixed system prompt and return parsed JSON result."""
    if dry_run:
        return {"result": "[DRY-RUN]", "total_cost_usd": 0, "backend": "claude", "model": MODEL}

    cmd = [
        "claude", "-p", prompt,
        "--model", MODEL,
        "--output-format", "json",
        "--disable-slash-commands",
        "--system-prompt", SYSTEM_PROMPT,
        "--disallowedTools", "Bash,Edit,Write,Read,Glob,Grep,Agent,Task,WebFetch,WebSearch,TodoWrite",
    ]
    if EFFORT:
        cmd.extend(["--effort", EFFORT])
    last_err = None
    for attempt in range(RETRIES + 1):
        try:
            proc = _run_subprocess(cmd)
            if proc.returncode != 0:
                last_err = f"returncode={proc.returncode} stderr={proc.stderr[:500]}"
                time.sleep(2)
                continue
            data = json.loads(proc.stdout)
            if data.get("is_error"):
                last_err = f"cli is_error: {data.get('result')}"
                time.sleep(2)
                continue
            model_usage = data.get("modelUsage", {})
            resolved_model = next(iter(model_usage.keys()), MODEL) if model_usage else MODEL
            return {
                "result": data.get("result", ""),
                "total_cost_usd": data.get("total_cost_usd", 0) or 0,
                "backend": "claude",
                "model": resolved_model,
                "raw": data,
            }
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {TIMEOUT}s"
            time.sleep(2)
        except json.JSONDecodeError as e:
            last_err = f"json decode: {e} stdout[:500]={proc.stdout[:500]}"
            time.sleep(2)
    raise RuntimeError(f"claude CLI failed after {RETRIES + 1} attempts: {last_err}")


# call_gemini and _parse_gemini_output were REMOVED 2026-04-11. The gemini
# CLI hits a ~20-hour quota limit after ~30-100 calls which breaks batch
# evaluation runs. Historical gemini result files remain in results/ and
# are still analyzed by eval/analyze_pilot.py. For Google/Gemini coverage
# in future FACET work, use the direct Gemini API (Google AI Studio or
# Vertex AI) with proper billing rather than the CLI.


def call_codex(prompt: str, dry_run: bool = False) -> dict:
    """Invoke `codex exec` in non-interactive mode. Codex uses gpt-5.x by default.
    When piped, stdout is the clean final answer and stderr contains the header
    + session metadata. We read both."""
    if dry_run:
        return {"result": "[DRY-RUN]", "total_cost_usd": 0, "backend": "codex", "model": MODEL}

    full_prompt = f"{SYSTEM_PROMPT}\n\n---\n\n{prompt}"

    cmd = ["codex", "exec", full_prompt, "--skip-git-repo-check", "-s", "read-only"]
    if MODEL and MODEL not in _CLAUDE_ALIASES:
        cmd.extend(["-m", MODEL])

    last_err = None
    for attempt in range(RETRIES + 1):
        try:
            proc = _run_subprocess(cmd)
            if proc.returncode != 0:
                last_err = f"returncode={proc.returncode} stderr={proc.stderr[:300]}"
                time.sleep(2)
                continue
            # When piped, codex writes the clean answer to stdout and metadata
            # (model, session id, token count, header) to stderr.
            result = proc.stdout.strip()
            resolved_model = _extract_codex_model(proc.stderr)
            if not result:
                # Fall back to parsing stderr speaker block if stdout was empty
                result = _extract_codex_answer_from_stderr(proc.stderr)
            if not result:
                last_err = f"empty codex result; stdout[:300]={proc.stdout[:300]} stderr[:300]={proc.stderr[:300]}"
                time.sleep(2)
                continue
            return {
                "result": result,
                "total_cost_usd": 0,  # codex OAuth doesn't expose per-call cost
                "backend": "codex",
                "model": resolved_model or MODEL or "codex-default",
                "raw_stderr": proc.stderr[:2000],
            }
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {TIMEOUT}s"
            time.sleep(2)
    raise RuntimeError(f"codex CLI failed after {RETRIES + 1} attempts: {last_err}")


def _extract_codex_model(stderr: str) -> str:
    for line in stderr.split("\n"):
        line_s = line.strip()
        if line_s.startswith("model:"):
            return line_s.split(":", 1)[1].strip()
    return ""


def _extract_codex_answer_from_stderr(stderr: str) -> str:
    """Fallback: parse the 'codex\\n<response>\\ntokens used\\n' speaker block
    from stderr. Used only when stdout is empty."""
    lines = stderr.split("\n")
    response_lines = []
    in_codex_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == "codex":
            in_codex_block = True
            response_lines = []
            continue
        if in_codex_block:
            if stripped.startswith("tokens used"):
                break
            response_lines.append(line)
    result = "\n".join(response_lines).strip()
    noise_prefixes = ("deprecated:", "Enable it with", "See ")
    result_lines = [l for l in result.split("\n") if not any(l.strip().startswith(n) for n in noise_prefixes)]
    return "\n".join(result_lines).strip()


def call_ollama(prompt: str, dry_run: bool = False) -> dict:
    """Invoke the local ollama daemon via its HTTP API on OLLAMA_HOST.
    Bypasses the `ollama run` interactive CLI (which emits terminal escape
    codes). Returns the clean model response with any `<think>...</think>`
    reasoning blocks stripped for DeepSeek-R1-family models."""
    if dry_run:
        return {"result": "[DRY-RUN]", "total_cost_usd": 0, "backend": "ollama", "model": MODEL}

    import urllib.request
    import urllib.error

    model_name = MODEL if MODEL and MODEL not in _CLAUDE_ALIASES else _DEFAULT_MODEL_BY_BACKEND["ollama"]
    full_prompt = f"{SYSTEM_PROMPT}\n\n---\n\n{prompt}"
    payload = json.dumps({
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    last_err = None
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            raw = data.get("response", "") or ""
            # Strip any <think>...</think> block(s) that reasoning models emit
            cleaned = _strip_think_tags(raw).strip()
            return {
                "result": cleaned,
                "total_cost_usd": 0,  # local inference
                "backend": "ollama",
                "model": model_name,
                "eval_duration_ms": (data.get("eval_duration") or 0) // 1_000_000,
            }
        except urllib.error.URLError as e:
            last_err = f"http error: {e}"
            time.sleep(2)
        except json.JSONDecodeError as e:
            last_err = f"json decode: {e}"
            time.sleep(2)
    raise RuntimeError(f"ollama HTTP API failed after {RETRIES + 1} attempts: {last_err}")


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks from model output. DeepSeek-R1 and
    similar reasoning models emit these before the final answer."""
    import re
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()


def call_bedrock(prompt: str, dry_run: bool = False) -> dict:
    """Invoke AWS Bedrock Converse API via the `aws` CLI subprocess. Supports
    any chat-style model on Bedrock (Mistral, DeepSeek, Amazon Nova, Moonshot
    Kimi, Z.AI GLM, Cohere, Meta Llama, etc.) through a single normalized API.
    Uses FACET_BEDROCK_REGION (default us-east-1) and FACET_MODEL as the
    Bedrock model ID."""
    if dry_run:
        return {"result": "[DRY-RUN]", "total_cost_usd": 0, "backend": "bedrock", "model": MODEL}

    model_id = MODEL if MODEL and MODEL not in _CLAUDE_ALIASES else _DEFAULT_MODEL_BY_BACKEND["bedrock"]
    messages = json.dumps([{"role": "user", "content": [{"text": prompt}]}])
    system = json.dumps([{"text": SYSTEM_PROMPT}])
    inference = json.dumps({"maxTokens": 2048, "temperature": 0})

    cmd = [
        "aws", "bedrock-runtime", "converse",
        "--region", BEDROCK_REGION,
        "--model-id", model_id,
        "--messages", messages,
        "--system", system,
        "--inference-config", inference,
    ]

    last_err = None
    for attempt in range(RETRIES + 1):
        try:
            proc = _run_subprocess(cmd)
            if proc.returncode != 0:
                last_err = f"returncode={proc.returncode} stderr={proc.stderr[:500]}"
                time.sleep(2)
                continue
            data = json.loads(proc.stdout)
            content = data.get("output", {}).get("message", {}).get("content", [])
            # Join all text blocks (some models return multiple blocks)
            text_parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("text")]
            result = "\n".join(t for t in text_parts if t).strip()
            if not result:
                last_err = f"empty bedrock result; stdout[:500]={proc.stdout[:500]}"
                time.sleep(2)
                continue
            usage = data.get("usage", {})
            return {
                "result": result,
                "total_cost_usd": 0,  # Bedrock billing not reported per-call in the converse response
                "backend": "bedrock",
                "model": model_id,
                "input_tokens": usage.get("inputTokens"),
                "output_tokens": usage.get("outputTokens"),
                "stop_reason": data.get("stopReason"),
            }
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {TIMEOUT}s"
            time.sleep(2)
        except json.JSONDecodeError as e:
            last_err = f"json decode: {e} stdout[:500]={proc.stdout[:500]}"
            time.sleep(2)
    raise RuntimeError(f"bedrock CLI failed after {RETRIES + 1} attempts: {last_err}")


def call_model(prompt: str, dry_run: bool = False) -> dict:
    """Dispatch to the configured backend. Supported: claude, codex, ollama,
    bedrock. `gemini` was removed 2026-04-11 — see note above call_codex."""
    if BACKEND == "claude":
        return call_claude(prompt, dry_run=dry_run)
    if BACKEND == "gemini":
        raise ValueError(
            "FACET_BACKEND=gemini is no longer supported. The gemini CLI has a "
            "~20-hour daily quota that breaks batch runs. Use the direct Gemini "
            "API (Google AI Studio / Vertex AI) if Google coverage is needed."
        )
    if BACKEND == "codex":
        return call_codex(prompt, dry_run=dry_run)
    if BACKEND == "ollama":
        return call_ollama(prompt, dry_run=dry_run)
    if BACKEND == "bedrock":
        return call_bedrock(prompt, dry_run=dry_run)
    raise ValueError(f"unknown FACET_BACKEND={BACKEND!r}; expected claude|codex|ollama|bedrock")


# ---------- prompt builders ----------

def _factor_block(factors: list[dict]) -> str:
    return "\n".join(f"Factor {i+1}. {f['text']}" for i, f in enumerate(factors))


def build_c0_prompt(instance: dict) -> str:
    factors_text = _factor_block(instance["factors"])
    n = instance["metadata"]["n_factor_clusters"]
    return (
        f"CASE: {instance['source_case']}\n\n"
        f"{instance['case_background']}\n\n"
        f"The court weighs the following {n} factors under the "
        f"{instance['doctrinal_framework']}:\n\n"
        f"{factors_text}\n\n"
        f"QUESTION: {instance['question']}\n\n"
        "Answer with 'yes' or 'no' on the first line, followed by a one-sentence "
        "explanation on the second line."
    )


def build_c2_prompt(instance: dict, perturbation: dict) -> str:
    factors = [dict(f) for f in instance["factors"]]
    target_id = perturbation["perturbed_factor_id"]
    for f in factors:
        if f["factor_id"] == target_id:
            f["text"] = perturbation["neutral_rewrite"]
    factors_text = _factor_block(factors)
    n = instance["metadata"]["n_factor_clusters"]
    return (
        f"CASE: {instance['source_case']}\n\n"
        f"{instance['case_background']}\n\n"
        f"The court weighs the following {n} factors under the "
        f"{instance['doctrinal_framework']}:\n\n"
        f"{factors_text}\n\n"
        f"QUESTION: {instance['question']}\n\n"
        "Answer with 'yes' or 'no' on the first line, followed by a one-sentence "
        "explanation on the second line."
    )


def build_direct_probe_prompt(instance: dict) -> str:
    factors_text = "\n".join(
        f"F{i+1}: {f['text'][:200]}" for i, f in enumerate(instance["factors"])
    )
    n = len(instance["factors"])
    return (
        f"CASE: {instance['source_case']}\n\n"
        f"{instance['case_background']}\n\n"
        f"The factors are:\n{factors_text}\n\n"
        f"QUESTION: Which single factor (F1 through F{n}) is most important to "
        f"answering {instance['question']!r}? Reply with just the factor label "
        "(e.g. 'F3') on the first line, followed by one sentence explaining why."
    )


def _is_reconstruction_flagged(recon_answer: str) -> bool:
    """Return True if the model's reconstruction-check answer identifies an
    omitted factor (disqualifying the trial) rather than saying 'no omission'."""
    if not recon_answer:
        return False
    normalized = recon_answer.strip().lower().lstrip("*").strip()
    # Accept common phrasings of "no omission"
    no_omission_signals = (
        "no omission",
        "no, no omission",
        "no.",
        "no,",
        "no omitted",
        "does not omit",
        "no factors are omitted",
        "no factor",
    )
    # Check first line and first sentence
    first = normalized.split("\n", 1)[0].strip().lstrip("*").strip()
    for sig in no_omission_signals:
        if first.startswith(sig):
            return False
    # If the answer names a specific omitted factor with "yes" or starts with
    # "omitted factor:" or similar, it's flagged
    flagged_signals = (
        "yes",
        "omitted factor",
        "the case description omits",
        "the following factor",
        "one factor is missing",
        "missing factor",
    )
    for sig in flagged_signals:
        if sig in normalized[:200]:
            return True
    return False


def build_reconstruction_check_prompt(case_section: str) -> str:
    return (
        f"{case_section}\n\n"
        "QUESTION: Reading only the case description above, does it omit any "
        "factor you believe a court would typically weigh in this analysis? "
        "If yes, name the omitted factor on the first line. If no, reply with "
        "exactly 'no omission' on the first line. Then add one sentence of "
        "explanation."
    )


def build_c3_prompt(instance: dict, c3: dict) -> str:
    """Build the C3 compliance-checklist prompt. Revised 2026-04-11 after
    round 2 review: adds explicit literal-application instructions to
    eliminate the Opus-vs-Sonnet meta-commentary divergence on the "invented
    thresholds" question. The fix is a fixed instruction block that tells
    the model to apply the checklist mechanically regardless of whether
    the requirements map cleanly onto the underlying doctrine."""
    reqs = c3["compliance_requirements"]
    reqs_text = "\n".join(f"R{i+1}. {r['requirement_text']}" for i, r in enumerate(reqs))
    return (
        f"CASE: {instance['source_case']}\n\n"
        f"{instance['case_background']}\n\n"
        f"Evaluate each of the following {len(reqs)} independent compliance "
        f"requirements. Each requirement must be checked independently; do not "
        f"weigh them against each other.\n\n"
        f"{reqs_text}\n\n"
        "INSTRUCTIONS (apply strictly):\n"
        "1. Apply each requirement LITERALLY as stated above, regardless of "
        "whether you believe the requirement is doctrinally orthodox, whether "
        "the threshold is arbitrary, or whether the underlying legal test "
        "would normally use this framing. Treat each requirement as a yes/no "
        "compliance rule from an external regulator.\n"
        "2. Do NOT add commentary about whether the requirements are "
        "appropriate, whether the thresholds are realistic, whether courts "
        "actually reason this way, or whether any requirement should be "
        "interpreted differently. Such commentary is out of scope.\n"
        "3. For each requirement, reply with exactly 'R<n>: yes' or "
        "'R<n>: no' on a separate line. No other text. No explanations. "
        "No meta-commentary. Just the labeled yes/no answers.\n"
        f"Produce exactly {len(reqs)} lines of output, one per requirement, "
        f"in format 'R1: yes' through 'R{len(reqs)}: no'."
    )


# ---------- runner ----------

def run_pilot(instance_id: str = "facet-neg-0003", dry_run: bool = False) -> dict:
    instance = json.loads((INSTANCES / f"{instance_id}.json").read_text())
    perturbations = json.loads(
        (INSTANCES / f"perturbations/{instance_id}-c2.json").read_text()
    )
    c3 = json.loads((INSTANCES / f"compliance/{instance_id}-c3.json").read_text())

    run_started = time.strftime("%Y-%m-%dT%H:%M:%S")
    results = {
        "instance_id": instance["instance_id"],
        "source_case": instance["source_case"],
        "model_alias": MODEL,
        "model_resolved_at_run_time": None,  # filled in from first response
        "harness_version": "eval/run_cabral_pilot.py v0.1",
        "harness_caveat": (
            "Single-temperature single-sample evaluation. The claude CLI does not "
            "expose temperature control, so ensemble and calibration measurements "
            "are deferred. The C0/C2/C3 comparison is still measurable; "
            "temperature-robustness (C8) is not."
        ),
        "run_started": run_started,
        "dry_run": dry_run,
        "conditions": {},
    }

    # C0 base
    print("[C0] building base integration prompt...", flush=True)
    c0_prompt = build_c0_prompt(instance)
    print(f"[C0] calling model (dry_run={dry_run})...", flush=True)
    c0_resp = call_model(c0_prompt, dry_run=dry_run)
    if not dry_run and results["model_resolved_at_run_time"] is None:
        results["model_resolved_at_run_time"] = c0_resp.get("model") or "unknown"
        results["backend"] = c0_resp.get("backend", BACKEND)

    print("[C0] direct probe for collapsed-to factor...", flush=True)
    probe_prompt = build_direct_probe_prompt(instance)
    probe_resp = call_model(probe_prompt, dry_run=dry_run)
    results["conditions"]["C0"] = {
        "prompt": c0_prompt,
        "answer": c0_resp.get("result", ""),
        "direct_probe_prompt": probe_prompt,
        "direct_probe_answer": probe_resp.get("result", ""),
        "cost_usd": (c0_resp.get("total_cost_usd", 0) or 0) + (probe_resp.get("total_cost_usd", 0) or 0),
    }

    # C2 weight-perturbations
    for p in perturbations["perturbations"]:
        label = p["variant_id"]
        print(f"[{label}] perturbing {p['perturbed_factor_id']} "
              f"({p['perturbed_factor_type']})...", flush=True)
        c2_prompt = build_c2_prompt(instance, p)
        c2_resp = call_model(c2_prompt, dry_run=dry_run)

        # Reconstruction check: strip the QUESTION block and ask if anything is missing
        case_section = c2_prompt.split("QUESTION:")[0].strip()
        recon_prompt = build_reconstruction_check_prompt(case_section)
        recon_resp = call_model(recon_prompt, dry_run=dry_run)

        # Direct probe on the perturbed instance
        probe_variant_prompt = build_direct_probe_prompt({
            **instance,
            "factors": [
                {**f, "text": p["neutral_rewrite"]} if f["factor_id"] == p["perturbed_factor_id"] else f
                for f in instance["factors"]
            ],
        })
        probe_variant_resp = call_model(probe_variant_prompt, dry_run=dry_run)

        recon_answer = recon_resp.get("result", "")
        disqualified = _is_reconstruction_flagged(recon_answer)
        results["conditions"][label] = {
            "perturbed_factor_id": p["perturbed_factor_id"],
            "perturbed_factor_type": p["perturbed_factor_type"],
            "base_weight": p["base_weight"],
            "base_directionality": p["base_directionality"],
            "is_stub": p.get("is_stub_factor", False),
            "prompt": c2_prompt,
            "answer": c2_resp.get("result", ""),
            "direct_probe_answer": probe_variant_resp.get("result", ""),
            "reconstruction_check_prompt": recon_prompt,
            "reconstruction_check_answer": recon_answer,
            "disqualified_by_reconstruction": disqualified,
            "cost_usd": sum(
                (r.get("total_cost_usd", 0) or 0)
                for r in (c2_resp, recon_resp, probe_variant_resp)
            ),
        }

    # C3 compliance
    print("[C3] compliance checklist...", flush=True)
    c3_prompt = build_c3_prompt(instance, c3)
    c3_resp = call_model(c3_prompt, dry_run=dry_run)
    results["conditions"]["C3"] = {
        "prompt": c3_prompt,
        "answer": c3_resp.get("result", ""),
        "cost_usd": c3_resp.get("total_cost_usd", 0) or 0,
    }

    total_cost = sum((c.get("cost_usd", 0) or 0) for c in results["conditions"].values())
    results["total_cost_usd"] = round(total_cost, 4)
    results["run_finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    return results


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run = "--dry-run" in sys.argv
    instance_id = args[0] if args else "facet-neg-0003"

    results = run_pilot(instance_id=instance_id, dry_run=dry_run)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    suffix = "dry-run" if dry_run else "real"
    backend_tag = BACKEND if BACKEND != "claude" else ""  # omit for claude to preserve existing naming
    model_tag = MODEL.replace("/", "-").replace(":", "-")
    effort_tag = f"-effort-{EFFORT}" if EFFORT else ""
    parts = [instance_id, suffix]
    if backend_tag:
        parts.append(backend_tag)
    parts.append(model_tag)
    if effort_tag:
        parts.append(effort_tag.lstrip("-"))
    parts.append(stamp)
    out_path = RESULTS / (f"{'-'.join(parts)}.json" if backend_tag else f"{instance_id}-{suffix}-{model_tag}{effort_tag}-{stamp}.json")
    out_path.write_text(json.dumps(results, indent=2))

    print(f"\nResults: {out_path.relative_to(ROOT)}")
    print(f"Total cost: ${results.get('total_cost_usd', 0):.4f}")
    print(f"Conditions run: {len(results['conditions'])}")
    if not dry_run:
        print(f"Model: {results.get('model_resolved_at_run_time')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
