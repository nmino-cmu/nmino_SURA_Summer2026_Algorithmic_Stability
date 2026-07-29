# ART-A-02 — Internal Modules (System A)

**Artifact ID:** `ART-A-02`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-24` (Section 2 — Internal modules)  
**Consistency amendment:** `2026-07-24` — add `SessionEvent` (Orchestrator-owned workflow history; ART-A-03)  
**Consistency amendment:** `2026-07-25` — add `SubmissionAttempt`, `SessionPolicy` (Orchestrator-owned workflow; ART-A-03 Phase-1)  
**Consistency amendment:** `2026-07-25b` — add `SubmissionBatch` (Orchestrator-owned; multi-package Gate-3 submit identity)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/`  
**Depends on:** ART-A-00 (FROZEN) · ART-01D · ART-04e · ART-08b · ART-08c · ART-CRP (schema only)  
**Does not modify:** Verification Architecture (`architecture_verifier/`) · ART-A-00 except noted consistency

> **FREEZE:** Section 2 is frozen. Do not change ownership/contracts without an explicit unfreeze. Later sections must not contradict this document.
>
> Section 2 defines ownership and read/write/revision contracts. It does **not** redefine overall architecture (ART-A-00).

---

## 0. Normative principles

**I-A02-01 Single class owner.** Every IR artifact class has exactly one owning module. Only that owner may mint new **versions** of that class.

**I-A02-02 Append-only versions.** Artifact **content** is never overwritten in place. Evolution of content = new `version_id` under a stable `lineage_id`. Lifecycle transitions are separate append-only records (I-A02-10).

**I-A02-03 Non-owner revision path.** A non-owner that wishes to change another class requests a `RevisionProposal` (or Soft Attack emits `RewriteProposal`). The class owner may accept (mint new version citing the proposal), reject, or defer. Orchestrator schedules responses; it does not invent the mathematical content of the response.

**I-A02-04 No silent discard.** Competing alternatives remain as sibling versions and/or `ConflictRecord`s until explicitly abandoned or selected into a portfolio branch.

**I-A02-05 Orchestrator ≠ mathematics.** `DISCOVERY_ORCHESTRATOR` owns workflow artifacts only.

**I-A02-06 Packager purity.** `CRP_PACKAGER` is a deterministic compiler: one package-coherent IR branch (§1.3.1) → one unsealed `DraftCRP`. Missing content ⇒ compilation **error**, not invention.

**I-A02-07 Soft ≠ verifier CX.** Soft Attack outputs are IR drafts only. They are never B `RECORD_COUNTEREXAMPLE`, never authoritative in B, never obligation closure.

**I-A02-08 B boundary.** No module certifies, audits, promotes/demotes, closes proof obligations, or mutates B ResearchState/ControlState/IrreversibleSafetyLog. Sole write into B = sealed CRP via `I.DiscoverySubmit` → `SUBMIT_CANDIDATE_PACKAGE`.

**I-A02-09 Runtime ≠ role.** Architectural roles may share a process; contracts bind responsibilities, not deployment topology (ART-A-00).

**I-A02-10 Immutable payload vs lifecycle.** No content contributing to `version_id` may ever be modified. Lifecycle state (e.g. SUPERSEDED, ABANDONED, SELECTED, PACKED) lives only in append-only lifecycle records; transitions preserve replayability.

**I-A02-11 Gate-3 ordering (ART-A-00).** Portfolio → Packager compiles **all** Gate-3 candidates to unsealed `DraftCRP`s (or `CompileError`s) **before** Gate 3 → Gate 3 reviews metadata + drafts/errors → human selects subset → Assistant seals selected drafts only → submit.

**I-A02-12 B intake ≠ mathematical truth.** Discovery IR artifacts are System A work products. They are **non-authoritative with respect to System B**. Successful B intake creates an authoritative **B intake record** only. Mathematical correctness is **not** implied by intake.

---

## 1. Discovery IR

### 1.1 Purpose

Session-local blackboard storing all discovery artifacts, versions, lineage, branches, and references.

Discovery IR artifacts are mathematical (and workflow) work products **owned by System A**. They are **non-authoritative with respect to System B**. Successful `SUBMIT_CANDIDATE_PACKAGE` creates an authoritative B **intake** record (ART-CRP / IntakeReceipt) only; it does **not** certify mathematical correctness, close obligations, or promote claims.

### 1.2 Identity, payload, and lifecycle

**Immutable content identity:**

