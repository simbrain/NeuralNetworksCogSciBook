"""One residual stream per token (after Beckmann and Queloz 2025, fig. 4b).

Each token gets its own vertical stream. Attention reads from the current
stream and earlier streams; the MLP reads only from its own stream. Both
write back into the stream. At the top, each stream predicts the next token.

Two variants: lanes_full draws every attention read; lanes_focus draws only
the reads into the "it" stream, with line width proportional to attention.
"""
from style import new_fig, save, rbox, arrow, line, dot, INK, MID
import data

L = 1.3                   # lane spacing
BW, BH = 0.5, 0.3         # attention / MLP box size
FS = 8
TOK = data.TOKENS[:data.IT + 1]
PRED = data.TOKENS[1:data.IT + 2]


def sublayer(ax, x, y_read, y_box, y_write, label):
    """Box to the left of the stream at x: read below, write back above."""
    bx = x - 0.15 - BW
    cx = bx + BW / 2
    rbox(ax, bx, y_box, BW, BH, label, fs=FS - 1)
    dot(ax, x, y_read)
    line(ax, [x, cx, cx], [y_read, y_read, y_box])
    line(ax, [cx, cx], [y_box + BH, y_write])
    arrow(ax, (cx, y_write), (x, y_write), ms=6)
    dot(ax, x, y_write)
    return bx, cx


def draw(variant):
    fig, ax = new_fig(7.5, 4.6)
    n = len(TOK)
    y_tap, y_attn, y_attn_w = 0.62, 1.0, 1.5
    y_mlp_r, y_mlp, y_mlp_w = 1.7, 1.9, 2.4
    y_un = 3.0
    for i, t in enumerate(TOK):
        x = i * L
        ax.text(x, 0.08, t, ha="center", va="top", fontsize=FS + 1)
        rbox(ax, x - 0.42, 0.18, 0.84, 0.27, "embed", fs=FS - 1)
        line(ax, [x, x], [0.45, 2.6])
        line(ax, [x, x], [2.6, y_un], ls=(0, (1, 2)))
        bx, cx = sublayer(ax, x, y_tap, y_attn, y_attn_w, "attn")
        sublayer(ax, x, y_mlp_r, y_mlp, y_mlp_w, "MLP")
        rbox(ax, x - 0.42, y_un, 0.84, 0.27, "unembed", fs=FS - 1)
        ax.text(x, y_un + 0.4, PRED[i], ha="center", va="bottom", fontsize=FS + 1, style="italic")

        # Reads from earlier streams into this stream's attention box.
        for j in range(i):
            xj = j * L
            if variant == "full":
                arrow(ax, (xj, y_tap), (bx + 0.08, y_attn), lw=0.5, color=MID, ms=4, rad=0.0, z=1)
            elif variant == "focus" and i == data.IT:
                wgt = data.IT_ROW[j]
                arrow(ax, (xj, y_tap), (bx + 0.08, y_attn), lw=0.3 + 5 * wgt, color=INK, ms=4 + 6 * wgt,
                      rad=0.0, z=1)

    # "k times" brace.
    bxl = -0.9
    line(ax, [bxl, bxl - 0.08, bxl - 0.08, bxl], [y_tap - 0.1, y_tap - 0.1, y_mlp_w + 0.1, y_mlp_w + 0.1])
    ax.text(bxl - 0.15, (y_tap + y_mlp_w) / 2, "$k$ blocks", ha="right", va="center", fontsize=FS)
    save(fig, f"lanes_{variant}")


OUTPUTS = ['lanes_full', 'lanes_focus']


def main():
    draw("full")
    draw("focus")


if __name__ == "__main__":
    main()
