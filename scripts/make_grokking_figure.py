"""Generate images/grokking.{svg,pdf,png} (figure grokking in LLMsCogSci.tex).

Grokking: error on training problems and on new problems over training. The curves were digitized from the train
and test loss curves for modular addition in Nanda et al. (2023), figure "mod_addition_loss_curve" in the arXiv
source of 2301.05217 (scripts/data/grokking_*_loss.csv). The phase boundaries (memorization 0-1.4k epochs, circuit
formation 1.4k-9.4k, cleanup 9.4k-14k) are from the same paper. Error (loss) is on a log scale, as in the paper.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from figure_style import DATA, INK, save

XMAX = 16000

test = np.loadtxt(DATA / "grokking_test_loss.csv", delimiter=",", skiprows=1)
train = np.loadtxt(DATA / "grokking_train_loss.csv", delimiter=",", skiprows=1)

fig, ax = plt.subplots(figsize=(4.8, 2.4))
for d, color, lw in ((train, "0.55", 1.2), (test, INK, 1.4)):
    keep = d[:, 0] <= XMAX
    ax.plot(d[keep, 0], d[keep, 1], color=color, lw=lw, solid_joinstyle="round")
ax.set_yscale("log")
ax.set_xlim(0, XMAX)
ax.set_ylim(5e-8, 1e5)

ax.text(4500, 40, "new problems", ha="left", va="bottom", fontsize=8)
ax.text(4500, 4e-7, "training problems", ha="left", va="bottom", fontsize=8, color="0.4")

# Phases.
for x in (1400, 9400, 14000):
    ax.axvline(x, color="0.6", lw=0.6, ls=(0, (3, 3)), zorder=0)
top = 8e4
ax.text(200, top, "memorize", ha="left", va="top", fontsize=8,
        bbox=dict(facecolor="white", edgecolor="none", pad=1))
for x0, x1, label in ((1400, 9400, "learn a general rule"), (9400, 14000, "drop memorized\nanswers")):
    ax.text((x0 + x1) / 2 + (600 if x0 == 1400 else 0), top, label, ha="center", va="top", fontsize=8)

ax.set_xlabel("training time (epochs)", fontsize=8)
ax.set_ylabel("error", fontsize=8)
ax.set_xticks([0, 5000, 10000, 15000])
ax.set_xticklabels(["0", "5,000", "10,000", "15,000"], fontsize=7)
ax.set_yticks([])
ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_linewidth(0.6)

save(fig, "grokking")