```text
ArtifactVersion
  lineage_id          # stable across versions
  version_id          # content-addressed; immutable once minted
  artifact_class      # from §1.4 taxonomy
  session_id
  owner_module        # class owner at mint time
  created_at
  parents[]           # prior version_ids and/or proposal refs
  payload             # IMMUTABLE — sole input to version_id digest
```

**Append-only lifecycle (does not enter `version_id`):**

```text
ArtifactLifecycleRecord
  lifecycle_record_id
  subject_kind          # ARTIFACT_VERSION | BRANCH | PROPOSAL | CONFLICT | …
  subject_id            # version_id | branch_id | proposal_id | …
  state                 # e.g. ACTIVE | SUPERSEDED | ABANDONED | SEALED_SNAPSHOT
                        # | OPEN | ACCEPTED | REJECTED | DEFERRED | WITHDRAWN
                        # | SELECTED | PACKED | CLOSED | RESOLVED_BY_BRANCH
  at
  cause_ref?            # schedule event, gate, accept, compile, …
  prev_lifecycle_record_id?
```

- **`lineage_id`:** immutable identifier for one evolving object (e.g. one conjecture family).
- **`version_id`:** digest of immutable `payload` (+ identity fields as defined by implementation). **No field that contributes to `version_id` may ever be modified.**
- **Supersession / abandon / select / pack:** expressed only by appending `ArtifactLifecycleRecord`s (and Branch lifecycle records). Prior content versions remain intact for replay.
- **`branch_ids` pins:** recorded as branch tip data / DepLinks / lifecycle association — not by mutating `ArtifactVersion.payload`.

### 1.3 Branch semantics

`Branch` is a **structural IR record** owned by `DISCOVERY_IR` (§1.4, §1.7). Semantic creation is **requested** by Portfolio Manager (portfolio branches) or Orchestrator (session scaffolding); DISCOVERY_IR persists and enforces integrity.

```text
Branch (immutable tip-set payload at mint; evolution = new branch version or new tip-pin record per store rules)
  branch_id
  session_id
  label                 # e.g. safe | balanced | ambitious | custom
  tip_pins[]            # version_ids — intended coherent set
  parent_branch_id?
```

Branch lifecycle states (`OPEN | SELECTED | PACKED | ABANDONED | CLOSED`, etc.) are **only** in lifecycle records (I-A02-10), never by rewriting tip-pin payload in place.

- A **portfolio member** references a `Branch` together with portfolio metadata (§6).
- Branches may share early lineage versions; divergence = different tip pins, not mutating shared `ArtifactVersion` payloads.
- Packager compiles **exactly one** `Branch` per compile attempt → one `DraftCRP` or one `CompileError`.

#### 1.3.1 Package coherence (normative)

A branch is **package-coherent** iff all of the following hold at compile time:

1. Every tip pin resolves to an existing `ArtifactVersion` in the session.  
2. Dependency closure over tip pins (via `DepLink`) is **complete** for all required compile inputs.  
3. The dependency graph is **acyclic**.  
4. No tip pin (nor required closure member) is in lifecycle state `ABANDONED`.  
5. No pair of simultaneously pinned artifacts is listed together in an `OPEN` `ConflictRecord` (or otherwise marked mutually exclusive for packaging).  
6. `DefinitionDraft` / `AssumptionDraft` references in the closure resolve consistently (no contradictory pins of the same lineage without an explicit conflict already excluding the branch).  
7. Required CRP payload fields for the member’s `profile_hint` can be projected from the closure **without invention** (ART-CRP profile rules; missing required content ⇒ not coherent).

Packager validation of package coherence is **deterministic**. Failure of any conjunct ⇒ `CompileError` (not repair-by-invention).

### 1.4 Artifact taxonomy (classes)

