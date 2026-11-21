"""Attention mixing drawn in the one-stream-per-token layout.

Each token's value vector sits in its own lane. The "it" lane takes a
weighted mix of the value vectors (line width = attention weight) and
adds it to its stream.
"""
from style import new_fig, save, cells, arrow, line, dot, INK
import data

L = 0.9
S = 0.15
FS = 8


OUTPUTS = ['attention_lanes']


def main():
    T, d = data.TOKENS, data.D
    n = data.IT + 1
    w = data.IT_ROW
    fig, ax = new_fig(6.0, 4.4)
    h = d * S
    xit = data.IT * L
    sig = (xit, h + 1.5)

    for j in range(n):
        x = j * L
        cells(ax, x - S / 2, 0, data.VALUES[j], size=S, vertical=True)
        ax.text(x, -0.12, T[j], ha="center", va="top", fontsize=FS + 1)
        ax.text(x, -0.42, f"{w[j]:.2f}".lstrip("0"), ha="center", va="top", fontsize=FS, color="0.35")
        arrow(ax, (x, h + 0.06), sig, lw=0.3 + 5 * w[j], ms=4 + 6 * w[j], shrink=6)
    ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(sig, 0.12, fc="white", ec=INK, lw=0.9, zorder=5))
    ax.text(*sig, r"$\Sigma$", ha="center", va="center", fontsize=FS, zorder=6)

    my = sig[1] + 0.35
    arrow(ax, (xit, sig[1] + 0.12), (xit, my), ms=6)
    cells(ax, xit - S / 2, my, data.it_output(), size=S, vertical=True)
    arrow(ax, (xit, my + h + 0.02), (xit, my + h + 0.4), ms=6)
    ax.text(xit + 0.2, my + h / 2, "mix added to\nthe “it” stream", ha="left", va="center", fontsize=FS)
    ax.text(-0.45, h / 2, "value\nvectors", ha="right", va="center", fontsize=FS)
    ax.text(-0.45, -0.5, "weights\nfor “it”", ha="right", va="center", fontsize=FS, color="0.35")
    save(fig, "attention_lanes")


if __name__ == "__main__":
    main()
