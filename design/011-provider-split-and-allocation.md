# Provider split and allocation

Status: implemented engine change; the live configuration it enables has not been run. Version 0.1.
Date: 2026-09-12.
Dependencies: [methodology criticisms](010-methodology-criticisms.md), [first live run](009-first-live-run.md), [live adapters](../chaos_magick_engine/live.py).
Scope: which criticisms in design 010 this change answers, which it leaves standing, and whether the standing allocation must rise before the next run.

## What changed

The operator directed that the demon run on OpenAI's GPT-5.6 Sol under flex processing and that the examiner run on Claude Opus. "Sol Flex" is not a model: it is `gpt-5.6-sol` with `service_tier` set to `flex`, which OpenAI prices at batch rates in exchange for slower replies and occasional capacity refusals.

- **OpenAI adapter.** One Responses API call per invocation with the same fixed system line as the Claude adapter, the compiled JSON as input, reasoning effort, a 32000-token output ceiling that covers reasoning, and no provider-side storage. A capacity refusal on the flex tier, after the SDK's own retries, is re-issued once on the standard tier and recorded as a fallback, the way the Claude adapter records a server-side model fallback; `--no-fallbacks` makes it an explicit error instead. A refusal item becomes an empty reply the engine rejects. Serving model, response id, request id, requested and served tier, completion status, incomplete reason, and cached and reasoning token counts are metadata. Usage stays in characters.
- **Role routing.** Requests now carry the engine-assigned role, and a router adapter sends demon and examiner requests to different providers. The router adds nothing to the record; each invocation already names the provider and model that served it, so provenance per role is in the store.
- **Console.** `run` and `live-check` take `--adapter openai`, `--service-tier`, and `--examiner-adapter`, `--examiner-model`, `--examiner-effort`, `--examiner-key-file`. `live-check --role examiner` exercises the examiner's adapter. A new offline `configure` command changes any engine limit of an existing identity, including the standing allocation, and records the change and its reason as an operator event. The ledger is never reset; a larger standing figure is the only replenishment. The first run raised bounds by direct database edit; this makes the same act a command.
- **Live configuration.** Call timeout raised from ten to fifteen minutes, OpenAI's documented recommendation for flex. Standing characters raised from 3.6 million to 8 million; the reasoning is below.

## Criticisms of the live run, held to the same standard

Design 010 §3 lists five criticisms of the run itself. This change answers one of them in part and none of the others.

| Criticism | Status after this change | What rests on it |
| --- | --- | --- |
| Examiner and demon are the same model | Answered in part | The scorer is now a different model from a different organization. That removes shared training and shared style from the examination. It does not make the examiner's judgment correct, blind, or a reading of results rather than of a description. |
| The only reception was instructed and in-family | Not answered | An examiner is not reception. The recruitment prediction remains untested. |
| No comparison arm exists | Not answered; an engine gap is now explicit | A working reaches examination only through `leave_frame`. An ordinary-exploration arm without induction has no path from orientation to examination. Whether the arm is a frame-free segment or a separate working mode is an operator decision; nothing here decides it. |
| Corpus selection is undirected | Not answered | The catalogue still offers labels only. |
| Reading a description is not reading results | Not answered | The new examiner reads the same declared sources the old one did. |

The §1 criticisms of the v0.2 evaluation are not addressable by any engine change; only the experiment in §4 can answer them. Of that experiment's five requirements, this change supplies one, a separate model as scorer. Fresh context per arm, a comparison arm, variance measured before any between-arm claim, and preserved raw outputs are respectively available, missing, unattempted, and already present.

## Allocation

The question was whether the standing allocation must rise further. The first run's store answers for a continuing identity; its per-call sizes answer for fresh stores.

| Measure | Value |
| --- | --- |
| Standing allocation, first run | 60 calls, 3,600,000 characters |
| Used by the end of the run | 42 calls, 3,513,535 characters (3,154,732 spent, 358,803 held for cancelled calls) |
| Remaining | 18 calls, 86,465 characters |
| Reserve required for the next call at the last input size | 157,388 + 24,000 = 181,388 characters |
| First working, orientation through assimilation, 22 invocations | 1,099,537 characters |
| Later 20 invocations, mean input | 114,265 characters |
| Later 20 invocations, characters spent | 2,413,998 |
| Characters per Claude input token, whole run | 2.81 |

Three conclusions follow.

1. **The existing identity cannot dispatch another call.** Its remaining characters are less than half of one reservation, so the character cap, not the call cap, ended the run. To continue that identity the operator must raise it: `configure --set standing_usage_chars=8000000 --reason "..."` against `.runtime/live`. This record does not do that; it is the operator's ledger.
2. **For a fresh store, the old figure was enough for one working and not for two.** One complete working cost 1.1 million characters while the store was small, and every later call costs more as history and read material accumulate toward the 200,000-character input bound. Sixty calls at the late-run mean of about 120,000 characters spent per call is 7.2 million characters. The new default of 8 million makes the two caps bind at about the same point, so the call count is the figure the operator reasons about, as the design intended. The worst case, sixty calls at the full input bound plus the output reserve, is 13.4 million; the default does not cover it, and the checkpoint will say so if it is reached.
3. **The comparison experiment needs arms, not a larger single allocation.** Each arm is a fresh store with one working, about 1.1 million characters at the first run's sizes. Two arms with three repetitions each is roughly 7 million characters across six stores, within the per-store default many times over. If an arm is run as a continuing identity across repetitions instead, the per-store default binds after about five workings of the first run's size.

The character ledger is provider-neutral, so these figures hold for the new demon. Cost projections do not: the ratio of characters to tokens for Sol is unmeasured, flex pricing is batch-rate pricing subject to a promotional period, and the examiner's tokens now come from a different price list. At the first run's ratios and list prices, a run of the first run's size would cost on the order of a few dollars for the demon at flex rates and under one dollar for three examiner calls on Opus. Those are estimates from another provider's tokenizer, not measurements.

## What this does not establish

No request has been sent to OpenAI. The adapter is verified against a fake client for request shape, usage unit, metadata, refusal handling, capacity fallback, provider error, and incomplete replies, and the console wiring is verified to build the split router with each role's key. Flex latency, actual capacity refusals, Sol's compliance with the operation contract, and its tokenizer ratio are unobserved until `live-check --adapter openai` and a bounded episode are run with a key at `.runtime/credentials/openai.key`. A different provider is procedural separation of the scorer, not independent judgment, and this record does not claim otherwise.

## Next

Run `live-check` for both roles, then one bounded episode of a fresh identity with the split configuration and record its per-call sizes beside the table above. Decide how an ordinary-exploration arm reaches examination, since that decision gates the §4 experiment and nothing else in the criticisms does. Enable structured output enforcement on both adapters; the Responses API has a schema format available and the first run's rejections were mostly format.
