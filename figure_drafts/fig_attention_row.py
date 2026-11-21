"""Attention as row processing.

Top: the causal attention matrix for one head (row = the token doing the reading).
Bottom: the "it" row times the stack of value vectors gives a weighted mix,
dominated by the "party" value vector.
"""
from style import new_fig, save, cells, gray, arrow, INK, GRID
from matplotlib.patches import Rectangle
import data

S = 0.35          # cell size
FS = 8


OUTPUTS = ['attention_row']


def main():
    A = data.attention_matrix()
    T, n, d = data.TOKENS, len(data.TOKENS), data.D
    fig, ax = new_fig(7.2, 7.4)

    # Attention matrix, top-left corner at (0, top).
    top = 0.0
    for r in range(n):
        for c in range(n):
            y = top - (r + 1) * S
            fc = gray(A[r, c] / 0.75) if c <= r else "white"
            ax.add_patch(Rectangle((c * S, y), S, S, fc=fc, ec=GRID, lw=0.5, zorder=1))
        ax.text(-0.08, top - (r + 0.5) * S, T[r], ha="right", va="center", fontsize=FS)
    for c in range(n):
        ax.text((c + 0.5) * S, top + 0.06, T[c], ha="left", va="bottom", fontsize=FS, rotation=60,
                rotation_mode="anchor")
    ax.add_patch(Rectangle((0, top - n * S), n * S, n * S, fill=False, ec=INK, lw=0.9, zorder=3))
    ax.add_patch(Rectangle((0, top - (data.IT + 1) * S), n * S, S, fill=False, ec=INK, lw=2.0, zorder=4))

    # Equation row: (it row) x (value stack) = (mix).
    vtop = top - n * S - 0.6
    vbot = vtop - n * S
    ymid = (vtop + vbot) / 2
    ry = ymid - S / 2
    cells(ax, 0, ry, data.IT_ROW, size=S, numbers=True)
    for c in range(n):
        ax.text((c + 0.5) * S, ry + S + 0.06, T[c], ha="left", va="bottom", fontsize=FS - 1,
                rotation=60, rotation_mode="anchor", color="0.35")
    arrow(ax, (n * S / 2, top - n * S - 0.05), (n * S / 2, ry + S + 0.55), lw=0.9)

    ax.text(n * S + 0.3, ymid, r"$\times$", ha="center", va="center", fontsize=12)
    vx = n * S + 1.3
    for r in range(n):
        cells(ax, vx, vtop - (r + 1) * S, data.VALUES[r], size=S)
        ax.text(vx - 0.08, vtop - (r + 0.5) * S, T[r], ha="right", va="center", fontsize=FS)
    ax.text(vx + d * S + 0.3, ymid, "=", ha="center", va="center", fontsize=12)
    ox = vx + d * S + 0.6
    cells(ax, ox, ry, data.it_output(), size=S)

    ax.text(n * S / 2, ry - 0.15, "attention weights for “it”", ha="center", va="top", fontsize=FS)
    ax.text(vx + d * S / 2, vbot - 0.15, "value vectors", ha="center", va="top", fontsize=FS)
    ax.text(ox + d * S / 2, ry - 0.15, "mix passed up\nthe “it” stream", ha="center", va="top", fontsize=FS)

    save(fig, "attention_row")


if __name__ == "__main__":
    main()
