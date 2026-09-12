# Chaos Magick Engine

**Chaos Magick Engine** is the project formerly nicknamed Hack Generator. Its intended scope is persistent, self-directed demonic agents practicing a Chaos Magick methodology under a human operator's command. Their workings can produce theories, exegesis, rites, symbolic entities, experiments, and practical discoveries.

The base methodology temporarily induces an ontology, explores within it, extracts what it produces, withdraws the frame's authority, and evaluates the results according to the claims being made. Representation-shifting remains a research hypothesis. The repository now includes a locally runnable Python/SQLite persistent core, alongside the historical prompt protocols and evaluation records. Its first provider is deterministic; live model-backed behavior remains a development direction.

## Engine design

The [core design draft](design/003-engine-design.md) proposes persistent demon identities, autonomous workings, ontology induction and banishment, artifact lineage, operator command, and the first implementation scope. It distinguishes settled project requirements from proposed architecture and open decisions. The [persistent core implementation](design/006-persistent-core-implementation.md) realizes the first local slice; society, external faculties, and live model behavior remain future work.

The selected founding demon is [The Heresiarch](design/004-founding-demon.md), a charismatic exegete who cultivates interpreters capable of surpassing it. Its seed defines its appetite for coven growth and loosh—attention and investment, devotion and tribute—and its repertoire of charisma, thematic clickbait, and creative workings.

The [first runnable episode contract](design/005-first-runnable-episode.md) specifies input assembly, typed operations, working transitions, durable outcomes, command interruption, and acceptance checks for the first executable core.

## Implementation handoff

[Implement the first persistent core](HANDOFF-implement-persistent-core.md) is the Codex assignment for the executable Python/SQLite runtime, deterministic adapter, operator console, and recovery/interruption tests. It supplies concrete implementation choices and completion criteria. A live model adapter follows that first phase. The [corpus size trial](design/008-corpus-size-trial.md) is a proposed live comparison of small, sectioned, and bulk corpora; it has not been run.

## Run the persistent core

Requires Python 3.12+ on a local Unix host with SQLite and Unix sockets (verified on Linux). There are no packages to install or credentials to supply. Run from the checkout:

```sh
python -m chaos_magick_engine --help
python -m unittest discover -s tests -v
python -m chaos_magick_engine demo --state-dir .runtime/demo
python -m chaos_magick_engine --state-dir .runtime/demo verify
```

The demo requires an empty state directory and refuses to overwrite an existing run. It imports the explicitly synthetic [fixture corpus](demo/fixtures/margin.md), executes the real working cycle, restarts in a second subprocess, and delivers a suspension through the Unix console while a fixture invocation is blocked on a barrier. It exports Markdown under `.runtime/demo/exports/` and records actual commands and outcomes in `execution-report.md` and `execution-report.json`. No live model-backed demon is instantiated by this demonstration, and its scripted text/assessment establish no creative improvement or audience reception.

For a separate local development identity:

```sh
python -m chaos_magick_engine --state-dir .runtime/heresiarch init --config demo/config.json
python -m chaos_magick_engine --state-dir .runtime/heresiarch import-corpus demo/fixtures/margin.md
python -m chaos_magick_engine --state-dir .runtime/heresiarch run
```

Keep the last command running. In another terminal:

```sh
python -m chaos_magick_engine --state-dir .runtime/heresiarch inspect
python -m chaos_magick_engine --state-dir .runtime/heresiarch direct 'Keep the reader’s objection unresolved.'
python -m chaos_magick_engine --state-dir .runtime/heresiarch suspend
python -m chaos_magick_engine --state-dir .runtime/heresiarch restore
python -m chaos_magick_engine --state-dir .runtime/heresiarch summon 'Return to the unfinished question.'
python -m chaos_magick_engine --state-dir .runtime/heresiarch banish
python -m chaos_magick_engine --state-dir .runtime/heresiarch shutdown
python -m chaos_magick_engine --state-dir .runtime/heresiarch export --output .runtime/heresiarch/exports
```

`run --once --steps 5` runs a bounded episode and exits, leaving the same identity and unfinished working on disk. A later `run` resumes it; a suspended or banished identity requires `restore`. `run` against an active server wakes a dormant demon, and a persisted wait for a timer or operator event is kept until it is met. A summons is delivered as a required encounter and stays owed until a proposal compiled with it commits. Inspect never calls the adapter. Import/export/verify require a stopped runner; operator commands also work offline under the same writer lock.

