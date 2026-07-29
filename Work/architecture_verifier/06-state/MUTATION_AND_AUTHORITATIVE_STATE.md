# 06b — Authoritative State and Mutation Semantics (Normative)

**Artifact ID:** `ART-06b`  
**Version:** `ARCH-0.3-REPAIR-ITER3.2`  
**Normative status:** `ACTIVE_NORMATIVE` (Iteration 3 complete; Sol reviews A–D PASS on ITER3.2)  
**Depends on:** `ART-07b` ITER1.26 · `ART-07c` ITER2.7  
**Supersedes for mutation/commit authority:** ART-06 event/registry poke prose; ART-24 direct `I.HardStop` / ProposeWrite-alone  
**Authority:** Design material. Changes reset Iteration-3 readiness.

## Purpose

One logically serialized authoritative mutation boundary. No caller-trusted booleans. ControlState fenced from ResearchState. Hard-stop is a commit-linearized fence. Stale writes fail closed. Event log is replay-sufficient.

## Scope lock

Architecture properties only — not a DB/queue/consensus product. Serialization = total order of accepted commits for Control+Research+Design+IrreversibleSafetyLog.

---

## 1. State stores (four)

| Store | Contents | Mutated only via |
|-------|----------|------------------|
| **ControlState** | Exact record below | `I.Commit` |
| **ResearchState** | ART-07b/07c objects + side tables | `I.Commit` |
| **DesignState** | Architecture package artifacts / critique ledger | `I.Commit` (`store_targets` includes DESIGN) |
| **IrreversibleSafetyLog** | ART-17b receipts / head (not restorable via ResearchState snapshot alone) | `I.Commit` — same atomic accept; if I-IR-01 fires and receipt append fails ⇒ reject whole Commit |

```text
ControlState                          # exact field set — no ellipsis
  event_seq                           # u64; last accepted commit seq (0 if none)
  hard_stop                           # HardStopRecord
  role_ceiling_profile_digest         # digest of active OPERABLE_MINIMAL / expanded profile
```

```text
HardStopRecord
  active                              # bool
  source                              # HUMAN | BUDGET | SYSTEM | ⊥ if !active
  set_at_event_seq                    # 0 if !active
  signal_ref_digest                   # ⊥ if !active
  release_dec_digest                  # ⊥ if active or never cleared; set only on CLEAR
```

**I-STATE-SEP-01:** Research object identity and promotion/audit effects live only in ResearchState. Shared EventLog holds MutationEvents (I-LOG-01). ControlState never stores Claims/certs/bridges as research authority.  
**I-STATE-SEP-02:** A single commit may list multiple `store_targets`, but effects for each store are typed and validated; no silent dual-write from agent scratch.

---

## 2. Heads (closed digests)

```text
control_head_digest = H(
  event_seq,
  hard_stop.active, hard_stop.source, hard_stop.set_at_event_seq,
  hard_stop.signal_ref_digest, hard_stop.release_dec_digest,
  role_ceiling_profile_digest
)

research_snapshot_digest = H(canonical serialization of all ResearchState
  objects/side-tables EXCLUDING the MutationEvent log)

research_head_digest = H(event_seq, research_snapshot_digest,
  H(ordered MutationEvent.event_digest for seq=1..event_seq))

design_head_digest = H(event_seq, DesignState snapshot digest)

state_head_digest = H(event_seq, control_head_digest, research_head_digest, design_head_digest)
```

**I-HEAD-01:** Heads are DERIVED only. Agent-supplied head values are never authoritative.

---

## 3. Command and effects (bound)

```text
Command                               # sole preimage; digest computed inside I.Commit
  command_kind
  store_targets[]                     # nonempty subset of {CONTROL, RESEARCH, DESIGN, IRREVERSIBLE}
  payload                             # typed per command_kind
  expected_state_head_digest          # = H(event_seq, control, research, design, irreversible heads)
  caller_principal_digest             # ART-04c — required when ART-04c ACTIVE
  caller_binding_digest
  # caller_signature_material NOT in command_digest preimage for unsigned hash;
  # signature verifies over H(Command without signature field)

command_digest = H(Command without caller_signature_material)

Effects                               # DERIVED — never caller-authoritative
  effects = DeriveEffects(Command, pre_ControlState, pre_ResearchState, pre_DesignState, pre_IrreversibleSafetyLog)
  research_control_design_effects     # object upserts / Control / Design only
  ir_receipt?                         # ART-17b; filled after event_digest known
  effects_digest = H(research_control_design_effects)  # NEVER hashes ir_receipt
```

**I-EFF-01:** `I.Commit` MUST set `effects = DeriveEffects(...)`. Validator validates **Command** and the derived **Effects**. No alternate effect set may be appended.  
**I-EFF-02:** `MutationEvent` stores the full `Effects` envelope (including `ir_receipt?`) so the log is replay-sufficient.  
**I-EFF-03:** Compute `event_digest` using receipt-free `effects_digest`; then set `ir_receipt.event_digest` if I-IR-01 fires; append receipt atomically with EventLog.

