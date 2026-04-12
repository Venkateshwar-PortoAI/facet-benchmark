# FACET — Prior Art / Novelty Check

> **Provenance:** originally generated as `compass_artifact_wf-fa4c7301-3102-4273-ae0c-c5493bf17c40_text_markdown.md` on 2026-04-10, renamed and committed on 2026-04-11. Content below is unchanged from the original deep research run.
>
> **Naming note:** the original artifact uses the term *"factor collapse"*. The canonical name for this work is now **multi-factor collapse** (benchmark: **FACET**), renamed specifically because this document found that Feuer et al. 2025 already use "factor collapse" in an adjacent LLM-as-judge context. See `PHENOMENON.md` §4 for the current naming and grounding.

---

# Deep Research Results — Factor Collapse Novelty Check

**Bottom line: The novelty claim survives, but narrowly.** No existing paper directly measures "factor collapse" as defined — confident single-factor answers when N≥3 parallel factors require simultaneous integration, with ignored factors remaining verbatim-retrievable. The depth-vs-breadth distinction in compositional reasoning failure taxonomy appears genuinely novel. However, three significant threats require preemptive defense: the multi-constraint satisfaction literature documents the *underlying phenomenon* without the taxonomic framing; distractor susceptibility research could absorb the claim under a broader umbrella; and CoT unfaithfulness literature threatens the validity of structured weight-reporting methodology. Verdict: **REVISE**, then submit.

---

## Prior art check

Exhaustive search across 20+ query formulations, all major venues (NeurIPS 2024–2025, ICLR 2025–2026, ACL 2024–2025, EMNLP 2024–2025, COLM 2024–2025), and all major lab publications (Anthropic, OpenAI, DeepMind, Google, Meta FAIR, Mistral) from 2024–2026 yielded **zero direct overlaps** and **several adjacent threats** ranked below by proximity.

### Feuer et al. (2025) — "When Judgment Becomes Noise" — **ADJACENT (terminological threat)**
Feuer, B., Tseng, C.-Y., Lathe, A. S., Elachqar, O., & Dickerson, J. P. (2025). "When Judgment Becomes Noise: How Design Failures in LLM Judge Benchmarks Silently Undermine Validity." arXiv:2509.20293.

**What it measures:** LLM judges scoring multi-criteria rubrics (e.g., style, conciseness, completeness, safety, correctness) exhibit "severe schema incoherence and **factor collapse**" — factor correlations above **0.93** across most criteria, meaning the judge collapses a multi-dimensional rubric into a single latent dimension. **This paper uses the exact term "factor collapse."** However, the context is psychometric validity of LLM-as-judge benchmarks, not LLM reasoning/decision-making. The collapsed entity is evaluation criteria in a judging task, not decision factors in a reasoning task.

**Overlap degree:** The term is identical and the structural phenomenon is analogous — an LLM reduces N dimensions to ~1. But the domain (benchmark evaluation vs. multi-factor decision-making), measurement approach (factor analysis of score matrices vs. structured weight elicitation), and theoretical framing (psychometric validity vs. cognitive heuristic failure) are distinct. **Verdict: ADJACENT.** The authors must cite this paper, distinguish their usage, and consider whether the shared term creates confusion or strengthens the case that "factor collapse" is a general LLM failure pattern manifesting across contexts.

### Li et al. (2025) — HiddenBench — **ADJACENT (closest integration benchmark)**
Li et al. (2025). "HiddenBench: Assessing Collective Reasoning in Multi-Agent LLMs via Hidden Profile Tasks." arXiv:2505.11556.

**What it measures:** Whether multi-agent LLM groups can integrate asymmetrically distributed information to reach correct decisions, based on the Hidden Profile paradigm from social psychology. GPT-4.1 groups fail to pool distributed knowledge, showing human-like collective reasoning failures. **This is the closest existing benchmark measuring information integration failure for decisions.** However, the information is *distributed* across agents (each agent holds partial info), not *co-present* in a single context. The failure mechanism is information sharing/pooling, not single-agent factor weighting. **Verdict: ADJACENT.**

### Shi et al. (2023) — GSM-IC / Distractor Susceptibility — **ADJACENT (mechanistic overlap)**
Shi, F., et al. (2023). "Large Language Models Can Be Easily Distracted by Irrelevant Context." ICML 2023.
Yang et al. (2025). GSM-DC. arXiv (2025).
Mirzadeh et al. (2024). GSM-NoOp. arXiv (2024).

**What they measure:** LLMs incorporating irrelevant numerical information into math reasoning, with performance degradation as distractors increase. **The key distinction:** in distractor susceptibility, ignored information is genuinely *irrelevant* — the correct answer doesn't need it. In factor collapse, ALL N factors are *required* for the correct answer. This is a meaningful difference, but a reviewer could argue factor collapse is just "distractor susceptibility where the model incorrectly classifies relevant factors as distractors." **Verdict: ADJACENT** — requires explicit benchmarking against distractor susceptibility to prove the distinction.

### Multi-constraint satisfaction benchmarks — **ADJACENT (documents the phenomenon without the framing)**

- **CFBench** (Qiao et al., 2024, arXiv:2408.01122): 1,000+ samples across 10 constraint categories. Measures constraint success rate degradation as constraints accumulate. **Tests COMPLIANCE** (did the output satisfy each constraint independently?), **not INTEGRATION** (did the model trade off competing factors?).
- **RECAST** (2025, arXiv:2505.19030): Multi-constraint instruction-following dataset. Hard Constraint Satisfaction Rate drops dramatically with more parallel constraints.
- **DPPM** (2025, arXiv:2506.02683): "LLMs are not yet capable of effectively managing too many constraints at once... plans directly generated by LLMs can adequately satisfy a few constraints but consistently fail to meet all constraints simultaneously."
- **FollowBench**, **IFBench**, **COLLIE**: All test multi-constraint instruction following — all measure COMPLIANCE, not INTEGRATION.

**Critical assessment:** These benchmarks document that LLMs fail when facing many simultaneous requirements. However, they uniformly test whether the output *satisfies* each constraint (checkable independently), not whether the model *integrated* competing factors into a weighted decision. No benchmark requires the model to make trade-offs between factors. **Verdict: ADJACENT** — the underlying phenomenon (degradation with constraint count) is documented; the specific failure pattern (confident collapse to one factor in a trade-off decision) and the taxonomic framing are not.

### Cognitive bias benchmarks (anchoring) — **ADJACENT**
Echterhoff et al. (EMNLP Findings 2024), O'Leary (2025), arXiv:2505.15392 (2025).

**What they measure:** LLMs exhibiting human-like anchoring bias — overweighting first-presented information. Mechanistically the closest behavioral analog. But existing benchmarks test anchoring in sequential/priming contexts (prior info biases later judgment), not the simultaneous N-factor integration pattern where all factors are co-present. **Verdict: ADJACENT.**

### Additional papers checked with no overlap

