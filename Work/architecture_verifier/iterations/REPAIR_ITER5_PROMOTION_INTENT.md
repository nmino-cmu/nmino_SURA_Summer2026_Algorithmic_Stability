# Repair Iteration 5 — Promotion Intent (Proof-Carrying Axis Application)

**ART-13b version:** `ARCH-0.3-REPAIR-ITER5.6`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Normative draft:** [../13-proof-review/PROMOTION_INTENT.md](../13-proof-review/PROMOTION_INTENT.md)  
**Depends on:** ART-07b · ART-07c · ART-06b · ART-04c · ART-15 · ART-01 · ART-14  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## A. Executive summary

Self-contained proof-carrying promotion: genesis PromotionPolicy registry; PromotionIntent; APPLY_PROMOTION with Commit-recomputed floor, exact CertificationRecord basis, RequiredGates, EffectiveDecision (log-derived), intent-bound EioAssessment ALLOW, generation-bound OVERRIDE_EIO. Caller `*_ok` forbidden.

## B–C. Addressed / deferred

Addressed: B-PROMO-BOOL-01 (caller predicates); B-STATUS-COUPLE RESULT apply; unbound basis; demotion-via-APPLY; gate/EIO fail-open; self-containment.  
Deferred: audit↔intent bind (6), demotion (7), Lean (8), FSM S09 (9), restore (10), release (14).

## Q. Migration matrix

See prior ITER5.6 matrix rows (unchanged at freeze). ART-13b → ACTIVE_NORMATIVE.

## U. Independent review findings

| Review | Status | Evidence |
|--------|--------|----------|
| A Adversarial | **PASS** | `adversarial_review_artifacts/REPAIR_ITER5.6_REVIEW_adv.txt` |
| B Correctness | **PASS** | `…/REPAIR_ITER5.6_REVIEW_corr.txt` |
| C Minimality | **PASS** | `…/REPAIR_ITER5.6_REVIEW_min.txt` |
| D Integration | **PASS** | `…/REPAIR_ITER5.6_REVIEW_integ.txt` |

Prior waves ITER5.0–5.5 FAIL archived. No open Critical/High on ITER5.6.

## W. Blocker ledger update

B-PROMO-BOOL-01 **CLOSED**. B-STATUS-COUPLE-01 **CLOSED** (RESULT requires CERTIFIED at APPLY). B-AUDIT-BIND-01 remains **OPEN** (Iter6).

## X. Iteration 5 completion decision

**YES — COMPLETE.** ART-13b `ARCH-0.3-REPAIR-ITER5.6` is `ACTIVE_NORMATIVE`.

## Y. Authorization to begin Iteration 6

**AUTHORIZED.** Package **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; blueprint / implementation planning still **no**.
