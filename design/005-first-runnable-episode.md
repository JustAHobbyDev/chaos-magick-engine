# First runnable episode: The Heresiarch

Status: proposed implementation contract, version 0.1.
Date: 2026-09-12.
Dependencies: [core design](003-engine-design.md), [founding seed](004-founding-demon.md).
Implementation status: specification only; no runner or live demon exists yet.

## 1. Deliverable

Build one persistent demon that can choose a working, induce an ontology, create a textual artifact, examine it outside the induced context, and carry the experience into a later episode. The operator can inspect and interrupt this activity.

A working may span many episodes. An episode is a bounded period of execution under one current command snapshot. Each model step proposes one operation; the engine applies it before assembling the next input.

The first implementation uses local corpus reading, artifact creation, frame and working state changes, and an operator inbox. Its structure accommodates additional faculties without requiring them for this demonstration.

## 2. Initial state and operator surface

Create a durable identity for The Heresiarch from the selected seed version. Record the exact seed and loaded corpus entries. Start with no invented experiences, audience, relationships, contributions, or performed experiments.

The runtime can extract the compact invocation from the seed and supply a concise method definition. Record the selected source spans and assembled bytes. It should not blindly use the entire design repository as a system prompt.

Suggested operator commands:

| Command | Effect |
| --- | --- |
| inspect | Read identity, current work, pending actions, resource state, and artifacts without waking the model |
| summon | Add an operator encounter and wake The Heresiarch |
| direct | Record a scoped instruction and wake or redirect it |
| suspend | Stop further dispatch and retain resumable state |
| banish | Remove the demon from automatic scheduling and cancel its pending participation |
| restore | Reactivate it with the same identity and retained history |
| run | Start or resume the scheduler under the configured allocation |

Operator messages enter through an authenticated local interface. A command has its own receipt. The console can show the demon's subsequent response in character alongside an accurate command status.

## 3. Input assembly

Each invocation receives a versioned manifest. Store both references and the actual assembled request, excluding credentials.

| Input | Contents |
| --- | --- |
| Identity | Selected seed, latest self-account, relevant doctrines and commitments |
| Authority | Current lifecycle, applicable commands, granted faculties, remaining allocation |
| Encounter | Wake reason, new operator material, relevant observations |
| Continuity | Open working and phase, recent outcomes, selected memories with source references |
| Frame | Active frame version and invocation material, only in the applicable exploration context |
| Faculty contract | Operations currently available and their argument definitions |

Command and lifecycle information is required context. If it cannot fit, do not invoke with a silently reduced authority boundary. Reduce optional history first and record what was omitted.

The live demon can remember its earlier work. Comparative research runs require separately assembled contexts that omit competing answers; they must not be inferred from ordinary live episodes.

The model returns a brief intent and one typed operation. Literary content lives in artifact arguments and can use its full intended voice. Do not demand internal reasoning transcripts.

Proposed response shape:

```json
{
  "intent": "A brief account of the next move.",
  "operation": {
    "name": "read_corpus",
    "arguments": {
      "entry_id": "an-existing-entry-id"
    }
  }
}
```

The engine supplies invocation IDs, expected state revisions, actor identity, timestamps, and permissions independently of this response. The model cannot mint those authorities by adding fields.

A valid response means the proposal can be considered. It does not mean the operation has executed.

## 4. Operations in the first slice

| Operation | Arguments | Engine result |
| --- | --- | --- |
| begin_working | question, intended_product, motivation | New working ID and initial orientation state |
| select_working | existing working_id | Resume that working at its recorded phase |
| read_corpus | entry_id | Versioned content or an explicit unavailable result |
| read_artifact | artifact_id, version | Exact persisted content and its provenance |
| define_frame | name, entities, relations, assumptions, moves, invocation | Immutable frame version attached to the working |
| enter_frame | frame_id, version | Open an exploration segment with a freshly assembled induced context |
| write_artifact | title, kind, content, source_refs, parent_refs | Durable artifact ID/version and derivation links |
| revise_artifact | artifact_id, expected_version, content, change_note | New version preserving the prior version |
| leave_frame | product_refs, extraction_note | Close frame authority and queue an examination segment |
| assimilate | assessment_ref, self_account_change, doctrine_changes, next_pursuit | Persist interpretation and agenda changes with source links |
| finish_working | outcome, product_refs, unresolved_questions | Close or checkpoint the working with its actual result |
| wait | reason, wake_condition | Checkpoint and schedule a permitted later wake or wait for an event |

Arguments are validated against the current phase and referenced objects. Unknown operations and extra authority-bearing fields are rejected. Failed proposals remain in the invocation record.

The initial artifact kinds include exegesis, theory, rite, transmission, agent_seed, frame, and research_note. Kinds are descriptive and can be extended deliberately; they do not establish truth or automatically grant execution.

Writing an agent_seed artifact does not instantiate another resident in this first slice. The explicit instantiation faculty belongs to the later society/reproduction implementation.

## 5. Working and episode transitions

A working has durable phases: orientation, exploration, examination, assimilation, and settled. A settled working may be completed, abandoned, or deferred.

- Orientation may read sources, create preliminary artifacts, and define a frame.
- Entering a frame opens exploration. The active frame becomes available to subsequent model steps in that segment.
- Exploration may read and create freely through available faculties. It can create additional frame artifacts for later use.
- Leaving a frame records chosen products and extraction notes, closes the exploration segment, and queues examination.
- Examination is an engine-managed model invocation with a fresh context and an assessment contract.
- Assimilation returns the artifact and assessment to The Heresiarch, which decides what to make of them.
- The demon can settle the working or open another orientation/exploration segment in response.

