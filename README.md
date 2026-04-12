# FACET — Factor Accessibility, Coverage, and Evidence Test

**Measuring Attribution Faithfulness in Multi-Factor LLM Reasoning**

Venkateshwar Reddy Jambula — Pranaalpha Labs

---

## What is FACET?

When LLMs are deployed in domains that require weighing 5–10 different factors simultaneously — medical diagnosis, regulatory compliance, legal balancing tests — do they actually integrate all the factors, or do they collapse onto whichever one is most canonical in their training data?

FACET answers this with a **counterfactual-outcome protocol**: neutralize the canonical factor, flip the remaining factors to the opposite direction, and measure whether the model's self-reported factor attribution updates to reflect the new case. We instantiate FACET on US tort law because legal balancing tests have explicit factor lists, verifiable ground truth, and naturally varying canonicity.

## Key Finding

We evaluate 9 frontier model configurations from 6 labs (Anthropic, OpenAI, Meta, Mistral, DeepSeek, Alibaba/Qwen) on 10 real tort cases and 3 counterfactual variants. **All models reach the correct outcome on counterfactuals, but probe faithfulness varies sharply by how canonical the factor is:**

| Counterfactual | Neutralized Factor | Canonicity | Models with Faithful Probe |
|---|---|---|---|
| CF-Cabral (Rowland duty) | F1 foreseeability | moderate | **7/8** |
| CF-Barker (risk-utility) | F3 feasibility of safer alternative | high | **0/8** |
| CF-Biakanja (third-party) | F1 intent-to-affect | intermediate | **4/8** |

**The more textbook-canonical the factor, the less trustworthy the model's self-report.** Barker's F3 is so deeply embedded in training data that every model reports it as "most important" even when the prompt explicitly says no such factor exists in the case.

## Repository Structure

```
facet-benchmark/
├── README.md                # This file
├── LICENSE                  # MIT (code)
├── LICENSE-DATA             # CC BY 4.0 (data)
├── factor_type_taxonomy.md  # Factor type definitions (schema reference)
├── eval/
│   ├── run_cabral_pilot.py  # 5-backend evaluation harness
│   ├── analyze_pilot.py     # Reproduces the tables from raw results
│   ├── gen_c2_c3.py         # Generates C2 perturbation and C3 compliance variants
│   └── requirements.txt
├── instances/               # Benchmark dataset
│   ├── facet-neg-00NN.json  # 10 in-distribution instances
│   ├── facet-neg-cf-00N.json # 3 counterfactual variants
│   ├── perturbations/       # C2 weight-perturbation variants
│   └── compliance/          # C3 compliance-matched variants
└── results/                 # Raw model output JSON (~100 files)
```

## Reproducing the Results

```bash
# Install dependencies
pip install -r eval/requirements.txt

# Regenerate the cross-family matrix from raw results
python3 eval/analyze_pilot.py
```

## Running New Models

The harness dispatches to five backends:

| Backend | Models supported |
|---|---|
| **Anthropic CLI** | Claude Sonnet, Opus, extended thinking |
| **OpenAI Codex CLI** | GPT-5.4 |
| **AWS Bedrock** | DeepSeek, Mistral, Llama 4, Qwen3 (via Converse API) |
| **Google Gemini CLI** | Gemini (removed from default due to quota limits) |
| **Ollama** | Local models |

```bash
python3 eval/run_cabral_pilot.py --instance facet-neg-0002 --backend anthropic --model claude-opus-4-6
```

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

| Model | Parameters | Probe Faithfulness |
|---|---|---|
| Claude Sonnet 4.6 | undisclosed | 1/3 |
| Claude Opus 4.6 | undisclosed | 1/3 |
| Claude Opus 4.6 (extended thinking) | undisclosed | 1/3 |
| GPT-5.4 | undisclosed | 1/3 |
| DeepSeek v3.2 | 671B / 37B active | 2/3 |
| Mistral Large 3 | 675B / 41B active | 2/3 |
| Llama 4 Maverick | 400B / 17B active | 1/3 |
| Llama 4 Scout | 109B / 17B active | 2/3 |
| Qwen3 Next 80B-A3B | 80B / 3.9B active | 1/3 |

## Status

This is a **pilot study**. The benchmark protocol is domain-general; legal balancing tests are the first instantiation. Medical differential diagnosis and multi-criteria compliance review are planned extensions.

**Known limitations:**
- 13 instances is pilot scale; expansion to 20–40 is planned
- Factor definitions and weights are sourced from secondary legal digests; verification against primary opinion texts is ongoing
- Single-temperature, single-sample evaluation
- California-only instances
- Counterfactual ground truth is author-declared (synthetic counterfactuals cannot be adjudicated)

## Paper

A pilot study describing the benchmark protocol, findings, and full methodology is available on SSRN (link forthcoming).

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

- **Code** (everything in `eval/`): MIT License — see [LICENSE](LICENSE)
- **Data** (everything in `instances/` and `results/`): CC BY 4.0 — see [LICENSE-DATA](LICENSE-DATA)

## Contact

Venkateshwar Reddy Jambula — venkateshwar.jambula@pranaalpha.com
