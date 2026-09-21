# Draft prose for the nine unpinned entries

Third pass. This one is drafted from the **cloned repositories** — source,
tests and docs — not from READMEs. That changed several entries substantively
and corrected two things I told you earlier.

Nothing has been written to `codex.json`. Edit the `desc:`/`foot:` lines and
tell me to apply.

All nine are validated: `desc` fits **6 wrapped lines** (so no card resizes and
`codex.gif` keeps its dimensions), `foot` fits **42 characters**, and no
character is outside the bitmap font.

---

## Corrections to what I told you earlier

**BrassBot is not empty — you were right.** The clone has 46 files and 175
tests. The REST API was serving stale cached responses: `/branches` returned
`[]` and `/contents` returned "This repository is empty" while the git remote
had the commit. I stated that too confidently. `git clone` is authoritative
here and the API is not.

**SaleSnipe's "AI" is not vapour.** I said there was nothing behind the claim.
There is: `pricePredictionService.js` genuinely requires `@tensorflow/tfjs-node`.
But `sentimentAnalysisService.js` is a nine-word positive list against a
nine-word negative list, so "AI-powered sentiment analysis" is generous. Left
out of the card on those grounds, not on the earlier one.

---

## No.015 BrassBot — Python, 2026
tags: SEARCH, ENGINE
desc: A rules engine, bots and a measurement harness for Brass: Birmingham. The MCTS bot wins 66.7% of four-player games against three heuristics, where an equal share would be 25%.
foot: 115.6 VP, 66.7% WIN - EQUAL SHARE 25%

> This is the strongest of the nine and it is not close. It belongs in the same
> family as ChessBot — and the sprite you picked now reads as deliberate.
>
> Source: playing-strength table — `mcts` at 1500 iterations scores 115.6 mean
> VP, 66.7% win rate, 3.73 VP/action against three heuristic bots; expert human
> ~155 and ~5.0 VP/action. Engine plays 2p/3p/4p. Determinized MCTS over a tuned
> position evaluation.
>
> What makes it profile-worthy is the harness, which is built to resist
> self-deception: seats rotate through every position; three disjoint seed
> blocks (tune on one, validate on a second, report on a third); distributions
> rather than means; and `yardstick.py` scores against a profile of expert
> *behaviour* from recorded tournament games, so a bot can beat everything else
> written here and still be told it plays badly. **"Five separate tuning results
> looked like gains on their own seeds and vanished on unseen ones."**
>
> It also withdraws its own target: the project began aiming at 200+ VP at 4
> players and the README now states that is unreachable — 31 actions per player
> at ~5 VP each caps expert play near 155 — with the realistic target restated
> as 150-165. That is the same move NashForge's entry records.
>
> **Resolved:** I installed pytest in a throwaway venv and ran the suite.
> **175 collected, 175 passed in 54.7s.** The README is right; `NEXT.md`'s
> "63 tests pass" is stale and worth correcting, since that file is the live
> handover document.
> **Flag:** `sync.py` will fill `lang: Python` on its next run now that GitHub
> has indexed the code.
> **Flag:** measured against its own bots and an expert *behaviour* profile, not
> an external ladder — so I left `verified: false`, unlike ChessBot's Lichess
> rating. Alternative footer: `3.73 VP/ACTION - EXPERT HUMAN 5.0`.

## No.007 HelperBoi — Python, 2026
tags: LLM, TOOLS
desc: A ReAct agent over an Obsidian vault: it classifies the request, retrieves matching notes, then chains tools. It can also write a new skill, compile-test it and register it for next time.
foot: OLLAMA - REACT LOOP - SELF-WRITTEN SKILLS

