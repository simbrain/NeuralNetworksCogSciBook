"""Shared drawing style for the CNN chapter figures (make_filter_figures.py, make_convolution_figure.py).

Grayscale, light gray grid lines, normal-weight labels, rounded joins (no miter overshoot at corners).
Boxes are drawn in cabinet projection: one channel is half a cell deep, so a 3x3x3 filter reads as a cube.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

U = 0.25                     # size of one cell
DS = 0.5 * U                 # drawn depth of one channel
FONT = dict(fontsize=11, ha="center", va="top")
TOP_FACE, SIDE_FACE = "0.88", "0.65"
TOP_LINE, SIDE_LINE, GRID_LINE = "0.65", "0.5", "0.78"
EDGE = dict(edgecolor="0.15", lw=0.8)


def new_fig(size):
    fig, ax = plt.subplots(figsize=size)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def finish(fig, ax, outdir, name, xlim=None, ylim=None):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    for ext in ("svg", "pdf", "png"):
        fig.savefig(f"{outdir}/{name}.{ext}", dpi=300 if ext == "png" else None,
                    bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def poly(ax, pts, z=1, **kw):
    ax.add_patch(Polygon(pts, closed=True, zorder=z, joinstyle="round", capstyle="round", **kw))


def line(ax, xs, ys, z=2, **kw):
    ax.plot(xs, ys, zorder=z, solid_joinstyle="round", solid_capstyle="round", **kw)


def gray(v, vmax, darkest=0.3):
    """Fill for a value: 0 is white, vmax is the darkest gray."""
    return "white" if v == 0 else str(round(1 - (1 - darkest) * v / vmax, 2))


def box(ax, x, y, rows, cols, chans=1, ds=DS, rf=None, kernel=False, zb=0, fills=None, numbers=None):
    """Oblique box with its front face's bottom-left corner at (x, y); depth chans * ds, up and to the right.

    rf = (r0, c0, size): shade a size x size receptive field through the full depth, (r0, c0) its top-left
        cell counted from the top-left of the front face.
    kernel: darken the front slice to mark it as one kernel.
    zb: added to every zorder, so later boxes can sit fully in front of earlier ones.
    fills: rows x cols array of front-face cell colors. numbers: rows x cols array of values to print.
    Returns P(r, c), the front-face point at row line r and column line c, counted from the top-left.
    """
    P = lambda r, c: (x + c * U, y + (rows - r) * U)
    w, h, d = cols * U, rows * U, chans * ds
    front = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    top = [(x, y+h), (x+w, y+h), (x+w+d, y+h+d), (x+d, y+h+d)]
    side = [(x+w, y), (x+w+d, y+d), (x+w+d, y+h+d), (x+w, y+h)]
    poly(ax, front, z=1+zb, facecolor="white", edgecolor="none")
    if d > 0:
        poly(ax, top, z=1+zb, facecolor=TOP_FACE, edgecolor="none")
        poly(ax, side, z=1+zb, facecolor=SIDE_FACE, edgecolor="none")
    if fills is not None:
        for r in range(rows):
            for c in range(cols):
                if fills[r][c] != "white":
                    poly(ax, [P(r, c), P(r, c+1), P(r+1, c+1), P(r+1, c)], z=1.5+zb,
                         facecolor=fills[r][c], edgecolor="none")
    if rf:
        r0, c0, s = rf
        poly(ax, [P(r0, c0), P(r0, c0+s), P(r0+s, c0+s), P(r0+s, c0)], z=1.5+zb, facecolor="0.6", edgecolor="none")
        if r0 == 0 and d > 0:
            fx = P(0, c0)[0]
            poly(ax, [(fx, y+h), (fx+s*U, y+h), (fx+s*U+d, y+h+d), (fx+d, y+h+d)], z=1.5+zb, facecolor="0.55",
                 edgecolor="none")
        if c0 + s == cols and d > 0:
            fy = P(r0+s, 0)[1]
            poly(ax, [(x+w, fy), (x+w+d, fy+d), (x+w+d, fy+s*U+d), (x+w, fy+s*U)], z=1.5+zb, facecolor="0.42",
                 edgecolor="none")
    if kernel and d > 0:
        poly(ax, [(x, y+h), (x+w, y+h), (x+w+ds, y+h+ds), (x+ds, y+h+ds)], z=1.5+zb, facecolor="0.4", edgecolor="none")
        poly(ax, [(x+w, y), (x+w+ds, y+ds), (x+w+ds, y+h+ds), (x+w, y+h)], z=1.5+zb, facecolor="0.3", edgecolor="none")
    if d > 0:
        for k in range(1, chans):
            o = k * ds
            line(ax, [x+o, x+w+o], [y+h+o, y+h+o], z=2+zb, color=TOP_LINE, lw=0.4)
            line(ax, [x+w+o, x+w+o], [y+o, y+h+o], z=2+zb, color=SIDE_LINE, lw=0.4)
        for i in range(1, cols):
            line(ax, [x+i*U, x+i*U+d], [y+h, y+h+d], z=2+zb, color=TOP_LINE, lw=0.4)
        for j in range(1, rows):
            line(ax, [x+w, x+w+d], [y+j*U, y+j*U+d], z=2+zb, color=SIDE_LINE, lw=0.4)
    for i in range(1, cols):
        line(ax, [x+i*U]*2, [y, y+h], z=2+zb, color=GRID_LINE, lw=0.5)
    for j in range(1, rows):
        line(ax, [x, x+w], [y+j*U]*2, z=2+zb, color=GRID_LINE, lw=0.5)
    if numbers is not None:
        for r in range(rows):
            for c in range(cols):
                fill = fills[r][c] if fills is not None else "white"
                dark = fill != "white" and float(fill) < 0.55
                cx, cy = P(r + 0.5, c + 0.5)
                ax.text(cx, cy, str(numbers[r][c]), ha="center", va="center", fontsize=7.5,
                        color="white" if dark else "0.15", zorder=4+zb)
    outline = [top, side, front] if d > 0 else [front]
    for p in outline:
        poly(ax, p, z=3+zb, fill=False, **EDGE)
    return P


def outline_cells(ax, P, r0, c0, nr, nc, z=5):
    """Heavier outline around a block of front-face cells."""
    poly(ax, [P(r0, c0), P(r0, c0+nc), P(r0+nr, c0+nc), P(r0+nr, c0)], z=z, fill=False, edgecolor="0.1", lw=1.5)


def sign(ax, x, y, t):
    ax.text(x, y, t, ha="center", va="center", fontsize=15, color="0.15")


def label(ax, x, y, t, **kw):
    ax.text(x, y, t, **{**FONT, **kw})


def pointer(ax, text, xy, xytext):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=FONT["fontsize"], ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color="0.15", lw=0.7))


# Shared example data: the 9x9 smiley face used in the chapter's convolution and pooling figures.
SMILEY = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]
BACKSLASH = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]      # -45 degree edge detector
SLASH = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]          # +45 degree edge detector


def convolve(image, filt):
    """Valid convolution (no padding, stride 1) of nested lists; returns nested lists of ints."""
    n, k = len(image), len(filt)
    return [[sum(image[i + a][j + b] * filt[a][b] for a in range(k) for b in range(k))
             for j in range(n - k + 1)] for i in range(n - k + 1)]
