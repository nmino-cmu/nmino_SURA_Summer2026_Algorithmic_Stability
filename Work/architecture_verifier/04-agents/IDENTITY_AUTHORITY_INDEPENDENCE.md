# 04c — Identity, Authority, Human Decisions, and Independence (Normative)

**Artifact ID:** `ART-04c`  
**Version:** `ARCH-0.3-REPAIR-ITER4.6`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-07c · ART-06b  
**Authority:** Design material. Material post-freeze edits require a new revision.

## Purpose

Authenticated principals, authorized role bindings, independence closures, model provenance, constructible HumanDecisions, and CERTIFIED reachability — without forgeable bootstrap or circular digests. Properties, not PKI products.

---

## 1. Genesis and command authentication

```text
TrustRoot                             # DesignState; package genesis (no principal-digest cycle)
  root_digest                         # = H(root_schema_id, genesis_subject_materials_sorted, policy_digest)
  genesis_subject_materials[]         # public materials of initial HUMANS (not principal digests)
  identity_admin_policy_digest
```

Genesis Principals: for each material M, `Principal{kind=HUMAN, subject_public_material=M, issuer_digest=root_digest}`.  
`principal_digest = H(schema, kind, M, root_digest)` — well-founded (root does not hash principal digests).  
Genesis RoleBindings (IDENTITY_ADMIN, HUMAN_GATE_OPERATOR, COMMITTER) are **package seed records** installed with the TrustRoot (DesignState), not produced by a prior Commit.

**Command authentication (extends ART-06b Command):**

```text
Command (+ Iter4)
  caller_principal_digest             # required
  caller_binding_digest               # live RoleBinding for this act
  caller_signature_material           # verifies over H(unsigned command fields excl. this signature)
```

**I-CMD-AUTH-01:** `I.Commit` REJECTS unless caller Principal ACTIVE, binding live at pre-state `event_seq`, signature verifies over unsigned command preimage, and command_kind ∈ authorized kinds for `binding.role_id` (matrix §8).

**I-GEN-01:** Package ships with ≥1 genesis subject materials ⇒ ≥1 HUMAN Principals as above. Emptying genesis set requires `SCOPE_CHANGE` from a remaining genesis principal.

---

## 2. Principal

```text
Principal                             # immutable identity preimage
  principal_digest                    # = H(principal_schema_id, kind, subject_public_material, issuer_digest)
  principal_schema_id
  kind                                # HUMAN | SERVICE | MODEL_RUNTIME
  subject_public_material
  issuer_digest                       # TrustRoot.root_digest OR authorizing HUMAN principal_digest
```

Status/revocation = **derived** from MutationEvent log (REGISTER_PRINCIPAL / REVOKE_PRINCIPAL), not stored mirrors in the identity digest.

**I-PRIN-01:** Free-text actor/agent IDs are non-authoritative.  
**I-PRIN-02:** REGISTER_PRINCIPAL for `kind=HUMAN` requires caller ∈ genesis OR caller has IDENTITY_ADMIN binding per TrustRoot policy.  
**I-PRIN-03:** MODEL_RUNTIME / SERVICE enrollment requires IDENTITY_ADMIN (or designated SERVICE_ADMIN) binding.

---

## 3. ModelProvenanceRecord

```text
ModelProvenanceRecord
  model_prov_digest                   # = H(provider_id, model_id, model_version,
                                      #    weights_or_build_digest, prompt_profile_digest,
                                      #    tool_allowlist_digest, decoding_profile_digest,
                                      #    attestation_digest)
  … fields as hashed …
  attestation_digest                  # provider or admin attestation payload digest (required)
```

**I-MP-01:** MODEL_RUNTIME RoleBinding MUST reference a registered `model_prov_digest`.  
**I-MP-02:** Credited acts pin `model_prov_digest` + `binding_digest` at act `event_seq` (no silent swap credit). ART-18 reports/reconciliations credited under this artifact MUST:  
1. carry `act_event_seq` equal to the introducing MutationEvent’s `event_seq`;  
2. carry `author_*` / `reconciler_*` principal and binding equal to that event’s `caller_principal_digest` and `caller_binding_digest`;  
3. carry `*_model_prov_digest` equal to the RoleBinding at `caller_binding_digest`’s `model_prov_digest` (absent/`⊥` when principal is not MODEL_RUNTIME);  
4. have that binding live at `act_event_seq` (I-RB-01).  
Missing, unbound, or mismatched ⇒ no credit (not a credited act).  
**I-MP-20:** Material replace/revoke of live `model_prov_digest` D ⇒ ART-11c ModelProvInvalidation; prior credited acts pinned to D are stale for APPLY (ART-11c).

---

## 4. RoleBinding

