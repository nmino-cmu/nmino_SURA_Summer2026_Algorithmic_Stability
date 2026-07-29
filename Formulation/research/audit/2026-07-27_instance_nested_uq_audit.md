# Audit: Nested UQ instance of (2) + Ass. concentration rates

Deliverable: Concrete instance of writeup (2) for nested score-threshold UQ; explicit DKW \(\varepsilon(n),\nu(n)\) for Ass.\ concentration; plug into Part I randomized design for goal (iii)  
Path(s): `research/formal/instance_nested_uq.tex`, `research/proofs/instance_nested_uq_sketch.md`, `research/experiments/instance_nested_uq_demo.py`  
Date: 2026-07-27  
Auditor: subagent (4-gate)  
Ceiling: `writeup/Problem_Writeup.tex` — \(\hat\theta\) from (2); goal (iii) = data-randomize selection, **no** \(\mathcal{C}\) recalibration.

Special checks requested:
1. Deterministic \(\arg\min=\theta=1\) a.s.\ — flagged honestly? Does randomized design still give a non-vacuous (2) for (iii)?
2. \(\varepsilon(n,\nu)=\sqrt{\log(2/\nu)/(2n)}\) DKW — math OK?
3. No CREDO/CREME problem expansion; CRC only for (FV)?
4. Infl demo uses fixed \(C^{(\alpha)}\), not level recalibration?

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served:
  - Selected object \(\hat\theta\) from constrained opt (2): writeup ll.50–61.
  - Fixed-\(\theta\) validity (1) as template: writeup ll.45–48.
  - Goal (iii) / no recalibration: writeup ll.78–80, Remark ll.83–87.
  - W5 data-randomize selection: writeup ll.115–116.
  - Closes Part I Ass.\ conc gap deferred in `part_i_randomized_design` audit (concrete \(\varepsilon,\nu\) for this \(\hat f,\hat g\)).

- Evidence in deliverable:
  - Instance is writeup (2) with nested \(C_\theta\), \(\hat f=\) empirical miscoverage, box \(\hat g\).
  - Remark FV: CRC nesting warrants fixed-\(\theta\) (1) only.
  - Cor.\ plug: RNM/soft rates \(\to\) Part II Infl at **fixed classical level of \(\mathcal{C}\)**: \(\mathrm{Infl}\le(e^\eta-1)\alpha+\nu\).
  - Sketch + demo ceiling match: randomize/concentrate selection scores only; do not touch \(C\)'s fixed-\(\theta\) map.
  - Demo run OK (`instance_nested_uq_demo: OK`; good_rate \(0.943\) at \(\nu=0.1\)).

- Special check (1) — deterministic collapse vs randomized (iii):
  - **Honestly flagged:** tex note after (2\(_\mathrm{nest}\)): \(\hat f\) nonincreasing \(\Rightarrow\) measurable tie-break yields \(\hat\theta=1\) a.s.; Remark “What is not claimed” denies interesting deterministic radius selection. Sketch §Instance item 4 matches.
  - **Randomized (iii) still non-vacuous as packaging:** live object is RNM-on-grid / soft-argmin on \(\hat f|_{\Theta_m}\) (or soft w.r.t.\ reference \(\mu\) on \([0,1]\)). Finite \(\eta\) (finite \(\beta\) / positive Laplace scale) yields a non-degenerate selection law; Ass.\ conc + Part I Lemmas rnm/soft give \((\eta,0,\nu)\)-stability; Infl bound at fixed \(C^{(\alpha)}\) is \(\le(e^\eta-1)\alpha+\nu\), which \(\to\nu\) as \(\eta\downarrow0\) (then \(\nu\downarrow0\) with \(n\)). That is exactly the writeup-(iii)/W5 bridge.
  - **Scope note (not a FAIL):** with box \(\hat g\) only, there is still no coverage–size tradeoff in the objective — soft/RNM prefer large \(\theta\). Deliverable does not claim otherwise; non-vacuous here means the **stability→Infl** chain, not a substantive radius-selector design problem.

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: CREDO \(z\) and CREME named only as **non**-imports (header, abstract, Rem.\ FV, final Remark). CRC cited solely to warrant fixed-\(\theta\) (FV)/(1) (Angelopoulos CRC Thm.~1 / indicator loss); CRC \(\hat\lambda\) explicitly not the live \(\hat\theta\). No CREAM, Woody-HT, general \(\hat S\), LASSO-PoSI.
- Special check (3): **PASS.** CRC = (FV) warrant only; no problem expansion.

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Claim / hyp | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| i.i.d.\ calibration scores; \(s\) fixed w.r.t.\ \(\mathcal{D}\) | Yes (setup + sketch Ceiling) | Lemma dkw-conc | If \(s\) fit on same \(\mathcal{D}\), lemma does not apply — flagged. |
| Box \(\hat g\); \(\Theta_0=\{g^\star\le0\}\) a.s. | Def.\ ghat | Ass.\ conc feasible-set half free | Trivial / pathwise — honest. |
| DKW \(\varepsilon(n,\nu),\nu(n)=\nu\) | Lem.\ dkw-conc | Ass.\ conc for continuum \(\Theta=[0,1]\) | Classical DKW; MC demo checks shape. |
| Grid Hoeffding+union \(\varepsilon_{\mathrm{grid}}\) | Cor.\ grid | Finite \(\Theta_m\) path | Standard; \(m\) explicit in rate. |
| RNM/soft design knobs \(b=2\varepsilon/\eta\), \(\beta=\eta/(2\varepsilon)\) | Cor.\ plug | Feed Part I Lemmas rnm/soft | Inherited; not re-proved here. |

