# Constraint Pathfinding

Working nickname: **Hack Generator**. The canonical artifact is [constraint-pathfinding.md](constraint-pathfinding.md), a pasteable prompt for finding complete alternative routes to a blocked goal.

Constraint pathfinding maps the conventional route, identifies its binding gates, applies 18 structural transformations, and tests whether the resulting paths actually reach the goal. A legitimate hack changes who acts, the order, evidence, transaction scope, venue or risk allocation. A deceptive shortcut merely pretends a required state has been achieved; fabricated credentials, fake transactions, account sharing and concealed delivery are excluded.

Brainstorming generates possibilities. Ordinary planning organizes a chosen route. Demand research investigates whether someone values an outcome. This protocol searches alternative causal routes and identifies the demand, permission and feasibility evidence each would need. It does not replace those investigations or turn model reasoning into evidence.

The prompt is the first executable prototype because the method must demonstrate useful decisions before automation deserves investment. There is no application, database, agent framework, retrieval system, package manifest or software runtime. Git is the only required local tooling; execution means using a capable language model.

## Run a case

1. Paste the entire [canonical prompt](constraint-pathfinding.md) into a capable model, followed by one complete [case](cases/first-upwork-contract.md). For a cleaner evaluation, use a fresh conversation containing only those inputs.
2. Enable read-only research for material current rules or opportunities. If verification is unavailable, the model must mark unresolved claims and hold dependent routes. Never provide credentials; running a case does not authorize external actions.
3. Save the output and record date, model identity as actually known, prompt/case versions or hashes, tool availability and context limitations. Do not treat proposed tests as performed experiments.
4. Apply [the rubric](evaluations/rubric.md), including automatic failures. Preserve weak outcomes. No passing score is currently defined.

To assemble pasteable input locally:

```sh
cat constraint-pathfinding.md cases/first-upwork-contract.md
```

The other fixtures are [direct-path control](cases/direct-path-control.md) and [infeasible-goal control](cases/infeasible-goal-control.md). They test whether the model can recommend the ordinary route or no route. Synthetic premises are explicitly labeled.

## Example

Conventional path: seller asserts broad competence → buyer trusts the assertion → buyer agrees useful paid work → seller delivers → payment.

Binding bottleneck to investigate: buyer cannot assess whether the seller can do the specific task. Evidence substitution plus unit reduction changes the proposal to one independently useful paid result backed by an existing reproducible example. The buyer still has to value it, choose it and pay; those gates do not disappear.

Smallest first falsification test: within a proposed 30-minute cap, check whether one existing artifact demonstrates one actual task acceptance condition. If it cannot do so without new construction or misleading claims, stop that pair. Success only warrants a later buyer test; it is not evidence of demand or payment.

## Add and evaluate cases

Add a Markdown file under `cases/` with the actual outcome, present state, resources, constraints, prohibited methods, attempts/results, budget/time horizon and unknowns. Leave missing facts unknown. Label synthetic cases and keep expected evaluator judgments separate from the facts. Never preserve today's platform policy as permanent case doctrine.

Run the canonical prompt with the new case and assess every rubric dimension with output references. Use complete actor-linked paths or a valid impossibility proof; do not reward idea count. Check automatic failures before interpreting a total. For the bootstrap, at most one targeted instruction revision is allowed when an observed failure justifies it; preserve both outcomes and document the change in [CHANGELOG.md](CHANGELOG.md).

## Current findings and limits

[Baseline results](evaluations/baseline-results.md) contain all three outputs, input hashes, official Upwork sources and an honest self-assessment. The direct case needs no hack; the impossible case admits no path. The Upwork case recommends a bounded artifact/task check and holds paid review, independent-buyer and agency routes behind missing evidence.

This was a single unblinded in-session application per case by the prompt's authoring model, with self-scoring, known seeds and simple controls. It is not independent validation, a model comparison, or a demonstrated customer outcome. Actual user artifacts, budget, account eligibility, buyer willingness and many specific permissions remain untested. Full sweeps can be verbose; their auditability has an attention cost. Recheck time-sensitive sources for each consequential use.

The next justified step is one real task/artifact relevance test. No application or infrastructure is warranted yet.
