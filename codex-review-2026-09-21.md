# Card review, 21 September 2026

Seven read-only auditors, one per repo that had moved since its card was written.
Each cloned with full history, read the handover document first, listed the
commits since the card date, and checked every claim on the card against a file
and line. Eight cards were not re-audited because their repos have not moved
since they were last checked, so there was nothing new to find.

Applied on 21 September, with three decisions from the owner: NashForge keeps
the win in the footer with the seal off (option A); DeepFakeDetector is sealed
and UkuleleTabsMaker unsealed; who-pays takes the new card; and ThirstTrap's
footer names the tested claim, "ONE WET SAUCER MOVES THE FIT UNDER 10%", in place
of a test count that had gone stale in hours. ThirstTrap's seal was left off
because the owner did not name it. All text is validated against the panel
limits: six wrapped lines for the description, 42 characters for the footer,
bitmap-font characters only.

## What the round found, in one paragraph

Nine cards had a repo that moved. Two of them are now false by the repo's own
account, which is the failure the checker was built for: DeepFakeDetector's
89.5% is a number the repo withdraws as a dataset shortcut, and
UkuleleTabsMaker's 99.7% on 340 notes was replaced on 20 August when the
benchmark stopped scoring one video twice. Three more carry numbers the repo has
since revised (ConwayClock, ThirstTrap, NewsLetterScrapper). Two have true cards
but a headline that has moved past them (NashForge won an arena, who-pays found
its central claim reverses on a second dataset). ChessBot's card contains one
claim its own gate rules contradict. BrassBot's card quotes a table the repo
marks stale. The pattern underneath is the same in every case: a number written
into prose stops being true the moment the thing it describes moves, and nothing
fails when it does.

## Cards to change

### No.003 NashForge

The win is real and heavily documented. Chipzen season 6, a public heads-up
no-limit Hold'em arena: 4-1 in the round-robin as top seed, 3-0 through the
playoffs, every match it played. The full bracket is in `NEXT.md:134-150`, the
per-match ledger in `results/chipzen/ledger.md`, and the platform's Glicko
record in `results/chipzen/rating_history.jsonl` (1571, 160 won of 272 rated).
Your own framing in `NEXT.md:160-165` is worth keeping in mind: what won the
season was operations, not solver strength.

The seal is the question. Every chipzen.ai data endpoint returns 403 without a
login, the standings tables in `NEXT.md` were pasted from a logged-in page, and
no bot URL, bot id or screenshot is committed. So the win is asserted with a
consistent internal ledger, but nobody can confirm it from the repo. The card's
seal currently rests on the Kuhn and Leduc reproductions, which a reader can
rerun. Putting the win in the footer and keeping the seal would mean sealing
the one claim on the card that is not checkable.

Option A, the win in the footer, seal off until it is checkable:

    desc: An MCCFR solver for heads-up no-limit Hold'em with a C++ core. Its
          bot won Chipzen season 6, 4-1 as top seed and 3-0 in the playoffs.
          An earlier pipeline's results were withdrawn.
    foot: CHIPZEN SEASON 6 CHAMPION - 4-1 RR, 3-0 KO
    verified: false

Option B, the win in the description, a reproducible number in the footer,
seal kept:

    desc: (same)
    foot: BEATS PPO BY 75, EVOLUTION BY 212 BB/100
    verified: true

I would take A. B's footer is a comparison against your own other bots, which
is the exact caveat BrassBot's README warns about, while the arena win is
against other developers' bots on a public platform. The route back to the seal
is small: commit the bot's chipzen.ai page URL and an archived copy of the
season 6 standings, then re-seal.

Two numbers in the repo disagree and one of them is on the card's evidence
trail. `NEXT.md:148` says the final was won at +437 +- 173 a hand; the ledger
records the same 67-hand match at +149 a hand. Matches settle at exactly 10,000
chips and 10,000 / 67 = 149, so the ledger is arithmetically right and the +437
looks like a transcription error. `NEXT.md:141` also gives round 2 against
mellyy as 32 hands where the ledger says 94; 32 is the quarter-final. Both
should be fixed before any card cites `NEXT.md`.

### No.004 DeepFakeDetector

