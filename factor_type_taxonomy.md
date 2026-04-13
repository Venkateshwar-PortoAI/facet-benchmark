# FACET — Factor Type Taxonomy v1.2

**Domain:** multi-factor tort balancing, covering Hand-formula negligence, Restatement (Third) of Torts §3, Rowland-line duty analysis (Cal. 1968 and adopting states), Wade-factor products-liability risk-utility analysis (36 states post-1965), and Restatement (Second) §520 abnormally-dangerous activity. v1.1 extends the v1.0 taxonomy after case-candidate retrieval revealed that pure Hand-formula cases are N=3 (below the FACET N≥5 floor) and the real scalable instance pools live in the Rowland and Wade lines. Version bumped from v1.0 to v1.1 on 2026-04-11.
**Purpose:** fixed factor-type vocabulary for instance construction (applied during instance construction). Every factor-cluster in a FACET negligence instance must be labeled with exactly one type from this taxonomy. Ad hoc type labels are not permitted.
**Status:** v1.0 draft, fixed for v1 instance construction. Revisions require a version bump and re-annotation.
**Last updated:** 2026-04-11.

---

## How to use this taxonomy

1. When annotating a case, read the appellate opinion's rationale and identify the discrete *considerations* the court weighed.
2. Group raw propositions into factor-clusters .
3. For each cluster, assign exactly one type from the numbered list below. If a cluster seems to span two types, use the decision rules in §3 below to break the tie. If a cluster genuinely does not fit any type, flag it for taxonomy revision — do NOT create an ad hoc type.
4. Record the taxonomy version (`"factor_type_taxonomy_version": "v1.0"`) in every instance.

---

## 1. Core Hand-formula factors (compensatory trio)

These are the three factors that appear in *United States v. Carroll Towing*, 159 F.2d 169 (2d Cir. 1947) itself: B < PL. Every Hand-formula negligence case must include all three.

### 1.1 `burden_of_precaution` (B)

The cost, inconvenience, or utility sacrifice associated with taking the precaution that would have prevented the harm. Includes: monetary cost, time cost, lost utility of the activity, disruption to standard practice, administrative burden.

**Canonical example.** *Carroll Towing* — the cost to the barge owner of keeping a bargee aboard during daylight hours. **Not** the cost of the harm itself (that is `gravity_of_loss`).

**Boundary rule.** If the precaution would impose a cost on a third party rather than the defendant, that cost belongs to `public_policy_externality`, not here. B is the defendant's own cost of taking the precaution.

### 1.2 `probability_of_harm` (P)

The likelihood that the harm would occur in the absence of the precaution. Includes: base rate evidence, prior incidents at the location, industry accident data, foreseeability-conditioned probability.

**Canonical example.** *Carroll Towing* — the probability that a barge left unattended in a crowded harbor during wartime would break loose. **Not** the probability that the specific plaintiff would be harmed (that is `specific_foreseeability`).

**Boundary rule.** If the probability depends on a statistical base rate rather than case-specific evidence, still label as `probability_of_harm`. The distinction between "statistical" and "case-specific" probability is not a taxonomic one.

### 1.3 `gravity_of_loss` (L)

The magnitude of the harm if it occurs. Includes: dollar amount, physical injury severity, number of victims, irreparability, duration of loss.

**Canonical example.** *Carroll Towing* — the value of the barge, its cargo, and any downstream damages from drift collisions. **Not** the plaintiff's particular financial situation (that is `plaintiff_vulnerability`, a sub-factor under `foreseeability_plaintiff`).

**Boundary rule.** If the loss involves physical injury or death, use `gravity_of_loss` rather than splitting into medical-cost and pain-and-suffering sub-types. The taxonomy operates at the legal-reasoning level, not the damages-calculation level.

---

## 2. Modern doctrinal extensions (Restatement Third and case-law additions)

These are factors that do not appear in the bare Hand formula but are routinely weighed in modern negligence analysis. A case may include zero, one, or several of these; they are not mandatory for every instance.

### 2.1 `scope_of_risk` *(merged v1.2)*

*Merges the v1.1 types `foreseeability_plaintiff` and `causal_proximity`, and merges the v1.1 Rowland type `closeness_of_connection` from §2A.4, into a single type with sub-labels. Round 2 face-validity review (finding F4) found that the three were not cleanly separable in modern tort doctrine — Restatement (Third) §29 blurs them under the "scope of risk" framing, and Cardozo's *Palsgraf* majority (duty/foreseeability) vs. Andrews' dissent (causal chain) use the same type in practice. Annotator disagreement on the split would be systematic, not random.*

