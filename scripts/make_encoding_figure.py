"""Generate images/encodingModel.{svg,pdf,png} (figure encodingModel in InternalRepresentations.tex).

Several stimuli (two apples, a banana, a kitten) are shown to a network (top) and to a brain (bottom). Each
stimulus produces a pattern in the network's hidden layer, drawn as a strip of shaded cells with the stimulus at its
left. A probe, a small network with one output node, combines each pattern into a single predicted value. The same
stimuli produce one recorded value each at a single site in the brain (a neuron or voxel). Encoding succeeds when
the predicted values match the recorded ones.
"""
from matplotlib.patches import Circle, Rectangle
from figure_style import DOT, INK, new_fig, finish, line, arrow, network, layer_box, strips, links, nodes, gray
from line_art import apple, banana, kitten, brain, brain_site

C = 0.18   # cell size in the strips

# One network pattern per stimulus, and one recorded value per stimulus at a single brain site. The predicted
# values are close to the recorded ones.
STIM = [(apple, dict()), (apple, dict(sx=1.08, sy=0.92, rot=0.12, stem=0.1)), (banana, dict(rot=0.55)),
        (kitten, dict())]
NET = [[0.8, 0.2, 0.6, 0.1, 0.5],
       [0.75, 0.25, 0.5, 0.15, 0.55],
       [0.5, 0.1, 0.9, 0.3, 0.2],
       [0.05, 0.9, 0.2, 0.8, 0.1]]
PREDICTED = [0.75, 0.7, 0.45, 0.15]
RECORDED = [0.8, 0.65, 0.5, 0.1]


def icon(ax, i, x, y, s=0.3):
    draw, kw = STIM[i]
    draw(ax, x, y, s=s * (0.85 if draw is banana else 1.0), lw=0.6, **kw)


def column(ax, x0, y0, vals, icons=False):
    """One cell per stimulus, stacked like the strips; returns the stack's height and each cell's center y."""
    h, centers = strips(ax, x0, y0, [[v] for v in vals], C)
    if icons:
        for r, y in enumerate(centers):
            icon(ax, r, x0 - 0.17, y)
    return h, centers


fig, ax = new_fig((5.6, 3.6))

# The stimuli, shown to both systems.
for r in range(4):
    icon(ax, r, 0.2, 2.1 - 0.33 * r, s=0.45)
arrow(ax, (0.45, 2.2), (0.75, 2.55))
arrow(ax, (0.45, 1.2), (1.35, 0.8))

# Network, with its hidden layer boxed and linked to its patterns.
nx, ny = 1.25, 2.45
layers = [(ny, 4), (ny + 0.4, 3), (ny + 0.8, 2)]
xs = network(ax, nx, layers)
hy = layers[1][0]
_, hx1 = layer_box(ax, xs[1], hy, 0.12, 0.06)
PX = 2.35
net_y = 2.25
h, centers = strips(ax, PX, net_y, NET, C)
for r, y in enumerate(centers):
    icon(ax, r, PX - 0.17, y)
line(ax, [hx1, PX - 0.35], [hy, net_y + h / 2], **DOT)
ax.text(PX + 2.5 * C, net_y + h + 0.08, "network layer", ha="center", va="bottom", fontsize=8)

# The probe: five input nodes, one per cell of a pattern, feeding one output node. Drawn sideways so that the
# patterns flow through it from left to right.
mid = net_y + h / 2
in_x, out_x, gap, rad = 3.55, 3.95, 0.16, 0.05
ys = [mid + gap * (2 - i) for i in range(5)]
for y in ys:
    line(ax, [in_x + rad, out_x - rad], [y, mid], color="0.7", lw=0.4, z=1)
for y in ys:
    ax.add_patch(Circle((in_x, y), rad, facecolor="white", edgecolor=INK, lw=0.7, zorder=3))
ax.add_patch(Circle((out_x, mid), rad, facecolor="white", edgecolor=INK, lw=0.7, zorder=3))
arrow(ax, (PX + 5 * C + 0.06, mid), (in_x - rad - 0.06, mid))
ax.text((in_x + out_x) / 2, ys[0] + 0.12, "probe", ha="center", va="bottom", fontsize=8)

# Predicted values, one per stimulus, aligned with the patterns.
QX = 4.3
column(ax, QX, net_y, PREDICTED)
arrow(ax, (out_x + rad + 0.04, mid), (QX - 0.06, mid))
ax.text(QX + C / 2, net_y + h + 0.08, "predicted", ha="center", va="bottom", fontsize=8)

# Brain, with the recorded site circled and linked to its values.
bx, by, bk = 2.2, 0.6, 0.45
brain(ax, bx, by, bk)
tip = brain_site(bx, by, bk)
ax.add_patch(Circle(tip, 0.06, facecolor="none", edgecolor="0.4", lw=0.8, zorder=5))
rec_y = 0.35
h2, _ = column(ax, QX, rec_y, RECORDED, icons=True)
line(ax, [tip[0] + 0.06, QX - 0.35], [tip[1], rec_y + h2 / 2], z=6, **DOT)
ax.text(QX + C / 2, rec_y - 0.06, "recorded", ha="center", va="top", fontsize=8)

# The predicted values are compared with the recorded ones.
xc, top, bot = QX + C / 2, net_y - 0.08, rec_y + h2 + 0.08
arrow(ax, (xc, bot), (xc, top), arrowstyle="<|-|>")
ax.text(xc + 0.12, (top + bot) / 2, "compare", ha="left", va="center", fontsize=8)

finish(fig, ax, "encodingModel", xlim=(-0.1, 5.0), ylim=(-0.05, 3.55))