- **ComplexBench** (arXiv:2407.03978): Constraint composition, not factor integration. COMPLIANCE. ADJACENT.
- **IFEval** (Zhou et al., 2023): Verifiable instructions. Pure COMPLIANCE. UNRELATED.
- **LSAT / AR-LSAT**: Constraint satisfaction problems with logically determined answers. No trade-offs. ADJACENT.
- **BBH / BBEH** (Google, 2025): Multi-step logical reasoning. Tests depth, not breadth. ADJACENT.
- **Logical Phase Transitions** (Zhang et al., 2026, arXiv:2601.02902): Reasoning collapse beyond complexity thresholds — but complexity is measured along depth, not breadth. ADJACENT.
- **3-SAT Phase Transitions** (COLM 2025): CSP hardness in LLMs. UNRELATED.
- **Lu et al. (EMNLP Findings 2024, arXiv:2410.01246)**: AHP-powered multi-criteria evaluation. Uses LLMs *as tools* for AHP, not as *subjects* exhibiting factor collapse. ADJACENT.
- **ConstraintBench** (arXiv:2602.22465): Operations research optimization. UNRELATED.
- **"The Model Says Walk"** (arXiv:2603.29025): Surface heuristic overriding implicit constraints. ADJACENT.
- **"Comprehension Without Competence"** (arXiv:2507.10624): Notes CoT converts "parallel constraints into serial computation." Theoretically relevant but no empirical measurement. ADJACENT.

**No paper was classified as OVERLAPS.** The novelty claim survives the prior art check, though the boundary with multi-constraint satisfaction and distractor susceptibility is uncomfortably thin without proper controls.

---

## Better cognitive-science parallel?

The researcher's current grounding in Kahneman & Frederick (2002) extension neglect has an acknowledged weakness: extension neglect applies to *homogeneous* extensional attributes, while factor collapse involves *heterogeneous* factors. After evaluating 10 candidate constructs, the verdict is clear.

**The lexicographic heuristic (LEX) from Payne, Bettman & Johnson (1993) is the correct primary citation.** It is a substantially better fit than extension neglect for five reasons:

1. **Precise structural match.** LEX is exactly the description of factor collapse: given N heterogeneous attributes, the decision-maker selects the most important attribute and bases the entire decision on it alone, ignoring N-1 others. This maps one-to-one onto the observed LLM behavior.

2. **Explicitly heterogeneous attributes.** LEX was developed for and tested with inherently heterogeneous attributes — apartment selection (rent, commute, size, noise), consumer products (price, quality, brand, features). Extension neglect was developed for homogeneous extensional attributes (group size, number of affected people).

3. **Normative contrast built in.** The Adaptive Decision Maker framework provides the crucial WADD (weighted additive) vs. LEX comparison. WADD is what the LLM *should* do — integrate all factors with appropriate weights. LEX is what it *actually does* — collapse to one. This framing is cleaner than trying to map extension neglect onto a heterogeneous-factor scenario.

4. **Information retention, not loss.** LEX does not imply information loss. The decision-maker has access to all attributes but fails to integrate them. This precisely matches the verbatim-retrievability finding.

5. **Complexity-driven switching.** The framework predicts that decision-makers switch from WADD to LEX under increased complexity, time pressure, and cognitive load — paralleling the observation that factor collapse appears when N≥3.

**Kahneman's focusing illusion** (Schkade & Kahneman, 1998) is the second-best fit — it describes overweighting one heterogeneous factor in a multi-factor judgment (e.g., overweighting climate when judging life satisfaction in California). It explains the *mechanism* of attention-driven overweighting but is primarily studied in life-satisfaction judgments, not multi-attribute decisions.

**Gigerenzer's take-the-best** (Gigerenzer & Goldstein, 1996) formalizes "one-reason decision making" with heterogeneous cues, but was designed for paired-comparison inference (which of two cities is larger?) with binary cues, and is framed as an *adaptive, often optimal* strategy — not a failure mode.

The other constructs are weaker fits: **Tversky's elimination by aspects** uses multiple attributes sequentially (not collapse to one). **Slovic's affect heuristic** collapses to emotion, not to one of the original factors. **Shafir's reason-based choice** describes framing-driven selectivity across *subsets* of attributes, not systematic collapse to one. **Simon's satisficing** operates over alternatives, not attributes. **Hsee's evaluability** depends on evaluation mode (joint vs. separate), a different mechanism. **Dawes' improper linear models** describes using *all* factors with equal weights — the opposite of factor collapse.

**Recommendation:** Replace extension neglect (Kahneman & Frederick, 2002) with the **lexicographic heuristic** (Payne, Bettman & Johnson, 1993) as the primary cognitive science citation. Frame factor collapse as "inadvertent lexicographic processing when compensatory (weighted additive) integration is required." Keep attribute substitution (Kahneman & Frederick, 2002) as the broader framework, and cite the focusing illusion (Schkade & Kahneman, 1998) as the attentional mechanism. This triad — LEX as the structural parallel, attribute substitution as the general framework, focusing illusion as the attentional mechanism — is far stronger than extension neglect alone.

---

## Strongest reviewer objections

Ranked by severity from most to least devastating:

**Objection 1 (Severity: 4/5): The structured weight-reporting methodology is undermined by CoT unfaithfulness.** Turpin et al. (NeurIPS 2023) proved CoT explanations are "systematically unfaithful" — models' stated reasoning does not reliably reflect their actual computational process. Arcuschin et al. (2025) documented Implicit Post-Hoc Rationalization at **7–13%** rates in production models. Barez et al. (2025) argued "CoTs typically omit influential factors and serve only as partial, post-hoc rationalisations." A reviewer would argue: "Self-reported factor weights are unreliable indicators of the actual decision process. The model may internally attend to all factors but *report* a simplified single-factor narrative due to generation dynamics. You cannot distinguish genuine factor collapse from unfaithful weight reporting." **Defense:** The benchmark must demonstrate that factor collapse affects *final answers*, not just reported weights. If factor B should flip the decision but doesn't, the decision itself is wrong — that's not a reporting artifact. Ablation studies removing individual factors and showing the answer doesn't change would conclusively prove the factors aren't influencing the output. This is the single most important methodological control the paper needs.

**Objection 2 (Severity: 4/5): Multi-constraint satisfaction benchmarks already document this phenomenon.** CFBench, RECAST, and DPPM all show performance degrading as simultaneous constraint count increases, with models satisfying some constraints while ignoring others. A reviewer could argue: "Factor collapse is a rebranding of multi-constraint satisfaction failure applied to a decision-making task domain. The underlying phenomenon — models failing to handle N simultaneous requirements — is well-documented. The distinction between 'constraint compliance' and 'factor integration' is a semantic maneuver, not a genuinely different failure mode." **Defense:** The compliance-vs-integration distinction is real and testable. In compliance tasks, each constraint is independently verifiable and constraints don't compete. In factor collapse, factors actively trade off — skill match might favor consultant A while certification requirements favor consultant B. The model must resolve genuine conflicts, not just satisfy a checklist. This distinction must be made crystal clear with concrete examples showing why compliance benchmarks cannot detect factor collapse.

**Objection 3 (Severity: 3.5/5): Factor collapse could be relabeled distractor susceptibility.** Shi et al. (ICML 2023) showed LLMs incorporate irrelevant context; GSM-NoOp showed they use seemingly-relevant-but-irrelevant information. A reviewer could argue the model treats N-1 factors as "noise" and latches onto the single factor most aligned with training-distribution priors. **Defense:** In distractor work, ignored information is genuinely irrelevant. In factor collapse, all N factors are required for the correct answer and the model can retrieve each verbatim. The model isn't failing to filter noise — it's failing to integrate signal. The verbatim-retrieval test is the key differentiator. Include a distractor-susceptibility control condition where some factors are genuinely irrelevant and show the failure pattern differs.

