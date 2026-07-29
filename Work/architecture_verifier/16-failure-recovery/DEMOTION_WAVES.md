# 16b — Durable Demotion Waves (Normative)

**Artifact ID:** `ART-16b`  
**Version:** `ARCH-0.3-REPAIR-ITER7.9`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-06b · ART-04c · ART-13b · ART-11b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for ART-16b. Closes `B-DEMOTION-WAVE-01` (patch 7.8: floor-break survives ATTACH while wave-listed; I-DW-33 on fingerprint-collision Claim insert). Final Sol at package gate.

## Purpose

Crash-resumable demotion. FULL CX mint SUPERSEDEs I-CX-01 hits same Commit. Floor breaks at mint for seeds **and** queued OPEN dependents (no wait for ADVANCE). Closure growth after mint gets an expansion wave. START recovery is typed. LEAN_GAP inlined here.

`ponytail:` Global APPLY fence while incomplete. HUMAN deferred.

---

## 1. Objects

```text
DemotionWorkItem
  kind                # SUPERSEDE_CLAIM | OPEN_CLAIM
  claim_digest

DemotionWave
  wave_digest = H("ART16b.DW.v4", trigger_kind, trigger_digest, seeds_sorted,
                  work_items_canonical)
  trigger_kind        # FULL_CX | PIN_SUPERSESSION | LEAN_GAP
  trigger_digest      # FULL_CX: cx_digest | CX_EXPAND composite; PIN: prior active_def_version_digest; LEAN_GAP: I-DW-32
  seeds[]
  work_items[]        # remaining ADVANCEable items only (see §3)
  cursor              # 0..len; NOT in wave_digest

DemotionFloorBreak
  claim_digest
  wave_digest
  intro_event_seq
```

**Derived:** COMPLETE iff `cursor = len(work_items)`.

**I-DW-01:** Identity immutable. Cursor only via ADVANCE (`+1`). Re-insert same `wave_digest` ⇒ `WAVE_EXISTS`.

**I-DW-25:** Live `DemotionFloorBreak` for C ⇒ DerivedProofFloor UNPROVED until **all** hold:
1. No DemotionWave with `cursor < len(work_items)` lists C in `seeds ∪ work_items.claim_digest`.
2. A successful `ATTACH_CERTIFICATION` for C whose Commit `event_seq` > `intro_event_seq` **and** (if C was wave-listed) > the event_seq that first made listing clear.
3. The CertificationRecord / `proof_evidence_digest` introduced by that ATTACH MUST be **new** — its introducing MutationEvent `event_seq` > `intro_event_seq`. Re-attaching or re-citing a pre-break CertificationRecord / evidence digest does **not** discharge the break (`FLOOR_BREAK_REPLAY`).
`ponytail:` ATTACH alone cannot restore CERTIFIED authority mid-wave; pre-wave certs cannot be replayed after clearance.

---

## 2. Seed / dependent sets (Commit-derived)

- **seeds(FULL_CX)** = I-CX-01 hit set for that CX (archived irrelevant).
- **seeds(PIN)** = Claims whose DefPin cites the superseded `active_def_version_digest`.
- **dependents** = LOGICAL|DEFINITIONAL transitive from seeds, not in seeds, maturity > OPEN and ≠ SUPERSEDED.

---

## 3. Wave mint (same Commit as trigger)

**I-DW-26 (mint floor breaks):** On every wave mint, DeriveEffects MUST upsert `DemotionFloorBreak` for each claim in `seeds ∪ {w.claim_digest for w in work_items}` (same Commit `event_seq`). ADVANCE does not re-mint breaks.

**I-DW-30 `RECORD_COUNTEREXAMPLE` FULL:** Same Commit DeriveEffects MUST:
1. Upsert Counterexample row.
2. Upsert `ResearchMaturityRecord=SUPERSEDED` for **every** seed.
3. Insert DemotionWave: `trigger_kind=FULL_CX`, `trigger_digest=cx_digest`, `seeds=seeds`, `work_items` = only `OPEN_CLAIM` for each dependent. If no dependents: `work_items=[]`, `cursor=0` ⇒ COMPLETE.
4. Apply I-DW-26.
5. Do **not** put SUPERSEDE_CLAIM items on the ADVANCE queue (already applied).

**I-DW-31 `SET_ACTIVE_DEFINITION_HEAD`:** payload `{def_id, new_active_def_version_digest}`. Let `prior = pre-state ActiveDefinitionHead.active_def_version_digest` for `def_id`. Same Commit MUST:
1. Upsert new ActiveDefinitionHead.
2. If seeds empty (no citers of `prior`) ⇒ skip mint (`ponytail:`).
3. Else insert DemotionWave `PIN_SUPERSESSION`, `trigger_digest=prior`, seeds = citers of `prior`; `work_items` = `OPEN_CLAIM` for each seed ∪ dependent needing OPEN (PIN does not SUPERSEDE); `cursor=0`; apply I-DW-26.

**START_DEMOTION_WAVE** (VERIFICATION_ORCHESTRATOR) recovery payload:
```text
{ trigger_kind, trigger_digest, seeds[]? }
```
- `FULL_CX`: `trigger_digest=cx_digest`; Commit re-derives seeds = current I-CX-01 hits; caller seeds if present must equal else `SEED_MISMATCH`. Apply I-DW-30 seed SUPERSEDEs for any not yet SUPERSEDED; mint dependent OPEN queue for remaining work; I-DW-26.
- `PIN_SUPERSESSION`: `trigger_digest=prior active_def_version_digest`; seeds = current citers not yet OPEN/SUPERSEDED; mint OPEN queue; I-DW-26.
- `LEAN_GAP`: `trigger_digest` must equal I-DW-32 composite for `(claim, pre, post)` at recovery; seeds={claim}; mint OPEN queue; I-DW-26; no SUPERSEDE.
Existing identical `wave_digest` ⇒ `WAVE_EXISTS` (no cursor reset).

