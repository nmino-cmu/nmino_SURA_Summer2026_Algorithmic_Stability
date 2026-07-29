# Audit: Tradeoff UQ instance of (2) + Ass. concentration (nontrivial ĝ)

Deliverable: Concrete cost–miscoverage instance of writeup (2); hard \(\hat\theta\) = empirical quantile (non-degenerate); DKW Ass.\ conc for \((\hat f,\hat g)\); plug into Part I randomized design for goal (iii)  
Path(s): `research/formal/instance_tradeoff_uq.tex`, `research/proofs/instance_tradeoff_uq_sketch.md`, `research/experiments/instance_tradeoff_uq_demo.py`  
Date: 2026-07-27  
Auditor: subagent (4-gate)  
Ceiling: `writeup/Problem_Writeup.tex` — \(\hat\theta\) from (2); goal (iii) = data-randomize selection, **no** \(\mathcal{C}\) recalibration.

Special checks requested:
1. Is hard \(\hat\theta\) non-degenerate (varies with \(\mathcal{D}\))? Demo evidence?
2. Nontrivial \(\hat g\) — concentration rates for \((\hat f,\hat g)\) sound?
3. No CREDO/CREME creep; (iii) still fixed \(C^{(\alpha)}\)?
4. Compatible with `part_i_randomized_design` rates?

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served:
  - Selected object \(\hat\theta\) from constrained opt (2): writeup ll.50–61.
  - Fixed-\(\theta\) validity (1) as template: writeup ll.45–48.
  - Goal (iii) / no recalibration: writeup ll.78–80, Remark ll.83–87.
  - W5 data-randomize selection: writeup ll.115–116.
  - Dual to nested instance: nontrivial empirical constraint \(\hat g\) (miscoverage) + size cost \(\hat f=\theta\); closes the “add size term / non-monotone selector” substance gap flagged in `2026-07-27_instance_nested_uq_audit.md`.

- Evidence in deliverable:
  - (2\(_\mathrm{trade}\)): \(\min\{\theta:\widehat{\mathrm{miscov}}(\theta)\le\alpha_0\}\) = empirical \((1-\alpha_0)\)-quantile.
  - Prop.\ quantile: hard \(\hat\theta=s_{(k)}\) varies with \(\mathcal{D}\) (contrast nest collapse \(\theta\equiv1\)).
  - Rem.\ FV: CRC/split-conformal warrants fixed-\(\theta\) (1) only; CRC \(\hat\lambda\) not live \(\hat\theta\).
  - Cor.\ plug: RNM/soft \(\to\) Part II Infl at **fixed classical level**: \(\mathrm{Infl}\le(e^\eta-1)\alpha+\nu\); live (iii) object = randomized \(\tilde\theta\), not \(\mathcal{C}\) recalibration.
  - Demo run OK (`instance_tradeoff_uq_demo: OK`).

- Special check (1) — hard \(\hat\theta\) non-degenerate + demo:
  - **Yes.** Prop.\ quantile + continuous-\(F\) clause: \(\hat\theta\in(0,1)\) a.s.\ and non-constant in \(\mathcal{D}\).
  - Demo evidence (\(n=400\), \(\alpha_0=0.1\), 400 trials, Uniform scores): \(\theta\) mean \(0.898\) (vs \(0.9\)), range \([0.841,0.941]\), **72** distinct values (rounded 3dp); asserts \(\max<0.999\), \(\ge10\) distinct. **Not** degenerate at 1.

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: CREDO \(z\) named only as **non**-import (header, final Remark). CRC cited solely for fixed-\(\theta\) (FV)/(1); CRC \(\hat\lambda\) explicitly not the selection map. No CREME, CREAM, Woody-HT, general \(\hat S\), LASSO-PoSI.
- Special check (3) creep half: **PASS.**

- Special check (3) — (iii) still fixed \(C^{(\alpha)}\)?
  - Cor.\ plug + Rem.\ “What is not claimed”: Infl at fixed classical level; “do **not** recalibrate \(\mathcal{C}\)”; live object = randomized selection. Matches writeup (iii)/W5 and Part II Cor.\ vanish packaging. **PASS.**
  - (Demo does not re-assert Infl algebra — tex/sketch carry that claim; nested demo already checked the same formula.)

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Claim / hyp | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| i.i.d.\ calibration scores; \(s\) fixed / ⊥ \(\mathcal{D}\) | Yes (setup + sketch Ceiling) | Lem.\ conc | If \(s\) fit on same \(\mathcal{D}\), DKW does not apply — flagged. |
| \(\hat f(\theta)=\theta=f^\star\) | Def.\ fhat | Lem.\ conc (\(\|\hat f-f^\star\|_\infty=0\)) | Pathwise / trivial half of Ass.\ conc. |
| Nontrivial \(\hat g=(1-\widehat F_n)-\alpha_0\) | Def.\ ghat | Feasible set; Lem.\ conc | Empirical miscoverage; data-dependent \(\Theta_0(\mathcal{D})\). |
| DKW \(\varepsilon(n,\nu),\nu(n)=\nu\) | Lem.\ conc | Ass.\ conc for continuum \(\Theta=[0,1]\) | Classical DKW; MC demo checks shape. |
| Grid Hoeffding+union \(\varepsilon_{\mathrm{grid}}\) | Cor.\ grid | Finite \(\Theta_m\) → Part I RNM/soft | Standard; \(m\) in rate. |
| Hausdorff / conservative \(\Theta_0^\varepsilon\) | Rem.\ hausdorff | Bridge when \(\Theta_0(\mathcal{D})\neq\{g^\star\le0\}\) | Honest; Ass.\ conc parenthetical already allows Hausdorff. |
| RNM/soft knobs \(b=2\varepsilon/\eta\), \(\beta=\eta/(2\varepsilon)\) | Cor.\ plug | Feed Part I Lemmas rnm/soft | Inherited; not re-proved. |

