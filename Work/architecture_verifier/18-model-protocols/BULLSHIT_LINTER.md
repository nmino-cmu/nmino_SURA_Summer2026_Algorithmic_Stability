# Bullshit / Speculative-Output Linter Contract

**Artifact ID:** `ART-18b`  
**Version:** `ARCH-0.3`  
**Addresses:** ITER5 R-10

## Purpose

Detect contribution theater and speculative prose before commit/synthesis.

## Inputs

- Text under review (synthesis, reconciliation fields, cycle memos)
- Registry snapshot (claim IDs, lit IDs, audit IDs)
- Mode: `synthesis` | `reconciliation` | `memo`

## Predicates (any true → action)

| ID | Predicate |
|----|-----------|
| B1 | Theorem-shaped sentence without `claim_id` |
| B2 | Contribution lexicon (“we prove”, “novel mechanism”, “main result”) without novelty-track / literature axis consistent |
| B3 | Assertive citation without `lit_id` or with `verification_status=UNRESOLVED` |
| B4 | Claims/evidence ratio: assertive claim sentences / (claim_ids + cx_ids + audit_ids) > 5 in one synthesis |
| B5 | `PLAUSIBLE_NOVELTY` or higher in prose while claim axis ≤ ADAPTATION |

## Outputs

| Result | Action |
|--------|--------|
| CLEAN | Allow commit |
| QUARANTINE | Store as scratch; do not cite as institutional belief |
| BLOCK | Reject synthesis commit; force stagnation report |
| ESCALATE | Human packet |

## Authority

EIO or Integration Auditor may run; Orchestrator cannot mark CLEAN on its own prose without verifier pass for `synthesis` mode.

## Failure modes
False CLEAN on contribution theater; Orchestrator self-lint; ignoring BLOCK/ESCALATE.

## Audit rules
Synthesis commits require `I.BullshitLinter` result ≠ BLOCK; ESCALATE needs human packet.

## Human gates
Linter `ESCALATE` path; novelty-related B2/B5 → ART-15 novelty gates.
