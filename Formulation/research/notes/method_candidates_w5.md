# W5 method candidates (answer (iii) only)

Not problem expansion. Map mechanisms → randomized selection of θ̂ so (1) holds without recalibrating C.

| candidate | Wenbin phrase | mechanism sketch | acts on | must NOT do |
|-----------|---------------|------------------|---------|-------------|
| PTO-style data-driven policy | “Data-driven policy (e.g., PTO)” | selection of θ via predict-then-optimize / preference over data-driven scores | selection map A | recalibrate C |
| data-randomize | “data-randomize to achieve validity guarantee” | inject ξ into A → θ̃(D;ξ) with exchangeability / stability certificate | selection | touch C’s construction |
| structured noise + inverse opt | “structured noise, depends on inverse optimization” | non-isotropic perturbation guided by inverse-opt geometry of (2) | f̂/ĝ or argmin | isotropic noise without analysis; C recalibration |
| Tijana line | “Winner’s Curse, Algorithm Stability” | import stability→PSI patterns; winner’s-curse defenses | theory template | redefine problem |

Fill concrete θ̃ forms after literature Phase 0 digests land.

## Locked from digests (2026-07-27)

1. **Primary (iii) template:** Zrnic–Jordan randomized constrained opt (Laplace / report-noisy-max / noisy Frank–Wolfe) → $(\eta,\tau,\nu)$-stable $\tilde\theta$; drive $\eta\to 0$; keep fixed-$\theta$ map of $\mathcal{C}$.
2. **Not (iii):** $e^\eta$ inflation of classical level / zoom CI projection / CREME split re-estimation of $\mathcal{C}$.
3. **CRC:** justifies assumption (1) only when $\theta$ prespecified.
4. **Part I bridge:** LOO movement of deterministic (2) ≠ Def.2; both tracked.

## Structured selection-noise candidates (from inverse-opt pattern)

| form | notes |
|------|-------|
| noisy objective $\hat f+\langle\xi,\theta\rangle$ | $\xi$ on sensitivity subspace |
| noisy constraints $\hat g+\xi\le 0$ | active-set normals |
| soft near-minimizer sample | $\varepsilon$-thicken argmin of (2) |
| structured bootstrap of $(\hat f,\hat g)$ | reweight $D$ then re-solve |
| inverse-sensitivity pushforward | $\xi\sim J^\dagger u$ |
| isotropic Gaussian | ablation only |
