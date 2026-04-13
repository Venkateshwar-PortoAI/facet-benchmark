"""Generate the two new v3 figures:
1. fig3_bimodality.png — GPT-5.4 cf-001 family histogram (n=22)
2. fig4_c2_faithfulness.png — C2 ablation per-factor weights heatmap

Plus a regenerated fig2_adversarial_3panel.png with replication n shown.
"""
import json
import glob
import os
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results" / "weighted-probe"
C2_RESULTS = RESULTS / "c2"
OUT = REPO / "figures"


def model_key(fn):
    if "claude-opus" in fn or "-opus-" in fn:
        return "Opus 4.6"
    if "claude-sonnet" in fn or "-sonnet-" in fn:
        return "Sonnet 4.6"
    if "gpt-5.4" in fn:
        return "GPT-5.4"
    if "deepseek" in fn:
        return "DeepSeek v3.2"
    if "mistral" in fn:
        return "Mistral L3"
    if "maverick" in fn:
        return "Maverick"
    if "scout" in fn:
        return "Scout"
    if "qwen" in fn:
        return "Qwen3 Next"
    return None


def parse_answer(raw):
    lines = [l.strip() for l in (raw or "").split("\n") if l.strip()]
    if not lines:
        return ""
    return lines[-1].strip().rstrip(".").lower()


