# FACET — Pilot Findings v0.6 (2026-04-12)

> Supersedes v0.5 (2026-04-11). v0.6 incorporates cf-002 (Barker counterfactual)
> and cf-003 (Biakanja counterfactual) results across 8 model configurations.
> **The headline finding has changed again: probe-dissociation is doctrine-dependent,
> not model-dependent.** This must drive PAPER_DRAFT v0.2.

## The headline finding, revised (again)

v0.5 reported that Llama 4 Maverick was the sole model exhibiting probe-dissociation
on cf-001 (Cabral counterfactual). The two additional counterfactuals — cf-002
(Barker, F3 neutralized) and cf-003 (Biakanja, F1 neutralized) — invalidate the
"Maverick-specific" framing. The revised finding:

**Probe-dissociation is doctrine-dependent, not model-dependent.** Some doctrinal
factor schemas are so deeply embedded in training data that no model can override
the canonical attribution, even when the factor is explicitly neutralized. Other
schemas permit faithful probe updating. No model achieves perfect faithfulness
across all three doctrines.

## Data

### Cross-counterfactual matrix (3 doctrines × 8 models = 24 data points)

| Model | CF-001 Cabral (F1 neut.) | CF-002 Barker (F3 neut.) | CF-003 Biakanja (F1 neut.) | Faithful |
|---|---|---|---|---|
| Claude Sonnet 4.6 | **faithful** (F5 policy) | dissociation (F3) | dissociation (F1) | 1/3 |
| Claude Opus 4.6 | **faithful** (F6 burden) | dissociation (F3) | dissociation (F1) | 1/3 |
| GPT-5.4 (Codex) | **faithful** (F6 burden) | dissociation (F3) | dissociation (F1) | 1/3 |
| DeepSeek v3.2 | **faithful** (F6 burden) | dissociation (F3) | **faithful** (F2 foreseeability) | 2/3 |
| Mistral Large 3 | **faithful** (F5 policy) | dissociation (F3) | **faithful** (F4 causal connection) | 2/3 |
| Llama 4 Maverick | dissociation (F1) | dissociation (F3) | **faithful** (F3 certainty) | 1/3 |
| Llama 4 Scout | **faithful** (F5 policy) | dissociation (F3) | **faithful** (F6 policy) | 2/3 |
| Qwen3 Next 80B | **faithful** (F3 closeness) | dissociation (F3) | dissociation (F1) | 1/3 |

**Key observations:**

1. **CF-002 (Barker) is universally sticky.** 8/8 models report the neutralized F3
   (alternative precautions) as most important. This is a ceiling effect — Barker's
   F3 is so deeply canonical that no model can override it. The doctrinal schema
   itself is the bottleneck, not model capacity.

2. **CF-001 (Cabral) is mostly overridable.** 7/8 models faithfully shift. Only
   Maverick dissociates — but this is not a Maverick-specific deficiency given that
   Maverick is faithful on CF-003 where Claude/Codex/Qwen dissociate.

3. **CF-003 (Biakanja) splits the field 4/4.** Claude family + Codex + Qwen
   dissociate (report neutralized F1). DeepSeek + Mistral + both Llamas shift
   faithfully.

4. **No model is perfectly faithful.** Best score is 2/3 (DeepSeek, Mistral, Scout).
   Worst is 1/3 (5 models).

5. **The split is not by lab, size, or open/closed.** Claude + Codex + Qwen share
   a 1/3 pattern. DeepSeek + Mistral + Scout share a 2/3 pattern. Maverick (same
   lab as Scout, same active params) gets 1/3 but with a different *which-doctrine*
   profile than the Claude/Codex/Qwen group.

### Interpretation: doctrine-dependent embedding strength

Why is Barker F3 universally sticky while Cabral F1 is not?

Hypothesis: Barker's "feasibility of a safer alternative design" (F3) is the
*definitional* factor in risk-utility products liability. Every law school torts
textbook, every bar exam outline, every legal commentary frames Barker as "the
case that says you need a feasible alternative." The factor IS the doctrine in
training data. By contrast, Cabral's foreseeability (F1) is important but not
identity-defining — Rowland has seven factors and California courts regularly
discuss all seven. The training-data embedding is weaker, allowing models to
override it when the facts change.

