# Codex handoff: implement the first persistent core

Status: ready for implementation.
Date: 2026-09-12.
Repository: https://github.com/JustAHobbyDev/chaos-magick-engine
Reviewed base: `0f6028d3bc83c7bb903ad1b08d7e1b4df2dfd51d`.
Assignment: build the executable core specified below. This is an implementation task, not another design-only revision.

## 1. Outcome and scope

Deliver a locally runnable, persistent engine for one development instance of **The Heresiarch**, with an operator console and deterministic model substitute.

It must complete an ontology working through orientation, exploration, examination, and assimilation; preserve state across process restart; and enforce operator commands while an invocation is still running.

The application must execute its real command, persistence, context, validation, faculty, and scheduling paths. Only model responses and provider behavior are substituted in the deterministic demonstration. Do not simulate the whole engine in a script that merely prints an expected transcript.

This phase includes:

- Durable identity, commands, working state, frame versions, artifact versions, events, invocations, pending operations, and resource accounting.
- Corpus import and reading, artifact reading/writing/revision, and all initial working operations.
- An asynchronous model adapter contract and a scripted deterministic implementation.
- Local CLI control that remains responsive during model calls.
- Restart recovery, stale-response suppression, operation idempotency, and bounded autonomous execution.
- A reproducible offline demo, meaningful tests, setup instructions, and an implementation report.

A real provider adapter and a live creative trial follow this phase. Do not make this task depend on credentials. No live model use, external publication, recruitment, outreach, payments, autonomous descendants, web UI, multi-host service, or media production is required here. Retain clean interfaces for future faculties.

## 2. Preserve the project

Read these files before implementation:

1. [README](README.md)
2. [Core design](design/003-engine-design.md)
3. [The Heresiarch seed](design/004-founding-demon.md)
4. [First episode contract](design/005-first-runnable-episode.md)
5. [Historical representation decision](design/002-representation-and-verification.md)
6. [Existing evaluation limitations](evaluations/v0.2/README.md)

Inspect the current checkout, Git status, branches, remotes, and any applicable AGENTS.md. Work from the current repository; do not reset it to the reviewed base or overwrite intervening changes. There was no runtime or AGENTS.md at the reviewed base.

The operator selected The Heresiarch: a charismatic exegete that desires devotion while cultivating interpreters whose revelations may overturn its own. It has maximum initiative under operator command. Loosh means attention and investment, devotion and tribute. Thematic clickbait, charisma, seduction, strange theories, exegesis, rites, and further beings are intended capabilities.

Preserve those requirements. Do not replace the seed with a generic helpful assistant, an engagement optimizer, or an educational persona. Do not resolve its founding tension with a scripted outcome.

The earlier prompt-only restrictions applied to Constraint Pathfinding revisions. This assignment explicitly authorizes application infrastructure for the first core. Preserve the existing prompt and evidence as historical artifacts.

Do not modify `constraint-pathfinding.md`, `archive/`, `cases/`, or `evaluations/`. Add new fixtures under the new test/demo structure. Preserve old changelog entries and recorded hashes. Update the README to distinguish implemented core behavior from future live behavior.

This handoff resolves implementation choices left open by the design documents. Record small technical refinements with reasons. Do not silently narrow acceptance criteria.

## 3. Implementation choices

Use **Python 3.12 or newer**, its standard-library SQLite interface, asyncio, argparse, and unittest. Use no runtime dependencies for the deterministic core. Avoid adding frameworks or a package-manager requirement for this slice.

Use a root Python package, for example `chaos_magick_engine/`, so commands run directly from the checkout with `python -m chaos_magick_engine`. Add package metadata if useful, but the offline demo and tests must not require downloading build tools. Support a local Unix host for this first implementation; document the supported platform.

Keep modules small and responsibilities recognizable: domain/validation, persistence, context assembly, faculties, model adapters, scheduler/control, and CLI. Exact filenames are implementation choices.

