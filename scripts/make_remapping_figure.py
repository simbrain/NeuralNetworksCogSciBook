"""Generate images/remappingLetters.{svg,pdf,png} (figure remappingClusters in InternalRepresentations.tex).

Remapping. A network (pixel-grid input, hidden layer, two output nodes) sits at left, with dotted lines from its
input and hidden layers to pictures of the input space and hidden-unit space. In the input space, uppercase A and
lowercase a form separate clusters with o between them (not linearly separable); in the hidden-unit space the A's
merge into one cluster, separate from the o's.
"""
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from figure_style import INK, DOT, new_fig, finish, line, rounded_box, nodes, links, layer_box

R = 0.045
rng = np.random.default_rng(7)


def cluster(ax, cx, cy, n, filled, sx=0.42, sy=0.32):
    # Points spread evenly over an ellipse, jittered, so there are no stray outliers.
    i = np.arange(n) + 0.5
    rr, th = np.sqrt(i / n), i * np.pi * (3 - np.sqrt(5))
    pts = np.c_[cx + sx * rr * np.cos(th), cy + sy * rr * np.sin(th)] + rng.normal(0, 0.03, (n, 2))
    for x, y in pts:
        ax.add_patch(Circle((x, y), R, facecolor=INK if filled else "white", edgecolor=INK, lw=0.7, zorder=3))


def panel(ax, x, y, w, h, label):
    rounded_box(ax, x, y, w, h, 0.2, facecolor="white", ls=(0, (1, 2)), zorder=0)
    ax.text(x + 0.15, y + h - 0.12, label, ha="left", va="top", fontsize=9)


def arrow(ax, p, q, rad):
    """Dotted curved line from p to q with a solid arrowhead (a dotted style would also dot the head)."""
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-",
                                 color="0.35", lw=0.8, ls=(0, (1, 2)), zorder=2, shrinkA=0, shrinkB=0))
    # arc3 is a quadratic Bezier; its end tangent runs from the control point to q.
    p, q = np.array(p), np.array(q)
    d = q - p
    ctrl = (p + q) / 2 + rad * np.array([d[1], -d[0]])
    t = (q - ctrl) / np.linalg.norm(q - ctrl)
    ax.add_patch(FancyArrowPatch(q - 0.12 * t, q, arrowstyle="-|>,head_length=5,head_width=2.5",
                                 color="0.35", lw=0.8, zorder=2, shrinkA=0, shrinkB=0))


def letter(ax, x, y, s, size=15):
    ax.text(x, y, s, ha="center", va="center", fontsize=size, family="serif", zorder=4)


fig, ax = new_fig((6.6, 4.6))

# Network: a pixel image of "A" as input, a hidden layer, and output nodes for "A" and "o".
NX, C = 0.9, 0.14
A = ["...#...", "..#.#..", "..#.#..", ".#...#.", ".#####.", "#.....#", "#.....#"]
gx0, gy0 = NX - 3.5 * C, 0.71
for r, row in enumerate(A):
    for c, ch in enumerate(row):
        ax.add_patch(Rectangle((gx0 + c * C, gy0 + (6 - r) * C), C, C, facecolor="0.3" if ch == "#" else "white",
                               edgecolor="0.78", lw=0.4, zorder=3))
ax.add_patch(Rectangle((gx0, gy0), 7 * C, 7 * C, facecolor="none", edgecolor=INK, lw=0.8, zorder=4))
gtop = gy0 + 7 * C

y_hid, y_out = 3.6, 4.65
xh = nodes(ax, NX, y_hid, [0.8, 0.1, 0.6, 0.0, 0.4], gap=0.27, r=0.1, lw=0.8)
xo = nodes(ax, NX, y_out, [0.9, 0.05], gap=0.5, r=0.1, lw=0.8)
for x in np.linspace(gx0 + 0.15, gx0 + 7 * C - 0.15, 4):
    for h in xh:
        line(ax, [x, h], [gtop, y_hid - 0.1], color="0.8", lw=0.4, z=1)
links(ax, xh, y_hid, xo, y_out, r=0.1, lw=0.5)
letter(ax, xo[0], y_out + 0.27, "A", size=11)
letter(ax, xo[1], y_out + 0.27, "o", size=11)

# Panels picturing the input space and the hidden-unit space.
PX, PW = 2.0, 4.0
panel(ax, PX, 0.0, PW, 2.4, "Input space")
panel(ax, PX, 2.85, PW, 1.5, "Hidden-unit space")

# Dotted lines from the network's input and hidden layers to the panels.
line(ax, [gx0 + 7 * C, PX], [gtop, 2.4], **DOT)
line(ax, [gx0 + 7 * C, PX], [gy0, 0.0], **DOT)
_, hx1 = layer_box(ax, xh, y_hid, 0.17, 0.1)
line(ax, [hx1, PX], [y_hid + 0.17, 4.35], **DOT)
line(ax, [hx1, PX], [y_hid - 0.17, 2.85], **DOT)

# Input space: A and a are far apart, with o between them.
dx = PX - 0.2
cluster(ax, dx + 1.05, 0.65, 16, True)
cluster(ax, dx + 2.1, 1.15, 16, False)
cluster(ax, dx + 3.2, 1.75, 16, True)
letter(ax, dx + 0.45, 0.65, "A")
letter(ax, dx + 2.1, 0.62, "o")
letter(ax, dx + 3.75, 1.8, "a")

# Hidden-unit space: the A's merge, separate from the o's.
cluster(ax, dx + 1.55, 3.5, 20, True, sx=0.4, sy=0.3)
cluster(ax, dx + 3.15, 3.5, 16, False, sx=0.36, sy=0.28)
letter(ax, dx + 0.72, 3.5, "A a")
letter(ax, dx + 3.7, 3.5, "o")

arrow(ax, (dx + 1.1, 1.05), (dx + 1.4, 3.15), -0.15)
arrow(ax, (dx + 3.1, 2.1), (dx + 1.75, 3.15), 0.25)
arrow(ax, (dx + 2.15, 1.5), (dx + 3.05, 3.15), -0.2)

finish(fig, ax, "remappingLetters", xlim=(0.1, 6.1), ylim=(-0.1, 5.0))