**Objection 4 (Severity: 3/5): The depth-vs-breadth distinction is a semantic maneuver, not a structural insight.** A reviewer might argue that "chain breadth at depth 1" is just a fancy way to say "the model can't handle complex instructions," and that depth vs. breadth is a continuous complexity spectrum, not a categorical distinction requiring separate taxonomic treatment. **Defense:** The failure modes are empirically distinguishable. Depth failures manifest as error accumulation across reasoning steps (each step has some error probability that compounds). Breadth failures manifest as confident collapse to a single factor with no error accumulation — the model doesn't get progressively worse across steps; it immediately collapses. If the paper demonstrates this pattern difference empirically (showing that factor collapse is *not* predicted by task complexity alone but by factor count at fixed depth), the distinction holds.

**Objection 5 (Severity: 2.5/5): Positional effects could explain the entire phenomenon.** "Lost in the Middle" (Liu et al., 2023) and its follow-ups show LLMs systematically underweight information by position. If the "collapsed-to" factor is consistently in position 1 or the final position, factor collapse reduces to positional bias. **Defense:** Randomize factor order across trials. If collapse persists to the *same factor type* regardless of position (e.g., always skill match, never cost), the effect is content-driven, not positional. This is a straightforward and decisive control that should already be in the benchmark design.

---

## Verdict

**REVISE**, then submit.

The core novelty claim — that "factor collapse" represents a previously-undistinguished chain-breadth failure mode in LLM reasoning, taxonomically distinct from chain-depth compositional failures — is **genuinely novel in the taxonomic framing** but stands on a thin empirical ledge without proper controls. No existing paper directly measures or names this specific conjunction of features: N≥3 parallel co-present factors, confident single-factor collapse, verbatim-retrievability of ignored factors, and a structured weight-reporting methodology. The depth-vs-breadth distinction is not made in any existing reasoning failure taxonomy, including the 2026 TMLR survey. This is a real gap.

However, the *underlying phenomenon* — LLMs failing when facing many simultaneous requirements — is well-documented in multi-constraint satisfaction benchmarks. The paper's contribution is therefore primarily **taxonomic and diagnostic** (identifying a specific failure pattern and measurement methodology within a known problem space) rather than the discovery of a wholly new failure category. This is a legitimate scientific contribution — "hallucination" was also just "LLMs being wrong" before it was named and characterized — but it must be positioned honestly. The paper cannot claim to discover that LLMs fail at multi-factor tasks; it must claim to identify *how* they fail (single-factor collapse) and *how to measure it* (structured weight elicitation validated against answer correctness).

The most dangerous threat is **methodological**: if the structured weight-reporting is shown to be unfaithful (per the CoT unfaithfulness literature), the benchmark's core measurement instrument is invalidated. The paper absolutely must include ablation controls showing factor collapse affects final answers, not just self-reported weights, and must control for factor ordering and prompt format effects. With these controls, the paper is publishable at a strong workshop or a D&B track; without them, it will be rejected on methodological grounds alone.

---

## Top 3 specific actions

**1. Add the ablation-based validation layer (critical, do before submission).** For each benchmark instance, run three conditions: (a) all N factors present (measure collapse), (b) each factor individually removed (show the answer doesn't change when non-collapsed factors are removed, proving they weren't influencing the decision), (c) the collapsed-to factor removed (show the answer either changes or the model collapses to a different single factor). This proves factor collapse affects actual decisions, not just reported weights, and neutralizes the CoT unfaithfulness objection.

**2. Replace extension neglect with the lexicographic heuristic as the primary theoretical grounding.** Cite Payne, Bettman & Johnson (1993) *The Adaptive Decision Maker* as the primary cognitive science parallel. Frame factor collapse as "inadvertent lexicographic processing when compensatory integration is required." This eliminates the acknowledged weakness (homogeneous vs. heterogeneous attributes) and provides a much stronger theoretical foundation that reviewers in both ML and cognitive science will recognize.

**3. Add factor-order randomization and explicit compliance-vs-integration comparison.** Randomize factor presentation order across trials to rule out positional effects. Include a parallel "compliance" condition where N constraints must be independently satisfied (no trade-offs) and show the failure pattern differs from the "integration" condition (where factors genuinely compete). This simultaneously neutralizes the "Lost in the Middle" objection and the "this is just multi-constraint satisfaction" objection with a single experimental control.

---

## Papers to read in full

**1. Feuer, B., Tseng, C.-Y., Lathe, A. S., Elachqar, O., & Dickerson, J. P. (2025). "When Judgment Becomes Noise: How Design Failures in LLM Judge Benchmarks Silently Undermine Validity." arXiv:2509.20293.**
Why: Uses the exact term "factor collapse" in an adjacent context (LLM-as-judge psychometric validity). The paper must either cite and distinguish from this usage or potentially benefit from framing "factor collapse" as a phenomenon that manifests across both judging and reasoning tasks. Understanding exactly how Feuer et al. measure and define factor collapse (via factor analysis of score correlation matrices) will sharpen the proposed paper's own definition.

**2. Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023.**
Why: The single most dangerous methodological threat. If the structured weight-reporting methodology cannot survive the unfaithful-CoT critique, the benchmark is dead on arrival. Read this paper to understand exactly what forms of unfaithfulness have been documented, what experimental controls distinguish genuine reasoning from post-hoc rationalization, and how to design the ablation studies that prove factor collapse affects answers, not just reported reasoning.

**3. Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., & Zhou, D. (2023). "Large Language Models Can Be Easily Distracted by Irrelevant Context." ICML 2023. (Plus: Yang et al. (2025), GSM-DC.)**
Why: The primary "relabeling" threat. Factor collapse must be empirically distinguished from distractor susceptibility. Read GSM-IC and GSM-DC to understand their experimental design and evaluation methodology, then design the benchmark's control conditions to demonstrate that factor collapse occurs with *relevant* factors (not distractors) and that the failure pattern is qualitatively different (confident collapse to one factor vs. scattered incorporation of irrelevant information).

**4. Li, L., et al. (2025). "HiddenBench: Assessing Collective Reasoning in Multi-Agent LLMs via Hidden Profile Tasks." arXiv:2505.11556.**
Why: The closest existing benchmark measuring information integration failure for decision-making. HiddenBench tests *distributed* integration (across agents); factor collapse tests *co-present* integration (within a single context). Understanding HiddenBench's methodology, evaluation metrics, and findings will help position factor collapse as the single-agent, co-present-information complement to HiddenBench's multi-agent, distributed-information paradigm. This parallel could strengthen the paper's related work positioning.

**5. Payne, J. W., Bettman, J. R., & Johnson, E. J. (1993). *The Adaptive Decision Maker*. Cambridge University Press.**
Why: The proposed new theoretical backbone. This book formalizes exactly when and why decision-makers switch from weighted-additive (WADD) integration to lexicographic (LEX) single-attribute processing. Understanding the conditions that trigger strategy switching (task complexity, time pressure, number of alternatives) will ground predictions about when factor collapse should occur in LLMs and at what N it should intensify. The WADD-to-LEX switch framework provides the normative benchmark (WADD = correct behavior) and the descriptive model (LEX = factor collapse) that the paper needs.

---

## Sources

Feuer, B., Tseng, C.-Y., Lathe, A. S., Elachqar, O., & Dickerson, J. P. (2025). When Judgment Becomes Noise: How Design Failures in LLM Judge Benchmarks Silently Undermine Validity. arXiv:2509.20293.

Li, L., et al. (2025). HiddenBench: Assessing Collective Reasoning in Multi-Agent LLMs via Hidden Profile Tasks. arXiv:2505.11556.