| Class | Owner module |
|-------|----------------|
| `SessionRecord` | DISCOVERY_ORCHESTRATOR |
| `ScopeBinding` | DISCOVERY_ORCHESTRATOR |
| `GateRecord` | DISCOVERY_ORCHESTRATOR |
| `ScheduleEvent` | DISCOVERY_ORCHESTRATOR |
| `SessionEvent` | DISCOVERY_ORCHESTRATOR |
| `SessionPolicy` | DISCOVERY_ORCHESTRATOR |
| `SubmissionAttempt` | DISCOVERY_ORCHESTRATOR |
| `SubmissionBatch` | DISCOVERY_ORCHESTRATOR |
| `VerifierPrior` | DISCOVERY_ORCHESTRATOR |
| `ConflictRecord` | DISCOVERY_ORCHESTRATOR |
| `RevisionProposal` | DISCOVERY_ORCHESTRATOR |
| `Branch` | DISCOVERY_IR |
| `DepLink` | DISCOVERY_IR |
| `ArtifactLifecycleRecord` | DISCOVERY_IR |
| `FrontierState` | FRONTIER_SCHEDULER |
| `QuestionLock` | FRONTIER_SCHEDULER |
| `QuarantineRow` | FRONTIER_SCHEDULER |
| `OperatorAnalysis` | OPERATOR_ANALYZER |
| `LiteratureNode` | NOVELTY_LITERATURE |
| `LiteratureEdge` | NOVELTY_LITERATURE |
| `NoveltyAssessment` | NOVELTY_LITERATURE |
| `ExampleCard` | CONJECTURE_ENGINE |
| `ConjectureCandidate` | CONJECTURE_ENGINE |
| `FalsificationTarget` | CONJECTURE_ENGINE |
| `TheoremCandidate` | ATP_ENGINE |
| `DefinitionDraft` | RESEARCH_DISCOVERY_ASSISTANT |
| `AssumptionDraft` | RESEARCH_DISCOVERY_ASSISTANT |
| `BridgeProposalDraft` | RESEARCH_DISCOVERY_ASSISTANT |
| `CertificateDraft` | RESEARCH_DISCOVERY_ASSISTANT |
| `StructuralQuantity` | STRUCTURAL_QUANTITY |
| `MechanismProposal` | MECHANISM_DESIGNER |
| `ProofSketch` | PROOF_SKETCHER |
| `SoftAttackLog` | SOFT_ATTACK |
| `SoftFalsifierDraft` | SOFT_ATTACK |
| `RewriteProposal` | SOFT_ATTACK |
| `PortfolioFrontier` | PORTFOLIO_MANAGER |
| `PortfolioMember` | PORTFOLIO_MANAGER |
| `DraftCRP` | CRP_PACKAGER |
| `CompileError` | CRP_PACKAGER |
| `SealedCRPSnapshot` | RESEARCH_DISCOVERY_ASSISTANT |

**No additional modules** beyond the required list plus the already-present `DISCOVERY_IR` store module. `RevisionProposal` is an Orchestrator-owned **workflow envelope**; `proposer_module` names who requested it. Soft Attack’s `RewriteProposal` remains Soft Attack–owned.

**`SessionEvent` (workflow history):** Orchestrator-owned, append-only FSM/session history records. Contain **no** mathematical content. Only `DISCOVERY_ORCHESTRATOR` may mint them. Used by ART-A-03 for replayable control history (may embed structured non-math control payloads such as discovery-slice schedules). `DiscoverySlice` is **not** a separate taxonomy class — it is a SessionEvent payload shape only.

**`SessionPolicy` (workflow):** Orchestrator-owned, append-only session-scoped deterministic policy documents (e.g. pre–Gate-3 waiver seal-set policy). Workflow-only; no mathematical content.

**`SubmissionAttempt` (workflow):** Orchestrator-owned, append-only records of sealed-CRP submission attempts (idempotency, transport, B intake). Workflow-only; no mathematical content.

**`SubmissionBatch` (workflow):** Orchestrator-owned identity for one Gate-3 authorized multi-package submit wave (seal_set → seals → attempts). Workflow-only; no mathematical content. Field schemas: ART-A-04; batch/partial semantics: ART-A-06; FSM timing: ART-A-03.

### 1.5 References & dependency links

`DepLink` is a **structural IR record** owned by `DISCOVERY_IR`. Semantic creation is requested by the module asserting the dependency; DISCOVERY_IR persists the link and enforces referential integrity.

```text
DepLink
  from_version_id
  to_version_id
  link_kind             # uses_def | assumes | cites_lit | attacks | revises
                        # | sketches | mechanism_for | quantity_for | compiles_to
```

Package coherence requires a closed, acyclic dependency set over tip pins (§1.3.1). Cycles ⇒ `CompileError`.

### 1.6 Sealed & temporary artifacts

| Kind | Rule |
|------|------|
| Ordinary IR versions | Session-local; readable by all A modules unless noted |
| `DraftCRP` | Unsealed; new compile = new `DraftCRP` version; not submittable |
| `CompileError` | Persistent packager output for a failed compile; shown at Gate 3; not submittable |
| `SealedCRPSnapshot` | Immutable submission snapshot; never mutated |
| `VerifierPrior` | Prior content derived from B read-only exports/receipts/status; Orch mints; engines read only |
| Ephemeral engine scratch | Not IR; must not be cited by Packager or Portfolio |

### 1.7 DISCOVERY_IR (store module)

**Purpose:** Provide the blackboard substrate (identity, versioning, structural records, indexes). Not a mathematical reasoner.

