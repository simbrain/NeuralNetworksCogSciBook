"""Generate images/representationStateSpace.{svg,pdf,png} (figure repStateSpace in InternalRepresentations.tex).

The opening figure of the representations chapter: an apple produces a pattern of activation
across three node layers, and the hidden-layer pattern is a point in a state space. The apples lie near
each other, the bananas lie near each other, a region around both represents fruit, and the kittens lie
farther away.
"""
import numpy as np
from matplotlib.patches import Circle, Ellipse
from figure_style import INK, DOT, new_fig, finish, line, arrow, rounded_box, nodes, links, layer_box
from line_art import apple, banana, kitten

LW = 0.9
LAYER = dict(r=0.13, lw=LW)      # node layers

# Each apple, banana, and kitten has a slightly different shape.
APPLES = [dict(), dict(sx=1.08, sy=0.92, rot=0.12, stem=0.1),
          dict(sx=0.9, sy=1.05, rot=-0.1, leaf=False, stem=0.02)]
BANANAS = [dict(rot=0.55), dict(bend=1.3, length=0.88, thick=1.15, rot=0.35)]
KITTENS = [dict(), dict(tilt=0.25, sx=1.15)]

fig, ax = new_fig((7.0, 3.6))

# Apples, bananas, and kittens along the bottom; the first apple is the current input.
NX = 1.45
fx = NX - 0.76 + 0.5 * np.arange(7) + np.r_[0, 0, 0, 0, 0, 0.08, 0.2]
for xx, kw in zip(fx[:3], APPLES):
    apple(ax, xx, 0.0, s=0.8, **kw)
for xx, kw in zip(fx[3:5], BANANAS):
    banana(ax, xx, 0.0, s=0.7, **kw)
for xx, kw in zip(fx[5:], KITTENS):
    kitten(ax, xx + 0.05, 0.02, s=0.8, **kw)
arrow(ax, (fx[0], 0.36), (fx[0], 0.68), lw=LW)

# Hidden-unit points: apples, bananas, kittens. The first apple matches the hidden activations below.
apple_pts = [(0.37, 0.24), (0.24, 0.31), (0.34, 0.42)]
banana_pts = [(0.25, 0.7), (0.34, 0.82)]
kitten_pts = [(0.86, 0.42), (0.93, 0.62)]

# Three node layers, bottom to top, shaded by activation.
y_in, y_hid, y_out = 0.85, 1.85, 2.85
xin = nodes(ax, NX, y_in, [0.9, 0.2, 0.7, 0.0, 0.5], gap=0.38, **LAYER)
xhid = nodes(ax, NX, y_hid, list(apple_pts[0]), gap=0.55, **LAYER)
xout = nodes(ax, NX, y_out, [0.1, 0.85, 0.2], gap=0.38, **LAYER)
links(ax, xin, y_in, xhid, y_hid, r=0.13, lw=0.5)
links(ax, xhid, y_hid, xout, y_out, r=0.13, lw=0.5)

# State space of the two hidden nodes.
sx0, sy0, W, H = 3.3, 0.75, 2.6, 2.1
rounded_box(ax, sx0 - 0.15, sy0 - 0.15, W + 0.3, H + 0.3, 0.15, facecolor="white", ls=(0, (1, 2)), zorder=0)
# The axes' origin sits a little below the lowest points, so no region touches the horizontal axis.
for tip in ((sx0 + W - 0.1, sy0 - 0.02), (sx0 + 0.1, sy0 + H - 0.1)):
    arrow(ax, (sx0 + 0.1, sy0 - 0.02), tip)


def sp(u, v):
    """Map hidden activations (u, v) in [0, 1] to figure coordinates."""
    return sx0 + 0.1 + u * (W - 0.4), sy0 + 0.1 + v * (H - 0.4)


def region(extents, scale=1.25, pad=0.05):
    """Faint solid ellipse around a set of (xmin, xmax, ymin, ymax) extents. Returns the ellipse's own extents."""
    e = np.array(extents)
    x0, x1, y0, y1 = e[:, 0].min(), e[:, 1].max(), e[:, 2].min(), e[:, 3].max()
    c, w, h = ((x0 + x1) / 2, (y0 + y1) / 2), scale * (x1 - x0) + pad, scale * (y1 - y0) + pad
    ax.add_patch(Ellipse(c, w, h, facecolor="none", edgecolor="0.72", lw=0.8, zorder=2))
    return [c[0] - w / 2, c[0] + w / 2, c[1] - h / 2, c[1] + h / 2]


def enclosing_region(ellipses, margin=0.08):
    """Faint ellipse that contains each of the given ellipses (as extents), with a margin."""
    t = np.linspace(0, 2 * np.pi, 200)
    pts = np.vstack([np.c_[(e[0] + e[1]) / 2 + (e[1] - e[0]) / 2 * np.cos(t),
                           (e[2] + e[3]) / 2 + (e[3] - e[2]) / 2 * np.sin(t)] for e in ellipses])
    c = (pts.min(axis=0) + pts.max(axis=0)) / 2
    half = (pts.max(axis=0) - pts.min(axis=0)) / 2
    k = np.sqrt((((pts - c) / half) ** 2).sum(axis=1).max())
    w, h = 2 * (k * half + margin)
    ax.add_patch(Ellipse(c, w, h, facecolor="none", edgecolor="0.72", lw=0.8, zorder=2))


groups = {}
for name, pts, draw, kws, dx, dy, sc in (("apples", apple_pts, apple, APPLES, 0.16, 0.0, 0.38),
                                         ("bananas", banana_pts, banana, BANANAS, 0.24, 0.03, 0.36),
                                         ("kittens", kitten_pts, kitten, KITTENS, 0.18, 0.02, 0.4)):
    ext = []
    for (u, v), kw in zip(pts, kws):
        p = sp(u, v)
        ax.add_patch(Circle(p, 0.04, color=INK, zorder=4))
        draw(ax, p[0] + dx, p[1] + dy, s=sc, lw=0.7, **kw)
        ext.append((p[0] - 0.05, p[0] + dx + 0.12, p[1] + dy - 0.12, p[1] + dy + 0.12))
    groups[name] = ext

# Regions for apples, bananas, fruit, and animals.
a = region(groups["apples"])
b = region(groups["bananas"])
enclosing_region([a, b])
region(groups["kittens"], pad=0.15)

# Dotted lines from the hidden layer to the state space.
_, hx1 = layer_box(ax, xhid, y_hid, 0.2, 0.12)
line(ax, [hx1, sx0 - 0.15], [y_hid + 0.2, sy0 + H], **DOT)
line(ax, [hx1, sx0 - 0.15], [y_hid - 0.2, sy0], **DOT)

finish(fig, ax, "representationStateSpace", xlim=(0.35, 6.25), ylim=(-0.35, 3.1))
