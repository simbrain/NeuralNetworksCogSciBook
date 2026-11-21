"""Attention as a weighted sum (linear combination) of value vectors.

Each earlier value vector is scaled by its attention weight for "it";
the scaled vectors are summed. Only "party" survives the scaling.
"""
from style import new_fig, save, cells, INK
import data

S = 0.3
FS = 8


OUTPUTS = ['attention_sum']


def main():
    T, d = data.TOKENS, data.D
    n = data.IT + 1                       # "it" reads only itself and earlier tokens
    w = data.IT_ROW
    fig, ax = new_fig(6.0, 4.6)

    gap = 0.12
    vx = 1.2
    sx = vx + d * S + 1.0
    for i in range(n):
        y = -(i + 1) * (S + gap)
        ax.text(0.0, y + S / 2, f"{w[i]:.2f}".lstrip("0"), ha="right", va="center", fontsize=FS)
        ax.text(0.25, y + S / 2, r"$\times$", ha="center", va="center", fontsize=FS + 1)
        ax.text(vx - 0.08, y + S / 2, T[i], ha="right", va="center", fontsize=FS)
        cells(ax, vx, y, data.VALUES[i], size=S)
        ax.text(vx + d * S + 0.5, y + S / 2, "=", ha="center", va="center", fontsize=FS + 2)
        cells(ax, sx, y, w[i] * data.VALUES[i], size=S)
        if i < n - 1:
            ax.text(sx + d * S + 0.25, y - gap / 2, "+", ha="center", va="center", fontsize=FS + 2)

    ybot = -(n + 1) * (S + gap) - 0.1
    ax.plot([sx, sx + d * S], [ybot + S + 0.12] * 2, color=INK, lw=0.9)
    cells(ax, sx, ybot, data.it_output(), size=S)
    ax.text(sx + d * S + 0.15, ybot + S / 2, "mix passed up the “it” stream",
            ha="left", va="center", fontsize=FS)
    ax.text(vx + d * S / 2, 0.05, "value vectors", ha="center", va="bottom", fontsize=FS)
    ax.text(sx + d * S / 2, 0.05, "scaled", ha="center", va="bottom", fontsize=FS)
    ax.text(-0.2, 0.05, "attention\nweights", ha="center", va="bottom", fontsize=FS)
    save(fig, "attention_sum")


if __name__ == "__main__":
    main()
