# Proof sketch: Nested UQ instance + Ass. concentration rates

Source: `research/formal/instance_nested_uq.tex`  
Feeds: Ass. concentration in `part_i_randomized_design.tex` (open gap closed).  
Selected object: \(\hat\theta/\tilde\theta\) only. Not CREDO \(z\). CRC nesting = (FV) warrant only.

---

## Instance of (2)

1. Score \(s(x,y)\in[0,1]\); nested sets \(C_\theta(x)=\{y:s(x,y)\le\theta\}\), \(\Theta=[0,1]\).
2. \(\hat f(\theta)=n^{-1}\sum_i 1\{s_i>\theta\}=1-\widehat F_n(\theta)\); \(f^\star=1-F\).
3. Box \(\hat g\): \(\Theta_0=[0,1]=\{g^\star\le 0\}\) always → feasible-set half of Ass. conc is free.
4. Deterministic \(\arg\min \hat f\) is \(\theta=1\) (monotone); live object for (iii) is randomized design on \(\hat f\).

**(FV):** For each fixed \(\theta\), nested monotone indicator loss + exchangeability ⇒ writeup (1). Cite CRC Thm 1 / split conformal as template only — do not import CRC \(\hat\lambda\) as \(\hat\theta\).

---

## Lemma dkw-conc

**Claim:** \(\varepsilon(n,\nu)=\sqrt{\log(2/\nu)/(2n)}\), \(\nu(n)=\nu\) ⇒ Ass. conc holds.

**Sketch:**
1. \(\|\hat f-f^\star\|_\infty=\|\widehat F_n-F\|_\infty\).
2. DKW: \(\mathbb{P}(\|\widehat F_n-F\|_\infty>\varepsilon)\le 2e^{-2n\varepsilon^2}\).
3. Set \(2e^{-2n\varepsilon^2}=\nu\) ⇒ \(\varepsilon=\sqrt{\log(2/\nu)/(2n)}\).
4. \(\Theta_0=\{g^\star\le 0\}\) holds on a probability-1 event.

**Ceiling:** Scores treated as i.i.d.\ on the calibration fold (score map fixed / independent of \(\mathcal{D}\)). If \(s\) is fit on the same \(\mathcal{D}\), this lemma does not apply as stated.

---

## Corollary grid (Hoeffding)

**Claim:** On finite \(\Theta_m\), \(\varepsilon_{\mathrm{grid}}=\sqrt{\log(2m/\nu)/(2n)}\).

**Sketch:** Each \(\theta_j\): Hoeffding on bounded \([0,1]\) indicators ⇒ \(2e^{-2n\varepsilon^2}\) per coordinate; union bound \(\times m\); solve for \(\varepsilon\).

---

## Corollary plug → design

1. Feed \(\varepsilon(n,\nu),\nu\) into RNM \(b=2\varepsilon/\eta\) or soft \(\beta=\eta/(2\varepsilon)\).
2. Get \((\eta,0,\nu)\)-stable \(\tilde\theta\) (part_i Lemmas rnm/soft).
3. Infl \(\le(e^\eta-1)\alpha+\nu\) shrinks in \(\eta\) at fixed \(\mathcal{C}^{(\alpha)}\) map.

---

## Status

- Ass. conc gap for this instance: **closed** (explicit \(\varepsilon(n),\nu(n)\)).
- Demo: `research/experiments/instance_nested_uq_demo.py`.
