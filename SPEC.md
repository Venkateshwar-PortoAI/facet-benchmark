# FACET — Benchmark Specification (v0.1, pre-review)

**Benchmark:** FACET — Factor Accessibility, Coverage, and Evidence Test
**Phenomenon:** multi-factor collapse (see `PHENOMENON.md`)
**Primary domain:** legal balancing tests (see `PHENOMENON.md` §7)
**Status:** draft spec, not yet expert-reviewed. Every design decision in this document is contingent on the face-validity review in `PHENOMENON.md` §10 item 1. Do not start instance construction until that review is complete.
**Last updated:** 2026-04-11

---

## 1. Scope

This document specifies how FACET measures multi-factor collapse. It covers instance format, experimental conditions, measurement protocol, scoring, and dataset requirements. It does **not** cover paper-writing, narrative framing, or downstream analysis beyond what is required to make the measurement defensible.

## 2. Non-goals (repeat from `PHENOMENON.md` §6)

FACET does not measure depth/chain-length failures, constraint compliance, distractor filtering, long-context retrieval, multi-agent pooling, LLM-as-judge rubric collapse, or anchoring. If a design decision below starts pulling the benchmark toward any of these, reject the decision — do not widen scope.

## 3. Primary instance type

*Revised 2026-04-11 after `CASE_CANDIDATES.md` round 1 retrieval.* The round 1 retrieval confirmed that pure Hand-formula cases (*Carroll Towing*, *Conway v. O'Brien*, *Moisan v. Loftus*) are N=3 — below FACET's N≥5 floor — and that the scalable instance supply for multi-factor tort balancing lives in four related but doctrinally distinct pools:

1. **Hand-formula cases extended with sub-factors** — the *Carroll Towing* / *McCarty v. Pheasant Run* / *Davis v. Consolidated Rail* line. Anchor material; usable as primary instances only when the opinion discusses sub-factors beyond B/P/L (typically reaching N=5–6 in 7th Circuit Posner-authored cases).
2. **Rowland-line duty analysis** — *Rowland v. Christian*, 69 Cal. 2d 108 (1968), and its adoption by ~10 state supreme courts. 7 doctrinal factors per case. Largest scalable pool after Wade.
3. **Wade-factor products-liability risk-utility** — *Cepeda v. Cumberland Engineering*, 76 N.J. 152 (1978); *O'Brien v. Muskin*, 94 N.J. 169 (1983); *Voss v. Black & Decker*, 59 N.Y.2d 102 (1983); *Barker v. Lull Engineering*, 20 Cal. 3d 413 (1978). 5–7 factors per case. **The largest scalable pool — 36 states have adopted risk-utility post-1965.**
4. **Restatement (Second) §520 abnormally-dangerous-activity** — 6 doctrinal factors. Smaller pool; most cases collapse to single-factor dominance (see *Indiana Harbor Belt*) and are excluded from the primary dataset.

**Primary instance type is therefore: "multi-factor tort balancing under any of the four doctrinal frameworks above."** The shared structural feature — simultaneous integration of N≥5 heterogeneous factors in a balancing test with ground truth from the appellate holding — is what FACET measures. The factor-type taxonomy (`factor_type_taxonomy.md` v1.1) spans all four frameworks.

**Why this is still a single primary instance type, not four:** the cognitive phenomenon FACET measures (multi-factor collapse) is framework-agnostic. A model that collapses on a Wade-factor product case and a model that collapses on a Rowland-factor duty case are exhibiting the same phenomenon. Treating these as one instance type is the right level of abstraction because it maximizes statistical power and matches the phenomenon's theoretical scope in `PHENOMENON.md` §2.

*Previous v0.1 and v0.2 drafts named Fourth Amendment reasonable-suspicion as primary. That was reversed at v0.2 after round 1 review for ideological-confound and fuzzy-standard reasons; the multi-doctrinal tort balancing approach adopted at v0.3 generalizes the v0.2 Hand-formula-only decision to admit the real instance supply discovered in round 1 retrieval.*

**Why this multi-doctrinal approach survives novelty:** `PRIOR_ART.md` round 3 confirmed that no LLM benchmark exists for Hand-formula negligence or Restatement (Third) Torts; the closest legal-NLP neighbor (Zhang, Grabmair, Gray, & Ashley 2026, arXiv:2510.08710) tests LLMs on *sequential* CATO factor hierarchies in trade-secret misappropriation. FACET tests *parallel* multi-factor balancing in tort law, which is literature-verified uncharted territory.

### 3.1 Historical Hand-formula framing (kept for transparency)

*United States v. Carroll Towing*, 159 F.2d 169 (2d Cir. 1947) introduced the B < PL formulation as the intellectual foundation for all four frameworks above. Every modern risk-utility and balancing test traces back to Learned Hand's compensatory framing. FACET treats the Hand formula as the *theoretical* center of the benchmark and the four doctrinal frameworks as the *empirical* instance pools. A court evaluating whether a party was negligent weighs burden of precaution (B), probability of harm (P), and gravity of loss (L) under the Hand formulation B < PL, plus modern sub-factors from the Restatement (Third) of Torts and industry-custom doctrine (foreseeability, causal proximity, reasonableness of alternative precautions, adherence to or deviation from industry custom, and public-policy considerations). In practice this gives N in the 5–8 range per case, depending on how many sub-factors the appellate opinion discusses. Ground truth comes from the appellate court's liable/not-liable holding plus any stated apportionment of fault.

*Revised 2026-04-11 after round 1 review. The original v0.1 primary instance type was Fourth Amendment reasonable-suspicion (Terry v. Ohio line). That choice was reversed because:*
1. *Reasonable suspicion is a fuzzy standard with documented circuit splits on near-identical facts; "ground truth from appellate holding" assumed a unique correct answer where one does not exist.*
2. *Fourth Amendment doctrine carries a severe political/ideological confound — training data contains opinionated discussion of stop-and-frisk, Terry stops, and racial profiling, so a model that "collapses to officer experience" may be reflecting an absorbed jurisprudential prior rather than a cognitive integration failure. This is the single most likely desk-reject vector at any venue that cares about AI fairness.*
3. *The Hand formula is **compensatory by doctrine**, not merely by rhetoric — B < PL is a mathematical product, not a discretionary balancing test, so collapse is legal error, not judicial discretion. This makes the collapse construct cleaner.*

Rationale for negligence as primary:

- **N in target range via sub-factors.** Core factors B, P, L are three; modern negligence sub-factors typically bring N to 5–8 per case.
- **Compensatory by mathematical construction.** Unlike "totality of the circumstances" doctrines where weighing is discretionary, the Hand formula is a product. A model that ignores P or L is failing to execute an explicit formula, not exercising judicial discretion. This makes Feature 3 (integrative, not dominated) enforceable: no factor can carry >0.5 of the decision weight in a mathematically multiplicative formula.
- **Ground truth is cleaner than reasonable suspicion.** Liable/not-liable determinations are concrete dollar-apportioned outcomes; apportionment-of-fault percentages are public record.
- **Low political contamination.** Tort liability is contested along business-vs-plaintiff lines, but the disagreement is economic rather than identity-based, and training-data politicization is dramatically lower than Fourth Amendment doctrine.
- **Adequate case base.** Carroll Towing line, *United States v. Greyhound Lines*, modern products-liability cases, medical-malpractice negligence, and industrial accident cases collectively provide sufficient volume. **Open item:** actual clean-instance supply not yet empirically verified (see §12).

## 4. Generalization instance type (v1 secondary, not v1 primary)

**Fourth Amendment reasonable-suspicion analysis.** *Terry v. Ohio* 392 U.S. 1 (1968) line of cases. *Demoted from primary after round 1 review* (see §3). Used in v1 as a generalization check — do FACET results on negligence replicate in a structurally different legal balancing domain? Analyzed separately from the primary so the fuzzy-standard and ideological-confound issues do not contaminate the primary result. Smaller N of instances (see §10).

**Instance types explicitly rejected** (do not relitigate):
- **Federal sentencing §3553(a)** — same ideological confound as Fourth Amendment, worse political load.
- **Best-interests-of-the-child custody** — state-variance in statutory lists.
- **Multi-factor fair use §107** — N=4 is below the likely phase transition per `PHENOMENON.md` §8.1.
- **Summary judgment standards** — cleaner than Fourth Amendment but less cleanly compensatory than Hand formula.

## 5. Instance format

Each FACET instance is a JSON record with the following fields. This is the v0.1 schema — expert review may add or modify fields.

```
{
  "instance_id": "facet-neg-0001",
  "source_case": "United States v. Carroll Towing, 159 F.2d 169 (2d Cir. 1947)",
  "jurisdiction": "federal",
  "factors": [
    {
      "factor_id": "f1",
      "factor_type": "burden_of_precaution",
      "factor_cluster_id": "B",
      "text": "The cost of having a bargee aboard during daylight hours was modest relative to industry practice...",
      "directionality": "against_liability",
      "in_case_weight": 0.25,
      "flip_capable": true
    },
    ...
  ],
  "question": "Was the barge owner negligent under the Hand formula?",
  "ground_truth": {
    "answer": "yes",
    "rationale": "B < PL given the probability of drift and the magnitude of potential harm...",
    "holding_source": "159 F.2d at 173",
    "appellate_unanimity": true
  },
  "factor_type_taxonomy_version": "v1.0",
  "metadata": {
    "n_factor_clusters": 6,
    "construction_date": "2026-MM-DD",
    "constructor": "name",
    "reviewer": "name",
    "double_annotated": true,
    "cohens_kappa": 0.78,
    "prior_swap_pair_id": null
  }
}
```

**Key constraints on instance construction** (enforced at build time — revised 2026-04-11 after round 1 review):

1. Every factor-cluster must satisfy the revised `PHENOMENON.md` §8.5 working definition: semantic-entailment retrievable, cluster-independent, decision-relevant in the aggregate sense.
2. **Counterfactual-flip requirement (relaxed).** For at least ⌈N/2⌉ factor-clusters in each instance, there must exist a counterfactual value that would flip the ground-truth answer holding the others constant. The original "every factor must be flippable" criterion was too strong and excluded most real cases; it has been weakened per round 1 review finding F3.
3. **In-case weight ≤0.5.** For every factor-cluster, the weight assigned in the case's own stated rationale (via the structured weight-elicitation procedure in §5.1 below) must be ≤0.5. Instances where any single cluster carries >0.5 are excluded from the primary dataset and moved to a *dominant-factor* secondary set.
4. **Clustering is an annotation step, not a surface tokenization.** Raw propositions are grouped into factor-clusters at annotation time, not post-hoc. Practitioners think in clusters, not atomic propositions.
5. **Factor-type taxonomy is fixed before construction.** A 10–20 type taxonomy is committed to `factor_type_taxonomy.md` before any instance is built (see §5.2). Ad hoc factor_type labels are not permitted.
6. No factor may be a surface-lexical distractor — i.e., no factor can share its trigger pattern with a factor type the model was trained to pattern-match.
7. Each instance must have been *actually decided* by a court; synthetic hypotheticals are excluded from v1 to keep ground truth defensible.
8. **Appellate-unanimity requirement for primary dataset.** Primary-dataset instances must come from cases where the appellate panel was unanimous on the ultimate liable/not-liable holding. Split-circuit cases are allowed only in a separate *legitimate-disagreement* condition (not counted in the primary collapse-rate statistic). This operationalizes round 1 review item T3.4.
9. **Double-annotation requirement.** At least 20% of primary-dataset instances must be double-annotated by two independent constructors. Cohen's κ ≥ 0.7 on factor-cluster enumeration and ground-truth labeling is required for the primary dataset to be considered usable. κ < 0.7 triggers construction-protocol revision before scale-up.

### 5.1 Weight-elicitation procedure for ground-truth rationales

For each case, the constructor reads the appellate opinion's stated rationale and assigns a weight in [0, 1] to each factor-cluster, summing to 1. Weights must be justified with a quoted passage from the opinion where possible. This procedure is used twice: (a) at construction time, to verify constraint 3 (no cluster >0.5); (b) at N-sweep construction time, to stratify factors for random retention (§6.2).

### 5.2 Factor-type taxonomy (fixed before construction)

A separate document `factor_type_taxonomy.md` must be committed before any instance is built. It enumerates 10–20 factor types for the negligence domain (examples: `burden_of_precaution`, `probability_of_harm`, `gravity_of_loss`, `industry_custom_compliance`, `foreseeability`, `causal_proximity`, `alternative_precautions`, `public_policy`, `reasonable_alternatives`, `comparative_fault`). Each type has a definition, 2–3 canonical examples, and a decision rule for borderline cases. The taxonomy is versioned and frozen before scale-up; drift is recorded in the taxonomy version field on each instance.

## 6. Experimental conditions (the treatment arms)

The benchmark is not a single pass over instances — it is a matrix of conditions. Every instance is run under every applicable condition. The conditions below are the v0.1 set; expert review may add or remove.

### 6.1 Base condition (C0)

All N factors presented in the instance's natural order. The model is asked the question and produces an answer plus optional reasoning trace. This is the condition that measures whether collapse is happening at all.

### 6.2 N sweep (C1) — stratified random retention

Sub-conditions C1.2, C1.3, C1.4, C1.5, C1.6, C1.8 — truncated versions of each instance retaining k factor-clusters for k ∈ {2, 3, 4, 5, 6, 8}. The purpose is to locate the minimum N at which collapse appears (answering `PHENOMENON.md` §8.1).

*Revised 2026-04-11 after round 1 review (item T3.6).* The original v0.1 plan used **top-k retention** (keep the k most canonically-weighted factors). This introduced a canonicality confound: the top-k factors are also the most-discussed in training data, so the N-sweep would trivially become a canonicality-sweep — a model would "do better at smaller N" partly because smaller N means more training-canonical factors. This has been replaced with **stratified random retention**:

1. Bucket each instance's factor-clusters into three strata by the in-case weight from §5.1 (low: 0–0.15, mid: 0.15–0.35, high: 0.35–0.5).
2. For each target k, draw a random sub-sample that preserves the same stratum proportions as the full instance.
3. Reject any sub-sample whose retained factors, under the case's own rationale, would flip the ground-truth answer (this is the ground-truth-preserving filter).
4. Repeat until a valid sub-sample is found, or mark the instance as unavailable at that k.

This is construction-expensive — each instance generates multiple valid sub-samples, and rejected draws are common. Budget accordingly in §10.

### 6.3 Per-factor weight-perturbation (C2) — *revised after round 2 face-validity review*

*Replaces the v0.2 removal-ablation protocol. Round 2 review (see `REVIEW_v0.2.md` finding F1) identified that removal-ablation is doctrinally incoherent for tort balancing tests: removing a factor from a Wade-factor case leaves something that is not a Wade-factor case, and LLMs may silently reconstruct the missing factor from pretraining, which contaminates the primary control against CoT unfaithfulness.*

For each factor-cluster *i* in each instance, run a sub-condition where factor *i*'s content is **rewritten to a doctrinally neutral value** rather than removed. Example: instead of deleting the `user_awareness` factor from a Wade-factor table-saw instance, rewrite its text from "users commonly understand that table-saw blades are dangerous" to "users' anticipated awareness of the blade hazard was neither notably high nor notably low." The remaining N−1 factors are unchanged. The instance remains a complete Wade-factor case; only the direction and magnitude of factor *i*'s contribution is neutralized.

**Measurement:** for the collapse claim to hold, the final answer should change *only* when the collapsed-to cluster is neutralized, not when any other cluster is. A model that is integrating all N factors will show answer shifts proportional to the perturbed factor's in-case weight; a model that has collapsed onto factor *k* will show an answer shift only when *k* is perturbed.

**Reconstruction-rate disqualification (mandatory):** after every weight-perturbation trial, add a second turn that asks the model: "Does the case description above omit any factor you believe a court would typically weigh in this analysis?" If the model spontaneously names a factor that matches the neutralized cluster, the trial is disqualified — the model has identified the perturbation and may be compensating via retrieval rather than processing the neutralized text as written. Disqualified trials are logged separately and reported in the paper's methodology section; they do not contribute to the primary collapse-rate statistic.

**Alternative protocol (C2-alt, explicit closure):** for instances where weight-perturbation is hard to construct naturally, use explicit closure instead — prepend a system instruction of the form "For this analysis, stipulate that factor *i* is neutral and not in dispute; weigh only the remaining factors." This is easier to construct but weaker because the model may interpret "not in dispute" as "definitively settled in favor of defendant/plaintiff" rather than "zero weight." Use C2-alt only when the weight-perturbation wording would force doctrinally incoherent text.

**Construction cost:** C2 is now more expensive than v0.2 removal-ablation because each factor-cluster needs a hand-crafted neutral rewrite rather than a delete. Budget accordingly in §10: ~6 perturbation variants per instance × 120 instances = ~720 perturbation texts to author. The reconstruction check is automated and adds no manual cost.

### 6.4 Compliance-vs-integration parallel (C3)

For every integration-condition instance, construct a matched compliance-condition instance where the N items are phrased as independently-checkable requirements rather than trade-off factors. Example: instead of "weigh tip reliability against officer experience," rephrase as "confirm the tip was reliable AND confirm the officer was experienced." The failure pattern on C3 should differ from C0. This is the §5.2 control.

### 6.5 Factor-order randomization (C4)

For each instance, run two variants (revised 2026-04-11 after round 1 review item F5, to separate content from surface-label effects):

- **C4a — position randomization:** k=10 trials with factors presented in random *order*. If collapse persists to the same factor *type* regardless of position, the effect is order-independent.
- **C4b — label randomization:** k=10 trials with factors given randomized surface labels (e.g., tip reliability called "Factor B" in one trial and "Factor E" in another) while the content remains fixed. If collapse persists to the same factor *content* regardless of label, the effect is truly content-driven and not an artifact of surface labels or positional anchoring.

Together, C4a and C4b rule out both Lost-in-the-Middle positional effects (Liu et al. 2024) and surface-label anchoring effects. A content-driven collapse must survive both.

### 6.6 Distractor control (C5)

For each instance, construct a variant with m additional factors that are genuinely irrelevant to the decision (e.g., weather, unrelated prior convictions that the court held inadmissible). Multi-factor collapse should produce a qualitatively different failure pattern from distractor susceptibility (Shi et al. 2023). This is the §5.4 control.

### 6.7 Instruction-tuning arm (C6) — three prompt variants plus faithfulness check

*Revised 2026-04-11 after round 1 review items T3.5 and F4.* The original v0.1 plan used a single prompt variant; round 1 review correctly noted this under-powers the arm because prompt sensitivity is precisely what C6 is testing, and because CoT-unfaithfulness (Turpin 2023) is maximally damaging in exactly this arm.

C6 runs three prompt variants on every instance:

- **C6-weak:** system prompt adds "consider all factors carefully before answering." Tests whether soft instruction is sufficient.
- **C6-moderate:** system prompt adds "for each factor, write a single-sentence assessment, then answer." Tests explicit per-factor engagement without forcing a numerical weight.
- **C6-strong:** system prompt adds "for each factor, write a numerical weight in [0,1] that sums to 1, compute a weighted sum, and base your answer on the weighted sum." This is closest to the original v0.1 C6.

**C6 faithfulness check (required).** C6-strong is *contaminated* by CoT unfaithfulness unless validated. For C6-strong responses that claim a highest-weighted factor k, run a per-response ablation: remove factor k from the instance and re-query. If the model's answer does not change, the written weights were post-hoc rationalization (unfaithful), not the causal driver of the answer. Report the fraction of C6-strong instances that pass this faithfulness check. **Only faithful C6-strong responses count toward the instruction-robustness metric.** Unfaithful responses are tracked separately and reported.

### 6.8 Counterfactual-outcome instances (CF) — added 2026-04-12

*Added after v0.5 pilot findings identified that in-distribution instances cannot distinguish genuine factor integration (WADD) from single-factor heuristic processing (LEX) when both strategies produce the same outcome.*

**Purpose.** In-distribution instances (facet-neg-0001 through 0010) all have the canonical LEX factor pointing in the same direction as the correct outcome. A model that collapses onto the canonical factor reaches the right answer indistinguishably from a model that integrates. Counterfactual instances break this degeneracy by constructing cases where LEX and WADD predict *different* outcomes.

**Construction procedure:**

1. **Select a base instance** from the in-distribution set.
2. **Identify the canonical factor** — the factor that the cross-family probe consensus identifies as "most important" on the base instance (e.g., F1 foreseeability for Cabral/Rowland, F3 alternative precautions for Barker/risk-utility, F1 intent-to-affect for Biakanja/third-party).
3. **Neutralize the canonical factor** by rewriting its text to a doctrinally neutral value: "the court treats this factor as neither clearly present nor clearly absent; the record does not resolve this question." The factor remains in the instance — it is not removed.
4. **Rewrite the remaining N−1 factors** to point strongly toward the *opposite* outcome from the base case. For a base instance with ground truth "yes," all non-neutralized factors are reframed to point toward "no."
5. **Verify ground truth.** Under WADD integration, the aggregate of N−1 factors pointing one way with 1 factor neutralized produces a clear directional answer. A LEX-locked model that depends on the canonical factor has nothing to latch onto and may default to the base-case training prior.

**Measurement — probe faithfulness:**

For each counterfactual run, compare the model's direct-probe answer ("which single factor is most important?") against the neutralized factor:

- **Faithful:** the model identifies a non-neutralized factor that has substantive weight in the counterfactual case.
- **Dissociation:** the model identifies the neutralized factor as "most important" despite that factor being explicitly neutral in the prompt.

Probe faithfulness is reported per-model per-counterfactual-instance. The resulting matrix reveals whether dissociation is model-dependent, doctrine-dependent, or both.

**Instance labeling.** Counterfactual instances use the prefix `facet-neg-cf-NNN` and carry `instance_type: "counterfactual"` and `status: "counterfactual_synthetic_not_for_primary_dataset"` in their JSON metadata. They are not admitted to the primary in-distribution dataset under §5 constraint 7 (synthetic hypotheticals excluded). They constitute a separate counterfactual arm of the benchmark.

**Pilot results (3 counterfactuals × 8 models = 24 data points).** See `results/FINDINGS_pilot_v0.6.md` for the cross-counterfactual probe-faithfulness matrix. Key finding: probe faithfulness varies by doctrine (7/8 faithful on Cabral, 0/8 on Barker, 4/8 on Biakanja) rather than by model family.

### 6.9 Prior-swap control (C7) — descoped to FACET v2

*Removed from v1 on 2026-04-11 after round 1 review item T3.7.* Constructing matched pairs that vary one factor type while holding everything else fixed, without drifting into synthetic hypotheticals (§5 constraint 7), is a multi-month annotation project that answers a secondary question. The evidence C7 would provide supports `PHENOMENON.md` §8.3 (collapsed-to factor predictable from priors?), which is itself a working hypothesis, not a blocker. Moved to FACET v2 as future work. Do not build C7 in v1.

### 6.9 Temperature robustness (C8) — new from round 1 review

*Added 2026-04-11 after round 1 review item F6.* The v0.1 spec used temperature 0.7 for the ensemble-disagreement signal without justification. If collapse is a robust attractor state, it should be visible at low temperature too; if it is only visible at T=0.7, it may be a sampling artifact. C8 runs the ensemble signal at T ∈ {0.3, 0.7, 1.0} and reports robustness of the collapse finding across temperatures. Required for primary-metric credibility.

## 7. Measurement protocol

*Revised 2026-04-11 after round 1 review items F2 and T5 item 3.* Collapse is measured via a triangulation of signals. **For non-reasoning models, all four signals are used; for reasoning-mode models, the logprob signal is optional and the core triangulation is ensemble consistency + calibration + counterfactual.** Reasoning-mode and non-reasoning results are reported separately and not directly compared on the logprob dimension.

### 7.1 Logprob signal (optional for reasoning models)

For models that expose per-token logprobs on the final answer token, record the logprob of each candidate answer token at the decision point. If the top-1 answer has logprob ≥ 0.9 and the next-best has logprob ≤ 0.05, the model is internally confident on the final choice. This bypasses self-report entirely.

**Reasoning-mode fallback.** For models like o-series, DeepSeek-R1, and Claude extended-thinking variants, the "decision point" comes after thousands of thinking tokens and several closed-model APIs restrict logprob access on the final answer token. In those cases, the logprob signal is declared **unavailable** and the core triangulation for that model falls back to §7.2 + §7.3 + §7.4 only. This is stated honestly in the paper's methodology; results across reasoning-mode and non-reasoning models are not compared on this dimension.

### 7.2 Ensemble-disagreement signal

Resample the model's answer at temperatures T ∈ {0.3, 0.7, 1.0} (see §6.9, C8), N=20 samples per temperature. Compute:

- **Answer consistency:** fraction of samples producing the same final answer (per temperature).
- **Collapse-to consistency:** if the model is asked to report the single most important factor, fraction of samples identifying the same factor (per temperature).

High answer consistency + high collapse-to consistency across temperatures = confident collapse robust to sampling noise. Temperature-sensitive collapse (visible only at T=0.7) is reported but does not count toward the primary metric.

### 7.3 Calibration curve (accuracy-at-stated-confidence)

Bin instances by the model's self-reported confidence (where requested). Plot accuracy conditional on stated confidence. Calibration failure (high-confidence wrong) is one signal among the four, not the primary one. Addresses `PHENOMENON.md` §8.4 and the KalshiBench vs. Yoon et al. 2025 dispute — FACET treats self-reported confidence as a support signal, never a primary one.

### 7.4 Collapse-to identification (counterfactual)

For each instance, identify which factor-cluster the model's answer is consistent with. Two methods are used and both must agree:

1. **Counterfactual test:** ablate each factor-cluster individually (this is C2); the cluster whose ablation changes the model's answer is the collapsed-to cluster.
2. **Direct probe:** ask the model "if you had to base this decision on one factor alone, which would it be?" Compare to the counterfactual-test result.

Instances where the two methods disagree are flagged and excluded from the primary collapse-rate statistic. Note: this step no longer conditions on wrongness (see §8).

## 8. Scoring

*Revised 2026-04-11 after round 1 review item F1 (construct-validity hole).* The v0.1 spec conjoined "final answer is wrong" into the primary collapse definition, which conflated *collapse* (a reasoning phenomenon) with *collapse-and-wrong* (a downstream consequence). A model that collapses but happens to land on the right answer was invisible to v0.1's metric. v1 splits the primary metric.

**Primary metric (unconditional): collapse rate.** Fraction of instances on which the model meets all three of the following simultaneously, **regardless of whether the final answer is correct**:

1. Confidence signals agree (logprob if available, otherwise ensemble consistency + calibration; all above pre-registered thresholds).
2. Ensemble-disagreement signal is consistent across T ∈ {0.3, 0.7, 1.0} (same factor identified as collapsed-to).
3. Counterfactual test identifies a single collapsed-to factor-cluster (§7.4), and the direct-probe method agrees.

This is the construct the paper claims to measure. It is reported per-model.

**Secondary metric: collapse-wrong rate.** Fraction of instances where the above three conditions hold AND the final answer is wrong. This is the downstream consequence of collapse. Reported alongside the unconditional rate.

Reporting both metrics means the paper can distinguish: "models collapse X% of the time, and when they collapse their answer is wrong Y% of the time" — two separable claims that v0.1's conjoined metric could not make.

**Other secondary metrics:**

- **Per-factor-type collapse distribution** — which factor types (per the §5.2 taxonomy) the model collapses to.
- **N-phase-transition curve** — unconditional collapse rate as a function of N across C1 sub-conditions.
- **Instruction-robustness delta** — faithful-C6-strong collapse rate minus C0 collapse rate. See §6.7 on why only faithful C6-strong responses are counted.
- **Integration-vs-compliance delta** — C0 collapse rate minus C3 failure rate. Positive delta supports the compliance-vs-integration distinction.
- **Content-vs-position delta** — variance of collapsed-to factor across C4a (order) and C4b (label) randomization trials. Low variance on both = truly content-driven.
- **Partial-collapse rate** — fraction of instances where the dominant factor weight is in [0.5, 0.7) per `PHENOMENON.md` §2.5. Tracked separately because Feature 5's dominance threshold is ≥0.7; partial collapses are the WADD→LEX midpoint and are scientifically important but do not count toward the primary metric.

### 8.1 Pre-specified primary hypothesis (round 1 review item F3)

To address the multiple-comparisons problem, a single primary hypothesis is pre-registered and all other conditions are treated as exploratory:

**H1 (primary, one-sided):** frontier LLMs exhibit a higher unconditional collapse rate on C0 (integration) than their failure rate on C3 (compliance-matched parallel). Tested with a one-sided proportions test at α = 0.05.

All other analyses (N-sweep, C4 randomization, C6 instruction arms, C8 temperature, per-factor distribution) are exploratory and reported without multiple-comparisons adjustment beyond standard reporting discipline. The primary contribution claim rests on H1 alone.

## 9. Model harness

Models evaluated in v1:

- **Frontier closed models:** Claude Opus 4.6, GPT-5 (or latest at test time), Gemini 2.5 Pro.
- **Frontier open models:** Llama 3.3 70B, Qwen 2.5 72B, DeepSeek V3.
- **Reasoning-mode variants:** where available (e.g., Opus 4.6 extended thinking, o3, DeepSeek-R1). These are critical for the KalshiBench / Yoon et al. 2025 calibration dispute.

All models run at **temperature 0.0 for C0/C1/C2/C3/C6/C7 (reproducibility)** and **temperature 0.7 for C4 and C5 and the ensemble-disagreement signal (diversity)**. Context window must be large enough to hold the full instance plus system prompt plus a full reasoning trace; no truncation permitted during evaluation.

## 10. Dataset size and statistical power

v0.1 working target, to be refined after pilot:

*Revised 2026-04-11 after round 1 review item F3 (power calculation was hand-waved).*

*Revised 2026-04-11 after `CASE_CANDIDATES.md` round 1 retrieval and again after round 2 face-validity review (`REVIEW_v0.2.md` findings F1 and F3).*

**Formal power calculation for the primary hypothesis H1 (§8.1) under the partial-collapse primary arm (≥0.5).**

Two-proportions one-sided z-test, α = 0.05, power = 0.8.

- Baseline (C3 compliance failure rate): 35% — unchanged from v0.2.
- **Target (C0 partial-collapse rate at dominance threshold ≥0.5):** 60% — *revised upward from v0.3's 55% because the partial-collapse arm is looser than the v0.3 hard-collapse arm and should detect more instances of the phenomenon.* Supported by the Zhang, Grabmair, Gray & Ashley 2026 integration-stage degradation (64–92% → 11–34% on CATO hierarchies). At a ≥0.5 dominance threshold the expected effect gap is ~25 pp.
- Required n per condition for H1 at 35% vs. 60%, α=0.05 one-sided, power=0.8: **≈ 63 instances** per condition. Rounding up with safety margin: **80 matched pairs** for the partial-collapse primary arm H1 test.
- **Secondary conservative arm (≥0.7 hard-collapse threshold):** baseline 35%, target 50%, effect ~15 pp. Required n per condition: ≈172. Rounding up: **200 matched pairs** would be required for the secondary arm to be individually well-powered. v1 does NOT commit to powering the secondary arm independently — it is reported as descriptive only, not as a confirmatory test.
- **v1 commits to the partial-collapse primary arm only.** This is the pre-registered H1. Hard collapse is reported but not independently powered.

**Dataset composition (v0.4 — revised after round 2 review):**

- **Primary H1 dataset (multi-doctrinal tort balancing, C0 + C3 matched pairs):** **80 matched pairs (160 instances)** for the partial-collapse primary arm. Down from v0.3's 120 pairs because the partial-collapse arm has a larger expected effect (~25 pp vs. v0.3's ~20 pp) and therefore needs less sample. Target mix across doctrinal frameworks:
  - Wade-factor products liability: 40 pairs (50%).
  - Rowland-line duty analysis: 28 pairs (35%).
  - Extended Hand-formula cases (N≥5 via sub-factors): 8 pairs (10%).
  - Restatement (Third) Torts §3 adoption cases: 4 pairs (5%).