| Field | Contract |
|-------|----------|
| **Owns** | `Branch`, `DepLink`, `ArtifactLifecycleRecord`; store invariants; indexing; referential integrity |
| **Reads** | All persisted IR (integrity checks) |
| **Writes** | Persists `ArtifactVersion`s minted by class owners; persists structural records on request; appends lifecycle records on authorized transitions |
| **May Revise** | None of mathematical **payload**. Appends lifecycle / structural records only |
| **Must Not** | Invent mathematics; seal CRPs; call B mutation APIs; accept writes that violate class-owner rules; mutate `version_id` payload |
| **Outputs** | Durable IR state for the session |

Semantic creation requests:

- **Branch:** Portfolio Manager (portfolio members) or Orchestrator (scaffolding).  
- **DepLink:** Module asserting the dependency.  
- **ArtifactLifecycleRecord:** Class owner or Orchestrator/Packager/Assistant as appropriate to the transition (supersede, abandon, pack, select, seal association).

---

## 2. Revision model

### 2.1 Ownership

The **class owner** (taxonomy §1.4) owns all lineages of that class within a session. Structural classes `Branch`, `DepLink`, `ArtifactLifecycleRecord` are owned by `DISCOVERY_IR`.

### 2.2 Minting

Only the class owner creates a new `ArtifactVersion` / `version_id` for that class. Mint payload MUST include `parents[]` when superseding or accepting a proposal. Minting a superseding version is accompanied by an append-only lifecycle transition on the prior version (`SUPERSEDED`), not by editing prior payload.

### 2.3 RevisionProposal

```text
RevisionProposal (payload immutable once minted)
  proposal_id
  proposer_module
  target_class
  target_version_id?
  proposed_content_ref
  rationale
```

Lifecycle of the proposal (`OPEN | ACCEPTED | REJECTED | DEFERRED | WITHDRAWN`) is append-only via `ArtifactLifecycleRecord`.

- Any module may **request** a `RevisionProposal`; Orchestrator **mints** the envelope.
- Preferred pattern for alternatives within one class: class owner mints sibling versions directly.
- **Accept:** target class owner mints new version citing `proposal_id`; lifecycle records mark proposal `ACCEPTED` and prior version `SUPERSEDED` if replaced.
- **Reject / defer:** lifecycle closes proposal; competing content retained.

### 2.4 Soft Attack RewriteProposal

`RewriteProposal` is Soft Attack–owned. Acceptance path: **target class owner** mints the new mathematical version. Soft Attack never directly mints foreign math classes.

### 2.5 Competing revisions

Represented by:

1. Multiple sibling versions whose lifecycle still allows selection, and/or  
2. Multiple `OPEN` proposals, and/or  
3. A `ConflictRecord` linking incompatible `version_id`s.

Portfolio / Gate 3 selection chooses among package-coherent compiled candidates; non-selected versions remain unless abandoned via lifecycle.

### 2.6 Abandoned branches

Branch lifecycle → `ABANDONED` (and/or tip artifacts abandoned). Content retained for replay. Not eligible as Packager input (fails §1.3.1 conjunct 4).

---

## 3. Write policy

1. Class owner mints versions of owned classes only.  
2. Non-owners request `RevisionProposal`; Soft Attack mints `RewriteProposal`.  
3. No in-place overwrite of any field contributing to `version_id`.  
4. Lifecycle transitions are append-only (`ArtifactLifecycleRecord`).  
5. Orchestrator may mint only its workflow classes (§1.4).  
6. Packager mints only `DraftCRP` and `CompileError`.  
7. Assistant mints authorship classes + `SealedCRPSnapshot`; does not mint workflow classes.  
8. DISCOVERY_IR persists `Branch`, `DepLink`, lifecycle records on authorized request.

---

## 4. Read policy

| Artifact | Who may read |
|----------|----------------|
| All IR versions in session | All A modules (default **global readability**) |
| `VerifierPrior` | All A modules (non-authoritative w.r.t. B) |
| `DraftCRP` / `CompileError` | Orch, Assistant, Portfolio, Packager (Gate 3 review set) |
| `SealedCRPSnapshot` | Orch, Assistant (submit path); others read-only for lineage |
| Other session’s IR | **Forbidden** by default |
| B live ResearchState | Forbidden except via `I.LibraryExport` / status / receipts, ingested only as new-session `VerifierPrior` (§4.1) |

No restricted mathematical reads between engines. Orchestrator MUST NOT hide IR behind private memory (ART-A-00).

### 4.1 Cross-session verifier information

Sessions do **not** share IR directly. Later sessions receive verifier information only through:

