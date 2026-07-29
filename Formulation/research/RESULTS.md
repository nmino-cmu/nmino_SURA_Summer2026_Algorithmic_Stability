# Working results (research)

**Freeze:** `writeup/` + `context/` unchanged. Scope = Wenbin UQ (1)(2), W5-(iii).  
**Deadline:** Jul 30 — see `notes/2026-07-30_triage.md`.

## Theorem chain (corrected Jul 27)

1. **(2_trade)** primary live instance: \(\hat f=\theta\), \(\hat g=\widehat{\mathrm{misc}}-\alpha_0\); hard \(\hat\theta=\) empiric quantile.  
   Use conservative \(\Theta_0^\varepsilon=\{\hat g\le-\varepsilon\}\) for RNM/soft so (OV) holds.  
   `(2_nest)` = DKW toy; hard argmin degenerate.

2. **Design:** RNM \(b=2\varepsilon/\eta\) / soft \(\beta=\eta/(2\varepsilon)\) on shared feasible support ⇒ \((\eta,0,\nu)\)-stable.  
   Ass.conc = Hausdorff primary; exact \(\Theta_0=\{g^\star\le0\}\) only for box-\(\hat g\).

3. **Transfer:** \(P(Y\notin C^{(q)}(X;D,\hat\theta))\le e^\eta q+\tau+\nu\) under (ST)+(OV).  
   \(C^{(q)}\) = writeup \(\mathcal{C}\) at classical level \(q\); third slot still \(\theta\).

4. **(iii)/W5:** fixed classical \(\alpha\); \(\mathrm{Infl}\le(e^\eta-1)\alpha+\nu\to0\) with selection inside \(\Theta_{\mathrm{val}}\).  
   Not \(C^{(\alpha e^{-\eta})}\).

5. **Chain:** `formal/chain_i_to_ii.tex` (requires \(\Theta_{\mathrm{val}}\) support).

## Notation (must use)
Dictionary: `notes/notation_quarantine.md`. Do not put \(\alpha\) in the third slot of \(\mathcal{C}\).  
\(\alpha_0\) = tradeoff constraint only; set \(=\alpha\) for Part II numerics by choice.

## Correctness status (Jul 27 swarm)
- [Notation](c4f2ee9b-fda8-4e02-8eb4-07298a511f73) ~82% mentor-safe symbols after fixes  
- [Math](1e2d15e1-482f-4567-a814-46086117d190) critical (OV)/feasible-support holes **fixed**  
- Demos: **7/7 PASS** (fresh)

## Honest gaps (say out loud)
- W3 LOO of deterministic (2): stub + \(O_P(n^{-1})\) quantile note — not a full Part I theorem product  
- \(\eta\to0\) buys Infl by softening selection (utility cost)  
- PTO / inverse-opt structured noise: not built

## Mentor packet
`notes/2026-07-27_mentor_onepager.pdf` + this RESULTS + triage note.
