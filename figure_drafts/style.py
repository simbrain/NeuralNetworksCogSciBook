"""Shared drawing helpers for draft figures. Grayscale, thin lines, minimal labels."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
INK, MID, GRID = "0.15", "0.5", "0.78"
plt.rcParams.update({"font.size": 10, "svg.fonttype": "none"})


def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name, pad=0.3):
    os.makedirs(OUT, exist_ok=True)
    for ax in fig.axes:
        ax.autoscale_view()
        (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim(x0 - pad, x1 + pad)
        ax.set_ylim(y0 - pad, y1 + pad)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(f"{OUT}/{name}.{ext}", dpi=200 if ext == "png" else None,
                    bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def gray(v, darkest=0.2):
    """0 -> white, 1 -> darkest gray."""
    v = max(0.0, min(1.0, v))
    return str(round(1 - (1 - darkest) * v, 3))


def rbox(ax, x, y, w, h, text=None, fc="white", ec=INK, lw=0.9, fs=9, z=2, ls="-", r=0.06, **tkw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=z + 1, **tkw)


def arrow(ax, p, q, lw=0.9, color=INK, z=3, ms=8, rad=0.0, style="-|>", shrink=0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                                 zorder=z, shrinkA=shrink, shrinkB=shrink,
                                 connectionstyle=f"arc3,rad={rad}", joinstyle="round", capstyle="round"))


def line(ax, xs, ys, lw=0.9, color=INK, z=2, **kw):
    ax.plot(xs, ys, lw=lw, color=color, zorder=z, solid_capstyle="round", solid_joinstyle="round", **kw)


def dot(ax, x, y, r=0.035, color=INK, z=4):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=z))


def cells(ax, x, y, vals, size=0.2, vertical=False, ec=MID, lw=0.6, z=2, numbers=False, fs=6, fmt="{:.2f}"):
    """Draw a vector as a strip of shaded cells. (x, y) is the bottom-left corner.
    Horizontal strips run left to right; vertical strips run top to bottom."""
    n = len(vals)
    for i, v in enumerate(vals):
        cx, cy = (x, y + (n - 1 - i) * size) if vertical else (x + i * size, y)
        ax.add_patch(Rectangle((cx, cy), size, size, fc=gray(v), ec=ec, lw=lw, zorder=z))
        if numbers and v != 0:
            ax.text(cx + size / 2, cy + size / 2, fmt.format(v).lstrip("0") if v < 1 else "1",
                    ha="center", va="center", fontsize=fs, zorder=z + 1,
                    color="white" if v > 0.55 else INK)
    w, h = (size, n * size) if vertical else (n * size, size)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=INK, lw=0.9, zorder=z + 1))
