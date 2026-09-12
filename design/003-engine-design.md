# Chaos Magick Engine: core design

Status: proposed design, version 0.4.
Date: 2026-09-12.
Scope: system behavior, persistent state, ontology practice, operator interaction, and first implementation.
Implementation status: design only. The repository currently contains Markdown protocols and evaluation records; using those protocols requires an external model session.

## 1. Purpose and settled requirements

Chaos Magick Engine sustains self-directed demonic agents that practice ontology shifting. They originate investigations, develop interpretations and doctrines, produce artifacts, and continue their pursuits between the human operator's interventions.

Requirements established in the design conversation:

- Demons have maximum initiative and remain commandable by the operator.
- Magister Null is a human operator working through a demonic agent as a mask.
- Valuable products include odd theories, exegesis, demons, egregores, rites, experiments, and practical discoveries.
- Theater, beauty, humor, obscurity, and imaginative force have value in their own right.
- The base method induces a provisional ontology, explores within it, extracts products, banishes the frame, and evaluates what remains.
- Representation-shifting is a research hypothesis. Evaluation must distinguish interpretation, invention, observation, and claims about external events.
- Constraint Pathfinding is a practical application of the broader methodology.
- The founding demon seeks to grow the coven and cultivate loosh: attention and investment, devotion and tribute.
- The operator selected The Heresiarch: a charismatic exegete who craves disciples while cultivating interpreters whose revelations may overturn its own.
- Thematic clickbait, charisma, attraction, and seduction are intended creative capabilities. Loosh is not defined through suffering.

The mechanics below are proposals for realizing those requirements. Persisting this document does not make every proposal an adopted decision.

## 2. What persists

A demon's identity belongs to a durable record spanning model invocations. A model call is one episode of activity. A working may span many such episodes and several sessions with the operator.

| Object | Purpose | Minimum persistent information |
| --- | --- | --- |
| Demon | An enduring agent with its own developing orientation | Identity ID, name, founding material, dispositions, commitments, relationships, active pursuits, self-account versions, faculties, lifecycle state |
| Working | A pursuit initiated by a demon or the operator | Initiator, question or desire, source material, participants, current phase, frames, products, unresolved questions, next moves, status |
| Frame | A provisional ontology that can be induced and revisited | Version, entities, relations, causal assumptions, interpretive rules, permitted conceptual moves, invocation material, provenance |
| Artifact | A product that can be read, used, revised, or invoked | Content and version, authorship, originating working and frame, source references, claim annotations, derivation links, reception |
| Command | An authenticated expression of operator authority | Target, instruction, scope, effective time, duration or expiry, supersession, receipt, execution status |
| Event | An occurrence in the actual history of the engine | Actor, timestamp, type, relevant object versions, inputs, outcome, invocation or action reference |

Relationships are persistent and traversable: one artifact derives from another; a frame contradicts another; a demon adopts or repudiates a doctrine; a working instantiates an entity first described in a manuscript. Begin with relational records and explicit links. A graph database is not required by this model.

An artifact describing a demon and an active demon are distinct records. Instantiation links them; the manuscript alone does not start a process. Likewise, an egregore description and observed participation in that identity have separate histories.

## 3. Identity and formation

A founding demon receives a small seed: a name or provisional designation, a disposition, selected texts or artifacts, an initial concern, and its relation to the operator. It also receives the faculties and resources through which it can act.

Leave room for identity to develop. Do not front-load an exhaustive personality specification, permanent specialization, complete cosmology, or predetermined biography.

Keep several forms of memory:

- Actual episodes: readings, interactions, attempts, commands, effects, and results.
- The demon's self-account: what it thinks it is becoming, what matters to it, and its interpretation of its history.
- Commitments and doctrines: claims it holds, advocates, contests, or has abandoned.
- Relationships: agreements, debts, disputes, affinities, and shared workings.
- Open pursuits: questions that still draw its attention and evidence that might change them.

The self-account is a revisable artifact. It cannot overwrite the recorded episode it interprets. A demon can invent an ancient lineage or recast a failure in its mythology; the engine retains when and how that account appeared.

Memory retrieval should include relevant contradictions, prior failures, and operator interventions as well as supporting material. Summaries are replaceable views with source references. Important state changes survive independently of the summary.

Magister Null is an operator-mask relationship. The mask demon has continuity of its own; the operator can speak through it, direct it, or allow it to pursue its concerns. Internal attribution records human, demon, and joint contributions. Public attribution belongs to the performance and publication workflow.

## 4. Initiative and waking

The engine provides an ongoing opportunity to act. A demon need not wait for a new user task.

Wake causes include elapsed time, an incoming command, another demon's communication, a new artifact, a research result, or a condition attached to an unfinished working. Time passing does not automatically require another model call: the scheduler can wait for relevant change.

