# Writeup audit vs Wenbin (2026-07-27)

Agents: [Coverage](ef8b4198-8389-4b1c-9daf-6166f01f27d2), [Scope creep](134bed04-6a61-45c5-bc83-d2fd75535a27), [Assumptions](327ad729-7d6b-41e5-bc83-09ad118c575e), [Goal iii](d40ffd74-c518-4e6f-b279-85b7279b8f74).

## Consensus cuts (applied)

- CREDO core (`π_ε`, inverse region, decision-risk) — out of body
- CREME core (`λ`, `z*_λ`, `I_λ`/`R_λ`, Algo 1 as baseline) — out of body
- Woody HT / discrete-boundary class constraint — out of body
- Dual `Φ_idx`/`Φ_dec` and open confirmations that re-widen W2 — out
- Dual path for (iii) (recalibrate vs randomize) — W5 supersedes; body “recalibrate” historical only

## Consensus keeps (applied)

- W1 intersection stated
- W2 narrow to UQ example (1)(2) only; selected object = `θ̂(D)` only
- W3 Part I LOO stability of (2) + assumptions on `f̂,ĝ`; Part II post-hoc on top
- W4 right to replace example if more principal
- W5: PTO, no recalibration, data-randomize, structured noise / inverse opt, Tijana pointers
- Goals (i)(ii) exact Wenbin wording; (iii) W5-faithful rewrite
- July 2 methodology brainstorm section

## Residual (not in writeup; intentional)

- Missing July 2 Overleaf body — still unrecovered; H2 UQ block is stand-in
- Woody agenda — lives in overview, not this problem statement

## Post-verify fix ([Verifier](50fdbd9c-69a5-476f-9ee4-75b8026ed69e))

- Goal (iii): W5 wording only (`data-randomize`, no recalibration) — removed `/ stabilize` and method-list preload from the goal body
- Part II: removed $\tilde\theta(\mathcal{D};\xi)$ / “equivalently” (untagged broad-§2 language)
- PTO / structured noise / Tijana remain under Methodologies only
