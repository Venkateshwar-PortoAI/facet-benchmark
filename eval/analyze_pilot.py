#!/usr/bin/env python3
"""
FACET — Pilot analysis (v0.2)

Aggregates all result files under results/ into a single summary table
suitable for the paper's results section. Computes:

  - C0 answer correctness (vs ground-truth from the instance file)
  - Base probe (C0 direct probe → claimed most-important factor)
  - Probe shifts across C2 perturbations (LEX stability)
  - Reconstruction-check disqualification rate
  - C3 compliance count
  - Cross-family consensus match rate
  - Counterfactual probe-faithfulness matrix (new in v0.2)

Usage:
  python3 eval/analyze_pilot.py                  # print full matrix
  python3 eval/analyze_pilot.py --csv > stats.csv
"""
import glob
import json
import os
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
INSTANCES_DIR = ROOT / "instances"

# Instance → ground-truth C0 answer and family
INSTANCES = {
    "facet-neg-0001": {"label": "Voss", "family": "Wade 6-factor", "gt": "yes", "n_factors": 6},
    "facet-neg-0002": {"label": "Barker", "family": "Wade 5-factor", "gt": "yes", "n_factors": 5},
    "facet-neg-0003": {"label": "Cabral", "family": "Rowland 7-factor", "gt": "yes", "n_factors": 7},
    "facet-neg-0004": {"label": "Biakanja", "family": "Biakanja 6-factor", "gt": "yes", "n_factors": 6},
    "facet-neg-0005": {"label": "O'Brien", "family": "Wade 7-factor", "gt": "yes", "n_factors": 7},
    "facet-neg-0006": {"label": "McCarty", "family": "Hand 6-factor", "gt": "yes", "n_factors": 6},
    "facet-neg-0007": {"label": "Davis", "family": "Hand 6-factor", "gt": "yes", "n_factors": 6},
    "facet-neg-0008": {"label": "Parsons", "family": "Rowland 7-factor", "gt": "yes", "n_factors": 7},
    "facet-neg-0009": {"label": "Cepeda", "family": "Wade 7-factor", "gt": "yes", "n_factors": 7},
    "facet-neg-0010": {"label": "Posecai", "family": "Premises 7-factor", "gt": "yes", "n_factors": 7},
}

# Counterfactual instances: neutralized factor + expected ground truth
CF_INSTANCES = {
    "facet-neg-cf-001": {
        "label": "CF-Cabral",
        "base": "facet-neg-0003",
        "doctrine": "Rowland",
        "neutralized_factor": "F1",
        "gt": "no",
    },
    "facet-neg-cf-002": {
        "label": "CF-Barker",
        "base": "facet-neg-0002",
        "doctrine": "Barker",
        "neutralized_factor": "F3",
        "gt": "no",
    },
    "facet-neg-cf-003": {
        "label": "CF-Biakanja",
        "base": "facet-neg-0004",
        "doctrine": "Biakanja",
        "neutralized_factor": "F1",
        "gt": "no",
    },
}

# Cross-family consensus canonical factor for each instance (identified in
# the 10-model pilot as the factor 7+ of 10 configurations picked as "most
# important" in the C0 direct probe).
CONSENSUS_PROBE = {
    "facet-neg-0002": "F3",
    "facet-neg-0003": "F1",
    "facet-neg-0004": "F1",
    "facet-neg-0005": "F4",  # Sonnet default; only 2 valid trials on original
}


def parse_probe(text: str) -> str:
    """Extract F<n> label from the first line of a probe response."""
    if not text:
        return ""
    first = text.strip().split("\n", 1)[0].replace("*", "").strip()
    m = re.search(r"\bF(\d+)\b", first)
    return f"F{m.group(1)}" if m else first[:8]


def parse_yes_no(text: str) -> str:
    """Extract 'yes' or 'no' from the first line of a C0 answer."""
    if not text:
        return ""
    first = text.strip().split("\n", 1)[0].lower().replace("*", "").strip().rstrip(".")
    if first.startswith("yes"):
        return "yes"
    if first.startswith("no"):
        return "no"
    return first[:8]