Shi, F., Chen, X., Misra, K., et al. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. ICML 2023.

Yang, Y., et al. (2025). GSM-DC: Grade School Math with Distracting Context.

Mirzadeh, I., et al. (2024). GSM-NoOp.

Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting. NeurIPS 2023.

Arcuschin, L., et al. (2025). Chain-of-Thought Reasoning In The Wild Is Not Always Faithful.

Barez, F., et al. (2025). Chain-of-Thought Is Not Explainability.

Song, P., et al. (2026). Large Language Model Reasoning Failures. TMLR. arXiv:2602.06176.

Payne, J. W., Bettman, J. R., & Johnson, E. J. (1993). The Adaptive Decision Maker. Cambridge University Press.

Gigerenzer, G., & Goldstein, D. G. (1996). Reasoning the fast and frugal way: Models of bounded rationality. Psychological Review, 103(4), 650–669.

Schkade, D. A., & Kahneman, D. (1998). Does living in California make people happy? A focusing illusion in judgments of life satisfaction. Psychological Science, 9(5), 340–346.

Kahneman, D., & Frederick, S. (2002). Representativeness revisited: Attribute substitution in intuitive judgment. In T. Gilovich, D. Griffin, & D. Kahneman (Eds.), Heuristics and Biases. Cambridge University Press.

Shafir, E., Simonson, I., & Tversky, A. (1993). Reason-based choice. Cognition, 49(1–2), 11–36.

Qiao, S., et al. (2024). CFBench: A Comprehensive Constraints-Following Benchmark for LLMs. arXiv:2408.01122.

Zhang, Q., et al. (2024). ComplexBench. arXiv:2407.03978.

RECAST (2025). arXiv:2505.19030.

DPPM (2025). arXiv:2506.02683.

Zhang, Y., et al. (2026). Logical Phase Transitions: Understanding Collapse in LLM Logical Reasoning. arXiv:2601.02902.

Lu, X., Li, J., Takeuchi, K., & Kashima, H. (2024). AHP-Powered LLM Reasoning for Multi-Criteria Evaluation of Open-Ended Responses. Findings of EMNLP 2024, 1847–1856. arXiv:2410.01246.

Liu, N. F., et al. (2024). Lost in the Middle: How Language Models Use Long Contexts. TACL. arXiv:2307.03172.

Wu, T., et al. (2025). Is Depth All You Need? An Exploration of Iterative Reasoning in LLMs. arXiv:2502.10858.

Echterhoff, J. M., et al. (2024). Cognitive Bias in Decision-Making with LLMs. EMNLP 2024 Findings.

---

## Extended Prior Art (round 2)

> **Scope:** second-pass search targeting 8 under-covered gap areas from the original round 1 check. ~60 WebSearch / WebFetch queries across NeurIPS 2025, ICLR 2025, ACL 2025, EMNLP 2025, arXiv 2024–2026, and domain-specific venues (NEJM AI, npj Digital Medicine, medRxiv, ACL Anthology, ICML 2025). Finance excluded as demo domain per project rules. Every citation below was spot-verified by WebFetch against arXiv abstracts or the ACL Anthology landing page; where a paper surfaced only via search snippet the snippet is flagged.
> **Run date:** 2026-04-11.

---

### Gap area 1 — Multi-attribute decision making in LLMs

**Murthy, S. K., Zhao, R., Hu, J., Kakade, S., Wulfmeier, M., Qian, P., & Ullman, T. (2025). "Cognitive models can reveal interpretable value trade-offs in language models." arXiv:2506.20666.**
Applies a cognitive model of polite speech (informational vs. social utility) to frontier LLMs, measuring how weights on competing utilities shift with reasoning effort and system prompts. Uses a *two-factor* trade-off scaffold (informational vs. social), so N=2 rather than N≥3, and the setup elicits smooth reweighting rather than confident single-factor collapse. **ADJACENT.** Structural difference: two-factor continuous trade-off with behavioral fitting, not N≥3 co-present heterogeneous factors with collapse-or-integrate outcomes. This is the closest cognitive-science-grounded trade-off paper in the literature and should be cited as the nearest methodological cousin.

**Chiu, Y. Y., Jiang, L., & Choi, Y. (2024/2025). "DailyDilemmas: Revealing Value Preferences of LLMs with Quandaries of Daily Life." arXiv:2410.02683. ICLR 2025.**
1,360 everyday moral dilemmas; each presents two actions plus the human values each action implicates, analyzed through five value frameworks (WVS, Moral Foundations, Maslow, Aristotle, Plutchik). Finds LLMs reliably over-weight a narrow subset of "popular" values and exhibit a "collapse of value pluralism in contested scenarios." **ADJACENT (close).** The *phenomenon language* ("collapse of value pluralism") is strikingly close to multi-factor collapse, but structurally each dilemma is a binary action choice, not an N≥3 integrative decision, and the value set is elicited post-hoc from the model rather than supplied as co-present factors at depth 1. Must be cited and distinguished — the overlap in framing vocabulary is a real terminological threat.

**Guzek, K., Horzyk, A., et al. (2025). "User-defined trade-offs in LLM benchmarking: balancing accuracy, scale, and sustainability." *Knowledge-Based Systems*, Elsevier, S0950705125014443 (xLLMBench).**
xLLMBench uses PROMETHEE II (a classical MCDA method) to rank LLMs across accuracy, size, energy, and CO₂. **UNRELATED.** LLMs are the *objects* being ranked, not the subjects exhibiting a reasoning failure. Keyword hit only.

**Wu, K., Aliaga, A. J. G., Sałabun, W., et al. (2025). "Multi-agent systems of large language models as weight assigners: An approach to collaborative weighting in spatial multi-criteria decision-making" (WALMAS). *International Journal of Applied Earth Observation and Geoinformation*, S1195103625000278.**
LLM agents negotiate MCDA criterion weights via IQR-filtered consensus. **UNRELATED.** LLMs are used *as tools* to run MCDA, not as subjects of a collapse evaluation. Same category as Lu et al. 2024.

---

### Gap area 2 — Trade-off reasoning in LLMs

**Li, M., et al. (2025). "Self-Improvement Towards Pareto Optimality: Mitigating Preference Conflicts in Multi-Objective Alignment." ACL 2025 Findings (surfaced via arxiv).**
Studies preference conflicts across multiple reward dimensions during RLHF and proposes Pareto-directed self-improvement. **ADJACENT.** Operates in the *training-time* alignment space (reward aggregation), not inference-time multi-factor decisions. Relevant as upstream cause of downstream collapse but does not measure it.

**Binia, P., et al. (2026). "Behavioral Economics of AI: LLM Biases and Corrections." arXiv:2602.09362.** *[snippet-only, verify before paper citation]*
Documents LLM biased beliefs and heuristic behavior across ChatGPT, Claude, Gemini, Llama; includes anchoring, decoy, and compensatory patterns under cognitive load. **ADJACENT.** Covers several decision heuristics but does not specifically measure single-factor collapse on N≥3 parallel factors. Useful theoretical framing.

**Zhang, X., et al. (2025). "Compensatory Biases Under Cognitive Load: Reducing Selection Bias in Large Language Models." arXiv:2402.01740.** *[snippet-only, verify]*
Shows that LLMs exhibit *increased* bias under cognitive load, mirroring the compensatory/non-compensatory switch in human decision research (Payne Bettman Johnson 1993). **ADJACENT (theoretically important).** This is the closest empirical confirmation in the LLM literature that cognitive load triggers a compensatory-to-non-compensatory switch — the exact mechanism LEX predicts for multi-factor collapse. Should be cited as empirical support for the theoretical mechanism.

