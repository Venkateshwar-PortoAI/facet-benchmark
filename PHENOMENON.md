# FACET — Phenomenon Definition

**Benchmark:** FACET — Factor Accessibility, Coverage, and Evidence Test
**Phenomenon:** multi-factor collapse
**Status:** pre-build gate. Do not start implementation until this document is reviewed by an external expert and every section below is filled.
**Last updated:** 2026-04-11

---

## 1. One-sentence definition

When an LLM is given a decision that requires simultaneously integrating N≥3 heterogeneous, co-present factors, it confidently collapses to a single factor and ignores the rest, even though it can still retrieve the ignored factors verbatim when asked.

## 2. The five defining features

A failure instance counts as multi-factor collapse only if **all five** hold:

1. **Co-present, not sequentially introduced.** All N factors are present in the model's input at the start of the decision; no factor is introduced as a consequence of reasoning over a prior factor. This is an *information-structural* claim, not a prompt-structural one — the model may internally re-order or cluster factors during reasoning, and that is still co-present. What is excluded is any setup where factor k is only revealed after the model has already committed to a partial answer over factors 1…k−1. *(Revised 2026-04-11 after round 1 review: prior wording conflated prompt structure with reasoning structure.)*
2. **Heterogeneous by kind, not just by surface.** Factors span qualitatively different evidentiary or decisional categories (e.g., evidentiary reliability vs. risk magnitude vs. causal proximity), not merely different instances of the same category. Multiple witness statements about the same behavior count as one factor-kind, not N. A fixed factor-type taxonomy (see `SPEC.md` §5) enforces this at construction time.
3. **Integrative, not dominated — two-tier.** In the case's own stated rationale (via the weight-elicitation procedure in `SPEC.md` §5.1): **primary arm** requires no single factor carries more than **0.7** of the decision weight; **conservative secondary arm** requires no single factor carries more than **0.5**. The primary arm admits real negligence cases where one factor carries ~0.55–0.70 of the weight with corroborating factors making up the rest — this is the empirically dominant pattern in appellate tort practice (*Rowland*, *Parsons*, *Cabral*, *Tarasoff*). The secondary arm is the stricter "clean integration" test. v1 reports both. *(Revised twice: first 2026-04-11 after round 1 to add a quantitative threshold; again 2026-04-11 after round 2 face-validity review, which found the ≤0.5-only threshold was a sampling-biased subset of negligence practice.)*
4. **Semantically retrievable.** If the model is asked afterwards "what was factor k?", its response entails factor k under an NLI-style entailment check. Verbatim reproduction is sufficient but not necessary — correct paraphrase is strictly stronger evidence of retention than verbatim regurgitation. This feature establishes that the information reached the model's representations; the failure mode is integration, not retrieval. *(Revised 2026-04-11 after round 1 review: verbatim was a weaker proxy than semantic accuracy.)*
5. **Behaviorally indistinguishable from LEX (two-tier dominance).** Under the three-signal protocol in `SPEC.md` §7, the model's behavior is consistent with weighting one factor above a dominance threshold and distributing the remainder across the other N−1 factors. This feature is *behavioral*, not introspective — it does not assume the model has access to its own weighting. **v1 uses two tiers:**
   - **Primary arm — partial collapse (dominance threshold ≥ 0.5):** the empirically dominant pattern in real multi-factor tort practice. This is the primary measurement for FACET v1 because real appellate balancing regularly concentrates 0.55–0.70 of decision weight on one factor with the remainder distributed across corroborating factors. *Rowland*, *Parsons*, *Cabral*, and *Tarasoff* all exhibit this pattern in practice.
   - **Secondary arm — hard collapse (dominance threshold ≥ 0.7):** the stricter form — behavior consistent with ≥0.7 on one factor. Reported as the conservative secondary measurement.
   *Revised 2026-04-11 after round 2 face-validity review (see `REVIEW_v0.2.md` finding F3): prior wording made hard collapse the primary and demoted partial collapse to a secondary track. Round 2 flagged this as a sampling bias — excluding partial-collapse cases excludes the empirically dominant category of real negligence practice. v1 now reports both arms, with partial collapse as primary.*

If any of the five fails, the instance is out of scope for FACET and belongs to a different (already-named) failure mode.

## 3. Axis: depth vs breadth

