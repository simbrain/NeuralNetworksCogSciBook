"""Generate images/rsaComparison.{svg,pdf,png} (figure rsaComparison in InternalRepresentations.tex).

Representational similarity analysis (RSA). Two rows: a network (top) and a brain with a recorded region circled
(bottom). Each system's responses to two apples and a banana are points in its state space, arranged differently
in the two systems but with the same relations (the apples close, the banana far). Each system's pairwise
similarities form a 3 x 3 table, and the two tables can be compared directly.
"""
import numpy as np
from matplotlib.patches import Circle, Rectangle
from figure_style import INK, DOT, new_fig, finish, line, gray, arrow, rounded_box, network, layer_box
from line_art import apple, banana, brain, brain_site

STIM = [(apple, dict()), (apple, dict(sx=1.08, sy=0.92, rot=0.12, stem=0.1)), (banana, dict(rot=0.55))]


def icon(ax, i, x, y, s):
    draw, kw = STIM[i]
    draw(ax, x, y, s=s * (0.9 if draw is banana else 1.0), lw=0.6, **kw)


def state_space(ax, x0, y0, w, h, pts):
    rounded_box(ax, x0, y0, w, h, 0.12, facecolor="white", ls=(0, (1, 2)), zorder=0)
    for i, (u, v) in enumerate(pts):
        p = (x0 + 0.15 + u * (w - 0.5), y0 + 0.15 + v * (h - 0.35))
        ax.add_patch(Circle(p, 0.035, color=INK, zorder=4))
        icon(ax, i, p[0] + 0.15, p[1], 0.3)


def table(ax, x0, y0, pts, c=0.3):
    """3 x 3 table of pairwise similarities (darker is more similar), rows and columns labeled with icons."""
    P = np.array(pts)
    d = np.linalg.norm(P[:, None] - P[None], axis=2)
    sim = 1 - d / 1.1
    for r in range(3):
        for col in range(3):
            ax.add_patch(Rectangle((x0 + col * c, y0 + (2 - r) * c), c, c, facecolor=gray(sim[r, col], 1.0, 0.2),
                                   edgecolor="0.6", lw=0.5, zorder=2))
        icon(ax, r, x0 - 0.2, y0 + (2 - r) * c + c / 2, 0.3)
        icon(ax, r, x0 + r * c + c / 2, y0 + 3 * c + 0.18, 0.3)
    ax.add_patch(Rectangle((x0, y0), 3 * c, 3 * c, facecolor="none", edgecolor=INK, lw=0.8, zorder=3))


fig, ax = new_fig((6.2, 3.6))

# Rows: network on top, brain below.
ROW_NET, ROW_BRAIN = 2.05, 0.0
SX, SW, SH = 1.75, 1.5, 1.35
TX = 4.15

# Network: three layers, hidden layer boxed, with dotted lines to its state space.
nx = 0.65
layers = [(ROW_NET + 0.12, 4), (ROW_NET + 0.67, 3), (ROW_NET + 1.22, 2)]
xs = network(ax, nx, layers, gap=0.25, r=0.08, color="0.75")
hy = layers[1][0]
_, hx1 = layer_box(ax, xs[1], hy, 0.15, 0.08)
line(ax, [hx1, SX], [hy + 0.15, ROW_NET + SH], **DOT)
line(ax, [hx1, SX], [hy - 0.15, ROW_NET], **DOT)

# Brain, with a circle marking the recorded region in the temporal lobe.
bx, by, bk = 0.62, ROW_BRAIN + 0.62, 0.55
brain(ax, bx, by, bk)
tip = brain_site(bx, by, bk)
ax.add_patch(Circle(tip, 0.12, facecolor="none", edgecolor="0.4", lw=0.8, zorder=5))
line(ax, [tip[0] + 0.1, SX], [tip[1] + 0.07, ROW_BRAIN + SH], z=6, **DOT)
line(ax, [tip[0] + 0.1, SX], [tip[1] - 0.07, ROW_BRAIN], z=6, **DOT)

# State spaces: different arrangements, same relations (the apples close, the banana far).
net_pts = [(0.05, 0.15), (0.3, 0.36), (0.75, 0.88)]
brain_pts = [(0.1, 0.86), (0.3, 0.62), (0.82, 0.12)]
state_space(ax, SX, ROW_NET, SW, SH, net_pts)
state_space(ax, SX, ROW_BRAIN, SW, SH, brain_pts)

# Similarity tables, compared directly.
table(ax, TX, ROW_NET + 0.15, net_pts)
table(ax, TX, ROW_BRAIN + 0.15, brain_pts)
for y in (ROW_NET + 0.6, ROW_BRAIN + 0.6):
    arrow(ax, (SX + SW + 0.05, y), (TX - 0.45, y))
arrow(ax, (TX + 0.45, ROW_BRAIN + 1.36), (TX + 0.45, ROW_NET + 0.08), arrowstyle="<|-|>")

finish(fig, ax, "rsaComparison", xlim=(-0.1, 5.25), ylim=(-0.1, 3.5))
