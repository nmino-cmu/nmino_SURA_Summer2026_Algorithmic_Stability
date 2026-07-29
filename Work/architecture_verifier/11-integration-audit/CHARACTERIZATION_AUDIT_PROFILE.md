# ART-11b-CHAR — Characterization Integration Audit Profile (Normative)

**Artifact ID:** `ART-11b-CHAR`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-11b · ART-CRP · ART-01 · ART-07b · ART-12-CHAR  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## Purpose

Integration-audit profile for characterization-only verification. Allows honest `PASS` / `FAIL` / `ESCALATE_HUMAN` (revision required) **without** MechanismInstance, Q_ψ, stability certificate, or inference bridge.

## Package-type routing (I-AR-ROUTE-01)

| CRP `profile` | Audit profile |
|---------------|---------------|
| `PHASE_A_CHARACTERIZATION` | **ART-11b-CHAR** (this file) + ART-11b question table with applicability overrides below |
| `PHASE_B_STABILIZATION` | ART-11b baseline (all ALWAYS modes as written) |
| `BRIDGE_ONLY` | ART-11b with IF_INFERENCE emphasis; Q04 NA unless mechanism present |
| `MIXED` | Per-claim: characterization claims → CHAR overrides; stability/mechanism claims → baseline |
| `OBLIGATION_ONLY` | CHAR overrides; Q17 checks obligation-facing progress |

Commit `RECORD_AUDIT` MUST record `audit_profile_id ∈ {ART11b.BASE, ART11b.CHAR, ART11b.BRIDGE, ART11b.MIXED}`.

## Applicability overrides (characterization)

When audit_profile = `ART11b.CHAR` (or MIXED claim is characterization-facing and no mechanism):

| ID | Mode under CHAR | Rule |
|----|-----------------|------|
| Q04 | **NOT_APPLICABLE** | Perturbation DD question NA unless live MechanismInstance / mechanism_proposal bound to claim |
| Q08–Q10 | NA if claim is pure characterization without induced policy/inference target | Else ALWAYS as baseline |
| Q11 | IF_INFERENCE only | Unchanged |
| Q17 | **PASS_REQUIRED (characterization-facing)** | YES iff claim advances **characterization** chain (ART-01 `characterization_facing`) or discharges a blocking `ProofObligation` for that claim — **not** the mechanism→stability→inference chain |

**I-AR-CHAR-01:** CHAR profile MUST NOT demand perturbation law, MechanismInstance, Q_ψ, stability certificate, or inference bridge as a condition of PASS.

**I-AR-CHAR-02 Verdicts:** `PASS` | `FAIL` | `IRRELEVANT` | `ESCALATE_HUMAN`. Map `ESCALATE_HUMAN` / failed structural binds → **REVISION_REQUIRED** for CRP resubmit messaging (not a separate AuditRecord enum — operational label).

## Characterization checklist prompts (auditor attestation)

In addition to applicable ART-11b questions, CHAR profile requires answers to:

| ID | Prompt |
|----|--------|
| QC1 | Tie / non-uniqueness cases addressed or explicitly scoped out |
| QC2 | Regime / domain of characterization stated |
| QC3 | No silent continuity / dimension assumptions |
| QC4 | Necessity/sufficiency claims match evidence |
| QC5 | ART-12-CHAR applicable classes attempted or skipped with reason |

QC* use same Answer schema; bijection over {applicable ART-11b Qs} ∪ {QC1–QC5}.

## Traces

```text
TRACE-CHAR-A  Phase A CRP, Q04=NA, Q17 characterization YES → may PASS
TRACE-CHAR-B  Phase A CRP forced Q04 YES without mechanism → AUDIT_PROFILE_VIOLATION
TRACE-CHAR-C  Argmax margin OK fixture → PASS path
TRACE-CHAR-D  Omit-ties negative → FAIL or FULL CX
```
