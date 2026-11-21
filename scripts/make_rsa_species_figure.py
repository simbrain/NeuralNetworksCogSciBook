"""Generate images/rsaHumanMonkey.{svg,pdf,png} (figure rsaHumanMonkey in InternalRepresentations.tex).

Schematic of Kriegeskorte et al. (2008): similarity tables for human IT and
monkey IT, for images of faces, bodies, natural objects, and artificial objects. Both show the same block
structure: animate images are similar to each other, inanimate images are similar to each other, and faces
form the tightest cluster. Values are made up to show the pattern, not taken from the paper.
"""
import numpy as np
from matplotlib.patches import Rectangle
from figure_style import INK, new_fig, finish, line, gray

GROUPS = ["faces", "bodies", "natural", "artificial"]
N, C = 4, 0.1                      # images per group, cell size
ANIMATE = [True, True, False, False]
WITHIN = [0.85, 0.6, 0.45, 0.45]   # similarity within each group


def similarity(seed):
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(4), N)
    S = np.full((4 * N, 4 * N), 0.12)
    for i in range(4 * N):
        for j in range(4 * N):
            if g[i] == g[j]:
                S[i, j] = WITHIN[g[i]]
            elif ANIMATE[g[i]] == ANIMATE[g[j]]:
                S[i, j] = 0.35
    noise = rng.normal(0, 0.06, S.shape)
    S = np.clip(S + (noise + noise.T) / 2, 0, 1)
    np.fill_diagonal(S, 1.0)
    return S


def table(ax, x0, y0, S, title):
    n = len(S)
    for r in range(n):
        for c in range(n):
            ax.add_patch(Rectangle((x0 + c * C, y0 + (n - 1 - r) * C), C, C, facecolor=gray(S[r, c], 1.0, 0.15),
                                   edgecolor="none", zorder=2))
    for k in range(1, 4):
        lw = 0.8 if k == 2 else 0.4
        line(ax, [x0 + k * N * C] * 2, [y0, y0 + n * C], color="0.5", lw=lw, z=3)
        line(ax, [x0, x0 + n * C], [y0 + (n - k * N) * C] * 2, color="0.5", lw=lw, z=3)
    ax.add_patch(Rectangle((x0, y0), n * C, n * C, facecolor="none", edgecolor=INK, lw=0.8, zorder=4))
    ax.text(x0 + n * C / 2, y0 + n * C + 0.1, title, ha="center", va="bottom", fontsize=9)


fig, ax = new_fig((5.0, 2.3))
size = 4 * N * C
table(ax, 0.0, 0.0, similarity(1), "Human IT (fMRI)")
table(ax, size + 0.45, 0.0, similarity(2), "Monkey IT (neurons)")

# Group labels and animate/inanimate brackets, on the left of the first table.
for k, name in enumerate(GROUPS):
    yc = size - (k + 0.5) * N * C
    ax.text(-0.08, yc, name, ha="right", va="center", fontsize=8)
for k0, name in ((0, "animate"), (2, "inanimate")):
    top, bot = size - k0 * N * C - 0.03, size - (k0 + 2) * N * C + 0.03
    bx = -0.78
    line(ax, [bx + 0.05, bx, bx, bx + 0.05], [top, top, bot, bot], color=INK, lw=0.7)
    ax.text(bx - 0.06, (top + bot) / 2, name, ha="right", va="center", fontsize=8)

finish(fig, ax, "rsaHumanMonkey", xlim=(-1.6, 2 * size + 0.5), ylim=(-0.05, size + 0.3))