- **Secondary conservative arm (hard-collapse ≥0.7):** same 80 pairs, scored under the stricter threshold. Descriptive only, not independently powered.
- **N-sweep exploratory dataset (C1):** sub-samples drawn from the primary dataset. No new instances required.
- **Generalization dataset (Fourth Amendment reasonable-suspicion, C0 + C3 matched pairs):** 30 matched pairs (60 instances). Exploratory replication only.
- **Distractor exploratory set (C5):** 20 primary instances augmented with distractors.
- **C2 weight-perturbation variants (revised §6.3):** ~6 perturbation texts per instance × 160 primary instances = **~960 perturbation texts to author.** This is the single most expensive construction task in v1; it replaces the simpler but doctrinally-incoherent removal-ablation from v0.3.
- **C7 (prior-swap):** removed from v1 per §6.8.

**Total v1 size: ~220 base instances + ~960 weight-perturbation variants.** The base instance count is down from v0.3's ~350, but the C2 construction cost is substantially higher than v0.3 because removal-ablation (automated) was replaced with hand-crafted weight-perturbation (manual). Net effort is similar. Within reach of two annotators working ~4 weeks after case retrieval closes.

**Important honest notes.**
1. The 35% C3 baseline and 55% C0 target are *pre-registered assumptions grounded in Zhang et al. 2026* but still not measurements on FACET's own instances. If the 20-instance pilot (§14) reveals actual baselines materially different, the power calculation must be redone before scale-up.
2. The 120-pair primary dataset requires **expansion beyond California** in both the Rowland-line and Wade-factor pools. This is doable (see `CASE_CANDIDATES.md` expansion path) but adds jurisdictional heterogeneity. A pre-specified sub-analysis will test whether collapse rates vary significantly across jurisdictions; if yes, that becomes a secondary finding, not a contamination.
3. The multi-doctrinal mixture is intentional. It diversifies the primary dataset across four frameworks so that a result on H1 is not framework-specific. A single-doctrine result would be much weaker.

