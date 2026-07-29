# 11c — Model / Data Provenance Binding (Normative)

**Artifact ID:** `ART-11c`  
**Version:** `ARCH-0.3-REPAIR-ITER11.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-07c · ART-04c · ART-11b · ART-06b · ART-13b · ART-15 · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for factual DD verification + model-prov lifecycle invalidation.

## Purpose

Machine-checkable VERIFIED path for data-independence / FIXED DD. Model provenance replace/revoke invalidates credited acts. ψ data-dependence is Commit-derived.

`ponytail:` Declared `reads[]` only — ambient undeclared OS reads are outside Commit (auditor may REJECTED). Literature import registry / full F_D chain → later. Fixtures → Iter12. Release dual-model → Iter14.

---

## 1. Objects

```text
DdReadRef
  kind                  # DATASET | CALIBRATION | ADAPTIVE | EXTERNAL_FETCH | OTHER
  digest

DataDependenceRecord                  # ART-07b identity; derivation_payload MUST include:
  # derivation_payload.reads[] : DdReadRef*   (canonical; absent ⇒ treat as [])

DdVerificationRecord
  dd_verification_digest = H("ART11c.DDV.v1", dd_digest, status, closure_digest,
                             verifier_binding_digest)
  dd_digest
  status                                # VERIFIED | REJECTED
  closure_digest                        # H(sorted (kind,digest) of reads) or H("EMPTY")
  verifier_binding_digest
  intro_event_seq

CalibrationSubmechanismCert           # minimal typed cert for I-PSI-02
  cal_cert_digest = H("ART11c.CAL.v1", claim_or_mechanism_digest, submechanism_digest,
                      proof_evidence_digest)
  claim_or_mechanism_digest
  submechanism_digest
  proof_evidence_digest                 # ART-07b ProofEvidence; floor ≥ INFORMAL

ModelProvKey = H(provider_id, model_id) # family key inside ModelProvenanceRecord fields

ModelProvInvalidation
  model_prov_digest
  at_event_seq
