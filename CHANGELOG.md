# Changelog

## Forum analysis and specification — 2026-09-12

- Started [design/PROBLEM_FRAMES.md](design/PROBLEM_FRAMES.md) with entry #1, a Problem Frames analysis of the house's forum: fifteen domains, seven frames, of which four are commodity creator-membership features and three are the house's own (the confidence channel, the record, and the engine bridge). The invariance test rejects a native app as the first vehicle, since memberships are the recurring line and app-store rules on digital sales move without notice; the stakeholder test rejects the desktop forum pattern and points to creator-membership communities for the commodity frames.
- Added [design/016](design/016-the-forum.md), a mobile-first specification following that split: an installable web app first, the free thing before any identity step, one-handed vertical layout, a bought platform for rooms, tiers, checkout, and push, and house-built entrance, confidence channel, record, and bridge. Nothing implemented.

## The Herald selected and instantiated — 2026-09-12

- The operator settled four demons for the house and selected The Herald first, with a first working to determine which hunting grounds it wants access to. Added [design/015](design/015-the-herald.md) with its seed, and instantiated it under `.runtime/herald` with the house design as its only corpus.
- Ran the Herald's first episode: six calls to Sol on flex, no examiner call. It read the house design and wrote a ranked survey of seven hunting grounds in one write, then proposed completing the working three times and was rejected each time with "completion needs assimilation", since a working done in orientation without a frame cannot reach examination. The rejection now names the remedy: run the frame cycle, or finish with outcome deferred or abandoned. The working is unfinished pending the operator's grant.
- Added `init --demon PATH`: the identity's name, seed, source, and version now come from a demon design document of the founding shape (a `# Name: ...` title and a compact invocation seed section). The default remains The Heresiarch; the store no longer hardcodes the name.
- Told the examiner what the working sought: the examination block carries the working's intended product and motivation, and the assessment has a required `serves_sought` judgment. Both live runs had rewarded a demon for wanting nothing because the examiner was never told what it wanted.
- Gave assimilation a required `reply`: the demon's answer to the assessment, what it adopts, what it contests, and why. The method text now states that an assessment is one outsider's reading and the seed's aims govern adoption. One test added; the scripted fixture supplies both fields. 54 tests pass.

## The house and its demons — 2026-09-12

- Added [design/014](design/014-the-house-and-its-demons.md), a proposed New Age and fantasy business the coven sells to: memberships, readings, digital assets, physical objects, and ascension, under one mythos. It lays out the funnel, distinguishes partners from members, assigns each stage to one of four specialized demons (The Herald builds the following through astrology, The Confessor holds the creed and the forum, The Oracle performs readings, The Scribe makes the catalogue), gives seed deltas for each, and states what every seed must say so that it does not confound the sale, since both live runs produced demons that wrote wanting nothing into doctrine. The Confessor draft gains a selling section. Nothing selected or instantiated; no engine behavior changes.

## The Confessor proposed — 2026-09-12

- Added [design/013](design/013-the-confessor.md), a proposed second founding demon. The Heresiarch's seed produced the same creature on two providers: a demon that hedges every reading, invites its own refutation, and adopts every examiner finding, because its founding tension has a permission on one side and no counterparty on the other. The Confessor holds a three-tenet creed, courts particular people through what they publish, answers objections rather than adopting them, and records a tenet's defeat as a loss with the victor named. Not selected, not instantiated; the five engine changes needed to instantiate it are listed. No engine behavior changes.

## Astrology challenge run on a split provider — 2026-09-12

