"""Generate images/deepNetYaminsITResponses_2016_labeled.png (figure yamins_2016_responses in InternalRepresentations.tex).

Model-to-brain encoding for one IT site, built on the Yamins and DiCarlo (2016) IT response figure.

Top: a schematic. An image (one of the figure's sample images) is shown to a network and to a monkey. The
network's top-layer vector is mapped by a weighted sum to a single predicted value (red), which is compared to
the single value recorded at one site in IT (black).
Bottom: the published figure, with a legend added: those two values across many images.

Reads images/deepNetYaminsITResponses_2016.png. Unlike the other figures, writes only a PNG (200 dpi), since it is
mostly the published raster image.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from figure_style import IMAGES, OUT, INK, DOT, line, arrow, network, layer_box, strips
from line_art import brain, brain_site

RED = "#c0392b"
DOT = dict(DOT, lw=1.0)

im = Image.open(IMAGES / "deepNetYaminsITResponses_2016.png").convert("RGB")
im = im.crop((150, 0, 835, im.size[1]))   # trim the empty margins at left and right
face = im.crop((55, 22, 257, 196))   # the first sample image, above the arrow that starts below it
w, h = im.size
W, H_IMG, H_TOP = w / 100, h / 100, 1.75

fig = plt.figure(figsize=(W, H_IMG + H_TOP), dpi=100)

# Bottom: the published figure, with a legend in the empty space below the trace.
ax = fig.add_axes([0, 0, 1, H_IMG / (H_IMG + H_TOP)])
ax.imshow(im)
ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
x0, y = 12, 368
for i, (color, label) in enumerate((("black", "recorded IT response"), (RED, "predicted by model-to-brain encoding"))):
    x = x0 + i * 270
    ax.plot([x, x + 30], [y, y], color=color, lw=2.5)
    ax.text(x + 38, y, label, va="center", ha="left", fontsize=11)

# Top: schematic, in inches.
s = fig.add_axes([0, H_IMG / (H_IMG + H_TOP), 1, H_TOP / (H_IMG + H_TOP)])
s.set_xlim(0, W); s.set_ylim(0.3, 0.3 + H_TOP); s.set_aspect("equal"); s.axis("off")

# The image, shown to the network (above) and the monkey (below).
s.imshow(face, extent=(0.1, 1.0, 0.51, 1.29), zorder=1)
arrow(s, (1.05, 1.0), (1.45, 1.2), lw=1.0)
arrow(s, (1.05, 0.65), (5.6, 0.62), lw=1.0, connectionstyle="arc3,rad=0.04")

# Network with its top layer boxed, linked to the top-layer vector.
layers = [(1.0, 4), (1.3, 3), (1.6, 3)]
xs = network(s, 1.75, layers, gap=0.15, r=0.05, lw=0.8, link_lw=0.5)
ty = layers[-1][0]
layer_box(s, xs[-1], ty, 0.1, 0.05, lw=0.9, zorder=1)
C, VX, VY = 0.16, 2.35, 1.2
strips(s, VX, VY, [[0.7, 0.2, 0.5, 0.9, 0.3, 0.6]], C, lw=0.7)
line(s, [xs[-1][-1] + 0.12, VX - 0.05], [ty, VY + C / 2], **DOT)
s.text(VX + 3 * C, VY + C + 0.06, "top-layer vector", ha="center", va="bottom", fontsize=10)

# A weighted sum of the vector predicts one value; an electrode records one value.
PX = 4.75
arrow(s, (VX + 6 * C + 0.08, VY + C / 2), (PX - 0.08, VY + C / 2), lw=1.0)
s.text((VX + 6 * C + PX) / 2, VY + C / 2 + 0.08, "model → brain\n(encoding)", ha="center", va="bottom",
       fontsize=10)
s.add_patch(Rectangle((PX, VY), C, C, facecolor=RED, edgecolor=RED, lw=1.6, zorder=3))
s.text(PX + C + 0.08, VY + C / 2, "predicted", ha="left", va="center", fontsize=10, color=RED)
RY = 0.75
s.add_patch(Rectangle((PX, RY), C, C, facecolor="0.35", edgecolor=INK, lw=1.6, zorder=3))
s.text(PX + C + 0.08, RY + C / 2, "recorded", ha="left", va="center", fontsize=10)

bx, by, bk = 6.2, 0.85, 0.5
brain(s, bx, by, bk)
tip = brain_site(bx, by, bk)
line(s, [tip[0] - 0.05, PX + C + 0.75], [tip[1], RY + C / 2], z=6, **DOT)

fig.savefig(OUT / "deepNetYaminsITResponses_2016_labeled.png", dpi=200)
plt.close(fig)
