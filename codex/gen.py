#!/usr/bin/env python3
"""Generate Codex-style UI panels as pure-pixel SVG (no fonts, no external assets)."""
import os
from sprites import SPRITES, avatar_sprite

F = {}
def g(c, *rows): F[c] = rows
g('A','.###.','#...#','#...#','#####','#...#','#...#','#...#')
g('B','####.','#...#','#...#','####.','#...#','#...#','####.')
g('C','.###.','#...#','#....','#....','#....','#...#','.###.')
g('D','####.','#...#','#...#','#...#','#...#','#...#','####.')
g('E','#####','#....','#....','####.','#....','#....','#####')
g('F','#####','#....','#....','####.','#....','#....','#....')
g('G','.###.','#...#','#....','#.###','#...#','#...#','.###.')
g('H','#...#','#...#','#...#','#####','#...#','#...#','#...#')
g('I','#####','..#..','..#..','..#..','..#..','..#..','#####')
g('J','..###','...#.','...#.','...#.','...#.','#..#.','.##..')
g('K','#...#','#..#.','#.#..','##...','#.#..','#..#.','#...#')
g('L','#....','#....','#....','#....','#....','#....','#####')
g('M','#...#','##.##','#.#.#','#...#','#...#','#...#','#...#')
g('N','#...#','##..#','#.#.#','#..##','#...#','#...#','#...#')
g('O','.###.','#...#','#...#','#...#','#...#','#...#','.###.')
g('P','####.','#...#','#...#','####.','#....','#....','#....')
g('Q','.###.','#...#','#...#','#...#','#.#.#','#..#.','.##.#')
g('R','####.','#...#','#...#','####.','#.#..','#..#.','#...#')
g('S','.####','#....','#....','.###.','....#','....#','####.')
g('T','#####','..#..','..#..','..#..','..#..','..#..','..#..')
g('U','#...#','#...#','#...#','#...#','#...#','#...#','.###.')
g('V','#...#','#...#','#...#','#...#','#...#','.#.#.','..#..')
g('W','#...#','#...#','#...#','#...#','#.#.#','##.##','#...#')
g('X','#...#','#...#','.#.#.','..#..','.#.#.','#...#','#...#')
g('Y','#...#','#...#','.#.#.','..#..','..#..','..#..','..#..')
g('Z','#####','....#','...#.','..#..','.#...','#....','#####')
g('0','.###.','#...#','#..##','#.#.#','##..#','#...#','.###.')
g('1','..#..','.##..','..#..','..#..','..#..','..#..','.###.')
g('2','.###.','#...#','....#','...#.','..#..','.#...','#####')
g('3','#####','...#.','..#..','...#.','....#','#...#','.###.')
g('4','...#.','..##.','.#.#.','#..#.','#####','...#.','...#.')
g('5','#####','#....','####.','....#','....#','#...#','.###.')
g('6','..##.','.#...','#....','####.','#...#','#...#','.###.')
g('7','#####','....#','...#.','..#..','.#...','.#...','.#...')
g('8','.###.','#...#','#...#','.###.','#...#','#...#','.###.')
g('9','.###.','#...#','#...#','.####','....#','...#.','.##..')
g(' ','.....','.....','.....','.....','.....','.....','.....')
g('.','.....','.....','.....','.....','.....','.##..','.##..')
g(',','.....','.....','.....','.....','.##..','.##..','.#...')
g("'",'.#...','.#...','.....','.....','.....','.....','.....')
g('-','.....','.....','.....','#####','.....','.....','.....')
g('/','....#','....#','...#.','..#..','.#...','#....','#....')
g(':','.....','.##..','.##..','.....','.##..','.##..','.....')
g('%','##..#','##.#.','..#..','.#...','#.##.','..##.','.....')
g('+','.....','..#..','..#..','#####','..#..','..#..','.....')
g('!','..#..','..#..','..#..','..#..','..#..','.....','..#..')
g('?','.###.','#...#','....#','...#.','..#..','.....','..#..')
g('(','...#.','..#..','.#...','.#...','.#...','..#..','...#.')
g(')','.#...','..#..','...#.','...#.','...#.','..#..','.#...')
g('=','.....','.....','#####','.....','#####','.....','.....')
g('#','.#.#.','#####','.#.#.','.#.#.','#####','.#.#.','.....')
g('*','.....','#...#','.###.','#####','.###.','#...#','.....')

