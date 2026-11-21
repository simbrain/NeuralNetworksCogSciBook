"""Generate images/encodingModel.{svg,pdf,png} (figure encodingModel in InternalRepresentations.tex).

Several stimuli (two apples, a banana, a kitten) are shown to a network (top) and to a brain (bottom). Each
stimulus produces a pattern in each system, drawn as a separate strip of shaded cells, one cell per unit, with the
stimulus at its left. The strips are separated by gaps so they read as individual states, not as a similarity
table. Model-to-brain encoding predicts the brain patterns from the network patterns (arrow).
"""
from matplotlib.patches import Circle
from figure_style import DOT, new_fig, finish, line, arrow, network, layer_box, strips
from line_art import apple, banana, kitten, brain, brain_site

C = 0.18   # cell size in the strips

# One pattern per stimulus. The two systems use different units and values, but similar stimuli produce similar
# patterns in both.
STIM = [(apple, dict()), (apple, dict(sx=1.08, sy=0.92, rot=0.12, stem=0.1)), (banana, dict(rot=0.55)),
        (kitten, dict())]
NET = [[0.8, 0.2, 0.6, 0.1, 0.5],
       [0.75, 0.25, 0.5, 0.15, 0.55],
       [0.5, 0.1, 0.9, 0.3, 0.2],
       [0.05, 0.9, 0.2, 0.8, 0.1]]
RECORDED = [[0.7, 0.3, 0.9, 0.2, 0.1, 0.6],
            [0.6, 0.35, 0.85, 0.25, 0.15, 0.65],
            [0.85, 0.1, 0.5, 0.15, 0.4, 0.3],
            [0.2, 0.8, 0.1, 0.9, 0.7, 0.1]]


def icon(ax, i, x, y, s=0.3):
    draw, kw = STIM[i]
    draw(ax, x, y, s=s * (0.85 if draw is banana else 1.0), lw=0.6, **kw)


def patterns(ax, x0, y0, rows):
    """One strip per stimulus, each labeled at left with the stimulus; returns the stack's height."""
    h, centers = strips(ax, x0, y0, rows, C)
    for r, y in enumerate(centers):
        icon(ax, r, x0 - 0.17, y)
    return h


fig, ax = new_fig((5.0, 3.6))

# The stimuli, shown to both systems.
for r in range(4):
    icon(ax, r, 0.2, 2.1 - 0.33 * r, s=0.45)
arrow(ax, (0.45, 2.2), (0.75, 2.55))
arrow(ax, (0.45, 1.2), (0.75, 0.85))

# Network, with its hidden layer boxed and linked to its patterns.
nx, ny = 1.25, 2.45
layers = [(ny, 4), (ny + 0.4, 3), (ny + 0.8, 2)]
xs = network(ax, nx, layers)
hy = layers[1][0]
_, hx1 = layer_box(ax, xs[1], hy, 0.12, 0.06)
PX = 2.5
net_y = 2.25
h = patterns(ax, PX + C / 2, net_y, NET)
line(ax, [hx1, PX - 0.35], [hy, net_y + h / 2], **DOT)
ax.text(PX + 3 * C, net_y + h + 0.08, "network layer", ha="center", va="bottom", fontsize=8)

# Brain, with the recorded region circled and linked to its patterns.
bx, by, bk = 1.2, 0.6, 0.45
brain(ax, bx, by, bk)
tip = brain_site(bx, by, bk)
ax.add_patch(Circle(tip, 0.1, facecolor="none", edgecolor="0.4", lw=0.8, zorder=5))
rec_y = 0.2
h = patterns(ax, PX, rec_y, RECORDED)
line(ax, [tip[0] + 0.1, PX - 0.35], [tip[1], rec_y + h / 2], z=6, **DOT)
ax.text(PX + 3 * C, rec_y - 0.06, "brain region", ha="center", va="top", fontsize=8)

# Model-to-brain encoding predicts the brain patterns from the network patterns.
xc, top, bot = PX + 3 * C, net_y - 0.08, rec_y + h + 0.08
arrow(ax, (xc, top), (xc, bot))
ax.text(xc + 0.1, (top + bot) / 2, "model \u2192 brain\n(encoding)", ha="left", va="center", fontsize=8)

finish(fig, ax, "encodingModel", xlim=(-0.1, 4.0), ylim=(-0.05, 3.55))
