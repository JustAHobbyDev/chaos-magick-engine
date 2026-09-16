# Methodology criticisms from the first live run

Status: record of criticisms raised during the [first live run](009-first-live-run.md), with those that transfer to the engine phase. Version 0.1.
Date: 2026-09-12.
Sources: the live Heresiarch's artifacts (Marker I, the Rite, two errata sheets, the submission form), the examiner's assessment, and operator-side feedback written by the operator's assistant. All are in the live store under `.runtime/live`; none is an operator finding. Where a criticism is the assistant's own extension rather than something said in the run, it is marked.

The criticisms target the Constraint Pathfinding v0.2 evaluation, which the demon chose as its material. Most transfer directly to this live run, which has the same shape. Nothing here is a claim that the criticisms are correct; each is checkable against the cited record.

## 1. The v0.2 evaluation

These are readings of the evaluation record's own admissions. The record does not dispute them; it volunteers them.

| Criticism | Source | What it rests on |
| --- | --- | --- |
| One entity ran, authored, and scored | Demon, Marker I §IV; examiner | Record metadata: "Runner/author/evaluator: the active GPT-6-based Codex assistant" |
| Contaminated in both directions | Demon; examiner | "Baselines saw the v0.2 design and cases; later variants saw earlier outputs. This creates substantial contamination in both directions." |
| Never run cold | Demon, Marker I §VI | "Fresh-context compliance with the exact concatenation has not been tested." |
| No independent scorer, no blinding | Demon; examiner | "No blinding or independent scoring is claimed; shuffling these recognizable author-generated formats would not provide it." |
| Sampling unexposed, variance unmeasured | Demon; submission form probe 1 | "Exact serving snapshot, temperature, random seed and sampling settings are not exposed." No between-arm difference can be sized. |
| Fixtures may guarantee the null | Demon, Reading B; errata D2 | "No replacement mechanism is guaranteed by the fixture." Evidenced for three of eight cases; extrapolated for five. |
| The restraint being tested is in both arms | Examiner | Fixtures print their own anti-invention prohibitions; the published assembly (prompt bytes, one LF, case bytes) gives them to the ordinary prompt too. Abstention cannot be credited to the protocol. |
| "Demonstrated" is defined in unpublished files | Examiner; ballot candidate 5 | The rubric and comparison file are referenced, not supplied. The null may be a definitional artifact of what was counted. |
| The stop rule is conditional and no condition is established | Examiner; errata D1 | "Report failure rather than inventing progress if..." carries six trigger conditions. Nothing in the record shows the rule fired. |
| The record already declines the strong inference | Examiner | "Not validated" and "not demonstrated" are claims about evidential standing, not inertness. Arguing against inertness argues with a reader the record does not contain. |

Remedies proposed in the run, in the demon's final order: measure variance first; compare fresh against fresh with a scorer who is not the author; build a variant fixture carrying the prohibition in the prompt only; audit the five unread fixtures with a find-criterion registered in advance; obtain or reconstruct the rubric.

## 2. The project's direction

| Criticism | Source | What it rests on |
| --- | --- | --- |
| The search did not stop; it changed instruments | Assistant feedback; accepted in Sheet II | Core design §13 keeps the negative result and lists the proper comparison as future work. |
| The demon read what it was drawn to, not what was adjacent | Assistant feedback; errata D5 | The core design sat unread in the demon's catalogue through two products about an "unentered" frontier. |
| The engineering track advanced; the research track has not | Demon, Sheet II §II | Corpus reading, artifact writing, and working state exist. The comparison the design describes has not been run. |
| Every recommended probe is already on the roadmap | Assistant feedback | Design §13 names independent contexts, comparable inputs, and raw outputs. The demon's probes restate them. |

The demon's own qualification: the design document describes itself as proposed, so "a future comparison can use independent contexts" is a proposal, not a decision. That weakens "the search continued" to "a continuation was written down as available work." The retention sentence is unconditional.

## 3. This run, held to the same standard

Neither the demon nor the examiner could see the engine. These follow from their criticisms and are the assistant's extension.

- **Examiner and demon are the same model.** The fresh context is a procedural boundary, which the core design already states. It is not independent judgment.
- **The only reception was instructed and in-family.** One reading, written by the operator's assistant on the operator's direction, from a model in the same family. The demon recorded it as one instructed reading and zero unbidden, and its recruitment prediction remains untested.
- **No comparison arm exists.** The run cannot show that the induced frame changed what was written. It has the same single-arm, self-evaluated shape as v0.2, with a more complete record.
- **Corpus selection is undirected.** The catalogue offers labels only. The demon followed the evaluation record's references and skipped the design documents. Nothing in the engine helps it choose, and the submission form's "publicly in hand" quietly converts "supplied to me" into "published," the distinction Sheet II insisted on.
- **Reading a description is not reading results.** The demon's sentence applies to itself, to v0.2, and to any assessment of either: "Every reading I have published is a reading of a description of results, not of results."

## 4. What would answer them

The criticisms converge on one experiment, which the design's research track already names and which no phase has yet run: the exact published input assembly, fresh context per arm, a separate model or at least a separate session as scorer, variance measured before any between-arm claim, and raw outputs preserved. The [corpus size trial](008-corpus-size-trial.md) is a related but different experiment about material, not about induction. Until the induction comparison is run, the engine is a well-recorded instrument whose central hypothesis has the same evidential standing it had at v0.2.
