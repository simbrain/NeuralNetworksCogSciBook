"""Generate images/filterChannels.{svg,pdf,png} (figure filterChannels in ConvolutionalNetworks.tex).

Redraw of filterDepth.png (Soraya Boza), in the shared style of cnn_figure_style.py.
Left: 3x4x8 input (wide and short), 3x3x3 filter, 2x6 output.
Right: 16x2x2 input, 16x1x1 filter, 2x2 output.
In each, the shaded receptive field runs through every channel of the input.
Every object, depth included, is centered on one horizontal line (Y), as are the signs.

Usage: python3 scripts/make_filter_channels_figure.py [outdir]   (default: images)
"""
import sys
from cnn_figure_style import U, DS, new_fig, finish, box, sign

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"
corner = lambda n: [["white"] * (n - 1) + ["0.6"]] + [["white"] * n] * (n - 1)

fig, ax = new_fig((10, 2.8))
Y = 1.0                                  # shared center line for front faces, signs, and outputs
mid = lambda n, chans=0: Y - (n * U + chans * DS) / 2   # bottom y that centers a box's full height on Y

# Left example
box(ax, 0.0, mid(4, 3), 4, 8, 3, rf=(0, 5, 3))
sign(ax, 2.7, Y, "×")
box(ax, 3.0, mid(3, 3), 3, 3, 3)
sign(ax, 4.45, Y, "=")
box(ax, 4.75, mid(2), 2, 6, 1, ds=0, fills=[["white"] * 5 + ["0.6"], ["white"] * 6])

# Right example: at the center line the rods lean right, so the signs sit past each rod's crossing
RX = 7.4
box(ax, RX, mid(2, 16), 2, 2, 16, rf=(0, 1, 1))        # crosses Y between RX+0.75 and RX+1.75
sign(ax, RX + 2.05, Y, "×")
FX = RX + 1.5
box(ax, FX, mid(1, 16), 1, 1, 16)                     # crosses Y between FX+0.875 and FX+1.375
sign(ax, FX + 1.7, Y, "=")
box(ax, FX + 2.0, mid(2), 2, 2, 1, ds=0, fills=corner(2))

ax.autoscale_view()
finish(fig, ax, OUT, "filterChannels")