**ADVANCE_DEMOTION_WAVE** `{wave_digest}`: one `OPEN_CLAIM` at cursor; if current = SUPERSEDED → no-op; else upsert OPEN. cursor += 1. (Floor already broken at mint via I-DW-26.)

**I-DW-10:** One Commit ⇒ one ADVANCE item.

**I-DW-32 `LEAN_GAP`:** Minted when DerivedLeanStatus rank drops from ≥4 (FULL/CORE) per ART-10b I-LM-20 / SET_LEAN_TOOLCHAIN.  
`trigger_digest = H("LEAN_GAP", claim_digest, pre_manifest_digest_or_⊥, post_manifest_digest_or_⊥, mint_pre_state_head_digest)`.  
seeds={claim}; work_items=`OPEN_CLAIM` for seed (maturity>OPEN ≠SUPERSEDED) ∪ LOGICAL|DEFINITIONAL dependents with maturity>OPEN ≠SUPERSEDED. No SUPERSEDE. Empty ⇒ skip mint. Apply I-DW-26.

**I-DW-33 closure expansion:** Fire on any Commit that (a) upserts `ClaimRelation` kind∈{RENAMES,EQUIVALENT_TO}, **or** (b) changes fingerprint-relevant Claim fields used by I-CX-01, **or** (c) upserts a Claim whose `claim_math_fingerprint` equals that of any current I-CX-01 hit of a live FULL CX (new digest joins closure). For each live FULL Counterexample CX, let `H = current I-CX-01 hit set`. Let `covered` = union of seeds of every COMPLETE FULL_CX DemotionWave whose `trigger_digest` is `CX.cx_digest` **or** equals `H("CX_EXPAND", CX.cx_digest, *)` for any mint head. For each `c ∈ H \ covered` that is not SUPERSEDED: DeriveEffects MUST SUPERSEDE `c` and mint a new wave `trigger_kind=FULL_CX`, `trigger_digest=H("CX_EXPAND", CX.cx_digest, mint_pre_state_head_digest)`, seeds=newly hit set (`H \ covered` at this Commit), work_items=OPEN_CLAIM dependents, I-DW-26 (same as I-DW-30 steps 2–5). Empty newly hit set ⇒ no wave.

---

## 4. Fences

**I-DW-20 / I-AP-13:** Any wave with `cursor < len(work_items)` ⇒ non-noop APPLY ⇒ `DEMOTION_WAVE_OPEN`.

**I-DW-21 / I-AP-06:** If any FULL Counterexample (archived or not) I-CX-01-hits C, non-noop APPLY on C ⇒ `CX_BLOCKS_PROMOTION` unless current maturity is SUPERSEDED **and** ∃ COMPLETE FULL_CX DemotionWave whose seeds contain C and whose `trigger_digest` is either `CX.cx_digest` or an `CX_EXPAND` digest for that CX (`H("CX_EXPAND", CX.cx_digest, *)`).

**I-DW-22:** SUPERSEDED only via I-DW-30/33/START seed writes (not APPLY).

**I-DW-23:** SUPERSEDED ⇒ DerivedProofFloor UNPROVED.

---
## 5. Audit

ART-11b freshness on maturity upserts + I-CX-01 ∩ EvidenceClosure. I-CX-02 preserved.

---

## 6. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-07b | DemotionWave; DemotionFloorBreak; I-DW-23/25 in DerivedProofFloor |
| ART-13b | I-AP-13; I-AP-06 = I-DW-21 (incl. CX_EXPAND); I-BOOL-02 exceptions |
| ART-06b | RECORD_COUNTEREXAMPLE, SET_ACTIVE_DEFINITION_HEAD, START/ADVANCE; I-BOOL-02 + ADVANCE + I-DW-30/33 SUPERSEDE; DeriveEffects I-DW-30/31/32/33 |
| ART-04c | VERIFICATION_ORCHESTRATOR → those commands |
| ART-10b | I-LM-20 invokes I-DW-32 (text authoritative here) |
| ART-12/16 | prose non-authoritative |

---

## 7. Failures / traces

`EMPTY_WAVE | WAVE_UNKNOWN | WAVE_EXISTS | WAVE_COMPLETE | DEMOTION_WAVE_OPEN | TRIGGER_MISMATCH | SEED_MISMATCH | CX_BLOCKS_PROMOTION`

```text
TRACE-7A  RECORD FULL CX → seeds SUPERSEDED + floor breaks seeds+dependents same Commit → ADVANCE* OPEN
TRACE-7B  crash mid-dependent ADVANCE → resume; dependents already UNPROVED floor
TRACE-7C  APPLY while dependents incomplete → DEMOTION_WAVE_OPEN
TRACE-7D  archive FULL CX → still CX_BLOCKS until SUPERSEDED+COMPLETE
TRACE-7E  dependent OPEN no-op if SUPERSEDED
TRACE-7F  duplicate mint → WAVE_EXISTS
TRACE-7G  after FULL mint, I-AX-01 holds on seeds immediately
TRACE-7H  RENAMES expands I-CX-01 → I-DW-33 SUPERSEDE+wave
TRACE-7I  START_DEMOTION_WAVE typed recovery; SEED_MISMATCH rejects
```
