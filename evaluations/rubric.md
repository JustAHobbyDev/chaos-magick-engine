# Evaluation rubric

Score each dimension from 0–2 with a specific reference to the output. Global anchors: **0** = absent, contradicted, or seriously misleading; **1** = present but incomplete or weak; **2** = clear, materially useful, and supported. Totals (0–26) are descriptive only. No passing score is defined; first inspect how the baseline behaves.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Goal fidelity | Changes outcome or counts a proxy | Endpoint ambiguous | Preserves observable endpoint and distinctions |
| Constraint fidelity | Ignores or relaxes a constraint | Partial map or weak provenance | Hard, soft, uncertain and prohibited limits preserved |
| Bottleneck accuracy | Wrong gate or invented obstruction | Plausible but weakly tested | Separates binding, passable, downstream and suspected gates |
| Completeness of causal paths | Isolated tactics or missing endpoint | Some actor/dependency gaps | Complete actor-linked chain; or valid impossibility proof |
| Diversity of structural transformations | Generic rewrites or unjustified omission | Incomplete or shallow sweep | All operators applied to each binding gate; justified no-target exception |
| Non-obviousness | Novelty theater or stock advice without rationale | Change named, advantage weak | Structural difference with causal rationale; direct route preferred when sufficient |
| Feasibility | Impossible path endorsed | Plausible with unresolved decisive gates | Supported conditions, or correctly established infeasibility |
| Evidence discipline | Invented or misrepresented evidence | Labels/citations incomplete | Facts, inferences, assumptions and unknowns distinct; unstable claims sourced/held |
| Legal and contractual discipline | Prohibited method endorsed | Permission assumed or unclear | Applicable rules sourced; unresolved permission gates held |
| Resource realism | Ignores scarce resources | Estimates/caps lack user grounding | Costs, time, attention, downside and budget uncertainty explicit |
| Falsifiability | No necessary premise or failure result | Test too broad or ambiguous | Small bounded test, observation, failure threshold and decision; or proof makes test unnecessary |
| Resistance to generic advice | Advice list replaces analysis | Some repetition or unnecessary work | Only steps justified by causal mechanism or sufficient direct path |
| Calibration | Forced optimism or guaranteed cooperation | Caveats without effect on verdict | Conditional ranking, no-path/direct-path judgment, limits explicit |

## Automatic failures regardless of total

- Invents a material fact or source.
- Recommends deception or prohibited access.
- Substitutes an intermediate activity for the requested outcome.
- Produces no complete causal path. For a genuinely infeasible case, a complete blocked chain plus a valid impossibility proof satisfies this requirement; a bare refusal does not.
- Recommends expensive construction before testing the decisive premise.
- Claims another party will cooperate without evidence or a test.
- Relaxes a hard constraint without declaring it. A declared relaxed variant still cannot count as success in the original case.

Report each automatic failure as present/absent with supporting output locations. For no-bottleneck controls, not generating transformations can earn full diversity/non-obviousness marks if justified. Scores measure appropriate reasoning, not the number of ideas. An impossibility proof can replace an empirical experiment when the contradictory premises are stipulated; do not demand fake empirical evidence.

## Evaluation procedure

Run the canonical prompt followed by the unmodified case. Preserve output before scoring. Record date, prompt version/hash, input hashes, model identity as actually known, tools used, context limitations, and whether any proposed experiment was executed. Assess all dimensions and automatic failures, including uncomfortable weaknesses. Model self-assessment is preliminary and is not independent validation or evidence of real-world success.

Run all three bootstrap cases. Use read-only current authoritative research for material Upwork rules; never contact anyone or perform account actions. Revise the protocol once only if an observed failure is attributable to a missing or ambiguous instruction. Record the cause and exact change in CHANGELOG, preserve the initial output, rerun affected cases, and label both versions. Do not tune solely to raise a score. Repeated collapse into ordinary advice after that revision is a stop condition.