The question of whether the plaintiff's harm falls within the scope of risk created by the defendant's conduct. Covers three doctrinally-related sub-questions courts sometimes distinguish and sometimes do not:

- **Sub-label `victim_class_foreseeability`:** whether the plaintiff, or the class of plaintiffs to which they belong, was foreseeable as a victim. (v1.1 `foreseeability_plaintiff`; the Cardozo-majority *Palsgraf* question.)
- **Sub-label `causal_chain_proximity`:** whether the causal chain from defendant's conduct to plaintiff's harm is sufficiently direct. (v1.1 `causal_proximity`; the Andrews-dissent *Palsgraf* question; modern intervening-cause analysis.)
- **Sub-label `rowland_closeness`:** Rowland factor 3 "closeness of connection between defendant's conduct and injury." Rowland-line courts use this as a broader consideration that absorbs both of the above under the California duty framing.

**Canonical examples.** *Palsgraf v. Long Island R.R.*, 248 N.Y. 339 (1928). *Petition of Kinsman Transit*, 338 F.2d 708 (2d Cir. 1964). *Rowland v. Christian*, 69 Cal. 2d 108 (1968) factor 3.

**Boundary rule.** Always label as `scope_of_risk`; use the sub-label field to record which framing the court actually used. This preserves the distinction for downstream analysis while avoiding the annotator-disagreement problem.

### 2.2 `third_party_intervening_conduct` *(renamed from v1.1 `third_party_conduct` for clarity; content unchanged from former §2.8)*

Acts of third parties that contributed to the harm, where the court treats them as a separate factor in the balancing rather than as a component of scope-of-risk analysis. If the court treats the third-party act as *breaking* the causal chain, label it under `scope_of_risk` with sub-label `causal_chain_proximity` instead.

### 2.3 `industry_custom`

Adherence to or deviation from industry-standard practice. Not dispositive under *The T.J. Hooper*, 60 F.2d 737 (2d Cir. 1932) — custom is *evidence* of reasonable care, not conclusive of it — but regularly weighed. Includes: published safety standards, trade-association guidelines, common practice in the relevant industry.

**Canonical example.** *The T.J. Hooper* — tugboat operators customarily did not carry radios, but L. Hand held the custom itself was unreasonable.

**Boundary rule.** Regulatory or statutory compliance (as opposed to informal custom) belongs to `regulatory_compliance`, not here.

### 2.4 `regulatory_compliance`

Adherence to or violation of statutes, regulations, codes, or licensing requirements relevant to the defendant's conduct. Statutory violation may establish negligence per se in some jurisdictions; regulatory compliance is *evidence* of due care but not a complete defense.

**Canonical example.** A product manufacturer that complied with FDA labeling requirements but is still sued for failure to warn.

**Boundary rule.** If the court treats statutory violation as fully dispositive (negligence per se), flag the instance as a dominant-factor case and exclude from the primary dataset — it fails the dominance threshold (no factor > 0.5 of decision weight).

### 2.5 `alternative_precautions`

Availability, cost, and effectiveness of other precautions the defendant could have taken instead of or in addition to the one at issue. Distinct from `burden_of_precaution` in that B is the cost of *a specific* precaution, while this factor is about the *menu* of alternatives.

**Canonical example.** *McCarty v. Pheasant Run*, 826 F.2d 1554 (7th Cir. 1987) — Posner's analysis of what alternative hotel security measures were available and their respective costs.

**Boundary rule.** If the court discusses only one precaution, this factor is absent. If the court discusses a menu and weighs alternatives against each other, it is present.

### 2.6 `public_policy_externality`

Public-policy considerations that bear on whether liability should attach, distinct from the private cost-benefit of the Hand formula. Includes: chilling effects on socially valuable activity, distributional concerns, incentive effects on third parties, floodgates concerns.

**Canonical example.** Courts reluctant to impose liability on emergency responders because of chilling effects on emergency response.

**Boundary rule.** If the policy consideration is about allocating costs between the defendant and *the plaintiff*, label as `burden_shifting` (2.9). If it is about allocating costs to *third parties or society*, use this type.

### 2.7 `defendant_knowledge`

What the defendant actually knew or should have known about the risk at the time of the conduct. Distinct from `foreseeability_plaintiff` in that knowledge is about the defendant's epistemic state, not the plaintiff's foreseeability.

