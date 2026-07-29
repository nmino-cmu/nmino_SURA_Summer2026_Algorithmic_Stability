# General architecture (big picture)

**What this is:** A dual-system design — **A** invents and packs research; **B** verifies, attacks, certifies, and promotes — joined only by `CandidateResearchPackage`. Agents may propose; only authenticated **`I.Commit`** mutates B state.

**What it is not (yet):** A shipping product. Package is `NON-RELEASE`; implementation and research execution stay blocked until you approve human gates.

See also: [18-dual-system-separation](18-dual-system-separation.md).

---

## 1. One sentence

> Agents may **propose**; only authenticated **`I.Commit`** may mutate authoritative state; promotion requires intent + derived proofs + audit/cycle/provenance fences; humans hold the master gates.

---

## 2. System at a glance

```mermaid
flowchart TB
  subgraph Humans["Human gates"]
    HD["HumanDecision<br/>DESIGN_FINAL / HARD_STOP / …"]
  end

  subgraph DiscoveryA["System A — Discovery"]
    DO["Discovery Orchestrator"]
    FS["Frontier Scheduler"]
    ME["Mechanism / Novelty / ATP / Conjecture"]
  end

  subgraph VerifyB["System B — Verification"]
    VO["Verification Orchestrator"]
    PROP["Proof Proposer"]
    CERT["Proof Certifier"]
    AUD["Integration Auditor"]
    EIO["EIO"]
    LEAN["Lean Verifier"]
  end

  subgraph Boundary["Sole mutation boundary"]
    COMMIT["I.Commit"]
  end

  subgraph Stores["Authoritative stores"]
    CTRL["ControlState<br/>hard-stop, role ceiling"]
    RES["ResearchState<br/>claims, audits, CX, waves…"]
    DES["DesignState<br/>architecture package"]
    IR["IrreversibleSafetyLog<br/>receipts"]
    LOG["EventLog<br/>MutationEvents"]
  end

  subgraph Derived["Derived only — never caller booleans"]
    FLOOR["DerivedProofFloor"]
    PRE["ValidationPreimage APPLY"]
    CEIL["I.RoleCeiling"]
  end

  VerifyB -->|"Command + auth"| COMMIT
  DiscoveryA -->|"CRP only"| COMMIT
  HD -->|"RECORD_HUMAN_DECISION / CLEAR"| COMMIT
  COMMIT --> CTRL & RES & DES & IR & LOG
  RES --> FLOOR & PRE & CEIL
  PRE -->|"pass/fail"| COMMIT
```

---

## 3. Dual loop (design vs research)

```mermaid
flowchart LR
  subgraph Design["Design loop"]
    D1["Architecture artifacts"]
    D2["Critics / Sol gate"]
    D3["ReleaseManifest"]
    D1 --> D2 --> D3
  end

  subgraph Research["A invent → CRP → B verify"]
    R0["Discovery / Human"]
    R1["CandidateResearchPackage"]
    R2["Attack / audit / Lean"]
    R3["APPLY_PROMOTION"]
    R0 --> R1 --> R2 --> R3
  end

  D3 -.->|"DESIGN_FINAL<br/>human"| Block["IMPLEMENTATION_BLOCK"]
  Block -.->|"later"| Research
```

Design freezes *how the system works*. Research freezes *what claims are believed*. They share Commit discipline but different stores.

---

## 4. Claim lifecycle (happy path)

```mermaid
stateDiagram-v2
  [*] --> OPEN
  OPEN --> CONJECTURE: APPLY
  CONJECTURE --> PARTIAL_RESULT: APPLY + audit/cycle
  PARTIAL_RESULT --> RESULT: APPLY + CERTIFIED floor
  RESULT --> SUPERSEDED: FULL CX / demotion
  CONJECTURE --> SUPERSEDED: FULL CX
  PARTIAL_RESULT --> SUPERSEDED: FULL CX
  SUPERSEDED --> [*]
```

Maturity axis ≠ proof floor. You can be `RESULT` only if `DerivedProofFloor = CERTIFIED_INFORMAL`.

---

## 5. Promotion pipeline (major milestone)

```mermaid
sequenceDiagram
  participant O as Orchestrator
  participant C as I.Commit
  participant S as Stores
  participant D as Derived checks

  O->>C: APPLY_PROMOTION(intent)
  C->>D: recompute ValidationPreimage
  Note over D: floor, gates, audit_ok,<br/>cycle_ok, dd_ok, psi_ok,<br/>model_prov_ok, roles_invoked_ok,<br/>CX / demotion fences
  alt any fail
    D-->>C: REJECT reason_code
    C-->>O: REJECTED
  else all pass
    C->>S: upsert ResearchMaturityRecord
    C->>S: append MutationEvent (+ IR if needed)
    C-->>O: ACCEPTED
  end
```

---

## 6. Where authority lives (cheat sheet)

| Concern | Authoritative artifact |
|---------|------------------------|
| Objects / digests | ART-07b |
| Certs / bridges | ART-07c |
| Mutation / hard-stop | ART-06b |
| Identity / roles | ART-04c + ART-04d |
| Promotion | ART-13b |
| Audit | ART-11b |
| Provenance (DD/model) | ART-11c |
| Cycle bind | ART-08d |
| Lean | ART-10b |
| Demotion | ART-16b |
| Checkpoint | ART-17b |
| Conformance H/canon | ART-21b |
| Release identity | ART-25b |

Appendix / descriptive files (old FSMs, ART-04b profile prose, ART-21 historical T-suite) are **not** authority when an ACTIVE_NORMATIVE `*b/*c/*d` binding exists.

---

## 7. Human gates that matter now

```mermaid
flowchart TD
  A["Package Sol gate PASS ✓"] --> B["Seal ReleaseManifest<br/>→ release_digest"]
  B --> C{"You: DESIGN_FINAL<br/>target = release_digest?"}
  C -->|approve| D["Blueprint / planning may proceed"]
  C -->|deny / hold| E["Stay NON-RELEASE"]
  D --> F{"IMPLEMENTATION_START"}
  F --> G{"RESEARCH_EXECUTION_START"}
```

---

## Next

Browse [README.md](README.md) section docs for zoomed-in charts.