g('a','.....','.....','.###.','....#','.####','#...#','.####','.....')
g('b','#....','#....','####.','#...#','#...#','#...#','####.','.....')
g('c','.....','.....','.###.','#....','#....','#....','.###.','.....')
g('d','....#','....#','.####','#...#','#...#','#...#','.####','.....')
g('e','.....','.....','.###.','#...#','#####','#....','.###.','.....')
g('f','..##.','.#..#','.#...','###..','.#...','.#...','.#...','.....')
g('g','.....','.....','.####','#...#','#...#','.####','....#','.###.')
g('h','#....','#....','####.','#...#','#...#','#...#','#...#','.....')
g('i','..#..','.....','.##..','..#..','..#..','..#..','.###.','.....')
g('j','...#.','.....','..##.','...#.','...#.','...#.','#..#.','.##..')
g('k','#....','#....','#..#.','#.#..','##...','#.#..','#..#.','.....')
g('l','.##..','..#..','..#..','..#..','..#..','..#..','.###.','.....')
g('m','.....','.....','##.#.','#.#.#','#.#.#','#...#','#...#','.....')
g('n','.....','.....','####.','#...#','#...#','#...#','#...#','.....')
g('o','.....','.....','.###.','#...#','#...#','#...#','.###.','.....')
g('p','.....','.....','####.','#...#','#...#','####.','#....','#....')
g('q','.....','.....','.####','#...#','#...#','.####','....#','....#')
g('r','.....','.....','#.##.','##..#','#....','#....','#....','.....')
g('s','.....','.....','.####','#....','.###.','....#','####.','.....')
g('t','.#...','.#...','###..','.#...','.#...','.#..#','..##.','.....')
g('u','.....','.....','#...#','#...#','#...#','#..##','.##.#','.....')
g('v','.....','.....','#...#','#...#','#...#','.#.#.','..#..','.....')
g('w','.....','.....','#...#','#...#','#.#.#','#.#.#','.#.#.','.....')
g('x','.....','.....','#...#','.#.#.','..#..','.#.#.','#...#','.....')
g('y','.....','.....','#...#','#...#','#...#','.####','....#','.###.')
g('z','.....','.....','#####','...#.','..#..','.#...','#####','.....')
g(';','.....','.##..','.##..','.....','.##..','.##..','.#...','.....')
g('"','.#.#.','.#.#.','.....','.....','.....','.....','.....','.....')

CW, CH, GAP = 5, 8, 1
def px(s, ox, oy):
    out = []
    for i, ch in enumerate(s):
        rows = F.get(ch) or F.get(ch.upper()) or F['?']
        if len(rows) < CH: rows = tuple(rows) + ('.....',) * (CH - len(rows))
        bx = ox + i * (CW + GAP)
        for ry, row in enumerate(rows):
            for rx, c in enumerate(row):
                if c == '#': out.append((bx + rx, oy + ry))
    return out

def path(pixels, u=1):
    """merge horizontal runs into one compact path"""
    if not pixels: return ""
    by = {}
    for x, y in pixels: by.setdefault(y, []).append(x)
    d = []
    for y in sorted(by):
        xs = sorted(by[y]); i = 0
        while i < len(xs):
            j = i
            while j + 1 < len(xs) and xs[j+1] == xs[j] + 1: j += 1
            x0, w = xs[i], xs[j] - xs[i] + 1
            d.append(f"M{x0*u} {y*u}h{w*u}v{u}h{-w*u}z")
            i = j + 1
    return "".join(d)

def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= n: cur = (cur + " " + w).strip()
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

TYPES = {
 'SEARCH':'#4F7BD6','ENGINE':'#8E96AD','VISION':'#D4497E','MUSIC':'#C9789F',
 'SOLVER':'#6F4FC0','RESEARCH':'#5A6B8C','FORENSICS':'#6E5A46','MOBILE':'#7A5F9E',
 'OFFLINE':'#3F8F63','PIPELINE':'#C9A227','LLM':'#D1793C','TOOLS':'#7E8570',
}
DARKTEXT = set()

