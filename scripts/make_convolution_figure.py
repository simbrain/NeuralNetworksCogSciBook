"""Generate the convolution figures in section 1 of ConvolutionalNetworks.tex.

  cnnConvolution       (figure cnn_filter) Left: a 9x9 smiley-face input, a 3x3 backslash-edge filter,
                       and the 7x7 feature map, drawn as one-channel boxes. Right: the same convolution
                       with every number shown. Replaces happyConvolution.png (Soraya Boza, after User
                       Cecbur) and CNN_WorkedExample.png.
  cnnConvolutionSlash  (figure cnn_filter2) cnnConvolution's right panel next to the same input with a
                       slash-edge filter, so the two filters and feature maps can be compared.

Prints the computed feature maps.

Usage: python3 scripts/make_convolution_figure.py [outdir]   (default: images)
"""
import sys
import numpy as np
from cnn_figure_style import U, DS, new_fig, finish, box, line, gray, outline_cells, SMILEY, BACKSLASH, SLASH, \
    convolve

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"

fills = lambda a, vmax: [[gray(v, vmax) for v in row] for row in a]
LINK = dict(color="0.6", lw=0.6)
GAP = 0.5                                           # vertical gap between rows
Y_OUT = 0.0
Y_FIL = Y_OUT + 7 * U + DS + GAP
Y_IN = Y_FIL + 3 * U + DS + GAP


def panel(ax, x0, filt, depth, numbers):
    """Input, filter, and feature map stacked vertically, with the best-matching receptive field outlined."""
    fmap = np.array(convolve(SMILEY, filt))
    r0, c0 = map(int, np.unravel_index(fmap.argmax(), fmap.shape))
    ds = DS if depth else 0
    kw = lambda a: dict(chans=1, ds=ds, numbers=a if numbers else None)
    Pi = box(ax, x0, Y_IN, 9, 9, fills=fills(SMILEY, 1), **kw(SMILEY))
    Pf = box(ax, x0 + 3 * U, Y_FIL, 3, 3, fills=fills(filt, 1), zb=10, **kw(filt))
    Po = box(ax, x0 + U, Y_OUT, 7, 7, fills=fills(fmap, 3), **kw(fmap.tolist()))
    outline_cells(ax, Pi, r0, c0, 3, 3)
    outline_cells(ax, Po, r0, c0, 1, 1)
    for a, b in [(Pi(r0+3, c0), Pf(0, 0)), (Pi(r0+3, c0+3), Pf(0, 3)),
                 (Pf(3, 0), Po(r0, c0)), (Pf(3, 3), Po(r0, c0+1))]:
        line(ax, [a[0], b[0]], [a[1], b[1]], z=3.5, **LINK)
    print(fmap)


def row_labels(ax):
    for y, t in [(Y_IN + 4.5 * U, "Input"), (Y_FIL + 1.5 * U, "Filter"), (Y_OUT + 3.5 * U, "Feature\nMap")]:
        ax.text(-0.15, y, t, fontsize=11, ha="right", va="center", color="0.1")


# cnnConvolution: two views of the backslash filter
fig, ax = new_fig((6.2, 6.2))
panel(ax, 0.0, BACKSLASH, depth=True, numbers=False)
panel(ax, 9 * U + DS + 0.6, BACKSLASH, depth=False, numbers=True)
row_labels(ax)
ax.autoscale_view()
finish(fig, ax, OUT, "cnnConvolution")

# cnnConvolutionSlash: backslash and slash filters side by side, numbers shown
fig, ax = new_fig((6.2, 6.2))
panel(ax, 0.0, BACKSLASH, depth=False, numbers=True)
panel(ax, 9 * U + DS + 0.6, SLASH, depth=False, numbers=True)
row_labels(ax)
ax.autoscale_view()
finish(fig, ax, OUT, "cnnConvolutionSlash")