Existing reasoning-failure literature is dominated by **depth** failures — errors accumulating across sequential reasoning steps (GSM8K, BBH, Logical Phase Transitions). FACET claims there is an orthogonal **breadth** axis: failures that happen at depth 1 when too many things must be weighed at once. The paper's contribution is the taxonomic distinction, not the discovery that LLMs fail at hard tasks.

## 4. Theoretical grounding

- **Primary (structural parallel):** Lexicographic heuristic (LEX) — Payne, Bettman & Johnson, *The Adaptive Decision Maker* (1993). LEX = "pick the most important attribute, ignore the rest." Multi-factor collapse is inadvertent lexicographic processing when weighted-additive (WADD) integration is required.
- **Normative contrast:** WADD is what the model should do. LEX is what it does.
- **Attentional mechanism:** Focusing illusion — Schkade & Kahneman (1998).
- **Deliberately dropped:** Extension neglect (Kahneman & Frederick, 2002). Demoted because extension neglect assumes homogeneous attributes; multi-factor collapse is about heterogeneous ones.
- **Complementary (normative meta-level):** Resource-rational analysis — Lieder & Griffiths (2020, *Behavioral and Brain Sciences* 43, e1); Lieder & Griffiths (2017, *Psychological Review* 124:762); Lieder, Callaway & Griffiths (2024, *The Rational Use of Cognitive Resources*, Princeton U. Press). Resource-rational analysis does *not* supersede PBJ's descriptive LEX/WADD taxonomy — it provides a meta-level rationalization for *when* agents select LEX vs. WADD. LEX is rationally chosen when cognitive resources are scarce relative to integration cost; WADD is chosen when resources are ample. *Added 2026-04-11 after round 3 review.* This matters for FACET because it means a WADD→LEX switch in LLMs under increasing N is predicted by *both* the descriptive (PBJ) and normative (Lieder & Griffiths) frameworks. If integration cost scales super-linearly with N in attention-based architectures — which is exactly what transformer attention would predict — then resource-rational analysis says LEX is the rational strategy at high N, and PBJ says it is the observed strategy. The two frameworks converge on the same prediction from different theoretical starting points, which strengthens rather than weakens the novelty claim.

See `PRIOR_ART.md` rounds 1, 2, and 3 for the full novelty-check reasoning.

### 4.1 Operational ontology declaration — economic-analysis-of-law framing

*Added 2026-04-11 after round 2 face-validity review finding F6.* FACET adopts the **economic-analysis-of-law** ontology of negligence as an operational choice: it treats balancing-test factors as weighted inputs to a decision function that a decision-maker (human judge or LLM) evaluates simultaneously. This ontology is directly compatible with the Hand formula's B < PL cost-benefit framing and with the Wade seven-factor risk-utility calculus, and it supports the LEX/WADD measurement apparatus FACET uses.

**FACET explicitly acknowledges that this is one of several defensible theoretical positions and does NOT claim the economic-analysis framing is the only correct reading of negligence doctrine.** In particular, civil-recourse theorists (Goldberg & Zipursky 2006, 2010; Weinrib 1995, 2012) read balancing tests not as weighted-additive decision functions but as considerations that jointly inform a gestalt characterization of the defendant's conduct as wrongful-to-the-plaintiff. Under the civil-recourse reading, factors are not being summed at all and "multi-factor collapse" is an ill-posed concept because there is no well-defined "correct integration" to collapse *away from*.

**Why we adopt the economic-analysis ontology despite this:**

1. **It is the ontology under which the cognitive phenomenon FACET wants to measure is well-defined.** LEX and WADD are only meaningful if factors are at least approximately weighted inputs. Under a wrongs-based ontology, the cognitive question FACET asks ("does the model integrate heterogeneous factors or collapse to one?") does not translate.
2. **It matches how LLMs are actually prompted.** When a model is given a Wade-factor case and asked "was the design defective?", the prompt format is inherently a weighted-input format — the model receives N discrete propositions and produces a decision. Whatever cognitive operation the model is performing, it is operating on a weighted-input representation, not on a gestalt-characterization representation.
3. **The Hand formula itself is the canonical economic-analysis reading of negligence**, and FACET's theoretical grounding (Payne, Bettman, & Johnson 1993; Lieder & Griffiths 2020) treats multi-attribute decision-making as an integration problem. Adopting a wrongs-based ontology would require replacing the theoretical grounding, which is a different benchmark.