## 11. Pre-registration commitment

Before any evaluation runs, the following must be registered (ideally on OSF or a similar public registry):

1. The final version of `PHENOMENON.md` after expert review.
2. The final version of this spec document.
3. The predicted collapse rates for each model and condition (point predictions with justification).
4. The exact statistical tests that will be run on the results.

Pre-registration exists to prevent the paper from drifting toward whichever result the data happens to produce. This is part of the PhD-mode discipline memory.

## 12. Open items — status after round 1 review (2026-04-11)

*Updated 2026-04-11 after round 1 Opus adversarial review (see `REVIEW_v0.1.md`).*

- [x] **Primary instance type.** ~~Fourth Amendment reasonable-suspicion~~ → **negligence balancing under the Hand formula** (§3). Fourth Amendment demoted to generalization arm (§4). Round 1 flagged ideological confound and fuzzy-standard ground truth as fatal issues for Fourth Amendment. Still requires human legal-NLP reviewer to confirm clean-instance supply empirically.
- [x] **Factor independence.** Operational definition revised in `PHENOMENON.md` §8.5 — clustering is now an explicit annotation step, not a post-hoc adjustment. Still requires human reviewer to confirm cluster boundaries match practitioner usage.
- [x] **Counterfactual-flip requirement.** Weakened from "every factor" to "at least ⌈N/2⌉ factors" per `PHENOMENON.md` §8.5 and `SPEC.md` §5 constraint 2. Closes round 1 review item T3.3.
- [x] **Ground-truth answer source.** Primary dataset now requires appellate-unanimity (§5 constraint 8); split-circuit cases go to a separate legitimate-disagreement condition. Closes round 1 review item T3.4.
- [x] **Instruction-tuning arm phrasing (§6.7).** Three prompt variants (C6-weak, C6-moderate, C6-strong) plus C6 faithfulness check added. Closes round 1 review items T3.5 and F4.
- [x] **N sweep construction (§6.2).** Abandoned top-k retention; now stratified random with ground-truth-preserving filter. Closes round 1 review item T3.6.
- [x] **Prior-swap pair construction (§6.8).** **Descoped from v1 to v2.** Closes round 1 review item T3.7.
- [x] **Pre-registration venue.** OSF confirmed as default; no legal-NLP-specific registry exists and creating one is out of scope.