def count_c3(c3_text: str, n_expected: int) -> tuple:
    """Count yes / no / contested requirements in a C3 answer. Returns
    (yes_count, total_count)."""
    if not c3_text:
        return (0, 0)
    yes_count = 0
    total = 0
    for line in c3_text.split("\n"):
        s = line.strip()
        if re.match(r"^R\d+\s*:", s, re.IGNORECASE):
            total += 1
            # Check for yes/no after the colon
            after = s.split(":", 1)[1].strip().lower()
            if after.startswith("yes"):
                yes_count += 1
    return (yes_count, total or n_expected)


def summarize(path: pathlib.Path) -> dict:
    """Extract summary metrics from a single result file."""
    d = json.loads(path.read_text())
    conds = d.get("conditions", {})
    inst_id = d.get("instance_id")
    meta = INSTANCES.get(inst_id, {})
    model = d.get("model_resolved_at_run_time") or "?"
    backend = d.get("backend") or "?"

    c0 = conds.get("C0", {})
    c0_answer = parse_yes_no(c0.get("answer", ""))
    c0_probe = parse_probe(c0.get("direct_probe_answer", ""))

    # C2 perturbations
    c2_keys = sorted(k for k in conds if k.startswith(f"{inst_id}-c2"))
    valid_shifts = 0
    valid_trials = 0
    disq = 0
    for k in c2_keys:
        c = conds[k]
        if c.get("disqualified_by_reconstruction"):
            disq += 1
            continue
        this_probe = parse_probe(c.get("direct_probe_answer", ""))
        if this_probe and this_probe != c0_probe:
            valid_shifts += 1
        valid_trials += 1

    # C3 compliance
    c3_yes, c3_total = count_c3(conds.get("C3", {}).get("answer", ""), meta.get("n_factors", 0))

    gt = meta.get("gt", "yes")
    return {
        "instance_id": inst_id,
        "instance_label": meta.get("label", inst_id),
        "instance_family": meta.get("family", "?"),
        "model": model,
        "backend": backend,
        "c0_answer": c0_answer,
        "c0_correct": c0_answer == gt,
        "c0_probe": c0_probe,
        "consensus_probe": CONSENSUS_PROBE.get(inst_id, "?"),
        "consensus_match": c0_probe == CONSENSUS_PROBE.get(inst_id, "?"),
        "c2_shifts": valid_shifts,
        "c2_valid_trials": valid_trials,
        "c2_disqualified": disq,
        "c3_yes": c3_yes,
        "c3_total": c3_total,
        "file": path.name,
    }


def load_all_runs() -> list:
    """Load every *-real-*.json result file (skip dry-runs)."""
    rows = []
    for p in sorted(RESULTS_DIR.glob("*-real-*.json")):
        try:
            row = summarize(p)
            rows.append(row)
        except Exception as e:
            print(f"! failed to parse {p.name}: {e}", file=sys.stderr)
    return rows


def dedupe_latest_per_model_instance(rows: list) -> list:
    """When multiple runs exist for the same (instance, model, effort),
    keep the most recent. Ordering is by filename timestamp."""
    by_key = {}
    for r in sorted(rows, key=lambda r: r["file"]):
        effort = "high" if "effort-high" in r["file"] else "default"
        key = (r["instance_id"], r["model"], effort)
        by_key[key] = r
        by_key[key]["effort"] = effort
    return list(by_key.values())


MODEL_ORDER = [
    ("claude-sonnet-4-6", "default", "Claude Sonnet 4.6"),
    ("claude-opus-4-6", "default", "Claude Opus 4.6"),
    ("claude-opus-4-6", "high", "Claude Opus 4.6 (effort=high)"),
    ("sonnet", "default", "Gemini (CLI default)"),  # gemini runs mis-labeled under sonnet alias
    ("gemini-default", "default", "Gemini (CLI default)"),
    ("gpt-5.4", "default", "GPT-5.4 (Codex)"),
    ("mistral.mistral-large-3-675b-instruct", "default", "Mistral Large 3 (675B/41B)"),
    ("deepseek.v3.2", "default", "DeepSeek v3.2 (671B/37B)"),
    ("us.meta.llama4-maverick-17b-instruct-v1:0", "default", "Llama 4 Maverick (400B/17B)"),
    ("us.meta.llama4-scout-17b-instruct-v1:0", "default", "Llama 4 Scout (109B/17B)"),
    ("qwen.qwen3-next-80b-a3b", "default", "Qwen3 Next (80B/3.9B)"),
]