> **My earlier "it's a planning document" call was wrong in the other
> direction.** The code is substantial — 34 modules. `agent_loop.py` is a real
> ReAct loop (Thought → Action → Action Input → Observation) chaining tools;
> `skill_engine.py` drafts a new skill with the LLM, `py_compile`-tests it, then
> registers it under `skills/`; `rag_context.py` injects vector-search hits and
> assistant memory into prompts; `intent_classifier.py` parses free text into
> structured JSON intents. `vector_search.py` sets `HF_HUB_OFFLINE=1` and
> `TRANSFORMERS_OFFLINE=1`, with sentence-transformers falling back to TF-IDF.
> `model_router.py` defaults to LLaMA 3 8B over Ollama on localhost.
> **Flag:** the README marks "Embed vector search" as `[Planned]` while
> `vector_search.py` and `rag_context.py` both exist and are wired in. It also
> lists "Initial scaffolding" as upcoming. That README understates the code as
> often as it overstates it — worth a rewrite before this is ever pinned.

## No.008 photo-dedupe-review — Python, 2026
tags: VISION, TOOLS
desc: Groups duplicate photos and videos for review and never picks a keeper for you. Hashes only propose a pair; the pixels decide, which stops burst shots being called copies.
foot: 251 TESTS - 865 PHOTOS IN 3.1S

> Source: "Hashes propose, pixels decide" — a perceptual match is re-checked as
> a 32×32 greyscale thumbnail at RMS under 3.5, because re-encodes score ~1
> while different shots of one scene start ~4.5. Both pHash and dHash must
> agree. **251 test functions across 19 files**, including
> `test_pixel_verification.py` and `test_delete_whole_group.py` — the safety
> invariants in `core/deletion.py` are covered, not just asserted in prose.
> Benchmark columns are serial vs parallel: 865 photos, 3.1s parallel, ~0.2s
> cached re-scan keyed on `(path, size, mtime)`.
> Alternative footer: `NEVER AUTO-DELETES - SEND2TRASH ONLY`.

## No.009 AudioTranscriber — Python, 2025
tags: SPEECH, TOOLS
desc: Transcribes audio and video with a local Whisper model, from a CLI or a Streamlit page. It also runs live on system audio, routed through a PulseAudio monitor, in three-second chunks.
foot: 3-SECOND CHUNKS - 1-2S LATENCY ON TINY

> Source: latency table measured "with 3-second chunks on GPU" — `tiny` ~1-2s,
> `base` ~2-3s, `small` default. Ten modules, with `windows_transcriber.py` as a
> separate platform path and `hardware_utils.py` auto-detecting VRAM to pick a
> model. System audio via `pactl set-default-source VirtualSink.monitor` — it
> captions what is playing, not just a microphone.
> **Flag:** the thinnest of the nine — no test suite. `SPEECH` is now `#2F8F8A`.

## No.010 LabEvaluationSystem — JavaScript, 2025
tags: WEB, TOOLS
desc: A lab-evaluation system for a university department. Faculty schedule tests from a question pool, a fresh login retires the older session, and every action is logged with its IP.
foot: ONE LIVE SESSION - IP-STAMPED AUDIT LOG

> Verified in code, not just the README: `backend/models/User.js` carries a
> `sessions: [{ token }]` array, and `backend/routes/faculty.js` stamps `req.ip`
> on logged actions at five separate call sites. Bulk import from
> XLSX/XLS/CSV/JSON/PDF; role-based dashboards for admin, faculty, student.
> `WEB` is now `#4C5BA8` in `TYPES`.

## No.011 Attendance_Tracker_Mobile — Kotlin, 2025
tags: MOBILE, TOOLS
desc: An Android attendance tracker in Compose and Room. Subjects carry a weekly timetable, so it opens on today's classes, and the safe-skip calculator says how many more you can miss.
foot: COMPOSE - ROOM - REMINDER WORKER

> **Footer corrected — Hilt is not in this project.** My last draft said "MVVM,
> ROOM, HILT" from the README's tech-stack list. `app/build.gradle.kts` pulls in
> Room only; there is no `dagger.hilt` dependency and no `@HiltAndroidApp`
> anywhere. There is a real `worker/AttendanceReminderWorker.kt`, so the footer
> names that instead.
> **Flag:** the README's architecture diagram shows a Domain Layer of Use Cases
> and Domain Models. The source tree is `data`, `repository`, `ui`, `viewmodel`,
> `worker` — there is no domain or usecase package. The README also describes
> unit, integration and UI testing strategies against 2 test files in 43 Kotlin
> files. I described what the app does and left the architecture claims out.

