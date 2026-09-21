# Housekeeping — 2026-09-04

Second round. Scope: all nine project repos plus the profile repo.

## Method

Re-cloned every repo and compared what the documents claim against what the code
does. Repos whose last commit predates the 2026-08-27 audit were checked for
drift by commit date rather than re-audited, since the code they were audited
against has not changed.

| repo | last commit | drifted? |
| --- | --- | --- |
| BrassBot | 2026-09-04 13:37 | **yes — card was false** |
| who-pays-for-fairness | 2026-08-28 00:14 | no, numbers re-verified unchanged |
| photo-dedupe-review, AudioTranscriber, LabEvaluationSystem | 2026-08-15 | no change since audit |
| HelperBoi, SaleSnipe, Carbon_Gauge, Attendance_Tracker_Mobile | 2026-08-15 | no change; last round's findings still open |

## Fixed

**Profile card No.015 was advertising a retired bot.** BrassBot archived `mcts`
this afternoon for losing to the evaluation it searches with (-4.81 +- 1.66 VP,
-2.9 sigma). The card said it *wins 66.7%*. Rewritten around the shipped
heuristic; footer now `131.3 VP MIRROR, 146.7 VS GREEDY AT 4P`.

**BrassBot test counts, both wrong in different directions.** README said 205,
NEXT.md said 175. Ran the suite: **204 passed in 4m31s**. Both corrected. Note
the count I fixed last round went stale inside a week — a hardcoded test count
in prose is a recurring maintenance cost, and `pytest -q` output would not be.

**Four claim/code mismatches, open since last round, now corrected:**

- `HelperBoi` — vector search marked `[Planned]` while `vector_search.py` and
  `rag_context.py` are both wired in.
- `Attendance_Tracker_Mobile` — README claimed Hilt DI (not a dependency; the
  build has Room, WorkManager and POI) and diagrammed a Domain Layer of use
  cases that does not exist. Testing section described unit, integration and UI
  suites against two test files.
- `SaleSnipe` — "AI-Powered Insights" covered a real TensorFlow.js price model
  *and* a nine-word keyword lexicon. Now says which is which.
- `Carbon_Gauge` — "Accurate ... industry-standard formulas" was unsourced, and
  every machine uses a hardcoded 0.475 kgCO2/kWh, so results are not
  region-aware. Now states both.

## Added

**ConwayClock is No.016**, pushed at 22:38 IST today — after the 14:21 sync, which
is why CI had not seen it. `sync.py` scaffolded the stub and read `lang: C` from
the API. Card written from the repo's README and RESEARCH.md; sprite drawn as
`lifeclock()` (`SPRITES[16]`); tag `AUTOMATA` added to `TYPES` at `#9B4FA8`, the
one hue the palette had left. Auto-label came out `ConwayCloc`, blunt truncation
at ten characters, so it is hand-set to `Conway`.

Not sealed: the CPU and memory figures are self-measured on one machine, and the
Life pattern is dim's (2017, CC BY-SA), credited in the repo. Nothing there is
externally checkable in the way ChessBot's Lichess rating is.

## Observations, not fixed

**The scheduled workflow runs 4-6 hours late.** `codex.yml` asks for 04:17 UTC;
the last eight runs landed 08:47-11:05 UTC. All succeeded and all committed
nothing. This is GitHub deprioritising scheduled jobs, not a fault — but the
comment "daily, 04:17 UTC" describes the request, not the behaviour.

**NEXT.md's `## Current state` section is the stalest part of the file.** The
top of that document is live and detailed; the section named "Current state" at
line 421 still carried a test count three months of work out of date, and also
claims "80 full 4-player games (40 random, 40 greedy)" which I could not verify
and did not touch.

**BrassBot's first playing-strength table is gone but its old inconsistency is
worth remembering.** The README has been rewritten since last round and now
labels the mirror tables properly — the note I added survived and was expanded.

## Not done

Nothing is committed or pushed. Line endings: all four project READMEs are CRLF;
my first attempt normalised them to LF and produced whole-file diffs, so the
edits were reverted and redone byte-safe. Verified: diffs are now 1-24 lines each.
