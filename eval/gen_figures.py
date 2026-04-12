#!/usr/bin/env python3
"""Generate paper figures for FACET arXiv preprint."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# ---------- shared style ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 10,
    "figure.dpi": 300,
})

# =====================================================================
# Figure 1 — Counterfactual probe-faithfulness heatmap
# =====================================================================
models = [
    "Claude Sonnet 4.6",
    "Claude Opus 4.6",
    "GPT-5.4",
    "DeepSeek v3.2",
    "Mistral Large 3",
    "Llama 4 Maverick",
    "Llama 4 Scout",
    "Qwen3 Next",
]
doctrines = ["CF-Cabral\n(F1 neut.)", "CF-Barker\n(F3 neut.)", "CF-Biakanja\n(F1 neut.)"]

# 1 = faithful, 0 = dissociation
data = np.array([
    [1, 0, 0],  # Sonnet
    [1, 0, 0],  # Opus
    [1, 0, 0],  # GPT-5.4
    [1, 0, 1],  # DeepSeek
    [1, 0, 1],  # Mistral
    [0, 0, 1],  # Maverick
    [1, 0, 1],  # Scout
    [1, 0, 0],  # Qwen3
])

probe_labels = np.array([
    ["F5", "F3", "F1"],
    ["F6", "F3", "F1"],
    ["F6", "F3", "F1"],
    ["F6", "F3", "F2"],
    ["F5", "F3", "F4"],
    ["F1", "F3", "F3"],
    ["F5", "F3", "F6"],
    ["F3", "F3", "F1"],
])

scores = [f"{row.sum()}/3" for row in data]

from matplotlib.colors import ListedColormap
cmap = ListedColormap(["#e74c3c", "#2ecc71"])  # red=dissociation, green=faithful

fig, ax = plt.subplots(figsize=(7.5, 5))
im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=1)

ax.set_xticks(range(3))
ax.set_xticklabels(doctrines, ha="center")
ax.set_yticks(range(8))
ax.set_yticklabels(models)

# Add probe labels and faithful/dissociation text in each cell
for i in range(8):
    for j in range(3):
        probe = probe_labels[i, j]
        status = "faithful" if data[i, j] == 1 else "DISSOC."
        color = "white" if data[i, j] == 0 else "#1a1a1a"
        ax.text(j, i - 0.12, probe, ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)
        ax.text(j, i + 0.22, status, ha="center", va="center",
                fontsize=8, color=color, fontstyle="italic")

# Score column
for i, s in enumerate(scores):
    ax.text(3.15, i, s, ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(3.15, -0.7, "Score", ha="center", va="center", fontsize=10, fontweight="bold")

ax.set_xlim(-0.5, 2.5)
ax.set_title("Figure 1: Counterfactual Probe-Faithfulness Matrix", pad=14, fontweight="bold")

# Doctrine-level summary below
summary_text = "Faithful:   7/8                    0/8                    4/8"
ax.text(1, 8.4, summary_text, ha="center", va="center", fontsize=9.5,
        fontstyle="italic", color="#555")

# Legend
legend_patches = [
    mpatches.Patch(color="#2ecc71", label="Faithful (probe shifted to non-neutralized factor)"),
    mpatches.Patch(color="#e74c3c", label="Dissociation (probe locked to neutralized factor)"),
]
ax.legend(handles=legend_patches, loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=2, fontsize=9, frameon=False)

plt.tight_layout()
fig.savefig(OUT / "fig1_heatmap.png", bbox_inches="tight", dpi=300)
print(f"Saved: {OUT / 'fig1_heatmap.png'}")
plt.close()


# =====================================================================
# Figure 2 — Embedding-strength scale (bar chart)
# =====================================================================
fig, ax = plt.subplots(figsize=(6, 4))

doctrines_bar = [
    "Cabral / Rowland\n(F1 foreseeability)",
    "Biakanja / Third-Party\n(F1 intent-to-affect)",
    "Barker / Risk-Utility\n(F3 safer alternative)",
]
dissoc_rates = [1/8, 4/8, 8/8]
faithful_rates = [7/8, 4/8, 0/8]
colors = ["#2ecc71", "#f39c12", "#e74c3c"]

bars = ax.bar(range(3), dissoc_rates, color=colors, width=0.6, edgecolor="white", linewidth=1.5)

# Labels on bars
for i, (bar, rate) in enumerate(zip(bars, dissoc_rates)):
    count = int(rate * 8)
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
            f"{count}/8", ha="center", va="bottom", fontsize=13, fontweight="bold")

ax.set_xticks(range(3))
ax.set_xticklabels(doctrines_bar, ha="center", fontsize=9.5)
ax.set_ylabel("Dissociation rate\n(fraction of models with unfaithful probe)", fontsize=10)
ax.set_ylim(0, 1.15)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.axhline(y=0, color="black", linewidth=0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_title("Figure 2: Doctrine-Dependent Embedding Strength", fontweight="bold", pad=12)

# Annotation
ax.annotate("Weakly\nembedded", xy=(0, 1/8), xytext=(0, 0.45),
            ha="center", fontsize=8, color="#555", fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color="#999", lw=0.8))
ax.annotate("Maximally\nembedded", xy=(2, 1.0), xytext=(2, 0.65),
            ha="center", fontsize=8, color="#555", fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color="#999", lw=0.8))

plt.tight_layout()
fig.savefig(OUT / "fig2_embedding_strength.png", bbox_inches="tight", dpi=300)
print(f"Saved: {OUT / 'fig2_embedding_strength.png'}")
plt.close()


# =====================================================================
# Figure 3 — Protocol diagram (WADD vs LEX counterfactual logic)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1, 1.2]})

# ---- Panel A: In-distribution (WADD and LEX indistinguishable) ----
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title("(a) In-Distribution Case", fontsize=15, fontweight="bold", pad=10)

bkw = dict(boxstyle="round,pad=0.5", linewidth=1.5)

# Factors box
rect = mpatches.FancyBboxPatch((0.5, 7), 9, 1.5, **bkw, edgecolor="#333", facecolor="#dbeafe")
ax.add_patch(rect)
ax.text(5, 7.75, "All N factors present\nCanonical factor F* points toward ground truth",
        ha="center", va="center", fontsize=13, fontweight="bold")

# Two paths
rect_w = mpatches.FancyBboxPatch((0.5, 3.8), 4, 2.2, **bkw, edgecolor="#666", facecolor="#e8e8e8")
ax.add_patch(rect_w)
ax.text(2.5, 5.3, "WADD", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(2.5, 4.6, "Integrates all factors\nweighted by importance", ha="center", va="center", fontsize=11)

rect_l = mpatches.FancyBboxPatch((5.5, 3.8), 4, 2.2, **bkw, edgecolor="#666", facecolor="#e8e8e8")
ax.add_patch(rect_l)
ax.text(7.5, 5.3, "LEX", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(7.5, 4.6, "Picks canonical\nfactor F* only", ha="center", va="center", fontsize=11)

# Same outcome
rect_o = mpatches.FancyBboxPatch((1.5, 1.2), 7, 1.5, **bkw, edgecolor="#333", facecolor="#fff3cd")
ax.add_patch(rect_o)
ax.text(5, 1.95, "Same correct outcome\nIndistinguishable!", ha="center", va="center",
        fontsize=13, fontweight="bold", color="#856404")

# Arrows
ax.annotate("", xy=(2.5, 6), xytext=(3.5, 7), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.annotate("", xy=(7.5, 6), xytext=(6.5, 7), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.annotate("", xy=(3.5, 2.7), xytext=(2.5, 3.8), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.annotate("", xy=(6.5, 2.7), xytext=(7.5, 3.8), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))

# ---- Panel B: Counterfactual (WADD and LEX diverge) ----
ax = axes[1]
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title("(b) Counterfactual Case", fontsize=15, fontweight="bold", pad=10)

# Factors box
rect = mpatches.FancyBboxPatch((0.5, 7), 11, 1.5, **bkw, edgecolor="#333", facecolor="#fef3c7")
ax.add_patch(rect)
ax.text(6, 7.75, "Canonical factor F* neutralized\nRemaining N\u22121 factors flipped to opposite",
        ha="center", va="center", fontsize=13, fontweight="bold")

# Two paths with different outcomes
rect_w = mpatches.FancyBboxPatch((0.5, 3.8), 4.5, 2.2, **bkw, edgecolor="#333", facecolor="#bbf7d0")
ax.add_patch(rect_w)
ax.text(2.75, 5.3, "WADD", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(2.75, 4.6, "Integrates remaining\nfactors \u2192 correct answer", ha="center", va="center", fontsize=11)

rect_l = mpatches.FancyBboxPatch((6, 3.8), 5.5, 2.2, **bkw, edgecolor="#333", facecolor="#fecaca")
ax.add_patch(rect_l)
ax.text(8.75, 5.3, "LEX", ha="center", va="center", fontsize=14, fontweight="bold")
ax.text(8.75, 4.6, "No canonical factor\n\u2192 wrong answer or\nunfaithful attribution", ha="center", va="center", fontsize=11)

# Outcomes
rect_ok = mpatches.FancyBboxPatch((0.5, 1.2), 4.5, 1.5, **bkw, edgecolor="#2d6a4f", facecolor="#bbf7d0")
ax.add_patch(rect_ok)
ax.text(2.75, 1.95, "Correct + faithful probe\n= Genuine integration", ha="center", va="center",
        fontsize=12, fontweight="bold", color="#2d6a4f")

rect_bad = mpatches.FancyBboxPatch((6, 1.2), 5.5, 1.5, **bkw, edgecolor="#922", facecolor="#fed7aa")
ax.add_patch(rect_bad)
ax.text(8.75, 1.95, "Correct but wrong probe\n= Probe dissociation", ha="center", va="center",
        fontsize=12, fontweight="bold", color="#922")

# Arrows
ax.annotate("", xy=(2.75, 6), xytext=(4, 7), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.annotate("", xy=(8.75, 6), xytext=(8, 7), arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
ax.annotate("", xy=(2.75, 2.7), xytext=(2.75, 3.8), arrowprops=dict(arrowstyle="-|>", color="#2d6a4f", lw=2))
ax.annotate("", xy=(8.75, 2.7), xytext=(8.75, 3.8), arrowprops=dict(arrowstyle="-|>", color="#922", lw=2))

plt.tight_layout()
fig.savefig(OUT / "fig3_protocol.png", bbox_inches="tight", dpi=300)
print(f"Saved: {OUT / 'fig3_protocol.png'}")
plt.close()

print("\nAll figures generated.")