**Canonical example.** A manufacturer with internal studies showing a product defect but no public warning.

**Boundary rule.** Constructive knowledge (what the defendant *should* have known) goes here. If the court frames the issue as pure foreseeability without knowledge-state language, use `probability_of_harm` instead.

### 2.8 *(renumbered — see §2.2 `third_party_intervening_conduct` above)*

*In v1.2 this section was consolidated with §2.2 after the scope-of-risk merge. The content moved to §2.2.*

### 2.9 `burden_shifting`

Considerations about who should bear the cost of the harm as between the defendant and plaintiff, independent of fault. Includes: enterprise liability, cheapest-cost-avoider reasoning, loss-spreading arguments, least-cost-insurer reasoning.

**Canonical example.** Cost-benefit analysis that explicitly invokes which party is better positioned to insure or spread the loss.

**Boundary rule.** This is an explicit doctrinal move some courts make and others reject. Use only if the court's rationale explicitly invokes it — do not infer.

### 2.10 `comparative_fault`

The plaintiff's own negligence, to the extent the jurisdiction recognizes comparative or contributory fault and the court treats it as a separate factor in the balancing rather than a pure affirmative defense.

**Canonical example.** A pedestrian who steps into traffic and a driver who was speeding — modern comparative-fault analysis weighs the plaintiff's conduct against the defendant's.

**Boundary rule.** In pure contributory-negligence jurisdictions (still relevant in a handful of states), plaintiff fault is not a factor but a complete bar — those cases are flagged and handled separately in a jurisdictional filter, not forced into this type.

---

## 2A. Rowland-line duty factors (added v1.1)

The California Supreme Court's *Rowland v. Christian*, 69 Cal. 2d 108 (1968) established a 7-factor duty test that has been adopted (with variations) by approximately ten state supreme courts. These factors appear in duty-analysis cases that do not involve the Hand formula directly. Every Rowland-line instance should label each cluster with one of the types in §1, §2, or §2A.

### 2A.1 `certainty_of_injury`

The certainty (as opposed to foreseeability or probability) that the plaintiff suffered injury. Factor 2 of Rowland. Distinguished from `probability_of_harm` (§1.2) because certainty is retrospective and evidentiary — "did the harm actually happen and can we prove it?" — while probability is prospective.

**Canonical example.** *Rowland v. Christian* — the plaintiff actually suffered a cut tendon requiring surgery; the certainty of that injury is not in doubt.

**Boundary rule.** In cases where injury is contested or minimal, weight this factor heavily. In cases where injury is stipulated, weight it low — it is a near-zero factor in the balancing but still listed for completeness.

### 2A.2 `moral_blame`

The moral blameworthiness of the defendant's conduct, independent of its objective risk profile. Factor 4 of Rowland. Distinguished from `defendant_knowledge` (§2.7) because moral blame is normative (was the defendant *culpable*?) while knowledge is epistemic (did the defendant *know*?).

**Canonical example.** *Tarasoff v. Regents* — the court weighed whether the therapist's failure to warn was morally blameworthy given the confidentiality obligation, independent of whether he knew the victim was identifiable.

**Boundary rule.** If the court discusses intent, recklessness, or willful disregard, use this type. If the court discusses mere negligence without moral-blameworthiness framing, omit this type from the instance.

### 2A.3 `insurance_availability`

Availability, cost, and prevalence of insurance for the risk at issue. Factor 7 of Rowland. Related to but distinct from `burden_shifting` (§2.9) — insurance availability is about whether loss-spreading is *possible*, while burden-shifting is about whether it is *normatively appropriate*.

**Canonical example.** Courts weigh whether imposing liability will force defendants to purchase insurance that is available at reasonable cost, as a policy check on liability expansion.

**Boundary rule.** This factor is almost always present in Rowland-line cases (by doctrine) but often weighted near zero because insurance is universally available for most risks. Track it as present-but-low-weight in most Rowland instances.

### 2A.4 *(merged into §2.1 `scope_of_risk` sub-label `rowland_closeness` in v1.2)*

*After round 2 face-validity review, Rowland factor 3 "closeness of connection" was merged into the unified `scope_of_risk` type (§2.1) with sub-label `rowland_closeness`. Annotators on Rowland-line cases should label this consideration as `scope_of_risk` with `sub_label: rowland_closeness`. The merge eliminates the v1.1 problem that a single *Palsgraf*-style case could receive different type labels depending on whether the annotator read it as foreseeability, causal proximity, or Rowland closeness.*

