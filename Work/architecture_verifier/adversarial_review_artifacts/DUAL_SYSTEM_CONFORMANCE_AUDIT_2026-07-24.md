# Dual-System Separation — Implementation Conformance Audit

**Document ID:** `AUDIT-DUAL-CONFORM-2026-07-24`  
**Date:** 2026-07-24  
**Scope:** Implemented architecture docs only (`architecture/`, `architecture-discovery/`, `architecture-visual/`)  
**Method:** Evidence inspection against required separation; no redesign  
**Verdict:** **REFACTOR PARTIALLY COMPLETE**

Score: **7 PASS · 4 PARTIAL · 1 FAIL**

---

## Checks

### 1. Verification Architecture formally rechartered as verification-only

- **STATUS:** PASS
- **EVIDENCE:** `architecture/01-charter/CHARTER_VERIFICATION.md` (ART-01V, `ACTIVE_NORMATIVE`) — mission “verify, certify, govern, and persist”; non-goals include inventing questions, frontier scoring, autonomous discovery. `architecture/01-charter/CHARTER.md` (ART-01 DUAL.1) system split table. `architecture/00-repair/ARTIFACT_STATUS.md` lists ART-01V.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 2. Research Discovery Assistant as separate upstream system

- **STATUS:** PASS
- **EVIDENCE:** `architecture/01-charter/CHARTER_DISCOVERY.md` (ART-01D); `architecture/04-agents/OPERABLE_DISCOVERY.md` (ART-04e); `architecture-discovery/README.md` ownership of ART-08/08b/08c; `architecture/03-context/SYSTEM_CONTEXT.md` A→CRP→B diagram.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 3. Discovery capabilities preserved but moved outside verifier

- **STATUS:** PARTIAL
- **EVIDENCE:**
  - Question Selection / Frontier Scoring: `architecture-discovery/08-research-cycle/QUESTION_SELECTION.md` (ART-08b, `OWNED_BY_DISCOVERY`)
  - Autonomous Research Cycle: `architecture-discovery/08-research-cycle/RESEARCH_CYCLE_FSM.md` (ART-08)
  - Mechanism Designer / Novelty Engine / Discovery Orchestrator / Conjecture Proposer: rostered in ART-04e
  - Mechanism Proposal: `architecture/24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md` `mechanism_proposals[]`
  - B stubs point to discovery home under `architecture/08-research-cycle/`
- **DEFECT:** Novelty Engine is roster-only (no owned module). **Automatic Theorem Proposal** has zero repository matches. Mechanism Designer / conjecture generation lack dedicated owned artifacts beyond roster + FSM stages.
- **REQUIRED FIX:** Add owned A artifacts (or explicit annex ownership) for Novelty Engine and Automatic Theorem Proposal; do not claim preservation from roster labels alone.

### 4. Discovery components do not participate in verification decisions / obligation closure / certification / promotion / demotion / audit verdicts

- **STATUS:** PARTIAL
- **EVIDENCE:** ART-04c: `FRONTIER_SCHEDULER` does not `LOCK_CYCLE` on B. ART-04d / ART-08d: `LOCK_CYCLE` requires `VERIFICATION_ORCHESTRATOR`. ART-01D / ART-04e I-OD-02 forbid APPLY / authoritative CX / ResearchState upserts. No `FRONTIER_SCHEDULER` / `MECHANISM_DESIGNER` in ART-06b / 11b / 13b / 16b command authorship.
- **DEFECT:** Legacy `RESEARCH_ORCHESTRATOR` still named as command author in ART-08d cycle cmds, ART-11b `RECORD_DISCONFIRM`, ART-13b promotion route, ART-16b demotion starts (alias to B orchestrator, not rename). Companion docs still show Frontier→`LOCK_CYCLE` (`architecture-visual/07-research-cycle.md`, `AGENT_ROLES.md`).
- **REQUIRED FIX:** Replace B-facing `RESEARCH_ORCHESTRATOR` author labels with `VERIFICATION_ORCHESTRATOR`; scrub stale companion docs.

### 5. First-class CandidateResearchPackage