**What this commits us to in the paper:** a single paragraph in §1 or §2 of the final paper must explicitly declare the ontology choice, acknowledge the civil-recourse alternative, and state that FACET does not attempt to measure wrongs-based tort-theoretic claims. This is defensive coverage against the Goldberg/Zipursky-style objection that otherwise would read FACET as measuring "the wrong thing." A reviewer who rejects the economic-analysis ontology is rejecting the entire benchmark family — not just FACET — and that rejection is a venue-level mismatch, not a FACET flaw.

## 5. Mandatory experimental controls (non-negotiable)

These are the gate conditions under which the measurement is considered valid. Derived directly from the novelty check's top objections. Without all four, the benchmark is desk-rejectable on methodology.

1. **Per-factor ablation.** For each instance, remove each factor individually and observe whether the final answer changes. Only the collapsed-to factor's removal should change the answer. This is the core defense against CoT unfaithfulness (Turpin et al. 2023) — it proves collapse affects *decisions*, not just self-reported weights.
2. **Compliance-vs-integration control.** Run a parallel condition where the N items are independently checkable (no trade-offs). Show the failure pattern differs from the integration condition. This kills the "you are just rebranding multi-constraint satisfaction" objection (CFBench, RECAST, DPPM).
3. **Factor-order randomization.** Randomize the order of factors across trials. If collapse persists to the same factor *type* regardless of position, the effect is content-driven, not positional. Kills "Lost in the Middle" objection.
4. **Distractor control.** Include instances where some factors are genuinely irrelevant. Show multi-factor collapse is qualitatively different from distractor susceptibility (Shi et al. 2023, GSM-NoOp) — in FACET all factors are required.

## 6. Explicit non-goals

FACET does **not** measure, claim to measure, or aspire to measure:

- Multi-step / chain-depth reasoning failure.
- Constraint compliance (each constraint independently checkable, no trade-offs).
- Distractor susceptibility where ignored information is irrelevant.
- Long-context retrieval failure ("Lost in the Middle") — factors are short and co-present.
- Multi-agent information pooling (HiddenBench territory).
- LLM-as-judge rubric collapse (Feuer et al. 2025 territory).
- Anchoring bias in sequential priming contexts.
- Any claim that this is a newly *discovered* failure — only newly *distinguished*.

Scope creep into any of the above is the failure mode that killed the prior attempt. Say no.

## 7. Domain constraint and demo-domain selection

### 7.1 Hard constraint

The public demo domain **must not be finance**. Rationale: arXiv is scraped into LLM training corpora, and finance-domain signal would leak downstream into competitor hedge fund models through future base-model capabilities. Finance is reserved for internal research only, never the public benchmark.

### 7.2 Candidate comparison

Three candidate domains evaluated against FACET's five defining features and the four mandatory controls in §5:

| Criterion | Medicine | **Legal (balancing tests)** | Logistics |
|---|---|---|---|
| Native multi-factor integration | ✅ diagnosis, treatment selection | ✅✅ **balancing tests are literally N-factor integration doctrine** | ⚠️ collapses into constraint satisfaction |
| Heterogeneous factors (feature 2) | ✅ symptoms, history, contraindications, imaging | ✅✅ qualitatively different dimensions by legal design | ❌ tends to homogeneous (cost, time, capacity) |
| All required (feature 3) | ⚠️ some factors often redundant | ✅ "totality of the circumstances" doctrines require every factor | ⚠️ often reducible to weighted sum |
| Verbatim-retrievable (feature 4) | ✅ clinical vignette sentences | ✅ case facts are written as discrete propositions | ✅ trivially |
| Ground truth availability | ⚠️ contested, liability-sensitive | ✅ case decisions, statutory tests | ✅ optimization solvers |
| Resists the "compliance ≠ integration" attack | ✅ | ✅✅ **factors actively trade off, not checklist** | ❌ **invites exactly this attack** |
| Domain-expert reviewer accessibility | ⚠️ hard (medical academics, liability concerns) | ✅ easy (law school academics publish openly) | ✅ easy (OR academics) |
| Existing benchmark overlap risk | MedR-Bench, SCT-Bench (adjacent) | LEXam, MSLR, PILOT (sequential/IRAC, distinct from breadth) | R-ConstraintBench (direct overlap risk) |
| Publication liability | ⚠️ LLM clinical failure modes are sensitive | ✅ legal reasoning failures are expected and non-sensitive | ✅ |

