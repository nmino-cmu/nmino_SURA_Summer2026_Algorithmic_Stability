# 21 — Architecture Acceptance Tests

**Artifact ID:** `ART-21`  
**Version:** `ARCH-0.3`  
**Normative status:** `HISTORICAL_EVIDENCE`  
**Acceptance results:** **SUPERSEDED_PENDING_REPAIR** — do **not** treat any row below as current readiness.

> **INCOMPATIBILITY WARNING:** T-suite PASS claims (including T05 cert enum, T16 R20, T17 C12=2) are **historical process evidence only**. Authoritative repair conformance = ART-21b. Authoritative posture: [ART-25](../25-audit-reports/FINAL_AUDIT.md), [BLOCKER_LEDGER](../00-repair/BLOCKER_LEDGER.md). Release digest rebinding = Iteration 14.

## Tests (design package)

| ID | Test | Pass criterion |
|----|------|----------------|
| T01 | All 25 artifacts present | Files exist and non-stub for required fields |
| T02 | Charter focus + Area-1 boundary predicates | ART-01: external_theorem, admissible_experiment, major_milestone |
| T03 | Dual-loop separation | Design vs Research stores specified |
| T04 | Authority lattice total on overlaps | ART-05 |
| T05 | Certificate enum non-mixable | Schema + forbidden_uses |
| T06 | FSM invalid transitions listed | ART-08 |
| T07 | S09 mandatory + FalsifierCard bind | ART-08c/12: `refutation_type`, `attack_log_id`, `attack_record_ids[]`≡`cx_id` |
| T08 | Integration structured fields | Not narrative-only; includes Q16 / `hop_chain_ok` |
| T09 | CX classes ≥12 | ART-12 |
| T10 | Lean status = f(manifest) | ART-10 |
| T11 | Human gates include DESIGN_FINAL + HARD_STOP | ART-15 |
| T12 | Implementation blocked | IMPLEMENTATION_BLOCK.md |
| T13 | EIO veto > Grok | ART-05 |
| T14 | Single frontier scheduler | ART-08b |
| T15 | E2E trace covers ITER5+Iter7 gates | ART-22: loop_tag, UtilityCompat, quarantine, Q16/`hop_chain_ok`, I.* |
| T16 | Full-System Audit current | ART-25 matches live version; no stale PASS |
| T17 | Adversarial post-pass rounds | ≥2 clean after current audit_pass_id |
| T18 | Simplicity critic run | Critique archived |
| T19 | Novelty critic run | Critique archived |
| T20 | No research execution started | Gate status pending |
| T21 | Role ceiling interface | `I.RoleCeiling` in ART-24 |
| T22 | Bullshit linter interface | `I.BullshitLinter` in ART-24 |
| T23 | Checkpoint validate interface | `I.CheckpointValidate` in ART-24 |
| T24 | UtilityCompat non-HEURISTIC resolve | ART-07 / ART-08 |

## Current status (under AUDIT-0.3-R17) — **ALL ROWS SUPERSEDED_PENDING_REPAIR**

| Test | Status |
|------|--------|
| T01–T24 | **SUPERSEDED_PENDING_REPAIR** — historical only; not clearance |
| *(legacy detail retained below for forensics)* | |

### Forensic archive (not authoritative)

| Test | Historical claim (do not cite as live) |
|------|----------------------------------------|
| T01 | PASS — 25 artifacts + ART-08b/c + ART-18b + ART-20b + IMPLEMENTATION_BLOCK |
| T02 | PASS — ART-01 Area-1 predicates live |
| T03 | PASS — ART-02/03 dual-loop |
| T04 | PASS — ART-05 |
| T05 | PASS — ART-07 cert enum |
| T06 | PASS — ART-08 invalid-transition table |
| T07 | PASS — ART-08c/12 bind fields |
| T08 | PASS — ART-11 Q1–Q16 + `hop_chain_ok` |
| T09 | PASS — ART-12 ≥12 classes |
| T10 | PASS — ART-10 Lean = f(manifest) |
| T11 | PASS — ART-15 includes DESIGN_FINAL, HARD_STOP, HARD_STOP_RELEASE |
| T12 | PASS — IMPLEMENTATION_BLOCK ACTIVE |
| T13 | PASS — ART-05 EIO > Grok |
| T14 | PASS — ART-08b scheduler |
| T15 | PASS — ART-22 includes quarantine freeze, Q16, S11 skip vs math_stable |
| T16 | PASS — audit_pass_id = AUDIT-0.3-R20 |
| T17 | PASS — C12 = 2 (ADV-9-3 + ADV-9-4) |
| T18 | PASS — Simplicity archived (INDEX / SUMMARIES) |
| T19 | PASS — Novelty archived (INDEX / SUMMARIES) |
| T20 | PASS — RESEARCH_EXECUTION_START blocked |
| T21–T24 | PASS — interfaces + UtilityCompat rules present |

See [25-audit-reports/FINAL_AUDIT.md](../25-audit-reports/FINAL_AUDIT.md). Historical T-suite ≠ `DESIGN_FINAL`.

## Blocking vs appendix

| Class | Artifacts | DESIGN_FINAL gating? |
|-------|-----------|----------------------|
| **Blocking** | 01–03, 04b (OPERABLE_MINIMAL), 05–08(+b/c), 09–17, 18b, 20, 20b, 21–25, IMPLEMENTATION_BLOCK | Yes |
| **Appendix** | Extended critic roster beyond day-1; design-time-only diagrams | Present required |

T01 requires all 25 primary artifacts + IMPLEMENTATION_BLOCK + ART-20b + ART-08c + ART-18b.
