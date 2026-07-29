# Discovery (System A) — Architecture Information Flow

**Purpose:** Explain how information moves through System A (Discovery) — not how to implement it.  
**Package:** `ARCH-0.3-REPAIR` · **DUAL.2**  
**Normative status:** Narrative companion to frozen ART-A-00…A-07  
**Charter:** [ART-01D](../architecture_verifier/01-charter/CHARTER_DISCOVERY.md)  
**Canvas:** [discovery-information-flow](/Users/nicholasmino/.cursor/projects/Users-nicholasmino-Desktop-Research-Work/canvases/discovery-information-flow.canvas.tsx)

> **System A invents and packs; System B certifies.** Sole write into B = sealed CRP via `I.DiscoverySubmit` → `SUBMIT_CANDIDATE_PACKAGE`. Intake ≠ mathematical truth. Soft Attack ≠ B counterexample.

**Related guides:** [System B flow](../architecture_verifier/ARCHITECTURE_INFORMATION_FLOW.md) · [A↔B bridge](../architecture-visual/DISCOVERY_VERIFIER_INFORMATION_FLOW.md) · canvas `discovery-information-flow.canvas.tsx`

---

## 0. How to read this document

1. **Big picture** — one flowchart of the whole discovery session (sections labeled A–F).  
2. **Each section** — its own flowchart plus **IN / OUT / WHO / STORE**.  
3. Arrows mean *information or control*, not code calls.

| Symbol | Meaning |
|--------|---------|
| **IN** | What must exist before this section runs |
| **OUT** | What this section produces |
| **WHO** | Module or role that may write or veto |
| **STORE** | Where durable artifacts land |

**Hard rules (surface everywhere):**

| Rule | Meaning |
|------|---------|
| Orchestrator ≠ math | `DISCOVERY_ORCHESTRATOR` owns FSM/workflow only; never invents mathematics |
| Assistant seals | `RESEARCH_DISCOVERY_ASSISTANT` seals CRPs; does not own session FSM |
| Packager purity | `CRP_PACKAGER` is deterministic IR→CRP; invents nothing at pack time |
| Soft Attack ≠ CX | Soft Attack writes IR drafts only; never `RECORD_COUNTEREXAMPLE` |
| Intake ≠ truth | B intake creates authoritative intake record only; not certification |
| Parallel engines | Only inside `DiscoverySlice` between barriers (ART-A-03 I-A03-06) |
| Waivers | Session-scoped, gate-specific; never waive B `admissible_package` |

---

## 1. Big picture — labeled sections

```mermaid
flowchart TB
  subgraph A["A · Math problem scope (Area-1 chain)"]
    Lambda[Finite Λ + F_D] --> Pert[Q_ψ perturbation]
    Pert --> Sel[Selection / stability]
    Sel --> Comp[Composition]
    Comp --> Obj[Object / policy]
    Obj --> Inf[Inference via bridge]
  end

  subgraph B["B · Session lifecycle DS00→DS13"]
    DS00[DS00 Init] --> DS01[DS01 Scope]
    DS01 --> DS02[DS02 Frontier]
    DS02 --> DS03[DS03 Discovery]
    DS03 --> DS04[DS04 Gate1?]
    DS04 --> DS05[DS05 Refine]
    DS05 --> DS06[DS06 Gate2?]
    DS06 --> DS07[DS07 Portfolio]
    DS07 --> DS08[DS08 Draft compile]
    DS08 --> DS09[DS09 Gate3]
    DS09 --> DS10[DS10 Seal]
    DS10 --> DS11[DS11 Submit]
    DS11 --> DS12[DS12 Feedback]
    DS12 --> DS13[DS13 Close]
  end

  subgraph C["C · Discovery IR blackboard"]
    OrchC[DISCOVERY_ORCHESTRATOR<br/>FSM · gates · workflow]
    BB[Discovery IR<br/>session-local · non-authoritative]
    FS[FRONTIER_SCHEDULER]
    Store[DISCOVERY_IR store]
    OrchC --> BB
    FS <--> BB
    BB --> Store
  end

  subgraph D["D · Engines → Packager"]
    Eng[Specialist engines<br/>write IR only]
    Port[PORTFOLIO_MANAGER]
  end

  subgraph E["E · Human gates 1–3"]
    Hum[Human researcher]
    G1[Gate 1 scope]
    G2[Gate 2 novelty]
    G3[Gate 3 seal set]
    Hum <--> G1
    Hum <--> G2
    Hum <--> G3
  end

  subgraph F["F · Submit boundary"]
    Pack[CRP_PACKAGER]
    Draft[Unsealed DraftCRP]
    Seal[SealedCRPSnapshot]
    Submit[I.DiscoverySubmit]
    Bbox[System B black box]
    Receipt[IntakeReceipt / exports]
    Pack --> Draft
    Draft --> Seal
    Seal --> Submit
    Submit --> Bbox
    Bbox --> Receipt
    Receipt -.->|VerifierPrior read-only| BB
  end

  A -.->|constrains| B
  Eng --> BB
  Port --> BB
  BB --> Pack
  OrchC --> E
  E --> OrchC
  D --> F
  B --> C
```