- No smuggled Ass.\ Lip / diam for this plug (RNM/soft on grid). Note: \(\hat f(\theta)=\theta\) is linear, so Lem.\ lin-lap *could* apply on an interval/polytope; deliverable correctly stays on the finite-grid RNM/soft path already audited in Part I.

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Special check (2) — nontrivial \(\hat g\) + rates:
  - \(\|\hat g-g^\star\|_\infty=\|\widehat F_n-F\|_\infty\); DKW \(\Rightarrow\varepsilon=\sqrt{\log(2/\nu)/(2n)}\). **Sound** (same algebra as nested).
  - \(\|\hat f-f^\star\|_\infty=0\) pathwise. Joint Ass.\ conc event reduces to the \(\hat g\) half — valid and stronger than needed for Part I’s displayed Ass.\ conc (which only names \(\|\hat f-f^\star\|\) + feasible-set clause).
  - Grid Cor.: Hoeffding + union \(\Rightarrow\varepsilon_{\mathrm{grid}}=\sqrt{\log(2m/\nu)/(2n)}\). **Sound.**
  - Demo: \(\hat g\) good-event rate \(0.907\) at \(\nu=0.1\) (\(\ge1-2\nu\) and \(\ge0.85\)). Supports the concentration claim.

- Prop.\ quantile: \(\hat f=\theta\) strictly ↑ \(\Rightarrow\) leftmost feasible = \(\inf\{\theta:\widehat F_n(\theta)\ge1-\alpha_0\}=s_{(k)}\), \(k=\lceil n(1-\alpha_0)\rceil\). Correct under the stated tie-break.

- Special check (4) — Part I rate compatibility:
  - Scales \(b=2\varepsilon/\eta\), \(\beta=\eta/(2\varepsilon)\), \(\varepsilon_{\mathrm{grid}}\) match `part_i_randomized_design` Lemmas rnm/soft and Cor.\ grid usage. **Compatible.**
  - Ass.\ conc equality \(\Theta_0=\{g^\star\le0\}\) fails pathwise for empirical \(\{\hat g\le0\}\); Rem.\ hausdorff flags this and cites Ass.\ conc’s allowed Hausdorff weakening — honest, matches Part I parenthetical.
  - **Hygiene (not FAIL):** claiming conservative \(\Theta_0^\varepsilon=\{\hat g\le-\varepsilon\}\) “restores Ass.\ conc equality” overstates — inclusion \(\subseteq\{g^\star\le0\}\) is not equality, and a data-dependent \(\Theta_0^\varepsilon(\mathcal{D})\) cannot be the oracle set in Def.\ zj-stable. Correct readings that *do* feed Part I rates: (i) Hausdorff weakening as already allowed; or (ii) RNM/soft on a fixed/oracle-feasible grid with \(\|\hat f-f^\star\|=0\) (here \(\varepsilon=0\) on the objective). Packaging for (iii) remains fixed \(C^{(\alpha)}\).

- Notation: miscoverage level \(\alpha\) / nominal \(\alpha_0\) for the constraint; optimized \(\theta\)/\(\tilde\theta\) — no silent α/θ swap.

- [x] PASS
- [ ] FAIL — list:

---

## Overall
- [x] ALL PASS — may proceed
- [ ] FAIL — open fix task before next phase work

**Notes:** All four special checks pass. Hard \(\hat\theta\) is a non-degenerate empirical quantile (demo: 72 distinct values, not stuck at 1). Nontrivial \(\hat g\) concentrates at the stated DKW/grid rates; \(\hat f\) is exact. No CREDO/CREME live math; (iii) keeps fixed \(C^{(\alpha)}\). Part I \(b\)/\(\beta\)/\(\varepsilon_{\mathrm{grid}}\) plug-in is rate-compatible; Ass.\ conc equality gap is flagged with Hausdorff/conservative bridge (wording on “equality restored” is slightly loose, not rate-breaking).
