# Repair Iteration 4 — Identity, Authority, Human Decisions, Independence

**ART-04c version:** `ARCH-0.3-REPAIR-ITER4.6`  
**Normative draft:** [../04-agents/IDENTITY_AUTHORITY_INDEPENDENCE.md](../04-agents/IDENTITY_AUTHORITY_INDEPENDENCE.md)  
**Depends on:** ART-07b · ART-07c · ART-06b  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## A. Executive summary

Authenticated Principals (genesis TrustRoot over subject materials), command auth, IndependenceAtoms with typed attestations + controller-key merge + atomic EXTEND_ATOM, constructible HumanDecisions, minimal CertificationRecord (`proof_evidence_digest` + `certifier_binding_digest`), CERTIFIED_INFORMAL via I-CERTIFY-01. ART-18 credited acts require caller-equal provenance + model_prov from binding. RESULT axis application deferred to Iteration 5.

## B–C. Addressed / deferred

Addressed: forgeable actor_id, HD non-auth, CERTIFIED unreachable, bootstrap/certify digest cycles (incl. ProofEvidence), HS release deadlock, same-controller false independence, atom extend, author substitution, cert mirrors, status pins.  
Deferred: PromotionIntent (5), audit bind (6), demotion/Lean/FSM/restore/release (7–14).

## Q. Migration matrix

| Artifact | Status | Migration | Remaining dialect conflicts | Temporary compatibility | Prohibited | Later | Blocker |
|----------|--------|-----------|----------------------------|-------------------------|------------|-------|---------|
| ART-04 | ACTIVE_PARTIAL | roster→04c | id-as-auth | warn; 04c wins | label independence | — | — |
| ART-04b | PENDING_MIGRATION | Commit+bindings | poke writes | quarantine warn | direct poke | 13 | — |
| ART-04c | ACTIVE_NORMATIVE | this iter | — | — | — | — | B-IDENTITY CLOSED |
| ART-05 | ACTIVE_PARTIAL | actor_principal_digest | free-form actor | warn | free-form actor | — | — |
| ART-06b | ACTIVE_NORMATIVE | Command auth; HS CONTROL | — | — | unauthenticated Commit | — | — |
| ART-07b | ACTIVE_NORMATIVE | floor→I-CERTIFY | — | — | — | — | — |
| ART-07c | ACTIVE_NORMATIVE | floors when CERTIFIED | — | — | — | RESULT apply | B-STATUS-COUPLE residual Iter5 |
| ART-13 | ACTIVE_PARTIAL | IndependenceAtom / certify | id≠id theater | warn | label independence | 5 | — |
| ART-15 | ACTIVE_PARTIAL | HD auth | authenticity-by-id | warn; 04c wins | ResearchState HS | — | — |
| ART-18 | ACTIVE_PARTIAL | caller-equal act pin | optional carriers | warn; I-MP-02 | unpinned credit | 11 | — |
| ART-25 | ACTIVE_NORMATIVE | repair ledger pin ITER4.6 | not blueprint clearance | status-only | cite as clearance | 14 | — |
| ART-ASI | ACTIVE_NORMATIVE | pin ART-04c ITER4.6 | — | — | stale pins | — | — |
| ART-RBL/RIR | ACTIVE_NORMATIVE | repair plane | — | — | — | — | — |

**No undocumented compatibility assumption remains:** identity/auth/HD/independence consumers follow ART-04c; ART-25 is repair posture only.

## U. Independent review findings

| Review | Status | Evidence |
|--------|--------|----------|
| A Adversarial | **PASS** | `adversarial_review_artifacts/REPAIR_ITER4.6_REVIEW_adv.txt` |
| B Correctness | **PASS** | `…/REPAIR_ITER4.6_REVIEW_corr.txt` |
| C Minimality | **PASS** | `…/REPAIR_ITER4.6_REVIEW_min.txt` |
| D Integration | **PASS** | `…/REPAIR_ITER4.6_REVIEW_integ.txt` |

Prior waves: ITER4.0–4.5 FAIL (archived). No open Critical/High on ITER4.6.

## V. Resolution log

| Item | Resolution |
|------|------------|
| TrustRoot↔principal cycle | Genesis over subject materials |
| Certification↔HD↔ProofEvidence cycle | Dec only on ATTACH; no dec in PE/CertificationRecord |
| Same-controller false independence | I-IND-05 merge + EXTEND_ATOM |
| ART-18 author substitution | I-MP-02 caller equality; model_prov from binding |
| Certification mirrors | Record = evidence + certifier binding only |

## W. Blocker ledger update

B-IDENTITY-01 **CLOSED** (ART-04c ACTIVE). B-BRIDGE-PROOF-01 **PARTIAL→improved** (CERTIFY reachable; residual dialect). B-STATUS-COUPLE-01 **PARTIAL** (CERTIFIED floor reachable; RESULT apply Iter5). B-PROMO-BOOL-01 still **PARTIAL** (caller ban closed; PromotionIntent Iter5).

## X. Iteration 4 completion decision

**YES — COMPLETE.**

ART-04c `ARCH-0.3-REPAIR-ITER4.6` is `ACTIVE_NORMATIVE`. Sol reviews A–D PASS with no Critical/High.

## Y. Authorization to begin Iteration 5

**AUTHORIZED.**

Package remains **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; blueprint / implementation planning still **no**.
