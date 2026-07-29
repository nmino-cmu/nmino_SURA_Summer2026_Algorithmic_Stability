# 10b — Lean Manifest Binding (Normative)

**Artifact ID:** `ART-10b`  
**Version:** `ARCH-0.3-REPAIR-ITER8.9`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-06b · ART-04c · ART-13b · ART-16b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for ART-10b. Targets `B-LEAN-CLOSURE-01`.

## Purpose

Digest-bound LeanManifest; status = f(manifest, state) only; LEAN_REF → INFORMAL when FULL/CORE; LEAN_GAP on rank drop. Lean ≠ CERTIFIED for RESULT.

`ponytail:` FSM math_stable → Iter9. Filesystem drift without RECORD is outside ResearchState.

---

## 1. Objects

```text
LeanToolchainHead
  toolchain_digest
  mathlib_pin_digest
  set_at_event_id

VerifierTranscript                    # sole rebuild authority
  toolchain_digest
  mathlib_pin_digest
  entry_module_id
  lean_statement_digest
  proof_tree_digest
  import_closure_digest
  definition_pin_set[]
  sorry_count
  admit_count
  custom_axiom_ids_sorted[]
  imported_axiom_closure_sorted[]
  build_ok
  rebuild_log_digest

LeanManifest
  claim_digest
  claim_math_fingerprint
  transcript                          # VerifierTranscript
  manifest_digest = H("ART10b.LM.v4", claim_digest, claim_math_fingerprint, H(transcript))
```

**Side binding:** If `transcript.custom_axiom_ids_sorted` nonempty, Commit selects ART-13b EffectiveDecision approve `AXIOM_ADOPTION` with `target_digest = H("AXIOM_ADOPTION", claim_digest, custom_axiom_ids_sorted)` (no caller-supplied decision_digest).

**I-LM-01:** No writable lean_status.  
**I-LM-02:** live Claim; `claim_math_fingerprint` match else `FINGERPRINT_MISMATCH`.  
**I-LM-03:** custom axioms ⇒ side-bound HD else `AXIOM_GATE_REQUIRED`.  
**I-LM-04:** `transcript.toolchain/mathlib` = live LeanToolchainHead; `definition_pin_set` = live ActiveDefinitionHead else `PIN_MISMATCH`.  
**I-LM-05:** `transcript.lean_statement_digest = ConclusionDigest(Claim)` else `STATEMENT_MISMATCH`.

---

## 2. DerivedLeanStatus

**Rank:** LEAN_FULL=5, LEAN_CORE=4, LEAN_STATEMENT=3, LEAN_BLOCKED=2, NOT_READY_FOR_LEAN=1, LEAN_STALE=0.

Latest LeanManifest for C; none ⇒ `NOT_READY_FOR_LEAN`.

**I-LM-10:** If pin≠head ∨ toolchain≠head ∨ FULL CX hits C ∨ SUPERSEDED ⇒ `LEAN_STALE`.  
Else if `build_ok=false` ⇒ `LEAN_BLOCKED`.  
Else if sorry=0 ∧ admit=0 ∧ no custom axioms ∧ `axiom_closure_captured` ⇒ `LEAN_FULL`.  
Else if sorry=0 ∧ admit=0 ∧ (custom axioms present or axiom closure missing) ⇒ `LEAN_CORE` or `LEAN_BLOCKED` (missing capture ⇒ `LEAN_BLOCKED`).  
Else if build_ok ⇒ `LEAN_STATEMENT`.  
Else `NOT_READY_FOR_LEAN`.

**Runtime note (filesystem surrogate):** `LEAN_FULL` additionally requires `#print axioms` capture stored in `imported_axiom_closure_sorted` with `axiom_closure_captured=true`. `--skip-lake` never yields `LEAN_FULL`. Certificates under `lean/certificates/` are ART-10b surrogates (`LEAN_MANIFEST_WITHOUT_COMMIT`), not Commit EventLog records. Re-verify with `verify_certificate` before trusting on-disk status JSON.

**I-LM-11:** Status never stored as a label.

---

## 3. Commands

**SET_LEAN_TOOLCHAIN** (VERIFICATION_ORCHESTRATOR): upsert head; mint I-DW-32 for each claim with pre rank≥4 becoming LEAN_STALE.

**RECORD_LEAN_MANIFEST** (LEAN_VERIFIER): `{ claim_digest, claim_math_fingerprint, VerifierTranscript, signature }`. Commit builds LeanManifest, checks I-LM-01..05 (incl. EffectiveDecision for axioms), upserts.  
**I-LM-20:** if rank(pre)≥4 and rank(post)<rank(pre) ⇒ I-DW-32.

**I-DW-32:** `trigger_digest = H("LEAN_GAP", claim_digest, pre_manifest_or_⊥, post_manifest_or_⊥, mint_pre_state_head_digest)`; OPEN_CLAIM seeds/dependents; no SUPERSEDE.

---

## 4. LEAN_REF floor

Authoritative floor ordering is ART-07b `DerivedProofFloor`: **LEAN_REF is evaluated before I-CERTIFY-01**, so Lean evidence cannot launder into CERTIFIED_INFORMAL. LEAN_REF yields INFORMAL iff live manifest has DerivedLeanStatus ∈ {LEAN_FULL, LEAN_CORE}; else UNPROVED. ATTACH_CERTIFICATION requires ProofEvidence.kind=CERTIFIED_STRUCTURED (ART-04c).

**I-LM-30:** LEAN_REF body `manifest_digest` = live. **I-LM-31:** RESULT needs CERTIFIED.

---

## 5. Consumer deltas

ART-07b LeanManifest/ToolchainHead + LEAN_REF floor · ART-06b RECORD/SET · ART-04c LEAN_VERIFIER · ART-16b LEAN_GAP · ART-05/10 legacy → 10b · ART-13b unchanged.

**Runtime (2026-07-25):** Until ART-06b Commit EventLog is implemented, the Python runtime uses `LeanManifestStore` (`store_kind=ART10b_SURROGATE_V1`) under `lean/certificates/`. Digests match ART-10b shapes; `LEAN_MANIFEST_WITHOUT_COMMIT` is recorded. Prop STATEMENT-region hash is the ConclusionDigest surrogate (I-LM-05). See [LEAN_RUNTIME.md](LEAN_RUNTIME.md) · [FORMALIZATION_IR.md](FORMALIZATION_IR.md).

---

## 6. Failures / traces

`FINGERPRINT_MISMATCH | STATEMENT_MISMATCH | PIN_MISMATCH | AXIOM_GATE_REQUIRED | MANIFEST_INVALID | WAVE_EXISTS`

```text
TRACE-8A  RECORD FULL → LEAN_REF → INFORMAL
TRACE-8B  toolchain SET → STALE + LEAN_GAP
TRACE-8C  RESULT needs CERTIFIED
TRACE-8D  axiom HD side-bound (no digest cycle)
TRACE-8E  STATEMENT_MISMATCH if conclusion ≠ Lean statement
TRACE-8F  LEAN_GAP generations unique via trigger_digest
```