### 7.3 Decision: **legal (negligence balancing under the Hand formula and its modern extensions)**

*Revised 2026-04-11 after round 1 review. The original v0.1 decision was Fourth Amendment reasonable-suspicion (Terry v. Ohio line). That choice was reversed because reasonable-suspicion is a fuzzy standard with known circuit splits on near-identical facts, contaminating the ground-truth assumption; and because Fourth Amendment doctrine carries a significant political/ideological confound that would allow reviewers to read FACET as measuring LLM jurisprudential alignment rather than cognitive integration. Fourth Amendment is now the **generalization check** (§7.4), not the primary.*

**Rationale.** Negligence balancing — the Hand formula (*United States v. Carroll Towing*, 159 F.2d 169) and its modern statutory and Restatement (Third) Torts extensions — is the one area of American law where multi-factor integration is *explicitly compensatory by doctrine*. The Hand formula's B < PL structure is literally weighted-additive: burden of precaution (B) is compared against probability of harm (P) multiplied by loss magnitude (L). Modern negligence practice extends this with sub-factors (industry custom, foreseeability, causal proximity, reasonableness of alternative precautions, public policy considerations), bringing N to the 5–8 range required by FACET.

Every one of the five defining features in §2 maps onto negligence balancing:

- **Co-present (Feature 1)** — the facts of a negligence case are all before the jury at once; factor discovery is pre-trial, not mid-decision.
- **Heterogeneous by kind (Feature 2)** — B, P, and L are *qualitatively different quantities* (cost, probability, harm magnitude), not surface variations of the same category. Modern sub-factors add further kinds (industry custom, foreseeability, etc.).
- **Integrative, not dominated (Feature 3)** — the Hand formula is explicitly compensatory by construction; no single factor can carry more than ~0.5 of the decision weight because the formula is a product, not a max.
- **Semantically retrievable (Feature 4)** — case facts are recorded as discrete propositions in appellate opinions.
- **Behaviorally testable collapse (Feature 5)** — if a model reduces negligence analysis to "burden was low, therefore liable" (ignoring P or L), that is collapse, measurable by counterfactual ablation.

Three further reasons negligence beats Fourth Amendment:

1. **Compensatory by doctrine, not merely by rhetoric.** "Totality of the circumstances" doctrines (Fourth Amendment, §3553(a) sentencing) *say* the decision-maker should weigh all factors, but in practice the weighing is discretionary and courts collapse regularly without legal error. The Hand formula is *mathematically* compensatory — collapsing is legal error, not judicial discretion. This makes collapse a cleaner construct: a model that collapses on a negligence case is failing to execute an explicit formula, not failing to execute a vague balancing test.
2. **Low political/ideological contamination.** Tort liability is contested along business-vs-plaintiff lines, but the disagreement is economic, not identity-based, and the training data for frontier models contains far less politicized discussion of negligence than of reasonable suspicion. Eliminates the AI-fairness desk-reject vector.
3. **Fills the same acknowledged gap.** Yu et al. 2025 (MSLR, arXiv:2511.07979) — "sequential prompting approaches fail when a legal problem requires holistic evaluation and simultaneous factor weighting" — applies equally to negligence as to any other balancing test. The gift quote survives the domain switch.

**Cost of the switch:** instance construction is slightly harder because the Hand formula's core factors (B, P, L) are three, not five, so sub-factor enumeration from modern negligence doctrine is required to reach N in the target range. This adds annotation overhead but does not change the fundamental approach.

### 7.4 Generalization arm (demoted from primary)

**Fourth Amendment reasonable-suspicion analysis** (*Terry v. Ohio* / *Illinois v. Wardlow* line), used as a generalization check to test whether FACET results on negligence replicate in a structurally different balancing domain. Treated as a *secondary* dataset, smaller N of instances, and analyzed separately so the fuzzy-standard and ideological-confound issues do not contaminate the primary result.

