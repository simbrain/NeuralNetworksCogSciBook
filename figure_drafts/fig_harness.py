"""A harness: the program around the model.

The model only ever maps a context to more tokens. The harness reads those
tokens; if they are a tool call it runs the tool and appends the result to
the context, otherwise it shows the reply to the user.
"""
from style import new_fig, save, rbox, arrow, line, INK

FS = 8


OUTPUTS = ['harness']


def main():
    fig, ax = new_fig(6.4, 3.4)
    # Context drawn as a stack of strips.
    cx, cy, cw, ch = 0, 0, 1.3, 1.8
    for k in range(6):
        rbox(ax, cx, cy + k * 0.3, cw, 0.26, fc="0.88" if k % 2 else "white", lw=0.7, r=0.03)
    ax.text(cx + cw / 2, cy - 0.12, "context", ha="center", va="top", fontsize=FS)

    rbox(ax, 2.0, 0.6, 1.2, 0.6, "LLM", fs=FS + 1)
    rbox(ax, 4.0, 0.6, 1.3, 0.6, "harness", fs=FS + 1)
    rbox(ax, 3.85, -1.1, 1.6, 0.6, "tools\n(search, code, files)", fs=FS - 1)
    rbox(ax, 4.0, 2.3, 1.3, 0.5, "user", fs=FS + 1)

    arrow(ax, (cw + 0.05, 0.9), (2.0, 0.9))
    arrow(ax, (3.2, 0.9), (4.0, 0.9))
    ax.text(3.6, 0.98, "tokens", ha="center", va="bottom", fontsize=FS - 1)
    arrow(ax, (4.65, 0.6), (4.65, -0.5))
    ax.text(4.72, 0.05, "tool call", ha="left", va="center", fontsize=FS - 1)
    arrow(ax, (4.65, 1.2), (4.65, 2.3))
    ax.text(4.72, 1.75, "reply", ha="left", va="center", fontsize=FS - 1)

    # Tool result appended to the context.
    line(ax, [3.85, cw / 2, cw / 2], [-0.8, -0.8, -0.45])
    arrow(ax, (cw / 2, -0.45), (cw / 2, -0.02), ms=7)
    ax.text(2.6, -0.72, "result appended", ha="center", va="bottom", fontsize=FS - 1)
    # User message appended to the context.
    line(ax, [4.0, cw / 2, cw / 2], [2.55, 2.55, 2.2])
    arrow(ax, (cw / 2, 2.2), (cw / 2, 1.82), ms=7)
    ax.text(2.6, 2.63, "message appended", ha="center", va="bottom", fontsize=FS - 1)
    save(fig, "harness")


if __name__ == "__main__":
    main()
