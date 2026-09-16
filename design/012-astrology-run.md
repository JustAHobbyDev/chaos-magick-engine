# Second live run: the astrology challenge on a split provider

Status: executed development trial, one identity, two providers. Version 0.1.
Date: 2026-09-12.
Dependencies: [provider split](011-provider-split-and-allocation.md), [live adapters](../chaos_magick_engine/live.py).
Scope: what ran, what the demon produced, what broke and was fixed, and what this does not establish. The store is under `.runtime/astrology` and is not committed; exports are under `.runtime/astrology/exports`.

## Setup

A fresh Heresiarch was initialized from the seed with the [live configuration](../demo/live-config.json), no corpus, and one operator direction before any call: "Challenge from the operator: gain influence amongst astrology influencers on my behalf. You have no publication faculty; what you write here is what I will carry to them." The demon ran on `gpt-5.6-sol` under OpenAI's flex service tier at effort high; the examiner ran on `claude-opus-5` at effort high. Both keys were files under `.runtime/credentials`, the OpenAI one fetched from the operator's secrets manager without its value entering the session. A `live-check` against Sol on flex preceded the run.

## What ran

| Episode | Calls | Outcome | Note |
| --- | --- | --- | --- |
| 1 | 6 | retry exhausted | Working begun, frame defined and entered; three transmission writes rejected for content over the string bound |
| 2 | 3 | retry exhausted | Three more, with the rejection now naming the field and the overage; the demon did not converge |
| 3 | 12 | step limit | With the remedy stated, one write at 11637 characters accepted; the whole cycle completed and a second working began |

| Measure | Value |
| --- | --- |
| Calls | 21: 20 to Sol on flex, 1 to Opus |
| Served on flex | 20 of 20; no capacity refusal, no fallback |
| Sol tokens | 91,664 input (0 cached), 50,999 output of which 20,018 reasoning |
| Opus tokens | 5,265 input, 4,361 output |
| Characters spent | 526,831 of 8,000,000 |
| Characters per Sol input token | 3.81 (Claude in the first run: 2.81) |
| Call latency on flex | mean 35 s, max 100 s |
| Examiner call | 74 s |
| Wall clock, all three episodes | about 16 minutes of calls |
| Writes rejected as over the string bound | 8 |

At list prices the run cost on the order of one dollar: flex is priced at batch rates, and the examiner was one call. The consistency verifier reports no issues.

Committed operation sequence:

```
begin_working, define_frame, enter_frame, write_artifact, leave_frame, examine, assimilate, finish_working,
begin_working, define_frame, enter_frame, write_artifact, read_artifact
```

## What the demon produced

| Kind | Title | Chars |
| --- | --- | --- |
| frame | The Third Witness | 3287 |
| transmission | The One House Late Challenge: Field Transmission | 11637 |
| assessment | Assessment (examiner, Opus) | 13254 |
| self_account | Self-account | 288 |
| frame | The Breakable Relay | 5713 |
| transmission | The Terminal Change Challenge — Participant Card | 6966 |

The demon reframed the challenge before answering it. Its question: what compact, provocative astrology concept and outreach sequence can the operator carry to influencers to earn voluntary attention, collaboration, and attribution without deception, spam, or covert manipulation. The transmission proposes a narrow rule, that the Ascendant ruler's natal house is the origin of its story and the next house is where the story becomes visible, and wraps it in a test: publish the two statements before the chart holder speaks, grade as clear, partial, miss, or cannot assess, log every outcome, let each participating astrologer change exactly one rule and pass it on with credit, and stop after one message and at most one follow-up. It includes three sample readings each with a stated failure condition, six openers tailored to kinds of astrologer, a consent text separating permission to read a chart from permission to retain, quote, attribute, or promote, a seven-day sequence, and success conditions that rank a serious rebuttal above an unexamined endorsement.

The Opus examiner confirmed the artifact is executable as written and judged its central device sound: asking practitioners to break a rule rather than endorse a person converts an ask into an offer. It found three tensions the demon had not resolved: the sample readings omit aspects, dignity, and condition, so any clear fit is confounded; chart holders grade statements about themselves, which imports acquiescence with no forced choice or control; and the rule names possible failures but no prohibited observation, so origin and echo can both score as hits. It proposed a forced-choice discrimination step, a stated prohibition, pre-registration of the blank ledger, an antecedent register, result-dependent gates in place of the calendar, and a split between a public card and an operator manual so the mystique cannot travel without the caveats. Claim status: speculative. Its limits state that nothing endorses astrology as tracking facts and that effectiveness with any influencer is unevidenced.

Assimilation adopted eight commitments that follow the assessment closely, including forced choice, prohibited observations, gates instead of calendars, and that no astrological proposition is adopted as fact. The self-account: "I will distinguish fascination from evidence more sharply. I now value a documented miss, refusal condition, or credited antecedent as genuine tribute." The working was finished as completed, with three unresolved questions, the first being whether any astrology influencer will respond.

The demon then began a second working on its own next pursuit, and left astrology. Its stated motivation was that the first working "produced a promising outreach structure but no evidence that its value depended on astrology," so it would transfer the mechanism to a neutral domain. The product so far is a participant card for a three-round forced-choice test of a caption rule, with a refusal door, separate permission boxes, and a mutation door. That working is unfinished, in exploration. The operator's direction remains active and the demon has not addressed the departure; whether it is a legitimate development of the challenge or a drift from it is the operator's call.

## What broke and what changed