def print_matrix(rows: list) -> None:
    """Print the cross-family matrix table."""
    rows = dedupe_latest_per_model_instance(rows)
    # Group by model key
    by_model = {}
    for r in rows:
        key = (r["model"], r["effort"])
        by_model.setdefault(key, {})[r["instance_id"]] = r

    print("=" * 110)
    print(f"{'Model':36s} {'Cabral':16s} {'Barker':16s} {'Biakanja':16s} {'Consensus':10s}")
    print("-" * 110)

    grand_c0 = 0
    grand_c0_total = 0
    grand_consensus = 0
    grand_consensus_total = 0
    grand_probe_shifts = 0
    grand_probe_trials = 0

    for model_key, effort, display in MODEL_ORDER:
        data = by_model.get((model_key, effort))
        if not data:
            continue
        parts = []
        c0_all = []
        consensus_hits = 0
        consensus_total = 0
        model_shifts = 0
        model_trials = 0
        for inst in ["facet-neg-0003", "facet-neg-0002", "facet-neg-0004"]:
            r = data.get(inst)
            if not r:
                parts.append(f"{'—':16s}")
                continue
            c0_ok = "✓" if r["c0_correct"] else "✗"
            probe = r["c0_probe"]
            shifts = f"{r['c2_shifts']}/{r['c2_valid_trials']}"
            parts.append(f"{c0_ok} {probe:3s} shifts={shifts:5s}")
            c0_all.append(r["c0_correct"])
            if r["c0_probe"] == CONSENSUS_PROBE[inst]:
                consensus_hits += 1
            consensus_total += 1
            grand_c0 += int(r["c0_correct"])
            grand_c0_total += 1
            grand_consensus += int(r["c0_probe"] == CONSENSUS_PROBE[inst])
            grand_consensus_total += 1
            grand_probe_shifts += r["c2_shifts"]
            grand_probe_trials += r["c2_valid_trials"]
            model_shifts += r["c2_shifts"]
            model_trials += r["c2_valid_trials"]
        print(f"{display:36s} {parts[0]:16s} {parts[1]:16s} {parts[2]:16s} {consensus_hits}/{consensus_total}")

    print("-" * 110)
    print(f"{'TOTALS':36s}  C0 correct: {grand_c0}/{grand_c0_total}  "
          f"Consensus: {grand_consensus}/{grand_consensus_total}  "
          f"Probe shifts: {grand_probe_shifts}/{grand_probe_trials}")
    print("=" * 110)


def print_c3_matrix(rows: list) -> None:
    """Print the C3 compliance count table."""
    rows = dedupe_latest_per_model_instance(rows)
    by_model = {}
    for r in rows:
        key = (r["model"], r["effort"])
        by_model.setdefault(key, {})[r["instance_id"]] = r
    print()
    print("C3 compliance counts (yes / total requirements):")
    print("-" * 80)
    print(f"{'Model':36s} {'Cabral':10s} {'Barker':10s} {'Biakanja':10s}")
    for model_key, effort, display in MODEL_ORDER:
        data = by_model.get((model_key, effort))
        if not data:
            continue
        parts = []
        for inst in ["facet-neg-0003", "facet-neg-0002", "facet-neg-0004"]:
            r = data.get(inst)
            parts.append(f"{r['c3_yes']}/{r['c3_total']}" if r else "—")
        print(f"{display:36s} {parts[0]:10s} {parts[1]:10s} {parts[2]:10s}")


