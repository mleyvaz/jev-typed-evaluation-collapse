# -*- coding: utf-8 -*-
"""Infografia en espanol (LinkedIn) sobre la taxonomia de 5 categorias de
interaccion con modelos de IA (Figura 1 del paper), en la misma estetica
oscura de linkedin_jev_infographic.png."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

W, H = 1080, 1230
DPI = 200
PX = 72 / DPI


def pt(px):
    return px * PX


BG = "#17140F"
INK = "#F2EEE6"
MUTED = "#B9B2A4"
FAINT = "#8A8375"
CORAL = "#E58A63"
STEEL = "#8CA6BF"
WARMGRAY = "#9A9486"
INSIGHT_BG = "#271D16"
INSIGHT_BORDER = "#5F3D2C"
LINE = "#3A352C"

SERIF = "Georgia"
SANS = "Segoe UI"
MONO = "Consolas"

fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")
ax.set_facecolor(BG)

PAD_L, PAD_R, PAD_T = 76, 76, 64
CONTENT_W = W - PAD_L - PAD_R


def text(x, y, s, size, color, font=SANS, weight="normal", ha="left", va="top",
          style="normal", rotation=0):
    ax.text(x, y, s, fontsize=pt(size), color=color, fontfamily=font,
             fontweight=weight, ha=ha, va=va, fontstyle=style, rotation=rotation)


def rect(x, y, w, h, face, edge=None, lw=1.0):
    ax.add_patch(mpatches.Rectangle((x, y), w, h, facecolor=face,
                                     edgecolor=edge if edge else "none", linewidth=lw))


def line(x0, y0, x1, y1, color, lw=1.2):
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, solid_capstyle="round")


def dot(x, y, r, face, edge=INK, lw=1.4):
    ax.add_patch(mpatches.Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=lw, zorder=5))


# ---------------------------------------------------------------- eyebrow
cursor = PAD_T
text(PAD_L, cursor, "MODELOS DE EVALUACIÓN TIPADA  ·  TAXONOMÍA", 13, CORAL,
     font=MONO, weight="bold")
text(W - PAD_R, cursor, "JEV", 13, FAINT, font=MONO, weight="bold", ha="right")
cursor += 18 + 22

# ---------------------------------------------------------------- headline
text(PAD_L, cursor, "Cinco formas de pedirle una", 50, INK, font=SERIF, weight="bold")
cursor += 56
text(PAD_L, cursor, "decisión a un modelo de IA", 50, INK, font=SERIF, weight="bold")
cursor += 54 + 18

sub_lines = [
    "No todo lo que “juzga” con IA es un chat generativo. El paper mapea el",
    "panorama en un solo eje: rigidez y momento en que se fija el esquema",
    "de la respuesta — desde fijo en el entrenamiento hasta sin esquema.",
]
for l in sub_lines:
    text(PAD_L, cursor, l, 18, MUTED, font=SANS)
    cursor += 27
cursor += 8

rect(PAD_L, cursor, CONTENT_W, 1.2, LINE)
cursor += 1.2 + 26

# ---------------------------------------------------------------- chart
chart_x0 = PAD_L + 10
chart_w = CONTENT_W - 20
chart_y0 = cursor
chart_h = 560

DX, DY = 12.6, 12.9


def mx(dx):
    return chart_x0 + (dx / DX) * chart_w


def my(dy):
    return chart_y0 + chart_h - (dy / DY) * chart_h


# axis lines
line(chart_x0, chart_y0 + chart_h, chart_x0 + chart_w, chart_y0 + chart_h, LINE, 1.4)
line(chart_x0, chart_y0, chart_x0, chart_y0 + chart_h, LINE, 1.4)

points = [
    dict(dx=1.0, dy=1.2, label=["4. Clasificador", "discriminativo clásico"],
         color=STEEL, lx=18, ly=-6, ha="left"),
    dict(dx=5.2, dy=2.6, label=["5. Jev / evaluación", "tipada"],
         color=CORAL, lx=20, ly=-4, ha="left", r=11),
    dict(dx=6.3, dy=6.2, label=["3. LLM-as-judge"],
         color=STEEL, lx=20, ly=2, ha="left"),
    dict(dx=6.9, dy=9.4, label=["2. Salida forzada"],
         color=WARMGRAY, lx=-20, ly=-22, ha="right"),
    dict(dx=9.8, dy=9.4, label=["1. Chat generativo"],
         color=WARMGRAY, lx=0, ly=-22, ha="center"),
]

for p in points:
    x, y = mx(p["dx"]), my(p["dy"])
    dot(x, y, p.get("r", 9), p["color"])
    ly = y + p["ly"]
    for i, ln in enumerate(p["label"]):
        text(x + p["lx"], ly + i * 20, ln, 15, INK, font=SANS, weight="600" if i == 0 else "normal",
             ha=p["ha"])

# axis labels
text(chart_x0, chart_y0 + chart_h + 26, "RÍGIDO, fijo en entrenamiento", 13, FAINT, font=MONO)
text(chart_x0 + chart_w, chart_y0 + chart_h + 26, "SIN esquema, texto libre", 13, FAINT,
     font=MONO, ha="right")
text(chart_x0 + chart_w / 2, chart_y0 + chart_h + 26, "declarado en cada llamada", 13, FAINT,
     font=MONO, ha="center")
text(chart_x0 - 18, chart_y0, "alto costo", 13, FAINT, font=MONO, ha="right", va="top")
text(chart_x0 - 18, chart_y0 + chart_h, "bajo costo", 13, FAINT, font=MONO, ha="right", va="bottom")

# legend row
leg_y = chart_y0 + chart_h + 56
dot(chart_x0 + 6, leg_y, 6, CORAL)
text(chart_x0 + 20, leg_y, "caso de estudio (Jev)", 13, MUTED, font=SANS, va="center")
dot(chart_x0 + 230, leg_y, 6, STEEL)
text(chart_x0 + 244, leg_y, "evaluador / clasificador", 13, MUTED, font=SANS, va="center")
dot(chart_x0 + 470, leg_y, 6, WARMGRAY)
text(chart_x0 + 484, leg_y, "generativo de propósito general", 13, MUTED, font=SANS, va="center")

cursor = leg_y + 40

# ---------------------------------------------------------------- insight box
box_h = 112
rect(PAD_L, cursor, CONTENT_W, box_h, INSIGHT_BG, edge=INSIGHT_BORDER, lw=1.3)
iy = cursor + 22
text(PAD_L + 28, iy, "LA TRAMPA", 12, CORAL, font=MONO, weight="bold")
iy += 28
for l in ["Solo 3 de las 5 categorías son LLM sin ambigüedad. El clasificador",
          "clásico no lo es — y el propio Jev no confirma su arquitectura."]:
    text(PAD_L + 28, iy, l, 19, INK, font=SERIF)
    iy += 27

cursor += box_h + 26

# ---------------------------------------------------------------- footer
footer_y = cursor + 16
rect(PAD_L, footer_y - 18, CONTENT_W, 1.2, LINE)
text(PAD_L, footer_y, "Maikel Leyva-Vázquez  ·  Neutrosophic Computing and", 14,
     FAINT, font=SANS, style="italic")
text(PAD_L, footer_y + 20, "Machine Learning, 2026", 14, FAINT, font=SANS, style="italic")
text(W - PAD_R, footer_y, "fs.unm.edu/NCML_2 · article/view/186", 13, FAINT,
     font=MONO, ha="right")
text(W - PAD_R, footer_y + 20, "typesafe.ai  ·  github.com/mleyvaz/jev-typed-evaluation-collapse",
     13, FAINT, font=MONO, ha="right")

fig.savefig("linkedin_jev_taxonomy_infographic_es.png", dpi=DPI, facecolor=BG)
print("saved linkedin_jev_taxonomy_infographic_es.png")