```text
MutationEvent                         # append-only EventLog (shared; not a Research object table)
  event_seq
  command                             # full Command preimage
  effects                             # full Effects envelope (may include ir_receipt?)
  validation_preimage                 # derived predicates, reason_codes, art07c_results[]
  event_digest = H(event_seq, command_digest, effects_digest,
                   H(validation_preimage), pre_state_head_digest)
```

**I-LOG-01:** EventLog append is allowed on CONTROL-only / IRREVERSIBLE commits. “Zero ResearchState mutations” means zero Research **object** upserts — not a ban on EventLog.

---

## 4. Mutation boundary (exclusive)

### I.Commit  (**sole mutator**; sole public write interface)

**In:** `Command` (inline).  
**Out:** `ACCEPTED{event_seq, event_digest, new_state_head_digest} | REJECTED{reason_codes[]}`.

**Pipeline (one indivisible transition; logical single-committer exclusivity — no `commit_busy` state bit):**
1. Recompute `state_head_digest`; if ≠ `Command.expected_state_head_digest` → `STALE_WRITE`.  
2. **ART-04c I-CMD-AUTH-01** (when ART-04c ACTIVE): authenticate caller + authorize command_kind.  
3. Hard-stop fence (§5) on **derived effects**.  
4. Caller-boolean ban (§6) on Command.payload.  
5. `effects = DeriveEffects(...)`; validate Command+Effects (ART-07b/07c/04c as applicable).  
6. **Tentative** post-state = Reduce(pre, effects). If reduce would fail → `REDUCE_ABORT` (**no** event appended).  
7. Else atomically: append MutationEvent; install post-state; `event_seq+=1`; recompute heads; ACCEPTED.

**I-MUT-01:** No normative write outside `I.Commit`.  
**I-MUT-02:** Rejected commits append nothing and leave heads unchanged (ART-24).  
**I-MUT-03:** Direct registry poke / scratch-as-authority → invalid.

`DeriveEffects` / `Reduce` are **internal pure functions** of Commit — not separate public interfaces.

---

## 5. Hard-stop fencing

**I-HS-01:** While `hard_stop.active=true`, Commit REJECTS unless **all** derived effects are in the allowlist:
- ControlState-only updates to `HardStopRecord` / `role_ceiling_profile_digest` / ControlState decision-log append for `HARD_STOP_RELEASE` only  
- IrreversibleSafetyLog receipt append when command_kind ∈ {`HARD_STOP_SET`,`HARD_STOP_CLEAR`} (ART-17b I-IR-01; receipt bytes excluded from event_digest preimage)  
- command kinds `HARD_STOP_SET`, `HARD_STOP_CLEAR`, `CONTROL_DIAGNOSTIC_NOOP`, and `RECORD_HUMAN_DECISION` **only when** `gate_id=HARD_STOP_RELEASE`  
with `store_targets ⊆ {CONTROL, IRREVERSIBLE}` and **zero Research object upserts** and **zero** DesignState mutations (EventLog + IR receipt append allowed per I-LOG-01 / I-EFF-03)

Provenance / ResearchState writers are **not** allowlisted during hard-stop.

`HARD_STOP_CLEAR` payload MAY embed the HumanDecision envelope (preferred during stop) so release need not be a prior ResearchState write.

**I-HS-02:** `HARD_STOP_SET` / `HARD_STOP_CLEAR` transitions:

| Kind | Requires | Post HardStopRecord |
|------|----------|---------------------|
| SET | `payload.source ∈ {HUMAN,BUDGET,SYSTEM}`, `signal_ref_digest` | `active=true`, source/signal/set_at_event_seq set, **`release_dec_digest=⊥`** |
| CLEAR | `payload.release_dec_digest ≠ ⊥` | `active=false`; `release_dec_digest=payload.release_dec_digest`; source/signal/set_at = ⊥ / 0 |

**I-HS-03:** Fence check uses ControlState fixed after stale-write head agreement and before accept — linearizable in the commit total order.  
**I-HS-04:** `HARD_STOP_CLEAR` requires `release_dec_digest` → ART-04c-valid HumanDecision `HARD_STOP_RELEASE` whose `target_digest` binds this freeze (`H(set_at_event_seq, signal_ref_digest)`), when ART-04c is ACTIVE.  
**I-HS-05:** Legacy `ResearchState.hard_stop` / direct `I.HardStop` are non-authoritative.

---

## 6. Caller-boolean ban

Forbidden as authoritative payload fields (reject `CALLER_BOOLEAN_FORBIDDEN`):

```text
dep_closure_ok | contradiction_clear | eio_pass | lit_closure_ok
hop_chain_ok | lean_manifest_ok | audit_pass | bridge_ok | cert_ok
math_stable | roles_ok | floor_ok | applicable | any authorizing *_ok
```