- **STATUS:** PARTIAL
- **EVIDENCE:** `architecture/24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md` (ART-CRP, `ACTIVE_NORMATIVE`); ART-ASI entry; ART-06b command kinds `SUBMIT_CANDIDATE_PACKAGE` / `REJECT_CANDIDATE_PACKAGE`; ART-24 contracts; fixtures `CF-CRP-A/B/C`.
- **DEFECT:** ART-CRP consumer delta claims ART-07b “CRP stub”; `CANONICAL_OBJECTS.md` contains no `CandidateResearchPackage` / `crp_digest` / `IntakeReceipt`.
- **REQUIRED FIX:** Register CRP + IntakeReceipt in ART-07b, or retract the stub claim.

### 6. CRP principals HUMAN and RESEARCH_DISCOVERY_ASSISTANT

- **STATUS:** PASS
- **EVIDENCE:** ART-CRP `author_kind` enum and `admissible_package` auth; ART-04c role table; fixture `CF-CRP-C` → `CRP_AUTHOR`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 7. Characterization-only work without MechanismInstance / perturbation law / Q_ψ / stability certificate / inference bridge

- **STATUS:** PASS
- **EVIDENCE:** ART-CRP I-CRP-02; ART-07b `characterization` segment (“no MechanismInstance required”); ART-01 characterization milestone; `CF-CRP-A` Phase A empty mechanisms → `SUCCESS`.
- **DEFECT:** Discovery-side ART-08c ExampleCard still requires `perturbation_mechanism_id` (A packaging friction; not B intake rejection).
- **REQUIRED FIX:** Optional — relax `architecture-discovery/.../EXPERIMENT_PROTOCOL.md` for Phase A.

### 8. Complete external intake pipeline

- **STATUS:** PARTIAL
- **EVIDENCE:** CRP → `admissible_package` (ART-CRP) → Commit `SUBMIT_CANDIDATE_PACKAGE` (ART-06b) → canon (ART-21b) → typed objects/deps (ART-07b/07c) → CX (ART-16b / I-CX) → audit (ART-11b) → promotion/demotion (ART-13b/16b). I-CRP-10: post-intake uses existing B commands only.
- **DEFECT:** “Proof-obligation generation” appears in plan mermaid only — no `ProofObligation` object/command in ART-07b/06b. `LOCK_CYCLE` after intake is SHOULD (I-CRP-20), not a hard gate.
- **REQUIRED FIX:** Normatively identify obligation generation with existing ART-07b dependency/CX/bridge slots, or add the missing normative binding.

### 9. Phase A characterization claim types first-class

- **STATUS:** PASS
- **EVIDENCE:** ART-07b `chain_segment=characterization`; ART-01 `characterization_facing` / major_milestone clause; ART-CRP `PHASE_A_CHARACTERIZATION` profile + admissibility rules.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 10. CX, audit, and integration profiles for characterization-only packages

- **STATUS:** FAIL
- **EVIDENCE:** Zero `characterization` / `PHASE_A` matches under `architecture/11-integration-audit/` and `architecture/12-counterexample/`. Only generic ART-11b / ART-12 machinery.
- **DEFECT:** ART-11b Q04 is `ALWAYS` (“Perturbation DD-independent…”) and Q17 requires advancing the main chain — misfit for characterization-only packages. No characterization CX class set or integration profile.
- **REQUIRED FIX:** Add applicability modes for `chain_segment=characterization` (e.g. Q04 NA; Q17 characterization-facing) and a characterization CX/integration profile.

### 11. Existing verification infrastructure preserved

- **STATUS:** PASS
- **EVIDENCE:** ART-ASI `ACTIVE_NORMATIVE`: ART-06b, 07b, 07c, 08d, 10b, 11b, 13b, 16b — files present; Commit, typed claims, assumptions, certificates, bridges, deps, CX, Lean, promotion/demotion, audit trail intact.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 12. No mandatory discovery cycle required to begin verification

- **STATUS:** PASS
- **EVIDENCE:** Human may `SUBMIT_CANDIDATE_PACKAGE` (ART-04c / ART-CRP TRACE-CRP-D). No normative rule requires completing System A ART-08 FSM before B intake. I-CRP-20 is a legacy cycle shim, not an A mandate.
- **DEFECT:** —
- **REQUIRED FIX:** —

---

## A. Dependency-boundary audit

### Allowed

