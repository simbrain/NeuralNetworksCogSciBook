"""Generate images/llmWorldMapProbe.{svg,pdf,png} (figure llmWorldMap in LLMsCogSci.tex).

A linear probe reads a place's location off an LLM's residual stream. Left: a place name ("Merced") enters a
transformer's residual stream (drawn as in the linear probe figure of the mechanistic interpretability chapter),
and a probe on one layer outputs a latitude and longitude (Merced's actual location, for illustration).
Right: the world map of probe predictions for held-out places from Gurnee and Tegmark (2024).

Reads images/llmWorldMap.png.
"""
import numpy as np
from matplotlib.patches import Ellipse, Polygon
from figure_style import IMAGES, INK, new_fig, finish, line, arrow, rounded_box, place_image

FS = 7.5

fig, ax = new_fig((6.6, 3.0))


def block(x, y, w, h, text):
    rounded_box(ax, x, y, w, h, 0.06, facecolor="white", edgecolor=INK, zorder=3)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=FS, zorder=4)


# Residual stream, from the embedding up through two sublayers; more layers above (dotted).
SX = 1.15
line(ax, [SX, SX], [0.62, 2.35], color=INK, lw=1.0)
line(ax, [SX, SX], [2.38, 2.6], color=INK, lw=1.0, ls=(0, (1, 2)))
ax.text(SX, 0.0, "\u201cMerced\u201d", ha="center", va="bottom", fontsize=FS + 1, style="italic")
arrow(ax, (SX, 0.17), (SX, 0.32))
block(SX - 0.5, 0.32, 1.0, 0.3, "embedding")
for (y0, y1, name) in [(0.78, 1.28, "attention"), (1.45, 1.95, "MLP")]:
    bx, bw, bh = SX - 1.12, 0.8, 0.26
    by = (y0 + y1) / 2 - bh / 2
    block(bx, by, bw, bh, name)
    cx = bx + bw / 2
    line(ax, [SX, cx, cx], [y0, y0, by], color=INK, lw=0.8)
    ax.plot([SX], [y0], "o", color=INK, ms=2.5, zorder=4)
    line(ax, [cx, cx], [by + bh, y1], color=INK, lw=0.8)
    arrow(ax, (cx, y1), (SX - 0.03, y1))
    ax.plot([SX], [y1], "o", color=INK, ms=2.5, zorder=4)

# The probe on the residual stream, and its output.
# Electrode facing left (into the empty space above the sublayers), its wire running straight to an oval
# around the output.
tip = np.array([SX - 0.01, 2.15])
a = np.radians(155)
u, n = np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])
p0, p1 = tip + 0.22 * u, tip + 0.45 * u
line(ax, [tip[0], p0[0]], [tip[1], p0[1]], color=INK, lw=0.8, z=7)
bw = 0.03
ax.add_patch(Polygon([p0 + bw * n, p1 + bw * n, p1 - bw * n, p0 - bw * n], closed=True, facecolor="white",
                     edgecolor=INK, lw=0.8, joinstyle="round", zorder=7))
OW, OH = 1.45, 0.3
end = tip + 0.62 * u                      # right end of the oval
center = end - np.array([OW / 2, 0])
line(ax, [p1[0], end[0]], [p1[1], end[1]], color=INK, lw=0.7, z=7)
ax.add_patch(Ellipse(center, OW, OH, facecolor="white", edgecolor=INK, lw=0.8, zorder=7))
ax.text(*center, "37.3\u00b0 N, 120.5\u00b0 W", ha="center", va="center", fontsize=FS, zorder=8)
XL = center[0] - OW / 2 - 0.05

# Right: probe predictions for held-out places.
MW = 4.1
MX, MY = 1.75, 0.35
place_image(ax, IMAGES / "llmWorldMap.png", MX, MY, MW)

finish(fig, ax, "llmWorldMapProbe", xlim=(XL, MX + MW + 0.02), ylim=(-0.05, 2.65))