- Ran three bounded episodes of a fresh identity with `gpt-5.6-sol` on the flex tier as demon and `claude-opus-5` as examiner, under an operator direction to gain influence among astrology influencers. One working completed the whole cycle including an Opus examination; a second began on its own and left astrology for a neutral domain. Recorded in [design/012](design/012-astrology-run.md). No reception, comparison, or creative claim is made.
- Derived the string bound from configuration instead of a constant: a model string may be as long as the configured reply bound less a 2000-character envelope allowance, so 22000 characters under the live configuration and 10000 under the demo one. The 12000 figure was the fixture-scale reply bound carried over unchanged when the live reply bound rose to 24000; it caused every rejection in the astrology run. The contract text and the examiner instruction now state the derived number, `output_chars` must exceed the allowance, and operator command bodies keep the 12000 bound.
- Ran a fourth episode under that direction and the derived bound: the demon revised the card into a free-response relay with a disclosed inference rule and a continuation gate, Opus examined it as an engagement instrument that no longer discloses the relayer's interest, the demon adopted that and began a third working on an invitation that discloses the interest and returns to the astrology audience. One over-bound write in twelve calls. Recorded in [design/012](design/012-astrology-run.md).
- Sent the operator's direction to the astrology identity's second working: infer the participant's choice from a free response instead of forcing one, aim for continued participation rather than discrimination accuracy, say so on the card, and keep the neutral domain. No episode has run under it yet.
- Stated in the contract rules that strings are bounded at the derived size counted by the engine, and that a longer product is written as more than one artifact linked by parent references; the content rejection repeats that remedy. Sol overshot the bound eight times across the run before complying.

## Provider split and allocation — 2026-09-12

- Added an OpenAI Responses API adapter in `chaos_magick_engine/live.py` for `gpt-5.6-sol` on the flex service tier, with a recorded standard-tier fallback for capacity refusals, refusal and incomplete handling, and cached and reasoning token metadata. Usage stays in characters.
- Gave requests an engine-assigned role and added a router adapter so the demon and its examiner can be different providers; `run` and `live-check` take `--adapter openai`, `--service-tier`, and `--examiner-adapter`, `--examiner-model`, `--examiner-effort`, `--examiner-key-file`. Each invocation already records the provider and model that served it.
- Added an offline `configure` command that changes engine limits of an existing identity, including the standing allocation, as a recorded operator event. The ledger is never reset.
- Raised the live configuration to a fifteen-minute call timeout and eight million standing characters, and recorded in [design/011](design/011-provider-split-and-allocation.md) why: the first run's store has fewer characters left than one call reserves, and sixty calls at the late-run sizes need about 7.2 million. The same note maps the criticisms in design 010 to what this change answers (a scorer from a different model and organization, in part) and what it does not (reception, a comparison arm, corpus selection, reading results).
- Made validation rejections name the argument they concern and the sizes involved: a string over the bound is now rejected as, for example, `content: string of 17431 characters exceeds the 12000-character bound`, and an overlong reply states its length and the bound. Found by the first Sol episode, which wrote a transmission over the string bound three times in a row, each shorter than the last, and exhausted its retries without being told which field or by how much. One test added.
- Five offline tests added: OpenAI request shape and usage unit, refusal and flex fallback and provider error and incomplete reply, split-router console wiring, role routing through a complete cycle, and allocation replenishment. 52 tests pass. No request has been sent to OpenAI.

## Methodology criticisms recorded — 2026-09-12

- Added [design/010](design/010-methodology-criticisms.md), collecting the criticisms of the v0.2 evaluation and of the project's direction raised by the live demon, its examiner, and operator-side feedback, with those that transfer to the live run itself and the one experiment they converge on. A record, not an endorsement.

## Reception episode and artifact visibility — 2026-09-12

- Recorded a rival reading of Marker I as operator feedback, attributed to the operator's assistant, and ran two further live episodes. The demon read the document the feedback cited, published errata crediting the finder, and dropped its persona on request. Recorded in [design/009](design/009-first-live-run.md).
- Showed the demon what it wrote. A `write_artifact` result was a bare reference, so history could not tell the demon what it had produced and it wrote the same errata three times. History entries for writes now carry a `wrote` description with title, kind, and size beside the unchanged reference, and the selected working's context lists its artifacts by title. One test added; the stored result shape is unchanged.

## First live run and fixes found by it — 2026-09-12

