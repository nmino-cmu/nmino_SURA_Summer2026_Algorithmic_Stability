# Question-Selection Policy (System A ownership)

**Artifact ID:** `ART-08b`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Owner:** Frontier Scheduler (System A only)  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Home:** `architecture-discovery/` (DUAL.1 M4)

> **DUAL.1:** Selects next question for CRP packaging. Does **not** authorize B `LOCK_CYCLE` / ResearchState quarantine writes. B intake = ART-CRP; B bind = ART-08d.  
> **INCOMPATIBILITY WARNING:** Scheduler “commits” are non-authoritative on B. A-local frontier state only.

## Purpose
Select the next research question to maximize chain information; enforce quarantine at S02 lock.

## IO
**In:** `open_questions`. **Out:** atomic `S02` lock + `quarantine[q_id]` via `I.Frontier`.

## Authority
Frontier Scheduler alone commits selection; Orchestrator must not mint-and-select without scheduler commit.

## Failure modes
Easy-only selection; narrative OOS without registry; missing `chain_link`/classifier on S02; dual frontier writers; S02/S14 commit while `hard_stop.active`.

## Audit rules
`I.Frontier` output must include full quarantine tuple; ART-01 `admissible_experiment` checked at lock; reject scheduler commits when `ResearchState.hard_stop.active=true`.

## Human gates
Anti-easy override; `SCOPE_CHANGE` for `BRIDGE_CANDIDATE`; weight revision; `HARD_STOP_RELEASE` before resume after freeze.

## Principle

Choose the next mathematical question to maximize expected information along the main chain — not ease, not novelty theater, not volume.

## Score components (normalized weights fixed until human revises)

| Factor | Direction | Notes |
|--------|-----------|-------|
| Main-chain relevance | + | Must map to a chain link |
| Unblocks proof bottleneck | + | Dependency fan-in |
| Counterexample value | + | Likely to refute or constrain |
| Tractability | + | But capped — see anti-easy |
| Lean formalizability (near-term) | + | After math stable |
| Integration impact | + | |
| Novelty risk | − | High novelty → deprioritize or escalate |
| Accumulated failure fingerprint match | − | Avoid rehash unless new angle |
| Easy-only indicator | − | High tractability + low chain relevance |

## Anti-easy-question rule

If `tractability` is top-quartile and `main_chain_relevance` is bottom-half → **reject** as next question unless human overrides.

## Default scoring function

```text
score(q) =
  + 3.0 * main_chain_relevance
  + 2.5 * unblocks_bottleneck
  + 2.0 * counterexample_value
  + 1.0 * min(tractability, 0.7)      # cap ease contribution
  + 1.0 * lean_near_term
  + 1.5 * integration_impact
  - 2.0 * novelty_risk
  - 2.5 * failure_fingerprint_match
  - 3.0 * easy_only_indicator         # 1 if anti-easy triggers

Select argmax score among open_questions with score > 0; else escalate stagnation.
```

Weights are defaults until human revises.

## Refutation reward

Verified REFUTED / FULL_REFUTE outcomes update frontier value of similar questions **upward** (information), not downward as “failure.”

## Single scheduler

`frontier` is a **derived prioritized view** of `open_questions`. No second writable priority list.

## Supply / selection split

- **Question supply:** specialists may propose candidate `q_id`s into `open_questions` (append-only proposals)
- **Question selection:** Frontier Scheduler alone commits the next locked `S02` question via atomic frontier commit transaction
- Research Orchestrator must not both mint and select the same question without scheduler commit

## Stagnation controls

- N cycles without promotion or verified refutation → emit stagnation report; force attack on oldest PARTIAL_RESULT
- Novelty pressure dampener: consecutive “plausible novelty” labels without literature packet → block

## Out of scope questions

Topics that must not enter as `IN_CHAIN` without `SCOPE_CHANGE`: general DP theory, general SI, continuous Λ, unconstrained optimization geometry, empirical benchmarking programs.

**Auto-quarantine (hard):** Frontier Scheduler (or Research Scope) **writes** `quarantine[q_id]` with `class ∈ {ADJACENT, REFUSED}`, `chain_link`, `classifier_role`, `classifier_id` before any `S02` attempt on OOS topics. Narrative lists without a registry row are invalid.

**S02 positive quarantine (hard):** Every S02 lock — including `IN_CHAIN` / `BRIDGE_CANDIDATE` — **must** write `quarantine[q_id]` with full ART-06 schema `{chain_link, class, classifier_role, classifier_id, frozen_at_s02=true}` via `I.Frontier`. Constraints: ART-01 (`IN_CHAIN` ⇒ classifier ≠ Orchestrator, `chain_link ≠ bridge`); `BRIDGE_CANDIDATE` ⇒ `SCOPE_CHANGE`/`exc_id`. Post-lock edits invalid until cycle end.
