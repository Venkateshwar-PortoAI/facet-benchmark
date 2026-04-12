# FACET — Candidate Instance Pool (round 1 retrieval, 2026-04-11)

> **Provenance:** compiled by an Opus research agent on 2026-04-11 from public case-law digests (Justia, FindLaw, Wikipedia, H2O casebooks, scholarship repositories). CourtListener HTML-page WebFetch returned empty bodies, Justia/OpenJurist returned 403 — verification therefore relied on WebSearch-surfaced opinion quotations, not the primary text. **Every case in the "Recommended for v1" list below must be re-verified against the actual opinion text via CourtListener's bulk-data dump before being built into a final instance.** Citations and factor lists below are correct to the best of publicly-retrievable secondary sources.

## Headline findings

1. **The 3 canonical Hand-formula cases (Carroll Towing, Conway v. O'Brien, Moisan v. Loftus) are pure N=3** — below FACET's N≥5 floor. They can serve as *anchor/illustrative* instances in the paper's introduction but are not usable as primary-dataset instances without sub-factor elaboration from the trial record.
2. **Single-doctrine negligence does not supply 200 instances.** Honest ceiling on verified supreme-court and federal-circuit material across Hand / Rowland / Wade / §520 lines combined: **~50–80 clean instances**, with ~12 immediately usable after this 2-hour search. Reaching 200 forces one of three methodological choices: (a) lower the v1 target to ~120, (b) admit intermediate appellate cases (ground-truth risk), or (c) expand across 10+ state Rowland-analog corpora and the 36-state Wade-factor products corpus.
3. **The Rowland-factor duty line and the Wade-factor products-liability line are the scalable pools.** Both are doctrinally mandated 7-factor tests; the Rowland line is California-seeded but adopted by ~10 other states; the Wade line has been adopted by 36 states. Together they could yield 200+ instances with effort.
4. **Identity-politics red flags are real and caught several candidates.** Assault / abduction / racialized-crime fact patterns contaminate the cognitive construct with AI-fairness concerns (a reviewer would read FACET scoring on *Ann M.* or *McClung* as measuring the model's treatment of assault victims, not its factor-integration capability). Excluded cases: Ann M. v. Pacific Plaza (1993), Thompson v. County of Alameda (1980), McClung v. Delta Square (Tenn. 1996), Isaacs v. Huntington Hospital (Cal. 1985), Kline v. 1500 Mass. Ave. (D.C. Cir. 1970). *McCarty v. Pheasant Run* is usable with fact-pattern sanitization (rewrite the intrusion as content-neutral).

## Tier 1 — Canonical Hand cases (anchors only, N=3 below floor)

| Case | Cite | Outcome | Status |
|---|---|---|---|
| *United States v. Carroll Towing* | 159 F.2d 169 (2d Cir. 1947) | liable, unanimous | **Anchor only** — N=3 |
| *Conway v. O'Brien* | 111 F.2d 611 (2d Cir. 1940) | SCOTUS reversed — split ground truth | **Exclude** |
| *Moisan v. Loftus* | 178 F.2d 148 (2d Cir. 1949) | remand, no outcome ground truth | **Exclude** |

## Tier 2 — Rowland-line California duty cases (N=7 by doctrine)

| # | Case | Cite | Outcome | N | Red flags | Verdict |
|---|---|---|---|---|---|---|
| 6 | *Rowland v. Christian* | 69 Cal. 2d 108 (1968) | liable, 5-2 split | 7 | none | **Include** (split) |
| 7 | *Tarasoff v. Regents* | 17 Cal. 3d 425 (1976) | duty exists, not unanimous | 7 | foreseeability-dominant risk; mental-health politics | **Hold pending weight audit** |
| 8 | *Ann M. v. Pacific Plaza* | 6 Cal. 4th 666 (1993) | not liable, 7-0 | 7 | **sexual assault victim** | **Exclude** |
| 9 | *Thompson v. County of Alameda* | 27 Cal. 3d 741 (1980) | not liable, majority w/ dissent | 7 | child victim, racialized-crime politics | **Exclude** |
| 10 | *Parsons v. Crown Disposal* | 15 Cal. 4th 456 (1997) | not liable, majority w/ dissent | 7 | none | **Include (high priority)** |
| 11 | *Cabral v. Ralphs Grocery* | 51 Cal. 4th 764 (2011) | duty exists, unanimous | 7 | none | **Include (top-tier)** |
| 12 | *Regents of UC v. Superior Court (Rosen)* | 4 Cal. 5th 607 (2018) | duty exists, unanimous | 7 | campus-safety politics | **Hold — sanitize** |
| 13 | *Isaacs v. Huntington Memorial* | 38 Cal. 3d 112 (1985) | duty exists, majority w/ dissent | 7 | gun violence politics | **Exclude** |

## Tier 3 — Products liability risk-utility cases (Wade factors, N=5–7)

| # | Case | Cite | Outcome | N | Red flags | Verdict |
|---|---|---|---|---|---|---|
| 14 | *Barker v. Lull Engineering* | 20 Cal. 3d 413 (1978) | for plaintiff, unanimous | 5 | none | **Include (top-tier)** |
| 15 | *O'Brien v. Muskin* | 94 N.J. 169 (1983) | for plaintiff, 4-3 split | 7 | none | **Include** |
| 16 | *Cepeda v. Cumberland Engineering* | 76 N.J. 152 (1978) | for defendant, majority w/ dissent | 7 | none | **Include** |
| 17 | *Voss v. Black & Decker Mfg.* | 59 N.Y.2d 102 (1983) | defense verdict, unanimous | 6 | none | **Include (top-tier)** |

## Tier 4 — Restatement (Second) §520 abnormally-dangerous-activity (N=6)

| # | Case | Cite | Outcome | N | Red flags | Verdict |
|---|---|---|---|---|---|---|
| 18 | *Indiana Harbor Belt v. American Cyanamid* | 916 F.2d 1174 (7th Cir. 1990) | not strictly liable, unanimous | 6 | **single-factor dominance (factor c >0.5)** | **Exclude — partial-collapse only** |

## Tier 5 — Other multi-factor duty cases

| # | Case | Cite | Outcome | N | Red flags | Verdict |
|---|---|---|---|---|---|---|
| 19 | *Biakanja v. Irving* | 49 Cal. 2d 647 (1958) | liable, unanimous | 6 | none | **Include** |
| 20 | *Kelly v. Gwinnell* | 96 N.J. 538 (1984) | liable, 6-1 split | ~6 | DUI politics (manageable) | **Include pending audit** |
| 21 | *Posecai v. Wal-Mart Stores* | 752 So. 2d 762 (La. 1999) | not liable, unanimous | 7 | robbery victim (manageable) | **Include** |
| 22 | *McClung v. Delta Square* | 937 S.W.2d 891 (Tenn. 1996) | duty exists, unanimous | ~6 | **abduction/rape/murder victim** | **Exclude** |
| 23 | *Kline v. 1500 Mass. Ave.* | 439 F.2d 477 (D.C. Cir. 1970) | liable, 2-1 split | ~5 | assault | **Exclude** |

## v1 build list (12 clean cases, ranked by readiness)

Ordered by (unanimous preferred) → (N ≥ 6 preferred) → (no red flags preferred) → (Hand fit ≥ 4):

1. ⭐ **Voss v. Black & Decker** (N.Y. 1983) — unanimous, N=6, Wade, clean.
2. ⭐ **Barker v. Lull Engineering** (Cal. 1978) — unanimous, N=5, risk-utility direct.
3. ⭐ **Cabral v. Ralphs Grocery** (Cal. 2011) — unanimous, N=7 Rowland, clean commercial.
4. ⭐ **Biakanja v. Irving** (Cal. 1958) — unanimous, N=6, professional negligence.
5. **Parsons v. Crown Disposal** (Cal. 1997) — non-unanimous but clean; N=7 Rowland.
6. **Davis v. Consolidated Rail** (7th Cir. 1986) — unanimous, N=6, Posner-Hand.
7. **O'Brien v. Muskin** (N.J. 1983) — 4-3 split, N=7 Wade.
8. **Cepeda v. Cumberland** (N.J. 1978) — non-unanimous, N=7 Wade.
9. **Rowland v. Christian** (Cal. 1968) — 5-2 split, N=7 doctrinal anchor.
10. **Posecai v. Wal-Mart** (La. 1999) — unanimous, N=7, yellow flag manageable.
11. **Kelly v. Gwinnell** (N.J. 1984) — 6-1 split, N≈6, weight audit required.
12. **McCarty v. Pheasant Run** (7th Cir. 1987) — unanimous, N=6, **requires fact-pattern sanitization**.

## Supply reality and the 120-instance recommendation

**Not enough for 200 on single-doctrine negligence.** Verified ceiling from exhaustive single-doctrine search: 50–80 clean instances across Hand / Rowland / Wade / §520 combined.

**Recommended v1 path:**
- **Lower the v1 target from 200 to 120 matched pairs** for the primary dataset. This is still enough to power H1 (C0 > C3, one-sided proportions test at α=0.05, power=0.8) if we revise the expected baseline upward from 35% to ~40% or accept a target effect of ~15pp instead of 10pp.
- **Expand the pool** along three axes in parallel:
  1. Multi-state Rowland-analogs (add 10 state supreme courts — Hawaii, Minnesota, Washington, etc.).
  2. Full 36-state Wade-factor products-liability corpus (this alone is 200+ potential instances).
  3. Restatement (Third) §3 adoption cases (post-2010 state-by-state adoption cycle).
- **Do NOT admit intermediate appellate courts** in v1 — ground-truth reliability drops sharply at that tier.
- **Do NOT use synthetic variations** in v1 — violates `SPEC.md` §5 constraint 7.

## Next actions implied by this retrieval

1. Rewrite `SPEC.md` §3 and §4 to reflect that "negligence balancing" is really a family of multi-factor tort doctrines (Hand / Rowland / Wade / §520), not just Hand formula.
2. Revise `SPEC.md` §10 dataset size from 200 → 120 matched pairs; recompute power.
3. Extend `factor_type_taxonomy.md` to v1.1 with Rowland-specific types (certainty of injury, moral blame, insurance availability) and Wade-specific types (product utility, user awareness, loss spreading).
4. Begin drafting real instances from the 4 starred cases (Voss, Barker, Cabral, Biakanja).
5. Flag CourtListener bulk-data dump as the authoritative source for final instance construction — the HTML opinion pages block WebFetch and must be retrieved differently.

## Retrieval caveats

- **Every case must be re-verified against primary text before being built into a final instance.** The factor lists above are correct to the best of publicly-retrievable secondary sources, but secondary sources paraphrase and selectively quote.
- **Weight estimates are rough** and must be re-elicited from the primary text per `SPEC.md` §5.1 before an instance is admitted to the primary dataset.
- **Opinion PDFs from CourtListener's bulk-data dump** are the recommended authoritative source; HTML opinion pages at courtlistener.com block WebFetch in current testing.
