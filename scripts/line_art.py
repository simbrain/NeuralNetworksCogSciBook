"""Line-art apples, bananas, kittens, a brain, and an electrode, shared by the representations and LLM chapter figures.

Each function draws one object centered at (x, y), about 0.5 * s tall, with keyword options that vary its shape.
"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, PathPatch, Polygon
from matplotlib.path import Path
from figure_style import INK, line

LW = 0.9


def _place(x, y, k, rot, pts):
    c, s = np.cos(rot), np.sin(rot)
    return [(x + k * (c * px - s * py), y + k * (s * px + c * py)) for px, py in pts]


def apple(ax, x, y, s=1.0, lw=LW, sx=1.0, sy=1.0, rot=0.0, leaf=True, stem=0.06):
    """Line-art apple centered at (x, y), about 0.5 * s tall. sx, sy stretch it; rot tilts it (radians)."""
    k = 0.25 * s
    body = [(0, 0.62), (0.25, 0.85), (0.95, 0.8), (0.98, 0.15),
            (0.95, -0.55), (0.55, -0.95), (0.22, -0.82),
            (0.1, -0.78), (-0.1, -0.78), (-0.22, -0.82),
            (-0.55, -0.95), (-0.95, -0.55), (-0.98, 0.15),
            (-0.95, 0.8), (-0.25, 0.85), (0, 0.62)]
    body = [(sx * px, sy * py) for px, py in body]
    top = sy * 0.62
    ax.add_patch(PathPatch(Path(_place(x, y, k, rot, body), [Path.MOVETO] + [Path.CURVE4] * 15),
                           facecolor="white", edgecolor=INK, lw=lw, zorder=3))
    sx_, sy_ = zip(*_place(x, y, k, rot, [(0, top), (stem * 4, top + 0.5)]))
    line(ax, sx_, sy_, color=INK, lw=lw, z=3)
    if leaf:
        lf = _place(x, y, k, rot, [(0.08, top + 0.33), (0.3, top + 0.7), (0.75, top + 0.43), (0.08, top + 0.33)])
        ax.add_patch(PathPatch(Path(lf, [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO]),
                               facecolor="white", edgecolor=INK, lw=lw * 0.8, zorder=3))


def banana(ax, x, y, s=1.0, lw=LW, bend=1.0, length=1.0, thick=1.0, rot=0.0):
    """Line-art banana centered at (x, y), concave side up, about 0.6 * s long.

    bend: curvature, length: arc length, thick: width, rot: tilt (radians).
    """
    k = 0.25 * s
    R = 1.9 / bend
    span = 3.0 * length / R
    u = np.linspace(0, 1, 50)
    a = -np.pi / 2 + span * (u - 0.5)
    w = 0.33 * thick * np.sin(np.pi * (0.03 + 0.94 * u)) ** 0.8
    n = np.c_[np.cos(a), np.sin(a)]
    c = R * n
    outline = np.vstack([c + w[:, None] * n, (c - w[:, None] * n)[::-1]])
    shift = outline.mean(axis=0)
    outline, c = outline - shift, c - shift
    ax.add_patch(Polygon(_place(x, y, k, rot, outline), closed=True, facecolor="white", edgecolor=INK,
                         lw=lw, joinstyle="round", zorder=3))
    # Stem at the right end, small dark tip at the left end.
    t = np.array([-np.sin(a[-1]), np.cos(a[-1])])
    stem = _place(x, y, k, rot, [c[-1], c[-1] + 0.3 * t])
    line(ax, *zip(*stem), color=INK, lw=lw * 2.2, z=3)
    t0 = np.array([np.sin(a[0]), -np.cos(a[0])])
    tip = _place(x, y, k, rot, [c[0], c[0] + 0.08 * t0])
    line(ax, *zip(*tip), color=INK, lw=lw * 2.2, z=3)


def kitten(ax, x, y, s=1.0, lw=LW, tail=1, tilt=0.0, sx=1.0):
    """Line-art sitting kitten centered at (x, y), about 0.5 * s tall.

    tail: 1 curls right, -1 curls left. tilt: head tilt (radians). sx: body width.
    """
    k = 0.25 * s
    kw = dict(facecolor="white", edgecolor=INK, lw=lw, zorder=3)
    t = tail
    tl = _place(x, y, k, 0, [(0.45 * t * sx, -0.85), (1.15 * t * sx, -0.95), (1.2 * t * sx, -0.2), (0.85 * t * sx, 0.0)])
    ax.add_patch(PathPatch(Path(tl, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]),
                           facecolor="none", edgecolor=INK, lw=lw * 1.6, capstyle="round", zorder=3))
    ax.add_patch(Ellipse((x, y - 0.4 * k), 1.3 * k * sx, 1.15 * k, **kw))
    hx, hy = x, y + 0.42 * k
    for side in (-1, 1):
        ear = _place(hx, hy, k, tilt, [(side * 0.12, 0.3), (side * 0.38, 0.62), (side * 0.4, 0.12)])
        ax.add_patch(Polygon(ear, closed=True, joinstyle="round", **kw))
    ax.add_patch(Circle((hx, hy), 0.42 * k, **kw))
    for side in (-1, 1):
        ex, ey = _place(hx, hy, k, tilt, [(side * 0.16, 0.05)])[0]
        ax.add_patch(Circle((ex, ey), 0.05 * k, color=INK, zorder=4))


def smooth_closed(pts):
    """Closed Catmull-Rom curve through pts, as a matplotlib Path."""
    P = np.array(pts, float)
    n = len(P)
    verts, codes = [P[0]], [Path.MOVETO]
    for i in range(n):
        p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % n], P[(i + 2) % n]
        verts += [p1 + (p2 - p0) / 6, p2 - (p3 - p1) / 6, p2]
        codes += [Path.CURVE4] * 3
    return Path(verts, codes)


def smooth_open(ax, pts, **kw):
    P = np.array(pts, float)
    verts, codes = [P[0]], [Path.MOVETO]
    for i in range(len(P) - 1):
        p0, p1, p2 = P[max(i - 1, 0)], P[i], P[i + 1]
        p3 = P[min(i + 2, len(P) - 1)]
        verts += [p1 + (p2 - p0) / 6, p2 - (p3 - p1) / 6, p2]
        codes += [Path.CURVE4] * 3
    ax.add_patch(PathPatch(Path(verts, codes), facecolor="none", **kw))


def brain(ax, x, y, k, mirror=False, cerebellum=True):
    """Side view of a brain facing left (right if mirror), centered at (x, y), about 2k wide. cerebellum=False
    leaves out the cerebellum and brainstem."""
    m = -1 if mirror else 1
    T = lambda pts: [(x + m * k * px, y + k * py) for px, py in pts]
    if cerebellum:
        stem = T([(0.22, -0.3), (0.3, -0.8), (0.46, -0.8), (0.5, -0.3)])
        ax.add_patch(Polygon(stem, closed=True, facecolor="white", edgecolor=INK, lw=0.8, joinstyle="round", zorder=2))
        ax.add_patch(Ellipse((x + m * 0.66 * k, y - 0.36 * k), 0.62 * k, 0.36 * k, facecolor="white", edgecolor=INK,
                             lw=0.8, zorder=2))
        for dy in (-0.36, -0.45):
            smooth_open(ax, T([(0.42, dy + 0.02), (0.66, dy - 0.04), (0.92, dy + 0.03)]), edgecolor="0.45", lw=0.5, zorder=2)
    outline = T([(-1.0, -0.12), (-1.02, 0.32), (-0.62, 0.72), (0.0, 0.84), (0.62, 0.7), (0.98, 0.3),
                 (0.95, -0.12), (0.55, -0.26), (0.05, -0.36), (-0.55, -0.32)])
    ax.add_patch(PathPatch(smooth_closed(outline), facecolor="white", edgecolor=INK, lw=0.9, zorder=3))
    sulc = dict(edgecolor="0.45", lw=0.6, zorder=4)
    smooth_open(ax, T([(-0.62, -0.06), (-0.2, 0.06), (0.3, 0.12)]), **sulc)          # lateral sulcus
    smooth_open(ax, T([(0.12, 0.82), (0.02, 0.5), (-0.06, 0.2)]), **sulc)            # central sulcus
    smooth_open(ax, T([(-0.5, 0.62), (-0.45, 0.36), (-0.6, 0.18)]), **sulc)
    smooth_open(ax, T([(0.5, 0.66), (0.42, 0.42), (0.6, 0.22)]), **sulc)
    smooth_open(ax, T([(-0.35, -0.2), (0.1, -0.16), (0.5, -0.1)]), **sulc)


def brain_site(x, y, k, mirror=False):
    """A point in the temporal lobe of brain(ax, x, y, k, mirror), where figures mark a recorded region."""
    return (x - (-1 if mirror else 1) * 0.1 * k, y - 0.12 * k)


def electrode(ax, tip, angle=60, length=0.8, lw=0.8, z=7):
    """Line-art recording electrode with its tip at `tip`, pointing in from direction `angle` (degrees), with a
    curling wire at the far end."""
    a = np.radians(angle)
    u, n = np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])
    t = np.array(tip, dtype=float)
    p0, p1 = t + 0.45 * length * u, t + 0.8 * length * u
    line(ax, [t[0], p0[0]], [t[1], p0[1]], color=INK, lw=lw, z=z)
    w = 0.045 * length
    body = [p0 + w * n, p1 + w * n, p1 - w * n, p0 - w * n]
    ax.add_patch(Polygon(body, closed=True, facecolor="white", edgecolor=INK, lw=lw, joinstyle="round", zorder=z))
    q = p1 + 0.25 * length * u
    line(ax, [p1[0], q[0]], [p1[1], q[1]], color=INK, lw=lw * 0.8, z=z)
    curl = [q, q + 0.15 * length * u + 0.12 * length * n, q + 0.05 * length * u + 0.3 * length * n,
            q + 0.25 * length * u + 0.4 * length * n]
    smooth_open(ax, [tuple(c) for c in curl], edgecolor=INK, lw=lw * 0.8, zorder=z)
