# codex

The panels on the profile page. Everything here is generated, not hand-drawn.

- `gen.py` — layout, the 5×8 bitmap font, and the entry text. Edit `PARTY` or `BOX` and rerun.
- `sprites.py` — the sprites, built from primitives (discs, boxes, tapers) with an automatic
  outline pass. Also pixelates `avatar-src.png` for the ID card.
- `animate.py` — rasterises the same output into `codex-{light,dark}.gif`.

```bash
python3 gen.py       # all SVG panels, both themes
python3 animate.py   # the animated screen
```

No webfont and no external assets: every glyph is drawn as rectangles, so the panels render
identically anywhere and stay sharp at any size.
