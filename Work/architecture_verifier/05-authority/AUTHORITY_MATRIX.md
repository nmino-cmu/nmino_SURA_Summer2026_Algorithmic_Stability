# 05 — Authority and Escalation Matrix

**Artifact ID:** `ART-05`  
**Version:** `ARCH-0.3`  
**Normative status:** `ACTIVE_PARTIAL` · lattice order here; Human Decision authenticity → ART-04c

> **INCOMPATIBILITY WARNING (Iter4/6/8):** “New `cert_kind`” → ART-07c. Lattice item 1 = ART-04c HD only. Lattice item 4 Lean = ART-10b DerivedLeanStatus/manifest only — legacy ART-10 non-authoritative. Lattice item 6 = ART-11b bound PASS only.

## Purpose
Total conflict-resolution lattice and escalation paths across overlapping authorities.

## IO
**In:** conflicting decisions / vetoes. **Out:** resolution record per lattice order.

## Authority
Lattice below is total on overlaps. EIO veto > Grok on integrity. Human scoped decisions top.

## Failure modes
Grok overriding EIO; ignoring lattice; unscoped human override without blast radius.

## Audit rules
Resolution records required when authorities disagree; EIO standing veto logged.

## Human gates
`OVERRIDE_EIO`, `HARD_STOP`, all ART-15 gates as triggered.

## Authority lattice (conflict resolution order)

1. Human Decision (scoped, typed, with expiry)
2. Immutable Charter (`ART-01`)
3. Pinned Definition (`ART-02`)
4. Lean Manifest at pin (`ART-10b` DerivedLeanStatus; legacy `ART-10` non-authoritative)
5. Counterexample at pin (`ART-12`)
6. Integration Audit PASS (`ART-11b` bound AuditRecord; legacy `ART-11` non-authoritative)
7. Literature claim with primary-source attachment
8. Mechanism sketch / heuristic
9. Frontier priority

Every resolution emits `resolution_record{winner, loser_ids[], rule, actor_principal_digest, event_seq}`.

## Write / veto matrix

| Action | Grok | Critic/Specialist | Integration Auditor | EIO | Lean Verifier | Human |
|--------|------|-------------------|---------------------|-----|---------------|-------|
| Propose state write | Yes | No | No | No | No | Yes |
| Edit critic reports of others | No | No | No | No | No | Yes |
| PASS/FAIL integration | No | No | Yes | No | No | Override |
| Veto promotion | No | No | Block via FAIL | **Yes** | Block via manifest | Yes |
| Set LEAN_* label | No | No | No | No | **Manifest only** | Force demote |
| Change scope / cert kind | No | No | No | No | No | **Only** |
| Claim novelty | No | No | No | No | No | **Only** |
| DESIGN_FINAL | No | No | No | No | No | **Only** |
| Start implementation | No | No | No | No | No | **Only** |

## Escalation triggers → human packet

- Scope drift detector / charter semantic distance
- New `cert_kind` or neighbor relation
- Data-dependent \(\psi\)
- Continuous \(\Lambda\) or data-dependent feasible sets
- Inference theorem claim
- Novelty above “adaptation”
- Custom Lean axiom
- Unresolved contradiction age > threshold
- `LEAN_BLOCKED` beyond SLA cycles
- EIO vs Grok disagreement

## EIO vs Grok

EIO **blocks promotions**. Grok may escalate to human; Grok **cannot** override EIO without human `OVERRIDE_EIO` decision.