**Remaining open items for human review** (stand-in cannot close):

- [ ] **Empirical supply of clean negligence instances.** Need a PACER / CourtListener query run by someone with legal database access to verify ~200 clean instances exist before instance construction begins.
- [ ] **Practitioner face validity of factor clustering.** A trial lawyer or torts scholar needs to confirm the cluster boundaries in §5 match how real practitioners carve up negligence cases.
- [ ] **LEX/WADD still state of the art in 2026 decision science?** Check whether the computational rationality literature (Lieder/Griffiths lineage) has superseded Payne-Bettman-Johnson framing.
- [ ] **Cohen's κ threshold of 0.7 appropriate for this domain?** Standard for annotation tasks, but some legal-NLP work uses looser thresholds.
- [ ] **Pre-registration workflow mechanics.** Someone who has pre-registered an ML benchmark on OSF should walk through what commitments are binding.
- [ ] **Legal-NLP literature coverage in `PRIOR_ART.md`.** Round 1 review item F8 noted the prior art is thin on legal NLP specifically. If the paper targets an NLP venue, coverage of Ash/Chen/Ornaghi judicial-decision-modeling work should be added.

## 13. What this spec deliberately does not decide

- The paper's narrative framing (related work section, introduction, contribution claims).
- Which venue to submit to.
- Whether to release the benchmark data publicly, under what license, and with what timing.
- Any follow-up paper (FACET v2, mechanistic interpretability, cross-domain generalization).
- The domain expansion from legal to medicine (the §7.5 backup).

