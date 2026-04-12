# FACET: Factor Accessibility, Coverage, and Evidence Test

**Doctrine-Dependent Probe Dissociation in Frontier LLM Legal Reasoning**

Venkateshwar Reddy Jambula | Pranaalpha Labs | [Paper (PDF)](PAPER_ARXIV_v1.pdf)

---

## What is FACET?

FACET is a benchmark that measures whether large language models genuinely integrate multiple factors in legal balancing tests or collapse onto a single canonical factor. US tort law requires judges to weigh 5-10 heterogeneous factors simultaneously — FACET tests whether LLMs actually do this or just pick one factor and report the answer it drives.

## Key Finding

We evaluate 9 frontier model configurations from 6 labs (Anthropic, OpenAI, Meta, Mistral, DeepSeek, Alibaba/Qwen) on 10 real tort cases and 3 counterfactual variants. **All models get the right answer, but their self-reported factor attributions are unreliable in a doctrine-dependent way:**

| Counterfactual | Neutralized Factor | Models with Faithful Probe |
|---|---|---|
| Cabral / Rowland (duty) | F1 foreseeability | **7/8** |
| Barker / Risk-Utility (product liability) | F3 safer alternative design | **0/8** |
| Biakanja / Third-Party (duty) | F1 intent-to-affect | **4/8** |

**The more textbook-canonical the factor, the less trustworthy the model's self-report.** Barker's F3 is so deeply embedded in training data that every model reports it as "most important" even when it's explicitly neutralized in the prompt.

## Repository Structure

```
facet-benchmark/
├── instances/              # JSON instance definitions (10 real + 3 counterfactual)
├── results/                # Raw model output JSON (~100 files)
├── eval/
│   ├── run_cabral_pilot.py # 5-backend evaluation harness
│   ├── analyze_pilot.py    # Reproduces all tables from the paper
│   ├── gen_figures.py      # Generates paper figures
│   └── requirements.txt
├── figures/                # Generated figures (PNG)
├── latex/                  # LaTeX source for the paper
├── PHENOMENON.md           # Formal phenomenon definition
├── SPEC.md                 # Benchmark specification
├── PRIOR_ART.md            # Literature review and novelty analysis
├── factor_type_taxonomy.md # Factor type definitions
└── PAPER_ARXIV_v1.pdf      # Preprint PDF
```

## Reproducing Results

```bash
# Install dependencies
pip install -r eval/requirements.txt

# Reproduce the tables from the paper
python3 eval/analyze_pilot.py

# Regenerate figures
python3 eval/gen_figures.py
```

## Models Evaluated

| Model | Parameters | Probe Faithfulness |
|---|---|---|
| Claude Sonnet 4.6 | undisclosed | 1/3 |
| Claude Opus 4.6 | undisclosed | 1/3 |
| GPT-5.4 | undisclosed | 1/3 |
| DeepSeek v3.2 | 671B / 37B active | 2/3 |
| Mistral Large 3 | 675B / 41B active | 2/3 |
| Llama 4 Maverick | 400B / 17B active | 1/3 |
| Llama 4 Scout | 109B / 17B active | 2/3 |
| Qwen3 Next 80B-A3B | 80B / 3.9B active | 1/3 |

## Evaluation Harness

The harness supports five backends:
- **Anthropic** (Claude CLI)
- **OpenAI** (Codex CLI)
- **AWS Bedrock** (DeepSeek, Mistral, Meta, Qwen via Converse API)
- **Google Gemini** (CLI, removed from default due to quota limits)
- **Ollama** (local models)

## Citation

```bibtex
@article{jambula2026facet,
  title={FACET: Doctrine-Dependent Probe Dissociation in Frontier LLM Legal Reasoning},
  author={Jambula, Venkateshwar Reddy},
  year={2026},
  note={Preprint}
}
```

## License

Code: MIT. Instance data and model outputs: CC-BY-4.0.

## Contact

Venkateshwar Reddy Jambula — venkateshwar.jambula@pranaalpha.com