```text
RoleBinding
  binding_digest                      # = H(principal_digest, role_id, model_prov_digest_or_⊥,
                                      #    valid_from_event_seq, valid_to_event_seq_or_⊥)
  principal_digest
  role_id                             # PROOF_PROPOSER | PROOF_CERTIFIER | EIO | INTEGRATION_AUDITOR
                                      # | VERIFICATION_ORCHESTRATOR | FRONTIER_SCHEDULER | LEAN_VERIFIER
                                      # | HUMAN_GATE_OPERATOR | COMMITTER | IDENTITY_ADMIN
                                      # | LITERATURE_ANALYST | RESEARCH_SCOPE | COUNTEREXAMPLE_ATTACKER
                                      # | RESEARCH_DISCOVERY_ASSISTANT | DISCOVERY_ORCHESTRATOR  # DUAL.2
                                      # | …
  model_prov_digest?                  # required iff principal.kind=MODEL_RUNTIME
  valid_from_event_seq
  valid_to_event_seq?
```

**I-RB-01:** Live = `valid_from ≤ event_seq` and (`valid_to` absent or `event_seq < valid_to`) and principal not revoked.  
**I-RB-02:** Overlapping live PROOF_PROPOSER + PROOF_CERTIFIER for same principal → invalid.  
**I-RB-03:** BIND_ROLE for HUMAN_GATE_OPERATOR / IDENTITY_ADMIN / COMMITTER requires caller authorized by TrustRoot policy (typically genesis or IDENTITY_ADMIN).

Independence is **not** a field on RoleBinding — derived in §5.

---

## 5. Independence (authoritative closure)

```text
IndependenceAtom
  atom_digest                         # = H(policy_digest, controller_key_digest,
                                      #    controller_attestation_digest, member_principal_digests_sorted)
  policy_digest
  controller_key_digest               # = H(controller_attestation.subject_material) under policy schema
  controller_attestation              # typed payload: issuer_principal_digest, subject_material,
                                      #   statement_schema_id, statement_payload, signature_material
  controller_attestation_digest       # = H(controller_attestation without its signature);
                                      #   signature verifies over that digest; issuer must be IDENTITY_ADMIN
                                      #   or TrustRoot-authorized attestor
  member_principal_digests[]
```

**I-IND-01:** Every Principal has exactly one live atom membership per `policy_digest` used by a check (registered via Commit by IDENTITY_ADMIN). Self-membership required.  
**I-IND-02:** Overlapping membership under the same policy merges into one equivalence component (transitive closure).  
**I-IND-03:** Independence check for certify: atoms of proposer vs certifier are disjoint components under the policy.  
**I-IND-04:** REGISTER_ATOM rejected unless attestation verifies and `controller_key_digest` matches attestation subject; all listed members’ enrollment records cite the same controller_key under the policy schema (machine-checkable enrollment field on Principal registration metadata).  
**I-IND-05:** Under one `policy_digest`, all live atoms sharing the same `controller_key_digest` are one equivalence component for I-IND-02/03 (merge by controller key). REGISTER_ATOM that would introduce a second live atom with an already-live controller key under that policy is **rejected**. Membership growth uses `EXTEND_ATOM(old_atom_digest, new_atom)`: one Commit effect set that (a) retires the live atom with `old_atom_digest`, (b) installs `new_atom` with same `policy_digest` + `controller_key_digest`, recomputed `atom_digest`, and member set ⊇ old members; I-IND-04 attestation rules apply to `new_atom`. No other path may replace a live atom’s membership.

Default certify checks (both required when applicable): policy `SAME_HUMAN` always; additionally `SAME_MODEL_FAMILY` when either party `kind=MODEL_RUNTIME`.

---

## 6. HumanDecision (constructible)

```text
HumanDecisionUnsigned
  gate_id
  target_digest
  decision
  principal_digest
  evidence_packet_digest
  expires_at_event_seq?
  blast_radius_digest

decision_payload_digest = H(HumanDecisionUnsigned)
decision_digest = decision_payload_digest   # identity = unsigned payload; signature detached

HumanDecision
  decision_digest
  unsigned
  signature_material                  # verifies over decision_payload_digest; NOT part of decision_digest
```

**I-HD-AUTH-01:** Authoritative iff: Principal ACTIVE HUMAN; live HUMAN_GATE_OPERATOR binding; signature OK; gate∈ART-15; target matches gate schema; approve when authorizing; not expired at use `event_seq`; committed via authenticated Commit.  
**I-HD-AUTH-02:** ESCALATE_HUMAN ≠ Decision.  
**I-HD-01:** REVOKED when this artifact ACTIVE.

---

## 7. CertificationRecord (CERTIFIED path)

```text
CertificationRecordUnsigned
  proof_evidence_digest               # claim DERIVED from ProofEvidence; attachment DERIVED
  certifier_binding_digest            # principal + model_prov DERIVED from RoleBinding
  # proposer/certifier atoms DERIVED at attachment seq via I-IND-01 for certify policies

certification_digest = H(CertificationRecordUnsigned)
```

