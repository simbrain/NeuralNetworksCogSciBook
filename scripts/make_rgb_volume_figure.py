"""Generate images/rgbVolume.{svg,pdf,png} (figure rgbVolume in ConvolutionalNetworks.tex).

A 9x9 pixel-art flower in a pot, the same data drawn as a 3x9x9 volume (channel layers tinted red,
green, and blue), and its three channels side by side. Petals are red, the stem and leaves green, and
the pot blue. The center is yellow, a mix of red and green, so it appears in two channels. Following
the book's convention, 0 is drawn as white, so the image has a white background rather than the black
of true RGB.

Usage: python3 scripts/make_rgb_volume_figure.py [outdir]   (default: images)
"""
import sys
from matplotlib.colors import to_rgb
from cnn_figure_style import U, DS, new_fig, finish, box, poly, sign, label

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"

RED, GREEN, BLUE, YELLOW = "#c44e52", "#55a868", "#4c72b0", "#dcc13a"   # muted; yellow = red + green

# Pixel art: R red, Y yellow (red + green), G green, B blue, . empty
ART = [
    "...RRR...",
    "..RRYRR..",
    "...RRR...",
    "....G....",
    "..GGG....",
    "....GGG..",
    "....G....",
    "..BBBBB..",
    "...BBB...",
]
CODES = {"R": {0}, "Y": {0, 1}, "G": {1}, "B": {2}}         # channels: 0 = red, 1 = green, 2 = blue
n = len(ART)
pixels = {(r, c): CODES[ch] for r, row in enumerate(ART) for c, ch in enumerate(row) if ch != "."}

COLOR_OF = {frozenset({0}): RED, frozenset({1}): GREEN, frozenset({2}): BLUE, frozenset({0, 1}): YELLOW}
CHANNEL_COLORS = [(RED, "Red"), (GREEN, "Green"), (BLUE, "Blue")]
composite = [[COLOR_OF[frozenset(pixels[(r, c)])] if (r, c) in pixels else "white" for c in range(n)]
             for r in range(n)]
channel = lambda k: [[CHANNEL_COLORS[k][0] if k in pixels.get((r, c), ()) else "white" for c in range(n)]
                     for r in range(n)]


def tint(color, amount):
    """Mix a color with white; amount is the share of the color."""
    return tuple(1 - amount * (1 - v) for v in to_rgb(color))


fig, ax = new_fig((13, 2.9))
W = n * U                                                  # width of one 9x9 grid
LY = -0.12                                                 # label baseline

# Color image
box(ax, 0, 0, n, n, 1, ds=0, fills=composite)
label(ax, W / 2, LY, "Color image")
sign(ax, W + 0.35, W / 2, "=")

# The same image as a volume: front face is the red channel; each channel's layer is tinted
vx = W + 0.7
box(ax, vx, 0, n, n, 3, fills=channel(0))
for k, (color, _) in enumerate(CHANNEL_COLORS):
    o0, o1 = k * DS, (k + 1) * DS
    poly(ax, [(vx + o0, W + o0), (vx + W + o0, W + o0), (vx + W + o1, W + o1), (vx + o1, W + o1)],
         z=1.5, facecolor=tint(color, 0.35), edgecolor="none")
    poly(ax, [(vx + W + o0, o0), (vx + W + o1, o1), (vx + W + o1, W + o1), (vx + W + o0, W + o0)],
         z=1.5, facecolor=tint(color, 0.55), edgecolor="none")
label(ax, vx + W / 2, LY, "3 × 9 × 9 volume")
sign(ax, vx + W + 3 * DS + 0.4, W / 2, "→")

# Channels side by side
x = vx + W + 3 * DS + 0.8
for k, (color, name) in enumerate(CHANNEL_COLORS):
    box(ax, x, 0, n, n, 1, ds=0, fills=channel(k))
    label(ax, x + W / 2, LY, f"{name} channel")
    x += W + 0.3

ax.autoscale_view()
finish(fig, ax, OUT, "rgbVolume")
