"""Generate images/llmEncodingModel.{svg,pdf,png} (figure llmEncodingModel in LLMsCogSci.tex).

Model-to-brain encoding with an LLM. Left: fragments of a story are read by an LLM and by a person. Each
fragment produces a pattern in one LLM layer, drawn as a strip of shaded cells. A probe, a small network with one
output node, combines each pattern into a single predicted value for one site in the brain's language network,
which is compared with the value recorded there. Same layout as make_encoding_figure.py.
Right: the published map of prediction scores for GPT2-xl from Schrimpf et al. (2021).

Reads images/brainPredictionsLLM.png.
"""
from matplotlib.patches import Circle
from figure_style import IMAGES, DOT, INK, new_fig, finish, line, arrow, network, layer_box, strips, place_image
from line_art import brain, brain_site

C = 0.18   # cell size in the strips

STORY = ["\u201cThe old fisherman\u201d", "\u201ccast his net\u201d", "\u201cand pulled up\u201d", "\u201ca golden fish\u201d"]
LLM = [[0.8, 0.2, 0.6, 0.1, 0.5],
       [0.3, 0.7, 0.2, 0.6, 0.4],
       [0.5, 0.1, 0.9, 0.3, 0.2],
       [0.75, 0.25, 0.5, 0.15, 0.55]]
PREDICTED = [0.7, 0.3, 0.55, 0.65]
RECORDED = [0.75, 0.25, 0.6, 0.6]


def numbered(ax, x0, y0, rows):
    """One strip per fragment, each labeled at left with the fragment's number; returns height and centers."""
    h, centers = strips(ax, x0, y0, rows, C)
    for r, y in enumerate(centers):
        ax.text(x0 - 0.08, y, str(r + 1), ha="right", va="center", fontsize=8)
    return h, centers


fig, ax = new_fig((8.6, 3.6))

# The story, read by both systems.
for r, frag in enumerate(STORY):
    ax.text(0.0, 2.1 - 0.3 * r, f"{r + 1}  ", ha="left", va="center", fontsize=8)
    ax.text(0.14, 2.1 - 0.3 * r, frag, ha="left", va="center", fontsize=8, style="italic")
arrow(ax, (0.75, 2.3), (1.4, 2.55))
arrow(ax, (0.75, 1.05), (1.4, 0.85))

# LLM, with one layer boxed and linked to its patterns.
nx, ny = 1.85, 2.45
layers = [(ny, 4), (ny + 0.4, 5), (ny + 0.8, 4)]
xs = network(ax, nx, layers)
hy = layers[1][0]
_, hx1 = layer_box(ax, xs[1], hy, 0.12, 0.06)
ax.text(nx, layers[-1][0] + 0.15, "LLM", ha="center", va="bottom", fontsize=8)
PX = 2.95
net_y = 2.25
h, _ = numbered(ax, PX, net_y, LLM)
line(ax, [hx1, PX - 0.2], [hy, net_y + h / 2], **DOT)
ax.text(PX + 2.5 * C, net_y + h + 0.08, "LLM layer", ha="center", va="bottom", fontsize=8)

# The probe: five input nodes, one per cell of a pattern, feeding one output node.
mid = net_y + h / 2
in_x, out_x, gap, rad = PX + 1.2, PX + 1.6, 0.16, 0.05
ys = [mid + gap * (2 - i) for i in range(5)]
for y in ys:
    line(ax, [in_x + rad, out_x - rad], [y, mid], color="0.7", lw=0.4, z=1)
for y in ys:
    ax.add_patch(Circle((in_x, y), rad, facecolor="white", edgecolor=INK, lw=0.7, zorder=3))
ax.add_patch(Circle((out_x, mid), rad, facecolor="white", edgecolor=INK, lw=0.7, zorder=3))
arrow(ax, (PX + 5 * C + 0.06, mid), (in_x - rad - 0.06, mid))
ax.text((in_x + out_x) / 2, ys[0] + 0.12, "probe", ha="center", va="bottom", fontsize=8)

# Predicted values for one brain site, one per fragment.
QX = out_x + 0.35
strips(ax, QX, net_y, [[v] for v in PREDICTED], C)
arrow(ax, (out_x + rad + 0.04, mid), (QX - 0.06, mid))
ax.text(QX + C / 2, net_y + h + 0.08, "predicted", ha="center", va="bottom", fontsize=8)

# Brain, with one site of the language network circled and linked to its recorded values.
bx, by, bk = 1.8, 0.6, 0.45
brain(ax, bx, by, bk)
tip = brain_site(bx, by, bk)
ax.add_patch(Circle(tip, 0.06, facecolor="none", edgecolor="0.4", lw=0.8, zorder=5))
rec_y = 0.35
h2, _ = numbered(ax, QX, rec_y, [[v] for v in RECORDED])
line(ax, [tip[0] + 0.06, QX - 0.2], [tip[1], rec_y + h2 / 2], z=6, **DOT)
ax.text(QX + C / 2, rec_y - 0.06, "recorded", ha="center", va="top", fontsize=8)

# The predicted values are compared with the recorded ones.
xc, top, bot = QX + C / 2, net_y - 0.08, rec_y + h2 + 0.08
arrow(ax, (xc, bot), (xc, top), arrowstyle="<|-|>")
ax.text(xc + 0.12, (top + bot) / 2, "compare", ha="left", va="center", fontsize=8)

# Right: prediction scores across the language network, from Schrimpf et al. (2021).
MW = 2.6
MX, MY = QX + 1.15, 0.9
place_image(ax, IMAGES / "brainPredictionsLLM.png", MX, MY, MW)

finish(fig, ax, "llmEncodingModel", xlim=(-0.05, MX + MW + 0.02), ylim=(-0.05, 3.55))
