# 17b — Checkpoint / Restore Binding (Normative)

**Artifact ID:** `ART-17b`  
**Version:** `ARCH-0.3-REPAIR-ITER10.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-06b · ART-07b · ART-16b · ART-04c · ART-13b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for durable checkpoint/restore. Closes `B-RECOVERY-PREFIX-01` and `B-HARDSTOP-FENCE-01` restore leg. Supersedes ART-17 / ART-16 P2–P6 restore prose.

## Purpose

Restore cannot accept a self-presented event prefix that omits or substitutes later irreversible commits. Validate binds an independent irreversible receipt chain. Hard-stop after restore is ControlState only. Mid-wave crash resume = last CP + forward-fix of durable events through irreversible head (open waves OK; APPLY still fenced).

`ponytail:` Anchor is a property (append-only monotonic head), not a product store choice. Envelope signing / migration versioning → Iter14. Executable fixtures → Iter12.

---

## 1. Objects

```text
IrreversibleKind                      # exactly one per irreversible Commit
  FULL_CX                             # RECORD_COUNTEREXAMPLE FULL (+ I-DW-30 in same Commit)
  PIN_SUPERSESSION                    # SET_ACTIVE_DEFINITION_HEAD that mints I-DW-31
  LEAN_GAP                            # Commit that mints I-DW-32
  CX_EXPAND                           # Commit that mints I-DW-33
  DEMOTION_START                      # START_DEMOTION_WAVE that inserts a new wave
  HARD_STOP_SET
  HARD_STOP_CLEAR
  EIO_VETO                            # SET_EIO_VETO

IrreversibleReceipt
  event_seq
  event_digest          # = MutationEvent.event_digest (computed WITHOUT hashing this receipt)
  kind                  # IrreversibleKind
  receipt_digest = H("ART17b.IR.v1", event_seq, event_digest, kind)

IrreversibleSafetyLog                 # property, not a restorable table
  receipts[]                          # append-only, ordered by event_seq
  irreversible_head_seq               # max event_seq; monotonic
  head_receipt_digest                 # receipt_digest of head

CheckpointRecord
  checkpoint_id                       # immutable
  event_seq_max                       # inclusive merkle-covered end
  merkle_root
  pin_table_hash
  open_contradiction_ids[]
  gate_status_snapshot                # verify-only; hard_stop = ControlState.HardStopRecord names
  lean_manifest_ids[]
  audit_ledger_tail_id
  irreversible_head_seq_at_create
  irreversible_head_digest_at_create  # head_receipt_digest at create
  release_digest_at_create?           # ART-25b optional at seal-bound ops
  created_at