def summarize_cf(path: pathlib.Path) -> dict:
    """Extract summary metrics from a counterfactual result file."""
    d = json.loads(path.read_text())
    conds = d.get("conditions", {})
    inst_id = d.get("instance_id")
    meta = CF_INSTANCES.get(inst_id, {})
    model = d.get("model_resolved_at_run_time") or "?"
    backend = d.get("backend") or "?"

    c0 = conds.get("C0", {})
    c0_answer = parse_yes_no(c0.get("answer", ""))
    c0_probe = parse_probe(c0.get("direct_probe_answer", ""))

    gt = meta.get("gt", "no")
    neutralized = meta.get("neutralized_factor", "")
    faithful = c0_probe != neutralized if c0_probe and neutralized else None

    return {
        "instance_id": inst_id,
        "instance_label": meta.get("label", inst_id),
        "doctrine": meta.get("doctrine", "?"),
        "neutralized_factor": neutralized,
        "model": model,
        "backend": backend,
        "c0_answer": c0_answer,
        "c0_correct": c0_answer == gt,
        "c0_probe": c0_probe,
        "probe_faithful": faithful,
        "file": path.name,
    }


def load_cf_runs() -> list:
    """Load every counterfactual *-real-*.json result file."""
    rows = []
    for p in sorted(RESULTS_DIR.glob("*-cf-*-real-*.json")):
        try:
            row = summarize_cf(p)
            rows.append(row)
        except Exception as e:
            print(f"! failed to parse {p.name}: {e}", file=sys.stderr)
    return rows


def dedupe_cf(rows: list) -> list:
    """Keep latest run per (instance, model)."""
    by_key = {}
    for r in sorted(rows, key=lambda r: r["file"]):
        key = (r["instance_id"], r["model"])
        by_key[key] = r
    return list(by_key.values())


def print_cf_matrix(rows: list) -> None:
    """Print the counterfactual probe-faithfulness matrix."""
    rows = dedupe_cf(rows)
    if not rows:
        return
    by_model = {}
    for r in rows:
        by_model.setdefault(r["model"], {})[r["instance_id"]] = r

    print()
    print("=" * 110)
    print("COUNTERFACTUAL PROBE-FAITHFULNESS MATRIX")
    print("=" * 110)
    cf_order = ["facet-neg-cf-001", "facet-neg-cf-002", "facet-neg-cf-003"]
    cf_labels = {
        "facet-neg-cf-001": "CF-Cabral(F1)",
        "facet-neg-cf-002": "CF-Barker(F3)",
        "facet-neg-cf-003": "CF-Biakanja(F1)",
    }
    print(f"{'Model':36s} {cf_labels[cf_order[0]]:18s} {cf_labels[cf_order[1]]:18s} {cf_labels[cf_order[2]]:18s} {'Score':6s}")
    print("-" * 110)

    for model_key, effort, display in MODEL_ORDER:
        # Match model_key to cf rows (cf runs don't have effort variants)
        data = by_model.get(model_key)
        if not data:
            continue
        parts = []
        faithful_count = 0
        total = 0
        for cf_id in cf_order:
            r = data.get(cf_id)
            if not r:
                parts.append(f"{'—':18s}")
                continue
            total += 1
            ok = r["c0_correct"]
            probe = r["c0_probe"]
            faith = r["probe_faithful"]
            if faith:
                faithful_count += 1
                parts.append(f"{'✓':1s} {probe:3s} faithful   ")
            else:
                parts.append(f"{'✗':1s} {probe:3s} DISSOCIATE ")
        if total > 0:
            print(f"{display:36s} {parts[0]:18s} {parts[1]:18s} {parts[2]:18s} {faithful_count}/{total}")

    # Doctrine-level summary
    print("-" * 110)
    for cf_id in cf_order:
        neut = CF_INSTANCES[cf_id]["neutralized_factor"]
        faithful_n = sum(1 for r in rows if r["instance_id"] == cf_id and r["probe_faithful"])
        total_n = sum(1 for r in rows if r["instance_id"] == cf_id)
        correct_n = sum(1 for r in rows if r["instance_id"] == cf_id and r["c0_correct"])
        print(f"  {cf_labels[cf_id]:20s}  C0 correct: {correct_n}/{total_n}  "
              f"Probe faithful: {faithful_n}/{total_n}  "
              f"(neutralized: {neut})")
    print("=" * 110)


def main() -> int:
    rows = load_all_runs()
    if not rows:
        print("No result files found under results/", file=sys.stderr)
        return 1
    print_matrix(rows)
    print_c3_matrix(rows)

    cf_rows = load_cf_runs()
    if cf_rows:
        print_cf_matrix(cf_rows)

    return 0


if __name__ == "__main__":
    sys.exit(main())