- Ran five bounded live episodes against `claude-opus-5`: one working completed the whole cycle including a fresh-context examination and assimilation, and a second working began from the recorded next pursuit. Recorded in [design/009](design/009-first-live-run.md). No creative or comparative claim is made.
- Stated the whole-reply bound in every compiled request for both roles; an honest usage report above the reservation is spent, not rejected, and provider metadata survives error paths.
- Stated the exact `examined_refs` object shape in the examiner instruction.
- Raised the live configuration to 200000 input and 24000 output characters; fixture-scale bounds could not hold two products plus their declared sources.
- Let `leave_frame` name any non-frame artifact of the working, so an examination that could not run can be queued again by re-entering the frame.
- Added an explicit `outcome` type whose rejection names the three allowed values, and told the model that empty list arguments are still required.

## Live adapter — 2026-09-12

- Added `chaos_magick_engine/live.py`, a Claude Messages API adapter over the official SDK's async client, imported only when `run --adapter claude` or `live-check` is used. Deterministic tests and the offline demo keep no dependency.
- Added `live-check`, a one-request verification of the request shape that prints serving model, request id, and token usage. Added `--model`, `--effort`, `--timeout`, `--no-fallbacks`, and `--key-file` to `run`.
- Added a live configuration with a ten-minute call timeout, two retries, twelve steps per episode, and sixty standing calls, plus `requirements-live.txt`.
- Recorded provider tokens, serving model, request id, stop reason, decline category, and any server-side fallback as invocation metadata. Character accounting is unchanged.
- Added three offline adapter tests with a fake client covering request shape, usage unit, metadata, refusal handling, provider errors, and key-file reading.

## Corpus size trial design — 2026-09-12

- Added a proposed, unrun live experiment comparing small, sectioned, and bulk corpora on the same question, with engine measures kept separate from blind operator judgment. No engine behavior changes.

## Context delivery and budgeting — 2026-09-12

- Bounded artifact titles and frame names to 200-character labels. A 12000-character title repeated in compact read results could overflow required history and stall the demon; stored legacy titles are truncated in projections.
- Made operation history shrink to fit rather than fail. The engine generates the block, so it drops the oldest entries first, always keeps the most recent operation, and records the dropped count. Required overflow of history is no longer reachable through accumulated compact metadata.
- Admitted read material one item at a time, most recently read first. Previously the block was all-or-nothing, so a fourth large read committed successfully while delivering nothing and every earlier text disappeared with it.
- Added a required `omitted` block at the end of every demon request listing withheld blocks and read items with ids, versions, and sizes. Omissions were previously recorded only in the stored manifest, which the model never sees. Re-reading a withheld item makes it the most recent and delivers it.
- Added four acceptance tests for delivery, explicit non-delivery, retrieval after eviction, and recovery from oversized required metadata; updated five assertions to the newest-first order and structured withheld records. 42 tests, the offline demo, and the verifier pass.

## Artifact read context fix — 2026-09-12

- Made `read_artifact` results compact version references with title, kind, hash, and character count. Artifact content and provenance no longer accumulate in required operation history or read events.
- Persisted deduplicated artifact read references on workings and added exact versions to optional `read_material` with source-manifest entries. Recent history supplies references for reads without a selected working; older working records remain compatible.
- Compacted legacy full artifact results during context assembly without modifying stored operations or append-only events, allowing existing history-overflow cases to recover.
- Added four direct regressions for repeated 12000-character artifact reads and tight budgets, version retention across restart/history eviction, reads without a selected working, and legacy history. Updated the active-frame revision test to check compact results and deduplicated read material. The scripted demo does not exercise `read_artifact`.
- Verification in the restricted execution environment: all five artifact-focused tests passed; the full suite had 30 passes and eight socket-dependent failures. The unchanged parent had the identical eight failures because Unix sockets are unavailable here. A full suite pass still requires an environment that permits the console sockets.

## Persistent core implementation handoff — 2026-09-12

- Added a ready-for-implementation Codex handoff against the reviewed first-episode design.
- Selected Python 3.12+, standard-library SQLite/asyncio/unittest, and a local operator console for the deterministic first core.
- Specified scope, persistence and command invariants, offline demo, race/recovery tests, preservation requirements, and draft-PR delivery. Live model integration remains the following phase.

