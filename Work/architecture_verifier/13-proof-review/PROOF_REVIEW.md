# 13 — Proof Review Protocol

**Artifact ID:** `ART-13`  
**Version:** `ARCH-0.3`  
**Normative status:** `ACTIVE_PARTIAL`

> **INCOMPATIBILITY WARNING (Iter4/5):** `certifier_id ≠ proposer_id` string checks are **non-authoritative**. Use ART-04c Principals, PROOF_CERTIFIER RoleBinding, IndependenceAtom closure, and CertificationRecord. Axis raises: ART-13b `PromotionIntent` / `APPLY_PROMOTION` only — not this artifact’s prose.

## Purpose
Enforce proposer/certifier separation and review packets for major mathematical claims (INVARIANT #16).

## IO
**In:** claim + pins + proof object + attack summary. **Out:** certifier outcome enum; gap list; optional `REQUEST_CX`.

## Authority
Certifier may ACCEPT/REJECT/REQUEST_CX/ESCALATE; cannot be the Proposer instance for major claims. Integration Auditor/EIO do not substitute for Certifier on local algebra.

## Failure modes
Sole agent proposes and marks PROVED; rubber-stamp ACCEPT without packet; Certifier == Proposer; using Integration PASS as proof certification.

## Audit rules
Promotion to `PROVED_ON_PAPER`+ requires certifier outcome record with `certifier_id ≠ proposer_id`; packet fields present; EIO checks label integrity only.

## Human gates
`AXIOM_ADOPTION`; unresolved Certifier/Proposer dispute → human; inference-facing ACCEPT without bridge → `INFERENCE_THEOREM_CLAIM` path.

## Separation of roles

| Role | May |
|------|-----|
| Proof Proposer | Construct arguments; density-ratio; coupling; bounds; impossibility sketches |
| Proof Certifier | Independent check; must be different agent instance/role for major claims |
| Counterexample Attacker | Falsify; not certify |
| Integration Auditor | Chain fit; not certify local algebra |
| EIO | Provenance / label integrity; not mathematical correctness alone |

## Major claim threshold

Any claim intended `PROVED_ON_PAPER` or higher, or any bridge, or any inference-facing cert → **requires Certifier ≠ Proposer**.

## Review packet contents

- Claim statement + pins
- Assumption list
- Dependency closure
- Proof object / sketch with gap markers
- Attack log summary
- Known failure modes checked

## Certifier outcomes

`ACCEPT | ACCEPT_WITH_GAPS (→ PARTIAL) | REJECT | REQUEST_CX | ESCALATE`

## Banned

Sole agent proposes, “proves,” and marks PROVED without certifier.
