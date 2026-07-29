# ART-12-CHAR — Characterization CX Profile (Normative)

**Artifact ID:** `ART-12-CHAR`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-12 · ART-07b · ART-CRP · ART-16b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## Purpose

First-class counterexample attack profile for **characterization-only** packages (`profile=PHASE_A_CHARACTERIZATION` or claims with `chain_segment=characterization` and no MechanismInstance). Must **not** evaluate as though a perturbation mechanism / Q_ψ / stability certificate were present.

## Routing

| CRP profile / claim shape | CX profile |
|---------------------------|------------|
| `PHASE_A_CHARACTERIZATION` | **This profile** (ART-12-CHAR) |
| Characterization claims in `MIXED` without mechanism | ART-12-CHAR for those claims |
| `PHASE_B_STABILIZATION` / mechanism present | ART-12 baseline classes |
| `BRIDGE_ONLY` | ART-12 bridge-facing subset + `CX.bridge_fail` as applicable |

**I-CX-CHAR-01:** For characterization-only targets, mandatory ART-12 classes that presuppose ψ / DD-scale / bridge-to-inference (`CX.data_dep_scale`, `CX.bridge_fail` as stability→inference) are **NOT_APPLICABLE** unless a mechanism or inference-facing bridge is present on the claim.

## Characterization attack classes

Every characterization CX session MUST attempt applicable classes below (log skips with reason + HD if policy requires):

| Class ID | Attack |
|----------|--------|
| `CX.CHAR.omit_ties` | Omitted tie / non-unique optimizer cases |
| `CX.CHAR.nonunique_opt` | Non-unique argmax/argmin falsifies uniqueness claim |
| `CX.CHAR.boundary` | Boundary / knife-edge cases |
| `CX.CHAR.bad_radius` | Incorrect perturbation radius (when radius mentioned without MechanismInstance — radius-as-assumption only) |
| `CX.CHAR.wrong_norm` | Wrong norm dependence |
| `CX.CHAR.hidden_continuity` | Hidden continuity / smoothness assumptions |
| `CX.CHAR.dim_depend` | Dimension dependence ignored |
| `CX.CHAR.degen_feasible` | Degenerate feasible sets |
| `CX.CHAR.bad_compose` | Invalid composition assumptions |
| `CX.CHAR.false_necessity` | False necessity claims |
| `CX.CHAR.false_sufficiency` | False sufficiency claims |
| `CX.CHAR.adv_perturb` | Failure under adversarial perturbations of the stated regime |
| `CX.CHAR.out_of_regime` | Instability outside the claimed regime |

**Baseline minimum:** ≥1 of `{CX.CHAR.omit_ties, CX.CHAR.nonunique_opt, CX.CHAR.boundary}` always applicable for argmax/selection characterization claims.

## Outcomes

Authoritative CX still minted only via B `RECORD_COUNTEREXAMPLE` (ART-07b I-CX / ART-16b). Discovery soft search is non-authoritative.

## Fixtures

- Positive: margin condition preserves argmax → no FULL CX (`CF-CHAR-CX-OK`)  
- Negative: argmax “stability” omits ties / bad radius → FULL CX or audit FAIL path (`CF-CHAR-CX-NEG`)