## No.012 SaleSnipe — JavaScript, 2025
tags: PIPELINE, WEB
desc: Scrapes Amazon, eBay and Flipkart into MongoDB on a cron, keeps the price history and alerts on a drop. A CLI reports what is trending, what discounts hardest and what is volatile.
foot: 4 SCRAPERS - TRENDING AT 15% IN 7 DAYS

> Source: four scrapers on a shared `BaseScraper` — Amazon, AmazonIndia,
> Flipkart, eBay — plus `cronService.js`, `currencyService.js`,
> `notificationService.js`. `analyze-data.js --trending` is documented as
> ">15% discount in last 7 days".
> **Flag:** see the correction above. Price prediction really does use
> TensorFlow.js; sentiment analysis is a hardcoded nine-word lexicon. Neither is
> in the card.

## No.013 Carbon_Gauge — JavaScript, 2025
tags: WEB, TOOLS
desc: Splits a machining job's CO2 into four terms - electricity, tool wear, coolant and material - so the tool grade and the coolant's disposal route change the answer, not just the run hours.
foot: 4 TERMS - 29 TOOL GRADES, 4 DISPOSALS

> Much more specific than its README. `server/services/calculation.service.js`
> implements `CEelec`, `CEtool`, `CEcoolant` and `CEm` separately. Tool wear is
> `(runTime / (Ttool * 60)) * CEFtool * toolMass` over a table of **29 tool
> materials**, each with its own emission factor and tool life — HSS 33.75 at
> 45 min, PCD 50 at 300. Coolant is five types by lifetime against **four
> disposal routes** — recycle 0.35, incineration 1.25, landfill 0.1, waste
> coolant 1.5. Machines are seeded per manufacturer (Mazak, DMG Mori, Haas,
> Okuma, Makino, Fanuc, Brother).
> **Flag:** every machine uses a hardcoded `carbonIntensity: 0.475` kgCO2/kWh,
> so `emissionFactor` is just power × a single fixed grid factor — the result is
> not grid- or region-aware despite the compliance framing. The coolant
> function also has a commented-out `* 260` and two pass-through aliases. That
> is why the card describes the decomposition and claims no accuracy.

## No.014 who-pays-for-fairness — Python, 2026
tags: RESEARCH, FAIRNESS
desc: Reproduces a fairness-constraint paper on Adult Census, then asks who paid. The demographic-parity constraint makes equalized odds 3.3x worse, and closes the gap by taking, not lifting.
foot: DP 0.161 TO 0.019 - EO 3.3X WORSE

> Source: mitigation table, decision tree depth 8, mean ± std over 5 seeds.
> ExpGrad(DP) takes DP diff 0.161 → 0.019 for 1.5pp accuracy and lifts disparate
> impact 0.31 → 0.88, while equalized-odds difference goes 0.083 → 0.277 — "3.3×
> worse than doing nothing at all", which the README calls its sharpest result.
> Ten numbered analysis documents in `docs/`, five of them beyond the
> specification. Metrics implemented from definitions and cross-checked against
> `fairlearn` on every run.
> Alternative footer: `2.7 LOST PER 1 GAINED - 5 SEEDS`.
> **Recommendation: set `verified: true`.** The seal means externally
> checkable, and the precedent is NashForge — its seal rests on reproducing a
> known analytic value (`Kuhn -1/18`), not on a big number. This reproduces
> Agarwal et al.'s published result and cross-checks every metric against
> `fairlearn`, an independent implementation, on each run. Both halves are
> checkable by someone else. Contrast DeepFakeDetector, which carries a much
> larger number (89.5% on 77,865 images) and is deliberately *not* sealed,
> because nobody else can rerun it. Still false until you say so — it is a
> public claim on your ID card, which would read 4 verified results.
> `FAIRNESS` is now `#A0526B` in `TYPES`.
