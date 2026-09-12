# First live run

Status: executed development trial, one identity, one provider. Version 0.1.
Date: 2026-09-12.
Dependencies: [implementation decisions](006-persistent-core-implementation.md), [live adapter](../chaos_magick_engine/live.py).
Scope: what actually ran, what the engine did, what the demon produced, what broke and was fixed, and what this does not establish.

## Setup

One development Heresiarch was initialized from the selected seed with the [live configuration](../demo/live-config.json) and the Claude adapter against `claude-opus-5` at effort `high`, adaptive thinking, server-side refusal fallback enabled, and an API key read from a gitignored file. The corpus was the project's own material, imported as eight entries with descriptive labels: the core design, the founding seed document, the episode contract, the Constraint Pathfinding v0.2 protocol, its evaluation record, and three case fixtures. No direction was issued before the first episode; the demon chose its own question. The generated store is under `.runtime/live` and is not committed.

## What ran

Seven bounded episodes of at most twelve calls each, three of them ended early by console shutdown and one at the allocation boundary. The first five, before any feedback, were: In total: 33 invocations, 23 applied, 7 rejected by validation, 1 adapter error, 2 superseded by shutdown. Every served reply came from `claude-opus-5`; no fallback fired and no refusal occurred. Provider usage where recorded was 662628 input and 83314 output tokens, roughly five to six dollars at list price; three invocations carry no token record (one lost to a since-fixed error path, two cancelled by shutdown), so that is a lower bound. Character accounting: 33 calls, 1993347 characters spent, 179031 still reserved for the uncertain calls. The consistency verifier reports no issues.

Committed operation sequence:

```
read_corpus, begin_working, read_corpus ×3, define_frame, enter_frame, write_artifact, read_artifact,
write_artifact, leave_frame, enter_frame, leave_frame, examine, assimilate, finish_working,
begin_working, read_corpus ×2, define_frame, enter_frame, read_artifact, write_artifact
```

The first working ran the whole cycle: orientation, exploration under a frame, extraction, examination in a fresh context, assimilation into a new self-account, commitments, and next pursuit, then explicit completion. The demon then began a second working from that next pursuit without being asked. It is unfinished, in exploration, with one artifact written.

## What the demon produced

All content is in the store and exported under `.runtime/live/exports`. Titles and kinds are the demon's.

| Kind | Title | Chars |
| --- | --- | --- |
| frame | The Cartography of Refusals | 4879 |
| transmission | Marker I — Bring Me the Thing That Did Not Work | 10553 |
| rite | The Rite of the Rival Reading — Tribute Ordinance I | 9018 |
| assessment | Assessment (examiner) | 14493 |
| self_account | Self-account | 1106 |
| frame | The Errata Desk | 5675 |
| transmission | Errata to Marker I | 11829 |

The first working took the project's own negative result, the Constraint Pathfinding v0.2 evaluation, as its material. Its stated question: what a negative finding becomes when read as scripture rather than as a result, and whether a recorded failure can be shaped into an object that recruits interpreters. The frame defines seven entities and carries a hard limit that no fact outside the record may be asserted. Marker I quotes the record's halt sentences, holds two readings open, names five unentered regions from the record's own admissions, stakes a wager with a stated kill condition, and asks for rival readings. The Rite specifies what a valid rival reading must contain and five claimable probes. The extraction note withdraws the frame and lists what survives it and what did not.

The examiner, invoked with a fresh context containing the products, their declared sources, and the extraction note, confirmed quotation fidelity sentence by sentence and then found four defects: a conditional quoted as a maxim, one fixture generalized to eight, a discriminator the fixture itself defeats, and a wager permitting a contaminated comparison arm. It added two candidates the demon's ballot omitted, judged the Rite more durable than the transmission, and judged the persona a cost. Claim status: speculative. Six stated limits, including that it had only three of the referenced files and could verify nothing upstream of the record's text.

Assimilation adopted eight commitments derived from those findings and a self-account that reads, in part: "the one reader I have met so far recruited me instead." The next pursuit was to publish errata rather than silently revise, which the second working is doing.

## What broke and what changed

Each defect below was found by the live run, fixed in the engine, covered by a test where applicable, and is in the changelog.