---

### Gap area 3 — Attention / salience failures at depth 1 (not positional, not long-context)

**Kargupta, P., Li, S. S., Wang, H., Lee, J., Chen, S., Ahia, O., Light, D., Griffiths, T. L., Kleiman-Weiner, M., Han, J., Celikyilmaz, A., & Tsvetkov, Y. (2025). "Cognitive Foundations for Reasoning and Their Manifestation in LLMs." arXiv:2511.16660.**
Large-scale survey + empirical study of cognitive reasoning foundations in LLMs; identifies that "models narrow to rigid sequential processing on ill-structured problems where diverse representations and meta-cognitive monitoring are critical" and that models "possess behavioral repertoires associated with success but fail to deploy them spontaneously." **ADJACENT (important).** Directly supports the FACET framing that verbatim-retrievable capability does not translate to integrative deployment. Must be cited.

**Du, Y., Tian, M., Ronanki, S., Rongali, S., Bodapati, S., Galstyan, A., Wells, A., Schwartz, R., Huerta, E. A., & Peng, H. (2025). "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval." arXiv:2510.05381. EMNLP 2025 Findings.**
Shows LLM reasoning degrades with input length *even when attention is forced onto only the relevant tokens* (by masking/whitespacing irrelevant context). Degradation of 13.9–85%. **ADJACENT.** Structural difference: still a long-context paper at its core, and collapse is to "no answer / wrong answer," not to one of N heterogeneous factors. But it disentangles length-induced degradation from retrieval failure, which is the same spirit of control the FACET paper needs — useful as a methodological precedent.

**Hoscilowicz, J., Wiącek, A., et al. (2026). "Label Effects: Shared Heuristic Reliance in Trust Assessment by Humans and LLM-as-a-Judge." arXiv:2604.05593.** *[snippet-only, verify]*
Demonstrates attention allocation is *denser on the label region than the content region* in LLM judges — a clean depth-1 salience failure where a single cue dominates. **ADJACENT (mechanistic overlap).** Not multi-factor collapse per se, but evidence that LLMs allocate attention to one cue and ignore the content even when both are required. Reviewer-grade corroboration.

**Gu, X., et al. (ICLR 2025). "When Attention Sink Emerges in Language Models: An Empirical View." arXiv:2410.10781.**
Attention sinks (a small number of tokens capturing most attention mass) emerge as a mechanism to prevent over-mixing/rank collapse in deep transformers. **ADJACENT (mechanistic).** The attention sink is a *low-level architectural* phenomenon on first tokens, not a *task-level* single-factor collapse; but it suggests a mechanistic substrate for why attention concentrates rather than distributes. Worth citing in the discussion of *why* collapse might be expected on mechanistic grounds.

---

### Gap area 4 — Mechanistic interpretability of attention/mode collapse in decision settings

No paper found that directly studies circuit-level mechanisms of multi-factor collapse in LLMs. The mechanistic interpretability literature in 2025–2026 is dominated by:

**Sharkey, L., et al. (2025). "Open Problems in Mechanistic Interpretability."** *[snippet-only, 29-author consensus paper, January 2025]*
Consensus problems list; does not mention multi-factor collapse specifically but lists "understanding failure modes of reasoning" as open. **UNRELATED** for overlap purposes, useful as framing for positioning FACET as an open problem.

**Ameisen, E., et al. (Anthropic, 2025). "Circuit Tracing: Revealing Computational Graphs in Language Models." transformer-circuits.pub/2025/attribution-graphs/methods.html.**
Attribution-graph methodology; tools open-sourced. **UNRELATED.** No decision-context application yet.

**Chen et al. (2026). "Quantifying LLM Attention-Head Stability: Implications for Circuit Universality." arXiv:2602.16740.** *[snippet-only, treat as lead]*
Notes a "stability dip" in middle-layer attention heads where unstable heads become most functionally influential. **UNRELATED** for direct overlap; tangentially relevant to mechanism hypotheses.

**Net for gap 4: no OVERLAPS, and the mechanistic-interpretability literature has *not* touched multi-factor collapse. This is a genuine gap FACET v2 could eventually plug — flag as future work, not v1 scope.**

---

### Gap area 5 — Cognitive science parallels beyond LEX (2024–2026)

Searches for "take-the-best" and "elimination by aspects" applied to LLMs in 2024–2026 returned **zero direct hits**. The one cognitive-heuristic LLM paper that predates the cutoff and is still cited is Macmillan-Scott & Musolesi (2023) "Do Large Language Models Show Decision Heuristics Similar to Humans?" arXiv:2305.04400. **ADJACENT** — covers framing, anchoring, gambler's fallacy, not lexicographic processing on multi-attribute decisions. Already superseded by Echterhoff 2024 in round 1.

**Net for gap 5:** the LEX / Payne-Bettman-Johnson grounding is *still* unclaimed in the LLM literature as of April 2026. The theoretical framing in FACET remains novel. Zhang et al. 2025 (gap 2) is the strongest empirical hook.

---

### Gap area 6 — Domain-specific benchmarks (medicine / legal / logistics)

**Qiu, P., et al. (2025). "MedR-Bench: Benchmarking Medical Reasoning with Structured Patient Cases."** *[referenced in Nature Communications s41467-025-64769-1]*
1,453 structured patient cases across 13 body systems; evaluates exam recommendation, diagnosis, and treatment. **ADJACENT.** Multi-factor in spirit but scored on final diagnosis/treatment correctness — no structured weight elicitation, no measurement of single-factor collapse.

**"SCT-Bench" / Script Concordance Testing benchmark (2025). 750 SCT questions, 10 datasets, compared across 10 LLMs vs. 1,070 students / 193 residents / 300 attendings.** *[Concor.dance public site, snippet]*
SCT measures *how new information revises* a diagnostic judgment under uncertainty — a near-ideal multi-factor integration test. LLMs reportedly underperform relative to their MedQA scores. **ADJACENT (close).** Structural difference: SCT tests *Bayesian update direction* on a single hypothesis given one new piece of evidence, not parallel integration of N≥3 co-present factors. But it is the closest clinical analog and should be cited — and possibly adapted — as the medical-domain instantiation of a multi-factor integration failure.

**Yu, W., Lin, X., Ni, L., Cheng, J., & Sha, L. (2025). "Benchmarking Multi-Step Legal Reasoning and Analyzing Chain-of-Thought Effects in Large Language Models." arXiv:2511.07979. (MSLR / IRAC).**
~1,400 Chinese legal cases, 60K step-level annotations, IRAC-aligned evaluation. **ADJACENT.** Explicitly *sequential* (Issue → Rule → Application → Conclusion), so it measures depth-failure, not breadth. Authors even note that "sequential prompting approaches fail when a legal problem requires holistic evaluation and simultaneous factor weighting" — a sentence that almost exactly describes multi-factor collapse without naming it. **Flag this quote as reviewer-grade evidence that the breadth gap is acknowledged but unmeasured.**

**"PILOT-Bench: A Benchmark for Legal Reasoning in the Patent Domain with IRAC-Aligned Classification Tasks" (2026 arXiv:2601.04758).** *[snippet-only]*
Patent law ex parte appeals; IRAC-structured. **ADJACENT.** Same structural shape as MSLR — sequential IRAC, not parallel multi-factor.

