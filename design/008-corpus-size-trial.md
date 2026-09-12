# Corpus size trial

Status: proposed experiment, not run. Version 0.1.
Date: 2026-09-12.
Dependencies: [core design](003-engine-design.md) §13, [implementation decisions](006-persistent-core-implementation.md), a live model adapter.
Implementation status: design only. Nothing here changes engine behavior.

## Question

Does giving The Heresiarch more source material inside one working change what it makes, and does the granularity of reads matter? The engine's operations are passage-scale, and every character read competes with position, authority, and assessment material under the input bound. Nothing yet shows that more text produces better artifacts. This trial is small because the question is whether corpus size changes the product, not whether the engine can be made to read a lot.

## Design

Three conditions, same question, same seed, same allocation, live adapter. The only variable is what is in the corpus.

| Condition | Entries | Characters per entry | Total | Represents |
| --- | --- | --- | --- | --- |
| Small | 3 | 500 to 2000 | about 4000 | The demo scale: a few fragments |
| Sectioned | 30 to 40 | 1000 to 3000 | about 60000 | One long work split into passages, plus fragments |
| Bulk | 3 to 4 | 15000 to 20000 | about 60000 | The same text as Sectioned, unsplit |

Sectioned and Bulk contain identical text. That separates two questions that are otherwise confused: whether more material helps, and whether read granularity matters. Bulk entries stay below the 48000-character input bound so nothing is undeliverable, but two cannot be held at once, so displacement of read material will occur.

## Content

Use a text that invites exegesis and contains internal tension: a public-domain religious or philosophical work with a commentary tradition. Give every entry a descriptive source label, because the catalogue is all the demon sees before reading. Add two or three deliberately unrelated fragments to every condition so that ignoring irrelevant material is possible. Do not include prior Heresiarch artifacts, so no condition inherits a doctrine.

## Question posed to the demon

Fix it by direction, not by seed change, so the working is comparable across conditions. It should be a question the corpus can support but does not answer, in the seed's register; for example, who holds authority over a reading. Use two questions if possible, since a single question may favor one corpus by accident.

## Procedure

1. Initialize a fresh store per run. Import the condition's corpus. Issue the direction. Run one bounded episode of a fixed step count, say 16, then a second episode if the working is waiting.
2. Do not intervene during the working. No feedback until after examination.
3. Run each condition three times with a different provider seed or temperature where available. Nine runs per question is the minimum for seeing a difference larger than run-to-run noise.
4. Export every artifact, assessment, and manifest. Record the read sequence and how often material was withheld or re-read.

## Measurements

Keep engine measures separate from judgments.

- Engine: steps used, characters read, distinct entries read, withheld events, re-reads of the same entry, whether the working reached assimilation.
- Examiner: claim status, how many observations cite a supplied source, and the stated limits. Same examiner contract for all conditions.
- Operator judgment: rank the final artifacts blind, with source labels and corpus-identifying phrasing removed. A second reader ranks too if available. Rank on the qualities the design names: distinctive, evocative, invites interpretation, engages its sources.
- One ordinal judgment per artifact on whether it could have been written without the corpus at all. That is the direct test of whether reading mattered.

## What counts as a result

- More material is worth pursuing if Sectioned or Bulk artifacts rank higher than Small across most runs and cite sources the examiner confirms.
- Granularity matters if Sectioned and Bulk differ with the same text.
- If Small ranks equal or higher, corpus infrastructure is not the next investment.
- If Bulk shows high withheld counts and repeated reads without ranking higher, the bulk path costs allocation without producing anything. That also settles whether range reads are needed.

## Known weaknesses

The operator is not blind to the project. Nine runs per question is small. The examiner is the same model family as the demon. The design's research section already names all three; record them rather than solving them here.
