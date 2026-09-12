# Changelog

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
