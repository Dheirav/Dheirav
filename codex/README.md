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
- `source.py` — measures what the repos are written in, into `source.json`.
- `stale.py` — flags cards whose repo has moved since the prose was written.

```bash
python3 sync.py      # reconcile with GitHub  (--check to test without writing)
python3 gen.py       # all SVG panels
python3 readme.py    # the profile README
python3 animate.py   # the animated screen
python3 stale.py     # which cards are worth re-reading
python3 source.py    # what the repos are written in
```

`.github/workflows/codex.yml` runs all six daily, and on demand via *Actions →
codex → Run workflow*. It commits only when something actually changed.

`sync.py`, `readme.py`, `stale.py` and `source.py` are stdlib only. `gen.py` and `animate.py` both need
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

## The source panel

`source.py` asks the API what each repo is written in, one call a repo, and
writes `source.json`. `gen.py` draws the bars from that file, so it still
reaches no network and every panel is rebuildable offline.

Two decisions in it are worth keeping:

**It stores only what the panel draws, already rounded.** Byte counts move on
every push, so storing them raw would file a commit for a bar nobody could see
change. The resolution of the stored number is what sets how often this
commits, which is the same reason a card's footer should not quote a figure
that moves.

**A language needs to round to 2 percent to earn a row.** Of the 16 languages
GitHub detects here, seven are Makefile, CSS, PowerShell, Dockerfile, CMake,
Batchfile and Mako, together a quarter of one percent. Counting those as
languages you build in would be padding a number. Everything under the floor
folds into `Other`, which is computed as the remainder so the column totals 100
even though each row was rounded on its own.

The bars are one hue because each row already carries its name and its number,
so colour would be decoration. A seven-hue set from the tag palette was tried
first and failed validation, two of its colours 5.8 apart where 15 is the floor
for a pair being distinguishable with full colour vision.

`source.py` writes nothing unless every repo answered, so a half-counted total
cannot reach the panel, and the workflow step is `continue-on-error`: a stale
breakdown is better than a wrong one.

## When a card goes stale

`sync.py` reconciles which repos exist. Nothing reconciles whether a card's
prose is still *true*, and that is the failure this repo is most exposed to: a
card can start lying while every job stays green. It has happened — No.015 spent
eight days advertising a bot that had been retired for losing.

`stale.py` is the cheap half of that. It dates a card from the history of
`codex.json` — the commit that introduced the `desc` and `foot` it carries today
— and compares that against the repo's last push:

```
  No.015  BrassBot   card 2026-09-04 23:06  repo 2026-09-04 23:06  ok
  No.003  NashForge  card 2026-08-20 14:25  repo 2026-09-04 02:07  repo moved 14d later
```

It never reads the prose and never says a card is wrong. Most pushes touch
nothing a card claims. What it gives you is a short list worth re-reading.

That list only stays short if you can answer it, so re-reading a card and
finding it still true is recordable:

```bash
python3 stale.py --ack NashForge     # or --ack-all for everything flagged
```

which stamps `checked` on the entry and settles it until the next push. Without
that the report would flag most cards most days and you would learn to skip it.

The date comes from git rather than a stored field so it cannot drift from the
prose it describes. That needs real history: the workflow checks out with
`fetch-depth: 0`, because at the default depth of 1 every card looks as though
it was written at the only commit present.

The workflow runs it for report only — findings go to the run summary and to
warning annotations, and never fail the build. A card going stale is a prompt to
re-read a sentence, not a broken build, and a daily red cross would only teach
us to ignore it.

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
