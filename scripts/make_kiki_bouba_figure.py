"""Generate images/kikiBouba.{svg,pdf,png} (figure kikiBouba in LLMsCogSci.tex).

The classic kiki-bouba shapes: a spiky star (usually called "kiki") and a rounded blob (usually called "bouba").
Unlabeled, as in the classic demonstration.
"""
import numpy as np
from figure_style import INK, EDGE, new_fig, finish, poly

fig, ax = new_fig((3.2, 1.5))

# Spiky shape: irregular star with sharp points
rng = np.random.default_rng(3)
n = 9
angles = np.linspace(0, 2 * np.pi, 2 * n, endpoint=False) + rng.uniform(-0.12, 0.12, 2 * n)
radii = np.where(np.arange(2 * n) % 2 == 0, rng.uniform(0.85, 1.0, 2 * n), rng.uniform(0.3, 0.42, 2 * n))
star = np.c_[radii * np.cos(angles), radii * np.sin(angles)] * 0.65 + [0, 0]
poly(ax, star, facecolor="0.8", **EDGE)

# Rounded shape: smooth blob with soft lobes
t = np.linspace(0, 2 * np.pi, 400)
r = 0.62 + 0.1 * np.sin(5 * t + 0.4) + 0.04 * np.sin(3 * t + 1.1)
blob = np.c_[r * np.cos(t), r * np.sin(t)] + [2.0, 0]
poly(ax, blob, facecolor="0.8", **EDGE)

finish(fig, ax, "kikiBouba", xlim=(-0.75, 2.8), ylim=(-0.75, 0.75))