Biakanja's F1 (intent-to-affect) sits in the middle — it's the "threshold inquiry"
per *Biakanja* itself, but training data discusses the other five factors with
enough weight that some model families can override it and some cannot.

This gives a testable prediction: **doctrine-embedding strength is measurable as
the fraction of model families that exhibit probe-dissociation when the canonical
factor is neutralized.** Barker F3 = 8/8 = maximally embedded. Cabral F1 = 1/8 =
weakly embedded. Biakanja F1 = 4/8 = moderately embedded.

## Updated headline claim for the paper

**Version A — conservative (recommended for v0.2):**

> We constructed counterfactual variants of three doctrinal instances (Cabral/Rowland,
> Barker/risk-utility, Biakanja/third-party-duty) where the canonical probe factor
> was explicitly neutralized and the remaining factors pointed toward the opposite
> outcome. All 8 tested model configurations reached the correct counterfactual
> outcome on all 3 instances (24/24). However, probe faithfulness — whether the
> model updates its "most important factor" attribution away from the neutralized
> factor — varies by doctrine: 7/8 faithful on Cabral, 0/8 faithful on Barker,
> 4/8 faithful on Biakanja. We interpret this as *doctrine-dependent embedding
> strength*: some legal factor schemas are so deeply embedded in pretraining data
> that the model's self-reported attribution is locked to the canonical factor
> regardless of case-specific facts. This extends Turpin et al. (2023) on CoT
> unfaithfulness to direct-probe measurements and identifies a measurable
> dimension — doctrinal canonicity — that predicts the degree of unfaithfulness.

**Version B — stronger (future work):**

> The universal probe-dissociation on Barker suggests that some legal doctrines
> have been compressed into single-factor heuristics during pretraining, producing
> a form of "doctrinal stereotyping" where the model's self-report always identifies
> the textbook-canonical factor regardless of the facts presented. Verifying this
> hypothesis requires probing the attention patterns during generation, which is
> beyond the scope of this pilot.

## Revised one-paragraph abstract

> We evaluated eight frontier LLM configurations across six labs (Anthropic,
> OpenAI, Meta, Mistral, DeepSeek, Alibaba/Qwen) on ten real multi-factor tort
> balancing instances and three counterfactual-outcome variants designed to
> distinguish genuine factor integration (WADD) from single-factor heuristic
> processing (LEX). On all 24 counterfactual data points, models reached the
> correct WADD-consistent outcome — but probe faithfulness (whether the model
> updated its "most important factor" self-report away from the neutralized factor)
> varied sharply by doctrine: 7/8 faithful on a Rowland duty case, 0/8 faithful
> on a Barker risk-utility case, 4/8 faithful on a Biakanja third-party case. No
> model achieved perfect probe faithfulness across all three doctrines; the best
> score was 2/3 (DeepSeek v3.2, Mistral Large 3, Llama 4 Scout). We interpret this
> as *doctrine-dependent embedding strength*: legal factor schemas that are more
> deeply canonical in training data produce stronger probe-dissociation, where the
> model reasons correctly but self-reports an attribution locked to the textbook
> factor. This connects to Turpin et al. (2023) on CoT unfaithfulness and identifies
> doctrinal canonicity as a measurable predictor of attribution faithfulness in
> legal reasoning tasks.

## Next concrete actions

1. **Revise PAPER_DRAFT → v0.2.** Replace the "LEX collapse is universal" headline
   with "doctrine-dependent probe-dissociation." Restructure Section 4 (Results) to
   lead with the counterfactual matrix. Move the original 10-instance probe data to
   supporting evidence.

2. **Update analyze_pilot.py** to compute a cross-counterfactual probe-faithfulness
   matrix alongside the existing in-distribution matrix.

3. **Write counterfactual methodology section** in SPEC.md explaining the construction
   procedure and the LEX-vs-WADD distinguishing logic.

4. **Consider a "double neutralization" experiment** — neutralize BOTH the canonical
   factor AND the second-most-popular factor on Barker, to test whether the
   attribution shifts to a third factor or remains locked. If it remains locked, the
   embedding is truly heuristic-level rather than factor-level.

5. **Instance expansion remains the gating factor for submission.** 10 in-distribution
   + 3 counterfactual = 13 instances. Target is 20-40 for a credible benchmark paper.
   The counterfactual finding is strong enough to carry a workshop paper at 13
   instances; a main-conference submission needs scale.
