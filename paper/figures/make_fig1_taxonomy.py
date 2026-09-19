# -*- coding: utf-8 -*-
"""Figura 1 (v2, corregida): posicionamiento de las 5 categorias de interaccion con modelos
de IA. Eje X = rigidez y MOMENTO de fijacion del esquema de decision (NO "flexibilidad de
entrada" - correccion tras observacion de Maikel de que la v1 sugeria, erroneamente, que un
chat generativo es MENOS flexible que un modelo tipado). Orden correcto de izq. a der.:
clasificador (esquema fijo en ENTRENAMIENTO, el mas rigido) -> salida forzada/juez/Jev
(esquema declarado en cada LLAMADA) -> chat generativo (SIN esquema declarado, texto libre,
el extremo opuesto - maxima libertad expresiva, CERO garantia estructural). 300 dpi."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10

fig, ax = plt.subplots(figsize=(8.8, 6.8), dpi=300)

# Puntos: (x=rigidez/momento del esquema 0-11, y=costo/latencia 0-11, label, color, marker)
points = [
    (1.0, 1.2, "4. Clasificador\ndiscriminativo clasico\n(BERT afinado, EDL)", "#2563eb", "s"),
    (5.2, 2.4, "5. Jev / modelo de\nevaluacion tipada", "#dc2626", "^"),
    (6.3, 6.0, "3. LLM-as-judge\n(GPT-4 juez, jueces\nafinados)", "#2563eb", "s"),
    (6.9, 9.2, "2. Salida forzada\n(function calling,\nOutlines, Instructor)", "#6b7280", "o"),
    (9.8, 9.2, "1. Chat generativo\n(GPT, Claude en chat)", "#6b7280", "o"),
]

for x, y, label, color, marker in points:
    ax.scatter([x], [y], s=280, c=color, marker=marker, edgecolors="black",
               linewidths=1.1, zorder=3)

# Etiquetas de texto, ajustadas a mano para no solaparse
offsets = {
    "4. Clasificador\ndiscriminativo clasico\n(BERT afinado, EDL)": (0.45, 0.7, "left"),
    "5. Jev / modelo de\nevaluacion tipada": (0.45, -0.7, "left"),
    "3. LLM-as-judge\n(GPT-4 juez, jueces\nafinados)": (0.45, 0.4, "left"),
    "2. Salida forzada\n(function calling,\nOutlines, Instructor)": (-1.0, -1.15, "center"),
    "1. Chat generativo\n(GPT, Claude en chat)": (0.0, -1.15, "center"),
}
for x, y, label, color, marker in points:
    dx, dy, ha = offsets[label]
    ax.annotate(label, (x, y), xytext=(x + dx, y + dy), fontsize=8.6,
                ha=ha, va="center", color="black", zorder=4)

# Flechas de convergencia hacia Jev (desde judge y desde clasificador)
arrow1 = FancyArrowPatch((6.0, 5.35), (5.55, 3.05), connectionstyle="arc3,rad=0.2",
                          arrowstyle="-|>", mutation_scale=14, color="#2563eb",
                          linewidth=1.3, linestyle="--", alpha=0.75, zorder=2)
arrow2 = FancyArrowPatch((1.6, 1.65), (4.75, 2.25), connectionstyle="arc3,rad=-0.22",
                          arrowstyle="-|>", mutation_scale=14, color="#2563eb",
                          linewidth=1.3, linestyle="--", alpha=0.75, zorder=2)
ax.add_patch(arrow1)
ax.add_patch(arrow2)
ax.text(6.15, 4.15, "flexibilidad de\nesquema heredada", fontsize=7.5, color="#2563eb",
        ha="left", va="center", style="italic")
ax.text(2.9, 0.55, "costo/latencia\nheredado", fontsize=7.5, color="#2563eb",
        ha="center", va="center", style="italic")

# Corchete + nota explicita advirtiendo que "sin esquema" (chat) NO es mas confiable
# (acotado SOLO a chat generativo - salida forzada SI tiene garantia estructural completa)
ax.annotate("", xy=(10.85, 10.3), xytext=(8.75, 10.3),
            arrowprops=dict(arrowstyle="-", color="#7c2d12", lw=1.1))
ax.text(9.8, 10.55, "cero garantía estructural\npese a máxima libertad expresiva",
        fontsize=7.3, color="#7c2d12", ha="center", va="bottom", style="italic")

ax.set_xlim(0, 12.6)
ax.set_ylim(0, 12.9)
ax.set_xlabel(
    "Rigidez y momento de fijación del esquema de decisión\n"
    "(fijo en ENTRENAMIENTO, clasificador  →  declarado en cada LLAMADA  →  SIN esquema, texto libre)",
    fontsize=9.0)
ax.set_ylabel("Costo computacional / latencia\n(bajo, ms  →  alto, s)", fontsize=9.2)
ax.set_xticks([])
ax.set_yticks([])
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

legend_elems = [
    mpatches.Patch(color="#6b7280", label="Generativo de proposito general"),
    mpatches.Patch(color="#2563eb", label="Evaluador / clasificador"),
    mpatches.Patch(color="#dc2626", label="Caso de estudio (Jev)"),
]
ax.legend(handles=legend_elems, loc="upper center", bbox_to_anchor=(0.5, -0.16),
          ncol=3, frameon=False, fontsize=8.2)

fig.tight_layout()
fig.savefig("fig1_taxonomy.png", dpi=300, bbox_inches="tight")
print("saved fig1_taxonomy.png")