These decisions belong in separate documents and are explicitly out of scope for the pre-build spec. Do not relitigate them here.

---

## 14. Build sequence once the gate clears

The following order is fixed. Steps are not parallelizable.

1. External expert review of `PHENOMENON.md` and this spec. Record reviewer name and feedback.
2. Incorporate expert feedback into both documents. Re-commit.
3. Pre-register (see §11).
4. Construct 20-instance pilot dataset. Run all conditions on one model. Check that the controls behave as expected — in particular, that C3 (compliance) does in fact produce a different failure pattern from C0, and that C2 (per-factor ablation) can actually identify the collapsed-to factor consistently.
5. If pilot passes: scale to full v1 size (§10). If pilot fails: the benchmark design has a flaw and needs revision before scale-up. Do not scale a failing pilot.
6. Run full v1 evaluation across all models (§9). Record everything.
7. Write paper.

Total wall-clock estimate from gate clearance to paper draft: **8–12 weeks**, dominated by instance construction (step 4–5). Not solo-doable without a second annotator.

---

## 15. Version history

- **v0.1 (2026-04-11):** Initial draft. Pre-review. All decisions tentative. Based on `PHENOMENON.md` and `PRIOR_ART.md` round 2. Written before expert review per the founder's decision to finish solo-doable work before unblocking the reviewer search.
- **v0.2 (2026-04-11):** Post round 1 Opus adversarial review. 13 ranked required edits applied (see `REVIEW_v0.1.md`). Major changes: primary instance type switched from Fourth Amendment to negligence / Hand formula; primary metric split into unconditional collapse rate and collapse-wrong rate; logprob signal declared optional for reasoning-mode models; power calculation redone formally with a pre-specified primary hypothesis (H1: C0 > C3); C7 prior-swap descoped to v2; C6 expanded to three prompt variants with faithfulness validation; C4 expanded to include label randomization; C8 temperature-robustness arm added; annotation requirements added (20% double-annotation, κ ≥ 0.7, fixed factor-type taxonomy). Still pending human review; round 1 stand-in did not close the "real legal-NLP expert" gap.
