"""24x24-ish pixel sprites built from primitives, with an automatic outline pass."""
N = 26
def blank(): return [['.']*N for _ in range(N)]
def disc(g, cx, cy, r, ch):
    for y in range(N):
        for x in range(N):
            if (x-cx)**2 + (y-cy)**2 <= r*r: g[y][x] = ch
def erase(g, cx, cy, r):
    for y in range(N):
        for x in range(N):
            if (x-cx)**2 + (y-cy)**2 <= r*r: g[y][x] = '.'
def box(g, x0, y0, x1, y1, ch):
    for y in range(max(0,y0), min(N,y1+1)):
        for x in range(max(0,x0), min(N,x1+1)): g[y][x] = ch
def tri(g, cx, ytop, ybot, wtop, wbot, ch):
    n = ybot - ytop
    for i in range(n+1):
        w = wtop + (wbot-wtop)*i//max(1,n)
        box(g, cx-w//2, ytop+i, cx+w//2, ytop+i, ch)
def outline(g, ch='K'):
    src = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if src[y][x] != '.': continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < N and 0 <= ny < N and src[ny][nx] not in ('.', ch):
                    g[y][x] = ch; break

def chess():
    g = blank()
    disc(g, 13, 6, 3, 'W')                 # head
    box(g, 11, 9, 15, 11, 'W')             # neck
    box(g, 9, 11, 17, 12, 'W')             # collar
    tri(g, 13, 13, 19, 5, 13, 'W')         # body
    box(g, 7, 20, 19, 21, 'S')             # base
    box(g, 11, 10, 12, 11, 'S')
    outline(g)
    return g, {'W':'#F2F2F5','S':'#9AA3B8','K':'#1B2233'}

def uke():
    g = blank()
    disc(g, 12, 17, 6, 'B')                # lower bout
    disc(g, 12, 11, 4, 'B')                # upper bout
    box(g, 11, 2, 13, 9, 'N')              # neck
    box(g, 10, 1, 14, 3, 'H')              # headstock
    disc(g, 12, 16, 2, 'K')                # sound hole
    for x in (11, 12, 13): box(g, x, 4, x, 20, 'S')
    outline(g)
    return g, {'B':'#D9A05B','N':'#8A5A2B','H':'#6E4520','S':'#F3E4C8','K':'#2A1B0E'}

def chip():
    g = blank()
    disc(g, 12, 12, 9, 'R')
    for a in ((12,3),(12,21),(3,12),(21,12)):
        box(g, a[0]-2, a[1]-1, a[0]+2, a[1]+1, 'W')
    box(g, 4, 11, 8, 13, 'W'); box(g, 16, 11, 20, 13, 'W')
    disc(g, 12, 12, 5, 'W'); disc(g, 12, 12, 4, 'R')
    outline(g)
    return g, {'R':'#C0392B','W':'#F5F5F0','K':'#2B1512'}

def eye():
    g = blank()
    tri(g, 12, 6, 12, 3, 21, 'W')          # upper lid
    tri(g, 12, 12, 18, 21, 3, 'W')         # lower lid
    disc(g, 12, 12, 5, 'I')
    disc(g, 12, 12, 2, 'K')
    box(g, 9, 9, 10, 10, 'W')              # glint
    outline(g)
    return g, {'W':'#F2F4FA','I':'#5B7BC9','K':'#14161F'}

def moon():
    g = blank()
    disc(g, 11, 13, 9, 'M')
    erase(g, 17, 10, 8)
    disc(g, 8, 10, 1, 'C'); disc(g, 7, 16, 1, 'C')
    outline(g)
    return g, {'M':'#E8E2F5','C':'#B9AEDC','K':'#2A2340'}

def news():
    g = blank()
    box(g, 3, 5, 21, 20, 'P')
    box(g, 5, 7, 13, 11, 'D')
    for y in (13, 15, 17): box(g, 5, y, 19, y, 'D')
    for y in (8, 10): box(g, 15, y, 19, y, 'D')
    box(g, 21, 8, 22, 20, 'S')
    outline(g)
    return g, {'P':'#F4F1E4','D':'#4A5568','S':'#C9C3AE','K':'#20242E'}

def photos():
    g = blank()
    box(g, 3, 4, 15, 16, 'P'); box(g, 5, 6, 13, 12, 'A')
    box(g, 10, 9, 22, 21, 'P'); box(g, 12, 11, 20, 17, 'B')
    outline(g)
    return g, {'P':'#F6F4EC','A':'#7FA8D8','B':'#8FC08A','K':'#23262E'}

SPRITES = {1:chess, 2:uke, 3:chip, 4:eye, 5:moon, 6:news, 7:photos}

# ---------- PC-box sprites (smaller, simpler silhouettes) ----------
def helper():
    g = blank()
    box(g, 6, 6, 19, 17, 'M')              # head
    box(g, 9, 9, 11, 11, 'E'); box(g, 14, 9, 16, 11, 'E')
    box(g, 9, 14, 16, 15, 'E')             # mouth
    box(g, 12, 2, 13, 6, 'A'); disc(g, 12, 2, 2, 'A')
    box(g, 4, 10, 5, 14, 'M'); box(g, 20, 10, 21, 14, 'M')
    outline(g)
    return g, {'M':'#9BB3D4','E':'#2E4A6E','A':'#D96C4A','K':'#1A2436'}

def mic():
    g = blank()
    box(g, 9, 3, 16, 14, 'M'); disc(g, 12, 4, 4, 'M'); disc(g, 12, 13, 4, 'M')
    for y in (6, 8, 10): box(g, 10, y, 15, y, 'D')
    box(g, 6, 13, 7, 16, 'S'); box(g, 18, 13, 19, 16, 'S')
    box(g, 6, 16, 19, 17, 'S'); box(g, 11, 17, 14, 21, 'S')
    box(g, 8, 21, 17, 22, 'S')
    outline(g)
    return g, {'M':'#C6CBD8','D':'#5A6478','S':'#8A93A6','K':'#1D2230'}

def clipboard():
    g = blank()
    box(g, 4, 3, 20, 22, 'B'); box(g, 6, 6, 18, 20, 'P')
    box(g, 9, 1, 15, 5, 'C')
    for y in (9, 12, 15): box(g, 8, y, 16, y, 'D')
    box(g, 8, 17, 12, 18, 'G')
    outline(g)
    return g, {'B':'#8A6A45','P':'#F4F1E4','C':'#B0B7C4','D':'#6B7686','G':'#4FA05A','K':'#22252E'}

def calendar():
    g = blank()
    box(g, 3, 5, 21, 21, 'P'); box(g, 3, 5, 21, 9, 'R')
    box(g, 7, 2, 8, 6, 'D'); box(g, 16, 2, 17, 6, 'D')
    for y in (12, 15, 18):
        for x in (6, 10, 14, 18): box(g, x, y, x+1, y+1, 'D')
    box(g, 13, 14, 14, 15, 'G'); box(g, 15, 13, 16, 14, 'G'); box(g, 16, 12, 17, 13, 'G')
    outline(g)
    return g, {'P':'#F5F2E6','R':'#C4574B','D':'#78829A','G':'#3F9E52','K':'#22252E'}

def tag():
    g = blank()
    for i in range(14): box(g, 4+i, 4+i, 17+i-i, 5+i, 'T')
    box(g, 4, 4, 16, 16, 'T')
    tri(g, 16, 16, 22, 12, 1, 'T')
    disc(g, 8, 8, 2, 'H')
    outline(g)
    return g, {'T':'#D9A33C','H':'#F5F1E2','K':'#2A2214'}

def gauge():
    g = blank()
    disc(g, 12, 14, 9, 'F')
    erase(g, 12, 20, 7)
    box(g, 3, 15, 21, 22, '.')
    disc(g, 12, 14, 6, 'P')
    box(g, 11, 8, 12, 14, 'N'); disc(g, 12, 14, 2, 'N')
    box(g, 4, 18, 20, 20, 'B')
    outline(g)
    return g, {'F':'#5FA35A','P':'#F2F0E2','N':'#C4483C','B':'#7C8796','K':'#1E2A20'}

SPRITES.update({8:helper, 9:mic, 10:clipboard, 11:calendar, 12:tag, 13:gauge})

# ---------- trainer sprite from the real avatar ----------
def avatar_sprite(path_png):
    from PIL import Image
    im = Image.open(path_png).convert('RGB').resize((24, 24), Image.LANCZOS)
    im = im.quantize(colors=6, method=Image.MEDIANCUT).convert('RGB')
    seen, pal, g = {}, {}, blank()
    letters = 'ABCDEFGH'
    for y in range(24):
        for x in range(24):
            rgb = im.getpixel((x, y))
            if rgb not in seen:
                c = letters[len(seen)]
                seen[rgb] = c
                pal[c] = '#%02X%02X%02X' % rgb
            g[y+1][x+1] = seen[rgb]
    outline(g)
    pal['K'] = '#1A1F2B'
    return g, pal


# ---------- generic fallback ----------
def generic():
    """Used for a repo that has no sprite of its own yet. A sealed carton with a
    question mark, so an un-illustrated entry reads as 'not drawn yet' rather
    than as a real sprite."""
    g = blank()
    box(g, 4, 7, 21, 21, 'B')          # carton body
    box(g, 4, 7, 21, 10, 'L')          # lid band
    for y, x0, x1 in ((12, 11, 14), (13, 10, 11), (13, 14, 15), (14, 14, 15),
                      (15, 13, 14), (16, 12, 13), (17, 12, 13), (19, 12, 13)):
        box(g, x0, y, x1, y, 'Q')      # question mark
    outline(g)
    return g, {'B': '#C9A46A', 'L': '#E0BE86', 'Q': '#3A2E1C', 'K': '#241C10'}

SPRITES[0] = generic