1. **Explicit export/import** of B read-only artifacts / receipts, or  
2. **Explicit human-authorized transfer**,

after which the Orchestrator of the **receiving** session mints new `VerifierPrior` `ArtifactVersion`s for that session. The evolution sketch MUST NOT be read as ambient cross-session IR access.

---

## 5. Conflict resolution

### 5.1 Representation

`ConflictRecord` (Orchestrator-owned; payload immutable; status via lifecycle):

```text
ConflictRecord
  conflict_id
  kind                    # theorem_stmt | assumption | sketch | quantity
                          # | mechanism | operator | novelty_claim | mixed
  member_version_ids[]
  notes
```

### 5.2 Rules

- Engines discovering incompatibility SHOULD request a `ConflictRecord` rather than deleting rivals.  
- Soft Attack MAY request conflicts when attacks distinguish incompatible tips.  
- **Packaging resolution:** a branch that pins conflicting members fails package coherence (§1.3.1). Portfolio only advances package-coherent candidates (or surfaces `CompileError`). Lifecycle may mark a conflict `RESOLVED_BY_BRANCH` relative to a chosen branch without erasing alternatives.  
- Orchestrator does not pick mathematical truth; humans may force via `GateRecord`.

---

## 6. Portfolio contract

**PORTFOLIO_MANAGER** builds portfolio members over IR branches; invents no mathematics.

```text
PortfolioMember
  member_id
  branch_id
  draft_crp_version_id?     # set after successful pre–Gate-3 compile
  compile_error_id?         # set if pre–Gate-3 compile failed
  profile_hint
  novelty_estimate
  survivability_estimate
  confidence
  unresolved_risks[]
  primary_contribution
  expected_verifier_challenges[]
  tip_pins[]                # mirrors branch tips for review convenience
```

```text
PortfolioFrontier
  frontier_id
  members[]                 # Pareto set — not a scalar ranking
  dominated_member_ids[]    # retained, not silently dropped from IR
```

**Ordering (ART-A-00 / I-A02-11):**

1. Portfolio Manager builds `PortfolioMember`s (distinct directions; Pareto metadata; branch tips).  
2. Packager compiles **every** Gate-3 candidate member/branch **before** Gate 3 → `DraftCRP` or `CompileError`.  
3. Gate 3 review packet includes: portfolio metadata, corresponding `DraftCRP`s, and any `CompileError`s.  
4. Human selects any non-empty subset of members that have a successful `DraftCRP` (failed compiles are not sealable).  
5. Assistant seals **only** the selected `DraftCRP`s → `SealedCRPSnapshot`.  
6. Submit sealed snapshots only.

**Rules:**

1. Members MUST be meaningfully distinct directions (not cosmetic clones). **Predicate home:** ART-A-04 `P-A04-DISTINCT-01` / `P-A04-PARETO-01`.  
2. Mutually incompatible hypotheses live on **different** branches / members.  
3. No collapse to a single scalar score.  
4. Packager is invoked **per Gate-3 candidate before Gate 3**, not after human selection.  
5. Estimates are advisory portfolio metadata, not B novelty/audit verdicts.  
6. `dominated_member_ids[]` retains dominated alternatives; they are not silently deleted from IR.

---

## 7. Packager contract

1. Deterministic function `compile(branch_id) → DraftCRP | CompileError`.  
2. Introduces **no** new definitions, claims, mechanisms, sketches, quantities, or literature nodes.  
3. Compiles **one** branch per call → **one** `DraftCRP` or **one** `CompileError`.  
4. Runs for **all** Gate-3 candidates **before** Gate 3 (I-A02-11).  
5. Validates **package coherence** (§1.3.1); any failure ⇒ `CompileError`.  
6. Maps IR classes to CRP payload fields (ART-CRP §2) by fixed projection rules (later CRP-generation section); may omit optional empty fields; must not invent required ones.  
7. Output `DraftCRP` is always **unsealed**. `CompileError` is persistent for Gate 3 display; never sealed or submitted.  
8. Compilation failures remain failures; Orchestrator may reschedule owners to repair IR, then recompile (new `DraftCRP` / `CompileError` version). Packager never fills gaps.

---

## 8. Soft Attack contract

| Field | Contract |
|-------|----------|
| **Ownership** | `SoftAttackLog`, `SoftFalsifierDraft`, `RewriteProposal` |
| **Invocation** | Only via Orchestrator / session FSM schedule (ART-A-00) |
| **Outputs** | Attack logs; soft falsifier drafts; rewrite proposals; may request `ConflictRecord` |
| **Rewrite path** | Owner of target class accepts → new math version; Soft Attack does not mint foreign classes |
| **Must Not** | `RECORD_COUNTEREXAMPLE`; close obligations; certify; claim B audit/CX authority |
| **Distinction** | Soft results may later appear as CRP `falsifiers[]` / `counterexample_claims[]` **drafts**; B re-derives authority independently |