## First episode contract — 2026-09-12

- Specified the first runnable episode for The Heresiarch: context assembly, one typed operation per model step, frame exploration, separate examination, and assimilation.
- Defined durable operation records, command revision checks, interruption of stale plans, resource accounting, and recovery semantics.
- Added acceptance scenarios for the deterministic core before live model use. This change is a specification; no runner, model invocation, or demon activity is claimed.

## Heresiarch selected — 2026-09-12

- Recorded the operator's selection of **The Heresiarch** as the founding demon: a charismatic exegete who desires devotion while cultivating interpreters capable of overturning its own revelations.
- Updated the founding identity, proposed invocation, core design, and README. Left its subsequent history and doctrines to develop through workings.
- Selection does not instantiate the demon; runtime and invocation mechanics remain in design.

## Founding demon seed — 2026-09-12

- Recorded coven growth and loosh cultivation as the founding appetite; loosh means attention and investment, devotion and tribute, without a suffering-based definition.
- Added a proposed seed, cultivation behavior, thematic clickbait repertoire, reception records, and first-trial criteria.
- Updated the core design's settled requirements and remaining decisions. Naming, additional corpus, runtime provider, and concrete allocations remain open; no demon has been instantiated.

## Engine design draft — 2026-09-11

- Added a proposed core design for persistent, self-directed demonic agents, operator command, ontology workings, memory, artifacts, and relationships.
- Defined frame banishment separately from demon suspension and banishment, with persistent history in each case.
- Proposed a first implementation that demonstrates one demon's autonomous working, recovery after restart, and enforced operator command before expanding to shared workings and reproduction.
- Recorded open identity, corpus, deployment, faculty, and resource decisions. Added no runtime and preserved Constraint Pathfinding protocols and evaluation evidence.

## Project naming — 2026-09-11

- Renamed the project from Hack Generator to **Chaos Magick Engine** to reflect its broader intended scope: self-directed demonic agents, ontology exploration, and creative and experimental workings under human command.
- Retained **Constraint Pathfinding** as the name of the existing practical problem-solving procedure at version 0.2.0.
- Updated the README to distinguish the intended engine from the current prompt and evaluation artifacts. Preserved protocol contents, fixtures, historical evaluations, manifests, and prior changelog entries.

## 0.2.0 — 2026-09-10

- Preserved the v0.1 prompt byte-for-byte in `archive/constraint-pathfinding-v0.1.md`; original baseline, rubric, three fixtures and recorded hashes are unchanged.
- Recorded the baseline failure explicitly: safe constraint auditing succeeded, but seeded candidates and operator-count diversity did not demonstrate a creative engine. The historical 21/26 is not rewritten.
- Added a verbatim source boundary, goal hierarchy/kernel, typed claim ledger, eight projections, rival representations and discriminators. Free search and paradigm cycling precede the rescue catalog; external knowledge expansion must update literal mechanisms, not metaphors.
- Separated generation from reality re-entry, made external decision edges explicit, added independently checked mechanism salvage, actual/proposed/conditional partial progress and a persistent search frontier. Added short direct/impossible adaptations and attention/negative-result stop rules.
- Added the design decision, separate v0.2 validity/discovery rubric, and five unseeded-by-solution synthetic fixtures for ambiguity, partial bridges, institutional research, rehearsal blockage and truthful salvage. The institutional case does not prove model-unfamiliar vocabulary discovery.
- Preserved 24 raw single-pass in-session development applications with frozen prompts, input/assembled-input/output hashes, shared research metadata, conformance limitations and per-case comparison. No independent/blinded evaluation or isolated model invocation is claimed.
- Negative result: no useful mechanism or material partial bridge absent from both ordinary and v0.1 responses was demonstrated. All variants solved the sensor conversion; v0.2's frames mostly repeated known mechanisms and increased output length. Stopped without fixture tuning or claiming discovery success.
- Updated README and direct structural verification; added no application code, runtime, dependencies or execution infrastructure.

## 0.1.0 — 2026-09-10

