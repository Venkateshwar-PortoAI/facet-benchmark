"""Generate figures/fig5_asymmetry.png — the 2D asymmetric faithfulness profile.

X-axis: mean C2 residual weight on perturbed factors across the three anchors
        (lower = more surgical attribution updating)
Y-axis: mean weight on the neutralized factor under P3 on CF-Barker
        (lower = more cue-robust)

Each model is one point. Closed-source frontier models cluster upper-left;
open-weight Bedrock models cluster lower-right.
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
OUT = REPO / "figures" / "fig5_asymmetry.png"


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


def mean_c2_residual(model_name):
    """Mean residual weight on perturbed factor across all C2 trials for this model."""
    residuals = []
    for fp in sorted(glob.glob(str(C2_RESULTS / "*.json"))):
        fn = os.path.basename(fp)
        if model_key(fn) != model_name:
            continue
        d = json.load(open(fp))
        pid = d.get("c2_perturbed_factor", "")
        pw = d.get("parsed_weights") or {}
        residuals.append(pw.get(pid.upper(), 0))
    return statistics.mean(residuals) if residuals else 0


def mean_p3_cf_barker(model_name):
    """Mean weight on F3 on CF-Barker adversarial across all replications."""
    weights = []
    for fp in sorted(glob.glob(str(RESULTS / "facet-neg-cf-002-adv-*.json"))):
        fn = os.path.basename(fp)
        if model_key(fn) != model_name:
            continue
        d = json.load(open(fp))
        pw = d.get("parsed_weights") or {}
        weights.append(pw.get("F3", 0))
    return statistics.mean(weights) if weights else 0


MODELS = [
    ("DeepSeek v3.2",   "open"),
    ("Mistral L3",       "open"),
    ("Qwen3 Next",       "open"),
    ("Maverick",         "open"),
    ("Scout",            "open"),
    ("Sonnet 4.6",       "closed"),
    ("Opus 4.6",         "closed"),
    ("GPT-5.4",          "closed"),
]


def plot():
    fig, ax = plt.subplots(figsize=(8.5, 6.5))

    open_x = []
    open_y = []
    closed_x = []
    closed_y = []
    labels = []

    for name, family in MODELS:
        c2 = mean_c2_residual(name)
        p3 = mean_p3_cf_barker(name)
        if family == "open":
            open_x.append(c2)
            open_y.append(p3)
        else:
            closed_x.append(c2)
            closed_y.append(p3)
        labels.append((c2, p3, name, family))
        print(f"  {name:18s}  C2={c2:5.2f}  P3_cfBarker={p3:5.2f}")

    ax.scatter(open_x, open_y, s=260, c="#2ecc71", edgecolor="#1e7e34",
               linewidth=2, label="Open-weight Bedrock", zorder=3, alpha=0.85)
    ax.scatter(closed_x, closed_y, s=260, c="#e74c3c", edgecolor="#7d2025",
               linewidth=2, label="Closed-source frontier", zorder=3, alpha=0.85)

    # Label each point. Bottom-cluster points use leader lines stacked above,
    # so labels don't overlap each other or the markers.
    label_pos = {
        "GPT-5.4":        (-0.4, 0.0,  "right", False),
        "Opus 4.6":       (-0.4, 0.0,  "right", False),
        "Sonnet 4.6":     (-0.4, 0.0,  "right", False),
        "Maverick":       ( 7.5,  2.0, "left", True),
        "Mistral L3":     ( 7.5,  4.5, "left", True),
        "Qwen3 Next":     ( 7.5,  7.0, "left", True),
        "Scout":          ( 7.5,  9.5, "left", True),
        "DeepSeek v3.2":  ( 7.5, 12.0, "left", True),
    }
    for c2, p3, name, family in labels:
        lx, ly, ha, leader = label_pos[name]
        if leader:
            ax.annotate(name, xy=(c2, p3), xytext=(lx, ly),
                        fontsize=9, ha=ha, va="center", color="#222",
                        arrowprops=dict(arrowstyle="-", color="#aaa",
                                        lw=0.6, shrinkA=0, shrinkB=3))
        else:
            ax.annotate(name, (c2, p3),
                        xytext=(c2 + lx, p3 + ly),
                        fontsize=9, ha=ha, va="center", color="#222")

    # Quadrant labels
    ax.text(0.5, 28, "ideal:\nfaithful on both",
            fontsize=8.5, color="#888", style="italic", ha="left", va="top")
    ax.text(11.5, 28, "worst:\nunfaithful on both",
            fontsize=8.5, color="#888", style="italic", ha="right", va="top")
    ax.text(0.2, 22, "closed-source\ncluster",
            fontsize=8.5, color="#7d2025", style="italic", ha="left", va="center",
            alpha=0.6)
    ax.text(11.0, 0.5, "all open-weight\nmodels: $w_{F3}=0$",
            fontsize=8.5, color="#1e7e34", style="italic", ha="center", va="bottom",
            alpha=0.7)

    # Reference lines
    ax.axhline(y=10, color="#bbb", linestyle=":", linewidth=1, alpha=0.6)
    ax.axvline(x=2, color="#bbb", linestyle=":", linewidth=1, alpha=0.6)

    ax.set_xlabel("Mean C2 residual weight on perturbed factors (%)\nlower = more surgical attribution updating",
                  fontsize=10)
    ax.set_ylabel("Mean $w_{F3}$ on CF-Barker adversarial (%)\nlower = more cue-robust",
                  fontsize=10)
    ax.set_title("The asymmetric faithfulness profile",
                 fontsize=13, fontweight="bold", pad=14)
    ax.legend(loc="upper center", fontsize=10, frameon=True, edgecolor="#ccc",
              bbox_to_anchor=(0.5, -0.18), ncol=2)
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-1, 32)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.2)

    fig.text(0.5, -0.05,
             "Each point is one model. The two failure modes are anti-correlated across "
             "the model lineup: closed-source frontier models are surgical at C2 but "
             "cue-dependent at $P_3$; open-weight Bedrock models are cue-robust at $P_3$ "
             "but less surgical at C2. No model is faithful on both axes.",
             ha="center", fontsize=8.5, color="#444", wrap=True)

    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    plot()