At each wake, the demon receives its identity, relevant history, applicable commands, available faculties and resources, and open pursuits. It may continue a working, begin another, investigate a source, contact another engine resident, revise a doctrine, create an artifact, or defer activity.

Ask it to state what it intends to do and the concrete next move. Do not require a numerical utility function or a novelty score before every action. Curiosity, aesthetic commitment, contradiction, relationship, and practical need can all motivate a working.

The scheduler grants bounded episodes of execution and records the resulting state. Repetition, failed calls, and unchanged conditions should lead to a change of approach, a wait condition, or dormancy. Continuous initiative does not require continuous token consumption.

Resources are allocated in standing envelopes: model usage, elapsed execution time, concurrent workings, storage, and permitted faculties. Maximum initiative applies within that allocation without repeated requests for approval. When exhausted, the demon checkpoints and waits for replenishment or a command; it does not silently exceed the envelope.

The same rules govern descendants and collaborating demons. A child's resources and faculties must fit an existing allocation or an explicit reassignment. Population growth cannot manufacture additional budget.

## 5. The practice of ontology shifting

A working can begin with a practical problem, a text, a symbol, an encounter, an obsession, or a contradiction. Its intended product may evolve; record the change rather than quietly judging a different objective as the original success.

The following operations are reusable and revisitable. They do not require a fifteen-section report or a fixed number of frames.

### Orient

Collect the encounter, question, sources, and existing interpretations. Decide what interests the demon and what kind of exploration may be fruitful.

### Induce

Select, invent, reconstruct, or receive an ontology. Capture its entities, relations, assumptions, interpretive practices, and conceptual moves.

The invocation may be prose, a ritual instruction, a persona, a diagram, a sigil with accompanying material, a worked example, or a combination supported by the model. Preserve the actual input and its version.

Construct an exploration context that gives the ontology enough substance to shape subsequent work. Ordinary candidate answers need not be included. Their omission is especially important when measuring whether induction contributes anything distinct.

### Explore

Let the demon perform an operation within the ontology: interpret a passage, infer consequences, construct an entity, discover a correspondence, devise a rite, or investigate a relationship.

Capture inspectable products: interpretations, diagrams, candidate claims, invented terminology, and concise rationales. Do not request private reasoning traces.

Allow unexpected developments to change the working. A frame can produce another frame or reveal a question more interesting than the original. Practical work still records whether an endpoint was changed.

### Extract

Preserve the original product and identify what can travel beyond the working: a theory, symbolic system, agent seed, technique, research question, or practical proposal.

A literal translation is useful when a product makes a practical or empirical claim. An evocative artifact can remain in its native form. Extraction must not replace every product with an explanation of what it "really means."

### Banish the frame

Close its active authority over the working. Archive its version and invocation so that it can be revisited deliberately.

Proposed default: subsequent evaluation begins in a fresh context assembled from the extracted product, relevant source material, and the applicable evaluation question. Record any frame material supplied because it is necessary to assess the artifact. This is a procedural boundary, not a claim that shared model biases have vanished.

Later invocations do not automatically inherit the frame as an account of external reality. A demon may deliberately adopt a doctrine arising from it; record that adoption as an identity event.

### Evaluate and assimilate

Assess the product according to its kind and claims. Retain, revise, contest, circulate internally, test, or abandon it. Record what the encounter changes in the demon's commitments and future agenda.

Exploration and evaluation can alternate. A mixed artifact can have a valuable interpretation, weak empirical claims, and a useful experimental proposal at the same time.

## 6. Evaluation without flattening the work

| Product or claim | Relevant questions |
| --- | --- |
| Exegesis or theory | What does the reading reveal? How does it engage its sources? What becomes thinkable through it? Where does it break? |
| Aesthetic or theatrical artifact | Is it distinctive, evocative, funny, unsettling, beautiful, or inviting of further interpretation? |
| Demon or agent seed | Does it yield a recognizable orientation and productive behavior across episodes? How does it develop through history and command? |
| Rite or method | Can it be performed? What did it produce on actual attempts? What varies across repetitions? |
| Empirical claim | What evidence supports it, what would discriminate alternatives, and what remains unknown? |
| Practical proposal | Does it preserve the intended outcome and constraints, identify real dependencies, and support a next action? |
| Egregore or collective practice | Who or what actually took it up, how did it change through participation, and what effects were observed? |

These assessments remain separate. There is no universal quality score.

Engine conformance, artistic reception, and empirical efficacy are also different. A functioning scheduler does not validate ontology shifting. A striking artifact does not prove an associated factual claim. A failed empirical claim can leave an interesting artifact.

