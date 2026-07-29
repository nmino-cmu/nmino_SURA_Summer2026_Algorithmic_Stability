# Repair Iteration 3 — Authoritative State and Mutation Semantics

**ART-06b version:** `ARCH-0.3-REPAIR-ITER3.2`  
**Normative draft:** [../06-state/MUTATION_AND_AUTHORITATIVE_STATE.md](../06-state/MUTATION_AND_AUTHORITATIVE_STATE.md)  
**Depends on:** ART-07b ITER1.26 · ART-07c ITER2.7  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

---

## A. Executive repair summary

Iteration 3 defines a single logically serialized **mutation boundary** (`I.Commit`), separates **ControlState** from **ResearchState**/**DesignState**, bans caller-trusted commit booleans, linearizes **hard-stop** as ControlState commits, and requires **expected head / event_seq** stale-write checks. ART-06 ID registries and caller-boolean promotion fields are quarantined. ART-24 routes all writes through Commit. Promotion axis application remains deferred to Iteration 5 (`PromotionIntent`).

## B. Defects addressed

- No exclusive authoritative mutation path (breaker C1)  
- Caller-trusted promotion/commit booleans (partial — ban now; Intent Iter5)  
- Hard-stop without commit fencing  
- Missing ControlState vs ResearchState separation  
- Missing stale-write / current-head checks  
- ART-06/24 treating ProposeWrite / ID registries as authority  

## C. Defects explicitly deferred

| Defect | Iteration |
|--------|-----------|
| Authenticated principals / CERTIFY | 4 |
| PromotionIntent + apply axis transitions | 5 |
| Audit intent binding | 6 |
| Demotion waves | 7 |
| Lean closure | 8 |
| FSM rewrite | 9 |
| Restore trust anchor vs hard-stop | 10 |
| Model/data provenance | 11 |
| Conformance executable | 12 |
| Minimality consolidation | 13 |
| Release identity | 14 |

## D–K. Models

See ART-06b §§1–8 (stores, heads, Commit pipeline, boolean ban, hard-stop, stale-write, digest registries, evaluation record).

## L. Ownership

ART-06b §11 — labels; authenticity Iter4.

## M. Interfaces

ART-06b + ART-24: **`I.Commit` only** (public write). DeriveEffects/Reduce internal. Deprecated: ProposeWrite, ProposeCommand, public Reduce, direct HardStop.

## N. Failure taxonomy

ART-06b §8.

## O. Validation fixtures

TRACE-3A…3H (ART-06b §9).

## P. Tabletop traces

See ART-06b TRACE-3A–3F.

## Q. Legacy-artifact migration matrix

| Artifact | Status | Mutation/state refs | Migration | Prohibited uses | Later iter | Blocker |
|----------|--------|---------------------|-----------|-----------------|------------|---------|
| ART-01 | ACTIVE_PARTIAL | hop_chain_ok | redirected Commit-derived | caller boolean authority | 5 | B-PROMO-BOOL |
| ART-03 | PENDING_MIGRATION | Design/Research writes | warning + ControlState | bypass Commit; promo authority | 4/5 | B-IDENTITY |
| ART-04b | PENDING_MIGRATION | day-1 registries | Commit-only warning | direct poke | 9/13 | B-MUTATION |
| ART-05 | PENDING_MIGRATION | lattice | warning | authenticity | 4 | B-IDENTITY |
| ART-06 | QUARANTINED_LEGACY | ID registries, caller booleans | superseded by 06b | any commit authority | 5 residual | B-PROMO-BOOL |
| ART-06b | ACTIVE_NORMATIVE | mutation kernel | frozen ITER3.2 | — | — | B-PROMO-BOOL residual Iter5; B-HARDSTOP restore Iter10 |
| ART-07b/07c | ACTIVE_NORMATIVE | objects/certs | mutate via 06b | — | — | — |
| ART-08 / 08b / 08c | PENDING_MIGRATION | cycle/frontier writes; math_stable | Commit + ControlState HS warnings | bypass Commit; ResearchState HS | 9 | — |
| ART-11 | PENDING_MIGRATION | audits | warning | promote via PASS | 6 | B-AUDIT-BIND |
| ART-12 | PENDING_MIGRATION | cx register/demotion | Commit-only warning | direct mutate | 7 | B-DEMOTION |
| ART-13 / 18 / 19 | ACTIVE_PARTIAL | promotion/validation prose | booleans non-authoritative | caller *_ok | 5 | B-PROMO-BOOL |
| ART-15 | PENDING_MIGRATION | HARD_STOP_RELEASE | ControlState + Commit warning | ResearchState HS / I.HardStop | 4 | B-IDENTITY |
| ART-16/17 | PENDING_MIGRATION | restore / I.HardStop | ControlState + Commit warning | direct HS mutate | 10 | B-RECOVERY |
| ART-20 | PENDING_MIGRATION | rules 20/24/25 | redirected to 06b | caller hop_chain_ok | 5 | — |
| ART-22 | PENDING_MIGRATION | E2E trace writes | Commit warning | Frontier/registry as authority | 14 | B-RELEASE |
| ART-24 | ACTIVE_PARTIAL | interfaces | Commit-only ITER3.2 | ProposeWrite/HardStop direct | later | — |
| ART-25 | ACTIVE_NORMATIVE | pins ART-06b ITER3.2 | posture | blueprint | 14 | B-RELEASE |
| Info-flow | PENDING_MIGRATION | narrative | Commit/HS warning | ART-06 authority | 14 | — |
| ART-RBL/RIR/ASI | ACTIVE_NORMATIVE | repair plane | updated | — | — | — |

**Temporary compatibility:** Digest keys authoritative; legacy IDs alias-only if 1:1 bound (ART-06b I-REG-01).  
**Undocumented assumptions:** None intended; missing classification → QUARANTINED_LEGACY.

## R. Cross-document changes

ART-06b created; ART-06 quarantined; ART-24 Commit-centric; ART-07b mutate pointer; ART-20 rules 20/24/25; ART-03 warning; INTEGRATION_RULE precedence; IMPLEMENTATION_BLOCK phase; ARTIFACT_STATUS; BLOCKER_LEDGER.

## S. Quarantined artifacts

ART-06 (state model legacy), ART-07, ART-09 (prior).

## T. Active incompatibility warnings

ART-03, 04b, 05, 06, 08*, 11, 15, 16, 17, 20, 24 banner, info-flow.

## U. Independent review findings

| Review | Status | Evidence |
|--------|--------|----------|
| A Adversarial | **PASS** | `adversarial_review_artifacts/REPAIR_ITER3.2_REVIEW_adv.txt` |
| B State | **PASS** | `…/REPAIR_ITER3.2_REVIEW_state.txt` |
| C Minimality | **PASS** | `…/REPAIR_ITER3.2_REVIEW_min.txt` |
| D Integration | **PASS** | `…/REPAIR_ITER3.2_REVIEW_integ.txt` |

Prior waves: ITER3.0–3.1 FAIL (archived). No open Critical/High on ITER3.2.

## V. Resolution log

| Item | Resolution |
|------|------------|
| Unbound effects vs command | DeriveEffects; full Effects in MutationEvent |
| Hard-stop kind-wide bypass | CONTROL-only + zero Research/Design effects |
| Legacy HS / Frontier / booleans | Warnings + ControlState precedence; ART-06 quarantined |
| commit_busy CAS bug | Removed; logical single-committer exclusivity |
| HARD_STOP_SET release_dec | Explicitly cleared to ⊥ on SET |
| Propose/Pending/public Reduce | Removed; Commit-only |
| Migration matrix gaps | ART-01/12/13/18/19/22 + TRACE-3A…3H |

## W. Blocker ledger update

B-MUTATION-KERNEL-01 **CLOSED** (ART-06b ACTIVE). B-HARDSTOP-FENCE-01 **PARTIAL** (commit fence closed; restore interaction Iter10). B-PROMO-BOOL-01 **PARTIAL** (caller ban closed; PromotionIntent Iter5).

## X. Iteration 3 completion decision

**YES — COMPLETE.**

ART-06b `ARCH-0.3-REPAIR-ITER3.2` is `ACTIVE_NORMATIVE`. Sol reviews A–D PASS with no Critical/High.

## Y. Authorization to begin Iteration 4

**AUTHORIZED.**

Package remains **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; blueprint / implementation planning still **no**.
