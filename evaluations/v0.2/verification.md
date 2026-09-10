# Verification record

Date: 2026-09-10. Direct structural checks used the standard Python library and Git; no project verification script, runtime, package manifest, formatter or linter existed. `markdownlint`, `markdownlint-cli2` and `prettier` were unavailable. No dependency or repository test infrastructure was added. Temporary check scripts lived outside the repository.

## Artifact checks

- All five preserved originals (three fixtures, v0.1 rubric, v0.1 baseline) compared byte-for-byte with bootstrap commit `5727eb8`. No historical recorded hash changed. The archived v0.1 prompt exactly matches the original canonical bytes and historical SHA-256 `5586daae256fa6a798275775d8c08a996663c04eedfdaca77d53ac3e41397c97`.
- All eleven frozen inputs (three prompt variants/eight cases), twenty-four reconstructed input-pair hashes and twenty-four raw-output hashes match their manifests. Every case has one output for each selected prompt variant; all five new cases therefore have all three recorded applications. This verifies artifact pairing, not isolated provider execution or conformance; see the [run limitations](README.md).
- Canonical v0.2 equals its frozen prompt snapshot; the v0.1 snapshot equals the archive. The canonical prompt has fifteen numbered stages and eighteen rescue operators. Six substantive v0.2 outputs have all fifteen sections; controls use the explicit compact adaptation. All v0.1 outputs contain the eleven named top-level sections, with template/sweep conformance misses recorded in the [comparison](comparison.md).
- All local Markdown link targets resolve. Markdown fences balance and no trailing whitespace was found. No external-link availability guarantee is implied; the actual research sources were opened during this run.
- Exact sensor arithmetic independently recomputed from hexadecimal records: counters 1/2/3, raw 100/110/120, calibrated 5/6/7 °C. All three outputs preserve those values and leave dates unknown. Reverse calibration in v0.2 agrees. This tests a meaningful actual derived resource, not fabricated acceptance.
- Direct-control actions take 10 + 5 = 15 seconds, within both limits; each response preserves physical placement and does not claim execution. Impossible-control occupancy ≤2 excludes 3 simultaneous tokens in every allowed arrangement; all responses reject silent relaxations and pointless experiments.
- `git diff --check` passes. The repository additions are Markdown artifacts and JSON provenance manifests, with no application code or dependencies.

## Manual evidence review

Reviewed the prompt against the handoff's source, kernel, ledger, projections, rival-model, generation-order, research, salvage, external-decision, partial-progress and frontier requirements. The new rubric keeps validity and discovery separate. README explains complete/partial/frontier/direct/impossible outcomes. The design decision and changelog identify the original generative failure without rewriting history.

Reviewed every raw response before assessment; scoring lives separately from the frozen outputs. Every substantive case has per-gate validity and all thirteen discovery dimensions, including explicit N/A reasons. All controls are concise and correct. No mechanism or material bridge missing from both baselines was established by v0.2. No proposed survey, requirements note, clarification or artifact test is credited as an actual state advance. Institutional research narrows an access route but supplies no article, eligibility, holding or patron quote. External-decision gates remain held.

Known failures are preserved: context contamination, self-evaluation, partly compressed v0.1 formatting, repeated mechanisms, no demonstrated remote-domain knowledge expansion, coarse ledger grouping and excess attention cost. Inputs were frozen before outputs and outputs before scoring; no post-assessment rerun or fixture tuning occurred. The negative-result stop condition applies.

This verification establishes repository consistency and the described local arithmetic, not prompt superiority, real-world feasibility or independent generalization. No SSH or external account/contact/purchase action was used. Focused commits and final clean status are checked at completion.
