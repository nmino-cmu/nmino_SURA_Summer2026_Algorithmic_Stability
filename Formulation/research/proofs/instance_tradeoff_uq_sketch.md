# Proof sketch: Tradeoff UQ instance + Ass. concentration

Source: `research/formal/instance_tradeoff_uq.tex`  
Contrast: `instance_nested_uq.tex` (monotone \(\hat f\), box \(\hat g\), hard \(\hat\theta=1\)).  
Selected object: \(\hat\theta/\tilde\theta\) only. Not CREDO \(z\). No \(\mathcal{C}\) recalibration.

---

## Instance of (2_trade)

1. Same nested sets \(C_\theta(x)=\{y:s(x,y)\le\theta\}\), \(\Theta=[0,1]\).
2. **Objective:** \(\hat f(\theta)=\theta=f^\star(\theta)\) (cost ↑ with set size).
3. **Constraint:** \(\hat g(\theta)=(1-\widehat F_n(\theta))-\alpha_0\), \(g^\star=(1-F)-\alpha_0\).
   Nontrivial \(\hat g\): feasible set \(\Theta_0(\mathcal{D})=\{\theta:\text{empirical miscoverage}\le\alpha_0\}\) is data-dependent.
4. Program: \(\hat\theta\in\arg\min\{\theta:\hat g(\theta)\le 0\}\) = empirical \((1-\alpha_0)\)-quantile of scores.

**(FV):** Fixed-\(\theta\) nested indicator loss + exchangeability ⇒ writeup (1). CRC nesting = warrant only; do not import CRC \(\hat\lambda\).

**Non-degeneracy:** Continuous \(F\) with \(F^{-1}(1-\alpha_0)\in(0,1)\) ⇒ \(\hat\theta\in(0,1)\) a.s.\ and varies with \(\mathcal{D}\). Not \(\theta\equiv 1\).

---

## Prop. quantile

**Claim:** Leftmost feasible \(\hat\theta=\inf\{\theta:\widehat F_n(\theta)\ge 1-\alpha_0\}=s_{(k)}\), \(k=\lceil n(1-\alpha_0)\rceil\).

**Sketch:** \(\hat f(\theta)=\theta\) strictly increasing ⇒ unique minimizer is the left endpoint of \(\{\hat g\le 0\}\). Nested indicators: \(1-\widehat F_n\) nonincreasing ⇒ that endpoint is the empirical quantile.

---

## Lemma conc (DKW on \(\hat g\))

**Claim:** \(\varepsilon(n,\nu)=\sqrt{\log(2/\nu)/(2n)}\) ⇒ \(\|\hat g-g^\star\|_\infty\le\varepsilon\) w.p.\ \(\ge 1-\nu\); \(\|\hat f-f^\star\|_\infty=0\) always.

**Sketch:**
1. \(\hat f\equiv f^\star\).
2. \(\|\hat g-g^\star\|_\infty=\|\widehat F_n-F\|_\infty\).
3. DKW → same \(\varepsilon,\nu\) as nested instance.

**Ceiling:** Scores i.i.d.\ on the calibration fold (score map fixed / ⊥ \(\mathcal{D}\)).

---

## Remark Hausdorff / Ass. conc equality

part_i Ass. conc wants \(\Theta_0=\{g^\star\le 0\}\) pathwise on the good event. Data-dependent \(\hat g\) breaks equality.

On \(\|\hat g-g^\star\|_\infty\le\varepsilon\):
\[
\{g^\star\le-\varepsilon\}\subseteq\{\hat g\le 0\}\subseteq\{g^\star\le\varepsilon\}.
\]
Conservative \(\Theta_0^\varepsilon=\{\hat g\le-\varepsilon\}\subseteq\{g^\star\le 0\}\) restores the equality clause for design.

---

## Corollary plug → design (iii)

1. Grid \(\Theta_m\); \(\varepsilon_{\mathrm{grid}}=\sqrt{\log(2m/\nu)/(2n)}\).
2. RNM \(b=2\varepsilon/\eta\) or soft \(\beta=\eta/(2\varepsilon)\) on \(\hat f\) over empirically feasible (or conservative) grid points.
3. \((\eta,0,\nu)\)-stable \(\tilde\theta\); Infl \(\le(e^\eta-1)\alpha+\nu\) at fixed \(C^{(\alpha)}\).

Live (iii) object = randomized selection. Hard \(\hat\theta\) already non-degenerate — noise is for stability, not to fix a collapsed argmin.

---

## Status

- Ass. conc for \((\hat f,\hat g)\): **closed** (DKW on \(\hat g\); \(f\) exact).
- Hard \(\hat\theta\) non-degenerate: **yes** (empirical quantile).
- Demo: `research/experiments/instance_tradeoff_uq_demo.py`.