TH = {
 'light': dict(shell='#B3261E', shell_hi='#E2564C', shell_lo='#7E1A14',
               screen='#F4F6E8', line='#2B3A67', ink='#16233F', dim='#5C6B8A',
               bar='#2B3A67', bartx='#F4F6E8', box='#FFFFFF', edge='#98A6C8', well='#E4EAF6', tile='#EDF1F9', scan='#E9ECDC', bevel='#C9CFB8', screw='#8E1F18'),
 'dark':  dict(shell='#8E1E18', shell_hi='#B3352C', shell_lo='#4E0F0B',
               screen='#0F141C', line='#5C74B8', ink='#DCE6F5', dim='#8A9AC0',
               bar='#22304F', bartx='#DCE6F5', box='#161D28', edge='#3A4A72', well='#1E2938', tile='#19212E', scan='#0C1017', bevel='#050810', screw='#3C0B08'),
}

U = 3  # pixel scale
W = 268  # virtual width

def sprite_paths(kind, ox, oy, u):
    g, pal = SPRITES[kind]()
    groups = {}
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != '.': groups.setdefault(c, []).append((ox + x, oy + y))
    order = [k for k in groups if k != 'K'] + (['K'] if 'K' in groups else [])
    return "".join(f'<path d="{path(groups[c], u)}" fill="{pal[c]}"/>' for c in order)


AVATAR = None
def set_avatar(p):
    global AVATAR
    AVATAR = avatar_sprite(p)

def draw_sprite(sp, ox, oy, u):
    g, pal = (AVATAR if sp == 'me' else SPRITES[sp]())
    grp = {}
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != '.': grp.setdefault(c, []).append((ox + x, oy + y))
    order = [k for k in grp if k != 'K'] + (['K'] if 'K' in grp else [])
    return "".join(f'<path d="{path(grp[c], u)}" fill="{pal[c]}"/>' for c in order)

def seal(x, y, u, col='#3F8F63'):
    """9x9 check-in-a-disc: this number is externally checkable"""
    D, C = [], []
    for j in range(9):
        for i in range(9):
            if (i-4)**2 + (j-4)**2 <= 17: D.append((x+i, y+j))
    for i, j in ((2,4),(3,5),(4,6),(5,5),(6,4),(7,3)):
        C.append((x+i, y+j))
        if i >= 4: C.append((x+i, y+j-1))
    D = [p for p in D if p not in C]
    return (f'<path d="{path(D,u)}" fill="{col}"/>'
            f'<path d="{path(C,u)}" fill="#F4F6F0"/>')

def arrow(x, y, u, col):
    p = [(x+i, y+r) for r in range(3) for i in range(r, 5-r)]
    return f'<path d="{path(p,u)}" fill="{col}"/>'

def frame(H, t, o):
    A = o.append
    A(f'<rect width="{W*U}" height="{H*U}" rx="{3*U}" fill="{t["shell"]}"/>')
    A(f'<rect x="{U}" y="{U}" width="{(W-2)*U}" height="{2*U}" fill="{t["shell_hi"]}"/>')
    A(f'<rect x="{U}" y="{(H-3)*U}" width="{(W-2)*U}" height="{2*U}" fill="{t["shell_lo"]}"/>')

def screen(x, y, w, h, t, o):
    A = o.append
    A(f'<rect x="{x*U}" y="{y*U}" width="{w*U}" height="{h*U}" fill="{t["line"]}"/>')
    A(f'<rect x="{(x+1)*U}" y="{(y+1)*U}" width="{(w-2)*U}" height="{(h-2)*U}" fill="{t["screen"]}"/>')
    # LCD scanlines
    scan = [(sx, sy) for sy in range(y+2, y+h-1, 3) for sx in range(x+1, x+w-1)]
    A(f'<path d="{path(scan, U)}" fill="{t["scan"]}"/>')
    # inner bevel, top and left
    bev = ([(sx, y+1) for sx in range(x+1, x+w-1)] +
           [(x+1, sy) for sy in range(y+1, y+h-1)])
    A(f'<path d="{path(bev, U)}" fill="{t["bevel"]}"/>')

def titlebar(x, y, w, label, t, o, right=None, verified=False):
    A = o.append
    A(f'<rect x="{x*U}" y="{y*U}" width="{w*U}" height="{11*U}" fill="{t["bar"]}"/>')
    A(f'<path d="{path([(i, y) for i in range(x, x+w)], U)}" fill="{t["edge"]}"/>')
    A(f'<path d="{path(px(label, x+3, y+2), U)}" fill="{t["bartx"]}"/>')
    if verified: A(seal(x + w - 14, y + 1, U))
    elif right: A(f'<path d="{path(px(right, x+w-3-len(right)*6, y+2), U)}" fill="{t["bartx"]}"/>')