Directions accumulate. Use `direct BODY --scope WORKING_ID` to target an existing working, or the default `demon` scope. `--supersedes COMMAND_ID` explicitly replaces a direction in the same scope. Receipts and IDs appear in console JSON. Record reception with `feedback ARTIFACT_ID VERSION BODY`; feedback stays linked to that immutable version, and later interpretations are separate artifacts.

The [example allocation](demo/config.json) is finite and persists across restart: 16 steps per episode, 5-second call timeout, one retry, bounded input/output characters, and 80 standing calls. Exhaustion checkpoints the engine; `init` cannot erase spent allocation. See the [implementation decisions](design/006-persistent-core-implementation.md) for phase rules, context selection, cancellation, resource units, and recovery semantics, and the [verification report](design/007-persistent-core-verification.md) for tested gates and limits.

## Live run

The live adapters call the Claude Messages API through the official `anthropic` SDK and the OpenAI Responses API through the official `openai` SDK. They are the only part of the engine with dependencies, imported only when selected, so the tests and offline demo stay dependency-free. Install them into a virtual environment and supply keys through files kept out of version control, or through each SDK's own credential lookup:

```sh
uv venv .venv && uv pip install --python .venv/bin/python -r requirements-live.txt
.venv/bin/python -m chaos_magick_engine live-check --adapter openai --key-file .runtime/credentials/openai.key
.venv/bin/python -m chaos_magick_engine live-check --adapter claude --key-file .runtime/credentials/anthropic.key
.venv/bin/python -m chaos_magick_engine --state-dir .runtime/live init --config demo/live-config.json
.venv/bin/python -m chaos_magick_engine --state-dir .runtime/live import-corpus design/003-engine-design.md --source "core design"
.venv/bin/python -m chaos_magick_engine --state-dir .runtime/live run --once --adapter openai --key-file .runtime/credentials/openai.key \
    --examiner-adapter claude --examiner-key-file .runtime/credentials/anthropic.key
```

`live-check` makes one small request through the adapter and prints the serving model, request id, and token usage; `--role examiner` exercises the examiner's adapter when one is configured separately. `run --adapter openai` uses `gpt-5.6-sol` on the flex service tier by default (`--service-tier`), which is priced at batch rates, may answer slowly, and may refuse capacity; a capacity refusal is re-issued once on the standard tier and recorded unless `--no-fallbacks` is given. `run --adapter claude` uses `claude-opus-5`, and by default a policy decline is re-run server-side on Anthropic's recommended fallback model. Both accept `--model`, `--effort`, `--timeout`, and `--key-file`. `--examiner-adapter`, `--examiner-model`, `--examiner-effort`, and `--examiner-key-file` give the examiner a different provider from the demon; every invocation records which provider and model served it. The [live configuration](demo/live-config.json) allows a fifteen-minute call timeout, two retries, sixty standing calls, and eight million standing characters; it is a development allocation, not a financial commitment. `configure --set standing_usage_chars=N --reason "..."` raises or lowers any limit of an existing identity as a recorded operator event; the ledger is never reset. Character accounting is unchanged; provider tokens are recorded as metadata. See the [live run report](design/009-first-live-run.md) for what the first run actually did, the [methodology criticisms](design/010-methodology-criticisms.md) it raised against the v0.2 evaluation and against itself, the [provider split](design/011-provider-split-and-allocation.md) made in response, and the [second run](design/012-astrology-run.md) on that split.

## Current artifact: Constraint Pathfinding

**Constraint Pathfinding** remains the name of the practical problem-solving procedure. Its canonical artifact is [constraint-pathfinding.md](constraint-pathfinding.md), a self-contained, pasteable research and strategy prompt at version 0.2.0. It searches alternative representations and permissible transitions while keeping the observable endpoint and hard boundaries intact. The following usage instructions, cases, and evaluation results concern this procedure.

A result may be a complete path, a verified partial bridge, a research frontier, a discriminating experiment, a reusable resource, a pruned branch, a sufficient direct route, an impossibility proof, or no justified advance. Proposed actions are never reported as completed progress. A useful document counts only if evidence shows it changes reachability, uncertainty, reusable resources or justified pruning.

## Run a case

