"""Draw the coordinate-list example used in the abridged chapter."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

points = [(-2, 2), (2, 2), (-3, 0), (-2, -1), (-1, -2),
          (0, -2), (1, -2), (2, -1), (3, 0)]
fig, ax = plt.subplots(figsize=(3.2, 3.2))
ax.scatter(*zip(*points), s=65, color="#17619b", zorder=3)
ax.set(xlim=(-4, 4), ylim=(-3, 4), xticks=range(-3, 4),
       yticks=range(-2, 4), xlabel="$x$", ylabel="$y$")
ax.set_aspect("equal")
ax.grid(alpha=.2)
ax.axhline(0, color="gray", linewidth=.7)
ax.axvline(0, color="gray", linewidth=.7)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(Path(__file__).resolve().parents[1] / "images/coordinateHappyFace.pdf")
