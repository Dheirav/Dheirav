#!/usr/bin/env python3
"""Reconcile codex.json against what GitHub actually shows publicly.

A repo that is deleted or flipped to private simply stops appearing in the
public listing, so one unauthenticated call covers both removal cases and the
addition case. That is why this needs no PAT: it only ever asks the question a
visitor to the profile could ask.

Curated content is never invented here. Featured (party) entries carry
hand-written prose, so this only ever *drops* one whose repo has gone; adding a
repo to the party stays a manual edit. New repos land in the archive with the
generic sprite until someone draws them one.

    python3 sync.py            # rewrite codex.json
    python3 sync.py --check    # exit 1 if it would change anything, write nothing
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "codex.json")
API = "https://api.github.com/users/{owner}/repos?per_page=100&type=owner"
MAXLABEL = 10  # 60px tile / 6px glyph advance


def fetch_public(owner):
    """Public, non-fork, non-archived repos. Paginated defensively."""
    names, url = [], API.format(owner=owner)
    while url:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "codex-sync",
        })
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", f"Bearer {tok}")
        with urllib.request.urlopen(req, timeout=30) as r:
            batch = json.load(r)
            link = r.headers.get("Link", "")
        for repo in batch:
            if repo.get("fork") or repo.get("archived") or repo.get("private"):
                continue
            names.append(repo["name"])
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part[part.index("<") + 1:part.index(">")]
    return names


def shorten(name, taken):
    """Fit a repo name into an archive tile without colliding with another."""
    base = name.replace("_", " ").replace("-", " ")
    words = [w for w in base.split() if w]
    for cand in (
        "".join(w[0].upper() + w[1:] for w in words),   # AudioTranscriber
        words[0] if words else name,                    # first word
        "".join(w[0].upper() for w in words),           # initials
    ):
        cand = cand[:MAXLABEL]
        if cand and cand not in taken:
            return cand
    stem = (words[0] if words else name)[:MAXLABEL - 1]
    for i in range(2, 10):
        cand = f"{stem}{i}"
        if cand not in taken:
            return cand
    return name[:MAXLABEL]


def main():
    check = "--check" in sys.argv
    data = json.load(open(DATA))
    before = json.dumps(data, indent=2, sort_keys=True)

    live = set(fetch_public(data["owner"]))
    if not live:
        print("refusing to sync: the API returned no repos at all", file=sys.stderr)
        return 2
    exclude = set(data.get("exclude", []))

    # 1. Drop featured entries whose repo is gone. Numbers are identity, so the
    #    survivors keep theirs and the sequence is allowed to have holes.
    kept, dropped = [], []
    for e in data["party"]:
        (kept if e["repo"] in live else dropped).append(e)
    data["party"] = kept
    for e in dropped:
        print(f"  - party  {e['no']} {e['repo']} (no longer public)")
    retired = data.setdefault("retired", [])
    for e in dropped:
        if e["repo"] not in retired:
            retired.append(e["repo"])

    # 2. Archive = everything public that is not featured and not excluded.
    featured = {e["repo"] for e in data["party"]}
    want = [r for r in live if r not in featured and r not in exclude]
    old = [r for r in data.get("archive", []) if r in want]   # keep existing order
    new = sorted(r for r in want if r not in old)
    for r in new:
        print(f"  + archive {r}")
    for r in data.get("archive", []):
        if r not in want:
            print(f"  - archive {r} (no longer public)")
    data["archive"] = old + new

    # 3. Give every archive repo a label, without clobbering hand-set ones.
    labels = data.setdefault("labels", {})
    taken = {labels[r] for r in data["archive"] if r in labels}
    for r in data["archive"]:
        if r not in labels:
            labels[r] = shorten(r, taken)
            taken.add(labels[r])
            print(f"    label {r} -> {labels[r]}")
    for r in list(labels):
        if r not in data["archive"] and r not in featured:
            del labels[r]

    sprites = data.setdefault("sprites", {})
    for r in list(sprites):
        if r not in data["archive"] and r not in featured:
            del sprites[r]
    for r in data["archive"]:
        if r not in sprites:
            print(f"    sprite {r} -> 0 (generic, draw one in sprites.py to replace)")

    data["counts"] = {
        "repos": len(live - exclude),
        "verified": sum(1 for e in data["party"] if e["verified"]),
        "entries": len(data["party"]),
        "archive": len(data["archive"]),
    }

    after = json.dumps(data, indent=2, sort_keys=True)
    if before == after:
        print("codex.json already in sync")
        return 0
    if check:
        print("codex.json is OUT OF SYNC")
        return 1
    with open(DATA, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("codex.json updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