**Section map**

| ID | Name | One-line job |
|----|------|----------------|
| **A** | Math problem scope | Same finite-candidate perturbation chain; A invents, does not certify |
| **B** | Session lifecycle | DS00→DS13 FSM: init → scope/frontier → discovery/refine → gates → portfolio → draft → seal → submit → feedback → close |
| **C** | Discovery IR | Session blackboard; engines write IR; Orchestrator owns FSM |
| **D** | Engines & portfolio | Specialist engines mint IR; Portfolio → Packager → DraftCRP |
| **E** | Human gates | Gates 1–3 review packets; session-scoped waivers |
| **F** | Submit boundary | Seal → `I.DiscoverySubmit` → sole B write; read-only priors back |

---

## 2. Section A — Mathematical problem scope

System A works within the same Area-1 scientific program as System B. Discovery **invents** candidates along this chain; it does **not** certify them.

```mermaid
flowchart LR
  IN_A[IN: finite Λ<br/>scores F_D λ<br/>neighbor relation<br/>mechanism Q_ψ] --> M1[Structured perturbation]
  M1 --> M2[Argmin / selection]
  M2 --> M3[Stability certificate]
  M3 --> M4[Composition rules]
  M4 --> M5[Selected object / policy]
  M5 --> M6[Inference claim<br/>typed bridge only]
  M6 --> OUT_A[OUT: IR artifacts<br/>conjectures · mechanisms · sketches<br/>non-authoritative w.r.t. B]
```

| | |
|--|--|
| **IN** | Finite candidate set Λ; scores \(F_D(\lambda)\); neighbor pin; mechanism \(Q_\psi\) with explicit data-dependence flag; human scope binding (Area-1) |
| **OUT** | Engine-owned IR: `OperatorAnalysis`, `ConjectureCandidate`, `MechanismProposal`, `ProofSketch`, `StructuralQuantity`, literature/novelty assessments — all session-local, non-authoritative |
| **WHO** | Specialist engines invent; Soft Attack proposes rewrites; Orchestrator schedules only; human gates on scope/objective shifts |
| **STORE** | Discovery IR (`ArtifactVersion` per class owner); **not** B `ResearchState` |
| **Must not** | Certify, promote, demote, mint authoritative CX, close proof obligations, write B ControlState |

---

## 3. Section B — Session lifecycle (DS00→DS13)

`DISCOVERY_ORCHESTRATOR` is the **sole** FSM control owner. Executing modules never advance the FSM.

```mermaid
stateDiagram-v2
  [*] --> DS00
  DS00 --> DS01: init
  DS01 --> DS02: scope bound
  DS02 --> DS03: frontier locked
  DS02 --> DS13: no_viable_frontier
  DS03 --> DS04: gate1_required
  DS03 --> DS05: not gate1
  DS04 --> DS05: approve/waive
  DS04 --> DS03: revise
  DS04 --> DS13: reject
  DS05 --> DS04: gate1_required
  DS05 --> DS06: gate2_and_not_gate1
  DS05 --> DS07: cleared
  DS05 --> DS13: no_viable_branch
  DS06 --> DS07: approve/waive
  DS06 --> DS05: revise
  DS06 --> DS13: reject
  DS07 --> DS08: portfolio built
  DS07 --> DS05: repair
  DS08 --> DS09: ≥1 DraftCRP
  DS08 --> DS05: all CompileError
  DS09 --> DS10: sealable_set
  DS09 --> DS07: revise portfolio
  DS09 --> DS05: revise discovery
  DS09 --> DS13: reject
  DS10 --> DS11: sealed
  DS11 --> DS12
  DS11 --> DS13: submit done
  DS12 --> DS13
  DS12 --> DS05: optional continue
  DS03 --> DS90: cancel
  DS13 --> [*]
  DS90 --> [*]
  DS91 --> [*]
```

