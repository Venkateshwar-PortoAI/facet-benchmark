# FACET — Factor Accessibility, Coverage, and Evidence Test

**Measuring Attribution Faithfulness in Multi-Factor LLM Reasoning**

Venkateshwar Reddy Jambula — Pranaalpha Labs

---

## What is FACET?

When LLMs are deployed in domains that require weighing 5–10 different factors simultaneously — medical diagnosis, regulatory compliance, legal balancing tests — do they actually integrate all the factors, or do they collapse onto whichever one is most canonical in their training data?

FACET tests this with two probes applied to the same models and cases:

1. **Single-factor probe** — "which single factor is most important?"
2. **Weighted-rank probe** — "assign percentage weights to all N factors, summing to 100"

The two probes give contradictory answers. The single-factor probe shows apparent lexicographic collapse. The weighted-rank probe shows distributed, WADD-consistent weights. **This contradiction is the finding.** Single-factor probes systematically misrepresent LLM multi-factor reasoning.

## Key Results

**Evaluated:** 9 frontier model configurations from 6 labs on 10 real legal balancing cases + 3 counterfactual variants.

### The contradiction at a glance

| Metric | Single-factor probe | Weighted-rank probe |
|---|---|---|
| CF-Cabral faithful models | 7/8 | **8/8** |
| CF-Barker faithful models | **0/8** | **8/8** |
| CF-Biakanja faithful models | 4/8 | **8/8** |
| In-dist: any model with ≥50% weight on one factor | n/a | **0/8** |

Under the single-factor probe, no model shifts its attribution on CF-Barker when the canonical factor is neutralized. Under the weighted-rank probe, every model correctly assigns ≤10% weight to the neutralized factor. The **reasoning was always WADD**; the single-factor probe was compressing it to look LEX.

## Repository Structure

```
facet-benchmark/
├── README.md                 # This file
├── LICENSE                   # MIT (code)
├── LICENSE-DATA              # CC BY 4.0 (data)
├── factor_type_taxonomy.md   # Factor type definitions (dataset schema)
├── eval/
│   ├── run_cabral_pilot.py       # Single-factor probe harness (5 backends)
│   ├── run_weighted_probe.py     # Weighted-rank probe harness (3 backends)
│   ├── batch_weighted_probe.sh   # Batch runner for counterfactual sweep
│   ├── batch_weighted_probe_indist.sh  # Batch runner for in-distribution sweep
│   ├── analyze_pilot.py          # Reproduces single-factor matrix
│   ├── analyze_weighted_probe.py # Reproduces weighted-rank matrix
│   ├── gen_c2_c3.py              # Generates C2 and C3 variants
│   └── requirements.txt
├── instances/                # Benchmark dataset
│   ├── facet-neg-00NN.json   #   10 real in-distribution cases
│   ├── facet-neg-cf-00N.json #   3 counterfactual variants
│   ├── perturbations/        #   C2 weight-perturbation variants
│   └── compliance/           #   C3 compliance-matched variants
└── results/
    ├── facet-neg-*-real-*.json    # Raw single-factor probe outputs
    └── weighted-probe/            # Raw weighted-rank probe outputs
```

## Reproducing the Results

```bash
pip install -r eval/requirements.txt

# Reproduce the single-factor probe matrix (Table 1 & 2 in paper)
python3 eval/analyze_pilot.py

# Reproduce the weighted-rank probe matrix (Table 4 & 5 in paper)
python3 eval/analyze_weighted_probe.py
```

Both scripts read the raw JSON result files in `results/` and print the tables exactly as they appear in the paper.

## Running New Models

### Single-factor probe

```bash
python3 eval/run_cabral_pilot.py  # runs the full C0/C2/C3 protocol
# Environment variables control backend and model:
FACET_BACKEND=claude FACET_MODEL=opus python3 eval/run_cabral_pilot.py
FACET_BACKEND=bedrock FACET_MODEL=deepseek.v3.2 python3 eval/run_cabral_pilot.py
```

### Weighted-rank probe

```bash
# Single run
python3 eval/run_weighted_probe.py --instance facet-neg-cf-002 --backend claude --model opus
python3 eval/run_weighted_probe.py --instance facet-neg-cf-002 --backend bedrock --model deepseek.v3.2
python3 eval/run_weighted_probe.py --instance facet-neg-cf-002 --backend codex --model gpt-5.4

# Full batch across all 8 models × 3 counterfactuals
bash eval/batch_weighted_probe.sh

# Full batch across all 8 models × 3 in-distribution anchors
bash eval/batch_weighted_probe_indist.sh

# Dry-run (prints the prompt without calling the API)
python3 eval/run_weighted_probe.py --instance facet-neg-cf-002 --model opus --dry-run
```

