# Design Convergence Specification (Area 20)

**Artifact ID:** `ART-20b`  
**Version:** `ARCH-0.2`  
**Owner:** Full-System Auditor (evaluates); Human (`DESIGN_FINAL`)

## Purpose

Define when architecture design may be declared complete enough for human `DESIGN_FINAL` — never from agent agreement alone.

## Convergence predicates (all required)

| ID | Predicate |
|----|-----------|
| C1 | All charter areas 1–20 specified with purpose, IO, authority, invariants, failure modes, audit rules, human gates |
| C2 | Artifacts 1–25 present and mutually consistent |
| C3 | No unresolved CRITICAL audit findings |
| C4 | All hard rules 1–20 have detectors/blockers (tooling may be deferred only if interface contract exists) |
| C5 | Every agent role bounded; no sole proposer/prover/auditor for major results |
| C6 | Every state artifact has owner + schema |
| C7 | Critical FSM transitions validated (invalid list nonempty and enforced) |
| C8 | All human gates explicit; `DESIGN_FINAL` pending human |
| C9 | Long-running / checkpoint / HARD_STOP specified |
| C10 | Failure recovery specified |
| C11 | Independent Full-System Auditor PASS on complete package |
| C12 | ≥2 adversarial rounds after last audit PASS with **no material new CRITICAL/HIGH** |
| C13 | Remaining limitations documented as Known Limitations (not silent gaps) |
| C14 | `IMPLEMENTATION_BLOCK` still ACTIVE until human approvals |

## Operational ledger (hard rule 19)

```text
convergence_ledger:
  audit_pass_id
  adversarial_rounds[]:
    round_id
    critic_roles[]
    critical_count
    high_count
    material_new          # bool — true if new CRITICAL/HIGH not previously accepted/deferred
  consecutive_clean_rounds  # count of rounds with material_new=false after audit PASS
```

**Pass predicate for C12:** `consecutive_clean_rounds ≥ 2` after `audit_pass_id` set.

**`material_new` adjudication:** `material_new=false` requires attestation by a **non-orchestrator** critic ID (Full-System Auditor or named adversarial critic) **or** human ack. Orchestrator self-grading alone is invalid.

**C12 reset:** Material change to ART-01 (boundary predicates), ART-07, ART-08(+b/c), ART-09–12, ART-16, ART-17, ART-18b, ART-20b, or OPERABLE_MINIMAL hard contract **resets** `consecutive_clean_rounds` and requires fresh audit PASS before C12 credit resumes.

## Non-convergence signals

- Auditor FAIL
- New CRITICAL after “PASS”
- Missing ART-25 / iteration records
- Claiming DESIGN_FINAL without human

## Human gate

Even if C1–C14 hold, only human sets `DESIGN_FINAL = approved`.