### Phase IO cards

#### Init / scope / frontier (DS00–DS02)

| | |
|--|--|
| **IN** | Authorized open request; human Area-1 scope; ART-08b frontier candidates |
| **OUT** | `SessionRecord`, `ScopeBinding`, `FrontierState`, `QuestionLock`, `QuarantineRow` |
| **WHO** | Orchestrator (control); Frontier Scheduler executes frontier lock |
| **STORE** | Discovery IR + append-only `SessionEvent` log |

#### Discovery & refinement (DS03, DS05)

| | |
|--|--|
| **IN** | Locked question; IR snapshot at slice open (`input_snapshot_digest`) |
| **OUT** | Engine-owned IR versions; `DiscoverySlice` completion records; evaluated `gate1_required` / `gate2_required` |
| **WHO** | Orchestrator opens/closes slices; engines execute scheduled invocations only |
| **STORE** | Discovery IR; `SessionEvent` (slice payloads) |
| **Parallel rule** | Engines run in parallel **only** inside an open `DiscoverySlice`; barrier before FSM predicate evaluation |

#### Portfolio & draft (DS07–DS08)

| | |
|--|--|
| **IN** | Refined IR tips; Gate 1 cleared; Gate 2 cleared or skipped |
| **OUT** | `PortfolioFrontier`, `PortfolioMember`, `Branch`; per-member `DraftCRP` or `CompileError` |
| **WHO** | Portfolio Manager builds frontier; Packager compiles deterministically |
| **STORE** | Discovery IR (`Branch` via DISCOVERY_IR store) |
| **Ordering** | Portfolio → compile **all** Gate-3 candidates **before** Gate 3 (I-A02-11) |

#### Seal / submit / feedback / close (DS10–DS13)

| | |
|--|--|
| **IN** | Gate 3 `seal_set` of successful `DraftCRP.version_id`s |
| **OUT** | `SealedCRPSnapshot`; `SubmissionBatch` + `SubmissionAttempt`; optional `VerifierPrior`; `SessionClosed` with `close_reason` |
| **WHO** | Assistant seals and submits; Orchestrator ingests feedback as priors |
| **STORE** | Discovery IR; workflow records only in Orchestrator-owned classes |
| **Terminal** | DS13 orderly closure (any `close_reason`); DS90 cancel; DS91 infrastructure allowlist only |

---

## 4. Section C — Discovery IR blackboard + module ownership

```mermaid
flowchart TB
  subgraph Orch["DISCOVERY_ORCHESTRATOR owns"]
    SR[SessionRecord · ScopeBinding]
    GR[GateRecord · ScheduleEvent]
    SE[SessionEvent · SessionPolicy]
    SA[SubmissionAttempt · SubmissionBatch]
    VP[VerifierPrior · ConflictRecord]
    RP[RevisionProposal]
  end

  subgraph Store["DISCOVERY_IR store owns"]
    BR[Branch · DepLink]
    LC[ArtifactLifecycleRecord]
  end

  subgraph Engines["Engine-owned classes (write IR only)"]
    OA[OPERATOR_ANALYZER]
    NL[NOVELTY_LITERATURE]
    CE[CONJECTURE_ENGINE · ATP_ENGINE]
    SQ[STRUCTURAL_QUANTITY]
    MD[MECHANISM_DESIGNER]
    PS[PROOF_SKETCHER]
    SA2[SOFT_ATTACK]
    PM[PORTFOLIO_MANAGER]
    CP[CRP_PACKAGER]
  end

  subgraph Auth["RESEARCH_DISCOVERY_ASSISTANT owns"]
    DD[DefinitionDraft · AssumptionDraft]
    BP[BridgeProposalDraft · CertificateDraft]
    SCR[SealedCRPSnapshot]
  end

  subgraph Frontier["FRONTIER_SCHEDULER owns"]
    FS2[FrontierState · QuestionLock · QuarantineRow]
  end

  Orch -->|schedules · gates| Engines
  Engines -->|mint versions| IR[(Discovery IR blackboard)]
  Store -->|persist structure| IR
  Frontier --> IR
  Auth --> IR
  IR -->|read all modules| Engines
```