```

**I-DDV-01:** `dd_verification_status(dd)` = VERIFIED iff live `DdVerificationRecord` with matching `dd_digest` and `status=VERIFIED`; else not VERIFIED.

**I-DDV-11:** A VERIFIED `dd_digest` authorizes Claim/certificate C only when `C.parameter_domain_core_digest = D.bound_core_digest`. Else `DD_CORE_MISMATCH` (not authorized even if VERIFIED).

**I-CERT-DD-01 / `dd_ok`:** Data-independence / FIXED uses require I-DDV-01 VERIFIED **and** I-DDV-11; else `DD_BLOCKED` or `DD_CORE_MISMATCH`.

---

## 2. Closure + I-DDV-20 (Commit-executable)

**Declared closure** of a `DataDependenceRecord` = the `reads[]` array in `derivation_payload` (canonical JSON). No other ambient walk.

**I-DDV-20** (`REGISTER_DD_VERIFICATION` checks; all required):
1. `dd_digest` resolves to live DataDependenceRecord D.
2. Schema of `D.derivation_schema_id` is registered.
3. Every `reads[].kind` ∈ schema `allowed_read_kinds` (FIXED ⇒ must be empty list and `reads[]` empty).
4. If schema `dd_class_fixed=true`: `reads=[]` else reject `DD_HIDDEN_READ` when any read present; `closure_digest` MUST equal `H("EMPTY")`.
5. If not FIXED: `closure_digest = H(sorted (kind,digest) pairs of reads)` MUST equal payload; empty reads allowed only if schema permits.
6. `status=VERIFIED` only if 1–5 hold; `REJECTED` always allowed for auditor judgment (incl. suspected undeclared reads).

**Schema marker:** ART-07b `SchemaRegistryEntry` for a FIXED derivation schema MUST set `dd_class_fixed=true` and `allowed_read_kinds=[]` (empty). Non-FIXED schemas list allowed kinds ⊆ {DATASET,CALIBRATION,ADAPTIVE,EXTERNAL_FETCH,OTHER}.

---

## 3. Commands

**REGISTER_DD_VERIFICATION** (INTEGRATION_AUDITOR): `{dd_digest, status, closure_digest}` → I-DDV-20 → upsert DdVerificationRecord.

**REGISTER_MODEL_PROV** (IDENTITY_ADMIN): ART-04c upsert. If a prior live digest D shares the same `ModelProvKey` and differs in `model_prov_digest`, DeriveEffects MUST also upsert `ModelProvInvalidation(D)`.

**REVOKE_MODEL_PROV** (IDENTITY_ADMIN): `{model_prov_digest}` → upsert `ModelProvInvalidation`; RoleBindings citing it become non-live for MODEL_RUNTIME (treat as revoked digest).

**RECORD_CAL_SUBMECH_CERT** (PROOF_CERTIFIER or INTEGRATION_AUDITOR): upsert CalibrationSubmechanismCert when proof_evidence_digest resolves and floor ≥ INFORMAL.

**I-MP-20:** Live `ModelProvInvalidation` for D ⇒ any AuditRecord / CertificationRecord / ART-18 credited act pinned to D is **stale** for APPLY / credit until re-done under a live non-invalidated `model_prov_digest`.

---

## 4. ψ dependence (derived)

**I-PSI-01:** `requires_DATA_DEP_PSI(C)` ⇔ Commit-derived mechanism/domain snapshot for C has non-FIXED DD class on the ψ/calibration path **or** mechanism payload marks `calibration_submechanism` present. Writer labels non-authoritative.

**I-PSI-02:** If `requires_DATA_DEP_PSI(C)` on major APPLY / S06-exit for C, require all of:
1. EffectiveDecision(`DATA_DEP_PSI`, target) approve (ART-15 / ART-13b EffectiveDecision),
2. live `CalibrationSubmechanismCert` whose `claim_or_mechanism_digest` binds C’s mechanism,
3. if C asserts data-independence / FIXED: I-DDV-01 VERIFIED for its `dd_digest`.  
Else `DATA_DEP_PSI_REQUIRED` / `DD_BLOCKED`.

**I-CERT-DD-01:** Data-independence / FIXED uses require I-DDV-01 VERIFIED for its `dd_digest` **and** I-DDV-11 core match; else `DD_BLOCKED` / `DD_CORE_MISMATCH`.

---

## 5. Audit / ART-18 / ART-19

**I-Q04-01:** ART-11b Q04 YES only if (a) FIXED ∧ I-DDV-01 VERIFIED, or (b) I-PSI-02 holds. Attestation without those ⇒ not a valid YES for I-BIND-01.

**I-MP-02:** ART-04c unchanged; ART-18 credit requires it.

**I-EV-01:** For major APPLY, `evidence_refs` ≔ `PromotionIntent.basis_digests[]`. Each digest MUST resolve to a live non-quarantine, non-SUPERSEDED, non-I-CX-01-hit-without-I-DW-21-clear object with pin/label match; else `EVIDENCE_PROV_FAIL`. No separate carrier field.

---

## 6. APPLY fences (ART-13b I-AP-15)

While DRAFT_REPAIR or ACTIVE_NORMATIVE: ValidationPreimageAPPLY.v7 `dd_ok` / `psi_ok` / `model_prov_ok` Commit-derived per §§2–5. Fail codes: `DD_BLOCKED` | `DATA_DEP_PSI_REQUIRED` | `MODEL_PROV_STALE` | `EVIDENCE_PROV_FAIL` | `DD_HIDDEN_READ` | `DD_CORE_MISMATCH`.

---

## 7. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-07b | SchemaRegistryEntry `dd_class_fixed` / `allowed_read_kinds`; reads[] in DD payload |
| ART-07c | I-CERT-DD-01 → I-DDV-01 / `DD_BLOCKED` |
| ART-04c | REGISTER_DD_VERIFICATION; REVOKE_MODEL_PROV; I-MP-20 |
| ART-11b | Q04 = I-Q04-01 |
| ART-13b | I-AP-15 + v7 preimage + failure codes |
| ART-15 | DATA_DEP_PSI |
| ART-18/19 | credit / evidence under §§5 |

---

## 8. Traces

```text
TRACE-11A  FIXED without VERIFIED → DD_BLOCKED
TRACE-11B  FIXED schema with reads[] → DD_HIDDEN_READ
TRACE-11C  requires_DATA_DEP_PSI without HD/cal cert → DATA_DEP_PSI_REQUIRED
TRACE-11D  REGISTER_MODEL_PROV supersede key → MODEL_PROV_STALE on old audit APPLY
TRACE-11E  evidence_ref SUPERSEDED → EVIDENCE_PROV_FAIL
```
