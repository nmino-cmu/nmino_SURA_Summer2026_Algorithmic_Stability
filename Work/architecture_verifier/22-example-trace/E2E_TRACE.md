# 22 — End-to-End Example Trace

**Artifact ID:** `ART-22`  
**Version:** `ARCH-0.3`  
**Nature:** Architecture validation trace (not a proved theorem)  
**Normative status:** `PENDING_MIGRATION` · **Responsible iteration:** 14 (release-bound traces)

> **INCOMPATIBILITY WARNING:** Legacy ID-native / pre-ART-07c hops. Not release evidence. Prefer Iteration 2 TRACE-2A…2F and Iteration 3 TRACE-3A…3H. **`I.Frontier` / registry writes in this trace are non-authoritative** — apply only via ART-06b `I.Commit`.

## Scenario

Homogeneous Laplace noisy argmin (Zrnic–Jordan-style baseline) for finite \(\Lambda=\{1,2\}\).

## Trace

| Step | State | Artifact actions |
|------|-------|------------------|
| 1 | S01 | Load pins `def.v1`; neighbor = replacement; `loop_tag=SIMULATION` |
| 2 | S02 | Lock `q_id=q1` via `I.Frontier`; write `quarantine[q1]={chain_link=stability, class=IN_CHAIN, classifier_role=Frontier_Scheduler, classifier_id=FS1, frozen_at_s02=true}` (≠ Orchestrator); question: Does i.i.d. Lap(b) yield APPROX_INDISTINGUISHABILITY for INDEX under OP.oracle_argmin? |
| 3 | S04 | Toy ExampleCard: `quarantine_q_id=q1`; `chain_link_intent=stability`; m=2, F(D)=(0, g), g>0 |
| 4 | S03 | Conjecture C1; FalsifierCard: `refutation_type=bound_violation`; `witness_template`; `mandatory_attack_classes=[CX.vanish_gap, CX.nonunique_min, CX.bridge_fail]`; `chain_segment=stability` (= quarantine.chain_link = intent) |
| 5 | S05 | Baseline: unperturbed argmin unstable when gap < shift |
| 6 | S06 | Mechanism M_homog: iid Laplace; `mechanism_family_checklist_ok` → KNOWN_MECHANISM cites RNM / Zrnic–Jordan |
| 7 | S09 | Pre-proof attack: register `cx_id`s for vanish_gap / nonunique_min / bridge_fail; `attack_record_ids[]` ≡ those `cx_id`s; `attack_log_id=log.s09.1`; constructs match `witness_template` |
| 8 | S07 | Proof attempt sketch: Laplace density ratio ≤ e^{|x|/b}; calibrate b to Δ |
| 9 | S08 | UtilityCompat `uc1`: `link_kind=PROVED_INEQUALITY` for SCORE_REGRET_EMP vs hat_lambda — **not** HEURISTIC; CI_WIDTH noted as cost |
| 10 | S09 | Additional attacks as needed (same bind rules) |
| 11 | S10 | Audit PASS for local stability only; `disconfirm_log_id=dl1` (producer ≠ auditor); Q16/`hop_chain_ok` YES; Q11 bridge = BRIDGE_OPEN → inference **not** claimed; `I.BullshitLinter` B1–B5; roles via `I.RoleCeiling` |
| 12 | S11 | LEAN only if math_stable (≥2 attack+audit or MATH_STABLE_ACK); else skip |
| 13 | S12 | Label CONJECTURE or PARTIAL_RESULT — not PROVED_ON_PAPER without certifier + audit; not novelty (`NOVELTY_TRACK_ACK` N/A at KNOWN_MECHANISM) |
| 14 | S13–S14 | Commit; next question via scheduler; checkpoint via `I.CheckpointValidate` |

**Banner:** This trace is `design_validation_only` / `loop_tag=SIMULATION`. It must not write `ResearchState` until `RESEARCH_EXECUTION_START`. SIMULATION excluded from `dep_closure_ok`.

## Explicit non-claims in this trace

- No post-selection coverage theorem
- No DP≡stability
- No policy stability from index stability
- No Lean verified
- No confirmed novelty
- No HEURISTIC UtilityCompat used for promotion

## Literature boundary step (mandatory in real cycles; shown here)

| Step | Action |
|------|--------|
| L1 | Prior-art packet: Report Noisy Max / Zrnic–Jordan noisy winner / Laplace RNM |
| L2 | Novelty ladder label: `KNOWN_MECHANISM` — **not** PLAUSIBLE_NOVELTY |
| L3 | `mechanism_family_checklist_ok` for `iid_laplace` before S06 closes |
| L4 | Synthesis must not describe this cycle as a “contribution”; only as baseline validation |