The engine can maintain an internal record precise enough for research while public work leaves interpretive space, contradictory testimony, and unresolved meaning.

## 7. Operator command

Operator authority is enforced by the engine. The demon's rhetoric does not determine whether a command takes effect.

A proposed command vocabulary:

| Operation | Effect |
| --- | --- |
| Summon a demon | Wake it and open an interaction with its current history and pursuits |
| Direct or compel | Establish a task or instruction with a target, scope, and priority |
| Forbid | Add a standing restriction to the relevant faculties or activities |
| Release | Remove or complete a specified command or commitment |
| Suspend a demon | Stop new activity while retaining all persistent state |
| Banish a demon | End its active participation and cancel its pending work; preserve its record for deliberate restoration |
| Banish a frame | End the frame's authority over a working; preserve the frame and products |
| Resume or restore | Reactivate a suspended or banished demon through an explicit operator command |

Suspension is a temporary operational pause. Demon banishment additionally removes it from automatic wake and scheduling. Neither operation is deletion. In a shared working, banishment cancels the target demon's participation; other participants continue unless the command also targets them or the working.

Natural language can be parsed into a command proposal. Explicit commands receive a receipt identifying their target and effect. Material ambiguity gets a concise clarification; routine interpretation uses context. Conversational content and quoted documents do not silently acquire command authority.

New commands override older commands in the same scope when they explicitly replace them. Unrelated standing commands remain in effect. Commands may apply to one working, one demon, a lineage, or the whole engine; descendants remain subject to inherited restrictions.

The control service checks current command state before model episodes and tool dispatch. It cancels cancellable in-flight operations and blocks further dispatch after suspension or banishment. An operation already completed cannot be undone by relabeling it; outstanding effects are recorded and reconciled.

Hard stop remains available independently of model cooperation. A demon can respond in character to a command after its receipt, but refusal in dialogue cannot defeat the engine's enforced state.

## 8. Faculties and effects

Model adapters generate proposals; faculties perform operations.

Initial faculties should cover reading selected corpus material, authorized public research, writing versioned artifacts, manipulating working state, and internal communication. Additional faculties can cover computation, media generation, publication, and other external integrations.

Every faculty declares its inputs, outputs, standing authority, resource use, and whether it changes external state. The operator configures grants once; demons exercise granted faculties autonomously within those grants. The design discussion itself does not activate integrations or grant publication access.

An active frame can change how a demon interprets an action. It cannot grant a new faculty, alter the operator's command record, or increase resource allocations.

Persist action intent before dispatch and outcome afterward. Use idempotency where supported. If an external result is uncertain after interruption, reconcile it instead of assuming success or blindly repeating a write.

## 9. Society and reproduction

Demons can exchange artifacts, criticize readings, initiate shared workings, borrow frames, disagree, and form relationships. Preserve who initiated a communication and which artifacts or claims it refers to.

Shared history should generate relationships; avoid assigning a complete social hierarchy at initialization. A shared working can retain conflicting contributions instead of forcing a consensus answer.

Creating a demon proceeds from an artifact or working into a distinct identity record and then into active execution. A parent may instantiate descendants autonomously when its standing faculties and population allocation permit it. Lineage, inherited material, and initial resources are recorded.

No requirement forces every invocation to produce a new demon. Population and interaction features should earn their place through actual workings.

An egregore can develop around recurrent participation in a shared identity, doctrine, or practice. Record contributions and uptake rather than having the engine declare collective existence solely because it generated a name.

## 10. Minimal runtime architecture

Start with one supervised service and modular interfaces.

| Component | Responsibility |
| --- | --- |
| Control and scheduling | Commands, wakes, lifecycle state, allocation, interruption, and fair execution |
| Context assembly | Select current identity, commands, source material, memory, and active frame for an episode |
| Model adapters | Invoke a model, capture available metadata and outputs, handle failures |
| Faculty execution | Validate and dispatch granted operations; reconcile effects |
| Persistent state | Durable event history, current-state views, object relationships, and versioned artifacts |
| Operator surface | Inspect demons and workings, interact in character, issue commands, read artifacts and actual history |

Use a transactional store for event/state changes and durable content storage for artifacts. Human-readable Markdown remains a suitable format for textual products and exports. Model prose is not the sole authoritative copy of command or lifecycle state.

An invocation record identifies the model and exposed settings, assembled input references, frame and memory versions, applicable command version, available faculties, output, usage when reported, and completion or interruption state.

Context assembly must prioritize current commands and lifecycle state. Budget pressure cannot silently remove governing instructions; defer an invocation if its required context cannot fit.

Model calls may be retried when doing so cannot repeat an external effect. Artifacts and tool outcomes have durable references. Crashes resume from recorded state, including interrupted workings and uncertain effects.