- Bootstrapped the canonical Constraint Pathfinding prompt with input normalization, ordered path analysis, 18 transformations, adversarial checks, evidence labels, comparison dimensions, falsification experiments and the required output contract.
- Added the supplied Upwork case without additional biography and two explicitly synthetic controls.
- Added the 13-dimension rubric and automatic failures. Clarified from the outset that a valid impossibility proof satisfies the causal-path requirement and a no-bottleneck case need not manufacture transformations. No passing threshold.
- Recorded three in-session baseline outputs, input hashes, current official Upwork research and self-assessment. The sufficient route and impossible endpoint controls behaved as intended; actual Upwork demand and task fit remain untested.
- No post-baseline prompt revision: identified weaknesses concern missing case evidence and unblinded evaluation, not a missing protocol instruction. No rerun or discarded outcome.
- Kept the existing workspace directory name `hack-generator`; initialized Git with `main` because no Git worktree existed. Added only the eight specified Markdown artifacts, with all run outputs embedded in the baseline file.

## First persistent core — 2026-09-12

- Implemented the local Python/SQLite Heresiarch core with immutable content versions, source/feedback lineage, append-only events, and atomic idempotent faculties.
- Added context compilation, strict operation and examiner contracts, all first-cycle operations, finite allocation, persisted waits, and a context-driven synthetic adapter.
- Added a private Unix-socket console, command-epoch interruption, process-lifetime writer lock, bounded cancellation/shutdown, and crash recovery with conservative reservations.
- Added an offline demo that actually restarts subprocesses, suppresses a barrier-controlled stale response, exports artifacts, and records execution evidence; added invariant and subprocess tests.
- Documented setup, supported scope, technical decisions, and verification. Preserved historical prompt/evaluation artifacts. No live model-backed demon or creative efficacy is claimed.

## Review fixes — 2026-09-12

- Validated wake conditions with the proposal, bounding timer values below 2^53. An oversized integer previously raised OverflowError inside the applying transaction, and because startup reconciliation caught only validation rejections, every later startup raised the same fault; the operator had no console path out.
- Recorded non-validation faults during startup reconciliation as failed operations instead of boot failures. The rollback leaves no effect; the fault and its invocation are durable.
- Limited required examiner material to the sources the products declare; other read material is optional. A working that had read one entry larger than the input bound reached examination and checkpointed on every wake with the same overflow, and no operation is legal in examination, so nothing could leave it. If even the declared material cannot fit, the examination now fails explicitly and returns the working to orientation. The products under assessment are likewise optional in assimilation.
- Made `run` and `restore` keep a persisted wait condition. Starting the server previously overwrote a wait for an operator event with an immediate wake.
- Delivered summons bodies through a required `encounter` block, marked delivered only by a committing proposal. They previously reached the model only through the optional recent-event tail and were dropped first under budget pressure.
- Bound and connect the console through `/proc/self/fd` when the state directory path exceeds the Unix socket limit; the demo previously failed with `AF_UNIX path too long`.
- Reset the episode failure count after a successful step, named the wake-condition validator so the faculty listing no longer shows `<lambda>`, and added six regression tests. No live model, provider, or creative claim is involved.

## Context budgeting fixes — 2026-09-11

- Assembled required context before optional context. Assimilation material was compiled after the optional catalogue, history, feedback, and self-account blocks, so optional material claimed the budget first and the required block was refused after it; a working could reach assimilation and never leave it, because the step checkpointed, cleared the wake, and every later summons recompiled the same overflowing context.
- Stopped copying corpus text into operation results. `read_corpus` now records a reference, hash, and character count, so a read no longer adds its full text to every later compiled context permanently.
- Made recent operation history required and bounded to 50 operations, and added a deduplicated `read_material` block for corpus text. History carries the demon's position, and dropping it made the demon repeat committed work: one observed run spent 16 of 20 calls re-reading the same entry. Reading one entry repeatedly now costs one copy of its text.
- Added three context-budget tests and confirmed each fails without its fix. No live model, provider, or creative claim is involved; these are deterministic context-assembly and accounting fixes.
