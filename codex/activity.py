#!/usr/bin/env python3
"""Fetch the contribution calendar and write activity.json.

Separate from sync.py because the two answer different questions, and separate
from gen.py because gen.py must stay offline and deterministic: it renders from
a committed file, so the panels can always be rebuilt byte for byte without a
network.

The source is the public HTML at github.com/users/<owner>/contributions, which
needs no token. That keeps the property the rest of this directory relies on --
the workflow's built-in token is enough, no PAT anywhere.

Scraping HTML is the weak point, so every assumption is asserted rather than
trusted. The first version of this read each cell's position from its index in
the document and drew a scrambled year that looked entirely plausible, because
the markup is row-major: every Sunday, then every Monday, and so on. Position
now comes from the dates themselves, and a layout that does not match what the
panel expects aborts without writing, leaving the previous panel in place. A
wrong picture is worse than a stale one.

    python3 activity.py            # rewrite activity.json
    python3 activity.py --check    # exit 1 if it would change anything
"""
import datetime
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "codex.json")
OUT = os.path.join(HERE, "activity.json")
URL = "https://github.com/users/{owner}/contributions"


def fetch(owner):
    req = urllib.request.Request(URL.format(owner=owner),
                                 headers={"User-Agent": "codex-activity"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    """{start, levels, total, active} or raise. Every assumption is checked."""
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?data-level="(\d)"', html)
    if len(cells) < 300:
        raise ValueError(f"only {len(cells)} day cells found; the markup has changed")

    seen = {}
    for date, lvl in cells:
        if date in seen and seen[date] != lvl:
            raise ValueError(f"{date} appears twice with different levels")
        seen[date] = lvl
    days = sorted(seen.items())

    start = datetime.date.fromisoformat(days[0][0])
    end = datetime.date.fromisoformat(days[-1][0])
    if start.weekday() != 6:
        raise ValueError(f"the calendar starts on a {start:%A}, not a Sunday")
    span = (end - start).days + 1
    if span != len(days):
        raise ValueError(f"{len(days)} cells span {span} days; the range has holes")
    if not 52 <= span / 7 <= 54:
        raise ValueError(f"{span} days is not about a year")

    levels = "".join(l for _, l in days)
    if set(levels) - set("01234"):
        raise ValueError("a cell carries a level outside 0-4")

    m = re.search(r"([\d,]+)\s+contribution", html)
    total = int(m.group(1).replace(",", "")) if m else None
    return {
        "start": days[0][0],
        "levels": levels,
        "total": total,
        "active": sum(1 for c in levels if c != "0"),
    }


def main():
    check = "--check" in sys.argv
    owner = json.load(open(DATA))["owner"]
    try:
        new = parse(fetch(owner))
    except Exception as exc:
        print(f"refusing to write activity.json: {exc}", file=sys.stderr)
        return 2

    old = json.load(open(OUT)) if os.path.exists(OUT) else None
    if old == new:
        print("activity.json already current")
        return 0
    if check:
        print("activity.json is OUT OF DATE")
        return 1
    with open(OUT, "w") as f:
        json.dump(new, f, indent=2)
        f.write("\n")
    print(f"activity.json: {new['total']} contributions, {new['active']} active "
          f"days, {len(new['levels'])} days from {new['start']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
