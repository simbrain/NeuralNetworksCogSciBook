"""Render every draft figure and write gallery.html.

Usage (from this folder):  python3 build.py            # all figures
                           python3 build.py lanes      # only fig_lanes.py
Open gallery.html in a browser; images reload every few seconds, so leave it
open while editing and rerunning.
"""
import glob
import html
import importlib
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)


def run(mods):
    for m in mods:
        try:
            importlib.import_module(m).main()
            print("ok  ", m)
        except Exception:
            print("FAIL", m)
            traceback.print_exc()


def gallery():
    cards = []
    for path in sorted(glob.glob("fig_*.py")):
        mod = os.path.splitext(path)[0]
        doc = (importlib.import_module(mod).__doc__ or "").strip()
        outs = getattr(importlib.import_module(mod), "OUTPUTS", [])
        imgs = "".join(
            f'<figure><img data-src="out/{o}.png"><figcaption>{o} '
            f'<a href="out/{o}.pdf">pdf</a> <a href="out/{o}.svg">svg</a></figcaption></figure>'
            for o in outs)
        cards.append(f'<section><h2>{mod[4:]}</h2><p class="src">{path}</p>'
                     f'<pre>{html.escape(doc)}</pre>{imgs}</section>')
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Figure drafts</title>
<style>
body{{font:14px/1.4 -apple-system,sans-serif;margin:24px;background:#f4f4f4;color:#222}}
section{{background:#fff;border:1px solid #ddd;border-radius:6px;padding:12px 16px;margin:0 0 20px}}
h2{{margin:0;font-size:16px}} .src{{color:#888;margin:2px 0 6px;font-size:12px}}
pre{{white-space:pre-wrap;font:13px/1.4 -apple-system,sans-serif;color:#444;margin:0 0 8px}}
figure{{margin:8px 0}} img{{max-width:100%;max-height:70vh;border:1px solid #eee}}
figcaption{{font-size:12px;color:#888}}
</style></head><body><h1 style="font-size:18px">Transformer figure drafts</h1>
{''.join(cards)}
<script>
function refresh(){{const t=Date.now();document.querySelectorAll('img[data-src]').forEach(i=>i.src=i.dataset.src+'?t='+t)}}
refresh();setInterval(refresh,3000);
</script></body></html>"""
    open("gallery.html", "w").write(page)


if __name__ == "__main__":
    names = sys.argv[1:]
    mods = [f"fig_{n}" for n in names] if names else [p[:-3] for p in sorted(glob.glob("fig_*.py"))]
    run(mods)
    gallery()
    print("gallery:", os.path.join(HERE, "gallery.html"))
