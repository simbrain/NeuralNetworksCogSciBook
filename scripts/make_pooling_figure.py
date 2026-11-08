"""Generate images/maxPooling.{svg,pdf,png} (figure maxPooling in ConvolutionalNetworks.tex).

2x2 max pooling, with windows that do not overlap, applied to the 7x7 feature map of figure cnn_filter
(smiley face, backslash filter), giving a 3x3 output. Laid out like cnnConvolution: feature map above,
pooled output below, one window outlined and connected to its output cell by light lines. The last
row and column fit no window and are shown in light gray. Prints the pooled output.

Usage: python3 scripts/make_pooling_figure.py [outdir]   (default: images)
"""
import sys
from cnn_figure_style import U, new_fig, finish, box, line, gray, outline_cells, SMILEY, BACKSLASH, convolve

OUT = sys.argv[1] if len(sys.argv) > 1 else "images"

FMAP = convolve(SMILEY, BACKSLASH)                 # 7x7
P = 2                                              # pool size; windows do not overlap
N = len(FMAP) // P                                 # 3 windows per side; last row and column dropped
POOLED = [[max(FMAP[P*i + a][P*j + b] for a in range(P) for b in range(P)) for j in range(N)] for i in range(N)]
WR, WC = 2, 2                                      # highlighted window (readers find the 3 themselves)
VMAX = max(max(r) for r in FMAP)
LINK = dict(color="0.6", lw=0.6)
GAP = 0.6

n = len(FMAP)
used = lambda r, c: r < N * P and c < N * P
Y_OUT = 0.0
Y_IN = Y_OUT + N * U + GAP

fig, ax = new_fig((3.4, 3.6))

# Feature map: light gray numbers for the dropped row and column
fills = [[gray(FMAP[r][c], VMAX) if used(r, c) else "white" for c in range(n)] for r in range(n)]
nums = [[FMAP[r][c] if used(r, c) else "" for c in range(n)] for r in range(n)]
Pf = box(ax, 0, Y_IN, n, n, 1, ds=0, fills=fills, numbers=nums)
for r in range(n):
    for c in range(n):
        if not used(r, c):
            x, y = Pf(r + 0.5, c + 0.5)
            ax.text(x, y, str(FMAP[r][c]), ha="center", va="center", fontsize=7.5, color="0.7", zorder=4)
outline_cells(ax, Pf, WR * P, WC * P, P, P)

# Pooled output, centered below
x0 = (n - N) * U / 2
Po = box(ax, x0, Y_OUT, N, N, 1, ds=0, fills=[[gray(v, VMAX) for v in r] for r in POOLED], numbers=POOLED)
outline_cells(ax, Po, WR, WC, 1, 1)
for a, b in [(Pf(WR*P + P, WC*P), Po(WR, WC)), (Pf(WR*P + P, WC*P + P), Po(WR, WC + 1))]:
    line(ax, [a[0], b[0]], [a[1], b[1]], z=3.5, **LINK)

for y, t in [(Y_IN + n * U / 2, "Feature\nMap"), (Y_OUT + N * U / 2, "Pooled\nOutput")]:
    ax.text(-0.15, y, t, fontsize=11, ha="right", va="center", color="0.1")

ax.autoscale_view()
finish(fig, ax, OUT, "maxPooling")
for r in POOLED:
    print(r)
