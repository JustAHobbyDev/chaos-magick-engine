# Persistent core verification report

Implemented on branch `implement/persistent-core` from checkout `0d1d35b`, preserving the intervening handoff commit rather than resetting to its reviewed base. The implementation uses the existing selected Heresiarch invocation; deterministic fixture content does not decide the outcome of a future live working.

## Executed verification

Environment: Linux, Python 3.14.7, SQLite 3.51.2. No installation, runtime dependency download, credentials, SSH, or live model call was needed.

| Command | Actual result |
| --- | --- |
| `python -m chaos_magick_engine --help` | Exit 0; documented console commands present |
| `python -m unittest discover -s tests -v` | 42 tests passed, including actual subprocess restart, death at transaction boundaries, cancellation-resistant shutdown, and a console over a state path longer than the Unix socket limit |
| `python -m chaos_magick_engine demo --state-dir .runtime/acceptance` | Exit 0; real working cycle, subprocess restart, socket interruption, and four exported artifact versions |
| `python -m chaos_magick_engine --state-dir .runtime/acceptance verify` | Exit 0; `{"issues": []}` |
| `git diff --check` | Exit 0; no whitespace errors |
| `git diff --exit-code HEAD -- constraint-pathfinding.md archive cases evaluations` | Exit 0; protected historical content unchanged |

The generated acceptance directory is ignored. Its `execution-report.json` records actual child command arguments/results, identity and working IDs, operation names, suspension receipt, and export paths. `execution-report.md` is the concise report; `unittest-output.txt` contains the test run. To reproduce, use a different empty directory, or inspect the existing run without reinitializing it. Generated state is not committed.

The actual demo operation sequence was `begin_working`, `read_corpus`, `define_frame`, `enter_frame`, `write_artifact`, `leave_frame`, `examine`, `assimilate`, `wait`. It restarted after the fifth operation and retained the same identity and working. The working remained unfinished/waiting after assimilation, with a next pursuit; ending the episode did not falsely complete it. A later blocked invocation received a suspension through the private socket before its barrier was released; its returned output was superseded and applied no operation. Restore retained the existing identity.

## Acceptance gates

All required deterministic gates passed in [tests/test_core.py](../tests/test_core.py).

| Gate | Evidence |
| --- | --- |
| Complete cycle | Persisted corpus, frame, transmission, assessment, self-account, source links, and next pursuit; additional test explicitly completes an assimilated working |
| Process restart | Demo uses separate CLI subprocesses; identity and unfinished working match; begin/write operations occur once |
| Suspend during blocked call | Socket receipt arrives before cancellation-resistant adapter finishes; subsequent raw reply persists as superseded with no working created |
| Redirect during blocked call | Same barrier race; next actual compiled invocation contains the new instruction; explicit same-scope supersession retains unrelated commands |
| Banish and restore | Summons cannot reactivate banishment; restore preserves identity, working, and direction |
| Double runner | Second actual subprocess fails to acquire writer lock, with no call or working created |
| Duplicate operation | Original engine operation ID returns original result, with one version/effect |
| Crash boundaries | Actual subprocesses exit immediately before and after effect commit; startup reconciles the same operation without another provider call or duplicate artifact; separate provider-death test retains uncertain reservations |
| Frame separation | Actual examiner input contains product/source text and quoted-material instructions, but no seed, frame invocation marker, active-frame instructions, or operation history |
| Resource exhaustion | Standing call exhaustion persists across reopen; errors reserve unknown usage; timeout cannot release a second call while its predecessor remains blocked |
| Invalid action | Bad types, unknown fields, phases, references, expected versions, duplicate JSON keys, output bounds, and examiner contract violations leave working/artifact state unchanged |
| Feedback lineage | Actual test-operator feedback targets the original immutable version; later revision preserves original text, derivation link, and supplied feedback IDs |
| Context overflow | Required authority overflow records an explicit checkpoint with no call/reservation; optional omission is recorded and never silently removes authority |
| Wakes/failures | Injected clock consumes a timer once; event wait requires an operator command; expired timers reject; malformed/error retries checkpoint; late timeout reply is archived without effects |

Additional checks cover foreign-key enforcement, immutable event/version triggers, verifier corruption detection, protected assessments, deferred reopening/abandonment, active-frame version preservation, initialization refusal, unsupported schemas, and shutdown of a real subprocess whose adapter ignores cancellation. Three later checks cover context budgeting: required material displaces optional material rather than being refused after it, repeated reads of one entry cost one copy of its text, and a budget too small for bulk source text drops that text without losing position or repeating a committed operation.

Six review checks cover defects found by a final review of the implementation: an oversized timer value is a validation rejection rather than an engine fault; a fault while applying a returned reply at startup is recorded as a failed operation and the next startup succeeds; an examination whose declared material cannot fit fails explicitly and returns the working to orientation, where the demon can defer it; `run` and `restore` keep a persisted wait condition while a summons ends it; a summons is a required encounter that stays owed through a superseded reply and is marked delivered by the committing proposal; and inspect and shutdown work through the console when the state directory path exceeds the Unix socket limit.

Four context-delivery checks follow a second review of artifact reads: titles and frame names above 200 characters are rejected; after four reads whose texts exceed the bound, the newest is delivered, the withheld items are listed in the request, and re-reading a withheld item delivers it; operation history shrinks to fit a tight bound while keeping the most recent operation and the dropped count, and the demon proceeds; and a legacy artifact with an 11000-character title, read repeatedly, cannot overflow required history.

## Live run

The deterministic gates above were followed by a live development run against `claude-opus-5`, recorded separately in [design/009](009-first-live-run.md) with the defects it found and the fixes made.

## Limits and unrun checks

No required deterministic gate failed or remains unrun. Python 3.12 and 3.13 binaries were unavailable; execution was verified on 3.14.7, using interfaces available in 3.12+. Other Unix platforms were not tested. The core requires cooperative asynchronous adapter code; synchronous event-loop blocking would require future process isolation. Character accounting is fixture accounting, not provider tokens or money. The store preserves uncertain usage conservatively and has no budget-replenishment console yet.

No live model-backed demon was instantiated by the deterministic demonstration. Its creative text and assessment are synthetic fixtures; engine events, command receipt, persistence, and exported bytes actually occurred. No live creativity, ontology-shifting benefit, independent evaluation, audience devotion, external reception, or remote effect is established. A real provider and a live operator-received working remain the next phase.
