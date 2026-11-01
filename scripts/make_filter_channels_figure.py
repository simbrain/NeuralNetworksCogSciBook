"""Generate images/filterChannels.{svg,pdf,png} (figure filterChannels in ConvolutionalNetworks.tex).

Redraw of filterDepth.png (Soraya Boza) with light grid lines.
Left: 8x8 input with 3 channels, 3x3x3 filter, 6x6 output.
Right: 2x2 input with 16 channels, 1x1x16 filter, 2x2 output.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

U = 0.25                       # size of one cell
GRID = dict(color="0.75", lw=0.5, zorder=2)
EDGE = dict(edgecolor="black", lw=0.9)
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.set_aspect("equal"); ax.axis("off")

def box(x, y, rows, cols, chans, dslice, show_chan_lines=True):
    """Oblique box: front face rows x cols cells, depth = chans * dslice (drawn up-right).

    Faces are drawn first (zorder 1), grid lines next (zorder 2), and outlines last (zorder 3),
    so grid lines stop at the black edges instead of crossing them.
    """
    w, h = cols * U, rows * U
    dx = dy = chans * dslice
    side = [(x+w, y), (x+w+dx, y+dy), (x+w+dx, y+h+dy), (x+w, y+h)]
    top = [(x, y+h), (x+w, y+h), (x+w+dx, y+h+dy), (x+dx, y+h+dy)]
    front = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    ax.add_patch(Polygon(side, closed=True, facecolor="0.55", edgecolor="none", zorder=1))
    ax.add_patch(Polygon(top, closed=True, facecolor="0.85", edgecolor="none", zorder=1))
    ax.add_patch(Polygon(front, closed=True, facecolor="white", edgecolor="none", zorder=1))
    top_line = dict(color="0.6", lw=0.4, zorder=2)
    side_line = dict(color="0.4", lw=0.4, zorder=2)
    if dx > 0:
        if show_chan_lines:
            for k in range(1, chans):
                o = k * dslice
                ax.plot([x+o, x+w+o], [y+h+o, y+h+o], **top_line)   # channel lines on top
                ax.plot([x+w+o, x+w+o], [y+o, y+h+o], **side_line)  # channel lines on side
        for i in range(1, cols):                                     # column lines on top
            ax.plot([x+i*U, x+i*U+dx], [y+h, y+h+dy], **top_line)
        for j in range(1, rows):                                     # row lines on side
            ax.plot([x+w, x+w+dx], [y+j*U, y+j*U+dy], **side_line)
    for i in range(1, cols):
        ax.plot([x+i*U]*2, [y, y+h], **GRID)
    for j in range(1, rows):
        ax.plot([x, x+w], [y+j*U]*2, **GRID)
    for poly in ([side, top] if dx > 0 else []) + [front]:
        ax.add_patch(Polygon(poly, closed=True, fill=False, zorder=3, **EDGE))

def square(x, y, n):
    box(x, y, n, n, 1, 0, show_chan_lines=False)

def receptive_field(x, y, r0, c0, size, chans, dslice):
    """Dashed column through the full depth of an input box, starting at cell (r0, c0) from bottom-left."""
    fx, fy = x + c0*U, y + r0*U
    s = size * U
    d = chans * dslice
    kw = dict(color="0.35", lw=0.9, ls=(0, (3, 2)), zorder=4)
    for (ax0, ay0) in [(fx, fy), (fx+d, fy+d)]:
        ax.plot([ax0, ax0+s, ax0+s, ax0, ax0], [ay0, ay0, ay0+s, ay0+s, ay0], **kw)
    for (px, py) in [(fx, fy), (fx, fy+s), (fx+s, fy+s), (fx+s, fy)]:
        ax.plot([px, px+d], [py, py+d], **kw)

def sign(x, y, t):
    ax.text(x, y, t, ha="center", va="center", fontsize=13)

# Left example
ds_left = 0.06
box(0.0, 0.0, 8, 8, 3, ds_left)
receptive_field(0.0, 0.0, 0, 5, 3, 3, ds_left)
sign(2.6, 1.0, "x")
box(3.0, 0.6, 3, 3, 3, ds_left)
sign(4.25, 1.0, "=")
square(4.7, 0.25, 6)

# Right example
ds_right = 0.11
box(8.0, 0.0, 2, 2, 16, ds_right)
receptive_field(8.0, 0.0, 0, 0, 1, 16, ds_right)
sign(10.6, 1.0, "x")
box(10.95, 0.35, 1, 1, 16, ds_right)
sign(13.2, 1.0, "=")
square(13.7, 0.75, 2)

ax.set_xlim(-0.1, 14.3); ax.set_ylim(-0.1, 2.5)
for ext in ("svg", "pdf", "png"):
    fig.savefig(f"images/filterChannels.{ext}", dpi=300 if ext == "png" else None,
                bbox_inches="tight", pad_inches=0.03)