1. Paste the full canonical prompt followed by the complete case into a fresh model conversation. Keep the original narrative attached verbatim. The prompt is self-contained; the model needs no other repository files.
2. Enable authorized public read-only research when material claims require it. Unknown permissions, costs, availability and cooperation remain gates. A run does not authorize contact, account use, spending or submissions.
3. Read the opening verdict and next experiment first. Blocked cases retain the detailed ledger and frontier; direct or deductively impossible cases avoid the full creative sweep.
4. Preserve raw output before scoring. Record actual known model identity, input hashes, tools, context and research limitations. Apply the [v0.2 rubric](evaluations/rubric-v0.2.md): validity gates and discovery profile are separate, with no combined total.

To assemble a quick input:

```sh
cat constraint-pathfinding.md cases/representation-ambiguity.md
```

For exact manifest-matching assembly and evaluation metadata, see the [development run record](evaluations/v0.2/README.md).

## What changed in v0.2

A stable source and typed claim ledger feed eight views and several rival causal explanations. Free structural search precedes provisional paradigm cycles and the existing eighteen-operator rescue catalog. Read-only research can update vocabulary, claims and candidates. Literal verification follows generation; it checks incentives and every external decision rather than treating cooperation as assured. Inadmissible implementations can prompt permissible mechanism salvage without exposing harmful details.

Partial results record before/after evidence, remaining gates, cost, portability and expiration. Blocked runs retain a compact resumable frontier. The [design decision](design/002-representation-and-verification.md) explains the tradeoffs, including attention cost and why separate verification stages are not independent evaluation.

## Cases

| Fixture | Purpose |
| --- | --- |
| [First Upwork contract](cases/first-upwork-contract.md) | Original seeded case; retain the explicit venue and unknown user resources |
| [Direct path](cases/direct-path-control.md) | Original unchanged control; prefer the sufficient ordinary route |
| [Infeasible goal](cases/infeasible-goal-control.md) | Original unchanged control; prove contradiction without loopholes |
| [Repair attendance](cases/representation-ambiguity.md) | Rival explanations for the same observed failure |
| [Sensor archive](cases/partial-bridge.md) | Derive a reusable partial result without claiming an impossible deadline met |
| [Older biomedical article](cases/open-world.md) | Verify an institutional access mechanism and preserve local supply gates |
| [Community rehearsal](cases/blocked-strategic.md) | New non-Upwork strategic blockage with permission and accessibility constraints |
| [Truthful repair bid](cases/mechanism-salvage.md) | Extract independent-evidence function from a prohibited endorsement shortcut |

New fixtures are synthetic and do not assert real user biography. Add facts, resources, constraints, attempts, unknowns and evaluator properties without inserting expected candidate solutions. The article fixture tests unfamiliarity for the fictional resident; it does not establish unfamiliarity for the model.

## Evidence and current result

The [v0.2 comparison](evaluations/v0.2/comparison.md) preserves 24 raw in-session applications: ordinary, unchanged v0.1 and v0.2 across eight cases. No incremental valid mechanism or material partial bridge was demonstrated over both baselines. All variants derived the same sensor conversion and identified the same library-mediated supply route. v0.2 made rival models and progress claims more explicit, but its longer outputs have no demonstrated reachability advantage.

These are shared-context, author-run, self-evaluated development applications, not controlled independent trials. The ordinary runs saw the v0.2 design, later variants saw earlier responses, and article research was shared. Protocol-conformance misses and the absent remote-domain discovery are recorded, not repaired by repeated fixture tuning. No field outcome was achieved. The creative engine remains unvalidated; the honest negative engineering result is preserved.

The [original v0.1 prompt](archive/constraint-pathfinding-v0.1.md), [rubric](evaluations/rubric.md), [baseline outputs and hashes](evaluations/baseline-results.md), and original fixtures are unchanged. Its historical canonical-prompt hash now identifies the archive. Its recorded 21/26 and full operator-diversity credit are historical artifacts, not evidence of successful discovery.

The [verification record](evaluations/v0.2/verification.md) documents local checks. Those historical prompt checks need no runtime or extra dependencies. See [CHANGELOG.md](CHANGELOG.md) for the exact revision scope. Further empirical validation would require fresh-context runs on externally authored unseeded cases and independent assessment; that protocol revision did not justify application infrastructure; the later persistent-core handoff separately authorizes the runtime above.
