# codex

The panels on the profile page. Everything here is generated, not hand-drawn.

- `codex.json` — the data. Featured entries, the archive list, label and sprite
  overrides, and the derived counts. **This is the file you edit.**
- `sync.py` — reconciles `codex.json` against the repos GitHub actually shows
  publicly. Adds new ones, drops deleted or newly-private ones.
- `gen.py` — layout and the 5×8 bitmap font. Reads `codex.json`.
- `sprites.py` — the sprites, built from primitives (discs, boxes, tapers) with
  an automatic outline pass. Also pixelates `avatar-src.png` for the ID card.
- `readme.py` — rewrites the profile `README.md` from the same data.
- `animate.py` — rasterises the entries into `codex.gif`.

```bash
python3 sync.py      # reconcile with GitHub  (--check to test without writing)
python3 gen.py       # all SVG panels
python3 readme.py    # the profile README
python3 animate.py   # the animated screen
```

`.github/workflows/codex.yml` runs all four daily, and on demand via *Actions →
codex → Run workflow*. It commits only when something actually changed.

`sync.py` and `readme.py` are stdlib only. `gen.py` and `animate.py` both need
Pillow — `gen.py` because `sprites.avatar_sprite()` pixelates `avatar-src.png`
for the ID card, which is easy to miss since nothing at the top of the file
imports it.

## How it stays current

A repo that is deleted or flipped to private stops appearing in the public
listing, so one unauthenticated call covers both — no PAT needed, and the
workflow's built-in token is enough.

Curated content is never invented. A **featured** entry carries hand-written
prose, so `sync.py` only ever *drops* one whose repo has gone; promoting a repo
to featured stays a manual edit to `codex.json`. New repos land in the
**archive** automatically.

Entry numbers are identity. When a featured entry goes, the survivors keep their
numbers and the sequence is left with a hole — `No.003` always means the same
project. `gen.py` deletes the orphaned `entry-00N.svg` so a panel describing a
now-private repo cannot be fetched by raw URL.

## Adding a repo

Nothing to do — the next sync files it in the archive with the generic sprite
(the tan carton with a question mark). To finish it off:

1. Draw a sprite in `sprites.py` and register it in the `SPRITES` dict.
2. Point `codex.json`'s `sprites` at that key.
3. Set a `labels` entry if the auto-shortened name is ugly — tiles fit **10
   characters**, and `sync.py` truncates bluntly (`rust_ray_tracer` →
   `RustRayTra`).

To feature it instead, add an object to `party` with the next free `No.00N` and
write the prose yourself.

No webfont and no external assets: every glyph is drawn as rectangles, so the
panels render identically anywhere and stay sharp at any size.
