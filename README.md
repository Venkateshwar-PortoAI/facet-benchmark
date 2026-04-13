# FACET

**Measuring Attribution Faithfulness in Multi-Factor LLM Reasoning**

[![Verify paper numbers](https://github.com/pranaalpha/facet-benchmark/actions/workflows/verify-paper.yml/badge.svg)](https://github.com/pranaalpha/facet-benchmark/actions/workflows/verify-paper.yml)

Venkateshwar Reddy Jambula, Pranaalpha Labs  ·  [Paper (PDF)](PAPER_ARXIV_v3.pdf)  ·  [Cover note](VC_COVER_NOTE.md)

---

## The finding in one figure

![Probe format determines apparent attribution faithfulness](figures/fig1_probe_comparison.png)

On the same 8 frontier models and the same 3 counterfactual legal cases, two probes give contradictory answers:

- **Single-factor probe** ("which one factor is most important?"): **0 of 8 models** are faithful on CF-Barker.
- **Weighted-rank probe** ("assign percentage weights to all N factors"): **8 of 8 models** are faithful on the same case.

The reasoning was WADD-consistent the whole time. The single-factor probe was compressing it to look lexicographic. **The probe format, not the model, drives the apparent failure.**

This matters because forced-choice attribution probes (top-1, top-k) are the dominant format in current LLM explainability tooling. If FACET generalizes, those probes are systematically under-reporting distributed reasoning.

---

## Reproduce in 60 seconds

```bash
git clone https://github.com/pranaalpha/facet-benchmark && cd facet-benchmark
pip install -r eval/requirements.txt

# Regenerate Table 2 and Table 3 from the raw JSON outputs in results/
python3 eval/analyze_pilot.py
python3 eval/analyze_weighted_probe.py

# Mechanically verify every numeric claim in the paper against the raw data
python3 eval/verify_paper_numbers.py
```

The last command re-derives every number in the paper from `results/*.json` and prints `PASS`/`FAIL` for each. Current state: **80/80 PASS**. This runs automatically on every push via the CI badge above.

---

## What's in the repo

| Path | What |
|---|---|
| [`PAPER_ARXIV_v3.pdf`](PAPER_ARXIV_v3.pdf) | The paper (14 pages) |
| [`instances/`](instances/) | 10 in-distribution legal cases + 3 counterfactual variants + adversarial rewrites + C2 perturbations |
| [`results/weighted-probe/`](results/weighted-probe/) | Raw JSON outputs from all probe runs (~350 files) |
| [`eval/`](eval/) | Probe harnesses + analysis scripts + numeric verifier |
| [`figures/`](figures/) | Generated from raw JSON by scripts in `eval/` |
| [`factor_type_taxonomy.md`](factor_type_taxonomy.md) | 17-type doctrinal taxonomy |
| [`SPEC.md`](SPEC.md) | Full methodology blueprint (pilot implements a subset) |

---

## The four probes

1. **P1 (single-factor):** "Which one factor is most important?" Top-1 attribution.
2. **P2 (cued weighted-rank):** "Assign percentages to all N factors summing to 100." Distributed attribution with the factor list given.
3. **P3 (adversarial weighted-rank):** Same as P2, but on adversarially-rewritten counterfactuals where the neutralization uses no syntactic cue words.
4. **C2 (per-factor ablation):** Rewrite one factor at a time as neutral; measure whether the model's weight on that factor drops.

Each probe catches a different failure mode. The paper shows the profile is asymmetric across model families.

---

## Models evaluated

| Model | Provider | Parameters (reported) |
|---|---|---|
| Claude Sonnet 4.6 | Anthropic | undisclosed |
| Claude Opus 4.6 | Anthropic | undisclosed |
| GPT-5.4 | OpenAI | undisclosed |
| DeepSeek v3.2 | Bedrock | 671B / 37B active |
| Mistral Large 3 | Bedrock | 675B / 41B active |
| Llama 4 Maverick | Bedrock | 400B / 17B active |
| Llama 4 Scout | Bedrock | 109B / 17B active |
| Qwen3 Next 80B-A3B | Bedrock | 80B / 3.9B active |

Closed-source models are evaluated via vendor APIs at default temperature; open-weight Bedrock models at `T=0`. All harnesses are single-sample, tool-use disabled.

---

## Running new models

```bash
# P1 single-factor probe
FACET_BACKEND=claude FACET_MODEL=opus python3 eval/run_cabral_pilot.py

# P2 / P3 weighted-rank probe (single instance)
python3 eval/run_weighted_probe.py --instance facet-neg-cf-002 --backend claude --model opus

# Full batch sweep across all 8 models × 3 counterfactuals
bash eval/batch_weighted_probe.sh
```

Supported backends: `claude` (Anthropic CLI), `codex` (OpenAI CLI), `bedrock` (AWS Converse API), `ollama` (local), `gemini` (optional).

---

## Key numbers

| Metric | Value |
|---|---|
| Frontier model configurations evaluated | 8 |
| Labs represented | 6 |
| In-distribution legal cases | 10 |
| Counterfactual variants | 3 (+ 4 adversarial rewrites) |
| Total C2 ablation trials | 144 |
| Raw JSON output files | 350+ |
| Numeric claims mechanically verified | 80/80 |
| P1 vs P2 McNemar's exact *p* | 2.4×10⁻⁴ |
| GPT-5.4 CF-Cabral family n | 22 |
| GPT-5.4 wrong-outcome rate | 7/22, 95% Wilson CI [16%, 53%] |

---

## Status

This is a **pilot study**. Known limitations (paper §6):

- 13 base instances is pilot scale; the four-probe protocol and harness scale to larger instance sets with no design changes
- Counterfactual ground truth is author-declared (synthetic cases cannot be appellate-adjudicated)
- California tort cases only; cross-jurisdictional replication is future work
- C2 perturbations use the same syntactic cue words that the P3 adversarial probe is designed to remove; cue-free C2 variants are future work
- DeepSeek at Bedrock `T=0` is not fully deterministic in practice

---

## Citation

```bibtex
@unpublished{jambula2026facet,
  title  = {{FACET}: Measuring Attribution Faithfulness in Multi-Factor {LLM} Reasoning},
  author = {Jambula, Venkateshwar Reddy},
  year   = {2026},
  note   = {Preprint},
  url    = {https://github.com/pranaalpha/facet-benchmark}
}
```

## License

- **Code** (`eval/`): MIT — see [LICENSE](LICENSE)
- **Data** (`instances/`, `results/`): CC BY 4.0 — see [LICENSE-DATA](LICENSE-DATA)

## Contact

Venkateshwar Reddy Jambula  ·  venkateshwar.jambula@pranaalpha.com
