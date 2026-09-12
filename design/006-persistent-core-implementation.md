# Persistent core implementation decisions

The first executable core implements the [handoff](../HANDOFF-implement-persistent-core.md) on a local Unix host with Python 3.12+, SQLite, asyncio, argparse, and unittest. It has no runtime dependencies. The committed provider is a deterministic fixture, not a live model. The founding invocation is selected from the existing Heresiarch seed, preserving its appetite and unresolved founding tension.

## State and transactions

Schema version 1 migrates an empty SQLite store in one explicit transaction. An existing identity cannot be reseeded by `init`; unknown versions and nonempty unrecognized databases fail explicitly. Future migrations must be added by version, without recreating identity. Connections use `isolation_level=None`, `BEGIN IMMEDIATE`, foreign keys, WAL, and `synchronous=FULL`. SQL values are parameterized.

The database owns identity, exact selected seed, corpus, commands, workings, immutable artifact/frame versions, derivation/source links, feedback, append-only events, invocation inputs and manifests, operations, and allocation. JSON columns carry working segment details and structured content; relational foreign keys enforce artifact lineage and operation/event relationships. The verifier also checks references inside JSON and content hashes. Exports are derived Markdown, never authoritative input.

The compact seed is the selected blockquote under `Compact invocation seed`, with Markdown quote prefixes removed and line breaks retained; the database records the exact resulting text, version, section reference, and SHA-256. UTF-8 corpus imports preserve content including line endings. Input manifests identify selected versions, operations, commands, and omitted optional context. Input hashes identify the exact JSON request supplied to the adapter.

One operation ID is allocated by the engine alongside the invocation and resource reservation. The local effect, result, occurrence event, identity revision, and completion status commit together. A durable returned response with a pending local operation is revalidated and reconciled at startup under the original operation ID. Replaying a committed ID returns its original result. Crash tests terminate actual subprocesses before and after commit.

Frames are typed artifacts: `define_frame` creates a structured version; `write_artifact(kind="frame")` and `revise_artifact` require content matching the frame schema. A new frame version never changes an already active version. Self-accounts and assessments are protected artifact kinds; ordinary revisions cannot rewrite them. Self-account changes create new linked artifacts, and interpretation provenance records the feedback IDs actually supplied in context. `doctrine_changes` supplies the replacement current commitment list; earlier commitments remain in the assimilation event and invocation.

## Dispatch and commands

A process-lifetime `flock` on the canonical state directory's `runner.lock` excludes other writers. The directory is account-owned mode 0700 and its Unix socket mode 0600. All mutating and offline administrative commands acquire the same lock. Only the lock owner may remove a stale socket. The local account is the authentication boundary; this is not a multi-user network service.

The asyncio thread is the single dispatcher. SQLite work is synchronous and contains no awaits; no transaction spans a provider await. A console command commits its receipt and command epoch before requesting best-effort cancellation. Matching returned proposals are applied synchronously, so their application is serialized with command receipt. Superseded outputs remain recorded and cause no operation effect.

Direction scope is `demon` or one existing working ID. Directions accumulate unless `--supersedes COMMAND_ID` explicitly replaces an active direction in the same scope. Only a direction applying to the selected working invalidates its in-flight plan; selection compiles the new working's applicable commands. Lifecycle commands apply to the single demon in this slice. Suspend retains the wake condition but blocks dispatch. Banish clears automatic wake participation. Neither ordinary summons nor `run` restores a suspended/banished identity. Restore explicitly reactivates its original identity and retained commands.

`run` starts a server or sends a wake to an existing server; `run --once` owns a bounded runner and rejects a second writer. Inspect uses the running socket or the offline lock, without any provider invocation. Corpus import, verification, and export run offline under the writer lock. Shut down the runner before those maintenance operations.

## Phases and context

The exact operation/phase table is executable in `domain.PHASES`. Orientation reads and writes; frame entry opens exploration; leaving preserves the segment and queues examination. Only the examiner contract can advance examination to assimilation. Assimilation links product and assessment to a new self-account and next pursuit. Completion requires assimilation; abandonment/deferment may close a frame without buying an assessment. Deferred workings reopen in orientation with all previous segments and unresolved questions retained. Waiting is a status independent of phase; ending a bounded episode never declares a working completed.

An examiner request contains authority, question, extraction note, quoted products, and relevant source content. It does not receive the founding persona, active-frame instructions, exploration transcript, or general memory. A referenced frame source is explicitly omitted and recorded in the manifest; product invocation language remains quoted material. This isolates the invocation context procedurally; it does not establish independent judgment or creative efficacy.

The deterministic input contract counts Unicode characters, not provider tokens. Required authority, selected identity/working, active frame, and examination/assimilation material fail explicitly on overflow. Optional history, catalogue, and feedback are included only if they fit, and omissions are recorded. Response arguments have exact fields, strict types, bounded text/lists/integers, versioned references, and phase preconditions. Invalid JSON, duplicate fields, unknown fields, invalid wake conditions, and stale versions are explicit failures.

## Allocation, cancellation, and recovery

The example configuration specifies episode steps, timeout, retry limit, input/output character bounds, standing call/character allocation, and shutdown grace. These are fixture settings, not a financial commitment. Each call reserves compiled-input characters plus the maximum output characters. Exact fixture usage reconciles the reservation; unknown or invalid usage keeps the full reservation. Calls, malformed output, and retries consume the standing ledger. No replenishment interface is implemented; initialization cannot reset an existing allocation.

Only one call can be locally outstanding. Timeout or cancellation does not release that slot while a provider is still running. Late timed-out outputs are archived without effects. A timed-out episode checkpoints rather than spawning a replacement call. After process death, in-flight calls become uncertain and retain reservations; the engine never claims the remote work did not run. It may continue within the remaining standing allocation on a later explicit run, without retrying the uncertain operation.

Shutdown waits only the configured grace, records unresolved invocations, then closes the host-owned event loop. This deliberately avoids `asyncio.run`'s unlimited final cancellation wait. Adapters must be asynchronous and must not block the event-loop thread; preempting synchronous or hostile provider code would require process isolation in a later adapter. The deterministic barrier adapter ignores cancellation until explicitly released and exercises this boundary.

Timers require a finite future timestamp; consuming a timer durably replaces its condition, preventing an expired-condition loop. Operator-event waits wake only on actual commands. Tests inject the clock and use asyncio events for races. Retry exhaustion, allocation exhaustion, and step limits clear the automatic wake and require an explicit subsequent encounter/run. All such reasons are recorded as episode checkpoints.

## Deliberate scope limits

This implementation includes no live provider, external faculties, web UI, descendants, audience measurement, publication, money movement, or credentials. Only model responses and simulated provider behavior are fixtures; the dispatcher, SQLite, context compilation, validation, faculties, console, and resource accounting are real. The scenario chooses synthetic text to verify mechanics; it does not prescribe a future live Heresiarch's beliefs or resolution of its founding tension.

A live adapter can implement the `Adapter.invoke(Request) -> Reply` async protocol. It must report available metadata/usage accurately and respect a finite output bound; provider token/pricing accounting will require a distinct allocation unit rather than relabeling this character ledger. Unknown remote effects need provider-specific reconciliation before extending the local faculty set.