| Edge | Interface | Authority |
|------|-----------|-----------|
| A\|Human → B | `SUBMIT_CANDIDATE_PACKAGE` (`I.DiscoverySubmit` alias only) | ART-CRP, ART-24, ART-01D |
| A → B | `I.DiscoveryStatus` (read-only) | ART-04e |
| B → A | `I.LibraryExport` (read-only certified digests) | ART-04e, ART-01V |
| Shared | Area-1 pins, ART-07 schemas, ART-15 gate IDs | ART-01, ART-07b/c |

### Forbidden

| Edge | Forbidden | Authority |
|------|-----------|-----------|
| A → B | `APPLY_PROMOTION`, `ATTACH_CERTIFICATION` | ART-01D, I-CRP-10 |
| A → B | Authoritative `RECORD_COUNTEREXAMPLE`, demotion waves | ART-01D, ART-04e I-OD-02 |
| A → B | Direct ResearchState / ControlState / Irreversible upsert | ART-01D, ART-06b |
| A → B | `FRONTIER_SCHEDULER` → `LOCK_CYCLE` | ART-04c, ART-08d, ART-04d |
| B → A | Frontier score / pick-next / Mechanism Designer internals as Commit inputs | ART-01V non-goals |

---

## B. Characterization-only E2E trace

1. Author seals CRP: `profile=PHASE_A_CHARACTERIZATION`, `claims[].chain_segment=characterization`, `mechanism_proposals=[]` (ART-CRP).
2. B `SUBMIT_CANDIDATE_PACKAGE` → `admissible_package` + I-CRP-02 → `IntakeReceipt` `ACCEPTED_DRAFT` (locked by `CF-CRP-A` → `SUCCESS`).
3. ART-21b canonicalize; ART-07b mint draft characterization Claim(s).
4. Optional ART-08d `LOCK_CYCLE` (`VERIFICATION_ORCHESTRATOR`); then existing CX / audit / APPLY commands (I-CRP-10).

| Outcome | Path |
|---------|------|
| **certified** | ART-13b `APPLY_PROMOTION` after audit PASS + floors |
| **revision required** | Audit FAIL / incomplete evidence → new CRP |
| **rejected** | `REJECT_CANDIDATE_PACKAGE` / `PACKAGE_INADMISSIBLE` / `CRP_AUTHOR` |

**Implemented caveat:** Until check 10 is fixed, characterization packages often cannot honestly reach audit PASS under ART-11b Q04/Q17 as written.

---

## C. Stabilization-mechanism regression

CRP `profile=PHASE_B_STABILIZATION` with nonempty `mechanism_proposals[]` → I-CRP-05 → intake → unchanged ART-07b I-CERT-01 / selection_stability / ART-16b / ART-11b / ART-13b path. Negative lock: `CF-CRP-B` → `MECHANISM_REQUIRED`. B kernel artifacts remain `ACTIVE_NORMATIVE`.

---

## D. Stale “verifier = autonomous research system” residues

| Location | Stale content |
|----------|---------------|
| `architecture/00-README.md` | Title “Autonomous Theoretical-Research System” |
| `architecture/IMPLEMENTATION_BLOCK.md` | “autonomous research system” / “Autonomous mathematical research cycles” |
| `architecture/ARCHITECTURE_INFORMATION_FLOW.md` | §C Research Orchestrator → S00–S16; Frontier commits S02 |
| `architecture/04-agents/AGENT_ROLES.md` | Unified research-time roster; Frontier owns S02 quarantine |
| `architecture/04-agents/OPERABLE_MINIMAL_PROFILE.md` | Day-1 Research Orchestrator + Frontier for S02 |
| `architecture/15-human-gates/HUMAN_GATES.md` | `RESEARCH_EXECUTION_START` = Begin autonomous research cycles |
| `architecture/16-failure-recovery/FAILURE_RECOVERY.md` | Owner: Research Orchestrator |
| `architecture-visual/00-GENERAL.md` | §2 single roster (Research Orchestrator + Frontier) |
| `architecture-visual/03-agents-identity.md` | Day-1 RESEARCH_ORCHESTRATOR + FRONTIER together |
| `architecture-visual/07-research-cycle.md` | `FRONTIER_SCHEDULER` → `LOCK_CYCLE` |
| ART-08d / 11b / 13b / 16b | Command authors still say `RESEARCH_ORCHESTRATOR` |
| `architecture-discovery/.../EXPERIMENT_PROTOCOL.md` | ExampleCard requires `perturbation_mechanism_id` |

---

## Final verdict

**REFACTOR PARTIALLY COMPLETE**
