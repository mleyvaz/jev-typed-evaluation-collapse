# -*- coding: utf-8 -*-
"""Figure 1 (English version). Same layout/semantics as make_fig1_taxonomy.py, translated
labels. X axis = rigidity and TIMING of decision-schema fixation. Order left to right:
classifier (schema fixed at TRAINING, most rigid) -> forced output/judge/Jev (schema declared
at each CALL) -> generative chat (NO declared schema, free text - opposite extreme, maximum
expressive freedom, ZERO structural guarantee). 300 dpi."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

fig, ax = plt.subplots(figsize=(8.8, 6.8), dpi=300)

points = [
    (1.0, 1.2, "4. Classical\ndiscriminative classifier\n(fine-tuned BERT, EDL)", "#2563eb", "s"),
    (5.2, 2.4, "5. Jev / typed\nevaluation model", "#dc2626", "^"),
    (6.3, 6.0, "3. LLM-as-judge\n(GPT-4 judge,\nfine-tuned judges)", "#2563eb", "s"),
    (6.9, 9.2, "2. Forced output\n(function calling,\nOutlines, Instructor)", "#6b7280", "o"),
    (9.8, 9.2, "1. Generative chat\n(GPT, Claude in chat)", "#6b7280", "o"),
]

for x, y, label, color, marker in points:
    ax.scatter([x], [y], s=280, c=color, marker=marker, edgecolors="black",
               linewidths=1.1, zorder=3)

offsets = {
    "4. Classical\ndiscriminative classifier\n(fine-tuned BERT, EDL)": (0.45, 0.7, "left"),
    "5. Jev / typed\nevaluation model": (0.45, -0.7, "left"),
    "3. LLM-as-judge\n(GPT-4 judge,\nfine-tuned judges)": (0.45, 0.4, "left"),
    "2. Forced output\n(function calling,\nOutlines, Instructor)": (-1.0, -1.15, "center"),
    "1. Generative chat\n(GPT, Claude in chat)": (0.0, -1.15, "center"),
}
for x, y, label, color, marker in points:
    dx, dy, ha = offsets[label]
    ax.annotate(label, (x, y), xytext=(x + dx, y + dy), fontsize=8.6,
                ha=ha, va="center", color="black", zorder=4)

arrow1 = FancyArrowPatch((6.0, 5.35), (5.55, 3.05), connectionstyle="arc3,rad=0.2",
                          arrowstyle="-|>", mutation_scale=14, color="#2563eb",
                          linewidth=1.3, linestyle="--", alpha=0.75, zorder=2)
arrow2 = FancyArrowPatch((1.6, 1.65), (4.75, 2.25), connectionstyle="arc3,rad=-0.22",
                          arrowstyle="-|>", mutation_scale=14, color="#2563eb",
                          linewidth=1.3, linestyle="--", alpha=0.75, zorder=2)
ax.add_patch(arrow1)
ax.add_patch(arrow2)
ax.text(6.15, 4.15, "inherited schema\nflexibility", fontsize=7.5, color="#2563eb",
        ha="left", va="center", style="italic")
ax.text(2.9, 0.55, "inherited\ncost/latency", fontsize=7.5, color="#2563eb",
        ha="center", va="center", style="italic")

# Bracket + note, scoped ONLY to generative chat (forced output DOES have full structural guarantee)
ax.annotate("", xy=(10.85, 10.3), xytext=(8.75, 10.3),
            arrowprops=dict(arrowstyle="-", color="#7c2d12", lw=1.1))
ax.text(9.8, 10.55, "zero structural guarantee\ndespite maximum expressive freedom",
        fontsize=7.3, color="#7c2d12", ha="center", va="bottom", style="italic")

ax.set_xlim(0, 12.6)
ax.set_ylim(0, 12.9)
ax.set_xlabel(
    "Rigidity and timing of decision-schema fixation\n"
    "(fixed at TRAINING, classifier  →  declared at each CALL  →  NO schema, free text)",
    fontsize=9.0)
ax.set_ylabel("Computational cost / latency\n(low, ms  →  high, s)", fontsize=9.2)
ax.set_xticks([])
ax.set_yticks([])
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

legend_elems = [
    mpatches.Patch(color="#6b7280", label="General-purpose generative"),
    mpatches.Patch(color="#2563eb", label="Evaluator / classifier"),
    mpatches.Patch(color="#dc2626", label="Case study (Jev)"),
]
ax.legend(handles=legend_elems, loc="upper center", bbox_to_anchor=(0.5, -0.16),
          ncol=3, frameon=False, fontsize=8.2)

fig.tight_layout()
fig.savefig("fig1_taxonomy_en.png", dpi=300, bbox_inches="tight")
print("saved fig1_taxonomy_en.png")
