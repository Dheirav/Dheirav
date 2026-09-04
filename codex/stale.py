#!/usr/bin/env python3
"""Flag cards whose repo has moved since the card was last written or checked.

A card carries prose about results. `sync.py` reconciles which repos exist; it
cannot tell whether a sentence is still true, and nothing else does either — a
card can go false while every job stays green. This is the cheap half of the
problem: it compares the moment a card's prose last changed against the moment
GitHub last saw a push, and lists the cards the repo has outrun.

It does not read the prose and never claims a card is wrong. Most pushes will
not touch anything a card says. What it buys you is a short list worth
re-reading instead of the whole codex.

That only stays short if you can answer it. `--ack` records that you re-read a
card and it is still true, which settles it until the next push — without
editing prose that does not need editing. An unanswerable checker is one you
learn to ignore.

The prose date comes from git history rather than a stored field, so it cannot
drift from the thing it describes. That needs real history: under
`actions/checkout` set `fetch-depth: 0`, or every card looks as though its prose
changed at the only commit present.

    python3 stale.py                 # report
    python3 stale.py --check         # exit 1 if any card is behind
    python3 stale.py --ack REPO ...  # record that those cards were re-read
    python3 stale.py --ack-all       # ... every card currently behind
"""
import datetime
import json
import os
import subprocess
import sys

import sync  # one fetch implementation, shared

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "codex.json")
# git stamps are local, the API's are UTC. Showing them as they arrive puts two
# timezones in adjacent columns and makes an ordering look wrong.
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def git(*args):
    r = subprocess.run(("git",) + args, cwd=HERE, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def when(iso):
    """Parse an ISO stamp from git or the API into an aware datetime."""
    if not iso:
        return None
    try:
        d = datetime.datetime.fromisoformat(iso)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)


def prose_dates():
    """{repo: when the prose it carries today was written}.

    Walks codex.json back through history while an entry's (desc, foot) is
    unchanged; the oldest commit still holding today's text is when it was
    written. Entries are read from `dex` and from the pre-dex `party`, so
    history from before that restructure still reads correctly.
    """
    log = git("log", "--format=%H %cI", "--", "codex.json")
    commits = [l.split() for l in (log or "").splitlines()]
    if len(commits) < 2:
        return {}, len(commits)

    def at(sha):
        blob = git("show", f"{sha}:./codex.json")
        if not blob:
            return None
        try:
            d = json.loads(blob)
        except json.JSONDecodeError:
            return None
        out = {}
        for e in list(d.get("dex", [])) + list(d.get("party", [])):
            if isinstance(e, dict) and "repo" in e:      # party was objects once
                out[e["repo"]] = (e.get("desc", ""), e.get("foot", ""))
        return out

    snaps = [(sha, date, at(sha)) for sha, date in commits]
    current = snaps[0][2] or {}
    dates = {}
    for repo, text in current.items():
        stamp = snaps[0][1]
        for _sha, date, ents in snaps:
            if ents is None or ents.get(repo) != text:
                break
            stamp = date
        dates[repo] = stamp
    return dates, len(commits)


def main():
    args = [a for a in sys.argv[1:]]
    check = "--check" in args
    ack_all = "--ack-all" in args
    ack = []
    if "--ack" in args:
        ack = args[args.index("--ack") + 1:]
        if not ack:
            print("--ack needs at least one repo name", file=sys.stderr)
            return 2

    data = json.load(open(DATA))
    dex = {e["repo"]: e for e in data["dex"]}
    written, ncommits = prose_dates()
    if not written:
        print("no usable git history for codex.json — "
              "fetch-depth: 0 is needed for the prose date", file=sys.stderr)

    pushed = {r["name"]: r.get("pushed") for r in sync.fetch_public(data["owner"])}
    now = datetime.datetime.now(datetime.timezone.utc)

    rows, behind = [], []
    for e in data["dex"]:
        repo = e["repo"]
        if not (e.get("desc") and e.get("foot")):
            continue                                    # no card to go stale
        card = max((d for d in (when(written.get(repo)), when(e.get("checked"))) if d),
                   default=None)
        moved = when(pushed.get(repo))
        if card and moved and moved > card:
            rows.append((e["no"], repo, card, moved, (moved - card).days, True))
            behind.append(repo)
        else:
            rows.append((e["no"], repo, card, moved, None, False))

    print(f"codex prose vs repo activity — {len(rows)} cards, "
          f"{ncommits} commits of codex.json history\n")
    def ist(d):
        return f"{d.astimezone(IST):%Y-%m-%d %H:%M}" if d else "unknown".ljust(16)
    for no, repo, card, moved, days, is_behind in sorted(rows, key=lambda r: r[0]):
        gap = f"repo moved {days}d later" if is_behind else "ok"
        print(f"  {no}  {repo:<26} card {ist(card)}  repo {ist(moved)}  {gap}")
    print("\n  (times IST)")

    targets = behind if ack_all else [r for r in ack if r in dex]
    if behind and not targets:
        print(f"\n{len(behind)} card(s) to re-read: {', '.join(behind)}")
        print("re-read them, then: python3 stale.py --ack " + " ".join(behind))
    elif not behind:
        print("\nevery card is at least as new as its repo")

    unknown = [r for r in ack if r not in dex]
    if unknown:
        print("not in the codex: " + ", ".join(unknown), file=sys.stderr)
        return 2
    if targets:
        stamp = now.isoformat(timespec="seconds")
        for repo in targets:
            dex[repo]["checked"] = stamp
        with open(DATA, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        print(f"\nmarked re-read: {', '.join(targets)}")
        return 0

    return 1 if (check and behind) else 0


if __name__ == "__main__":
    sys.exit(main())
