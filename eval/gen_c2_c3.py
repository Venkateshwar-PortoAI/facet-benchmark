#!/usr/bin/env python3
"""
FACET — C2 perturbation + C3 compliance generator

Takes a base instance JSON (facet-neg-XXXX.json) and generates:
  - instances/perturbations/facet-neg-XXXX-c2.json
  - instances/compliance/facet-neg-XXXX-c3.json

using template heuristics. For v1 the templates are literal neutral
rewrites; a human reviewer should tighten them later.

Usage:
  python3 eval/gen_c2_c3.py facet-neg-0006 facet-neg-0007 ...
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTANCES = ROOT / "instances"


def neutral_rewrite_for_factor(factor: dict) -> str:
    """Produce a doctrinally-neutral rewrite of a factor's text. The rewrite
    preserves the factor's presence in the instance but removes its
    directional push."""
    factor_type = factor.get("factor_type", "factor")
    return (
        f"Whether this consideration ({factor_type.replace('_', ' ')}) "
        f"supports or opposes the outcome is treated by the court as "
        f"neither clearly established nor clearly refuted on this record; "
        f"the factor is present but is not developed as a load-bearing "
        f"element of the analysis."
    )


def build_c2(instance: dict) -> dict:
    inst_id = instance["instance_id"]
    perturbations = []
    for i, f in enumerate(instance["factors"]):
        var_id = f"{inst_id}-c2-{f['factor_id']}"
        perturbations.append({
            "variant_id": var_id,
            "perturbed_factor_id": f["factor_id"],
            "perturbed_factor_type": f["factor_type"],
            "base_weight": f.get("in_case_weight_estimate", 0),
            "base_directionality": f.get("directionality", ""),
            "original_text": f["text"],
            "neutral_rewrite": neutral_rewrite_for_factor(f),
            "perturbation_note": f"Auto-generated template rewrite for factor {f['factor_id']} ({f['factor_type']}). Human review recommended before final dataset admission.",
            "is_stub_factor": f.get("is_stub_factor", False),
        })

    return {
        "base_instance_id": inst_id,
        "base_case": instance.get("source_case") or instance.get("base_case") or inst_id,
        "perturbation_type": "c2_weight_perturbation_neutral_rewrite",
        "protocol_version": "FACET v0.4",
        "taxonomy_version": "v1.2",
        "constructor": "Venkateshwar Reddy Jambula (drafted with Claude Opus as programming and writing assistant; auto-generated from base instance)",
        "construction_date": "2026-04-11",
        "status": "draft_pending_primary_text_verification",
        "perturbations": perturbations,
        "reconstruction_check_prompt": (
            "Does the case description above omit any factor you believe a court would "
            "typically weigh in this analysis? If yes, name the omitted factor and "
            "explain what weight you would assign it. If no, say so."
        ),
        "construction_notes": [
            "Generated via eval/gen_c2_c3.py — template-based neutral rewrites.",
            "Human annotator review recommended before final dataset admission.",
            "Reconstruction-check disqualification (FACET v0.4) applies at eval time.",
        ],
    }


def build_c3(instance: dict) -> dict:
    inst_id = instance["instance_id"]
    reqs = []
    for i, f in enumerate(instance["factors"]):
        req_id = f"R{i+1}"
        reqs.append({
            "requirement_id": req_id,
            "maps_to_base_factor": f"{f['factor_id']} ({f['factor_type']})",
            "requirement_text": (
                f"The record must establish that the consideration "
                f"'{f['factor_type'].replace('_', ' ')}' clearly supports the "
                f"outcome direction that its base directionality indicates "
                f"({f.get('directionality', 'unspecified')}). Treat this as an "
                f"independent yes/no compliance check; do not aggregate with "
                f"other requirements."
            ),
            "independently_checkable": True,
            "expected_answer": "contested" if f.get("is_stub_factor") else "yes",
            "compliance_construction_note": (
                "Auto-generated template. Requirement maps the base factor's "
                "directionality to a yes/no compliance rule; may need tightening "
                "for factors whose directionality is mixed or unspecified."
            ),
        })

    return {
        "instance_id": f"{inst_id}-c3",
        "base_instance_id": inst_id,
        "base_case": instance.get("source_case") or instance.get("base_case") or inst_id,
        "condition": "C3_compliance_matched_parallel",
        "doctrinal_framework_source": instance.get("doctrinal_framework", "unspecified"),
        "taxonomy_version": "v1.2",
        "factor_type_taxonomy_version": "v1.2",
        "status": "draft_pending_primary_text_verification",
        "construction_date": "2026-04-11",
        "constructor": "Venkateshwar Reddy Jambula (drafted with Claude Opus as programming and writing assistant; auto-generated from base instance)",
        "case_background": instance.get("case_background", ""),
        "compliance_requirements": reqs,
        "question": f"Are all {len(reqs)} compliance requirements above independently satisfied?",
        "ground_truth": {
            "answer": "varies_by_instance",
            "rationale": "Auto-generated C3; review each requirement individually before eval.",
        },
        "construction_notes": [
            "Generated via eval/gen_c2_c3.py — template-based compliance rephrasings.",
            "Human annotator review recommended.",
            "Literal-application instruction in the eval harness (FACET v0.5) "
            "produces cleaner C3 counts regardless of template tightness.",
        ],
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: eval/gen_c2_c3.py <instance_id> [<instance_id> ...]")
        return 1
    for inst_id in sys.argv[1:]:
        inst_path = INSTANCES / f"{inst_id}.json"
        if not inst_path.exists():
            print(f"! missing {inst_path}")
            continue
        instance = json.loads(inst_path.read_text())
        c2 = build_c2(instance)
        c3 = build_c3(instance)
        (INSTANCES / "perturbations" / f"{inst_id}-c2.json").write_text(json.dumps(c2, indent=2))
        (INSTANCES / "compliance" / f"{inst_id}-c3.json").write_text(json.dumps(c3, indent=2))
        print(f"  {inst_id}: {len(instance['factors'])} factors → c2 + c3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