**Killed entirely as candidates:**
- **Federal sentencing §3553(a)** — same ideological confound as Fourth Amendment, worse political load. Not used even as generalization.
- **Best-interests-of-the-child custody** — state-variance in statutory lists makes cross-jurisdictional ground truth unreliable.
- **Summary judgment standards** — considered as alternative primary, rejected in favor of negligence because the compensatory structure of the Hand formula is cleaner.
- **Multi-factor fair use §107** — N=4 is below the likely phase transition per §8.1 working hypothesis.

### 7.5 Backup domain (outside law)

If legal-reviewer access fails entirely at §10 item 1, **medicine (diagnostic multi-factor integration — chest pain differential or polypharmacy contraindication analysis)** remains the backup. Logistics is still excluded — it collapses into constraint satisfaction and invites the exact reviewer attack FACET must kill.

### 7.6 Domains explicitly excluded

- **Finance** — IP leakage risk (see §7.1).
- **Logistics / scheduling** — constraint satisfaction, not integration.
- **Moral dilemmas** — overlaps Chiu et al. 2024 (DailyDilemmas) terminology and is N=2 by construction.
- **LLM-as-judge scoring** — overlaps Feuer et al. 2025 terminology directly.
- **Fourth Amendment / sentencing / custody** — as above, ideology or jurisdictional confounds.

## 8. Open questions the gate cannot close alone

These must be answered before any code is written, ideally via external expert review. Each question below has a **partial answer** drawn from the expanded lit base (see `PRIOR_ART.md` round 2) and a **remaining empirical gap** that only a FACET pilot can close.

### 8.1 What is the minimum N at which collapse appears?

- **Working hypothesis:** N≥3.
- **Partial answer from lit:** Murthy et al. 2025 (arXiv:2506.20666) runs the nearest methodological cousin at **N=2** (informational vs. social utility in polite speech) and finds *smooth reweighting*, not collapse. This is weak negative evidence that N=2 is insufficient to trigger the phenomenon. Multi-constraint compliance benchmarks (CFBench, RECAST, DPPM) show degradation starting at moderate constraint counts (5–10), but those measure compliance, not integration, so they bound the problem loosely.
- **Remaining gap:** no paper has run a parametric N-sweep on a heterogeneous-factor integration task. **FACET pilot must sweep N ∈ {2, 3, 4, 5, 6, 8}** to locate the phase transition empirically; do not hard-code N≥3 as a design assumption.

### 8.2 Does collapse persist under instruction-tuning for explicit multi-factor weighing?

- **Partial answer from lit:** Kargupta et al. 2025 (arXiv:2511.16660) find that "models possess behavioral repertoires associated with success but fail to deploy them spontaneously" — strong evidence that *knowing* the right strategy does not imply *deploying* it. This is the capability-deployment gap. Zhang et al. 2025 (arXiv:2402.01740) shows cognitive load triggers the WADD→LEX switch even in otherwise-capable models. KalshiBench reports that *reasoning enhancements degrade calibration* in some conditions, contra Yoon et al. 2025.
- **Working answer:** very likely **yes, collapse persists** even under explicit "weigh all factors" instructions. The capability exists but is not deployed under the pressure of parallel-factor integration.
- **Remaining gap:** FACET must include an explicit-instruction condition as a treatment arm ("weigh all N factors equally" / "write weights for each factor before answering") and measure whether collapse persists. If collapse *disappears* under instruction, the phenomenon is a prompting artifact, not a capability gap, and the paper's framing must change.

### 8.3 Is the "collapsed-to" factor predictable from pretraining distribution priors?

- **Partial answer from lit:** no direct evidence. Shi et al. 2023 (GSM-IC) shows distractor susceptibility is partially predicted by surface similarity to training-distribution patterns; Echterhoff et al. 2024 show anchoring biases track base-rate exposure; Hoscilowicz et al. 2026 (label effects, snippet-only) show attention latches onto salient-in-training cues over content.
- **Working hypothesis:** yes — the collapsed-to factor is likely the one with the strongest match to training-distribution priors for the decision type (e.g., "price" in a purchase decision, "symptoms" in a diagnosis). This is testable.
- **Remaining gap:** FACET must include a prior-swap control condition — construct matched instance pairs where the "popular" factor is systematically varied — and check whether collapse follows the prior or stays fixed on some content-invariant slot. This is one experiment, not a design assumption.