**I-CERTIFY-01:** Floor CERTIFIED_INFORMAL at S iff ∃ committed ATTACH_CERTIFICATION where:  
- digests recompute; derived claim from evidence; derived attachment matches claim+evidence  
- **ProofEvidence.kind = CERTIFIED_STRUCTURED** (LEAN_REF / INFORMAL_STRUCTURED cannot certify)  
- caller binding = named `certifier_binding_digest`; derived caller principal/model_prov match binding  
- derived proposer_act_event_seq’s Command created exactly this `proof_evidence_digest`; derived proposer principal/binding/model_prov match that Command (model_prov from binding)  
- certifier_binding live PROOF_CERTIFIER at attachment seq  
- derived atoms at attachment seq disjoint per I-IND-03 (human; model if either party MODEL_RUNTIME)  
- HD valid; target_digest = certification_digest  

**I-CERTIFY-02:** Else no such record ⇒ not CERTIFIED_INFORMAL (INFORMAL at best).  
**I-CERTIFY-03:** Effects may add certification/proof links only — no ResearchMaturityRecord / inference axis writes.

---

## 8. Role × command authorization (minimum)

| role_id | May submit command_kinds (non-exhaustive) |
|---------|-------------------------------------------|
| COMMITTER | any otherwise authorized Commit (serialization actor) |
| IDENTITY_ADMIN | REGISTER/REVOKE_PRINCIPAL, BIND_ROLE (per policy), REGISTER_ATOM, EXTEND_ATOM, REGISTER_MODEL_PROV, REVOKE_MODEL_PROV (ART-11c), SEAL_RELEASE_MANIFEST (ART-25b) |
| HUMAN_GATE_OPERATOR | RECORD_HUMAN_DECISION; SUBMIT_CANDIDATE_PACKAGE when author_kind=HUMAN; HARD_STOP_CLEAR embed |
| PROOF_CERTIFIER | ATTACH_CERTIFICATION (caller must be named certifier); RECORD_CAL_SUBMECH_CERT (ART-11c) |
| PROOF_PROPOSER | REGISTER_CLAIM, ATTACH_INFORMAL_PROOF, … |
| EIO | SET_EIO_VETO, CLEAR_EIO_VETO, RECORD_EIO_ASSESSMENT (ART-13b); otherwise advice-only |
| INTEGRATION_AUDITOR | RECORD_AUDIT (ART-11b); REGISTER_DD_VERIFICATION / RECORD_CAL_SUBMECH_CERT (ART-11c); may author N/A_UTILITY_ACK HumanDecision (ART-13b I-AP-10c) |
| FRONTIER_SCHEDULER | Discovery-side only (ART-01D / ART-04e); does **not** LOCK_CYCLE on B after DUAL.1 |
| COUNTEREXAMPLE_ATTACKER | RECORD_COUNTEREXAMPLE (ART-16b) |
| VERIFICATION_ORCHESTRATOR | SUBMIT/REJECT_CANDIDATE_PACKAGE (ART-CRP); LOCK_CYCLE / cycle cmds (ART-08d); APPLY / demotion / CX orchestration (B) |
| RESEARCH_DISCOVERY_ASSISTANT | Author CRP only; no ResearchState Commit |
| DISCOVERY_ORCHESTRATOR | A-local only (ART-04e); never B Commit roles_invoked |
| LEAN_VERIFIER | RECORD_LEAN_MANIFEST (ART-10b) |

Genesis HUMANS initially hold IDENTITY_ADMIN + HUMAN_GATE_OPERATOR + COMMITTER bindings.


---

## 9. Interfaces

Public write: ART-06b `I.Commit` only (typed command_kinds above).  
Pure: `I.IndependenceCheck(principal_a, principal_b, policy) → DISJOINT | SAME_ATOM | UNKNOWN_ATOM`.

---

## 10. Failure taxonomy

```text
UNKNOWN_PRINCIPAL | PRINCIPAL_REVOKED | ROLE_BINDING_MISSING | ROLE_COLLISION
CMD_AUTH_FAIL | UNAUTHORIZED_COMMAND | TRUST_ROOT_VIOLATION
MODEL_PROV_MISSING | MODEL_PROV_STALE | INDEPENDENCE_VIOLATION | ATOM_UNREGISTERED
HD_SIGNATURE_INVALID | HD_EXPIRED | HD_GATE_MISMATCH | HD_TARGET_MISMATCH
CERTIFY_PROOF_MISMATCH | CERTIFY_NO_CERTIFIER | CERTIFY_HD_TARGET_MISMATCH
LEGACY_ACTOR_ID
```

---

## 11. Traces

4A self-enroll without genesis → UNAUTHORIZED_COMMAND.  
4B circular HD impossible (payload digest unsigned).  
4C two keys one human without shared atom → IDENTITY_ADMIN reject / IND fail.  
4D PROOF_CERTIFY targeting claim only → CERTIFY_HD_TARGET_MISMATCH.  
4E valid CertificationRecord → CERTIFIED_INFORMAL.  
4F ATTACH_CERTIFICATION writing RESULT → PROMOTION_DEFERRED_ITER5.

---

## 12. Non-goals

PromotionIntent (5); audit binding (6); specific OIDC/WebAuthn products.
