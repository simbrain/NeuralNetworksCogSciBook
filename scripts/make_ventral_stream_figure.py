"""Generate images/ventralStreamNetwork.{svg,pdf,png} (figure ventralStreamNetwork in InternalRepresentations.tex).

A deep network as a model of the ventral visual stream. An apple is shown to a brain (top, facing right) and to a
deep network (bottom, flowing left to right). Areas V1, V2, V4, and IT are marked along the ventral stream, and
dashed lines pair each network layer with the area it best predicts: early layers with early areas, the top layer
with IT. Below each layer, an icon shows the kind of feature its units (and the paired area's neurons) respond to:
edges, textures, shapes, and objects.
"""
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon, Rectangle
from figure_style import INK, new_fig, finish, line, arrow
from line_art import apple, brain

LINK = dict(color="0.35", lw=0.9, ls=(0, (4, 3)))
R = 0.06

fig, ax = new_fig((5.0, 3.4))

# Brain facing right, so that the ventral stream runs left to right like the network.
bx, by, bk = 2.55, 2.2, 1.25
brain(ax, bx, by, bk, mirror=True, cerebellum=False)
areas = [("V1", 0.9, 0.08), ("V2", 0.66, -0.03), ("V4", 0.38, -0.12), ("IT", 0.0, -0.22)]
area_xy = [(bx - bk * px, by + bk * py) for _, px, py in areas]
ax.add_patch(FancyArrowPatch(area_xy[0], area_xy[-1], connectionstyle="arc3,rad=0.12", arrowstyle="-|>",
                             mutation_scale=7, color="0.55", lw=0.8, shrinkA=8, shrinkB=8, zorder=5))
for (name, _, _), (x, y) in zip(areas, area_xy):
    ax.add_patch(Circle((x, y), 0.07, facecolor="0.6", edgecolor=INK, lw=0.6, zorder=6))
    ax.text(x, y + 0.11, name, ha="center", va="bottom", fontsize=8, zorder=6)

# Deep network: an input layer and four layers, getting smaller toward the top layer.
sizes = [6, 6, 5, 4, 3]
ny = 0.55
xs = [0.9 + 0.62 * i for i in range(len(sizes))]
cols = [ny + 0.17 * (np.arange(n) - (n - 1) / 2) for n in sizes]
for x0, x1, a, b in zip(xs, xs[1:], cols, cols[1:]):
    for p in a:
        for q in b:
            line(ax, [x0 + R, x1 - R], [p, q], color="0.78", lw=0.35, z=1)
for x, col in zip(xs, cols):
    for y in col:
        ax.add_patch(Circle((x, y), R, facecolor="white", edgecolor=INK, lw=0.7, zorder=3))

# The same image is shown to both.
apple(ax, 0.05, 1.45, s=0.6)
arrow(ax, (0.25, 1.55), (area_xy[0][0] - 0.12, area_xy[0][1] - 0.02))
arrow(ax, (0.2, 1.3), (xs[0] - 0.12, ny + 0.2))

# Each layer after the input is paired with one area.
for x, col, (ax_, ay) in zip(xs[1:], cols[1:], area_xy):
    line(ax, [x, ax_], [col[-1] + R + 0.04, ay - 0.1], z=7, **LINK)


def feature_icon(ax, cx, cy, kind, d=0.3):
    """A small square showing the kind of feature a layer responds to."""
    sq = Rectangle((cx - d / 2, cy - d / 2), d, d, facecolor="none", edgecolor=INK, lw=0.6, zorder=4)
    ax.add_patch(sq)
    arts = []
    if kind == "edges":
        a = np.radians(65)
        u, n = np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])
        c = np.array([cx, cy])
        arts.append(Polygon([c + d * u, c + d * u + d * n, c - d * u + d * n, c - d * u], closed=True,
                            facecolor="0.45", edgecolor="none", zorder=3.5))
    elif kind == "textures":
        rng = np.random.default_rng(3)
        g = np.linspace(-0.36, 0.36, 4) * d
        for x in g:
            for y in g:
                t = rng.uniform(0, np.pi)
                dx, dy = 0.07 * d * np.cos(t), 0.07 * d * np.sin(t)
                ax.plot([cx + x - dx, cx + x + dx], [cy + y - dy, cy + y + dy], color=INK, lw=0.9, zorder=3.5,
                        solid_capstyle="round")
    elif kind == "shapes":
        arts.append(Arc((cx + 0.3 * d, cy - 0.3 * d), 1.1 * d, 1.1 * d, theta1=90, theta2=180, color=INK, lw=1.6,
                        zorder=3.5))
    elif kind == "objects":
        apple(ax, cx, cy + 0.01, s=0.42, lw=0.6)
    for art in arts:
        ax.add_patch(art)
        art.set_clip_path(sq)
    ax.text(cx, cy - d / 2 - 0.06, kind, ha="center", va="top", fontsize=7)


for x, kind in zip(xs[1:], ("edges", "textures", "shapes", "objects")):
    feature_icon(ax, x, -0.25, kind)

finish(fig, ax, "ventralStreamNetwork", xlim=(-0.25, 4.1), ylim=(-0.6, 3.3))