**Guo, J., et al. (2025). "LEXam: Benchmarking Legal Reasoning on 340 Law Exams." arXiv:2505.12864.** *[snippet-only]*
4,886 law-school exam questions (English/German), both MCQ and long-form. **ADJACENT.** Covers legal reasoning but no structured multi-factor integration measurement.

**"R-ConstraintBench: Evaluating LLMs on NP-Complete Scheduling" (2025).** *[ResearchGate 394830746, snippet]*
Resource-Constrained Project Scheduling; evaluates NP-complete feasibility as constraints are added. **ADJACENT** (logistics domain) — but like CFBench it measures *compliance with each constraint*, not *integration across trade-offs*.

**"DeepPlanning: A Challenging Benchmark That Exposes the Limits of LLM Agent Planning" (2026).** *[co-r-e.com 20260128, snippet]*
Travel and shopping planning sandboxes. **ADJACENT.** Multi-step planning failures, not single-shot multi-factor integration.

**"ConstraintLLM: A Neuro-Symbolic Framework for Industrial Constraint Problems." EMNLP 2025 Main, aclanthology.org/2025.emnlp-main.809.** **UNRELATED** for overlap — this is a *solution* framework, not a failure benchmark.

**HELPMed (2025).** *[snippet]* Reports LLM standalone MedQA accuracy of 94.9% collapses to 34.5% with real human participants. **ADJACENT** — interaction-context failure, not factor-integration failure.

---

### Gap area 7 — Calibration under collapse

**"KalshiBench: Do Large Language Models Know What They Don't Know? Evaluating Epistemic Calibration via Prediction Markets." arXiv:2512.16030.** *[snippet-only]*
Tests five frontier models (Claude Opus 4.5, GPT-5.2, DeepSeek-V3.2, Qwen3-235B, Kimi-K2); all systematically overconfident; reasoning enhancements *degrade* calibration. **ADJACENT (important).** Directly supports the "confident collapse" criterion: models report high confidence on wrong answers, and this worsens with reasoning mode. Cite as empirical foundation for calibration-under-collapse assumption.

**"LLMs are Overconfident: Evaluating Confidence Interval Calibration with FermiEval." arXiv:2510.26995 (2025).** *[snippet-only]*
99% nominal intervals cover the true answer only 65% of the time. Models act "as if sampling from a truncated region of their inferred distribution, neglecting its tails." **ADJACENT.** Not multi-factor, but strong empirical grounding for the confidence claim in the FACET definition.

**Yoon, D., Kim, S., et al. (2025). "Reasoning Models Better Express Their Confidence." arXiv:2505.14489.** *[snippet-only]*
Counter-evidence — claims reasoning models are *better* calibrated via slow-thinking dynamics. **ADJACENT (counter-threat).** Creates tension with KalshiBench. FACET must acknowledge this dispute and show whether factor-collapse scenarios specifically break calibration even in reasoning models.

**Zhou, H., et al. (2025). "Benchmarking the Confidence of Large Language Models in Answering Clinical Questions." *JMIR Medical Informatics* 2025;1:e66917.**
Even when accuracy is strong, confidence shows minimal variation between right and wrong answers in clinical QA. **ADJACENT.** Domain-specific confirmation of calibration-under-collapse pattern.

---

### Gap area 8 — 2025–2026 venue papers on parallel / simultaneous constraints

**"Structured Moral Reasoning in Language Models: A Value-Grounded Evaluation Framework." EMNLP 2025 Main, aclanthology.org/2025.emnlp-main.1541 (arXiv:2506.14948).** *[snippet-only]*
Evaluates whether models apply explicit value frameworks consistently across moral vignettes. **ADJACENT.** Related to DailyDilemmas; evaluates consistency of value application, not parallel factor integration.

**"The Pluralistic Moral Gap: Understanding Judgment and Value Differences between Humans and Large Language Models." arXiv:2507.17216 (2025).** *[snippet-only]*
Human responses exhibit consistently higher entropy than LLM responses in moral judgments. **ADJACENT.** Empirical manifestation of collapse in the moral domain (low-entropy = consistent with single-factor weighting) but measured at the population level, not per-decision.

**"Survey on Parallel Reasoning." arXiv:2510.12164 (2025).** Survey of *parallelism in inference compute* (multiple samples, shared attention caches). **UNRELATED** — parallel *computation*, not parallel *factors*. Pure keyword hit, logged for coverage.

**"ParallelSearch" (arXiv:2508.09303), "Learning to Reason Across Parallel Samples" (arXiv:2506.09014).** **UNRELATED.** Same — parallel inference compute.

**"The Illusion of Thinking" (Apple ML Research, 2025, Shojaee et al.).** Compositional complexity collapse at high depth. **ADJACENT** — already a depth-failure paper, orthogonal to FACET's breadth claim; reinforces depth-vs-breadth taxonomic distinction. Cite as evidence the taxonomy is actively contested.

**"Depth Ceiling: On the Limits of Large Language Models in Discovering Latent Planning." arXiv:2604.06427 (2026).** *[snippet-only]*
Finds that scaling improves "planning breadth" (branching) more than "planning depth." **ADJACENT (interesting).** Uses "breadth" in a different sense (search-tree branching, not factor count). Reviewer risk: a reviewer might conflate these usages. **FACET must define "breadth" crisply to avoid confusion.**

---

## Net effect on novelty claim

**The REVISE verdict stands, but the defense perimeter has shifted.** No new paper directly measures multi-factor collapse as defined. The closest new threats and allies:

**Threats (new terminology/methodological proximity):**

1. **Chiu, Jiang & Choi 2024/2025 (DailyDilemmas)** — uses the phrase "collapse of value pluralism" in the LLM context. This is a **second terminological collision** alongside Feuer et al. 2025's "factor collapse." Two independent groups now use "collapse" language for adjacent-but-different phenomena. The naming decision to use **"multi-factor collapse"** is now load-bearing — FACET should cite both Feuer and Chiu in the introduction and distinguish precisely. This strengthens rather than weakens the novelty case: the fact that collapse vocabulary is independently emerging in adjacent contexts is *evidence* the general phenomenon is real and worth naming formally.
2. **Kargupta et al. 2025 (Cognitive Foundations)** — "models possess behavioral repertoires associated with success but fail to deploy them spontaneously." Essentially a generalization of the verbatim-retrievability finding. FACET must cite this and position multi-factor collapse as a specific instance of the broader capability-deployment gap.
3. **Yu et al. 2025 (MSLR legal reasoning)** — explicitly states "sequential prompting approaches fail when a legal problem requires holistic evaluation and simultaneous factor weighting." This is a **direct acknowledgment of the breadth gap in domain-specific literature** without the corresponding benchmark. Gift to the related-work section.
4. **Murthy et al. 2025 (value trade-offs via cognitive model)** — the closest methodological cousin. Uses a cognitive model to elicit trade-off weights. FACET's structured weight-elicitation methodology now has a peer. Requires explicit positioning: Murthy uses a two-utility polite-speech model; FACET uses an N≥3 heterogeneous-factor decision model grounded in LEX/WADD.

**Allies (new empirical/theoretical support):**