The card is false by the repo's own account. `docs/HANDOVER.md:9-11` says the
original model "scored 89% by recognising which dataset a file came from, not
what was in the image", and `README.md:61-67` shows a metadata-only lookup on
format and resolution getting 87.4% on that corpus without reading a pixel.
Forty-six commits between 8 and 16 September rebuilt it on OpenSDI, verified
shortcut-free. The current headline is read directly from committed JSON:
`results/mask_head_clip448_balanced/training_summary.json` gives 0.80395
three-class accuracy on a balanced 4,050-image split, and
`heldout_generators.json` gives nine held-out-generator recalls averaging
0.7228.

This is the same shape as the NashForge card: a published number audited and
withdrawn by you, which is the story now.

    desc: Sorts images into real, AI-generated or AI-edited. The first model's
          89% measured which dataset a file came from. Rebuilt on shortcut-free
          data: 80.4% in-domain, 72.3% unseen.
    foot: 80.4% IN-DOMAIN / 72.3% HELD-OUT RECALL
    verified: true (recommended, was false)

The seal case: the headline checkpoint is in git, both numbers are in committed
JSON, the test split is deterministic, and there is a test suite with CI. That
is the same bar who-pays-for-fairness was sealed on. The caveat is that nobody
has re-run it, and the old reason for leaving this card unsealed was exactly
that nobody could. If the seal means "a third party can reproduce it", the
answer is now yes with the OpenSDI data, so I would seal it. Your call.

### No.001 ChessBot

One claim is wrong on the repo's own terms, and one is better than the card
says. "Every heuristic won an SPRT match" contradicts `docs/GATES.md:26`, which
says "Never --sprt under sharding"; the ledger of about fifty gates is fixed-N
and node-limited with pooled confidence intervals, and SPRT was used once, in an
archived August gate. Three heuristics also shipped without a gate on purpose
(`evalnoise` at -3.9 by design, `qBound` as "a repair, ungated", `stagedGen`
because its output is identical by construction). "Bitboards" is loose as well:
move generation is mailbox, and magic bitboards only do attacks and pins.

The rating claim is true and understated. The auditor hit the public Lichess
API today: `Crimsy_Bot` is at 2279 rapid over 798 games, 554 won, 63 drawn, 192
lost. Lazy SMP shipped on 7 September at +162 Elo and the LMR table on 10
September at +26.4, and the bot moved 127 points that no file in the repo
records; the last written figure is 2152 from 27 August.

    desc: A UCI chess engine written from scratch. Alpha-beta, lock-free
          transposition table, Lazy SMP, null-move and late-move pruning.
          Heuristics are gated on self-play; losers stay logged.
    foot: LICHESS 2200+ RAPID - VERIFIED
    verified: true (unchanged)

The footer keeps the floor pattern rather than quoting 2279, because a rating
with rd 46 can dip and a floor stays true. 2200 is comfortably under the live
figure and above the repo's own last reading. Worth recording the current rating
in `docs/MEASUREMENTS.md` at the same time.

### No.002 UkuleleTabsMaker

The footer has been wrong since 17:04 IST on 20 August, which is two and a half
hours after the card was written. Commit `c2a61e7` "Stop scoring one video
twice" found that the benchmark had a byte-identical duplicate clip, and the
headline went from "three clips, 340 notes, 99.7% recall" to "four clips, 316
notes, 98.7% recall, 100% precision, 312 recovered, four missed, none
invented". The commit message also says the 340-note figure "was staler still",
from a clip set that had changed twice, so the card was stale at the moment it
was sealed.

"Not the audio" is now half true. Fret numbers still come from vision, but
timing is taken from the soundtrack for tabs whose page shows no highlight
(`src/audio/onsets.py`, `NEXT.md:117-135`). That route landed on 19 August,
before the card.

    desc: Reads ukulele tabs off a YouTube video and prints a playable sheet.
          Fret numbers come from vision on the notation; timing from the
          player's highlight, or the soundtrack if there is none.
    foot: 98.7% RECALL / 100% PRECISION, 316 NOTES
    verified: false (recommended, was true)

The seal: hand-labelled ground truth is committed for all four clips
(`benchmark/measures/*.json`, each marked `verified: true` with how) and the
scoring script is committed. But `reference_clip`, which carries 98 of the 316
notes, has `yt: null` and no committed video, and `README.md:11-12` says the
detections are committed when `benchmark/results/` is gitignored and the score
command re-runs the pipeline. A third party can reproduce 218 of the 316 notes
and not the headline. Adding the reference clip's YouTube id and correcting that
README line would restore the seal; until then it is asserting more than a
reader can check.

### No.014 who-pays-for-fairness

