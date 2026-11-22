"""Generate images/chatContext.{svg,pdf,png} (figure chatContext in Transformers.tex).

A conversation in one context window: user turns and model turns (gray) form a
single sequence. The last model turn is still being generated. On the right is
the raw input, a stack of token embeddings with one row per token; thin outlines
group the rows by turn. Tokens and embeddings match images/contextWindowAsStack.png
(figure sequenceDim) and images/contextWindow (figure nextWordPrediction).
"""
from matplotlib.patches import Rectangle
from figure_style import new_fig, save, rounded_box, label, arrow, INK

emb = {"hello": (1, 2, 1, 2), "how": (2, 1, 9, 8), "are": (7, 3, 5, 8),
       "you": (1, 2, 5, 6), "?": (1, 1, 2, 0), "good": (2, 8, 2, 5),
       "thank": (7, 7, 2, 5), ".": (1, 0, 1, 0)}

TURNS = [
    ("user", "hello how are you?", "hello how are you ?"),
    ("model", "good thank you. how are you?", "good thank you . how are you ?"),
    ("user", "good thank you.", "good thank you ."),
    ("model", "█", ""),
]

fig, ax = new_fig((6.6, 3.2))
rh, gap, lw_, bw, pad = 0.44, 0.17, 0.8, 3.0, 0.18
x0 = pad + lw_
for i, (who, text, _) in enumerate(TURNS):
    y = -i * (rh + gap)
    label(ax, pad + lw_ - 0.1, y + rh / 2, who, ha="right", va="center", fontsize=10)
    rounded_box(ax, x0, y, bw, rh, 0.05, edgecolor=INK,
                facecolor="0.88" if who == "model" else "white")
    label(ax, x0 + 0.12, y + rh / 2, text, ha="left", va="center", fontsize=10)

top = rh + pad
bot = -(len(TURNS) - 1) * (rh + gap) - pad
right = x0 + bw + pad
rounded_box(ax, 0, bot, right, top - bot, 0.08, edgecolor=INK, lw=1.0)
label(ax, 0.08, top + 0.06, "context window", ha="left", va="bottom", fontsize=10)

# Stack of token embeddings, one row per token, grouped by turn.
ch, tw, cw, tgap = 0.15, 0.5, 0.24, 0.08
groups = [(who, toks.split()) for who, _, toks in TURNS if toks]
ntok = sum(len(t) for _, t in groups)
stack_h = ntok * ch + (len(groups) - 1) * tgap
sx = right + 0.5
mid = (top + bot) / 2
arrow(ax, (right + 0.08, mid), (sx - 0.12, mid), color=INK, lw=0.8)
y = mid + stack_h / 2
for who, toks in groups:
    y_top = y
    for tok in toks:
        y -= ch
        ax.add_patch(Rectangle((sx, y), tw, ch, fill=False, edgecolor="0.6", lw=0.3, zorder=2))
        ax.text(sx + 0.04, y + ch / 2, tok, ha="left", va="center", fontsize=7.5, zorder=3)
        for k, v in enumerate(emb[tok]):
            xk = sx + tw + 0.06 + k * cw
            ax.add_patch(Rectangle((xk, y), cw, ch, fill=False, edgecolor="0.6", lw=0.3, zorder=2))
            ax.text(xk + 0.04, y + ch / 2, str(v), ha="left", va="center", fontsize=7.5, zorder=3)
    w = tw + 0.06 + 4 * cw
    ax.add_patch(Rectangle((sx - 0.03, y - 0.015), w + 0.06, y_top - y + 0.03, edgecolor=INK, lw=0.4,
                           facecolor="0.88" if who == "model" else "white", zorder=1))
    y -= tgap

ax.set_xlim(-0.05, sx + tw + 0.06 + 4 * cw + 0.1)
ax.set_ylim(min(bot, mid - stack_h / 2) - 0.05, max(top + 0.3, mid + stack_h / 2 + 0.05))
save(fig, "chatContext")