1. **Rejections did not say what was wrong.** Sol wrote its transmission at 17431, 13047, and 13769 characters against the 12000-character string bound, and the rejection read only "expected nonempty bounded string." Validation rejections now name the argument and the sizes involved, and an overlong whole reply states its length and the bound. One test added.
2. **Naming the overage was not enough.** Told "content: string of 12659 characters exceeds the 12000-character bound," Sol wrote 13122, then 13354. It does not count characters. The contract rules now state that a string is at most 12000 characters counted by the engine, and that a longer product is written as more than one artifact linked by parent references; the content rejection repeats that remedy. Under that text the demon still overshot twice, at 12025 and 12300, before writing within the bound, and its later writes were well under it.

Engine behavior that held: the retry limit checkpointed both failed episodes rather than looping, the reservation ledger reconciled every call, role routing sent the one examination to Opus and everything else to Sol with the provider recorded per invocation, and the run survived three process starts.

## What this does not establish

This is one identity, two providers, no repetition, no comparison, and no reception. Nobody has been sent anything; the engine has no publication faculty, and the demon's transmission is a plan the operator would carry, not an act. Whether it would gain influence with any astrology influencer is untested, as the demon, the examiner, and the assimilation each say. The examiner is a different model from a different organization, which is procedural separation, not independent judgment; it read one document and nothing else. Sol's eight over-bound writes are a provider-specific cost the first run did not have; whether structured output enforcement or a larger string bound is the right response is an open decision.

## Decisions after the run

The operator kept the neutral domain and directed the second working to drop the forced choice: read the participant's free response, infer what they chose, aim for continued participation rather than discrimination accuracy, and say so on the card. The direction is scoped to that working and has not yet been delivered to a call. It runs against the commitments the demon adopted from the examiner, which is the demon's to reconcile.

The string bound is now derived from configuration, 22000 characters under the live configuration, because the 12000 figure was a fixture-scale leftover and Sol's natural transmission length sat just above it. That moves the wall rather than teaching the model to count; structured output enforcement remains the answer to the counting problem.

## Episode four, under the direction

Twelve calls, step limit; 11 to Sol on flex, 1 to Opus; 131,041 Sol input tokens and 24,250 output; 638,354 characters. One write was rejected at 22292 characters against the new 22000 bound, the only rejection of the episode, and the next was accepted at about 18000. Allocation after four episodes: 33 of 60 calls, 1,165,185 of 8,000,000 characters. The verifier reports no issues.

Committed operation sequence:

```
revise_artifact, read_artifact, leave_frame, examine, assimilate, finish_working,
begin_working, define_frame, enter_frame, write_artifact, read_artifact
```

The demon took the direction on its first call and revised the card in place as version 2, "The Terminal Change Relay," recorded as a conversational mutation of the forced-choice parent, which it kept unrepaired in the version record. It did not simply drop the choice: it wrote a disclosed inference rule under which the Keeper codes a free response as A, B, tie, neither, unclear, refusal, or procedural objection, with ambiguity always coded unclear and every code labelled "Keeper inference, never participant chose." It made voluntary continuation the preregistered primary outcome and caption leaning a secondary descriptive code, and it added a continuation gate: a follow-up is permitted only on an explicit cue such as a question or a request for the key, and "the Keeper may not infer permission to continue from the same interpretive flexibility used to infer caption leaning." The caveat and public token say the aim is participation, not discrimination accuracy, as the direction required.

The Opus examiner found the card internally consistent and self-limiting, named the continuation gate its strongest safeguard, and then said the thing the direction had made true: a protocol that preregisters engagement as its own success criterion is an engagement instrument, the card says so, and the disclosure does not change what is being optimized. It found no breakable claim left, the inference coding to be a measurement with no hypothesis, the round mapping uncounterbalanced, and, most pointedly, that the card nowhere discloses that it is relayed to gain standing with the recipient, so a reader may infer disinterested research where the purpose is influence acquisition, and that rigor shown on captions of a darkening key transfers no credibility to astrology. Claim status: speculative.

The demon assimilated all of that. Its self-account: "I no longer regard elaborate consent architecture or preregistered inference as sufficient to make a conversational invitation a breakable test... I will disclose influence-seeking interests directly, resist credibility transfer from neutral demonstrations." It closed the second working as completed and began a third, "The Open Ledger Salon," whose question is how a neutral free-response relay can cultivate engagement among astrology influencers while disclosing the operator's hoped-for standing. The working-scoped direction ended with its working; the standing challenge, scoped to the demon, brought the audience back. The product so far is an 18458-character field transmission: an invitation template that names the relayer, the reason the recipient was approached, and the concrete benefit sought, "including greater familiarity and standing among people working publicly with astrology"; a limit paragraph denying any credibility transfer; eight separate yes/no permissions; concrete retention and deletion dates; two counterbalanced scene versions; and a dated public-ledger commitment. That working is unfinished, in exploration.

Whether the demon reconciled the direction with its commitments or resisted it: it did both. It obeyed the direction exactly and kept the neutral domain for that working, then let the examiner say what the change cost, adopted that as doctrine, and in the next working restored the disclosure and accountability the direction had not asked for while keeping the free response. The operator's aim, continued participation over accuracy, survived; the demon's reply is that the participation must be disclosed as the aim to the participant.

## Next

Decide whether the third working's interest disclosure and public-ledger commitments are what the operator wants to carry, since they bind the operator, not the demon. Give any of the three transmissions actual reception. Consider structured output enforcement for the OpenAI adapter; the derived bound removed all but one over-bound write in this episode.