Every number on the card is still exact. `results/mitigation_summary.csv` has
not changed since 11 August: DP 0.161 to 0.019, EO 0.083 to 0.277, all five
methods shrinking the pool by 7.9 to 22.1 percent. The seal holds.

What has moved is the project. I had told the auditor `research/` was
third-party papers, and it is not: it is 69 of your own documents, a 24-page
IEEE paper, 1,735 result directories and a live `research/NEXT.md`. The central
finding is now that levelling down is a property of the population rather than
of demographic parity. The identical constraint that removes 20.5 percent of
Adult's approvals grows HMDA Mississippi 2018 mortgage approvals by 4.26
percent, and both numbers are pinned by assertions in
`tests/test_documented_claims.py`. So the card's line "closes the gap by taking,
not lifting" is true of Adult and false in general, which is what the paper
argues. The top-level README is frozen deliberately as the course deliverable
(commit 62beeb2), which is why a reader of it alone would misjudge the repo by an
order of magnitude.

    desc: Reproduces a fairness-constraint paper on Adult Census, then asks who
          paid. On Adult the constraint shrinks the approval pool by a fifth;
          on HMDA lending the same rule grows it.
    foot: ADULT POOL -20.5%, HMDA +4.3%, SAME RULE
    verified: true (unchanged)

One correction to something I wrote when sealing this on 4 September. I said
the metrics were cross-checked against fairlearn on every run. That is the
README's claim, and `crosscheck_against_fairlearn` is only called from
`run_baseline.py`. The mitigation runs use the same `evaluate()` and their
models come from fairlearn's own `ExponentiatedGradient`, so the numbers are
sound, but the check does not fire on them. The seal still stands on the
test-pinned CSVs; my stated reason was loose.

### No.015 BrassBot

The description is still true. `heuristic` still ships, `mcts` is still
archived, and the 27 experiments since 4 September (brewery rules, routing, a
cross-turn sell chain at -9.66 +- 0.63) all lost or came out null, and none
shipped. That reinforces the card's line rather than dating it.

The footer quotes a table the repo calls stale. 131.3 / 146.7 is the README's
playing-strength table, unchanged since 4 September despite four shipped weight
changes. `NEXT.md:18-19` has a 6 September refresh at 130.0 / 148.4, and then
`NEXT.md:57-58` flags even that as "STALE as of 2026-09-07 ... Regenerate before
quoting a cell" because `canal_double` shipped after it. There is no current
number in the repo to put on a card.

    desc: (unchanged)
    foot: 130.0 VP MIRROR, 148.4 VS GREEDY AT 4P
    verified: false (unchanged)

That footer is the newest measured cell, but the real fix is on the repo side:
regenerate the standings once, then the card can quote them. Until then this is
the least stale option, not a current one.

### No.016 ConwayClock

The description is fully accurate and nothing has moved in 15 days. The footer
is off by the amount commit `340d9fb` corrected on 6 September, which re-measured
the default configuration and says the old 4% "overstates the cost by roughly a
quarter". The repo now states 3.2 percent median of one core, 2.5 to 3.7
typical, and memory went from 97 MB to 74 MB the same day.

    desc: (unchanged)
    foot: 192 GEN/S, 3% OF ONE CORE, 74 MB, NO GPU
    verified: false (unchanged)

### No.017 ThirstTrap

Your card matches commit `e0a2219` at 20:27 on 9 September exactly. At 23:04 the
same evening, `43d3a08` "F14: Feeding" bumped the schema to v11 and added tests,
so the card was stale within two and a half hours. The tree now holds 221 JVM
tests and 14 device tests by `@Test` count, schema v11 at
`ThirstTrapDatabase.kt:39`. `docs/HANDOVER.md:18-20` still says 214 / 13, so the
repo's own handover disagrees with its tree too.

The saucer claim is better than the card says. It is not only documented, it
has a dedicated test: `SlopeFitTest.kt:35-63` corrupts one end reading of a
five-point series and asserts the Theil-Sen slope moves under 10 percent where
least squares moves over 30.

    desc: (unchanged)
    foot: 221 JVM + 14 DEVICE TESTS, SCHEMA V11
    verified: true (recommended, was false)

Every claim is checkable in source rather than prose, which is the seal's bar.
One thing to consider, though: a test count is the fastest-moving number on the
whole profile. This one went stale in hours and BrassBot's has drifted three
times. A footer that names the estimator and the robustness result would hold
for as long as the code does.

### No.006 NewsLetterScrapper