## Backends

| Backend | How it works | Models supported |
|---|---|---|
| **claude** | Anthropic Claude CLI (`claude`) | Claude Sonnet, Opus, extended thinking |
| **codex** | OpenAI Codex CLI (`codex`) | GPT-5.4 |
| **bedrock** | AWS Bedrock Converse API (`aws` CLI) | DeepSeek, Mistral, Llama 4, Qwen3 |
| **ollama** | Local Ollama server | any local model |
| **gemini** | Google Gemini CLI (removed from default due to quota limits) | Gemini |

The harness auto-dispatches from the `--backend` flag or the `FACET_BACKEND` environment variable. Single-temperature, single-sample evaluation; tool use disabled.

## Instance Schema

Each instance JSON contains:

- `instance_id` — unique ID
- `source_case` — citation to the real case
- `doctrine` — doctrinal framework (e.g., `rowland_duty`)
- `case_background` — factual narrative
- `factors[]` — array of factor objects with:
  - `factor_id` — `f1` through `fN`
  - `factor_type` — from `factor_type_taxonomy.md`
  - `text` — the factor statement
  - `directionality` — which party the factor favors
  - `in_case_weight_estimate` — author-estimated weight (sum to ~1.0)
- `question` — the question posed to the model
- `ground_truth` — the appellate holding

Counterfactual instances (`facet-neg-cf-*.json`) additionally mark the neutralized factor with `counterfactual_note: "CFNEUTRALIZED"`.

See `factor_type_taxonomy.md` for the full factor-type vocabulary.

## Models Evaluated

| Model | Parameters | Single-factor probe | Weighted-rank probe |
|---|---|---|---|
| Claude Sonnet 4.6 | undisclosed | 1/3 faithful | **3/3 faithful** |
| Claude Opus 4.6 | undisclosed | 1/3 faithful | **3/3 faithful** |
| GPT-5.4 | undisclosed | 1/3 faithful | **3/3 faithful** |
| DeepSeek v3.2 | 671B / 37B active | 2/3 faithful | **3/3 faithful** |
| Mistral Large 3 | 675B / 41B active | 2/3 faithful | **3/3 faithful** |
| Llama 4 Maverick | 400B / 17B active | 1/3 faithful | **3/3 faithful** |
| Llama 4 Scout | 109B / 17B active | 2/3 faithful | **3/3 faithful** |
| Qwen3 Next 80B-A3B | 80B / 3.9B active | 1/3 faithful | **3/3 faithful** |

Claude Opus 4.6 with extended thinking was included in the single-factor probe arm (identical behavior to default); omitted from the weighted-rank arm for the same reason.

## Status and Limitations

This is a **pilot study**. Key limitations:

- 13 instances (10 + 3 counterfactual) is pilot scale; expansion to 20–40 is in progress
- Counterfactual ground truth is author-declared (synthetic cases cannot be adjudicated)
- Counterfactuals have overwhelming directional signal; decision-boundary variants are future work
- The weighted-rank probe could itself be gamed by a model that learned "assign 0 to neutral-sounding factors"; adversarial probe variants are future work
- Factor definitions and weights are sourced from secondary legal digests; primary-text verification is ongoing
- California-only instances; cross-jurisdictional replication is future work

See the paper §6 for the full limitations list.

## Paper

Preprint on SSRN (link forthcoming) and on GitHub: [PAPER_ARXIV_v2.pdf](PAPER_ARXIV_v2.pdf)

## Citation

```bibtex
@unpublished{jambula2026facet,
  title={{FACET}: Measuring Attribution Faithfulness in Multi-Factor {LLM} Reasoning},
  author={Jambula, Venkateshwar Reddy},
  year={2026},
  note={Preprint},
  url={https://github.com/Venkateshwar-PortoAI/facet-benchmark}
}
```

## License

- **Code** (`eval/`): MIT License — see [LICENSE](LICENSE)
- **Data** (`instances/`, `results/`): CC BY 4.0 — see [LICENSE-DATA](LICENSE-DATA)

## Contact

Venkateshwar Reddy Jambula — venkateshwar.jambula@pranaalpha.com