# ---------------- party entry ----------------
def entry(no, name, types, desc, foot, sp, lang, since, verified, theme, minlines=0, arrow_on=True):
    t = TH[theme]
    bx, by, bw = 8, 8, W - 16
    ctop = by + 11 + 5
    SB = 32
    rx, rw = bx + SB + 7, bw - (SB + 7)
    lines = wrap(desc, (rw - 14) // 6)
    body_h = max(len(lines), minlines) * 10
    tb_top = ctop + 15
    left_bottom = ctop + SB + 22
    bottom = max(left_bottom, tb_top + body_h + 8)
    fy = bottom + 6
    H = fy + 8 + 8
    o = []; A = o.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*U}" height="{H*U}" '
      f'viewBox="0 0 {W*U} {H*U}" role="img" aria-label="{no} {name}: {desc} {foot}">')
    frame(H, t, o); screen(5, 5, W-10, H-10, t, o)
    titlebar(bx, by, bw, f"{no}  {name}", t, o, verified=verified)
    A(f'<rect x="{bx*U}" y="{ctop*U}" width="{SB*U}" height="{SB*U}" rx="{2*U}" '
      f'fill="{t["well"]}" stroke="{t["edge"]}" stroke-width="{U}"/>')
    A(draw_sprite(sp, bx + (SB-26)//2, ctop + (SB-26)//2, U))
    for k, txt in enumerate((lang, since)):
        w = len(txt)*6 - 1
        A(f'<path d="{path(px(txt, bx + (SB - w)//2, ctop+SB+3+k*10), U)}" fill="{t["dim"]}"/>')
    cx = rx
    for ty in types:
        cw = len(ty)*6 + 7
        A(f'<rect x="{cx*U}" y="{ctop*U}" width="{cw*U}" height="{11*U}" rx="{2*U}" fill="{TYPES[ty]}"/>')
        A(f'<path d="{path(px(ty, cx+4, ctop+2), U)}" fill="{"#1A1A1A" if ty in DARKTEXT else "#FFFFFF"}"/>')
        cx += cw + 4
    A(f'<rect x="{rx*U}" y="{tb_top*U}" width="{rw*U}" height="{(body_h+8)*U}" rx="{2*U}" '
      f'fill="{t["box"]}" stroke="{t["edge"]}" stroke-width="{U}"/>')
    for i, ln in enumerate(lines):
        A(f'<path d="{path(px(ln, rx+6, tb_top+5+i*10), U)}" fill="{t["ink"]}"/>')
    if arrow_on: A(arrow(rx + rw - 10, tb_top + body_h + 2, U, t["edge"]))
    A(f'<path d="{path(px(foot, bx+2, fy), U)}" fill="{t["dim"]}"/>')
    A('</svg>')
    return "".join(o)

# ---------------- trainer card with device chrome ----------------
def trainer(theme):
    t = TH[theme]
    rows = [("NAME", "Dheirav Prakash"), ("ID No.", "63734286"),
            ("LOCATION", "Chennai, India"), ("CODEX", "16 repos"),
            ("VERIFIED", "3 results")]
    CH_H = 30
    sy = CH_H
    sh = 14 + len(rows)*11 + 12
    H = sy + sh + 6
    o = []; A = o.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*U}" height="{H*U}" '
      f'viewBox="0 0 {W*U} {H*U}" role="img" aria-label="ID card. Dheirav Prakash, '
      f'Chennai India, 16 repos, 3 verified results.">')
    frame(H, t, o)
    # lens
    for r, c in ((11, '#2B3A67'), (9, '#4F7BD6'), (7, '#7FA8EC')):
        A(f'<path d="{path([(x,y) for y in range(0,30) for x in range(4,32) if (x-18)**2+(y-15)**2 <= r*r], U)}" fill="{c}"/>')
    A(f'<path d="{path([(x,y) for y in range(8,13) for x in range(12,17) if (x-14)**2+(y-10)**2 <= 4], U)}" fill="#DCEAFF"/>')
    # LEDs
    for i, c in enumerate(('#D6413B', '#E5C04A', '#5FA35A')):
        cx = 40 + i*11
        A(f'<path d="{path([(x,y) for y in range(6,16) for x in range(cx-4,cx+5) if (x-cx)**2+(y-11)**2 <= 9], U)}" fill="{c}"/>')
    A(f'<path d="{path(px("CODEX", 78, 8), U)}" fill="{t["shell_lo"]}"/>')
    A(f'<rect x="{(W-9)*U}" y="{2*U}" width="{3*U}" height="{(H-5)*U}" fill="{t["shell_lo"]}"/>')
    screen(5, sy, W-10, sh, t, o)
    bx, by, bw = 8, sy+3, W-16
    titlebar(bx, by, bw, "ID CARD", t, o)
    AW = 34
    ax, ay = bx+1, by+15
    A(f'<rect x="{ax*U}" y="{ay*U}" width="{AW*U}" height="{AW*U}" rx="{2*U}" '
      f'fill="{t["well"]}" stroke="{t["edge"]}" stroke-width="{U}"/>')
    A(draw_sprite('me', ax + (AW-26)//2, ay + (AW-26)//2, U))
    fx, y = ax + AW + 8, by + 16
    for k, v in rows:
        A(f'<path d="{path(px(k, fx, y), U)}" fill="{t["dim"]}"/>')
        A(f'<path d="{path(px(v, fx+52, y), U)}" fill="{t["ink"]}"/>')
        y += 11
    A('</svg>')
    return "".join(o)

# ---------------- PC storage box ----------------
def archive(items, theme):
    t = TH[theme]
    COLS, TW, TH_, GAP = 4, 60, 34, 5
    rows = (len(items) + COLS - 1) // COLS
    bx, by, bw = 8, 8, W - 16
    gtop = by + 11 + 6
    sh = 14 + 6 + rows*(TH_+GAP) + 4
    H = 5 + sh + 5
    o = []; A = o.append
    labels = ", ".join(i[0] for i in items)
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*U}" height="{H*U}" '
      f'viewBox="0 0 {W*U} {H*U}" role="img" aria-label="Archive: {labels}">')
    frame(H, t, o); screen(5, 5, W-10, sh, t, o)
    titlebar(bx, by, bw, "ARCHIVE", t, o, right="7 repos")
    gx0 = bx + (bw - (COLS*TW + (COLS-1)*GAP)) // 2
    for i, (label, sp) in enumerate(items):
        r, c = divmod(i, COLS)
        x = gx0 + c*(TW+GAP); y = gtop + r*(TH_+GAP)
        A(f'<rect x="{x*U}" y="{y*U}" width="{TW*U}" height="{TH_*U}" rx="{2*U}" '
          f'fill="{t["tile"]}" stroke="{t["edge"]}" stroke-width="{U}"/>')
        A(small_sprite(sp, x + (TW-13)//2, y + 3, U))
        A(f'<path d="{path(px(label, x + (TW - (len(label)*6-1))//2, y + TH_ - 11), U)}" fill="{t["ink"]}"/>')
    A('</svg>')
    return "".join(o)


def half(g):
    """26x26 -> 13x13, majority of each 2x2 block"""
    out = [['.']*13 for _ in range(13)]
    for y in range(13):
        for x in range(13):
            cells = [g[2*y+dy][2*x+dx] for dy in (0,1) for dx in (0,1)]
            solid = [c for c in cells if c != '.']
            if solid:
                out[y][x] = max(set(solid), key=solid.count)
    return out

def small_sprite(sp, ox, oy, u):
    g, pal = (AVATAR if sp == 'me' else SPRITES[sp]())
    g = half(g)
    grp = {}
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != '.': grp.setdefault(c, []).append((ox+x, oy+y))
    order = [k for k in grp if k != 'K'] + (['K'] if 'K' in grp else [])
    return "".join(f'<path d="{path(grp[c], u)}" fill="{pal[c]}"/>' for c in order)

def listscreen(theme):
    t = TH[theme]
    bx, by, bw = 8, 8, W - 16
    RH = 16
    top = by + 11 + 4
    sh = 14 + len(PARTY)*RH + 8
    H = 5 + sh + 5
    o = []; A = o.append
    names = ", ".join(e[1] for e in PARTY)
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*U}" height="{H*U}" '
      f'viewBox="0 0 {W*U} {H*U}" role="img" aria-label="Codex index: {names}">')
    frame(H, t, o); screen(5, 5, W-10, sh, t, o)
    titlebar(bx, by, bw, "CODEX", t, o, right="6 entries")
    for i, e in enumerate(PARTY):
        no, name, tags, _d, _f, sp, lang, _s, ver = e
        y = top + i*RH
        if i % 2 == 0:
            A(f'<rect x="{bx*U}" y="{y*U}" width="{bw*U}" height="{RH*U}" fill="{t["tile"]}"/>')
        A(f'<path d="{path(px(no.split(".")[1], bx+4, y+4), U)}" fill="{t["dim"]}"/>')
        A(small_sprite(sp, bx+26, y+1, U))
        A(f'<path d="{path(px(name, bx+44, y+4), U)}" fill="{t["ink"]}"/>')
        tg = tags[0]
        cw = len(tg)*6 + 5
        cx = bx + bw - 19 - cw
        A(f'<rect x="{cx*U}" y="{(y+3)*U}" width="{cw*U}" height="{10*U}" rx="{2*U}" fill="{TYPES[tg]}"/>')
        A(f'<path d="{path(px(tg, cx+3, y+4), U)}" fill="#FFFFFF"/>')
        if ver: A(seal(bx + bw - 13, y + 3, U))
    A('</svg>')
    return "".join(o)

