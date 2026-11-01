"""Generate images/contextWindow.{svg,pdf,png} (figure nextWordPrediction in Transformers.tex).

Embeddings match images/contextWindowAsStack.png (figure sequenceDim).
Targets are one-hot over the seven-token vocabulary:
hello, how, are, you, ?, good, thank.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

emb = {"hello": (1, 2, 1, 2), "how": (2, 1, 9, 8), "are": (7, 3, 5, 8),
       "you": (1, 2, 5, 6), "?": (1, 1, 2, 0), "good": (2, 8, 2, 5),
       "thank": (7, 7, 2, 5)}
vocab = ["hello", "how", "are", "you", "?", "good", "thank"]
prompt = ["hello", "how", "are", "you", "?"]
rows = [prompt, prompt + ["good"], prompt + ["good", "thank"]]
targets = ["good", "thank", "you"]
ncols = 8

def onehot(w):
    return "(" + ",".join("1" if v == w else "0" for v in vocab) + ")"

def vec(t):
    return "(" + ",".join(str(x) for x in t) + ")"

cw, ch = 1.0, 0.5        # cell width/height (inches)
tw = 1.75                 # target column width
gap = 0.25
W = ncols * cw + gap + tw
fig = plt.figure(figsize=(W + 0.2, 4.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-0.1, W + 0.1)
ax.set_ylim(0, 4.6)
ax.axis("off")
mono = dict(family="DejaVu Sans Mono")
lw = 0.8

def table(y_top, cells, tgt, fs):
    for r, row in enumerate(cells):
        y = y_top - (r + 1) * ch
        for c in range(ncols):
            ax.add_patch(Rectangle((c * cw, y), cw, ch, fill=False, lw=lw))
            if c < len(row):
                ax.text(c * cw + cw / 2, y + ch / 2, row[c], ha="center",
                        va="center", fontsize=fs, **mono)
        x0 = ncols * cw + gap
        ax.add_patch(Rectangle((x0, y), tw, ch, fill=False, lw=lw))
        ax.text(x0 + tw / 2, y + ch / 2, tgt[r], ha="center", va="center",
                fontsize=fs, **mono)

def headers(y, left, right):
    ax.text(ncols * cw / 2, y, left, ha="center", va="bottom", fontsize=15)
    ax.text(ncols * cw + gap + tw / 2, y, right, ha="center", va="bottom", fontsize=15)

headers(4.32, "Input tokens", "Target")
table(4.25, rows, targets, 14)
headers(2.07, "Token embeddings", "Target")
emb_rows = [[vec(emb[w]) for w in row] for row in rows]
blank = vec((0, 0, 0, 0))
emb_rows = [r + [blank] * (ncols - len(r)) for r in emb_rows]
table(2.0, emb_rows, [onehot(t) for t in targets], 11)

for ext in ("svg", "pdf", "png"):
    fig.savefig(f"images/contextWindow.{ext}", dpi=300 if ext == "png" else None,
                bbox_inches="tight", pad_inches=0.05)