Playbook may include ART-12-aligned classes **and** A-only probes; results remain A-local until packaged as drafts.

---

## 9. Module contracts

---

### 9.1 DISCOVERY_ORCHESTRATOR

**Purpose:** Session lifecycle, scheduling, routing, gate management, workflow control.

| | |
|--|--|
| **Owns** | `SessionRecord`, `ScopeBinding`, `GateRecord`, `ScheduleEvent`, `SessionEvent`, `SessionPolicy`, `SubmissionAttempt`, `SubmissionBatch`, `VerifierPrior`, `ConflictRecord`, `RevisionProposal` |
| **Reads** | All IR (for scheduling); human gate decisions; B read-only exports/receipts/status (for prior minting) |
| **Writes** | Owned workflow classes only; mints `VerifierPrior` only after explicit export/import or human-authorized transfer into **this** session (§4.1) |
| **May Revise** | Own workflow lineages (new versions); requests lifecycle transitions |
| **Must Not** | Invent mathematics; mint math artifact classes; seal CRPs; mutate B state; hide priors off-IR; ambient cross-session IR read |
| **Outputs** | Session/gate/schedule/prior/conflict/proposal records; Gate 3 review packets (portfolio + drafts/errors) |

---

### 9.2 RESEARCH_DISCOVERY_ASSISTANT

**Purpose:** Mathematical authorship stewardship, CRP authorship metadata, sealing, immutable submission snapshots.

| | |
|--|--|
| **Owns** | `DefinitionDraft`, `AssumptionDraft`, `BridgeProposalDraft`, `CertificateDraft`, `SealedCRPSnapshot` |
| **Reads** | All IR; `DraftCRP`; `CompileError`; gate outcomes |
| **Writes** | Owned authorship classes; `SealedCRPSnapshot` **only** for Gate-3-selected successful `DraftCRP`s |
| **May Revise** | Own authorship lineages; accepts proposals targeting owned classes |
| **Must Not** | Own/control session FSM; submit unsealed CRPs; seal `CompileError`s; mutate sealed snapshots; mutate B; certify/promote |
| **Outputs** | Authorship drafts; sealed CRP snapshots for `I.DiscoverySubmit` |

---

### 9.3 FRONTIER_SCHEDULER

**Purpose:** A-local question selection and frontier ranking (ART-08b continuity).

| | |
|--|--|
| **Owns** | `FrontierState`, `QuestionLock`, `QuarantineRow` |
| **Reads** | Scope, priors, novelty assessments, soft-attack outcomes, portfolio outcomes, open conflicts |
| **Writes** | Owned frontier classes |
| **May Revise** | Own frontier lineages (mid-lock edits forbidden — terminate + re-lock) |
| **Must Not** | `LOCK_CYCLE` on B; write B quarantine/ResearchState; invent theorem bodies; seal CRPs |
| **Outputs** | Locked question + quarantine row |

---

### 9.4 OPERATOR_ANALYZER

**Purpose:** Analyze optimization/selection operators (argmax, top-k, sorting, thresholding, assignment, shortest path, MST, matching, LP, ILP, branch-and-bound, beam search, …).

| | |
|--|--|
| **Owns** | `OperatorAnalysis` |
| **Reads** | Scope, definitions/assumptions, quantities, mechanisms, priors, soft-attack rewrites targeting operators |
| **Writes** | `OperatorAnalysis` versions |
| **May Revise** | Own operator lineages; request `RevisionProposal` toward defs/assumptions/mechanisms/quantities |
| **Must Not** | Seal CRPs; certify stability; mint mechanisms as owned class; mutate B |
| **Outputs** | Operator decompositions, properties, failure modes, interface constraints |

---

### 9.5 NOVELTY_LITERATURE

**Purpose:** Structured prior-art graph and novelty assessment (extends ART-A-NOV + literature analyst).

| | |
|--|--|
| **Owns** | `LiteratureNode`, `LiteratureEdge`, `NoveltyAssessment` |
| **Reads** | Claims/conjectures/theorems, scope, priors, Gate 2 context |
| **Writes** | Literature graph + novelty assessments |
| **May Revise** | Own lit/novelty lineages; propose assumption/claim wording via `RevisionProposal` |
| **Must Not** | Issue B novelty-gate verdicts; certify; seal; treat lit notes as proved theorems |
| **Outputs** | Prior-art graph; novelty ladder notes; Gate 2 quarantine signals (via Orch) |