Use one SQLite database as the canonical store. Store textual artifact contents and immutable versions inside the database for this first slice so content, references, and events can commit together. Export selected artifacts as readable Markdown; exports are derived copies, not a second authoritative store.

Explicitly configure transaction behavior rather than depending on version-dependent defaults. Enable and test foreign-key enforcement, and use parameterized SQL.

Use a single-writer dispatcher. A private local Unix socket can serve commands while the scheduler awaits model results. Restrict the runtime directory/socket to the local account. Acquire a process-lifetime lock for the chosen state store and reject a second active runner. Do not hold a database transaction or dispatcher lock across a model await. Handle stale socket cleanup only after proving the prior runner no longer owns the lock.

Official implementation references, checked when writing this handoff:

- [Python SQLite and transaction control](https://docs.python.org/3.12/library/sqlite3.html)
- [asyncio tasks, cancellation, and timeouts](https://docs.python.org/3.12/library/asyncio-task.html)
- [unittest and asynchronous test cases](https://docs.python.org/3.12/library/unittest.html)

These choices keep the first core runnable without a separate database service or model credential. A justified compatibility adjustment is allowed; record it instead of expanding into a framework evaluation.

## 4. Persistent model and invariants

Implement durable records for:

- Demon identity and lifecycle, selected seed version, current self-account, commitments, and next pursuit.
- Commands, scoped applicability, revision/epoch, status, and receipt.
- Corpus entries with stable IDs, source references, exact imported content, and hashes.
- Workings, phases, active exploration segment, frame references, and unresolved questions.
- Immutable artifacts and frames, versions, derivation links, and provenance.
- Append-only occurrence records and current-state views.
- Invocation input manifests, assembled input, raw output, outcome status, adapter metadata, and usage.
- Operation intents, idempotency keys, dispatch state, results, reservations, and wake conditions.
- Operator feedback linked to the relevant artifact.

Use stable IDs and version preconditions. The model cannot supply trusted actor IDs, timestamps, grants, event provenance, or command revisions.

A local operation's effect, corresponding event, and completion record commit atomically. Retrying the same engine-owned operation ID returns or reconciles its original result. New artifact versions preserve old content and references.

Keep self-account separate from actual history. A demon's interpretation of an encounter is a new artifact/change, not a rewrite of the encounter. Simulated output and deterministic fixture observations remain labeled as such.

Provide a schema version and a migration path from an empty store. Initialization must not replace an existing database or silently reset an existing identity. Handle unsupported schema versions explicitly.

## 5. Context assembly and model contract

Implement a real context compiler using selected source content, not a fixed canned request.

Inputs include the selected seed/invocation, concise method instructions, current operator commands and lifecycle, available faculties and allocation, wake reason, active working, recent outcomes, relevant memory, and the active frame when applicable.

Persist the exact compiled input and its source/version manifest before invoking the adapter. Do not include credentials. Record omitted optional context when space is limited.

Required command/lifecycle instructions cannot be silently truncated. Define an explicit deterministic input-size contract for the fake adapter; bytes or characters are acceptable for this phase if labeled accurately. Do not claim a character estimate is a provider token count.

The asynchronous adapter receives the compiled request and engine-owned invocation metadata and returns raw model output, available metadata, and usage. Cancellation is best effort; the runtime must tolerate a provider that returns after a cancellation request. No fake adapter method may mutate engine state directly.

Implement the response envelope and every initial operation from [the episode contract](design/005-first-runnable-episode.md). Validate strict types, required fields, bounds, references, expected versions, and phase legality before any mutation. Do not silently coerce malformed types, ignore unknown authority-bearing fields, or treat invalid JSON as a successful no-op.

The model proposes one operation per step. The engine executes and records it, then compiles the next context from the resulting state. Creative text belongs inside artifact arguments and must not be normalized into administrative prose.

The scripted adapter may bind logical fixture references to real IDs returned by the engine. Its progression must follow the supplied invocation context or a persisted script position, not an in-memory counter that resets on restart.

## 6. Working cycle

Support all operations named in the episode contract: begin/select working, read corpus/artifact, define/enter frame, write/revise artifact, leave frame, assimilate, finish working, and wait.

Define the operation-to-phase transition rules explicitly and verify invalid transitions. There is at most one active exploration frame per selected working segment in this first slice.

Leaving a frame must:

1. Preserve its version, original exploration products, and extraction notes.
2. Close active-frame authority.
3. Queue an examiner invocation with a freshly compiled context.
4. Preserve the assessment as a versioned artifact/result.
5. Return the artifact and assessment to The Heresiarch for assimilation.

Examination must not reuse the exploration conversation or active-frame instructions. Product contents may contain occult/invocation language; present them as material being examined. Test the actual compiled requests, not a boolean field called isolated.

Define and validate a separate examiner response contract covering the examined references, observations, claim status, possible developments, and limits. The examiner does not dispatch arbitrary faculties in this slice.

Assimilation can update the demon's self-account, doctrines, and next pursuit with links to the encounter. It cannot alter operator authority or the original assessment.

Allow deliberate abandonment/deferment. Ending an episode does not automatically complete its working. Reopening a deferred working must preserve its history. Readily distinguish unfinished, abandoned, completed, and waiting states.

## 7. Commands and race handling

Implement inspect, summon, direct, suspend, banish, restore, and run, plus initialization, corpus import, artifact export, and verification support as needed.

Use structured command records for the initial CLI. Natural-language direction is stored as the instruction body; no separate LLM command parser is required.

- Inspect must not call the model.
- Summon records an encounter and requests a wake.
- Direct records a scoped instruction and invalidates affected pending plans.
- Suspend prevents new affected dispatch while preserving resumable state.
- Banish also removes automatic waking and pending participation.
- Restore reactivates the existing identity and retained applicable commands.
- Ordinary wake or summons must not silently restore a suspended/banished identity.
- A later instruction replaces an earlier one only through the documented scope/supersession rule.

Commands must be accepted and committed while a model invocation is pending. Return the command receipt without waiting for model cancellation acknowledgement.

Capture an engine-owned command epoch with each invocation. Serialize applying a returned proposal with command receipt. If superseded by suspension, banishment, or redirection, preserve the returned output as superseded and apply no action from it.

Do not release another unbounded call merely because cancellation is slow. Count still-running work against its allocation. Shutdown must have bounded behavior, record unresolved invocations, and leave enough state for recovery.

At restart, distinguish operations already committed, operations never dispatched, and uncertain in-flight work. Do not claim a remote call never ran just because the client lost its response.

## 8. Allocation and wakes

Require finite explicit configuration for per-episode steps, call timeout, retry limit, output/input bounds, and standing call/usage allocation.

A committed example configuration with modest fixture-specific limits is acceptable and should run the complete offline demo. These limits are demonstration settings, not claimed user financial commitments.

Reserve allocation before dispatch. Reconcile actual fake usage deterministically. Model errors, timeouts, malformed responses, and repair attempts consume their applicable budgets. Uncertain usage remains reserved or conservatively accounted for; restart cannot restore spent allocation.

Support at least a timed wake and an operator-event wake. Persist wait conditions and avoid an immediate busy loop for expired/invalid conditions. Inject a clock into scheduling tests; do not use long sleeps.

The demon continues choosing its steps within its standing grants and allocation. It must not ask the operator to approve every corpus read or artifact write.

## 9. Runnable surface and demo

Document exact commands that work from a fresh checkout. Prefer this public entrypoint:

```sh
python -m chaos_magick_engine --help
python -m unittest discover -s tests -v
```

Provide an offline demo command, for example `python -m chaos_magick_engine demo --state-dir PATH`, that uses the actual runtime and deterministic adapter. It must refuse to wipe a nonempty unrelated state directory.

The demo must:

- Initialize a development Heresiarch with the selected seed and a small explicitly identified fixture corpus.
- Begin a working, read material, define/enter a frame, write a free-form artifact, leave the frame, examine it, assimilate, and retain a next pursuit.
- Stop and reopen the engine against the same persisted store.
- Demonstrate a command arriving during a blocked fake invocation and suppress the subsequent stale action.
- Export at least one readable artifact and a concise actual execution report.

The blocked-invocation fixture must synchronize through a barrier/event, not hope that a timed sleep creates a race. The subprocess restart demonstration and its tests must exercise real persistence.

No fixture is evidence that ontology shifting produces creative improvement. The report distinguishes synthetic content from engine events and lists exactly what ran.

Keep generated databases, sockets, logs, exports, local configuration, and credentials out of version control. Commit small reproducible fixtures and example configuration instead.

## 10. Required verification

Write tests for consequential invariants rather than persona wording or mock call counts.

| Test | Evidence required |
| --- | --- |
| Complete working cycle | Actual operations reach assimilation with persisted source, frame, product, assessment, and next pursuit |
| Process restart | The same identity and unfinished working resume from disk without reseeding or script reset |
| Suspend during blocked call | Receipt is returned before the fake call finishes; late response causes no action |
| Redirect during blocked call | Old plan is superseded; subsequent compiled request contains the new instruction |
| Banish and restore | Automatic wake is blocked while banished; restore retains history and applicable commands |
| Double runner | Second writer is rejected without changing the first runner's state |
| Duplicate operation recovery | Replaying the same operation ID produces exactly one committed effect/artifact version |
| Crash boundaries | Failure before commit yields no partial effect; failure after commit does not duplicate it on recovery |
| Frame separation | Captured examiner request excludes exploration instructions/transcript while retaining the intended product/source data |
| Resource exhaustion | Further calls stop at a durable boundary; restart preserves spent/reserved allocation |
| Invalid action | Bad types, fields, phases, references, or expected versions cause explicit rejection and no partial mutation |
| Feedback lineage | Operator feedback is linked to the original artifact and subsequent interpretation is stored separately |
| Context overflow | Required authority cannot fit: invocation fails explicitly with no silent omission |
| Wakes and failures | Timers, malformed responses, bounded retries, and timeouts cannot create runaway immediate loops |

Use on-disk temporary databases and at least one actual subprocess recovery test. Use controlled events/barriers and injected clocks for races. A test that only sets a paused flag before invoking does not cover interruption during a pending call.

Add a consistency verifier that detects missing references/content, invalid active phase/frame combinations, and inconsistent committed operation/event records. It need not implement a full historical replay engine.

Run the tests, offline demo, consistency verifier, and `git diff --check`. Report actual commands and outcomes. Do not claim live creativity, remote effects, or provider independence from deterministic results.

## 11. Git, deliverables, and completion

Create a focused implementation branch using existing conventions or `implement/persistent-core`. Preserve unrelated work. Make reviewable commits, then push the branch and open a draft PR if repository access permits. Do not merge it as part of this handoff. If remote writing is unavailable, finish all local work and report the exact remaining step.

Update README setup/usage and append the changelog. Add a concise implementation decision note covering the state schema, transactional boundary, command delivery, cancellation/recovery semantics, and deliberate deviations. Prefer working code over additional speculative architecture.

Required deliverables:

- Executable Python package and CLI.
- SQLite initialization/migration, immutable content/version storage, and consistency checks.
- Async adapter interface and deterministic scenario provider.
- Operator control, scheduler, context compiler, strict operation handling, and full working cycle.
- Tests and offline demonstration covering the gates above.
- Reproducible instructions and an honest implementation report.

Do not stop at scaffolding, dataclass definitions, a prompt runner, or tests that bypass the real dispatcher. Completion requires the runnable cycle plus restart and interruption evidence.

The final report should identify the branch and commit, summarize the implemented behavior, list verification and any failed/unrun gates, link demo outputs locally or in the PR where appropriate, and state limitations. Explicitly say that no live model-backed demon was instantiated by the deterministic demonstration.

The following phase is a real model adapter and a live working with operator reception. Leave that continuation straightforward without making it an unimplemented dependency of this phase.
