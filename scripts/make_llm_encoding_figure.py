"""Generate images/llmEncodingModel.{svg,pdf,png} (figure llmEncodingModel in LLMsCogSci.tex).

Model-to-brain encoding with an LLM. Left: fragments of a story are read by an LLM and by a person. Each
fragment produces a pattern in one LLM layer and in a region of the brain's language network, drawn as a strip of
shaded cells. Model-to-brain encoding predicts the brain patterns from the LLM patterns (arrow). Same layout as
make_encoding_figure.py.
Right: the published map of prediction scores for GPT2-xl from Schrimpf et al. (2021).

Reads images/brainPredictionsLLM.png.
"""
from matplotlib.patches import Circle
from figure_style import IMAGES, DOT, new_fig, finish, line, arrow, network, layer_box, strips, place_image
from line_art import brain, brain_site

C = 0.18   # cell size in the strips

STORY = ["\u201cThe old fisherman\u201d", "\u201ccast his net\u201d", "\u201cand pulled up\u201d", "\u201ca golden fish\u201d"]
LLM = [[0.8, 0.2, 0.6, 0.1, 0.5],
       [0.3, 0.7, 0.2, 0.6, 0.4],
       [0.5, 0.1, 0.9, 0.3, 0.2],
       [0.75, 0.25, 0.5, 0.15, 0.55]]
RECORDED = [[0.7, 0.3, 0.9, 0.2, 0.1, 0.6],
            [0.2, 0.8, 0.3, 0.6, 0.7, 0.1],
            [0.85, 0.1, 0.5, 0.15, 0.4, 0.3],
            [0.6, 0.35, 0.85, 0.25, 0.15, 0.65]]


def patterns(ax, x0, y0, rows):
    """One strip per fragment, each labeled at left with the fragment's number; returns the stack's height."""
    h, centers = strips(ax, x0, y0, rows, C)
    for r, y in enumerate(centers):
        ax.text(x0 - 0.08, y, str(r + 1), ha="right", va="center", fontsize=8)
    return h


fig, ax = new_fig((7.2, 3.6))

# The story, read by both systems.
for r, frag in enumerate(STORY):
    ax.text(0.0, 2.1 - 0.3 * r, f"{r + 1}  ", ha="left", va="center", fontsize=8)
    ax.text(0.14, 2.1 - 0.3 * r, frag, ha="left", va="center", fontsize=8, style="italic")
arrow(ax, (0.75, 2.3), (1.4, 2.55))
arrow(ax, (0.75, 1.05), (1.4, 0.85))

# LLM, with one layer boxed and linked to its patterns.
nx, ny = 1.85, 2.45
layers = [(ny, 4), (ny + 0.4, 3), (ny + 0.8, 4)]
xs = network(ax, nx, layers)
hy = layers[1][0]
_, hx1 = layer_box(ax, xs[1], hy, 0.12, 0.06)
ax.text(nx, layers[-1][0] + 0.15, "LLM", ha="center", va="bottom", fontsize=8)
PX = 2.9
net_y = 2.25
h = patterns(ax, PX + C / 2, net_y, LLM)
line(ax, [hx1, PX - 0.12], [hy, net_y + h / 2], **DOT)
ax.text(PX + 3 * C, net_y + h + 0.08, "LLM layer", ha="center", va="bottom", fontsize=8)

# Brain, with a region of the language network circled and linked to its patterns.
bx, by, bk = 1.8, 0.6, 0.45
brain(ax, bx, by, bk)
tip = brain_site(bx, by, bk)
ax.add_patch(Circle(tip, 0.1, facecolor="none", edgecolor="0.4", lw=0.8, zorder=5))
rec_y = 0.2
h = patterns(ax, PX, rec_y, RECORDED)
line(ax, [tip[0] + 0.1, PX - 0.12], [tip[1], rec_y + h / 2], z=6, **DOT)
ax.text(PX + 3 * C, rec_y - 0.06, "brain region", ha="center", va="top", fontsize=8)

# Model-to-brain encoding predicts the brain patterns from the LLM patterns.
xc, top, bot = PX + 3 * C, net_y - 0.08, rec_y + h + 0.08
arrow(ax, (xc, top), (xc, bot))
ax.text(xc + 0.1, (top + bot) / 2, "model → brain\n(encoding)", ha="left", va="center", fontsize=8)

# Right: prediction scores across the language network, from Schrimpf et al. (2021).
MW = 2.6
MX, MY = 4.75, 0.9
place_image(ax, IMAGES / "brainPredictionsLLM.png", MX, MY, MW)

finish(fig, ax, "llmEncodingModel", xlim=(-0.05, MX + MW + 0.02), ylim=(-0.05, 3.55))
