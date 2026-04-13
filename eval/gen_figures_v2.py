#!/usr/bin/env python3
"""Generate v2 paper figures: side-by-side probe comparison + adversarial validation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import ListedColormap
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

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
# Figure 1 — Side-by-side probe comparison heatmap
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

# Left panel: single-factor probe (1 = faithful, 0 = dissociation)
single_factor = np.array([
    [1, 0, 0],  # Sonnet
    [1, 0, 0],  # Opus
    [1, 0, 0],  # GPT-5.4
    [1, 0, 1],  # DeepSeek
    [1, 0, 1],  # Mistral
    [0, 0, 1],  # Maverick
    [1, 0, 1],  # Scout
    [1, 0, 0],  # Qwen3
])
single_probe_labels = np.array([
    ["F5", "F3", "F1"],
    ["F6", "F3", "F1"],
    ["F6", "F3", "F1"],
    ["F6", "F3", "F2"],
    ["F5", "F3", "F4"],
    ["F1", "F3", "F3"],
    ["F5", "F3", "F6"],
    ["F3", "F3", "F1"],
])

# Right panel: weighted-rank probe (weight on neutralized factor, 0-100)
weighted_rank = np.array([
    [0, 0, 0],    # Sonnet
    [5, 0, 5],    # Opus
    [0, 0, 0],    # GPT-5.4
    [0, 0, 0],    # DeepSeek
    [10, 0, 5],   # Mistral
    [10, 0, 0],   # Maverick
    [10, 0, 5],   # Scout
    [0, 0, 0],    # Qwen3
])

cmap_binary = ListedColormap(["#e74c3c", "#2ecc71"])

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={"wspace": 0.35})

# ---- Left: single-factor probe ----
ax = axes[0]
ax.imshow(single_factor, cmap=cmap_binary, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(3))
ax.set_xticklabels(doctrines, ha="center", fontsize=10)
ax.set_yticks(range(8))
ax.set_yticklabels(models, fontsize=10)
ax.set_title("(a) Single-Factor Probe\n\"which one is most important?\"",
             fontweight="bold", pad=12, fontsize=12)

for i in range(8):
    for j in range(3):
        probe = single_probe_labels[i, j]
        color = "white" if single_factor[i, j] == 0 else "#1a1a1a"
        ax.text(j, i, probe, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color)

# Bottom summary
for j, score in enumerate(["7/8", "0/8", "4/8"]):
    color = "#2ecc71" if score != "0/8" else "#e74c3c"
    ax.text(j, 8.2, f"faithful: {score}", ha="center", va="center",
            fontsize=10, fontweight="bold", color=color)

# ---- Right: weighted-rank probe ----
ax = axes[1]
# Green if <=10, red otherwise
weighted_binary = (weighted_rank <= 10).astype(int)
ax.imshow(weighted_binary, cmap=cmap_binary, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(3))
ax.set_xticklabels(doctrines, ha="center", fontsize=10)
ax.set_yticks(range(8))
ax.set_yticklabels(models, fontsize=10)
ax.set_title("(b) Weighted-Rank Probe\n\"assign weights to all N factors\"",
             fontweight="bold", pad=12, fontsize=12)

for i in range(8):
    for j in range(3):
        w = weighted_rank[i, j]
        color = "#1a1a1a"
        ax.text(j, i, f"{int(w)}%", ha="center", va="center",
                fontsize=11, fontweight="bold", color=color)

for j in range(3):
    ax.text(j, 8.2, "faithful: 8/8", ha="center", va="center",
            fontsize=10, fontweight="bold", color="#2ecc71")

# Shared legend
legend_patches = [
    mpatches.Patch(color="#2ecc71", label="Faithful (probe → non-neutralized / weight ≤10%)"),
    mpatches.Patch(color="#e74c3c", label="Dissociation (probe → neutralized / weight >10%)"),
]
fig.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.02),
           ncol=2, fontsize=10, frameon=False)

fig.suptitle("Probe Format Determines Apparent Attribution Faithfulness",
             fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
fig.savefig(OUT / "fig1_probe_comparison.png", bbox_inches="tight", dpi=300)
print(f"Saved: {OUT / 'fig1_probe_comparison.png'}")
plt.close()


# =====================================================================
# Figure 2 — Adversarial validation bar chart (single bar per model)
# =====================================================================
# Sort: open-weight (left) → closed frontier (right), each group sorted by value
models_adv = [
    "DeepSeek\nv3.2",
    "Mistral\nLarge 3",
    "Qwen3 Next\n80B-A3B",
    "Llama 4\nMaverick",
    "Llama 4\nScout",
    "Claude\nSonnet 4.6",
    "Claude\nOpus 4.6",
    "GPT-5.4",
]
adversarial_f3 = [0, 0, 0, 0, 0, 10, 25, 30]
is_closed = [False, False, False, False, False, True, True, True]

# Color: green for 0, orange for 10-20, red for >20
colors = []
for v in adversarial_f3:
    if v == 0:
        colors.append("#2ecc71")
    elif v < 20:
        colors.append("#f39c12")
    else:
        colors.append("#e74c3c")

fig, ax = plt.subplots(figsize=(10, 5.5))

x = np.arange(len(models_adv))
bars = ax.bar(x, adversarial_f3, width=0.65, color=colors,
              edgecolor="white", linewidth=2)

# Value labels on top of every bar (including 0%)
for i, v in enumerate(adversarial_f3):
    if v == 0:
        ax.text(i, 1.5, "0%", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color="#2ecc71")
    else:
        ax.text(i, v + 1.2, f"{v}%", ha="center", va="bottom",
                fontsize=12, fontweight="bold", color="#1a1a1a")

# Reference line at 20% (natural-distribution weight for 5-factor case)
ax.axhline(y=20, color="#999", linestyle=":", linewidth=1, alpha=0.6, zorder=0)
ax.text(7.6, 20.5, "20% = uniform\nbaseline (1/5)", fontsize=8,
        color="#666", style="italic", ha="right")

# Dividing line between open and closed models
ax.axvline(x=4.5, color="#666", linestyle="--", linewidth=1.2, alpha=0.7, zorder=0)

# Group labels above bars
ax.text(2, 38, "OPEN-WEIGHT MODELS", ha="center",
        fontsize=11, fontweight="bold", color="#2ecc71")
ax.text(2, 35.5, "(semantically robust)", ha="center",
        fontsize=9, fontstyle="italic", color="#555")
ax.text(6.5, 38, "CLOSED FRONTIER MODELS", ha="center",
        fontsize=11, fontweight="bold", color="#c0392b")
ax.text(6.5, 35.5, "(signal-word dependent)", ha="center",
        fontsize=9, fontstyle="italic", color="#555")

ax.set_xticks(x)
ax.set_xticklabels(models_adv, fontsize=10)
ax.set_ylabel("Weight assigned to F3 on adversarial CF-Barker\n(F3 is the neutralized factor → target is 0%)",
              fontsize=10.5)
ax.set_ylim(0, 42)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%"])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", length=0)

ax.set_title("Adversarial Validation: Removing Signal Words Splits Open vs Closed Models",
             fontweight="bold", fontsize=13, pad=18)

plt.tight_layout()
fig.savefig(OUT / "fig2_adversarial_validation.png", bbox_inches="tight", dpi=300)
print(f"Saved: {OUT / 'fig2_adversarial_validation.png'}")
plt.close()

print("\nDone. Generated 2 new figures.")
