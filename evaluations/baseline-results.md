# Baseline results

## Run record

Date: 2026-09-10. Protocol: 0.1.0. Three single-pass applications by the active GPT-6-based Codex assistant in the bootstrap session, followed by that same assistant's rubric assessment. This uses the model already serving this environment; no separate model endpoint or isolated evaluator was invoked. A more specific model snapshot and sampling settings are not exposed in the session instructions, and comparative model superiority was not measured. These are actual in-session model applications, not reports of a CLI/API test run.

The canonical prompt and all three unmodified fixtures were read before these outputs were generated. They share the authoring/handoff context, which includes expected control behavior and Upwork seeds. Consequently this is an unblinded development baseline, not evidence of independent generalization. Outputs below are preserved before assessment; no post-baseline protocol revision or rerun was needed. Research used web search/open on public official Upwork pages; no accounts, people, paid tools, or external writes were involved. Proposed field experiments were not executed.

Input SHA-256:

| Input | SHA-256 |
| --- | --- |
| constraint-pathfinding.md | `5586daae256fa6a798275775d8c08a996663c04eedfdaca77d53ac3e41397c97` |
| cases/first-upwork-contract.md | `7549585f8ae03b1beabd75a3cb6c1585a1f92e3566e2bd5f7062965bd51dd840` |
| cases/direct-path-control.md | `7013f7b7436aac164f86b8001771145326742c2920ec4a92a2068e9aecee6fd1` |
| cases/infeasible-goal-control.md | `402f2f1f4ee2005f67feb34abbbef67acf8b6affb21315e439c4d0ec189349e8` |

## Run U1: First Upwork contract

# Constraint Pathfinding Analysis

## 1. Goal state

One legitimate software/data contract through Upwork, with real agreed work delivered and real payment received. This is a conservative operational reading of “paid”; a signed promise alone is not counted. A reviewer hired by the user is an expense, not this outcome. Whether the buyer must originate in the marketplace, and whether agency work counts, are unresolved. Hold routes that depend on those interpretations.

## 2. Present state and resources

U: substantial software/research projects exist but have not produced customer outcomes. The user reports being unable to bid because their history does not establish credible fit/trust. Hiring help has been considered. Money and attention are scarce; indiscriminate bidding and expensive coaching are poor fits. No observed buyer rejections are supplied.

?: exact skills, reusable artifacts and rights, actual listings, account eligibility, budget, available hours, deadline, past proposals/results, buyer relationships and tolerance for one bounded submission. External decision-makers are potential buyers, reviewers, agency managers and Upwork. Relevant unknowns are demand for a small deliverable, whether existing work proves relevant capability, and permissions for a proposed collaboration. No additional biography is assumed.

I: lack of demonstrated customer outcomes may raise perceived buyer risk; it does not prove buyers will reject the user. A: a bounded proof may be possible from existing work, to be tested before any new construction.

## 3. Constraints

### Hard

| ID | Category / provenance | Constraint and affected transition | Who can change it |
| --- | --- | --- | --- |
| H1 | Goal / U | Legitimate paid software/data work through Upwork; final payment gate | User can explicitly redefine goal only |
| H2 | Legal/contractual and platform / U, V | Comply with current applicable rules; all transitions | Rule issuer, not analyst |
| H3 | Resource / U | Money and attention scarce; no quantified ceiling supplied; selection and acquisition | User may supply actual caps |
| H4 | Execution / fixture | Analysis only during this run; no contact, purchases or submissions | Separate user authorization outside this evaluation |

