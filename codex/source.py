#!/usr/bin/env python3
"""Measure what the repos are written in, and write source.json.

Separate from sync.py because it answers a different question, and separate from
codex.json because byte counts move on every push: keeping them here means
codex.json still changes only when a repo or a card does, which is what stale.py
dates a card from.

Only what the panel draws is stored, already rounded. Raw byte counts would move
on every push and file a commit for a bar nobody could see change, so the
resolution of the stored number is what decides how often this commits. A
language folds into Other unless it rounds to at least 2 percent, which keeps
build files out: of the 16 languages GitHub detects here, seven are Makefile,
CSS, PowerShell, Dockerfile, CMake, Batchfile and Mako, together a quarter of
one percent.

    python3 source.py            # rewrite source.json
    python3 source.py --check    # exit 1 if it would change anything
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "codex.json")
OUT = os.path.join(HERE, "source.json")
API = "https://api.github.com/repos/{owner}/{repo}/languages"
FLOOR = 2          # percent, after rounding, to earn a row


def fetch(owner, repo):
    req = urllib.request.Request(API.format(owner=owner, repo=repo), headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "codex-source",
    })
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    check = "--check" in sys.argv
    data = json.load(open(DATA))
    repos = [e["repo"] for e in data["dex"]]

    totals, failed = {}, []
    for repo in repos:
        try:
            for lang, n in fetch(data["owner"], repo).items():
                if isinstance(n, int):
                    totals[lang] = totals.get(lang, 0) + n
        except Exception as exc:
            failed.append(f"{repo}: {exc}")

    if failed:
        print("refusing to write source.json, some repos did not answer:",
              file=sys.stderr)
        for f in failed:
            print(f"  {f}", file=sys.stderr)
        return 2
    grand = sum(totals.values())
    if grand <= 0:
        print("refusing to write source.json: no bytes counted", file=sys.stderr)
        return 2

    rows = []
    for lang, n in sorted(totals.items(), key=lambda kv: -kv[1]):
        pct = round(100 * n / grand)
        if pct >= FLOOR:
            rows.append([lang, pct])
    # Other is the remainder rather than its own sum, so the column always
    # totals 100 even after each row was rounded on its own.
    rows.append(["Other", 100 - sum(p for _, p in rows)])

    new = {"total_mb": round(grand / 1e6), "languages": len(totals), "rows": rows}
    old = json.load(open(OUT)) if os.path.exists(OUT) else None
    if old == new:
        print("source.json already current")
        return 0
    if check:
        print("source.json is OUT OF DATE")
        return 1
    with open(OUT, "w") as f:
        json.dump(new, f, indent=2)
        f.write("\n")
    print(f"source.json: {new['total_mb']} MB, {len(totals)} languages detected, "
          f"{len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
