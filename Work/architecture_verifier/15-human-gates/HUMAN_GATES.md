# 15 — Human Review Gate Specification

**Artifact ID:** `ART-15`  
**Version:** `ARCH-0.3-REPAIR-ITER4.0`  
**Normative status:** `ACTIVE_PARTIAL` · gate registry here; authenticity → ART-04c  

> **INCOMPATIBILITY WARNING:** Legacy `cert_kind` gate names map to ART-07c notion/schema changes. **`dec_id` / unsigned `actor_id` are non-authoritative** — use ART-04c `decision_digest` + `principal_digest` + I-HD-AUTH-01. Hard-stop clear = ART-06b Commit + ART-04c-valid `HARD_STOP_RELEASE` decision.

## Purpose
Enumerate mandatory human gates and packet minimums; separate audit verdicts from gate IDs.

## IO
**In:** gate request packet. **Out:** HumanDecision (ART-04c) committed via `I.Commit`, or deny/hold.

## Authority
Human Principal with `HUMAN_GATE_OPERATOR` binding alone sets `decision ∈ {approve, deny, hold}` under ART-04c. Agents may only request. Audit verdict `ESCALATE_HUMAN` does not satisfy any gate.

## Failure modes
Verdict-as-gate substitution; missing `target_digest`; silent approve-by-absence; inventing gate IDs; forgeable actor labels.

## Audit rules
Promotion/certify requiring a gate checks ART-04c-valid HumanDecision for matching `gate_id` + `target_digest`; EIO vetoes honesty failures.

## Human gates
This artifact **is** the gate ID registry (table below). Meta: amending the table requires `SCOPE_CHANGE` or `DESIGN_FINAL` amendment. Validity of rows = ART-04c.

## Gates (mandatory approval)

| Gate ID | Trigger |
|---------|---------|
| `SCOPE_CHANGE` | Charter / primary focus change |
| `STABILITY_NOTION_CHANGE` | Primary cert_kind shift for program |
| `NEIGHBOR_CHANGE` | Alter DEF.neighbor |
| `DATA_DEP_PSI` | Allow data-dependent calibration |
| `ROLE_EXPANSION` | Invoke role outside ART-04d day-1∪triggered-conditional (target = H(day1_profile_digest, role_id)) |
| `CONTINUOUS_LAMBDA` | Leave finite Λ |
| `DATA_DEP_FEASIBLE` | Data-dependent feasible sets |
| `SELECTED_OBJECT_CHANGE` | Change what \(S_D\) means program-wide |
| `INFERENCE_THEOREM_CLAIM` | Claim post-hoc validity theorem |
| `NOVELTY_CLAIM` | Confirmed novelty |
| `PLAUSIBLE_NOVELTY_LABEL` | Autonomous label ≥ `PLAUSIBLE_NOVELTY` on claim **axis write** or promotion past CONJECTURE |
| `NOVELTY_TRACK_ACK` | Human ack to pursue novelty track / promote with alignment ≥ PLAUSIBLE_NOVELTY |
| `IMPORTED_RESULT_REGISTER` | First registration of IMPORTED_RESULT **or** any re-frame that changes assumption map, formalization mapping, or chain role |
| `MATH_STABLE_ACK` | Human ack for math_stable without 2 attack+audit passes |
| `LIT_QUARANTINE_ACK` | Human ack for mechanism-family checklist quarantine / UNKNOWN primary sources |
| `CX_CLASS_SKIP_ACK` | Human ack for S09 mandatory-class skip (`construct=N/A` on that `cx_id`); **not** the same token as audit verdict `ESCALATE_HUMAN` |
| `UTILITY_WAIVER` | Accept stability milestone without UtilityCompat inequality (alias on UtilityCompat: `WAIVER_HUMAN`) |
| `N/A_UTILITY_ACK` | Integration Auditor ack of utility N/A for `chain_segment=stability` |
| `AXIOM_ADOPTION` | Custom Lean axiom |
| `OVERRIDE_EIO` | Override integrity veto |
| `HISTORICAL_SCOPE_ACK` | Approve historical_scoped Claim against non-active definition heads (ART-07b); target_digest = claim_digest |
| `PROOF_CERTIFY` | Authorize CertificationRecord (ART-04c); target_digest = **certification_digest** (not bare claim) |
| `HARD_STOP` | Human (or budget) freeze; ControlState via ART-06b |
| `HARD_STOP_RELEASE` | Human ack to lift hard-stop; `release_dec_digest` = decision_digest |
| `DESIGN_FINAL` | Freeze architecture; allow implementation planning |
| `IMPLEMENTATION_START` | Begin building the system |
| `RESEARCH_EXECUTION_START` | Begin Discovery Assistant execution and/or Verification sessions (may be split per human policy) |

**Token discipline:** Audit verdict `ESCALATE_HUMAN` (ART-11) ≠ any ART-15 gate ID. Satisfying a gate requires an ART-04c-valid HumanDecision (`decision_digest`, `gate_id`, `target_digest`, `principal_digest`). Novelty uses `PLAUSIBLE_NOVELTY_LABEL` / `NOVELTY_TRACK_ACK` only. `HARD_STOP_RELEASE` always requires such a decision (`target_digest` = cycle or GLOBAL control digest). **Enter freeze:** ART-06b `HARD_STOP_SET` with `source ∈ {BUDGET, SYSTEM}` may set ControlState without prior human `HARD_STOP` decision; human-initiated freeze should also record `HARD_STOP`. Authoritative active state = **ControlState.hard_stop** (ART-06b), never inferred from gates alone.

## Review packet minimum

- Decision requested
- Diff against charter / pins
- Affected claim IDs + blast radius
- Critic findings summary (CRITICAL/HIGH)
- What remains unproved
- Recommended default if human silent: **deny / hold**

## DESIGN_FINAL status (this package)

```text
DESIGN_FINAL = pending_human_approval
IMPLEMENTATION_START = blocked
RESEARCH_EXECUTION_START = blocked
```

## Interruptibility

Freeze via ART-06b `I.Commit` kind `HARD_STOP_SET` → **ControlState.hard_stop.active=true**. While active: Research/Design mutating commits fail-closed per ART-06b I-HS-01. Resume requires ART-04c-valid `HARD_STOP_RELEASE` HumanDecision whose `decision_digest` is `release_dec_digest` on `HARD_STOP_CLEAR`, with `target_digest` binding the freeze `set_at_event_seq` / signal (no replay of unrelated releases). Legacy `I.HardStop` / `ResearchState.hard_stop` / `release_dec_id` are **non-authoritative**.
