# Repair Iteration 7 — Durable Demotion Waves

**ART-16b version:** `ARCH-0.3-REPAIR-ITER7.5`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Normative draft:** [../16-failure-recovery/DEMOTION_WAVES.md](../16-failure-recovery/DEMOTION_WAVES.md)  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## A. Executive summary

FULL CX mint SUPERSEDEs seeds in the same Commit; dependent OPEN via durable ADVANCE cursor; incomplete waves fence APPLY; archive ≠ ignore; SUPERSEDED ⇒ floor UNPROVED.

## B–C. Addressed / deferred

Addressed: B-DEMOTION-WAVE-01.  
Deferred: Lean (8); FSM S14 (9); restore (10); HUMAN trigger.

## U. Independent review

| Review | Status | Evidence |
|--------|--------|----------|
| Combined Sol A–D | **PASS** | `adversarial_review_artifacts/REPAIR_ITER7.5_REVIEW_combined.txt` |

## W. Blocker ledger

B-DEMOTION-WAVE-01 **CLOSED**. B-LEAN-CLOSURE-01 remains **OPEN** (Iter8).

## X. Completion

**YES — COMPLETE.** ART-16b `ARCH-0.3-REPAIR-ITER7.5` is `ACTIVE_NORMATIVE`.

## Y. Authorization Iteration 8

**AUTHORIZED.** Package **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; no blueprint / implementation planning.

## ITER7.6 (post-freeze patch; Sol deferred)
Closes late Sol 7.5 FAIL residuals: DemotionFloorBreak on OPEN/SUPERSEDE (I-DW-25); I-DW-33 CX closure expansion on RENAMES/EQUIVALENT_TO; typed START_DEMOTION_WAVE payload. Final Sol at package gate.

## ITER7.7
Mint-time I-DW-26 DemotionFloorBreak for seeds∪work_items (closes pre-ADVANCE CERTIFIED hole); inlined I-DW-32; I-DW-33 covered-set includes CX_EXPAND; I-BOOL-02/I-AP-06 wired for I-DW-33. Sol deferred to final package gate.

## ITER7.8
I-DW-25 requires wave-unlist before ATTACH can restore floor; I-DW-33 fires on fingerprint-collision Claim insert.

## Freeze
ITER7.8 internal A–D **PASS** (`FREEZE_OK`). Sol deferred to final package gate.