```

**I-CP-01:** Checkpoint identity immutable. `gate_status_snapshot.hard_stop` uses ART-06b names: `active`, `source`, `set_at_event_seq`, `signal_ref_digest`, `release_dec_digest` — derived verify field only; **not** restore authority.

---

## 2. Irreversible append (I-IR-01)

**I-IR-01:** At every `I.Commit` accept that matches exactly one `IrreversibleKind` above:
1. Build `research_control_design_effects`; `effects_digest = H(research_control_design_effects)` (ART-06b).  
2. Compute `event_digest` from command + effects_digest + validation (ART-06b).  
3. Construct `IrreversibleReceipt` citing that `event_digest`; include as `Effects.ir_receipt`.  
4. Atomically append receipt to IrreversibleSafetyLog + EventLog MutationEvent.  
Priority if multiple fire: `FULL_CX` > `CX_EXPAND` > `PIN_SUPERSESSION` > `LEAN_GAP` > `DEMOTION_START` > `HARD_STOP_*` > `EIO_VETO`. Missing receipt ⇒ Commit REJECT.

`ponytail:` Broader human-denial set deferred; upgrade = extend IrreversibleKind only.

**I-IR-02:** Anchor lives outside the restorable ResearchState store. A candidate event prefix alone is not an authority for the irreversible floor.

---

## 3. Merkle (I-CP-10)

1. Canonicalize each committed `MutationEvent` 0..`event_seq_max` as UTF-8 JSON with sorted keys.  
2. `leaf_i = H(canonical_event_i)`.  
3. Merkle tree pairwise `H(left||right)`; odd promote.  
4. Stored `merkle_root` MUST equal recomputed root over **only** `0..event_seq_max`.

Legacy ART-17 “`event_seq_max ≥ max_seq(FULL_REFUTE)` from prefix alone” is **non-authoritative**.

---

## 4. `I.CheckpointValidate` (I-CP-20)

**Inputs:** `checkpoint_id`, candidate committed-event prefix covering `0..N` where `N ≥ irreversible_head_seq` and `N ≥ CheckpointRecord.event_seq_max`, full `IrreversibleSafetyLog` receipt chain through current head.

### Create-time checks (when verifying a just-minted CheckpointRecord)
- `irreversible_head_seq_at_create` = live `irreversible_head_seq`
- `irreversible_head_digest_at_create` = live `head_receipt_digest`
- Merkle over `0..event_seq_max` matches

### Restore / startup checks (all required; fail-closed)

| Check | Fail code |
|-------|-----------|
| Recompute merkle over `0..event_seq_max` = stored `merkle_root` | `MERKLE_MISMATCH` |
| Candidate prefix length `N ≥ irreversible_head_seq` | `IRREVERSIBLE_PREFIX` |
| For every receipt with `event_seq ≤ irreversible_head_seq`: prefix event at that seq has `event.event_digest = receipt.event_digest` and maps to `receipt.kind` | `IRREVERSIBLE_PREFIX` |
| Events `event_seq_max+1..N` (if any) are present and contiguous (forward-fix segment) | `FORWARD_FIX_GAP` |
| After replay of `0..N`: `ControlState.hard_stop` equals snapshot hard_stop fields **only if** `N = event_seq_max`; if `N > event_seq_max`, hard_stop MUST equal ControlState derived from full replay (snapshot is tip-at-create verify only) | `HARD_STOP_SNAPSHOT_MISMATCH` |

**I-CP-22:** Incomplete DemotionWave does **not** fail validate. Mid-wave Create is allowed. APPLY remains fenced by I-DW-20 / I-AP-13.

Any fail ⇒ route **S15**; **no** `APPLY_PROMOTION` until a later validate PASS.

**I-CP-21:** Prefer forward-fix (replay CP merkle tip, then events through irreversible head) over backward rollback.

---

## 5. Restore (I-CP-30)

1. Select `CheckpointRecord`; supply durable events `0..N` with `N ≥ max(event_seq_max, irreversible_head_seq)`; run `I.CheckpointValidate`.  
2. On PASS: replay `0..N` under ART-06b; rebuild derived indexes from replayed commits only.  
3. Discard scratch / uncommitted drafts.  
4. If post-restore `ControlState.hard_stop.active=true`: ART-06b I-HS-01 — promotions blocked until `HARD_STOP_CLEAR` + ART-04c `HARD_STOP_RELEASE`. Snapshot cannot clear the stop.  
5. Open waves may be present; ADVANCE continues; APPLY blocked until COMPLETE.

**I-CP-31:** ART-16 P2/P6 and ART-17 interrupt prose that write `ResearchState.hard_stop` via `I.HardStop` are shadow/non-authoritative. Authoritative path = `HARD_STOP_SET` / `HARD_STOP_CLEAR` → ControlState.

---

## 6. Commands

- `I.CheckpointCreate` — system: mint `CheckpointRecord` at current committed tip (open waves allowed) with live irreversible head seq/digest; merkle over `0..event_seq_max`.  
- `I.CheckpointValidate` — system read-only per I-CP-20.

No maturity / floor / inference writes.

---

## 7. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-07b | CheckpointRecord; IrreversibleReceipt stubs |
| ART-06b | I-IR-01 one receipt per irreversible Commit |
| ART-16b | open-wave restore + Create allowed; APPLY fence unchanged |
| ART-16 / 17 | restore + merkle watermark prose → 17b; hard-stop → ART-06b |
| ART-24 | I.CheckpointValidate trust anchor = this artifact |
| ART-RBL | close B-RECOVERY-PREFIX-01; close B-HARDSTOP-FENCE-01 on freeze |

---

## 8. Failures / traces

`MERKLE_MISMATCH | IRREVERSIBLE_PREFIX | FORWARD_FIX_GAP | HARD_STOP_SNAPSHOT_MISMATCH | CHECKPOINT_UNKNOWN`

```text
TRACE-10A  present prefix omitting later FULL CX Commit → IRREVERSIBLE_PREFIX
TRACE-10B  restore while hard_stop.active → promote blocked until HARD_STOP_CLEAR
TRACE-10C  crash mid-wave → last CP + forward-fix through demotion mint → PASS; APPLY still DEMOTION_WAVE_OPEN
TRACE-10D  merkle tamper → MERKLE_MISMATCH → S15
TRACE-10E  substitute event at irreversible seq (digest≠receipt) → IRREVERSIBLE_PREFIX
TRACE-10F  CheckpointCreate mid-wave → allowed
```