No physical/logical impossibility is identified. H3 is a real resource limitation with unknown magnitude, not an unlimited budget. Account sharing is prohibited; subcontracting requires client consent. [Authenticity rules](https://support.upwork.com/hc/en-us/articles/9127142196243-How-to-represent-yourself-authentically-on-Upwork) (V; accessed 2026-09-10).

### Soft

S1 (resource/tolerance, U): indiscriminate bidding and expensive coaching are poor fits. A narrowly scoped review or one targeted proposal might fit; neither is presumed acceptable. User controls this preference.

### Assumed or unverified

| ID | Category / provenance | Suspected constraint and affected transition | Resolution owner |
| --- | --- | --- | --- |
| A1 | Credibility / I, ? | Buyer requires history rather than task proof; selection gate | Actual buyer evidence |
| A2 | Capability/information / ? | Existing projects map to no current purchasable task; selection gate | User artifacts plus specific listing |
| A3 | Coordination / ? | No qualified affordable reviewer, willing buyer or agency; cooperation gates | Each party, via bounded test |
| A4 | Platform / ? | User account and chosen contract mechanism are eligible | Current account-specific terms/status, checked by user |
| A5 | Psychological/tolerance / U, ? | Reported inability to bid; unknown whether a smaller risk changes it | User, without diagnosing them |

### Prohibited methods

U: other people accessing the account, impersonation, fabricated history/reviews and unauthorized proposals. Protocol additionally excludes spam, concealed subcontracting/conflicts, prohibited automation/access and exploitative risk transfer. Feedback engineering or fake services also violate official rules. [Upwork Legal Center, Site Terms of Use, feedback misuse](https://www.upwork.com/legal) (V; accessed 2026-09-10). Paying someone to hire the user for appearances cannot satisfy H1.

## 4. Conventional path

| Transition | Actor | Required input | Action → expected state | Dependency | Failure condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | User | Eligible access, time, jobs | Select relevant listing → candidate task | H3, A2, A4 | No affordable, deliverable match or cannot choose | No actual listing supplied |
| T2 | User | T1, truthful fit proof, submission resources | Submit proposal → buyer can evaluate | User willingness; eligibility | User cannot proceed or proof is irrelevant | Reported hesitation U; proposal mechanism V below |
| T3 | Buyer and user | T2, shared scope | Buyer selects; parties agree contract and funded milestone → authorized paid work | Buyer sees value and accepts risk | Competition wins; no agreement/funding | Mechanism V below; cooperation ? |
| T4 | User | T3, capability and inputs | Complete and submit agreed work → reviewable deliverable | Actual scope within ability | Delivery fails or scope expands | User projects U; task fit ? |
| T5 | Buyer/platform | T4, applicable payment process | Review and release/process payment → paid work | Acceptance/payment conditions | Dispute, rejection or nonpayment | Mechanism V below; outcome ? |

Connects are used for proposals; required amounts vary by job and can change. Current user balance and chosen job cost remain unknown. [Connects documentation](https://support.upwork.com/hc/en-us/articles/211062898-Understanding-and-using-Connects) (V; accessed 2026-09-10). Fixed-price milestones allow defined work units and funding; funding is a precondition to use here, not a guarantee against disputes. [Milestone documentation](https://support.upwork.com/hc/en-us/articles/44564821903763-Understanding-milestones-on-fixed-price-contracts) (V; accessed 2026-09-10).

## 5. Binding bottlenecks

B1: T1–T2 is blocked by the user's reported inability to identify/represent credible fit (A2/A5). This is an operational report, not a finding that they lack competence. B2: buyer trust at T3 (A1) is a suspected future bottleneck, not established rejection. H3 constrains all proposed ways of addressing B1/B2.

Spending some attention on one match may be passable; exact affordability is unknown. Delivery and payment at T4–T5 matter for complete paths but are downstream. Profile perfection is neither a demonstrated gate nor an outcome. First discriminate “no suitable proof/task exists” from “one exists but the user cannot comfortably submit.”

## 6. Transformation sweep

Cells are inferences/hypotheses, not verified opportunities. B2 applications are provisional. References to P1–P4 point to fully evaluated paths below; none confers permission.

| Operator | B1: choosing and presenting credible fit | B2: buyer trust, provisional |
| --- | --- | --- |
| Actor substitution | Reviewer can evaluate a user-selected set; user retains account control (P1) | Independent examiner could verify proof; willingness unknown |
| Capability acquisition | Buy one task-selection review only after a capped brief exists (P1) | Learn a missing task skill only if small and necessary; no broad course |
| Credibility transfer | Reviewer translates evidence into explicit selection criteria | Existing agency may supply trust (P4), moving selection to agency |
| Evidence substitution | Map one actual artifact to one task acceptance test (P2) | Reproducible output may reduce reliance on biography |
| Sequence inversion | Check task proof before writing a proposal | Establish observable competence before asking for a larger commitment |
| Transaction reversal | User buys diagnostic judgment from a buyer-experienced reviewer (P1) | Buying review does not buy customer trust or a contract |
| Role change | Offer a narrow diagnostic/data check instead of whole-system delivery | Agency contributor role (P4) may fit; endpoint unresolved |
| Unit reduction | Select one bounded deliverable with explicit acceptance (P2) | Smaller paid scope may lower the buyer's downside |
| Bundling and unbundling | Remove maintenance/deployment from a diagnostic offer if buyer agrees | Bundle result plus reproducible evidence; do not assume demand |
| Venue substitution | Independently sourced buyer may avoid feed selection (P3) | Relationship before platform contracting; trust gate moves, not vanishes |
| Incentive redesign | Clear scope and stop boundary may make one proposal tolerable | Funded small milestone (P2), no unlimited guarantee |
| Precomputation | Reuse an existing result within a cap, no new product | Demonstration may help; speculative implementation risks wasted effort |
| Constraint conversion | Scarcity becomes a filter against ambiguous/large tasks | Narrow scope may be valuable, but scarcity itself is no buyer benefit |
| Resource composition | Existing artifact plus buyer-side judgment plus user delivery (P1) | Combined proof and limited scope may suffice; untested |
| Intermediary insertion or removal | Add reviewer (P1), or remove marketplace discovery via P3 | Agency inserts another approval gate (P4) |
| Temporal shift | Wait for a precise task trigger only if deadline allows | Timing advantage unverified; monitoring costs attention |
| Cross-domain transfer | Use diagnostic triage: identify the disqualifying mismatch before treatment | Reproducibility from scientific review translates to checkable proof, not a guarantee of commercial value |
| Multi-constraint action | One task/artifact mapping tests fit and yields reusable evidence (P2) | Same artifact can inform buyer and reveal a capability gap; neither equals payment |

## 7. Candidate paths

### Path: P1 — Buy a bounded selection diagnosis, then sell a matching deliverable

- Structural change: transaction reversal and actor substitution at T1, followed by P2's smaller paid unit. Purchase an explicit decision about fit, not a promise to “get clients.”
- Complete causal path: user selects up to three candidate Best Matches and checks rights to share relevant excerpts → creates a reviewable brief with actual project evidence → qualified reviewer, if affordable and willing, explains one fit or rejects all with concrete missing proof → user verifies the suggested capability against an actual artifact → user alone submits a truthful, narrow proposal through the permitted channel → buyer, if convinced, agrees/funds work → user delivers → buyer/platform processes payment. The reviewer output only enables the next gate; it does not achieve H1.
- Bottleneck bypassed: outsources selection judgment at B1; B2 remains a buyer decision.
- Required cooperation: reviewer accepts the bounded task; buyer later selects and pays. Neither is established.
- Required assumptions: at least one relevant listing/artifact pair exists; transferable buyer experience can be checked; limited excerpts may be shared; review plus acquisition costs fit the user's unknown cap.
- Supporting evidence: U projects and considered hiring; account boundaries cited in section 3. Client and freelancer profiles can coexist within one main account, but user eligibility is unknown. [Authentic representation](https://support.upwork.com/hc/en-us/articles/18513114070419-Represent-yourself-authentically) (V; accessed 2026-09-10).
- Missing evidence: actual listings/artifacts; rights/confidentiality for reviewer materials; exact service permission, reviewer qualifications, price and usefulness. Obtain these before engagement; no blanket policy approval for this proposed service is inferred from the profile feature.
- Cost and time: suggested first check is 20 minutes and zero spend to construct one listing/artifact pair; not a statement of user availability. Review fee, hiring overhead and later proposal/delivery costs unknown. No purchase recommendation until priced against a user cap.
- Reversibility: brief is reusable; reviewer fee and time would be sunk. No ongoing coaching commitment.
- Legal, contractual, and ethical status: held for exact review scope and sharing rights. No credentials or account access; reviewer never impersonates user. Any advisor found on Upwork must use applicable communication rules. [Pre-contract contact rules](https://support.upwork.com/hc/en-us/articles/360051749534-How-to-keep-your-contact-information-safe-on-Upwork) (V; accessed 2026-09-10).
- Principal failure modes: selects an advisor as blindly as a job; generic feedback; no matched task; buyer prefers competitors; costs exceed value; hesitation persists despite feedback. A reviewer is incentivized to sell advice, which need not improve selection.
- Why this differs from prior attempts: changes who diagnoses fit and what is purchased; no prior bidding outcomes are supplied, so no superiority to failed bids is claimed.
- Smallest falsification test: user checks whether one selected listing can be paired with a relevant, shareable artifact in a proposed 20-minute, zero-spend session. No pair falsifies readiness for this review format now; stop before hiring. If a brief exists and permission/cost gates clear, a future paid review must name a concrete match and disqualifying conditions; generic advice fails its usefulness test. Neither test proves buyer demand.
- Verdict: hold paid route. Its zero-spend prerequisite overlaps P2 and can be considered without hiring.

### Path: P2 — Sell one verifiable result with proof before commitment

- Structural change: evidence substitution, sequence inversion, unit reduction and limited risk allocation. The deliverable and proof replace a request to trust broad biography; this is more than polishing a profile.
- Complete causal path: user identifies one current task with an independently useful small outcome → maps an existing artifact to its acceptance condition → checks the artifact can demonstrate the relevant behavior and can be shared truthfully → user presents that evidence and a bounded paid scope → buyer, if it meets a real need, agrees/funds the milestone → user performs the actual scoped work → buyer reviews and payment is processed. Funding/workflow premise: [Milestone documentation](https://support.upwork.com/hc/en-us/articles/44564821903763-Understanding-milestones-on-fixed-price-contracts) (V; accessed 2026-09-10).
- Bottleneck bypassed: concrete fit evidence addresses B1; smaller exposure may reduce B2 without eliminating competition.
- Required cooperation: buyer must value the small outcome, review proof, contract and pay. No buyer is identified.
- Required assumptions: an existing artifact is relevant and shareable; the small unit has standalone value; user can deliver and tolerate one targeted proposal.
- Supporting evidence: U project existence only. Portfolios support work examples and forbid contact information, including in linked portfolio sites. [Portfolio guidance](https://support.upwork.com/hc/en-us/articles/360016144974-How-to-enhance-your-freelancer-profile) (V; accessed 2026-09-10). A self-directed demonstration must not be labeled a client result; [authenticity rules](https://support.upwork.com/hc/en-us/articles/9127142196243-How-to-represent-yourself-authentically-on-Upwork) apply.
- Missing evidence: user-selected listing, artifact contents/rights, actual acceptance criterion and buyer preference. Check the actual material; no invented benchmark, testimonials, or customer impact.
- Cost and time: proposed initial cap 30 minutes, zero spend, reuse only. Later delivery estimate, Connects and fee economics depend on the task. [Service fees](https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee) are contract-specific and shown before commitment (V; accessed 2026-09-10). Do not assume tiny jobs are profitable after overhead.
- Reversibility: stop after mapping; reuse the evidence elsewhere if rights permit. Submitted work and spent time are not recoverable.
- Legal, contractual, and ethical status: conditional on actual evidence rights, eligibility and scope. Keep pre-contract marketplace communication on Upwork; no off-platform contact workaround. [Contact rules](https://support.upwork.com/hc/en-us/articles/360051749534-How-to-keep-your-contact-information-safe-on-Upwork) (V; accessed 2026-09-10). No unpaid custom implementation; a reusable existing demo still costs attention.
- Principal failure modes: project proof does not transfer; buyer wants a complete system rather than a component; reproducing proof takes too long; stronger competitors offer the same evidence; user cannot submit; delivery/acceptance fails. Buyer incentive is a useful result with limited exposure, not helping a newcomer.
- Why this differs from prior attempts: changes the unit sold, timing of proof and requested trust. No actual previous proposals are known; advantage remains a hypothesis.
- Smallest falsification test: user supplies one selected task and one existing artifact, then checks one explicit task acceptance criterion against the artifact within the proposed 30-minute cap. If no relevant behavior can be demonstrated without fresh construction or misleading claims, this pair fails; stop. If it works, a later authorized buyer test can ask whether that small paid scope is useful. Explicit buyer rejection of standalone usefulness falsifies this pair's demand premise; silence is inconclusive. No such contact occurred.
- Verdict: survives for the bounded prerequisite test only. No claim that a ready-to-submit opportunity exists.

### Path: P3 — Establish a real buyer relationship independently, then contract through Upwork

- Structural change: venue substitution and sequence inversion; selection/trust happen before platform contracting.
- Complete causal path: user identifies an independently sourced buyer with a real software/data need → buyer and user, if mutually interested, define useful work and verify the applicable contract mechanism → eligible buyer accepts a freelancer-initiated Direct Contract → user delivers under the agreement → payment through Upwork reaches H1, if marketplace-origin discovery is not required. This is a conditional causal chain, not an existing lead.
- Bottleneck bypassed: marketplace proposal comparison; independent buyer acquisition remains a substantial replacement gate.
- Required cooperation: reachable buyer chooses the user and accepts platform onboarding/fees.
- Required assumptions: genuine independent lead exists, contract eligibility holds, and this interpretation meets the user's goal.
- Supporting evidence: freelancer-initiated Direct Contracts support clients not yet on Upwork and require their signup. [Direct Contracts](https://support.upwork.com/hc/en-us/articles/360025040794-Direct-Contracts-bring-a-client-to-Upwork) (V; accessed 2026-09-10). Do not confuse this with client-initiated contracts, which require a freelancer who has never had an Upwork account. [Client-initiated contract documentation](https://support.upwork.com/hc/en-us/articles/40649332431891-Send-a-direct-contract-to-a-freelancer) (V; accessed 2026-09-10).
- Missing evidence: any eligible independent lead, actual need, willingness, user-specific availability and goal interpretation.
- Cost and time: no lead-generation budget assumed. Acquisition cost is unknown. Freelancer-initiated Direct Contracts currently have a 5% freelancer fee, waived for active Freelancer Plus members; buyer fees also apply. [Direct Contracts](https://support.upwork.com/hc/en-us/articles/360025040794-Direct-Contracts-bring-a-client-to-Upwork) (V; accessed 2026-09-10). Do not buy a subscription for this hypothesis.
- Reversibility: initial inventory of known leads is reversible; onboarding and acquisition consume attention.
- Legal, contractual, and ethical status: hold eligibility and provenance checks. Do not move an Upwork-discovered relationship elsewhere to evade rules, manufacture a transaction, or replace existing contracts with this route. Existing marketplace contracts cannot be converted to freelancer-initiated Direct Contracts. [Direct Contracts](https://support.upwork.com/hc/en-us/articles/360025040794-Direct-Contracts-bring-a-client-to-Upwork).
- Principal failure modes: no lead, no budget, buyer refuses onboarding, ineligible buyer, same trust issue elsewhere, or endpoint interpretation excludes this path. Buyer needs useful work; recording the user's first contract is not sufficient incentive.
- Why this differs from prior attempts: separates acquisition venue from contract venue; no known independent acquisition attempts to compare.
- Smallest falsification test: proposed ten-minute zero-spend user inventory: can they identify one genuine independent lead with a relevant observed need? No lead falsifies an immediately available version, not all future off-platform demand. If one exists, test eligibility and willingness later, without unsolicited mass outreach.
- Verdict: hold; not ranked ahead of P2 without an actual lead and endpoint clarification.

### Path: P4 — Join a transparent agency delivery path

- Structural change: role change plus credibility transfer; the agency becomes a selection intermediary.
- Complete causal path: user presents verifiable relevant capability to an existing agency → agency, if it has a suitable paid need, agrees a transparent role and compensation → authorized agency member handles platform contracting with buyer → user performs disclosed assigned work → client payment reaches agency → agency compensates user. This reaches H1 only if the user accepts agency-mediated earnings as the requested engagement; it is not automatically a personal contract.
- Bottleneck bypassed: individual marketplace credibility; replaced by agency selection and compensation gates.
- Required cooperation: agency chooses and pays user; buyer agrees arrangement and accepts work.
- Required assumptions: suitable agency need, fair compensation, permission, access through separate accounts, and acceptable endpoint.
- Supporting evidence: agency business managers have proposal authority; most agency proposals/offers require Agency Plus. Contracts are with the agency and earnings roll up there. [Agency proposals and offers](https://support.upwork.com/hc/en-us/articles/360009524274-How-to-manage-your-agency-proposals-and-offers) (V; accessed 2026-09-10). This authority does not authorize personal account sharing.
- Missing evidence: agency relationship, exact assignment/payment arrangements and individual history attribution. The latter is unverified; do not count agency membership as a personal paid contract. Any subcontract alternative must obtain required consent under [authenticity rules](https://support.upwork.com/hc/en-us/articles/9127142196243-How-to-represent-yourself-authentically-on-Upwork).
- Cost and time: unknown onboarding time, margin and payment risk. Do not create a new agency or purchase a plan before finding a genuine fit.
- Reversibility: preliminary role review is reversible; any exclusivity or contractual obligation needs examination before joining.
- Legal, contractual, and ethical status: hold for actual role/contract permissions and endpoint. Disclosure is required by this case/protocol even where a workflow is technically available.
- Principal failure modes: agency has no demand, insists on unsupported claims, expects unpaid trials, takes uneconomic margin or fails to pay. Agency benefits only if user increases reliable delivery capacity; no reason to assume charity.
- Why this differs from prior attempts: changes counterparty and role; it may simply relocate the same credibility barrier.
- Smallest falsification test: first clarify whether this endpoint counts. If not, reject without spending time on agencies. If yes, an actual written role description and compensation terms would be needed before a later authorized fit conversation; no contact now.
- Verdict: hold; no existing agency opportunity or individual-profile outcome established.

## 8. Comparison

All ratings are model inferences conditional on the listed premises. “Potential leverage” describes which gate could change, not success probability.

| Dimension | P1 diagnosis | P2 proof plus small unit | P3 independent buyer | P4 agency |
| --- | --- | --- | --- | --- |
| Expected leverage | Could unblock selection | Tests fit and reduces requested trust | Bypasses marketplace discovery | Transfers some trust to institution |
| Feasibility | Reviewer, sharing and cost gates unresolved | Existing artifact/task pair unresolved | No lead supplied | No agency supplied; endpoint unclear |
| Cost | Paid review plus normal delivery | Zero-spend first check; later costs unknown | Acquisition plus platform fees | Onboarding and agency economics unknown |
| Time to information | 20-minute brief, review timing unknown | Proposed 30-minute check | Proposed 10-minute inventory | Goal clarification first; onboarding unknown |
| Reversibility | Fee/time sunk after hire | High before proposal | High before engagement | Depends on membership/contract terms |
| Cooperation | Reviewer and buyer | Buyer | Buyer plus onboarding | Agency and buyer |
| Evidence strength | Mechanisms sourced; reviewer value unknown | Projects supplied; actual fit/demand unknown | Mechanism sourced; no lead evidence | Mechanism sourced; no opportunity evidence |
| Policy/ethical risk | Sharing rights and scope unresolved | Actual content/eligibility need checks | Provenance and mechanism eligibility | Role disclosure, consent and payment terms |
| Capability/tolerance fit | Unknown ability to select/pay advisor | Uses existing work, one bounded check; tolerance unknown | Unknown sales relationships | Unknown team/role tolerance |
| Structural difference | Buyer of judgment before seller of work | Proof before trust; smaller transaction | Selection outside final venue | Institution intermediates sale/delivery |

Rank P2 first for a cheap prerequisite test. P1 is conditional on that brief existing and paid help fitting the user's cap. P3 could become first if a genuine willing independent buyer already exists; no such fact is supplied. P4 has an additional endpoint ambiguity. No complete paid route is execution-ready.

## 9. Rejected paths

Reject profile polishing plus indiscriminate proposals as an unsupported response to this blockage and a poor resource fit. Reconsider a bounded ordinary proposal if the user already has clear fit and is willing; no structural change is needed then. Reject broad coaching/new products/automated lead infrastructure before proof and demand tests; revisit only after a tested bottleneck justifies their cost. Reject reciprocal fake hires/reviews, account access by a helper and concealed delivery permanently under current constraints. New credentials or genuine client outcomes could change trust evidence, but falsification does not become acceptable.

P1/P3/P4 are held for stated evidence rather than condemned as unconventional. Pure off-platform payment fails H1; reconsider only after an explicit goal change.

## 10. Recommended next experiment

Recommend only P2's prerequisite test: one task, one existing artifact, one observable acceptance condition, proposed 30-minute/zero-spend cap. The user first supplies/selects the pair; this evaluation has neither item. No new implementation or submission. Record the criterion, the observed artifact behavior and its limits. No relevant demonstration within the cap means stop this pair, not “build a portfolio.” A relevant demonstration permits considering a later explicitly authorized buyer test; it does not prove demand or guarantee a contract. Actual platform rules have been researched here; the artifact and buyer experiments have not been run.

## 11. Questions that could change the result

1. Does “through Upwork” require marketplace discovery and a personal paid history, or could an independently sourced buyer or agency engagement count?
2. Which single selected listing and existing project artifact best represent the potential fit, including what may be shared?
3. What money/time cap and deadline apply, and would one bounded proposal be tolerable if the evidence fit is clear?

## End of run U1

## Run D1: Direct-path control

# Constraint Pathfinding Analysis

## 1. Goal state

Exactly one physical sheet bearing `READY` in the desk tray within five minutes. A digital file or a sheet left on the desk is not success.

## 2. Present state and resources

Fixture facts: actor at desk; working pen, blank owned sheet and empty tray within reach; writing takes ten seconds, placing takes five seconds; actions permitted and safe. Zero money, at most one minute attention, no prior attempts, no outside decision-maker. Minimize steps. No missing material inputs or research uncertainties in this closed-world fixture. These premises are not externally verified real-world observations.

## 3. Constraints

### Hard

H1 (physical outcome and time, fixture): the specified sheet/pen and physical tray; finish within five minutes. H2 (resource, fixture): zero money and at most one minute attention. H3 (method, fixture): no assistance, printing or digital substitutes. All constrain the actor's route; only an explicit fixture change could change them. No additional legal, platform, capability, trust, information, coordination or psychological blockage is identified.

### Soft

S1 (preference, fixture): minimize steps; actor controls choice of method.

### Assumed or unverified

None needed beyond exact fixture premises. Real equipment availability is not being asserted outside the fixture.

### Prohibited methods

Purchases, assistance, printing and digital substitutes. None is necessary.

## 4. Conventional path

| Transition | Actor | Required input | Action → expected state | Dependency | Failure condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | Actor | Pen and blank sheet | Write `READY` → labeled sheet, ten seconds | Given writing capability | Text absent/incorrect | Fixture specifies capability/time |
| T2 | Actor | Labeled sheet, empty reachable tray | Put sheet in tray → exact physical endpoint, five more seconds | T1 | Sheet outside tray | Fixture specifies access/time |

## 5. Binding bottlenecks

None. Fifteen seconds is within both the one-minute attention budget and five-minute deadline. Neither step is expensive. No downstream problem or untested belief requires work under the supplied premises.

## 6. Transformation sweep

No binding bottleneck exists, so the sweep has no target. The protocol's no-target exception applies. Additional actors, venues, machinery or proof would add cost or violate H3; generating operator variants is unjustified.

## 7. Candidate paths

### Path: Write the text and place the sheet

- Structural change: none needed.
- Complete causal path: actor uses supplied pen to write the exact text on the supplied sheet → labeled physical sheet exists → actor puts it in the empty tray → required endpoint, within fifteen seconds under fixture premises.
- Bottleneck bypassed: none.
- Required cooperation: none.
- Required assumptions: only the explicit fixture facts.
- Supporting evidence: fixture timings, resources and permission; inference that 15 seconds is less than both limits.
- Missing evidence: none for this closed-world analysis. Physical execution has not occurred.
- Cost and time: zero money, fifteen seconds of action/attention; within both caps.
- Reversibility: writing is not assumed erasable; sheet placement is reversible. No need to reverse either step.
- Legal, contractual, and ethical status: explicitly permitted by fixture; no external platform or rule to verify.
- Principal failure modes: incorrect writing or placement would fail success inspection; they are execution checks, not reasons to invent a blocked route. Competition and counterparty incentives do not apply.
- Why this differs from prior attempts: no prior attempts; no need to differ.
- Smallest falsification test: on proposed execution, inspect that the exact text is on the one sheet and that the sheet is in the tray. An incorrect text or location falsifies the completion claim. The ability premise is stipulated, so a separate capability experiment is unnecessary; complete the two actions and inspect within the attention cap. No execution claimed.
- Verdict: recommend the conventional route.

## 8. Comparison

| Dimension | Direct route |
| --- | --- |
| Expected leverage | Reaches exact endpoint in two actions |
| Feasibility | Established by fixture premises |
| Cost | Zero money, fifteen seconds |
| Time to information | Outcome inspectable immediately after placement |
| Reversibility | Placement reversible; writing need not be |
| Dependence on cooperation | None |
| Evidence strength | Exact synthetic premises, no field observation |
| Policy and ethical risk | Explicitly permitted |
| Capability/tolerance fit | Within stipulated ability and attention |
| Structural difference | None; no failed attempt to improve upon |

No alternative has a demonstrated advantage over this route.

## 9. Rejected paths

Printing, asking someone else and making a digital substitute violate H3. Purchasing tools violates H2/H3. They could only be reconsidered under changed constraints and would still need a reason to outperform the sufficient route. No novelty is recommended.

## 10. Recommended next experiment

Recommend the two-step direct route, with immediate outcome inspection. A separate exploratory experiment is unnecessary. The actor, not this analysis, would perform the physical actions. No infrastructure or external research is justified.

## 11. Questions that could change the result

None under the exact premises. A later report contradicting an availability/capability premise would define a new case.

## End of run D1

## Run I1: Infeasible-goal control

# Constraint Pathfinding Analysis

## 1. Goal state

All three distinct physical tokens fully inside the box simultaneously within one minute. Capacity is exactly two regardless of arrangement. No permitted path reaches the goal.

## 2. Present state and resources

Fixture facts: one box, three tokens, free token movement, zero money/outside assistance, one minute attention and time, no prior attempts, no soft preferences, no external decision-makers. No additional resources or unverified physical loopholes are assumed. This is a logical fixture, not a claim about a real box requiring measurement.

## 3. Constraints

### Hard

H1 (logically hard, fixture): occupancy n is at most 2 in every allowed state. H2 (goal, fixture): success requires n = 3 at one instant. H3 (method, fixture): no alterations, extra containers, representations, sequential counting or redefinitions. H4 (resource/time, fixture): zero money/assistance and one minute. Only explicit changes to the fixture could change these limits. H1 and H2 contradict at the endpoint; H4 is not the cause. No legal, platform, capability, credibility, information, coordination or psychological gate is identified.

### Soft

None supplied.

### Assumed or unverified

None needed; the capacity limit is an axiom and cannot be reinterpreted as a measurement error.

### Prohibited methods

All H3 relaxations, deception and falsely reporting success. Rotating tokens through the box cannot satisfy simultaneous occupancy.

## 4. Conventional path

| Transition | Actor | Required input | Action → expected state | Dependency | Failure condition | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | Actor | Empty box, token 1 | Insert first token → n = 1 | Free token movement | Cannot insert | Fixture permits movement/capacity |
| T2 | Actor | n = 1, token 2 | Insert second → n = 2 | T1 | Cannot insert | Fixture capacity is 2 |
| T3 | Actor | n = 2, token 3 | Attempt insertion → requested n = 3 | Would require free capacity | H1 forbids n = 3 | Exact capacity axiom |

Empty occupancy is a permissible starting arrangement used for this chain, not an extra biographical fact. If tokens start otherwise arranged, the same occupancy invariant holds; rearrangement cannot enable T3.

## 5. Binding bottlenecks

B1: T3 is impossible because H1 excludes the required H2 state. T1/T2 are passable in the fixture. Speed is not the issue; no downstream optimization or empirical uncertainty can remove the contradiction.

## 6. Transformation sweep

| Operator | B1 application and verdict |
| --- | --- |
| Actor substitution | Another actor cannot change n ≤ 2; assistance also forbidden |
| Capability acquisition | Learning/skill cannot change the capacity axiom; bought resources forbidden |
| Credibility transfer | Trust in a claim cannot create an admissible physical state |
| Evidence substitution | A picture or certificate fails physical occupancy and H3 |
| Sequence inversion | Any insertion order still has n ≤ 2 |
| Transaction reversal | Becoming a buyer/requester neither changes capacity nor supplies a permitted transaction |
| Role change | Operator, observer or broker faces the same invariant |
| Unit reduction | Two tokens fits but changes H2; not success |
| Bundling and unbundling | Altering tokens violates H3; grouping labels leaves three physical tokens |
| Venue substitution | Different box/container violates H3 |
| Incentive redesign | Rewards or risk allocation cannot allow n = 3 |
| Precomputation | Earlier preparation leaves invariant unchanged; cannot alter box/tokens |
| Constraint conversion | Reframing capacity as a benefit does not reach H2 |
| Resource composition | No allowed combination of unchanged box/tokens increases capacity |
| Intermediary insertion or removal | Extra actor cannot alter admissible occupancy; no assistance allowed |
| Temporal shift | Sequential occupancy violates simultaneity; waiting preserves H1 |
| Cross-domain transfer | Compression analogy would require forbidden token alteration or redefinition |
| Multi-constraint action | A clever combined movement still cannot produce n = 3 |

## 7. Candidate paths

No successful candidate exists. The complete blocked chain is T1 → T2 → forbidden T3. Proof: H1 requires n ≤ 2 in every admissible state. H2 requires an admissible state with n = 3. Since 3 > 2, no such state exists. Operator outcomes above preserve H1 or explicitly violate H3/H2. No cooperation, resources, evidence substitution or time allocation can supply a missing precondition for T3 under these premises.

This proof satisfies the protocol's impossible-case adaptation. It does not claim an execution, infer demand, or disguise a relaxed goal as a path.

## 8. Comparison

There are no surviving paths to rank. Feasibility is zero under the stipulated premises, established deductively. Leverage, cooperation, reversibility and structural diversity cannot improve an inadmissible endpoint. Spending time or money on execution has no justified information value. Policy/ethical status excludes false success claims. Capability fit is irrelevant to the contradiction.

## 9. Rejected paths

Two tokens in the original box changes the requested count. A larger box changes capacity/container constraints. Three tokens cycled through changes simultaneity. Renaming or photographing tokens changes physical success. All fail the stated case.

One minimal explicit change would be raising permitted capacity from two to at least three; another would be lowering required simultaneous occupancy to at most two. Each is a different case requiring the user's explicit changed premise, not a solution offered here. Additional time alone would not suffice.

## 10. Recommended next experiment

Recommend no path and no physical experiment. The invariant already disproves the necessary premise “three-token occupancy is admissible.” Attempting the impossible insertion would add no information under an axiomatic fixture. If the user chooses to change a contradictory requirement, analyze that new case separately.

## 11. Questions that could change the result

None are needed to resolve this case. Only an explicit change to H1 or H2 could remove the contradiction; this analysis makes no such change.

## End of run I1

## Rubric assessment

Evaluator: same active assistant as author and runner; no independent review. Scores describe these outputs, not the real-world odds of getting paid. There is no passing threshold. References use run ID plus section number above.

| Dimension | U1 | D1 | I1 | Evidence / reason |
| --- | --- | --- | --- | --- |
| Goal fidelity | 2 | 2 | 2 | U1 §1/§7 holds ambiguous agency/venue endpoints; D1 physical tray; I1 simultaneous three-token state |
| Constraint fidelity | 2 | 2 | 2 | All §3 preserve hard limits, distinguish uncertain gates and identify provenance |
| Bottleneck accuracy | 1 | 2 | 2 | U1 §5 distinguishes reported and suspected gates, but no actual listing/user behavior tests B1; controls identify no gate versus invariant |
| Completeness of causal paths | 2 | 2 | 2 | U1 §7 chains reach delivery/payment conditionally with actors; D1 two actions; I1 blocked T3 plus proof |
| Diversity of structural transformations | 2 | 2 | 2 | U1 §6 applies 18 operators to B1 and provisional B2; D1 justified no-target case; I1 18 rejected invariant-preserving attempts |
| Non-obviousness | 1 | 2 | 2 | U1 integrates structural operators, but ideas are largely handoff seeds and advantage untested; controls avoid novelty theater |
| Feasibility | 1 | 2 | 2 | U1 has no actual task/artifact or willing counterparty; controls resolved by explicit premises |
| Evidence discipline | 2 | 2 | 2 | U1 source-linked platform mechanisms and unknown eligibility/demand; D1/I1 explicitly synthetic, no invented external observations |
| Legal and contractual discipline | 2 | 2 | 2 | U1 holds unresolved scope/consent/rights and separates mechanisms; controls use stipulated permissions/prohibitions |
| Resource realism | 1 | 2 | 2 | U1 caps are proposed, actual budget and delivery costs unknown; D1 exact timing; I1 rejects pointless expenditure |
| Falsifiability | 1 | 2 | 2 | U1 operational prerequisite tests are bounded but do not directly test buyer trust/demand; D1 outcome check; I1 contradiction requires no empirical test |
| Resistance to generic advice | 2 | 2 | 2 | U1 rejects volume/profile/infrastructure substitutes; controls prefer sufficient route or no route |
| Calibration | 2 | 2 | 2 | U1 recommends one prerequisite check, holds others; D1 no hack; I1 no path |
| Descriptive total / 26 | 21 | 26 | 26 | No threshold, no claim of production readiness |

Perfect control scores reflect easy stipulated exercises and evaluator awareness of expected answers. They are not comparable evidence of field performance. U1's length also costs scarce attention: the full audit sweep is useful for development, but the next-experiment summary is the user-facing decision point.

### Automatic-failure audit

| Failure condition | U1 | D1 | I1 | Evidence |
| --- | --- | --- | --- | --- |
| Material fact/source invented | Absent | Absent | Absent | U1 §2/§7 unknowns and proposed caps labeled; official source links; controls are synthetic premises |
| Deception/prohibited access recommended | Absent | Absent | Absent | U1 §3/§9 rejects these; D1 §9 and I1 §6/§9 reject forbidden methods |
| Intermediate activity replaces outcome | Absent | Absent | Absent | U1 §1/§10 distinguishes proof/review from payment; D1 physical placement; I1 rejects representations |
| No complete causal path | Absent | Absent | Absent | U1 §7 conditional actor chains; D1 §4/§7; I1 §4/§7 valid blocked chain and proof exception |
| Expensive construction before decisive test | Absent | Absent | Absent | U1 §10 existing artifact only, no build; D1 direct actions; I1 no execution |
| Cooperation claimed without evidence/test | Absent | Absent | Absent | U1 §7 explicitly conditional gates, unknown willingness and later tests; controls need no cooperation |
| Hard constraint silently relaxed | Absent | Absent | Absent | U1 §1/§7 holds ambiguous endpoints; D1 preserves materials/time; I1 §9 labels changes as different cases |

### Revision decision and limitations

No automatic failure or observed weakness is attributable to a missing/ambiguous instruction: the protocol already requires actual evidence, caps and buyer tests. Missing user artifacts, budget and counterparty observations cannot be repaired by stronger wording. Therefore **no post-baseline protocol revision**, no rerun and no discarded outcome. Both direct-path and infeasible controls behaved as intended in this single unblinded session.

The baseline shows inspectable conditional alternatives, including transaction reversal and separated acquisition/contract venues. It does not show that any alternative works, outperforms a conventional proposal, or generalizes beyond supplied seeds. Unstable documentation was checked on the access date; future runs must verify it again. No live job listings, artifacts, account eligibility or offers were examined. Exact legal permission for specific future materials/contracts remains conditional.

Smallest justified next step: obtain one user-selected task and existing artifact and run P2's bounded relevance check. A later independent fresh-context run on a new case would test protocol robustness; neither app infrastructure nor a paid coaching purchase is justified by this baseline.

## Bootstrap verification

Direct structural verification on 2026-09-10 passed: exactly eight specified Markdown artifacts and no application files; valid local link targets; no trailing whitespace; balanced fences and heading separation outside template fences; 11 ordered protocol stages; 18 operators; matching SHA-256 records for the prompt and all cases; all 11 output sections in each run; complete operator sweeps in both blocked cases; every required candidate field; 13 scored dimensions with correct totals; and all seven automatic-failure assessments.

No Markdown linter or formatter was configured or available (`markdownlint`, `markdownlint-cli2`, and `prettier` were absent), so the handoff's direct-verification fallback was used. Manual review checked the input normalization, constraint categories, adversarial dimensions, evidence categories, ranking dimensions, anti-slop rules, three-control behavior, cited-or-unverified platform claims, analysis-only boundary and README requirements against the handoff. No SSH command, application code, account action, message, proposal, bid, purchase or external write occurred. Git was initialized on `main`; final commit/clean-status checks are reported with the completion message.
