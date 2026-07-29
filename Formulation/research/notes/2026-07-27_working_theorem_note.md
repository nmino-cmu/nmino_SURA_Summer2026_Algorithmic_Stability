# Working note — Stability → post-hoc UQ (W5)

**Status:** research draft only. Does **not** edit frozen `writeup/` / `context/`.  
**Ceiling:** Wenbin (1)(2); selected object \(\hat\theta(\mathcal{D})\) only; (iii) = data-randomize selection, **no** recalibration of \(\mathcal{C}\).

## Claim

For a UQ set \(C^{(\alpha)}(X;\mathcal{D},\theta)\) with classical level \(\alpha\) fixed
(writeup~(1) arity: third slot $=\theta$; superscript $\alpha$ indexes the classical level only),
if the plug-in \(\tilde\theta(\mathcal{D})\) from constrained opt (2) is \((\eta,0,\nu)\)-stable in the ZJ sense, then
\[
\mathrm{Infl}
\;=\;
P\bigl(Y\notin C^{(\alpha)}(X;\mathcal{D},\tilde\theta)\bigr)-\alpha
\;\le\;
(e^\eta-1)\alpha+\nu,
\]
so \(\mathrm{Infl}\to 0\) as \(\eta,\nu\to 0\). Goal (iii) is answered by **randomizing the selection map**, not by changing \(\alpha\) or reshaping \(\mathcal{C}\).

## Part I — make \(\tilde\theta\) stable

**Assumptions (ledger):** concentration of \((\hat f,\hat g)\) at rate \(\varepsilon(n,\nu)\); diam / uniqueness as needed per lemma; Ass. Lip reserved (unused in current rates).

**Design (audited PASS):**
- Report-noisy-max / Lap: scale \(b=2\varepsilon/\eta\)
- Soft-argmin: temperature \(\beta=\eta/(2\varepsilon)\)

Both yield \((\eta,0,\nu)\)-stable \(\tilde\theta\). Linear \(\hat f\) / single LMO required before extreme-point Lap claims; nonlinear → soft or discretize+RNM.

**Instances of (2):**
| ID | \(\hat f\) | \(\hat g\) | Hard \(\hat\theta\) |
| --- | --- | --- | --- |
| (2_nest) | \(1-\widehat F_n\) | box | degenerate (\(=\!1\) a.s.) — live object is randomized |
| (2_trade) | \(\theta\) (cost) | \(\widehat{\mathrm{misc}}-\alpha_0\) | empirical quantile — **non-degenerate** |

DKW supplies \(\varepsilon=\sqrt{\log(2/\nu)/(2n)}\) for both.

## Part II — transfer to coverage

Set-valued ZJ Thm2 analogue under (FV)+(ST)+(OV): miscoverage \(\le e^\eta q+\tau+\nu\). Specialize \(q=\alpha\), \(\tau=0\) → Infl bound above. **Do not** replace \(\alpha\) by \(\alpha e^{-\eta}\) (that is recalibration; rejected by W5 / re-audit).

## Files

- Formal: `instance_{nested,tradeoff}_uq.tex`, `part_i_{stability,randomized_design}.tex`, `part_ii_posthoc.tex`, `chain_i_to_ii.tex`
- Proofs / Sol: sketches under `proofs/`; set-valued gap in `proofs/sol_gaps/`
- Demos: all six under `experiments/` (PASS)

## Infl(\(n\)) table ((2_trade), \(\eta=\varepsilon\), \(\nu=0.05\), \(\alpha=0.1\))

| \(n\) | \(\varepsilon\) | bound | misc MC | Infl̂ |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.136 | 0.065 | 0.123 | +0.023 |
| 400 | 0.068 | 0.057 | 0.086 | −0.015 |
| 1600 | 0.034 | 0.053 | 0.064 | −0.036 |
| 6400 | 0.017 | 0.052 | 0.056 | −0.044 |

Demo: `experiments/tradeoff_infl_n_table.py` (PASS). Bound ↓ in \(n\); MC misc ≤ \(\alpha+\)bound. With \(\eta=\varepsilon\), \(\beta=\tfrac12\) stays diffuse → conservative mean \(\tilde\theta\) (negative Infl̂) at large \(n\).

## Open

1. Mentor-facing 1-page PDF from this note (under `research/`, not `writeup/`).
2. Cosmetic: Hausdorff / \(\Theta_0^\varepsilon\) wording (tradeoff audit).
