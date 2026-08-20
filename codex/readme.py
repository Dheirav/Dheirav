#!/usr/bin/env python3
"""Rewrite the profile README from codex.json.

The README is generated rather than edited so that a repo going private cannot
leave a dead <img> or a link to a 404 behind. Everything below FOOTER is yours
to edit by hand; everything above it is derived.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = json.load(open(os.path.join(HERE, "codex.json")))
RAW = "https://raw.githubusercontent.com/{owner}/{owner}/main/codex".format(owner=DATA["owner"])
GH = "https://github.com/" + DATA["owner"]

FOOTER = (
    "[LinkedIn](https://www.linkedin.com/in/dheirav-prakash-63a107308/) "
    "· [dheirav2005@gmail.com](mailto:dheirav2005@gmail.com)"
)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def nice(tag):
    """SEARCH -> Search, but LLM stays LLM. Short tags are acronyms."""
    return tag.upper() if len(tag) <= 3 else tag.capitalize()


def main():
    party, arch = DATA["party"], DATA["archive"]
    labels, counts = DATA["labels"], DATA.get("counts", {})
    out = []

    idcard = (f"ID card — Dheirav Prakash, Chennai India, "
              f"{counts.get('repos', 0)} repos, {counts.get('verified', 0)} verified results")
    out.append(f'<img alt="{esc(idcard)}" src="{RAW}/trainer.svg">\n')

    idx = "; ".join(
        f"{e['no'][3:]} {e['repo']} ({'/'.join(nice(t) for t in e['tags'])}, "
        f"{e['lang']}, since {e['since']})" for e in party)
    out.append(f'<img alt="{esc("Codex index — " + idx)}" src="{RAW}/index.svg">\n')

    arc = ", ".join(labels.get(r, r) for r in arch)
    out.append(f'<img alt="{esc("Archive — " + arc)}" src="{RAW}/archive.svg">\n')

    out.append("<details>\n<summary><b>Full entries</b></summary>\n<br>\n")
    for e in party:
        n = e["no"].split(".")[1]
        alt = (f"{e['no']} {e['repo']} — {'/'.join(nice(t) for t in e['tags'])}, "
               f"{e['lang']}, since {e['since']}. {e['desc']} {e['foot']}")
        out.append(f'<a href="{GH}/{e["repo"]}">'
                   f'<img alt="{esc(alt)}" src="{RAW}/entry-{n}.svg"></a>\n')
    out.append("</details>\n")

    out.append("---\n")
    links = [e["repo"] for e in party] + list(arch)
    body = " ·\n".join(f'<a href="{GH}/{r}">{r}</a>' for r in links)
    out.append(f"<sub>\n{body}\n</sub>\n")
    out.append("---\n")
    out.append(FOOTER + "\n")

    path = os.path.join(ROOT, "README.md")
    new = "\n".join(out)
    old = open(path).read() if os.path.exists(path) else ""
    if new == old:
        print("README.md already current")
        return
    open(path, "w").write(new)
    print(f"README.md rewritten ({len(party)} entries, {len(arch)} archived)")


if __name__ == "__main__":
    main()