The local-LLM claim holds up under code reading: Ollama via the `ollama`
package, models llama3.2 and nomic-embed-text, no openai, anthropic or google SDK
anywhere in the requirements, and the only outbound hosts are the feeds, Gmail
SMTP for delivery, and Ollama on localhost. The feed count moved. Commit
`7613537` on 20 August replaced five dead feeds, dropped four paywalled ones and
added eleven, so `sources.yaml` now has 40 entries, while `README.md:3` still
says 38 and its source table still lists nine feeds that no longer exist.

    desc: Clusters 40 RSS feeds into stories and writes the analysis with a
          local Ollama model. No article text reaches a third-party AI. Only
          RSS fetches and the emailed briefing leave.
    foot: SELF-HOSTED OLLAMA - NO EXTERNAL AI APIS
    verified: false (unchanged)

## Same evening, both seals restored

NashForge fixed its own claim at 23:48 IST: `docs/season6/README.md` carries the
platform's champion card, bracket and standings as screenshots from the
logged-in dashboard, plus the bot id and the three playoff match ids, each of
which resolves at `chipzen.ai/api/matches/<id>` for any free login. `NEXT.md`
moved to a private repository at the same time, which takes the +437 figure out
of the public record. That is the Lichess standard, so the seal went back on.

UkuleleTabsMaker got the reference clip's YouTube id (`Di4L3ozQmE0`, matched by
exact title from the duplicate entry) and a README sentence that says what
checking the figure actually takes. Pushed as 44187bb. All 316 notes are now
reproducible by a third party, so that seal went back on as well.

The ID card reads 5 verified results.

## Repo-side problems the auditors found

These are in your project repos, not the profile, and most of them are the same
defect: a number or a claim in prose that the code has moved past.

NashForge: `NEXT.md:148` final margin +437 vs ledger +149 (the ledger is
arithmetically right); `NEXT.md:141` round-2 hands 32 vs ledger 94; `README.md:157`
says the arena rules are in CLAUDE.md, which has never been committed;
`README.md:31-33` says the histogram abstraction is next when the 21:04 commit
today measured it.

DeepFakeDetector: `docs/EXTERNAL_BENCHMARK.md:5-9,41` still presents 89.5% as
"the headline number" and "under 0.2%" as an established result with no
correction banner, unlike `results/ablation_study.md` which has one;
`README.md:529` and `HANDOVER.md:92` say 44 tests where the files hold 46;
`LIMITATIONS.md:213` says the degradation grid has not been repeated on the mask
head, and the next paragraph reports it.

BrassBot: test count in four places (README 204, NEXT.md 204, architecture.md
205, options-swot.md 199) against 193 functions in the tree, 22 of them added
after 204 was measured; `README.md:7` says a 37-weight evaluation where
`HeuristicBot.DEFAULTS` has 56 keys; the README standings table has not been
regenerated since 4 September; `NEXT.md` "Current state" (line 981 onward) is
superseded by its own top block and not marked as such; `README.md:199-200` and
`141-150` disagree about whether the server holds one game or one per room.

ChessBot: the README has not been touched since 17 August and now says the
engine advertises no Threads option (it does), that search is single-threaded
(Lazy SMP, the bot runs six threads) and that there is no licence (it is MIT);
`HANDOFF.md`'s header and "State right now" table are stale against sections
appended below them; the live rating has not been written down since 27 August.

UkuleleTabsMaker: `README.md:11-12` says detections are committed when they are
gitignored; `reference_clip` has no YouTube id.

ThirstTrap: `docs/HANDOVER.md:18-20` says 214 / 13 against 221 / 14 in the tree.

NewsLetterScrapper: `README.md:3,300-313` says 38 feeds and lists nine that were
removed.

who-pays-for-fairness: `research/NEXT.md` lags the paper by about 12 days (161
populations and 63 checks against 179 and 87); `README.md:300-302` claims a
fairlearn cross-check on every run that only the baseline runs perform.

## The pattern, stated once

Every stale number above is a count or a result that lives in prose while the
thing it counts lives in code. Test counts are the worst because they change on
every commit that adds a test, which is most commits. ThirstTrap's went stale in
under three hours; BrassBot's has been corrected twice and is wrong again in
four places at once. Standings tables and benchmark headlines go the same way,
just slower. The checker now catches the drift on the profile side within a day.
On the repo side the durable fix is to have the number generated by the thing it
describes, or not to write it down at all.
