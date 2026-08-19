"""Render the party as an animated screen: one entry at a time, blinking arrow."""
import re, io, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen

def raster(svg):
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    W, H = int(m.group(1)), int(m.group(2))
    img = Image.new("RGB", (W, H), "#ffffff"); d = ImageDraw.Draw(img)
    for tag in re.findall(r'<(?:rect|path)[^>]*>', svg):
        fill = (re.search(r'fill="([^"]+)"', tag) or [None, None])[1]
        if tag.startswith('<rect'):
            gv = lambda k, dv=0: float((re.search(k + r'="([\d.]+)"', tag) or [0, dv])[1])
            x, y, w, h, rx = gv('x'), gv('y'), gv('width'), gv('height'), gv('rx')
            st = (re.search(r'stroke="([^"]+)"', tag) or [None, None])[1]
            sw = int(gv('stroke-width', 0))
            bb = [x, y, x + w - 1, y + h - 1]
            if rx: d.rounded_rectangle(bb, radius=rx, fill=fill, outline=st, width=sw if st else 0)
            else:  d.rectangle(bb, fill=fill, outline=st, width=sw if st else 0)
        else:
            dd = (re.search(r'd="([^"]*)"', tag) or [None, ''])[1]
            for mm in re.finditer(r'M([-\d.]+) ([-\d.]+)h([-\d.]+)v([-\d.]+)', dd):
                x, y, w, h = map(float, mm.groups())
                d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill)
    return img

def build(theme, out, hold=1300, blink=380):
    frames, durs = [], []
    for e in gen.PARTY:
        on  = raster(gen.entry(*e, theme, minlines=gen.MAXL, arrow_on=True))
        off = raster(gen.entry(*e, theme, minlines=gen.MAXL, arrow_on=False))
        frames += [on, off, on];  durs += [hold, blink, hold]
    # global palette across every frame, not just the first
    W0, H0 = frames[0].size
    strip = Image.new("RGB", (W0, H0 * len(frames)))
    for i, f in enumerate(frames): strip.paste(f, (0, i * H0))
    base = strip.quantize(colors=128, method=Image.MEDIANCUT)
    pal = [f.quantize(palette=base, dither=Image.NONE) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durs,
                loop=0, optimize=True, disposal=1)
    return out, os.path.getsize(out), frames[0].size, sum(durs)

print(build("dark", os.path.join(os.path.dirname(os.path.abspath(__file__)), "codex.gif")))