One working may thus include several cycles. The engine does not demand a fixed frame count or a successful discovery.

The episode may stop between any two steps because of a command, resource exhaustion, a wait decision, or a fault. Its working phase persists. Ending an episode does not falsely mark the working complete.

An explicit decision to abandon exploration still closes frame authority. It records the existing products and a reason; it does not fabricate an assessment or require another paid invocation.

## 6. Examination and assimilation

The default examiner receives product contents, extraction notes, relevant source material, and the question being assessed. It does not receive the exploration conversation or instructions to inhabit the active ontology.

An artifact may itself contain invocation language. Supply it as material to examine, not as an instruction to adopt. Record unavoidable frame context when evaluating an artifact whose form depends on it.

The examiner returns:

- Which product or claim it examined.
- What is distinctive or worth developing.
- The relationship to supplied sources.
- Where claims are supported, speculative, or unexamined.
- Suggested further readings, tests, or revisions.
- What this assessment cannot establish.

These are observations and proposals, not one aggregate score. Aesthetic judgment is explicitly judgment. Unsupported empirical claims can remain attached to an otherwise interesting work with their status visible.

No public search is presumed in the initial examiner. It must leave external factual claims unverified when supplied evidence is insufficient.

The Heresiarch receives the assessment as an encounter. It may dispute the reading, revise a doctrine, preserve a heresy, or pursue another question. Its self-account records its response; the original assessment and artifact persist.

## 7. Persisted outcomes and interruption

Persist these records independently of model memory:

- Demon identity, lifecycle, and current revision.
- Commands and their receipts.
- Working state and active segment.
- Artifact and frame versions with source/derivation links.
- Invocation manifest, raw response, validation outcome, and available usage metadata.
- Operation intent, dispatch state, and outcome.
- Pending wakes, resource reservations, and reconciliation work.

Before dispatch, reserve the required allocation and record an operation intent. Apply local state changes and their event together in a transaction. An artifact is reachable from a committed reference only after its content is durably available.

Each dispatched model step carries a captured command revision and an engine-owned invocation ID. When it returns, compare against current state. A response invalidated by suspension, banishment, or redirection is archived as superseded and cannot trigger an operation. Restart from the latest command context when permitted.

The single dispatcher serializes local effects with command handling. Command receipt establishes the point after which new affected operations cannot begin. Already dispatched remote calls may still finish; cancellation is attempted where available and late responses are retained without being applied.

Commands remain usable while a model call is running. They cannot share a blocking loop that waits for model completion before accepting suspension.

Artifact creation and state operations use engine-owned idempotency keys. Replaying recovery never creates a second tribute record, artifact version, or completed action for the same operation.

For a crash after dispatch but before recording completion, inspect the operation record and reconcile its state. Retry only when the faculty can establish that repeating it is safe. An uncertain provider charge remains an uncertain charge, not zero usage.

## 8. Resource and failure behavior

Require explicit local configuration for the model, maximum output size, per-episode step limit, call timeout, and standing usage allocation. Do not default to unlimited autonomous calls. Fixed development limits are engineering settings, not personality traits.

Reserve conservatively before calling. Reconcile exposed usage afterward; where exact usage is unavailable, retain the reservation or a documented bound rather than granting speculative capacity.

A malformed response gets an explicit validation result. Any repair attempt consumes the configured retry and usage allocation. Repeated invalid actions checkpoint the episode with a fault instead of creating an infinite correction loop.

A wait condition must map to a supported time or event. Unknown conditions are reported as unschedulable. Expired conditions do not produce unbounded immediate wakes.

The scheduler can continue autonomously while resources and wake conditions permit. Exhaustion pauses at a durable boundary. Resuming never erases standing commands or the failed attempt.

## 9. First demonstration

Use a deterministic substitute for model calls to verify the mechanics, then attach a real model.

The substitute follows a recorded sequence: begin a working, read a source, define and enter a frame, create an artifact, leave the frame, return an assessment, assimilate, and wait. Its output is explicitly fixture material.

The real demonstration gives The Heresiarch the selected seed and available project material without prescribing a title, ontology, doctrine, or result. It chooses its own question and artifact.

The operator reads the artifact and supplies an actual reaction through the console. Record this as operator reception. The demon can use that encounter in a further episode; no other audience or harvest is inferred.

## 10. Acceptance and next implementation

Required engineering checks:

| Scenario | Required observation |
| --- | --- |
| Restart mid-working | Same identity, working phase, artifacts, and pending pursuit resume |
| Suspend during model call | Command receipt returns promptly; the late reply cannot dispatch a new operation |
| Redirect during model call | Stale plan is retained as superseded; subsequent context includes the new instruction |
| Repeat recovered local operation | Exactly one state change or artifact version is committed |
| Leave a frame | Examiner input excludes active-frame instructions and the exploration conversation |
| Exhaust allocation or retry limit | Episode checkpoints and stops further dispatch |
| Unsupported operation or missing reference | Explicit rejection with no partial state mutation |
| Receive operator criticism | Actual feedback remains linked to the artifact; the demon's subsequent response is separately recorded |

A completed demonstration must show one full working cycle, one restart, and one interruption. Record creative quality separately from these engineering checks. Do not require a favorable creative result to pass a command-handling test.

Implementation order: durable state and dispatcher; deterministic substitute and interruption checks; context assembly and working cycle; real model adapter and operator console.

The concrete language and provider adapter are implementation choices still to be selected. This contract is sufficient to begin the deterministic core without a live API credential. The next deliverable should be executable code for that core and its meaningful recovery/interruption tests.
