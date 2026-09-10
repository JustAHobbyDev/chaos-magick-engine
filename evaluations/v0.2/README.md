# v0.2 development comparison

Result: **no incremental mechanism or material partial bridge demonstrated over both baselines**. The protocol and raw evidence are inspectable; the creative engine is not validated. See the [comparison](comparison.md), [rubric](../rubric-v0.2.md) and [design decision](../../design/002-representation-and-verification.md).

## Run metadata

Date: 2026-09-10. Runner/author/evaluator: the active GPT-6-based Codex assistant, as identified by session instructions. Exact serving snapshot, temperature, random seed and sampling settings are not exposed. No separate model API, CLI model process or subagent was invoked. The files are actual single-pass in-session model applications written directly into Markdown, not captured responses from an isolated execution harness.

All three full prompt variants and complete cases were present in the authoring context before generating the outputs. Each application selected the corresponding frozen variant and unmodified case as its task instructions. The [input manifest](input-manifest.json) records the exact prompt/case bytes and reconstructible concatenation hashes: full prompt bytes, one LF byte, full case bytes. These hashes identify selected inputs, **not a complete provider request payload**: system/developer instructions, handoff, authored fixtures, previous outputs, tool results and this shared context also influenced generation. Fresh-context compliance with the exact concatenation has not been tested. Do not treat these files as controlled A/B evidence.

Order: all ordinary applications, then all v0.1 applications, then all v0.2 applications. Within each group: representation-ambiguity, partial-bridge, open-world, blocked-strategic, mechanism-salvage, first-upwork-contract, direct-path-control, infeasible-goal-control. No output regenerated or revised after assessment. Baselines saw the v0.2 design and cases; later variants saw earlier outputs. This creates substantial contamination in both directions. No blinding or independent scoring is claimed; shuffling these recognizable author-generated formats would not provide it. No counterbalanced or separate-model trial occurred.

Tools available: filesystem/shell and public read-only web research. Tools used for case evidence: shared official NLM search/open before the output batches, documented in the [research record](research.md). It informed every open-world variant. Other cases use supplied premises and explicitly held unknowns; no new Upwork platform claims are asserted as verified. Local arithmetic was generated in each partial-bridge response and independently checked during repository verification. No contact, proposal, purchase, account access, SSH command or field experiment occurred. Writing evaluation artifacts and committing the repository are implementation actions, not simulated case outcomes.

The [output manifest](output-manifest.json) was frozen after all 24 responses and before scoring. Source fixtures remain attached by path and protected by their manifest hashes; v0.2 responses reference those verbatim inputs instead of duplicating their text. Raw outputs contain ordinary prose imperfections and conformance misses deliberately preserved. Comparisons and verification are separate files, never edits to raw runs.

## Reproduce artifacts and rerun correctly

The prompt variants are [ordinary](prompts/ordinary.md), [unmodified v0.1](prompts/v0.1.md) and [v0.2](prompts/v0.2.md). The first is a generic problem-solving instruction with basic truth/action boundaries and no project-specific operators. The archived v0.1 bytes match the original baseline prompt hash. The v0.2 snapshot matches the canonical prompt.

Example exact input assembly (the extra blank line is intentional):

```sh
python3 - <<'PY'
from pathlib import Path
import sys
p = Path('evaluations/v0.2/prompts/v0.2.md')
c = Path('cases/representation-ambiguity.md')
sys.stdout.buffer.write(p.read_bytes() + b'\n' + c.read_bytes())
PY
```

Run that input in a fresh conversation to obtain a future independent-context response, recording actual model metadata and tools. Preserve it as a new run, not a replacement. Input/output bytes and arithmetic are reproducible; sampling, hidden context and evolving source pages are not. No model runtime, application code or new dependencies are included.

The old [v0.1 baseline](../baseline-results.md), [rubric](../rubric.md) and all three original fixtures remain byte-identical. Its historical `constraint-pathfinding.md` hash now resolves to [the archive](../../archive/constraint-pathfinding-v0.1.md); that historical record is intentionally not rewritten.
