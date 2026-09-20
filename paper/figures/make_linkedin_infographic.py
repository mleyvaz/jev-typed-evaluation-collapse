# -*- coding: utf-8 -*-
"""Static PNG infographic for the LinkedIn post (Jev field note). Mirrors the
Artifact design canvas but rendered as a flat, upload-ready image via
matplotlib, using Windows system fonts (Georgia / Segoe UI / Consolas)."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

W, H = 1080, 1180
DPI = 200
PX = 72 / DPI  # px(css-like) -> pt conversion at this dpi


def pt(px):
    return px * PX


BG = "#17140F"
INK = "#F2EEE6"
MUTED = "#B9B2A4"
FAINT = "#8A8375"
CORAL = "#E58A63"
SAGE = "#9AC29A"
GOLD = "#D8C496"
CARD_BG = "#211E19"
CARD_BORDER = "#2D2A25"
INSIGHT_BG = "#271D16"
INSIGHT_BORDER = "#5F3D2C"
CORAL_BADGE_BG = "#3C291E"
SAGE_BADGE_BG = "#2F3328"
GOLD_BADGE_BG = "#3A3427"

SERIF = "Georgia"
SANS = "Segoe UI"
MONO = "Consolas"

fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)  # inverted: y grows downward like screen coords
ax.axis("off")
ax.set_facecolor(BG)

PAD_L, PAD_R, PAD_T = 76, 76, 68
CONTENT_W = W - PAD_L - PAD_R


def text(x, y, s, size, color, font=SANS, weight="normal", ha="left", va="top",
          style="normal", spacing=None):
    kw = dict(fontsize=pt(size), color=color, fontfamily=font, fontweight=weight,
              ha=ha, va=va, fontstyle=style)
    ax.text(x, y, s, **kw)


def rect(x, y, w, h, face, edge=None, lw=1.0):
    p = mpatches.Rectangle((x, y), w, h, facecolor=face,
                            edgecolor=edge if edge else "none", linewidth=lw)
    ax.add_patch(p)
    return p


def badge(x_right, y, label, fg, bg):
    # approximate width from label length
    w = 16 + len(label) * 7.6
    h = 24
    rect(x_right - w, y, w, h, bg, edge=fg, lw=1.1)
    text(x_right - w / 2, y + h / 2 + 1, label, 11, fg, font=MONO, weight="bold",
         ha="center", va="center")
    return w


# ---------------------------------------------------------------- eyebrow
cursor = PAD_T
text(PAD_L, cursor, "FIELD NOTE  ·  TYPED EVALUATION MODELS", 13, CORAL,
     font=MONO, weight="bold")
text(W - PAD_R, cursor, "JEV", 13, FAINT, font=MONO, weight="bold", ha="right")
cursor += 18 + 22

# ---------------------------------------------------------------- headline
text(PAD_L, cursor, "Does Jev’s speed come", 54, INK, font=SERIF, weight="bold")
cursor += 60
text(PAD_L, cursor, "with a hidden cost?", 54, INK, font=SERIF, weight="bold")
cursor += 58 + 20

# ---------------------------------------------------------------- subhead
sub_lines = [
    "Jev promises 20–200× the speed and up to 400× lower cost of a",
    "frontier LLM judge. Four experiments test what that trade-off",
    "costs: can it still tell conflicting evidence from no evidence at all?",
]
for line in sub_lines:
    text(PAD_L, cursor, line, 19, MUTED, font=SANS)
    cursor += 29
cursor += 6

# ---------------------------------------------------------------- divider
rect(PAD_L, cursor, CONTENT_W, 1.2, "#3A352C")
cursor += 1.2 + 28

# ---------------------------------------------------------------- grid
GAP = 22
CARD_W = (CONTENT_W - GAP) / 2
CARD_H = 232
grid_top = cursor

cards = [
    dict(num="EXPERIMENT 1", badge_="COLLAPSES", badge_fg=CORAL, badge_bg=CORAL_BADGE_BG,
         type_="type: boolean / Noul", value="0.46–0.57",
         desc=["Contradicting witnesses and total",
               "silence land in the same probability",
               "band — indistinguishable."]),
    dict(num="EXPERIMENT 2", badge_="SEPARATES", badge_fg=SAGE, badge_bg=SAGE_BADGE_BG,
         type_="type: Choice, named options", value="100%",
         desc=["A richer schema separates conflict",
               "from ignorance with full confidence,",
               "every time."]),
    dict(num="EXPERIMENT 3", badge_="BIASED", badge_fg=CORAL, badge_bg=CORAL_BADGE_BG,
         type_="type: Choice, binary (no escape)", value="0.67–0.85",
         desc=["Remove the escape categories and an",
               "unexpected directional bias appears —",
               "even with zero evidence."]),
    dict(num="EXPERIMENT 4", badge_="PARTIAL", badge_fg=GOLD, badge_bg=GOLD_BADGE_BG,
         type_="type: Score, ordinal rubric", value="2.04 vs 3.95",
         desc=["A second-order question on certainty",
               "separates the extremes, but fails to",
               "order the middle."]),
]

for i, c in enumerate(cards):
    col = i % 2
    row = i // 2
    cx = PAD_L + col * (CARD_W + GAP)
    cy = grid_top + row * (CARD_H + GAP)
    rect(cx, cy, CARD_W, CARD_H, CARD_BG, edge=CARD_BORDER, lw=1.2)

    ic = cx + 26
    iy = cy + 22
    text(ic, iy, c["num"], 12, FAINT, font=MONO, weight="bold")
    badge(cx + CARD_W - 24, iy - 6, c["badge_"], c["badge_fg"], c["badge_bg"])
    iy += 30
    text(ic, iy, c["type_"], 13, MUTED, font=MONO)
    iy += 34
    text(ic, iy, c["value"], 34, INK, font=SERIF, weight="bold")
    iy += 46
    for line in c["desc"]:
        text(ic, iy, line, 14.5, MUTED, font=SANS)
        iy += 20

cursor = grid_top + CARD_H * 2 + GAP + 30

# ---------------------------------------------------------------- insight box
box_h = 128
rect(PAD_L, cursor, CONTENT_W, box_h, INSIGHT_BG, edge=INSIGHT_BORDER, lw=1.3)
iy = cursor + 24
text(PAD_L + 30, iy, "THE PATTERN", 12, CORAL, font=MONO, weight="bold")
iy += 30
insight_lines = [
    "It’s not scalar vs. categorical output that matters — it’s",
    "which question your schema forces the model to answer.",
    "The cheapest interface throws away information by construction.",
]
for line in insight_lines:
    text(PAD_L + 30, iy, line, 21, INK, font=SERIF)
    iy += 30

# ---------------------------------------------------------------- footer
footer_y = H - 74
rect(PAD_L, footer_y - 20, CONTENT_W, 1.2, "#3A352C")
text(PAD_L, footer_y, "Maikel Leyva-Vázquez  ·  Neutrosophic Computing and", 14,
     FAINT, font=SANS, style="italic")
text(PAD_L, footer_y + 20, "Machine Learning, 2026", 14, FAINT, font=SANS, style="italic")
text(W - PAD_R, footer_y, "fs.unm.edu/NCML_2 · article/view/186", 13, FAINT,
     font=MONO, ha="right")
text(W - PAD_R, footer_y + 20, "github.com/mleyvaz/jev-typed-evaluation-collapse", 13,
     FAINT, font=MONO, ha="right")

fig.savefig("linkedin_jev_infographic.png", dpi=DPI, facecolor=BG)
print("saved linkedin_jev_infographic.png")
