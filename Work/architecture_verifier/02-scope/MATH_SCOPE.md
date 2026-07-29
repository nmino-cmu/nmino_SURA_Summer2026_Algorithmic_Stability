# 02 — Immutable Mathematical Scope

**Artifact ID:** `ART-02`  
**Owner:** Grok Design Orchestrator  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · cert/bridge transfer → ART-07c  
**Definition pin namespace:** `def.v*`

> **INCOMPATIBILITY WARNING (Iter2):** Operator-transfer / certificate-kind prose here is **non-authoritative for typing**. Bridges and certificates use ART-07c endpoints + `ENDPOINT_CONSTRUCTION`. Legacy `cert_kind` vocabulary is quarantined.

## Purpose
Version-pin every primary mathematical object. Silent edits forbidden.

## IO
**In:** proposed def edits. **Out:** pinned `def_id@version` objects; supersession links.

## Authority
Human/`SCOPE_CHANGE` for charter-touching pins; Grok maintains pin table; agents read-only on pins mid-cycle.

## Failure modes
Silent pin edit; mid-cycle def change without terminate; certificate-type synonym conflation.

## Audit rules
Every claim cites pin set; Full-System Auditor checks focus sentence + chain placement.

## Human gates
`NEIGHBOR_CHANGE`, `STABILITY_NOTION_CHANGE`, `SELECTED_OBJECT_CHANGE`, `CONTINUOUS_LAMBDA`, `DATA_DEP_*`.

## Primary objects

| Object ID | Symbol / name | Definition | Pin |
|-----------|---------------|------------|-----|
| `DEF.dataset` | \(D\) | \(D=(Z_1,\ldots,Z_n)\) | `def.v1` |
| `DEF.neighbor` | \(D\sim D'\) | Replacement adjacency: differ in exactly one observation | `def.v1` |
| `DEF.candidates` | \(\Lambda\) | \(\{\lambda_1,\ldots,\lambda_m\}\), finite, fixed independently of \(D\) | `def.v1` |
| `DEF.score` | \(F_D(\lambda)\) | Data-dependent score in \(\mathbb{R}\); vector \(F(D)\in\mathbb{R}^m\) | `def.v1` |
| `DEF.selector_unperturbed` | \(\hat\lambda(D)\) | \(\in\arg\min_{\lambda\in\Lambda} F_D(\lambda)\) | `def.v1` |
| `DEF.tie_break` | `TB` | Fixed deterministic total order on \(\Lambda\) resolving nonunique argmin | `def.v1` |
| `DEF.perturbation` | \(\xi\sim Q_\psi\) | Joint perturbation law; design object | `def.v1` |
| `DEF.selector_perturbed` | \(\tilde\lambda(D;\xi)\) | \(\in\arg\min_\lambda\{F_D(\lambda)+\xi_\lambda\}\) under `TB` | `def.v1` |
| `DEF.selected_object` | \(S_D(\lambda)\) | Object induced by candidate (model, policy index, etc.) | `def.v1` |
| `DEF.stabilized_object` | \(\tilde S(D;\xi)\) | \(S_D(\tilde\lambda(D;\xi))\) | `def.v1` |

## Selection operators (distinct IDs — no silent transfer)

| Operator ID | Meaning |
|-------------|---------|
| `OP.oracle_argmin` | Exact argmin + `TB` |
| `OP.eps_argmin` | \(\varepsilon\)-approximate argmin (requires \(\varepsilon\) pin) |
| `OP.implemented_solver` | Concrete algorithmic realization (requires error budget pin) |

Certificates bind to exactly one `OP.*`. Transfer requires `BRIDGE` with matching pins.

## Sensitivity objects

- \(\Delta_\lambda=\sup_{D\sim D'}|F_D(\lambda)-F_{D'}(\lambda)|\)
- \(\Delta_\infty=\sup_{D\sim D'}\|F(D)-F(D')\|_\infty\)
- \(K=\{F(D)-F(D'):D\sim D'\}\)

## Utility notions (must not be conflated)

- Score loss: \(L_{\mathrm{score}}=F_D(\tilde\lambda)-F_D(\hat\lambda)\)
- Policy loss: \(L_{\mathrm{policy}}=V_D(\pi_{\tilde\lambda,D})-V_D(\pi_{\hat\lambda,D})\)

## Constrained-optimization extension (narrow)

**In-scope:** same finite-argmin template with feasibility bit or penalty inside \(F_D(\lambda)\).  
**Out-of-scope / quarantine `CONSTRAINED-EXT-SEP`:** general constraint geometry, dual learning, path methods, infinite feasible sets, active-set theory as primary object.

## Defaults (human-gated to change)

| Item | Default |
|------|---------|
| \(\psi\) data dependence | Data-independent unless calibration is an explicit sub-mechanism |
| \(\Lambda\) generation | Fixed a priori (no adaptive candidate generation) |
| Experiment primary evidence | Analytic finite toys; Monte Carlo auxiliary only |

## Invariants

- Definition change → new pin → automatic demotion wave on dependents
- Mid-cycle definition edit is an **invalid transition** (see ART-08)

## Human gates

Change of neighbor relation, primary stability notion, selected-object type, data-dependent \(\psi\), move to continuous \(\Lambda\), data-dependent feasible sets.