---

### 9.6 CONJECTURE_ENGINE

**Purpose:** Propose conjectures, minimal examples, and falsification targets (ART-A-CONJ).

| | |
|--|--|
| **Owns** | `ExampleCard`, `ConjectureCandidate`, `FalsificationTarget` |
| **Reads** | Frontier lock, operators, quantities, lit/novelty, soft attack, priors |
| **Writes** | Owned conjecture/example/falsification classes |
| **May Revise** | Own lineages; `RevisionProposal` to defs/assumptions |
| **Must Not** | Authoritative CX; close obligations; seal; mint `TheoremCandidate` (ATP) |
| **Outputs** | Example cards; conjectures; falsification targets |

---

### 9.7 ATP_ENGINE

**Purpose:** Automatic theorem/lemma/corollary **candidates** (ART-A-ATP). Not a verifier.

| | |
|--|--|
| **Owns** | `TheoremCandidate` |
| **Reads** | Defs, assumptions, conjectures, quantities, operators, mechanisms, sketches, soft attack, priors |
| **Writes** | `TheoremCandidate` versions |
| **May Revise** | Own theorem lineages; `RevisionProposal` to defs/assumptions/conjectures |
| **Must Not** | Assert proof floors / Lean status; close obligations; certify; seal |
| **Outputs** | Theorem/lemma candidate statements |

---

### 9.8 STRUCTURAL_QUANTITY

**Purpose:** Discover structural quantities (broad Area-1–relevant quantities per locked choice).

| | |
|--|--|
| **Owns** | `StructuralQuantity` |
| **Reads** | Operators, mechanisms, defs/assumptions, theorems/conjectures, soft attack |
| **Writes** | `StructuralQuantity` versions |
| **May Revise** | Own quantity lineages; proposals toward mechanisms/claims |
| **Must Not** | Certify utility/stability in B; seal; invent full mechanism schemas |
| **Outputs** | Quantity definitions, intended roles, estimation/sketch notes |

---

### 9.9 MECHANISM_DESIGNER

**Purpose:** Propose selection/perturbation mechanisms for CRP `mechanism_proposals[]` (ART-A-MECH).

| | |
|--|--|
| **Owns** | `MechanismProposal` |
| **Reads** | Operators, quantities, scope, Phase B/MIXED intent, soft attack, priors |
| **Writes** | `MechanismProposal` versions |
| **May Revise** | Own mechanism lineages; proposals to operators/quantities/assumptions |
| **Must Not** | Force mechanisms onto Phase A packages; certify mechanisms; seal; mutate B |
| **Outputs** | Mechanism schemas / \(Q_\psi\) drafts / domains |

---

### 9.10 PROOF_SKETCHER

**Purpose:** Produce non-authoritative proof sketches for candidate claims.

| | |
|--|--|
| **Owns** | `ProofSketch` |
| **Reads** | Theorem/conjecture candidates, defs, assumptions, quantities, mechanisms, soft attack |
| **Writes** | `ProofSketch` versions |
| **May Revise** | Own sketch lineages; `RevisionProposal` toward claims/assumptions when gaps appear |
| **Must Not** | Claim CERTIFIED/Lean success; close obligations; seal |
| **Outputs** | Proof sketches |

---

### 9.11 SOFT_ATTACK

**Purpose:** Research-grade non-authoritative attack search and rewrite signaling.

| | |
|--|--|
| **Owns** | `SoftAttackLog`, `SoftFalsifierDraft`, `RewriteProposal` |
| **Reads** | Branch tips under attack; operators; mechanisms; claims; assumptions; quantities; priors |
| **Writes** | Owned soft-attack classes; may request Orch `ConflictRecord` |
| **May Revise** | Own attack lineages; foreign classes only via `RewriteProposal` |
| **Must Not** | Authoritative CX mint; audit verdicts; obligation closure; seal; B mutation |
| **Outputs** | Logs, soft falsifiers, rewrite proposals |

---

### 9.12 PORTFOLIO_MANAGER

**Purpose:** Maintain novelty–survivability Pareto frontier; prepare Gate 3 candidate set.

| | |
|--|--|
| **Owns** | `PortfolioFrontier`, `PortfolioMember` |
| **Reads** | Branch tips, novelty assessments, soft-attack outcomes, `DraftCRP`, `CompileError`, conflicts |
| **Writes** | Portfolio frontier/members (advisory estimates only) |
| **May Revise** | Own portfolio lineages (recompute frontier versions) |
| **Must Not** | Invent math; scalar-collapse as sole decision object; seal; compile CRPs; reorder I-A02-11 |
| **Outputs** | Pareto frontier; requests Branch persistence; triggers pre–Gate-3 compile for each candidate |

