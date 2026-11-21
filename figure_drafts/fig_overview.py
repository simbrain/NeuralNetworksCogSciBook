"""Redraw of TransformerOverview / TransformerOverview2 with a residual stream.

The embedding matrix feeds a vertical residual stream. Each transformer block
is a row of attention heads (with dots for the ones not shown) followed by one MLP. The heads share one read from
the stream and one write back; the MLP then does the same, as in the
residual-stream figures later in the chapter. The top of the stream feeds the softmax output.
Only the first time step is rendered; draw(2) gives the second.
"""
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from style import new_fig, save, arrow, line, dot, INK

FS_WORD, FS_NUM, FS_LABEL = 10, 7, 8

EMB = [[1, 2, 1, 2], [2, 1, 9, 8], [7, 3, 5, 8], [1, 2, 5, 6], [1, 1, 2, 0]]
GOOD_ROW = [2, 8, 2, 5]
N_ROWS = 11
CONTEXT = ["hello", "how", "are", "you", "?"]
OUT_WORDS = [["are", "hello", "how", "good"], ["thank", "you", ".", "?"]]

# Geometry (units are roughly 100 px of the original image).
TX, TY, CW, RH = 5.73, 0.39, 0.99, 0.414   # embedding table
SX = TX + 4 * CW - 0.25                         # residual stream x
HW, HH, HGAP, DGAP = 0.8, 0.6, 0.2, 0.55   # head size, spacing, and gap holding the dots
_r = SX - 0.5 - HW
HX = [_r - 2 * HW - HGAP - DGAP, _r - HW - HGAP, _r]               # head left edges
MX, MW, MH = HX[0], HX[-1] + HW - HX[0], 0.9                         # MLP box
GAP = 0.4                                   # stream-to-box spacing
SM_R = 4.45                                 # softmax box right edge
SEP = 0.4                                   # heads' write to MLP's read
BLOCK_H = 4 * GAP + HH + SEP + MH            # first read to last write
PAD = 0.25


def rr(ax, x, y, w, h, r, lw=0.9, fc="white", ec=INK, z=2, text=None, fs=7):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, fontsize=fs, ha="center", va="center", zorder=z + 1)


def block(ax, y0):
    """One transformer block on the stream, starting at y0.

    The heads share one read from the stream and one write back to it.
    The MLP then reads the updated stream and writes back above that."""
    rr(ax, MX - PAD, y0 - PAD, SX + PAD - (MX - PAD), BLOCK_H + 2 * PAD, 0.12, lw=0.7, fc="none", z=1)
    cxs = [x + HW / 2 for x in HX]
    # Attention heads: read, heads, write.
    yh, yw = y0 + GAP, y0 + 2 * GAP + HH
    dot(ax, SX, y0, r=0.05)
    line(ax, [SX, cxs[0]], [y0, y0])
    for x, cx in zip(HX, cxs):
        arrow(ax, (cx, y0), (cx, yh), ms=6)
        rr(ax, x, yh, HW, HH, 0.06, text="Head", fs=8)
        line(ax, [cx, cx], [yh + HH, yw])
    ax.text((HX[0] + HW + HX[1]) / 2, yh + HH / 2, "...", fontsize=9, ha="center", va="center")
    line(ax, [cxs[0], SX - 0.15], [yw, yw])
    arrow(ax, (SX - 0.15, yw), (SX, yw), ms=6)
    dot(ax, SX, yw, r=0.05)
    # MLP: read, MLP, write.
    mc = MX + MW / 2
    yr, ym = yw + SEP, yw + SEP + GAP
    ymw = ym + MH + GAP
    dot(ax, SX, yr, r=0.05)
    line(ax, [SX, mc], [yr, yr])
    arrow(ax, (mc, yr), (mc, ym), ms=6)
    rr(ax, MX, ym, MW, MH, 0.06, text="MLP", fs=9)
    line(ax, [mc, mc, SX - 0.15], [ym + MH, ymw, ymw])
    arrow(ax, (SX - 0.15, ymw), (SX, ymw), ms=6)
    dot(ax, SX, ymw, r=0.05)
    return ymw


def draw(step):
    fig, ax = new_fig(7.2, 12.2)

    # Context window.
    rr(ax, 0.5, 0.42, 3.52, 4.57, 0.0)
    words = CONTEXT + (["Good"] if step == 2 else [])
    for i, w in enumerate(words):
        ax.text(0.68, 4.7 - 0.4 * i, w, fontsize=FS_WORD, va="center")
    ax.text(2.26, 0.3, "Context Window", fontsize=FS_LABEL, style="italic", ha="center", va="top")
    arrow(ax, (4.02, 2.71), (TX - 0.05, 2.71), lw=1.4)

    # Embedding table.
    rows = EMB + ([GOOD_ROW] if step == 2 else [])
    rows = rows + [[0] * 4] * (N_ROWS - len(rows))
    for r, vals in enumerate(rows):
        y = TY + (N_ROWS - 1 - r) * RH
        for c, v in enumerate(vals):
            ax.add_patch(Rectangle(
                (TX + c * CW, y), CW, RH, fc="white", ec=INK, lw=0.9, zorder=2))
            ax.text(TX + c * CW + 0.15, y + RH / 2, str(v), fontsize=FS_NUM, va="center", zorder=3)
    ax.text(TX + 2 * CW, TY - 0.1, "Embedding", fontsize=FS_LABEL, style="italic", ha="center", va="top")

    # Residual stream with two blocks and a gap between them.
    top_table = TY + N_ROWS * RH
    y1 = top_table + 2.1
    y1_end = y1 + BLOCK_H
    y2 = y1_end + 1.5
    y_top = y2 + BLOCK_H + 0.6
    line(ax, [SX, SX], [top_table, y1_end + PAD], lw=1.4)
    line(ax, [SX, SX], [y1_end + PAD, y2 - PAD], lw=1.4, ls=(0, (1, 2)))
    line(ax, [SX, SX, SM_R + 0.2], [y2 - PAD, y_top, y_top], lw=1.4)
    arrow(ax, (SM_R + 0.25, y_top), (SM_R, y_top), lw=1.4)
    block(ax, y1)
    block(ax, y2)

    # Softmax output.
    sy = y_top - 2.37 + 0.45
    rr(ax, 0.2, sy, SM_R - 0.2, 2.37, 0.0)
    ax.text((0.2 + SM_R) / 2, sy + 2.37 + 0.12, "Softmax Output", fontsize=FS_LABEL, style="italic",
            ha="center", va="bottom")
    shade = {1: {"good": "0.6", "thank": "0.93"}, 2: {"thank": "0.6", ".": "0.93"}}[step]
    for r, row in enumerate(OUT_WORDS):
        for c, w in enumerate(row):
            x = 0.76 + 1.015 * c
            yw = sy + 2.09 - 1.2 * r
            ax.text(x, yw, w, fontsize=FS_WORD, ha="center", va="center")
            ax.add_patch(Circle((x, yw - 0.45), 0.23, fc=shade.get(w, "white"), ec=INK,
                                lw=0.9, zorder=2))

    save(fig, f"overview_{step}")


OUTPUTS = ["overview_1"]


def main():
    draw(1)  # draw(2) gives the next time step, with "Good" in the context


if __name__ == "__main__":
    main()
