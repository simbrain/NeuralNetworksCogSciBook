"""Generate images/repWidthDepth.{svg,pdf,png} (figure repWidthDepth in InternalRepresentations.tex).

Representational width and depth: two small feed-forward networks drawn bottom to top, a shallow one with a
wide hidden layer and a deeper one with narrower hidden layers. The number of nodes in each layer, which is
also the dimension of that layer's state space, is printed beside it.
"""
from figure_style import new_fig, finish, network

R, DY = 0.07, 0.5


def sized_network(ax, cx, sizes):
    """A network with each layer's size printed at its left."""
    layers = [(i * DY, n) for i, n in enumerate(sizes)]
    xs = network(ax, cx, layers, r=R, color="0.75")
    for (y, n), row in zip(layers, xs):
        ax.text(row[0] - R - 0.08, y, str(n), ha="right", va="center", fontsize=9)


fig, ax = new_fig((4.2, 2.2))
sized_network(ax, 0.0, [5, 9, 2])
sized_network(ax, 2.4, [5, 4, 4, 4, 2])
finish(fig, ax, "repWidthDepth", xlim=(-1.1, 3.1), ylim=(-0.15, 2.15))