| | |
|--|--|
| **IN** | Mint requests from class owners; structural persistence requests; lifecycle transition authorizations |
| **OUT** | Durable session-local IR: immutable `ArtifactVersion` payloads + append-only lifecycle |
| **WHO** | Class owner mints versions; DISCOVERY_IR persists structure; Orchestrator mints workflow envelopes only |
| **STORE** | Session-local Discovery IR (never B authoritative state) |
| **Must not** | In-place `version_id` mutation; cross-session IR sharing (priors via explicit import only) |

**Ownership highlights**

| Artifact class | Owner |
|----------------|-------|
| Workflow (`SessionEvent`, `GateRecord`, `VerifierPrior`, …) | DISCOVERY_ORCHESTRATOR |
| Structure (`Branch`, `DepLink`, lifecycle) | DISCOVERY_IR |
| Frontier (`FrontierState`, `QuestionLock`) | FRONTIER_SCHEDULER |
| Math content (conjectures, mechanisms, sketches, …) | Respective engine or Assistant |
| `DraftCRP` / `CompileError` | CRP_PACKAGER |
| `SealedCRPSnapshot` | RESEARCH_DISCOVERY_ASSISTANT |

---

## 5. Section D — Engines & Portfolio → CRP_PACKAGER → DraftCRP

```mermaid
flowchart TB
  subgraph Slice["DiscoverySlice (parallel zone)"]
    OA2[OPERATOR_ANALYZER]
    NL2[NOVELTY + LITERATURE]
    CE2[CONJECTURE + ATP]
    SQ2[STRUCTURAL_QUANTITY]
    MD2[MECHANISM_DESIGNER]
    PS2[PROOF_SKETCHER]
    SA3[SOFT_ATTACK]
  end

  BB2[Discovery IR]
  Slice -->|mint IR only| BB2
  BB2 --> PM2[PORTFOLIO_MANAGER<br/>Pareto · no scalar collapse]
  PM2 -->|Branch + PortfolioMember| BB2
  PM2 --> Pack2[CRP_PACKAGER<br/>deterministic · no invention]
  Pack2 --> Draft2[DraftCRP]
  Pack2 --> Err2[CompileError]
  Draft2 --> G3[Gate 3 review]
  Err2 --> G3
```

| | |
|--|--|
| **IN** | Package-coherent `Branch` tip pins; closed acyclic `DepLink` closure; `profile_hint` per portfolio member |
| **OUT** | One `DraftCRP` or one `CompileError` per `compile(branch_id)`; portfolio metadata (novelty/survivability estimates — advisory only) |
| **WHO** | Engines invent math into owned classes; Portfolio Manager assembles distinct directions; Packager projects only |
| **STORE** | `PortfolioFrontier`, `PortfolioMember`, `DraftCRP`, `CompileError` in Discovery IR |
| **Must not** | Packager fill gaps; Portfolio invent mathematics; scalar ranking collapse |

**Projection map (Packager → CRP payload)**

| CRP field | IR source |
|-----------|-----------|
| `definitions[]` | `DefinitionDraft` |
| `assumptions[]` | `AssumptionDraft` |
| `claims[]` | `TheoremCandidate`, `ConjectureCandidate` |
| `proof_sketches[]` | `ProofSketch` |
| `mechanism_proposals[]` | `MechanismProposal` (if profile requires) |
| `falsifiers[]` | `FalsificationTarget`, `SoftFalsifierDraft` |
| `declared_reads[]` | `VerifierPrior` / library digests |

Missing required content ⇒ `CompileError`, not invention.

---

## 6. Section E — Human gates 1–3 + waivers

```mermaid
flowchart TB
  OrchE[DISCOVERY_ORCHESTRATOR] -->|review packet| HumE[Human researcher]
  HumE -->|approve / revise / reject / defer / waive| OrchE

  subgraph G1box["Gate 1 — scope / operator / objective"]
    G1E[GateRecord + ScopeBinding version]
  end

  subgraph G2box["Gate 2 — novelty quarantine"]
    G2E[GateRecord]
  end

  subgraph G3box["Gate 3 — seal set"]
    G3E[GateRecord.seal_set<br/>DraftCRP.version_id[]]
  end

  OrchE --> G1box
  OrchE --> G2box
  OrchE --> G3box
```