- No smuggled Ass.\ Lip / diam for this instance (RNM/soft path only). Ass.\ uniq deferred to Part I noise lemmas as appropriate.

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- \(\hat f(\theta)=1-\widehat F_n(\theta)\), \(f^\star=1-F\) \(\Rightarrow\|\hat f-f^\star\|_\infty=\|\widehat F_n-F\|_\infty\). Matches Ass.\ conc \(\|\cdot\|_{\infty,\Theta_0}\) with \(\Theta_0=[0,1]\).
- Special check (2) — DKW algebra:
  \[
  \mathbb{P}\{\|\widehat F_n-F\|_\infty>\varepsilon\}\le 2e^{-2n\varepsilon^2}=\nu
  \;\Rightarrow\;
  \varepsilon=\sqrt{\frac{\log(2/\nu)}{2n}}.
  \]
  **Sound** (Massart form of DKW). \(\nu(n)=\nu\) is a valid Ass.\ conc instantiation; Cor.\ plug correctly notes sending \(\nu\downarrow0\) with \(n\) separately from \(\eta\downarrow0\).
- Grid Cor.: per-coordinate Hoeffding on \([0,1]\) indicators + union bound \(\Rightarrow\varepsilon_{\mathrm{grid}}=\sqrt{\log(2m/\nu)/(2n)}\). **Sound.**
- Special check (4) — Infl demo: `infl(eta)=(exp(eta)-1)*alpha+nu` with **fixed** \(\alpha,\nu\); asserts shrink as \(\eta\downarrow0\) and approach \(\nu\). No \(C^{(\alpha e^{-\eta})}\) / level recalibration. Docstring ceiling matches Part II Cor.\ vanish packaging. **PASS.**
- Notation: miscoverage level stays \(\alpha\); optimized parameter is \(\theta\) / \(\tilde\theta\) — no silent α/θ swap.
- Deterministic \(\arg\min\): flat on \([\max_i s_i,1]\) when scores \(\le1\); “measurable tie-break \(\Rightarrow\hat\theta=1\) a.s.” is the correct statement (not unique minimizer).

- [x] PASS
- [ ] FAIL — list:

---

## Overall
- [x] ALL PASS — may proceed
- [ ] FAIL — open fix task before next phase work

**Notes:** All four special checks pass. Deterministic (2\(_\mathrm{nest}\)) collapse to \(\theta=1\) is flagged honestly; randomized design remains a non-vacuous **(iii)** object via Ass.\ conc \(\to\) \((\eta,0,\nu)\)-stability \(\to\) fixed-\(C^{(\alpha)}\) Infl. DKW rate correct. No CREDO/CREME live math; CRC only for (FV). Demo Infl uses fixed \(\alpha\), not level recalibration. Optional future substance (not required to proceed): add a size/complexity term to \(\hat f\) or \(\hat g\) if a non-monotone radius-selector instance is desired.
