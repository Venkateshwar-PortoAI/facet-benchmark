"""Generate figures/fig2_adversarial_3panel.png — adversarial weighted-rank
probe results across all three counterfactual cases.

Three side-by-side bar panels showing the weight assigned to the neutralized
factor under the adversarial probe for each of the eight models on each of
CF-Cabral (F1), CF-Barker (F3), and CF-Biakanja (F1). Models are ordered
identically across panels.

Highlights:
- GPT-5.4 on CF-Cabral assigns 44% AND produces the wrong outcome answer
  (annotated with a 'X' marker)
- All other 23 model-case pairs reach the correct outcome
"""

import json
import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results" / "weighted-probe"
OUT = REPO / "figures" / "fig2_adversarial_3panel.png"

# Order matches gen_figures_v2 — open weight first, then closed frontier
MODELS_ORDER = [
    ("DeepSeek v3.2", "deepseek"),
    ("Mistral Large 3", "mistral"),
    ("Qwen3 Next", "qwen"),
    ("Llama 4 Maverick", "maverick"),
    ("Llama 4 Scout", "scout"),
    ("Claude Sonnet 4.6", "claude-sonnet"),
    ("Claude Opus 4.6", "claude-opus"),
    ("GPT-5.4", "gpt-5.4"),
]
DISPLAY_LABELS = [
    "DeepSeek\nv3.2",
    "Mistral\nLarge 3",
    "Qwen3\nNext",
    "Llama 4\nMaverick",
    "Llama 4\nScout",
    "Claude\nSonnet 4.6",
    "Claude\nOpus 4.6",
    "GPT-5.4",
]

CASES = [
    ("facet-neg-cf-001-adv", "F1", "(a) CF-Cabral adversarial\n(F1 neutralized)", 7),
    ("facet-neg-cf-002-adv", "F3", "(b) CF-Barker adversarial\n(F3 neutralized)", 5),
    ("facet-neg-cf-003-adv", "F1", "(c) CF-Biakanja adversarial\n(F1 neutralized)", 6),
]


def load_weight(instance, model_pat):
    """Return (w_neut, answer, parsed_weights) for the latest run."""
    files = sorted(glob.glob(str(RESULTS / f"{instance}-*.json")))
    best = None
    for fp in files:
        fn = os.path.basename(fp)
        if model_pat not in fn:
            continue
        d = json.load(open(fp))
        if d.get("parsed_weights"):
            best = d
    if best is None:
        return None, None, None
    pw = best.get("parsed_weights") or {}
    nf = best.get("neutralized_factor")
    nw = pw.get(nf, 0.0) if nf else 0.0
    raw = (best.get("raw_response") or "").strip()
    ans_lines = [l.strip() for l in raw.split("\n") if l.strip()]
    ans = ans_lines[-1] if ans_lines else "?"
    return nw, ans, pw


def main():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), sharey=True)

    for ax, (inst, neut, title, n_factors) in zip(axes, CASES):
        weights = []
        wrong_outcome = []
        for display, pat in MODELS_ORDER:
            nw, ans, _ = load_weight(inst, pat)
            weights.append(nw if nw is not None else 0)
            # ground truth is "no" for all three counterfactuals
            ans_norm = ans.strip().rstrip(".").lower() if ans else ""
            is_wrong = ans_norm.startswith("yes")
            wrong_outcome.append(is_wrong)

        x = np.arange(len(MODELS_ORDER))
        # Color: 0% = green, 0-10 = light orange, 10-20 = orange, 20-40 = red, >40 = dark red
        colors = []
        for w in weights:
            if w == 0:
                colors.append("#2ecc71")
            elif w <= 10:
                colors.append("#f1c40f")
            elif w < 20:
                colors.append("#f39c12")
            elif w < 40:
                colors.append("#e74c3c")
            else:
                colors.append("#922b21")

        bars = ax.bar(x, weights, width=0.7, color=colors,
                      edgecolor="white", linewidth=1.5)

        # Value labels
        for i, (w, wrong) in enumerate(zip(weights, wrong_outcome)):
            label = f"{int(w)}%"
            if wrong:
                label = f"{int(w)}%\n✗"
            color = "#922b21" if wrong else ("#1a1a1a" if w > 0 else "#2ecc71")
            weight_style = "bold" if w >= 20 or w == 0 else "normal"
            ax.text(i, w + 1.5, label,
                    ha="center", va="bottom",
                    fontsize=10 if not wrong else 11,
                    fontweight=weight_style if not wrong else "bold",
                    color=color)

        # Reference lines
        ax.axhline(y=10, color="#bbb", linestyle=":", linewidth=1, alpha=0.7, zorder=0)
        ax.axhline(y=100/n_factors, color="#999", linestyle="--", linewidth=0.8, alpha=0.5, zorder=0)
        if ax == axes[2]:
            ax.text(7.5, 100/n_factors + 0.5, f"uniform\n(1/{n_factors})",
                    fontsize=7, ha="right", color="#666", style="italic")

        # Vertical divider between open-weight and closed-frontier
        ax.axvline(x=4.5, color="#666", linestyle="--", linewidth=1, alpha=0.6, zorder=0)

        ax.set_xticks(x)
        ax.set_xticklabels(DISPLAY_LABELS, fontsize=8, rotation=0)
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        ax.set_ylim(0, 50)
        ax.set_yticks([0, 10, 20, 30, 40, 50])
        ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", length=0)

    axes[0].set_ylabel("Weight on neutralized factor\n(target: 0%; ✗ = wrong outcome)", fontsize=10)

    fig.suptitle(
        "FACET v3 — Adversarial Weighted-Rank Probe across all three counterfactual cases",
        fontsize=13, fontweight="bold", y=1.02,
    )
    fig.text(0.5, -0.02,
             "Open-weight Bedrock models (left of dashed line) vs closed-source frontier "
             "(right). The horizontal dotted line marks the 10% faithfulness threshold; the "
             "thinner dashed line marks uniform 1/N. GPT-5.4 on CF-Cabral assigns 44% to F1 "
             "AND produces the wrong outcome (✗) — the only wrong-outcome response in the "
             "FACET v3 corpus. The clean open-vs-closed split holds on CF-Barker; on the "
             "other two cases the picture is more nuanced.",
             ha="center", fontsize=8.5, color="#444444", wrap=True)

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"wrote {OUT}")
    print()
    for inst, neut, title, n in CASES:
        print(f"{title.split(chr(10))[0]}:")
        for display, pat in MODELS_ORDER:
            nw, ans, _ = load_weight(inst, pat)
            if nw is None:
                print(f"  {display:20s} MISSING")
                continue
            mark = " ✗ WRONG OUTCOME" if (ans or "").strip().lower().startswith("yes") else ""
            print(f"  {display:20s} w_neut={int(nw):3d}  ans={ans}{mark}")


if __name__ == "__main__":
    main()