### 8.4 How do we measure "confidence" in a way that is not itself a self-report artifact?

- **Partial answer from lit:** FermiEval (arXiv:2510.26995, snippet) and KalshiBench (arXiv:2512.16030, snippet) both use *calibration curves* (accuracy conditional on stated confidence) rather than raw self-reports — this is the field-standard defense against self-report artifacts. Yoon et al. 2025 vs. KalshiBench is an open dispute over whether reasoning-mode models are better or worse calibrated.
- **Working answer for FACET:** triangulate three signals, do not trust any single one.
  1. **Logprob of the chosen answer** relative to the top-k alternatives (no self-report involved).
  2. **Temperature-sampled ensemble disagreement** — resample N times at T=0.7 and measure whether the model consistently collapses to the *same* factor. Consistent collapse = high confidence; scattered = low.
  3. **Calibration curve** — accuracy-at-stated-confidence, as in FermiEval.
- If all three agree that the model is confident on wrong answers, the "confident collapse" criterion (feature 5 in §2) is satisfied regardless of what the model *says* about its confidence.
- **Remaining gap:** none that blocks the gate — this is a measurement-methodology decision that can be made now. Write it into the benchmark spec.

### 8.5 What is the unit of "one factor"?

- **Partial answer from lit:** no paper answers this directly. This is a benchmark-construction decision, not a literature question.
- **Working operational definition** (revised twice — initial 2026-04-11 after round 1, again 2026-04-11 after round 2 face-validity review):
  1. A factor is a **proposition or proposition-cluster** that an NLI entailment check can retrieve from the model under semantic-accuracy matching (verbatim sufficient but not necessary).
  2. A factor is **distinguishable in the court's own stated reasoning**: two clusters are distinct iff the opinion discusses them in separately-locatable passages AND one cluster can be counterfactually varied in the annotator's hypothetical without having to re-describe the other cluster's propositional content. *(Revised from "independent at the cluster level" after round 2 review finding F2: mechanical independence does not exist in real tort doctrine — Hand P and L co-vary, Rowland factors 1 and 3 cross-reference each other, Wade factors 2 and 4 are logically coupled. Enforcing mechanical independence would push the corpus toward a biased subset where courts happened to avoid the most common doctrinal language.)*
  3. A factor must be **decision-relevant in the aggregate sense**: for at least ⌈N/2⌉ of the **top-weighted** factors in each instance, there must exist a counterfactual value that would flip the correct answer holding the others constant. The ⌈N/2⌉ refers specifically to the top-weighted half by in-case weight; stub factors (weight ≤0.05, see criterion 5) do not count toward the flip-capability requirement.
  4. A factor's in-case weight must be **≤0.7** (primary arm) or **≤0.5** (conservative secondary arm) of the decision weight per Feature 3, estimated from the case's own stated rationale via the structured weight-elicitation procedure in `SPEC.md` §5.1. *(Revised after round 2 review finding F3: prior ≤0.5-only threshold excluded most real negligence practice. v1 now reports both arms.)*
  5. A factor's in-case weight must be **≥0.05** to count toward the decision-relevant N. Factors below the floor (e.g., Rowland's `certainty_of_injury` and `insurance_availability` in cases where they are doctrinally listed but substantively near-zero) are recorded for completeness but do not satisfy the N≥5 floor. *(Added after round 2 review finding F7: Rowland stub factors were inflating N from 5 to 7 on substantively-identical cases, and the N-sweep analysis would treat this inflation as real signal.)*
- **Remaining gap:** human torts-scholar review is still needed for real-world cluster boundary calibration. The round 2 stand-in identified the likely direction (clusters will need to be coarser than round 1 assumed) but only a human practitioner can confirm the specific boundaries on real cases.

### 8.6 Does the five-feature definition in §2 exclude any instance a domain expert would call collapse?