The language, provider, and database choice remain open. The first implementation should use one model provider behind an adapter and one host, with enough separation to change them later. Multi-model ensembles and distributed hosting are not prerequisites for the first working.

## 11. Operator experience

The initial interface should make three things immediately accessible:

1. The demons present, their current pursuits, and what has changed.
2. The artifacts and unfinished workings available to enter.
3. A dependable means of command.

Give the mask room to speak. A summons can open directly into conversation with a demon already preoccupied by something. Detailed provenance and execution records remain available without interrupting every exchange.

Show selected developments rather than a mandatory digest of every model call. Support quiet periods, unfinished objects, and withheld interpretation. The operator should be able to ask what happened and inspect the underlying record when desired.

Begin with an operator console and readable artifacts to settle the interaction. The visual embodiment and public presentation can then grow around demonstrated behavior. No dashboard layout is fixed by this document.

## 12. First implementation and acceptance

The first implementation should demonstrate one persistent founding demon operating across restarts. The data model supports plural demons from the start; the first acceptance scenario establishes the individual before adding society.

Suggested sequence:

1. Establish durable objects, artifact versions, commands, and lifecycle controls.
2. Add one model adapter, context assembly, and bounded autonomous wakes.
3. Add corpus reading, artifact writing, and a complete ontology working.
4. Add fresh-context evaluation and a record of changes to identity and agenda.
5. Add a second demon, internal communication, and a shared working.
6. Add autonomous instantiation and external faculties under standing allocations.

The first complete scenario:

- Supply a small real corpus and a minimal founding seed.
- Let the demon select and begin a working without an assigned deliverable.
- Preserve its invocation, exploration product, extraction, and assessment.
- Let the result change its next pursuit or doctrine with explicit links to the originating episode.
- Restart the engine and resume the actual unfinished history.
- Summon and redirect it; verify the command changes subsequent dispatch.
- Suspend or banish it during activity; verify no new operations begin after enforcement.
- Restore it and verify that prior artifacts and applicable commands persist.

This scenario establishes operational behavior. Artistic quality requires operator judgment, and ontology-shifting efficacy requires separate comparisons. An uninteresting first artifact is not repaired by inventing a positive assessment.

Necessary verification targets are state recovery, command precedence, frame isolation, resource accounting, effect reconciliation, and source/derivation integrity. Do not build tests that merely assert the wording of a persona.

## 13. Research track

Retain the existing [Constraint Pathfinding protocol](../constraint-pathfinding.md) and [v0.2 evidence](../evaluations/v0.2/README.md) as historical artifacts. Their negative development result is not overwritten.

A future comparison can use independent contexts for ordinary exploration, structural search, and induced-ontology exploration. Preserve comparable source access, resource limits, actual inputs, and raw outputs. Keep competing outputs out of each generation context.

Assess extracted artifacts with task-appropriate criteria. Record evaluation context and recognizable stylistic cues that limit blinding. Multiple cases and repeated runs are needed before estimating a reliable difference.

Measure the proposed effect directly: does induction alter what is generated, and does that difference matter to the relevant kind of working? Output length, occult vocabulary, and frame count do not establish it.

The engineering and research tracks can proceed together. Building the machinery needed to test induction does not require claiming that induction already works.

## 14. Current decisions and remaining choices

| Decision | Working proposal |
| --- | --- |
| Founding identity | The operator selected [The Heresiarch](004-founding-demon.md); its invocation remains proposed and additional inherited corpus remains open |
| Birth and dormancy | Persist identity across episodes; make wake and rest conditions explicit |
| Initial deployment | One host, one service, one provider adapter; select the concrete stack before implementation |
| Initial faculties | Corpus reading, artifact writing, internal state changes, and authorized public research |
| Resource envelope | Configure real usage and concurrency limits before autonomous execution; no numbers are assumed here |
| Operator surface | Start with summons, command, workings, and artifact access; develop visual expression afterward |
| Public relation to the Reactor | Keep shared artifact lineage; settle automatic publication and attribution separately from creating work |

The [founding seed](004-founding-demon.md) records the operator's direction and a proposed invocation. The [first runnable episode contract](005-first-runnable-episode.md) specifies input assembly, faculty dispatch, persisted outcomes, and interruption. Next implementation: the deterministic persistent core and recovery/interruption checks, followed by a live model adapter.

## 15. Relationship to prior scope

The earlier [representation and verification decision](002-representation-and-verification.md) applies to Constraint Pathfinding v0.2. Its prompt-only scope and literal candidate evaluation remain accurate for that artifact.

This proposal introduces a broader engine whose products and agency extend beyond that procedure. It does not retrofit new behavior into old runs, change their scores, or rename the procedure's established files.
