# Proof sketch: Part I randomized design lemmas

Source: `research/formal/part_i_randomized_design.tex`  
Template: Zrnic–Jordan Defs. 1–2, Ex. 1, Prop. 2/4 (design only) — remapped to noisy (2), not LASSO-PoSI.  
Selected object: \(\tilde\theta\) only. Goal (iii): small \(\eta\).

---

## Shared setup

1. Oracle program \((f^\star,g^\star)\) depends on law \(P\) only (Ass. conc).
2. Good event \(E=\{\|\hat f-f^\star\|_{\infty,\Theta_0}\le\varepsilon,\;\Theta_0=\{g^\star\le 0\}\}\) has \(\mathbb{P}(E)\ge 1-\nu\).
3. On \(E^c\), charge failure mass to \(\nu\) in Def. 2; on \(E\), prove \((\eta,0)\)-indistinguishability vs oracle \(A_0\) (same noise, \(f^\star\)).
4. Uniqueness / tie-break (Ass. uniq) makes \(A(\mathcal{D})\) a r.v.; diameter/Lipschitz used only where stated.

---

## Lemma rnm (finite \(\Theta_0\))

**Claim:** \(\tilde\theta=\arg\min_\theta(\hat f(\theta)-\xi_\theta)\), \(\xi_\theta\sim\mathrm{Lap}(b)\), \(b=2\varepsilon/\eta\) \(\Rightarrow\) \((\eta,0,\nu)\)-stable.

**Sketch:**
1. Fix realized scores on \(E\): \(|\hat f(\theta)-f^\star(\theta)|\le\varepsilon\) for all finite \(\theta\in\Theta_0\).
2. Classic report-noisy-max / min: if two score vectors differ by at most \(\varepsilon\) in \(\|\cdot\|_\infty\), Lap scale \(b=2\varepsilon/\eta\) yields max-divergence \(\le\eta\) between the discrete selection laws (same argument as DP-RNM; ZJ Ex. 1 / Prop. 4).
3. Oracle \(A_0\): same \(\xi\), scores \(-f^\star\). Then on \(E\), \(A(\mathcal{D})\approx_{\eta,0} A_0\).
4. Integrate: \(\mathbb{P}(E)\ge 1-\nu\) \(\Rightarrow\) \((\eta,0,\nu)\)-stability (ZJ Def. 2).

**Gap / ceiling:** Ass. conc must supply \(\varepsilon,\nu\) for the concrete \(\hat f\) (empirical process on \(\Theta_0\)). Not claimed here.

---

## Lemma lin-lap (polytope / one LMO)

**Claim:** Linear noisy objective over a polytope \(\Leftrightarrow\) RNM on extreme points \(\Rightarrow\) same \((\eta,0,\nu)\) with \(b=2\varepsilon/\eta\).

**Sketch:**
1. For linear (or FW-LMO) objective over a polytope, minimizers are extreme points a.s. under continuous noise.
2. Induced scores on \(v\in\mathrm{ext}(\Theta_0)\) differ by \(\le\varepsilon\) on \(E\) when \(\|\hat f-f^\star\|_\infty\le\varepsilon\).
3. Reduce to Lemma rnm on \(\mathrm{ext}(\Theta_0)\).
4. Multi-step: compose \(k\) such LMOs as ZJ Prop. 2 — basic \((k\eta_0,0,k\nu_0)\) or advanced \((\tfrac12 k\eta_0^2+\sqrt{2k\log(1/\delta)}\eta_0,\,\delta,\,k\nu_0+\delta)\). Choose \(\eta_0\) so total \(\eta\) meets goal (iii) budget.

**Non-import:** do not identify \(\tilde\theta\) with ZJ’s LASSO support / PoSI model \(\hat M\).

---

## Lemma soft (Gibbs / exponential tilt)

**Claim:** \(\beta=\eta/(2\varepsilon)\) \(\Rightarrow\) \((\eta,0,\nu)\)-stable soft-argmin.

**Sketch:**
1. On \(E\), \(|\hat f-f^\star|\le\varepsilon\) pointwise on \(\Theta_0\).
2. Densities: \(d\pi_\beta/d\mu\propto e^{-\beta\hat f}\), \(d\pi_\beta^\star/d\mu\propto e^{-\beta f^\star}\).
3. Pointwise density ratio and normalizing-constant ratio each contribute at most \(e^{\beta\varepsilon}\), hence max divergence \(\le 2\beta\varepsilon\).
4. Set \(\beta=\eta/(2\varepsilon)\) \(\Rightarrow\) \(\approx_{\eta,0}\) on \(E\) \(\Rightarrow\) \((\eta,0,\nu)\)-stable.

---

## Corollary small-η (goal iii)

1. \(\eta\) is free via \(b=2\varepsilon/\eta\) or \(\beta=\eta/(2\varepsilon)\).
2. Sequence \(\eta_r\downarrow 0\) (with \(\nu_r\) from tighter concentration or fixed \(\nu\) absorbed in Part II budget) feeds Part II Cor. vanish at **fixed** classical level of \(\mathcal{C}\).
3. Cost: larger \(b\) / smaller \(\beta\) \(\Rightarrow\) softer selection (utility ↓). That is the (iii) price — not widening \(\mathcal{C}\).

---

## Status

- Density-ratio / composition steps: standard (ZJ + exponential mechanism).
- Open: concrete \(\varepsilon(n),\nu(n)\) for a chosen \(\hat f,\hat g\) instance of (2).
- Demo: `research/experiments/noisy_objective_stability_demo.py` checks “more noise ⇒ less brittle selection” only.
