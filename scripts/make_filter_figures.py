"""Generate the filter and filter bank figures in ConvolutionalNetworks.tex.

Redraws of images by Soraya Boza, in the shared style of cnn_figure_style.py.

  filterToVolume  3x6x6 input, one 3x3x3 filter, 4x4 output
  filterComb      same, with the input channels and the filter's slices pulled apart
  filterBank      3x6x6 input, bank of five 3x3x3 filters, 5x4x4 output

Usage: python3 scripts/make_filter_figures.py [outdir]   (default: images)
"""
import sys
from cnn_figure_style import U, DS, new_fig, finish, box, sign, label, pointer

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"

# filterToVolume ---------------------------------------------------------------
fig, ax = new_fig((7, 2.6))
box(ax, 0, 0, 6, 6, 3, rf=(0, 3, 3))
label(ax, 0.75, -0.12, "Input Volume")
sign(ax, 2.2, 0.75, "×")
fx, fy = 2.55, 0.375
box(ax, fx, fy, 3, 3, 3)
label(ax, fx + 0.375, fy - 0.12, "Filter")
sign(ax, 4.1, 0.75, "=")
box(ax, 4.45, 0.25, 4, 4, 1, ds=0, fills=[["white"] * 3 + ["0.6"]] + [["white"] * 4] * 3)
label(ax, 4.95, 0.13, "Output")
finish(fig, ax, OUT, "filterToVolume", (-0.1, 5.55), (-0.45, 1.95))

# filterComb -------------------------------------------------------------------
GAP = 0.15
fig, ax = new_fig((7, 2.6))
for k in reversed(range(3)):
    box(ax, k * GAP, k * GAP, 6, 6, 1, ds=0, rf=(0, 3, 3), zb=10 * (3 - k))
label(ax, 0.75, -0.12, "Input Volume")
sign(ax, 2.3, 0.75, "×")
for k in reversed(range(3)):
    box(ax, 2.75 + k * GAP, 0.375 + k * GAP, 3, 3, 1, ds=0, zb=10 * (3 - k))
label(ax, 3.12, 0.25, "Filter")
sign(ax, 4.45, 0.75, "=")
box(ax, 4.9, 0.25, 4, 4, 1, ds=0, fills=[["white"] * 3 + ["0.6"]] + [["white"] * 4] * 3)
label(ax, 5.4, 0.13, "Output")
finish(fig, ax, OUT, "filterComb", (-0.1, 6.0), (-0.45, 1.85))

# filterBank -------------------------------------------------------------------
STEP = 1.3
fig, ax = new_fig((6.5, 7))
mid = 2 * STEP + 0.3 + (0.75 + 3 * DS) / 2          # vertical center of the middle filter
box(ax, 0, mid - (1.5 + 3 * DS) / 2, 6, 6, 3)
label(ax, 0.75, mid - (1.5 + 3 * DS) / 2 - 0.12, "Input Volume")
sign(ax, 2.3, mid, "×")
for k in range(5):
    box(ax, 2.7, k * STEP + 0.3, 3, 3, 3)
top_y = 4 * STEP + 0.3
pointer(ax, "Filter", (2.7 + 0.75 + 1.5 * DS, top_y + 0.375 + 1.5 * DS), (4.45, top_y + 0.375 + 1.5 * DS))
label(ax, 3.07, 0.18, "Filter Bank")
sign(ax, 4.3, mid, "=")
oy = mid - (1.0 + 5 * DS) / 2
box(ax, 4.7, oy, 4, 4, 5)
label(ax, 5.2, oy - 0.12, "Output Volume")
finish(fig, ax, OUT, "filterBank", (-0.1, 6.5), (-0.15, top_y + 0.75 + 3 * DS + 0.1))
