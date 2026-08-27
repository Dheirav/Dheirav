# codex

The panels on the profile page. Everything here is generated, not hand-drawn.

- `codex.json` — the data. **This is the file you edit.**
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

## The shape of codex.json

- **`dex`** — one entry per public repo, holding everything a card needs: `no`,
  `repo`, `tags`, `desc`, `foot`, `sprite`, `lang`, `since`, `verified`. Every
  repo lives here whether or not it is on display.
- **`party`** — the repos currently shown on the profile, as a list of names in
  display order. This is the pin list, and nothing else.
- **`archive`** — derived: everything public that is not pinned. Order is kept
  so the tiles do not shuffle.
- **`labels`** — archive tile captions. Tiles fit **10 characters**, and
  `sync.py` truncates bluntly (`rust_ray_tracer` → `RustRayTra`).
- **`counts`** — derived. Only `repos` and `verified` are read, by the ID card.

Card data lives in `dex` and nowhere else, so switching what the profile shows
never moves prose between places.

## How it stays current

A repo that is deleted or flipped to private stops appearing in the public
listing, so one unauthenticated call covers both — no PAT needed, and the
workflow's built-in token is enough.

Curated content is never invented. `sync.py` fills in only what GitHub states
as fact — the language and the year the repo was created — and scaffolds a new
entry with `tags`, `desc` and `foot` empty. `gen.py` declines to draw a card
until those are written, and prints what is still waiting.

Entry numbers are identity. A `no` is assigned once, when the repo is first
seen, and never moves — pinning and unpinning do not touch it. When a repo goes
for good the number retires with it and the sequence keeps the hole, so
`No.003` always means the same project. `gen.py` deletes the orphaned
`entry-00N.svg` so a panel describing a now-private repo cannot be fetched by
raw URL.

## Switching the party

Reorder or replace names in `party`, then run `sync.py` and `gen.py`.

Cards for unpinned repos are generated and committed too, so a swap is a
one-line edit rather than a card written from scratch. Only pinned entries
reach the profile `README.md` and `index.svg`; the rest sit in `codex/` waiting.

Run `sync.py` after a swap, not just `gen.py` — `sync.py` owns the `archive`
list, and until it re-runs a newly pinned repo is still in it. `gen.py` and
`readme.py` both drop pinned repos from the archive defensively so the panel
never shows one twice, but the list itself is only correct after a sync.

Pinning a repo whose prose is not written yet is not fatal: `sync.py` warns,
`gen.py` skips it, and `readme.py` leaves it out rather than linking a card
that does not exist.

## Adding a repo

Nothing to do — the next sync files it in the archive and scaffolds a dex entry
with the generic sprite (the tan carton with a question mark). To finish it off:

1. Draw a sprite in `sprites.py` and register it in the `SPRITES` dict.
2. Point the entry's `sprite` at that key.
3. Set a `labels` entry if the auto-shortened name is ugly.
4. Write `tags`, `desc` and `foot` to give it a card. Tags want a colour in
   `gen.py`'s `TYPES`; one without falls back to a dull slate rather than
   breaking the build.

Sprites are drawn at 26×26, but the archive tile renders them through
`gen.half()` at **13×13**. Check both — fine detail that reads at full size
dissolves in the majority vote. `brass()` carries a note about this.

`renderable()` — the rule deciding whether an entry has enough written to draw —
is duplicated in `sync.py`, `gen.py` and `readme.py`. It is three lines, and
`gen.py` builds everything at import time, so importing it to share would run
the whole build as a side effect.

No webfont and no external assets: every glyph is drawn as rectangles, so the
panels render identically anywhere and stay sharp at any size.