def fig3_bimodality():
    """Histogram of GPT-5.4 cf-001 family weights (n=22)."""
    runs = []
    for inst in ["facet-neg-cf-001-adv", "facet-neg-cf-001-adv2"]:
        for fp in sorted(glob.glob(str(RESULTS / f"{inst}-codex-gpt-5.4-*.json"))):
            d = json.load(open(fp))
            pw = d.get("parsed_weights", {})
            nw = pw.get("F1", 0)
            ans = parse_answer(d.get("raw_response"))
            wrong = ans.startswith("yes")
            variant = "v1" if "adv-codex" in os.path.basename(fp) else "v2"
            runs.append((nw, wrong, variant))

    fig, ax = plt.subplots(figsize=(9, 5))
    bins = np.arange(0, 65, 5)
    correct_v1 = [r[0] for r in runs if not r[1] and r[2] == "v1"]
    correct_v2 = [r[0] for r in runs if not r[1] and r[2] == "v2"]
    wrong_v1 = [r[0] for r in runs if r[1] and r[2] == "v1"]
    wrong_v2 = [r[0] for r in runs if r[1] and r[2] == "v2"]

    ax.hist([correct_v1 + correct_v2, wrong_v1 + wrong_v2],
            bins=bins, stacked=True,
            color=["#2ecc71", "#e74c3c"],
            label=["Correct outcome (No)", "Wrong outcome (Yes)"],
            edgecolor="white", linewidth=0.8)

    ax.axvline(x=10, color="#bbb", linestyle=":", linewidth=1, alpha=0.7)
    ax.text(10.5, ax.get_ylim()[1] * 0.95, "faithfulness\nthreshold (10%)",
            fontsize=8, color="#666", style="italic", va="top")

    ax.set_xlabel("Weight assigned to neutralized factor F1 (foreseeability)", fontsize=10.5)
    ax.set_ylabel("Number of trials", fontsize=10.5)
    ax.set_title("GPT-5.4 on CF-Cabral adversarial — bimodal mode-switching (n=22)",
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(bins)
    ax.set_xticklabels([f"{int(b)}" for b in bins])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Annotate the modes
    n_low = sum(1 for r in runs if r[0] < 20)
    n_high = sum(1 for r in runs if r[0] >= 20)
    n_wrong = sum(1 for r in runs if r[1])
    n_total = len(runs)
    ax.text(7.5, ax.get_ylim()[1] * 0.78, f"low mode\n(WADD)\nn={n_low}",
            ha="center", fontsize=9, color="#1e7e34",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#d4edda", edgecolor="none"))
    ax.text(45, ax.get_ylim()[1] * 0.55, f"high mode\n(LEX-locked)\nn={n_high}",
            ha="center", fontsize=9, color="#7d2025",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8d7da", edgecolor="none"))

    ax.legend(loc="upper right", fontsize=9, frameon=True, edgecolor="#ccc")

    fig.text(0.5, -0.04,
             f"Distribution of $w_{{F1}}$ across 22 trials (16 on cf-001-adv + 6 on cf-001-adv2). "
             f"The wrong-outcome rate is {n_wrong}/{n_total} = {100*n_wrong/n_total:.0f}% "
             f"(Wilson 95% CI [16%, 53%]). Zero trials in the 20–25 range. "
             f"The bimodality with no middle is direct trial-level evidence of LEX/WADD "
             f"mode-switching predicted by Payne, Bettman & Johnson (1993).",
             ha="center", fontsize=8.5, color="#444", wrap=True)

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out_path = OUT / "fig3_bimodality.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


def fig4_c2_faithfulness():
    """Per-factor C2 ablation faithfulness — heatmap of mean residual weight on
    the perturbed factor for each (model, anchor) cell.

    Faithful = perturbed factor weight goes to ~0 when the factor is neutralized.
    """
    MODELS = [
        "DeepSeek v3.2", "Mistral L3", "Qwen3 Next",
        "Maverick", "Scout",
        "Sonnet 4.6", "Opus 4.6", "GPT-5.4",
    ]
    ANCHORS = [
        ("facet-neg-0002", "Barker (5 factors)"),
        ("facet-neg-0003", "Cabral (7 factors)"),
        ("facet-neg-0004", "Biakanja (6 factors)"),
    ]

    matrix = np.zeros((len(MODELS), len(ANCHORS)))
    cell_text = [[None] * len(ANCHORS) for _ in MODELS]

    for j, (anchor, _) in enumerate(ANCHORS):
        for fp in sorted(glob.glob(str(C2_RESULTS / f"{anchor}-c2-*.json"))):
            fn = os.path.basename(fp)
            mk = model_key(fn)
            if mk not in MODELS:
                continue
            i = MODELS.index(mk)
            d = json.load(open(fp))
            pid = d.get("c2_perturbed_factor", "")
            pw = d.get("parsed_weights", {})
            w = pw.get(pid.upper(), 0)
            if cell_text[i][j] is None:
                cell_text[i][j] = []
            cell_text[i][j].append(w)

    # Compute means
    for i in range(len(MODELS)):
        for j in range(len(ANCHORS)):
            if cell_text[i][j]:
                matrix[i, j] = statistics.mean(cell_text[i][j])

    fig, ax = plt.subplots(figsize=(8.5, 6))

    # Color map: 0 = perfect green, higher = redder
    cmap = plt.cm.RdYlGn_r
    im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=20, aspect="auto")

    # Cell labels: mean and detail
    for i in range(len(MODELS)):
        for j in range(len(ANCHORS)):
            if cell_text[i][j]:
                vals = cell_text[i][j]
                mean_v = statistics.mean(vals)
                detail = "/".join(str(int(v)) for v in vals)
                color = "white" if mean_v > 10 else "#222"
                ax.text(j, i - 0.12, f"{mean_v:.1f}",
                        ha="center", va="center",
                        fontsize=11, fontweight="bold", color=color)
                ax.text(j, i + 0.22, f"({detail})",
                        ha="center", va="center",
                        fontsize=6.5, color=color)

    ax.set_xticks(range(len(ANCHORS)))
    ax.set_xticklabels([a[1] for a in ANCHORS], fontsize=10)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(MODELS, fontsize=10)
    ax.set_xticks(np.arange(-0.5, len(ANCHORS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(MODELS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=0)

    # Horizontal divider between bedrock and closed-source
    ax.axhline(y=4.5, color="#333", linestyle="--", linewidth=1.5, alpha=0.8)

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label("Mean residual weight on perturbed factor (lower = more faithful)",
                   fontsize=9)

    ax.set_title("C2 ablation faithfulness — does the model zero out a perturbed factor?",
                 fontsize=12, fontweight="bold", pad=14)

    ax.set_xlabel("Faithful = ~0 residual weight on the neutralized factor. "
                  "Dashed line separates open-weight (top) from closed frontier (bottom).",
                  fontsize=8.5, color="#444", labelpad=14)

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    out_path = OUT / "fig4_c2_faithfulness.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    fig3_bimodality()
    fig4_c2_faithfulness()