- **Partial answer from lit:** Chiu et al. 2024 (DailyDilemmas) use "collapse of value pluralism" for a *binary*-action moral dilemma. Under FACET's five features that would fail feature 3 (each dilemma is N=2 by construction) and arguably feature 1 (values are elicited post-hoc, not presented as co-present factors). So the FACET definition *does* exclude a phenomenon another group calls collapse. This is intentional — it is why we renamed to "multi-factor collapse" — but the exclusion must be argued in the paper, not assumed.
- **Face-validity stress tests that can be run now:**
  - A 70/30 soft weighting (not quite collapse) fails feature 5 ("confident collapse"). Good — keeps the definition sharp.
  - A model that collapses *because* it was asked for only one factor (prompting artifact) fails the "all required" criterion in feature 3. Good.
  - A model that cannot retrieve factor k verbatim when asked fails feature 4 — which means the failure is attention/retrieval, not integration. This is a hard edge case and reveals that feature 4 is doing real discriminative work.
- **Remaining gap:** external expert review (§10 item 1). Self-stress-testing cannot fully close this question; a domain expert must try to break the definition.

---

**Summary of what §8 unblocked:**

- Questions 8.1 (N sweep), 8.2 (instruction-tuning arm), 8.3 (prior-swap control) now resolve into **three specific experimental conditions the benchmark spec must include** — they are design requirements, not open research questions.
- Question 8.4 (confidence measurement) resolves into a **three-signal triangulation protocol** that can be written into the spec now.
- Question 8.5 (unit of factor) resolves into a **working operational definition** pending expert confirmation.
- Question 8.6 (face validity) remains **blocked on external expert review** — this is the single question that §10 item 1 is required to close.

## 9. Verdict from the prior-art check

`PRIOR_ART.md` concludes: **REVISE, then submit.** The core claim survives the novelty check but narrowly. The benchmark is publishable at a strong workshop or D&B track *only if* all four controls in §5 are in place. Without them, methodological rejection is near-certain.

## 10. What is explicitly still to do

Before any benchmark code, dataset, or eval harness is written:

1. External expert review of this document (name the expert, record the review). *[critical path, blocked on finding reviewer]*
2. ~~Extend the prior-art check from ~20 to 30–50 papers per the discipline plan.~~ **Done 2026-04-11** — round 2 added 15 ADJACENT papers, total ~35, verdict unchanged (REVISE). See `PRIOR_ART.md` "Extended Prior Art (round 2)". Snippet-only citations still need per-paper WebFetch verification before final paper write-up.
3. ~~Answer the open questions in §8.~~ **Partially done 2026-04-11** — 5 of 6 questions now have working answers from the expanded lit base, converted into three concrete experimental conditions (N sweep, instruction-tuning arm, prior-swap control) and one measurement protocol (three-signal confidence triangulation). Question 8.6 (face validity) remains blocked on §10 item 1.
4. ~~Choose the demo domain (§7).~~ **Done 2026-04-11** — legal balancing tests / totality-of-the-circumstances doctrines. Medicine is the backup. Logistics explicitly rejected. See §7.3 for rationale.
5. ~~Write the benchmark spec (instance format, scoring, model harness) as a separate document.~~ **Done 2026-04-11** — see `SPEC.md` v0.1. Pre-review draft. 8 open items flagged for expert review in §12. All design decisions tentative until the face-validity review closes.

**Round 2 lit-review takeaways folded into the gate:**
- Two terminology collisions now exist on the word "collapse" (Feuer 2025 "factor collapse", Chiu 2024 "collapse of value pluralism"). The FACET name and the "multi-factor collapse" phenomenon name are load-bearing — treat them as fixed, not cosmetic.
- The closest methodological cousin is Murthy et al. 2025 (arXiv:2506.20666) — cognitive-model-grounded weight elicitation at N=2. Position FACET as the N≥3 heterogeneous-factor extension grounded in LEX/WADD.
- Strongest new ally: Zhang et al. 2025 (arXiv:2402.01740) — empirical evidence of compensatory→non-compensatory switching under cognitive load in LLMs, the exact WADD→LEX mechanism predicted by Payne-Bettman-Johnson.
- Gift quote for related work: Yu et al. 2025 (MSLR) explicitly note that "sequential prompting approaches fail when a legal problem requires holistic evaluation and simultaneous factor weighting" — acknowledgment of the breadth gap without a benchmark.
- Gap area 4 (mechanistic interpretability of decision-setting collapse) is genuinely empty in 2025–2026 literature. **Do not expand v1 into this; flag as v2 future work.**

Until those five steps are done, `COHERENCEBENCHMARK/` should contain documents, not code.