---

### 9.13 CRP_PACKAGER

**Purpose:** Deterministic IR-branch → unsealed `DraftCRP` compiler (pre–Gate-3).

| | |
|--|--|
| **Owns** | `DraftCRP`, `CompileError` |
| **Reads** | Single `Branch` tip pins + `DepLink` closure; ART-CRP schema (read-only) |
| **Writes** | `DraftCRP` or `CompileError` versions only |
| **May Revise** | Own draft/error lineages (recompile = new version); never patches math IR |
| **Must Not** | Invent mathematics; seal; submit; coerce missing fields into existence |
| **Outputs** | Unsealed `DraftCRP` or persistent `CompileError` |

---

### 9.14 DISCOVERY_IR

See §1.7 (structural owner of `Branch`, `DepLink`, `ArtifactLifecycleRecord`).

---

## 10. End-to-end artifact evolution (normative sketch)

```text
ScopeBinding → Frontier QuestionLock
  → OperatorAnalysis / Literature+Novelty / Quantities
  → ExampleCard → ConjectureCandidate / TheoremCandidate
  → MechanismProposal (if Phase B/MIXED)
  → ProofSketch
  → SoftAttackLog (+ RewriteProposal → owner mints revised tips)
  → ConflictRecord? → Branch tip pins (DISCOVERY_IR)
  → PortfolioMember(s)                    # portfolio metadata + branches
  → DraftCRP | CompileError (per member)  # Packager BEFORE Gate 3
  → Gate 3 (review metadata + drafts/errors; select subset)
  → SealedCRPSnapshot (selected DraftCRPs only)
  → I.DiscoverySubmit
  → [later session] explicit export/import or human-authorized transfer
       → Orchestrator mints new VerifierPrior in THAT session
```

---

## 11. Consistency with ART-A-00

| ART-A-00 requirement | Section 2 handling |
|----------------------|--------------------|
| Orch does not invent math | Owns only workflow classes |
| Assistant seals; not FSM | Owns seal snapshot + authorship classes |
| Frontier first-class | Owns frontier classes; no B LOCK_CYCLE |
| Soft Attack FSM-invoked; IR drafts | Owns soft classes; rewrite via owners |
| Packager deterministic; no new math | §7 / §9.13 |
| B feedback → IR priors | `VerifierPrior` + §4.1 transfer rules |
| Pareto; no scalar collapse | Portfolio contract §6 |
| Portfolio → Pack → Gate 3 → seal | I-A02-11 / §6 / §7 / §10 |

**Consistency note (no ART-A-00 edit required):** Section 1 diagram aggregates “NOVELTY + LITERATURE” and “CONJECTURE + ATP”. Section 2 splits these into `NOVELTY_LITERATURE`, `CONJECTURE_ENGINE`, and `ATP_ENGINE`.

---

## 12. Internal architecture audit (post-repair)

| Check | Result |
|-------|--------|
| Ownership completeness | All taxonomy classes owned (§1.4), including `Branch`, `DepLink`, `ArtifactLifecycleRecord`, `CompileError` |
| Immutable payload semantics | I-A02-10; `ArtifactVersion.payload` vs `ArtifactLifecycleRecord` |
| Deterministic packaging | §1.3.1 + §7; failures → `CompileError` |
| Branch coherence defined | §1.3.1 package-coherent |
| Gate-3 / Packager order | I-A02-11 matches ART-A-00 |
| Section 1 compatibility | §11; ordering aligned |
| Verifier Architecture compatibility | I-A02-07/08/12; intake ≠ truth; no B mutation |
| Cross-session | §4.1; sketch corrected |
| Circular authority | Orch schedules; owners mint math; Packager compiles pre–Gate-3; Assistant seals selected drafts |
| Unchanged (per repair charter) | Module responsibilities, proposal model, ownership philosophy, append-only, Packager purity, Soft Attack, Portfolio philosophy, B boundary |

**Residual risk (later sections):** Exact CRP field projection tables; ART-04e roster documentation follow-on.

---

## Relation

- Overall: ART-A-00 (FROZEN)  
- Design companion: `docs/superpowers/specs/2026-07-24-discovery-assistant-design.md`  
- Extend-in-place engines: ART-A-NOV / ATP / MECH / CONJ (detailed behavior later; contracts here bind them)