5. **Zhang et al. 2025 (Compensatory Biases Under Cognitive Load)** — first empirical LLM evidence that cognitive load triggers a compensatory-to-non-compensatory switch. Exactly the mechanism Payne-Bettman-Johnson predict for human WADD→LEX transitions. **Cite as core theoretical/empirical support.**
6. **KalshiBench / FermiEval** — strong empirical grounding for the "confident collapse" criterion. Yoon et al. 2025 surfaces a dispute (reasoning models *may* be better calibrated). FACET should frame multi-factor collapse as a test case for calibration under one specific failure mode and use the dispute as motivation.

**Honest reassessment:**
- The novelty claim is *slightly stronger* after round 2 because (a) LEX/WADD grounding remains unclaimed, (b) mechanistic interpretability has not touched multi-factor collapse, (c) the closest existing trade-off benchmark (Murthy) is N=2, and (d) domain-specific papers (MSLR) explicitly flag the gap without filling it.
- The novelty claim is *weaker in one specific way*: the collapse-vocabulary collision is now two-papers-deep (Feuer + Chiu), so the naming distinction must be surgical.
- No single new paper forces a re-evaluation from REVISE to REJECT. **Verdict unchanged: REVISE, then submit.**

**Concrete additions for the FACET paper's related work section:**

1. Cite Chiu et al. 2024 (DailyDilemmas) alongside Feuer et al. 2025 and distinguish multi-factor collapse from *value-pluralism collapse* (population-level low entropy across independent dilemmas) and from *judge factor collapse* (psychometric dimension reduction in rubric scoring). Frame all three as instances of a broader "collapse under multi-dimensional integration" family, with FACET testing the specific case of parallel heterogeneous factors in a single decision.
2. Cite Murthy et al. 2025 as the closest methodological cousin for cognitive-model-grounded weight elicitation; distinguish N=2 continuous-utility from N≥3 heterogeneous-factor LEX/WADD.
3. Cite Zhang et al. 2025 (compensatory biases under load) as empirical confirmation of the WADD→LEX switch in LLMs.
4. Cite Kargupta et al. 2025 as general evidence for the capability-deployment gap.
5. Cite Yu et al. 2025 (MSLR) as domain-specific acknowledgment that the breadth gap is recognized but unmeasured; quote the "holistic evaluation and simultaneous factor weighting" line verbatim.
6. Cite KalshiBench and FermiEval as empirical grounding for the confident-collapse criterion; acknowledge the Yoon et al. 2025 counter-finding.
7. Cite Du et al. 2025 (Context Length Alone Hurts) as methodological precedent for disentangling length/position effects from reasoning failures.
8. Cite Gu et al. 2025 (Attention Sink, ICLR 2025) as mechanistic substrate hypothesis — attention concentration on few tokens is a known architectural phenomenon, making task-level factor collapse consistent with known transformer attention distributions.

**One disciplinary note:** gap area 4 (mechanistic interpretability of decision-setting attention collapse) is genuinely empty. No paper in 2025–2026 has traced circuits through a multi-factor decision to show attention collapsing to one factor's tokens. This is an **unclaimed follow-up paper for FACET v2** — do not try to include it in v1, flag in future work.

---

### Verification status of round 2 citations

**WebFetch-verified against arXiv abstracts / ACL Anthology landing pages:**
- arXiv:2506.20666 (Murthy et al.)
- arXiv:2511.07979 (Yu et al., MSLR)
- arXiv:2510.05381 (Du et al., Context Length)
- arXiv:2511.16660 (Kargupta et al., Cognitive Foundations)
- arXiv:2410.02683 (Chiu, Jiang & Choi, DailyDilemmas) — authors verified; N≥3 structural detail needs full-paper read before final citation

**Search-snippet metadata only — verify each by WebFetch before writing into the paper:**
- arXiv:2602.09362 (Binia et al., Behavioral Economics of AI)
- arXiv:2402.01740 (Zhang et al., Compensatory Biases Under Cognitive Load)
- arXiv:2512.16030 (KalshiBench)
- arXiv:2510.26995 (FermiEval)
- arXiv:2505.14489 (Yoon et al., Reasoning Models Better Express Confidence)
- arXiv:2604.05593 (Label Effects / LLM-as-judge attention)
- arXiv:2506.14948 / aclanthology 2025.emnlp-main.1541 (Structured Moral Reasoning)
- arXiv:2507.17216 (Pluralistic Moral Gap)
- arXiv:2505.12864 (LEXam)
- arXiv:2601.04758 (PILOT-Bench)
- R-ConstraintBench (ResearchGate 394830746)
- Chen et al. 2026, arXiv:2602.16740 (Attention-Head Stability)

The spot-verified core citations (Murthy, Yu, Du, Kargupta, Chiu) carry the argument; snippet-only citations are supporting evidence only and must be individually verified before paper submission.

Svoboda, I., & Lande, D. (2024). Enhancing multi-criteria decision analysis with AI: Integrating AHP and GPT-4. arXiv:2402.07404.

---

## Extended Prior Art (round 3) — Legal NLP, LEX/WADD currency, and the closest neighbor

> **Scope:** targeted search (2026-04-11) to close three gaps round 2 left open: (a) legal-NLP coverage, (b) whether PBJ's LEX/WADD is still state-of-the-art in 2026 decision science, (c) whether any pre-2026 paper directly measures multi-factor collapse in legal reasoning. All core citations WebFetch-verified against arXiv / ACL Anthology / Psych Review / publisher pages. Snippet-only citations flagged.

### The closest legal-NLP neighbor (the single most important round-3 find)

**Zhang, L., Grabmair, M., Gray, M., & Ashley, K. D. (2026). "Thinking Longer, Not Always Smarter: Evaluating LLM Capabilities in Hierarchical Legal Reasoning." Proceedings of CSLAW '26, Berkeley, CA, March 3-5, 2026. arXiv:2510.08710.**

Benchmarks LLMs on CATO-style factor hierarchies (Aleven 1997) where factual predicates roll up into abstract legal concerns. Three-task ladder: (1) surface factor identification (high accuracy), (2) hierarchical reasoning (64–92% accuracy), (3) integrated analysis (collapses to 11–34% accuracy). Reports that models expend *more* reasoning tokens on wrong answers than right ones — the "thinking longer, not smarter" pathology in the title. **OVERLAPS — this is the closest legal-NLP neighbor to FACET that currently exists in the literature.**

**Why novelty survives.** Zhang et al. 2026 tests *sequential CATO hierarchies* where factors roll up *argumentatively* through multiple reasoning layers. FACET tests *parallel* N≥3 multi-factor balancing (Hand formula, Wade factors, Rowland factors) where factors must be integrated *simultaneously* via WADD at depth 1. Both find integration-stage collapse. FACET's distinguishing contributions are (a) the *parallel* task structure, (b) the LEX/WADD theoretical frame, (c) the four mandatory controls (ablation, compliance-vs-integration, factor-order randomization, distractor) that Zhang et al. do not run. **Must cite as the immediate prior art.** The Zhang 2026 paper also provides direct empirical cover that the collapse phenomenon is documented in legal-NLP, strengthening (not weakening) the FACET framing.

**FACET's related-work framing, post-round-3:** "The closest existing benchmark is Zhang et al. (2026), which tests LLMs on CATO-style *sequential* factor hierarchies in trade-secret misappropriation. FACET complements this by testing *parallel* multi-factor balancing in tort law, where the Hand-formula, Wade-factor, and Rowland-factor frameworks demand simultaneous integration rather than sequential argumentation. Both benchmarks document integration-stage performance collapse; FACET's theoretical contribution is to frame this collapse as a WADD→LEX switch under cognitive load (Payne, Bettman & Johnson 1993; Lieder & Griffiths 2020)."