**I-BOOL-01:** Derived predicates appear only inside `validation_preimage`.  
**I-BOOL-02:** Commands that would **apply** research-maturity / inference-applicability **axis** transitions → `AXIS_WRITE_FORBIDDEN`, except `APPLY_PROMOTION` under ART-13b; `ADVANCE_DEMOTION_WAVE`; and DeriveEffects seed-`SUPERSEDED` writes of `RECORD_COUNTEREXAMPLE` (FULL) / `START_DEMOTION_WAVE` / I-DW-33 under ART-16b. Legacy codeword `PROMOTION_DEFERRED_ITER5` is an alias of `AXIS_WRITE_FORBIDDEN` for other non-APPLY commands until consumers migrate.  
Exception (ART-04c): `ATTACH_CERTIFICATION` may add CertificationRecord / proof-attachment links that make `DerivedProofFloor` evaluate to CERTIFIED_INFORMAL; it MUST NOT write ResearchMaturityRecord or inference axis fields.  
**ART-16b DeriveEffects:** I-DW-30/31/32/33/START mint waves + I-DW-26 `DemotionFloorBreak` upserts are Commit-derived (not caller booleans).

---

## 7. ResearchState keys

Authoritative keys = ART-07b/07c digests (`claim_digest`, `cx_digest`, …).  
**I-REG-01:** Legacy IDs alias-only if 1:1 bound; else `UNTYPED_LEGACY_OBJECT`.  
**I-REG-02:** ID-keyed cert/bridge tables non-authoritative.

---

## 8. Failure taxonomy

```text
STALE_WRITE | HARD_STOP_ACTIVE | CALLER_BOOLEAN_FORBIDDEN
PROMOTION_DEFERRED_ITER5 | AXIS_WRITE_FORBIDDEN | UNKNOWN_COMMAND | INVALID_PAYLOAD
DIGEST_MISMATCH | UNTYPED_LEGACY_OBJECT | STORE_SEPARATOR_VIOLATION
ART07_REJECT | ART07C_REJECT | ROLE_CEILING_REJECT | REDUCE_ABORT
EFFECTS_MISBIND
AUDIT_REQUIRED | AUDIT_FAIL | AUDIT_STALE | AUDIT_INDEPENDENCE | AUDIT_EVIDENCE_MISSING | DISCONFIRM_MISSING | UNKNOWN_AUDIT_QUESTION
```

**Command kinds (additive; auth ART-04c / ART-13b / ART-11b / ART-16b / ART-10b / ART-08d / ART-CRP):** includes `SUBMIT_CANDIDATE_PACKAGE`, `REJECT_CANDIDATE_PACKAGE`, `APPLY_PROMOTION`, `RECORD_EIO_ASSESSMENT`, `SET_EIO_VETO`, `CLEAR_EIO_VETO`, `RECORD_AUDIT`, `RECORD_DISCONFIRM`, `RECORD_COUNTEREXAMPLE`, `SET_ACTIVE_DEFINITION_HEAD`, `ATTACH_CERTIFICATION`, `START_DEMOTION_WAVE`, `ADVANCE_DEMOTION_WAVE`, `RECORD_LEAN_MANIFEST`, `SET_LEAN_TOOLCHAIN`, `LOCK_CYCLE`, `BIND_CYCLE_CARD`, `RECORD_CYCLE_ATTACK_LOG`, `RECORD_CYCLE_AUDIT`, `RECORD_CYCLE_LEAN`, `ADVANCE_CYCLE`, `CLOSE_CYCLE`, `HARD_STOP_SET`, `HARD_STOP_CLEAR`, `REGISTER_DD_VERIFICATION`, `REVOKE_MODEL_PROV`, `RECORD_CAL_SUBMECH_CERT`, …  
**ART-CRP:** `SUBMIT_CANDIDATE_PACKAGE` mints draft objects per ART-CRP; sole external math intake. Discovery engines are not Commit authorities.
**ART-16b DeriveEffects:** `RECORD_COUNTEREXAMPLE` (FULL) and `SET_ACTIVE_DEFINITION_HEAD` (head replace) MUST mint DemotionWave at cursor 0 in the same Commit (I-DW-30/31). I-DW-33 expansion and I-DW-32 LEAN_GAP mint under the same Commit when their triggers fire. I-DW-26 floor breaks on every mint.  
**ART-10b DeriveEffects:** `RECORD_LEAN_MANIFEST` / `SET_LEAN_TOOLCHAIN` mint LEAN_GAP per I-LM-20 / I-DW-32 when status drops.  
**ART-08d:** cycle commands mutate CycleRecord / QuarantineLock only via DeriveEffects above.

---

## 9. Traces

TRACE-3A sole write path · 3B caller boolean · 3C hard-stop (CONTROL-only effects) · 3D stale `state_head` · 3E promotion deferred · 3F unbound legacy id · 3G HARD_STOP_* with Research effect → HARD_STOP_ACTIVE · 3H validate≠effects attempt impossible under I-EFF-01.

---

## 10. Ownership (labels; auth Iter4)

Committer process; proposers supply Command only; hard-stop SET by source; CLEAR needs decision digest.

---

## 11. Alignment / non-goals

ART-06 quarantined. ART-24 Commit-only. PromotionIntent=ART-13b. Identity=ART-04c. Demotion=Iter7. Restore anchor=Iter10.