| Gate | Trigger | Human sees | On approve/waive |
|------|---------|------------|------------------|
| **1** | `gate1_required`: scope, operator class, or objective shift | Scope delta + operator analysis | New `ScopeBinding` version → DS05 |
| **2** | `gate2_required`: novelty quarantine | Novelty assessments + literature graph | → DS07 portfolio path |
| **3** | All Gate-3 candidates compiled | Portfolio metadata + all `DraftCRP`s + `CompileError`s | Explicit nonempty `seal_set` → DS10 |

| | |
|--|--|
| **IN** | `GateRequest` packet (digest of inputs; refs to scope, novelty, drafts, errors) |
| **OUT** | `GateRecord` with decision; Gate 3 adds `seal_set` when complete |
| **WHO** | Human decides; Orchestrator records and commits FSM transition |
| **STORE** | `GateRecord`, `SessionEvent`; optional `SessionPolicy` for deterministic Gate-3 waiver |
| **Waiver rule** | Session-scoped, gate-specific; **never** waives B `admissible_package`; Gate 3 waiver must resolve to explicit nonempty successful `DraftCRP` ids |

---

## 7. Section F — Submit boundary

```mermaid
flowchart LR
  SealF[SealedCRPSnapshot] --> SubmitF[I.DiscoverySubmit]
  SubmitF --> Cmd[SUBMIT_CANDIDATE_PACKAGE]
  Cmd --> BboxF[System B<br/>FROZEN black box]
  BboxF --> ReceiptF[IntakeReceipt]
  BboxF --> ExportF[I.LibraryExport / status]
  ReceiptF --> PriorF[VerifierPrior]
  ExportF --> PriorF
  PriorF -->|read-only into IR| IRF[Discovery IR]
```

| | |
|--|--|
| **IN** | `SealedCRPSnapshot` for each `DraftCRP.version_id` in Gate 3 `seal_set`; `SubmissionBatch` bound to `GateRecord` |
| **OUT** | B `IntakeReceipt` (authoritative intake only); read-only exports/status; A `VerifierPrior` citing `sealed_digest` and/or `receipt_ref` |
| **WHO** | Assistant executes `I.DiscoverySubmit`; Orchestrator mints `VerifierPrior` on authorized import |
| **STORE** | `SubmissionAttempt` (per-package idempotency); `VerifierPrior` in Discovery IR |
| **Sole B write** | `SUBMIT_CANDIDATE_PACKAGE` — no other B ResearchState/ControlState mutation |

**Batch / retry rules**

- One `SubmissionBatch` per Gate-3 seal wave.  
- Retry reuses `idempotency_key`; does not recreate Draft/Seal/Gate3.  
- Members already `ACCEPTED_DRAFT` are not resubmitted on partial retry.  
- Transport failure ≠ B intake rejection.  
- Material IR change ⇒ new draft → Gate 3 → seal → new logical submission.

**Late feedback**

- Open session: DS12 may mint active `VerifierPrior` with provenance.  
- Closed session (DS13): never reopens; late feedback seeds **new** session via authorized import.  
- Receipts are never certification/promotion authority.

---

## 8. Authority when things conflict

```text
Human gate decision
  → Charter (ART-01D)
  → Frozen ART-A-00…A-07
  → Package coherence predicates (P-A04-COH-*)
  → Portfolio advisory estimates (non-authoritative)
  → VerifierPrior (non-authoritative w.r.t. B math truth)
```

Orchestrator does not pick mathematical truth. Humans may force via `GateRecord`. Competing IR versions remain until explicitly abandoned or selected into a portfolio branch.

---

## 9. Relation

| Artifact | Role |
|----------|------|
| ART-A-00 | Overall architecture (primary diagram) |
| ART-A-02 | Module ownership & IR contracts |
| ART-A-03 | FSM states DS00–DS13, DS90/91 |
| ART-A-04 | Field schemas & predicates |
| ART-A-05 | DiscoverySlice invocation execution |
| ART-A-06 | Projection, seal, submit batch rules |
| ART-A-07 | Persistence & replay |
| ART-01D | Charter boundary |
| ART-CRP | CRP intake schema (read-only for A) |
