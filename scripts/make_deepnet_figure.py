"""Generate images/deepNetExample.{svg,pdf,png} (figure deepNetExample in ConvolutionalNetworks.tex).

Redraw of an image by Soraya Boza and Jeff Yoshimi, in the shared style of cnn_figure_style.py.
An AlexNet-like pipeline: input 3x227x227 -> 96 filters (3x11x11, stride 4) -> 3x3 max pooling (stride 2)
-> 120 filters (96x3x3, stride 3) -> flatten -> dense layer with 3 nodes. Boxes are schematic, not to
scale. Output shapes are computed with the sliding-window formula and checked against the labels.

Usage: python3 scripts/make_deepnet_figure.py [outdir]   (default: images)
"""
import sys
import math
from matplotlib.patches import Circle
from cnn_figure_style import new_fig, finish, poly, TOP_FACE, SIDE_FACE, EDGE

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"


def out_size(n, window, stride):
    return (n - window) // stride + 1


# Shapes, computed rather than typed
C0, H0 = 3, 227
H1 = out_size(H0, 11, 4); C1 = 96
H2 = out_size(H1, 3, 2); C2 = C1
H3 = out_size(H2, 3, 3); C3 = 120
FLAT = C3 * H3 * H3
assert (H1, H2, H3, FLAT) == (55, 27, 9, 9720)

face = lambda h: 0.3 + 0.25 * math.log2(h / 9)     # drawn size of the front face (schematic)
depth = lambda c: 0.06 + 0.0045 * c                # drawn depth (schematic)
SHAPE_FONT = dict(fontsize=10, ha="center", va="top", color="0.1")
OP_FONT = dict(fontsize=8.5, ha="center", va="top", multialignment="left", color="0.2", linespacing=1.3)

fig, ax = new_fig((13, 3.8))
BASE = -0.85                                       # top of shape labels
OP_TOP = -1.4                                      # top of operation descriptions
CENTERS, OPS = [], []                              # shape-label centers; (arrow midpoint, text) pairs


def solid(x, h, c, label):
    """Solid box centered vertically on y = 0 (front face plus depth); returns its right edge."""
    s, d = face(h), depth(c)
    y = -(s + d) / 2
    front = [(x, y), (x+s, y), (x+s, y+s), (x, y+s)]
    top = [(x, y+s), (x+s, y+s), (x+s+d, y+s+d), (x+d, y+s+d)]
    side = [(x+s, y), (x+s+d, y+d), (x+s+d, y+s+d), (x+s, y+s)]
    poly(ax, front, facecolor="white", edgecolor="none")
    poly(ax, top, facecolor=TOP_FACE, edgecolor="none")
    poly(ax, side, facecolor=SIDE_FACE, edgecolor="none")
    for p in (top, side, front):
        poly(ax, p, z=3, fill=False, **EDGE)
    ax.text(x + s / 2, BASE, label, **SHAPE_FONT)     # centered under the front face
    CENTERS.append(x + s / 2)
    return x + s + d


def nodes(x, count, label, dots=False):
    """A column of nodes centered on y = 0; with dots, a gap of vertical dots in the middle."""
    r = 0.09
    ys = [0.62, 0.36, -0.36, -0.62] if dots else [0.26, 0, -0.26]
    for y in ys:
        ax.add_patch(Circle((x + r, y), r, facecolor="white", zorder=3, **EDGE))
    if dots:
        for y in (-0.12, 0, 0.12):
            ax.plot([x + r], [y], marker="o", ms=1.5, color="0.2", zorder=3)
    ax.text(x + r, BASE, label, **SHAPE_FONT)
    CENTERS.append(x + r)
    return x + 2 * r


def arrow(x0, text, length=1.75):
    ax.annotate("", xy=(x0 + length - 0.1, 0), xytext=(x0 + 0.1, 0),
                arrowprops=dict(arrowstyle="-|>", color="0.2", lw=0.8, mutation_scale=9))
    OPS.append((x0 + length / 2, text))            # description placed once all label centers are known
    return x0 + length


x = solid(0.0, H0, C0, f"{C0}×{H0}×{H0}")
x = arrow(x, f"Bank of {C1} filters,\neach {C0}×11×11\nStride 4")
x = solid(x, H1, C1, f"{C1}×{H1}×{H1}")
x = arrow(x, "Max pooling\nPool shape 3×3\nStride 2")
x = solid(x, H2, C2, f"{C2}×{H2}×{H2}")
x = arrow(x, f"Bank of {C3} filters,\neach {C2}×3×3\nStride 3")
x = solid(x, H3, C3, f"{C3}×{H3}×{H3}")
x = arrow(x, "Flatten", 1.2)
x = nodes(x, 4, f"{FLAT} nodes", dots=True)
x = arrow(x, "Dense", 1.5)
nodes(x, 3, "3 nodes")

# Each description is centered between the shape labels on either side, with a dotted leader up to its arrow
for i, (xm, text) in enumerate(OPS):
    xc = (CENTERS[i] + CENTERS[i + 1]) / 2
    ax.plot([xm, xc], [-0.04, OP_TOP + 0.04], color="0.4", lw=0.7, ls=(0, (1, 2)), zorder=2)
    ax.text(xc, OP_TOP, text, **OP_FONT)

ax.autoscale_view()
finish(fig, ax, OUT, "deepNetExample")