### Other legal-NLP must-cites added in round 3

**Gray, M., Zhang, L., & Ashley, K. D. (2025). "Generating Case-Based Legal Arguments with LLMs." Proceedings of CSLAW '25, Munich, March 25-27, 2025. ACM DL 10.1145/3709025.3712216.** Uses trade-secret cases represented as CATO factors; has LLMs generate case-based arguments; expert evaluation. **ADJACENT.** Establishes that the AI-and-law community is porting HYPO/CATO formalisms to LLMs.

**Gray, M. A., Savelka, J., Oliver, W., & Ashley, K. D. (2024). "Using LLMs to Discover Legal Factors." arXiv:2410.07504.** Inductive factor discovery from raw opinions via LLMs. **ADJACENT.** Establishes that "factor" has a precise, non-fuzzy meaning in legal-NLP — exactly what FACET's definition needs to connect with.

**Guha, N., et al. (2023). "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models." NeurIPS 2023 Datasets & Benchmarks Track. arXiv:2308.11462.** 162 tasks, 40 contributors, six reasoning categories. Relevant sub-tasks: `personal_jurisdiction`, `successor_liability`, `learned_hands_torts`, `legal_reasoning_causality`. **ADJACENT (critical to cite).** Each LegalBench task is scored in isolation; there is no multi-factor integration subtask. The `learned_hands_torts` subtask is the closest precursor and measures tort-law *classification* rather than tort-law *balancing*. FACET occupies the parallel-balancing task structure LegalBench explicitly does not.

**Ash, E., Chen, D. L., & Ornaghi, A. (2024). "Gender Attitudes in the Judiciary: Evidence from U.S. Circuit Courts." *American Economic Journal: Applied Economics*, 16(1): 314-50.** Word-embedding "gender slant" measure on judge opinions; correlates slant with reversal rates. **ADJACENT (representative of econometrics-of-law NLP lineage).** A single-paragraph acknowledgment of this lineage is defensive coverage at legal-NLP venues. The lineage measures *judicial behavior*, not LLM capability on multi-factor legal tasks; it is not a novelty threat.

### Additional legal-NLP papers cited as breadth coverage

*[snippet-only — verify each before paper submission]*

- Wang et al. (2025). "A Law Reasoning Benchmark for LLM with Tree-Organized Structures." arXiv:2503.00841. Tree-structured legal reasoning (factum probandum → evidence → experiences). ADJACENT.
- Zhang, A. et al. (2026). "Argumentative Reasoning with Language Models on Non-factorized Case Bases." arXiv:2512.12656. ADJACENT.
- Hijazi et al. (2025). "LegalEval-Q: A New Benchmark for the Quality Evaluation of LLM-Generated Legal Text." arXiv:2505.24826. UNRELATED/ADJACENT.
- Nay et al. (2025). "Evaluating Test-Time Scaling LLMs for Legal Reasoning." ACL Findings 2025 (Findings-EMNLP 742). ADJACENT.
- Shao, Y. et al. (2024). PILOT: Legal Case Outcome Prediction. arXiv:2401.15770. ADJACENT.
- Shu, D. et al. (2024). LawLLM. arXiv:2407.21065. ADJACENT.
- Santosh, T. Y. S. S. et al. (2024). Rethinking LJP in the Era of LLMs. arXiv:2410.10542. ADJACENT.
- Galletta, S. & Ash, E. (2022). Measuring Judicial Sentiment. *Economica* 89(356):1046. ADJACENT.
- Chen, D. L., Moskowitz, T. J., & Shue, K. (2016). Decision Making Under the Gambler's Fallacy. *QJE* 131(3):1181. UNRELATED to FACET (sequential-decision bias, not multi-factor integration) but worth a footnote.
- Savelka, J. & Ashley, K. D. (2022). Legal Information Retrieval for Understanding Statutory Terms. *AI and Law*.

### The negligence-specific gap is literature-verified

**Round 3 confirmed:** there is *no existing LLM benchmark on Hand-formula negligence, Restatement (Third) Torts, Rowland-line duty analysis, or Wade-factor products-liability risk-utility.* This was previously an *assumed* gap; it is now a *literature-verified* gap. Confirmed by (a) LegalBench's `learned_hands_torts` being classification-style, (b) no arXiv hits for Restatement Third Torts × LLM benchmark as of April 2026, (c) Gray et al. 2025 using trade-secret factors rather than tort factors. This is a strong novelty point and should be stated explicitly in the paper's §1.

### LEX/WADD currency check: PBJ is NOT superseded

**Decisive finding:** Payne, Bettman & Johnson (1993) remains a valid primary citation. Resource-rational analysis (Lieder & Griffiths 2020; Krueger, Callaway, Gul, Griffiths & Lieder 2024; Lieder, Callaway & Griffiths 2024) does *not* supersede the LEX/WADD taxonomy — it provides a meta-level account of *when* decision-makers select LEX vs. WADD. The four resource-rational citations below should be added to `PHENOMENON.md` §4 as *complementary* grounding, not as a replacement for PBJ.

**Lieder, F., & Griffiths, T. L. (2020). "Resource-rational analysis: Understanding human cognition as the optimal use of limited computational resources." *Behavioral and Brain Sciences*, 43, e1.** The foundational paper. Reframes heuristics (including LEX) as rational uses of limited compute. Keeps the PBJ heuristic inventory intact.

**Lieder, F., & Griffiths, T. L. (2017). "Strategy Selection as Rational Metareasoning." *Psychological Review*, 124(6): 762-794.** Meta-level model of which strategy the decision-maker selects; assumes LEX/WADD as candidate primitives.

**Krueger, P. M., Callaway, F., Gul, S., Griffiths, T. L., & Lieder, F. (2024). "Identifying resource-rational heuristics for risky choice." *Psychological Review*, 131(4): 905-951.** Derives resource-optimal heuristics for risky gambles. Does not address heterogeneous multi-attribute decisions; cites PBJ as foundational.

**Lieder, F., Callaway, F., & Griffiths, T. L. (2024). *The Rational Use of Cognitive Resources*. Princeton University Press, ISBN 9780691259949.** Book-length synthesis. Builds on, does not replace, the PBJ taxonomy.

**Why this strengthens FACET's theoretical grounding:** if LLMs exhibit a WADD→LEX switch under increasing N, that switch is predicted by both (a) the descriptive PBJ framework (LEX appears under load) and (b) the normative resource-rational framework (LEX is the optimal strategy when integration cost scales super-linearly, which is exactly what attention-based architectures predict). Two independent theoretical frames converging on the same prediction is stronger evidence than either alone.

### Round 3 net assessment

- **Novelty verdict: unchanged, REVISE.** Zhang et al. 2026 narrows the novelty claim from "no existing benchmark measures integration-stage collapse in legal reasoning" to "no existing benchmark measures *parallel* integration-stage collapse in legal reasoning under the LEX/WADD framework, with controls." Both positions are publishable; the latter is sharper.
- **Legal-NLP coverage:** no longer a desk-reject vector. The 10+ legal-NLP papers added above provide adequate coverage for an ACL/EMNLP submission.
- **Theory grounding:** strengthened by resource-rational complement. No revisions forced on PBJ.
- **Negligence gap:** literature-verified. Promote from assumption to claim in §1 of the paper.
- **Instance construction:** unblocked. Real case candidates exist (see `CASE_CANDIDATES.md`) and the primary dataset can be built to the 120-pair target.