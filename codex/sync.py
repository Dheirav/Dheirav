#!/usr/bin/env python3
"""Reconcile codex.json against what GitHub actually shows publicly.

A repo that is deleted or flipped to private simply stops appearing in the
public listing, so one unauthenticated call covers both removal cases and the
addition case. That is why this needs no PAT: it only ever asks the question a
visitor to the profile could ask.

Every public repo gets a dex entry, so a card exists for all of them and
pinning one is an edit to the `party` list rather than a card written from
scratch. What this fills in is only what GitHub states as fact - the language
and the year the repo was created. `desc`, `foot` and `tags` are curated, so a
new entry is scaffolded with them empty and gen.py declines to render a card
until they are written. Prose is never invented here.

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
    """Public, non-fork, non-archived repos. Paginated defensively.

    Keeps language and creation year as well as the name: both are facts the
    listing already states, and a dex entry needs them to render.
    """
    repos, url = [], API.format(owner=owner)
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
            repos.append({
                "name": repo["name"],
                # null for a repo with no code in it yet
                "lang": repo.get("language") or "",
                "since": (repo.get("created_at") or "")[:4],
            })
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part[part.index("<") + 1:part.index(">")]
    return repos


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


def renderable(e):
    """Whether gen.py will draw a card for this entry.

    Duplicated in gen.py and readme.py rather than shared: those two run as
    scripts, and importing gen.py for one predicate would run the whole build.
    """
    return bool(e.get("desc") and e.get("foot") and e.get("tags"))


def main():
    check = "--check" in sys.argv
    data = json.load(open(DATA))
    before = json.dumps(data, indent=2, sort_keys=True)

    fetched = fetch_public(data["owner"])
    if not fetched:
        print("refusing to sync: the API returned no repos at all", file=sys.stderr)
        return 2
    facts = {r["name"]: r for r in fetched}
    live = set(facts)
    exclude = set(data.get("exclude", []))

    # 1. Drop dex entries whose repo is gone. Numbers are identity, so the
    #    survivors keep theirs and the sequence is allowed to have holes.
    kept, dropped = [], []
    for e in data["dex"]:
        (kept if e["repo"] in live else dropped).append(e)
    data["dex"] = kept
    retired = data.setdefault("retired", [])
    for e in dropped:
        print(f"  - dex    {e['no']} {e['repo']} (no longer public)")
        if e["repo"] not in retired:
            retired.append(e["repo"])

    # A dropped repo cannot stay pinned.
    data["party"] = [r for r in data["party"] if r in live and r not in exclude]

    # 2. Scaffold a dex entry for anything new. Only the facts GitHub states
    #    are filled; the curated fields stay empty until someone writes them.
    known = {e["repo"] for e in data["dex"]}
    nextno = max((int(e["no"].split(".")[1]) for e in data["dex"]), default=0)
    for name in sorted(live - known - exclude):
        nextno += 1
        data["dex"].append({
            "no": f"No.{nextno:03d}", "repo": name, "tags": [], "desc": "",
            "foot": "", "sprite": 0, "lang": facts[name]["lang"],
            "since": facts[name]["since"], "verified": False,
        })
        print(f"  + dex    No.{nextno:03d} {name} (stub - needs tags, desc, foot)")

    # Backfill only what is empty; a hand-set language is never overwritten.
    for e in data["dex"]:
        f = facts.get(e["repo"], {})
        for key in ("lang", "since"):
            if not e.get(key) and f.get(key):
                e[key] = f[key]
                print(f"    {e['repo']} {key} -> {f[key]}")

    # 3. Archive = everything public that is not pinned and not excluded.
    party = set(data["party"])
    want = [r for r in live if r not in party and r not in exclude]
    old = [r for r in data.get("archive", []) if r in want]   # keep existing order
    new = sorted(r for r in want if r not in old)
    for r in new:
        print(f"  + archive {r}")
    for r in data.get("archive", []):
        if r not in want:
            print(f"  - archive {r} (no longer shown here)")
    data["archive"] = old + new

    # 4. Give every archive repo a label, without clobbering hand-set ones.
    labels = data.setdefault("labels", {})
    taken = {labels[r] for r in data["archive"] if r in labels}
    for r in data["archive"]:
        if r not in labels:
            labels[r] = shorten(r, taken)
            taken.add(labels[r])
            print(f"    label {r} -> {labels[r]}")
    for r in list(labels):
        if r not in data["archive"] and r not in party:
            del labels[r]

    # 5. A pinned repo with no prose would leave readme.py pointing at a card
    #    gen.py refuses to draw, so say so loudly rather than shipping a 404.
    by_repo = {e["repo"]: e for e in data["dex"]}
    for r in data["party"]:
        if not renderable(by_repo[r]):
            print(f"  ! {r} is pinned but has no card yet "
                  f"(needs tags, desc, foot)", file=sys.stderr)

    cards = [e for e in data["dex"] if renderable(e)]
    data["counts"] = {
        "repos": len(live - exclude),
        "verified": sum(1 for e in data["dex"] if e["verified"]),
        "entries": len(data["dex"]),
        "cards": len(cards),
        "party": len(data["party"]),
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