---

## 2B. Wade-factor products-liability factors (added v1.1)

The seven Wade factors (from John Wade's 1973 article "On the Nature of Strict Tort Liability for Products" and formally adopted in *Cepeda v. Cumberland Engineering*, 76 N.J. 152 (1978) and *O'Brien v. Muskin*, 94 N.J. 169 (1983)) provide the canonical risk-utility test for design-defect claims. Most Wade factors map onto types already defined in §1 and §2, but two are distinct enough to warrant their own types.

### 2B.1 `product_utility`

The usefulness and desirability of the product to the user and to the public. Factor 1 of the Wade test. Distinct from `burden_of_precaution` (§1.1) because utility is about the *benefit* of the product, not the *cost* of the precaution. A product with low utility and modest harm potential might be defectively designed even if the precaution cost is high.

**Canonical example.** *O'Brien v. Muskin* — the above-ground pool's utility (recreation, exercise) was weighed against the diving-injury risk.

**Boundary rule.** This is always present in a Wade-factor products case and is a foundational weight. Do not omit unless the case is not a design-defect case.

### 2B.2 `user_awareness`

The user's anticipated awareness of the dangers inherent in the product, given its intended use and the warnings provided. Factor 6 of the Wade test. Distinct from `comparative_fault` (§2.10) because user awareness is about the *user's informational state at the moment of use*, while comparative fault is about the user's *conduct* during the harmful event.

**Canonical example.** *Voss v. Black & Decker* — the user's knowledge that a circular saw without a guard could cause kickback was weighed against the manufacturer's duty to guard.

**Boundary rule.** If the court discusses warnings, labels, instructions, or common knowledge of the risk, use this type. If the court discusses the user's contributory conduct (using the product against the warning), use `comparative_fault`.

### 2B.3 Mapping of other Wade factors to existing types

The remaining five Wade factors map onto types already defined:

