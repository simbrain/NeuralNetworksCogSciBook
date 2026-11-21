"""From internet text to agent: pretraining, post-training, harness."""
from style import new_fig, save, rbox, arrow

FS = 8
STAGES = ["internet\ntext", "base\nmodel", "chat\nmodel", "agent"]
STEPS = ["pretraining\n(next-token prediction)", "post-training\n(instruction tuning, RLHF)",
         "harness\nand tools"]


OUTPUTS = ['pipeline']


def main():
    fig, ax = new_fig(10, 1.8)
    bw, bh, gap = 1.15, 0.6, 2.1
    for i, s in enumerate(STAGES):
        x = i * (bw + gap)
        rbox(ax, x, 0, bw, bh, s, fs=FS + 1)
        if i < len(STEPS):
            arrow(ax, (x + bw + 0.08, bh / 2), (x + bw + gap - 0.08, bh / 2))
            ax.text(x + bw + gap / 2, bh / 2 + 0.08, STEPS[i], ha="center", va="bottom", fontsize=FS - 1)
    save(fig, "pipeline")


if __name__ == "__main__":
    main()