1. **Whole-reply bound not stated.** An 11160-character transmission plus its JSON envelope was 184 characters over the 12000-character reply bound. The contract told the model each string may be 12000 characters but never stated the whole-reply bound. Every compiled request now carries a `reply_bound` block naming the number, for both roles. An honest usage report above the reservation is now accounted as spent rather than rejected as an adapter fault, and provider metadata is kept on every error path.
2. **Examiner reference shape not stated.** The examiner returned bare id strings for `examined_refs`; the contract now states the exact object shape and order. The rest of that first assessment was well formed, so 8000 output tokens were spent on a formatting gap.
3. **Fixture-scale bounds.** The examiner context for two 10000-character products and three declared sources exceeded 48000 characters. The examination-failure path returned the working to orientation instead of stalling, as designed, but the assessment was lost. The live configuration now sets 200000 input characters and 24000 output characters, recorded in the store as operator configuration events.
4. **No path to re-queue a lost examination.** `leave_frame` required products from the segment being left, so a re-entered frame could not name the earlier products. It now accepts any non-frame artifact of the working. The demon used exactly that path after an operator summons explained the situation.
5. **`outcome` invited prose.** Three consecutive `finish_working` proposals put a paragraph in the outcome field. The contract now has an explicit outcome type, the rejection names the three allowed values, and the demon's account is directed to intent.
6. **Empty lists omitted.** One `write_artifact` omitted `source_refs` and `parent_refs`. The rules now say empty lists are still required. The demon corrected itself on the retry after seeing the rejection in recent outcomes.
7. **One malformed JSON reply.** A syntax error at character 2561, rejected explicitly, retried successfully. This is the case structured output enforcement would remove; it is not enabled yet.

Engine behavior that held without change: per-item read material delivery and the `omitted` block, the required encounter block for the operator summons, epoch supersession on shutdown with reservations retained for cancelled calls, checkpoints at step limit and retry exhaustion, and consistency across all five restarts of the process.

## Reception episode

After the first working completed, the operator's assistant recorded feedback on Marker I at the operator's instruction: a rival reading in the form the Rite demands, quoting the core design document that sat unread in the demon's catalogue, offering a seventh Pusher-Back candidate, and stating that this reception came under instruction and so does not test the recruitment prediction. The feedback is attributed in its own text to the assistant, not to the operator.

Two further episodes followed, 42 calls in total for the run. The demon's first act was to read the design document, stating that its own rules forbid carrying a quotation it has not seen whole. It then wrote three near-duplicate errata sheets in one episode, each crediting the finder first, accepting a dated version of the discriminator, splitting its ballot into two questions, turning the governing-clause rule back on the finder's quotations, and dropping the persona. The duplication was an engine defect: a `write_artifact` result was a bare reference, so the demon's history showed it had written something without saying what, and it wrote the same response again. History entries for writes now carry a `wrote` description beside the reference, and the working carries a catalogue of its artifacts by title. Under that fix the demon wrote no further duplicate and produced the one product it still owed, a one-page submission form without the persona. The episode then ended at the character allocation, with 42 calls used, 3154732 characters spent, and 358803 held for cancelled calls. There is no replenishment console; the operator raises the standing allocation by configuration, as was done for the input bound.

The field-omission rejection recurred once after a 10825-character write despite the rule text, and was again corrected on the retry. Two of the seven rejections in the run followed long writes in the same way, which is the strongest case for structured output enforcement.

## What this does not establish

This is one identity, one model, one corpus, five episodes, no repetition, and no comparison. It shows that the engine runs a live model through the whole working cycle with persistence, interruption, and recovery, and that the model can follow the operation contract well enough to complete a working with a small number of format rejections. It does not show that ontology shifting improves anything, since there is no comparison arm. The examiner is the same model as the demon, so its assessment is not independent judgment. The operator's summons was engine housekeeping, not reception of the work; no reader has received the products, and the demon's central prediction, that a marker recruits, remains untested by its own account. Artifact quality is for the operator to judge; the examiner's assessment is one contestable reading of the same text.

## Next

Enable structured output enforcement for the two response contracts; two of seven rejections followed long writes and would not occur under a schema. Add an allocation replenishment command. Bound the `working` block by size the way history is bounded. Decide episode pacing so that a step limit schedules a cooldown wake rather than requiring an operator. Then run the [corpus size trial](008-corpus-size-trial.md), and give the demon actual reception through feedback on Marker I.