PARTY = [
 ("No.001","ChessBot",["SEARCH","ENGINE"],
  "A UCI chess engine written from scratch. Bitboards, alpha-beta, transposition table, null-move pruning. Every heuristic won an SPRT match before it shipped.",
  "LICHESS 2100+ RAPID - VERIFIED", 1, "C++", "2025", True),
 ("No.002","UkuleleTabsMaker",["VISION","MUSIC"],
  "Reads ukulele tabs off a YouTube video and prints a playable sheet. Computer vision over the notation on screen, not the audio.",
  "99.7% RECALL / 100% PRECISION, 340 NOTES", 2, "Python", "2026", True),
 ("No.003","NashForge",["SOLVER","RESEARCH"],
  "A CFR solver for heads-up no-limit Hold'em. An earlier training pipeline here published results. I audited it, found the fitness scored the wrong player, and withdrew them.",
  "REPRODUCES KUHN -1/18 - EXACT LEDUC", 3, "Python", "2026", True),
 ("No.004","DeepFakeDetector",["FORENSICS","VISION"],
  "Sorts images into real, AI-generated or AI-edited. The forensic parts I expected to carry it bought under 0.2% over a plain baseline. All 26 runs are committed.",
  "89.5% ON 77,865 IMAGES / 20 SOURCES", 4, "Python", "2026", False),
 ("No.005","Luna",["OFFLINE","MOBILE"],
  "An Android cycle tracker with no INTERNET permission, and there never will be one. Predicts a window instead of inventing a single date.",
  "OFFLINE - NO ACCOUNT - NO TELEMETRY", 5, "Kotlin", "2026", False),
 ("No.006","NewsLetterScrapper",["PIPELINE","LLM"],
  "Clusters 38 RSS feeds into stories and writes the analysis with a local LLM. Nothing ever leaves the machine.",
  "SELF-HOSTED - NO EXTERNAL AI APIS", 6, "Python", "2026", False),
]
BOX = [("HelperBoi",8),("Dedupe",7),("Audio",9),
       ("LabEval",10),("Attend",11),("SaleSnipe",12),("Carbon",13)]

MAXL = max(len(wrap(e[3], (W - 16 - 39 - 14) // 6)) for e in PARTY)
here = os.path.dirname(os.path.abspath(__file__))
set_avatar(os.path.join(here, "avatar-src.png"))
# Single-theme output. TH still carries the light palette, so flipping this
# back to a themed build is a one-line change.
th = "dark"
open(os.path.join(here, "trainer.svg"), "w").write(trainer(th))
open(os.path.join(here, "archive.svg"), "w").write(archive(BOX, th))
open(os.path.join(here, "index.svg"), "w").write(listscreen(th))
for e in PARTY:
    n = e[0].split('.')[1]
    open(os.path.join(here, f"entry-{n}.svg"), "w").write(entry(*e, th, minlines=MAXL))
print("generated")