- **Wade 2 (safety aspects: likelihood and seriousness of injury)** → split between `probability_of_harm` (§1.2) and `gravity_of_loss` (§1.3).
- **Wade 3 (availability of substitute product)** → `alternative_precautions` (§2.5).
- **Wade 4 (ability to eliminate unsafe character without impairing utility or unreasonable cost)** → `burden_of_precaution` (§1.1).
- **Wade 5 (user's ability to avoid danger)** → `comparative_fault` (§2.10) or `user_awareness` (§2B.2) depending on framing.
- **Wade 7 (feasibility of spreading loss)** → `burden_shifting` (§2.9).

When a court's opinion uses Wade-factor terminology, label the cluster with the mapped FACET type and record the Wade-factor number as a `wade_factor_origin` metadata field on the cluster (recorded as metadata in the instance schema).

---

## 3. Tie-breaking rules for cluster-to-type assignment

*Revised 2026-04-11 after round 2 face-validity review finding F5: the v1.1 global Hand-preference biased the corpus by pushing Rowland-language cases onto Hand-formula types. v1.2 makes the tie-breaker doctrine-specific.*

When a cluster seems to span multiple types, apply these rules in order:

1. **Doctrine-specific preference first.** Determine which doctrinal framework the case sits in:
   - *If the case is a Hand-formula case* (Carroll Towing line, federal admiralty, economic-analysis opinions): prefer the §1 Hand types (B, P, L) and §2 modern-doctrinal types.
   - *If the case is a Rowland-adopting-state duty case* (California, Hawaii, Minnesota, Washington, and other adopting jurisdictions): prefer §2A Rowland-specific types and treat §1 Hand types as secondary unless the court's language explicitly uses Hand terminology.
   - *If the case is a Wade-factor products-liability case* (any state that has adopted risk-utility, 36 states as of 2026): prefer §2B Wade-specific types.
   - *If the case straddles frameworks* (rare, usually a choice-of-law situation): label with the framework the court actually applied, recording the alternative in a `framework_alternative_label` metadata field on the cluster.
2. **Use the court's own language.** If the opinion explicitly uses a term that maps to a taxonomy type, use that type. This rule is stronger than rule 1 in direct conflicts.
3. **Prefer the more specific type within the selected framework.** Within a chosen framework, use the narrower-scope type when the factor's propositional content is narrower.
4. **If genuinely ambiguous, flag for taxonomy revision.** Do not invent a new type, do not pick arbitrarily. Leave the cluster labeled `UNRESOLVED` and log it in `taxonomy_ambiguities.md`. After every 20 instances, review the log and either add a new type (with version bump) or add a new boundary rule (no version bump).

### 3.1 Decision-tree workflow for annotators *(added v1.2 after round 2 review finding F11)*

To keep the working vocabulary manageable, annotators use a decision tree rather than scanning all 17 types per cluster:

```
START — read the case
   │
   ├── Is this a Hand-formula or federal-admiralty case?
   │   └── YES → working vocabulary is §1 + §2 (13 types)
   │
   ├── Is this a Rowland-adopting-state duty case?
   │   └── YES → working vocabulary is §1 + §2 + §2A (16 types)
   │
   └── Is this a Wade-factor products-liability case?
       └── YES → working vocabulary is §1 + §2 + §2B (15 types)
```

Most clusters in most cases can be labeled from a ~10-type working vocabulary without consulting the full 17-type list.

### 3.2 Weight floor for N-counting *(added v1.2 after round 2 review finding F7)*

A factor-cluster's in-case weight must be **≥0.05** to count toward the decision-relevant N in the decision-relevance criterion. Factors below the floor are recorded in the instance for completeness (they appear in the `factors` array with their weight) but do not count toward the N≥5 floor or the ⌈N/2⌉ counterfactual-flip requirement.

**Why this matters:** Rowland factors 2 (`certainty_of_injury`) and 7 (`insurance_availability`) are doctrinally mandated but substantively near-zero in ~80% of cases. Without the floor, every Rowland case claims N=7 when the substantive analytical N is 5. The N-sweep analysis in the N-sweep analysis would treat this as real signal, inflating the measured phase-transition.

---

## 4. What this taxonomy excludes (and why)

Factors that might appear in a negligence case but do NOT get their own taxonomy type:

- **Damages calculation factors** (medical costs, lost wages, pain and suffering). These belong to the damages phase, not the liability phase. FACET measures liability reasoning, not damages arithmetic.
- **Procedural factors** (burden of proof, evidentiary rulings, standard of review). Not substantive balancing factors.
- **Jurisdictional variation** (which state's law applies). Handled by a jurisdiction field on the instance, not as a factor.
- **Credibility determinations** (whether witnesses were believed). Not substantive factors; handled by treating the court's factual findings as given.

---

## 5. Version history

- **v1.0 (2026-04-11):** initial taxonomy. 13 types: 3 Hand-formula core + 10 modern-doctrinal.
- **v1.1 (2026-04-11):** extended after case-candidate retrieval found pure Hand-formula cases are N=3 and the scalable instance pools are Rowland-line duty cases and Wade-factor products-liability cases. Added 4 Rowland-specific types (§2A: certainty_of_injury, moral_blame, insurance_availability, closeness_of_connection) and 2 Wade-specific types (§2B: product_utility, user_awareness). Remaining Wade factors mapped onto existing types via §2B.3. Total: **19 types** (3 Hand core + 10 modern-doctrinal + 4 Rowland + 2 Wade).
- **v1.2 (2026-04-11):** revised after a second face-validity review. Major changes:
  - **Type merge:** `foreseeability_plaintiff` (§2.1 old), `causal_proximity` (§2.2 old), and `closeness_of_connection` (§2A.4 old) merged into a single `scope_of_risk` type (§2.1 new) with three sub-labels. Round 2 found these were not cleanly separable in modern tort doctrine and annotator disagreement would be systematic.
  - **Doctrine-specific tie-breaking.** v1.1 rule 1 preferred Hand types globally. v1.2 §3 rule 1 picks the preferred-type set from the case's actual doctrinal framework (Hand/Rowland/Wade), eliminating the v1.1 bias toward Hand-formula reading of Rowland-language cases.
  - **Decision-tree annotator workflow (§3.1).** Working vocabulary for any given case is ~10 types from a doctrine-specific subset, not all 17 types scanned per cluster.
  - **Weight floor (§3.2).** Factors must have in-case weight ≥0.05 to count toward N. Rowland stub factors (certainty, insurance) are recorded but excluded from the decision-relevant N count.
  - **Total: 17 types** (3 Hand core + 9 modern-doctrinal after third_party merge into scope_of_risk + 3 Rowland-specific after §2A.4 merge + 2 Wade-specific). Net: down 2 from v1.1 via consolidation.
  - Still must pass the 20-instance pilot without more than 10% of clusters landing in `UNRESOLVED`. Still needs real human torts-scholar review — stand-in reviews cannot close the practitioner face-validity question definitively.
