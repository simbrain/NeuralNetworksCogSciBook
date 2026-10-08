"""Draw the hill-and-valley picture of basins of attraction."""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d import proj3d

# Four valleys (center x, center y, depth, width in x, width in y) in a
# gentle bowl. Unequal widths make orbits curve on their way down.
VALLEYS = [(-1.5, 1.1, 1.0, 1.0, 0.65),
           (1.4, 1.4, 0.8, 0.7, 0.8),
           (-1.1, -1.5, 0.75, 0.75, 0.7),
           (1.6, -1.0, 0.9, 0.65, 0.9)]
START = (-0.2, 2.8)          # initial condition of the highlighted orbit
FLOOR = -4.8                 # height of the projected state space


def f(x, y):
    z = 0.03 * (x**2 + y**2)
    for cx, cy, depth, sx, sy in VALLEYS:
        z = z - depth * np.exp(-(x - cx)**2 / (2 * sx**2)
                               - (y - cy)**2 / (2 * sy**2))
    return z


def grad(x, y, h=1e-4):
    return np.array([(f(x + h, y) - f(x - h, y)) / (2 * h),
                     (f(x, y + h) - f(x, y - h)) / (2 * h)])


def descend(start, rate=0.05, steps=600):
    path = [np.array(start, float)]
    for _ in range(steps):
        path.append(path[-1] - rate * grad(*path[-1]))
    return np.array(path)


x = y = np.linspace(-3, 3, 97)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Which attractor each point of a fine grid ends up at.
fine = np.linspace(-3, 3, 241)
FX, FY = np.meshgrid(fine, fine)
P = np.array([FX, FY])
for _ in range(1500):
    P = P - 0.1 * grad(*P)
attractors = np.array([descend(v[:2], steps=2000)[-1] for v in VALLEYS])
dist = np.linalg.norm(P[None] - attractors[:, :, None, None], axis=1)
basin = dist.argmin(axis=0)


def blur(a, sigma=2.0):
    """Smooth a basin mask so its boundary contour isn't pixel-jagged."""
    k = np.exp(-np.arange(-6, 7)**2 / (2 * sigma**2))
    k /= k.sum()
    a = np.apply_along_axis(np.convolve, 0, np.pad(a, 6, "edge"), k, "valid")
    return np.apply_along_axis(np.convolve, 1, a, k, "valid")


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection="3d", computed_zorder=False)
ax.view_init(elev=28, azim=-62)

# The floor: basin boundaries, energy contours, and a few orbits.
ax.contour(X, Y, Z, levels=14, zdir="z", offset=FLOOR, colors="black",
           linewidths=0.3, linestyles="solid", alpha=0.35, zorder=0)
for i in range(len(VALLEYS)):
    ax.contour(FX, FY, blur((basin == i).astype(float)), levels=[0.5], zdir="z",
               offset=FLOOR, colors="black", linewidths=1.0, zorder=0)
orbits = [descend(s) for sx0 in np.linspace(-2.7, 2.7, 6)
          for s in [(sx0, -2.8), (sx0, 2.8), (-2.8, sx0), (2.8, sx0)]]
for p in orbits:
    ax.plot(p[:, 0], p[:, 1], FLOOR, color="0.55", linewidth=0.5, zorder=0)
ax.plot([-3, 3, 3, -3, -3], [-3, -3, 3, 3, -3], FLOOR, color="black",
        linewidth=0.6, zorder=0)
path = descend(START)
ax.plot(path[:, 0], path[:, 1], FLOOR, color="black",
        linestyle=(0, (4, 2)), linewidth=1.4, zorder=0)
ax.scatter(*path[0], FLOOR, s=40, color="black", depthshade=False, zorder=0)
ax.scatter(attractors[:, 0], attractors[:, 1], FLOOR, s=30, marker="x",
           color="black", linewidth=1.3, depthshade=False, zorder=0)

# Dotted drop lines tie the marble and its attractor to the floor.
for px, py in (path[0], path[-1]):
    ax.plot([px, px], [py, py], [FLOOR, f(px, py)], color="black",
            linestyle=":", linewidth=0.8, zorder=0.5)

# The landscape, with the marble and its orbit down to the attractor.
shade = LightSource(azdeg=315, altdeg=40).shade(
    Z, cmap=plt.cm.gray, vmin=Z.min() - 1.2, vmax=Z.max() + 0.3,
    blend_mode="soft")
ax.plot_surface(X, Y, Z, facecolors=shade, rstride=3, cstride=3,
                edgecolor=(0, 0, 0, 0.35), linewidth=0.3, antialiased=True,
                shade=False, zorder=1)
lift = 0.04
ax.plot(path[:, 0], path[:, 1], f(path[:, 0], path[:, 1]) + lift,
        color="black", linestyle=(0, (4, 2)), linewidth=1.4, zorder=3)
end = path[-1]
ax.scatter(*end, f(*end) + lift, s=40, marker="x", color="black",
           linewidth=1.5, depthshade=False, zorder=4)
ax.scatter(*path[0], f(*path[0]) + 0.1, s=180, color="black",
           edgecolor="white", linewidth=1, depthshade=False, zorder=5)

ax.set_axis_off()
ax.set(xlim=(-3, 3), ylim=(-3, 3), zlim=(FLOOR, Z.max()))
ax.set_box_aspect((1.6, 1.6, 1.0), zoom=1.0)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)


def arrowhead(xs, ys, zs, frac=0.5, size=18, color="black", zorder=3.5):
    """Draw an arrowhead partway along a 3-D path, pointing downstream.

    frac is how far along the path (by length in the plane) to put it."""
    sx, sy, _ = proj3d.proj_transform(xs, ys, np.broadcast_to(zs, xs.shape),
                                      ax.get_proj())
    length = np.r_[0, np.cumsum(np.hypot(np.diff(xs), np.diff(ys)))]
    i = np.searchsorted(length, frac * length[-1])
    j = np.searchsorted(length, frac * length[-1] + 0.05)
    ax.annotate("", xy=(sx[j], sy[j]), xytext=(sx[i], sy[i]), zorder=zorder,
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=0,
                                mutation_scale=size, shrinkA=0, shrinkB=0))


# Arrows. Comment out any of these blocks to remove those arrows.
# On the marble's orbit along the surface.
arrowhead(path[:, 0], path[:, 1], f(path[:, 0], path[:, 1]) + lift, 0.55)
# On its projection on the floor.
arrowhead(path[:, 0], path[:, 1], FLOOR, 0.55, zorder=0.2)
# On the gray orbits on the floor.
for p in orbits:
    arrowhead(p[:, 0], p[:, 1], FLOOR, 0.45, size=9, color="0.55",
              zorder=0.1)

# Crop to the drawn content; tight_layout can't see into 3-D axes.
fig.canvas.draw()
pixels = np.asarray(fig.canvas.buffer_rgba())[..., :3]
rows, cols = np.nonzero((pixels < 250).any(axis=2))
h, dpi = pixels.shape[0], fig.dpi
pad = 4
crop = Bbox([[(cols.min() - pad) / dpi, (h - rows.max() - pad) / dpi],
             [(cols.max() + pad) / dpi, (h - rows.min() + pad) / dpi]])

root = Path(__file__).resolve().parents[1]
fig.savefig(root / "images/BasinsOfAttraction.pdf", bbox_inches=crop)
if len(sys.argv) > 1:
    fig.savefig(sys.argv[1], dpi=150, bbox_inches=crop)
