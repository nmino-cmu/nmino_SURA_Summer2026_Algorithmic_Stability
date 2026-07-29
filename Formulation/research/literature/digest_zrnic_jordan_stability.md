# Digest: Post-Selection Inference via Algorithmic Stability

**Paper:** Tijana Zrnic & Michael I. Jordan, *Post-Selection Inference via Algorithmic Stability* (arXiv:2011.09462v2, 14 Mar 2022).  
**Source PDF:** `context/papers/01_priority_current/Post-Selection Inference via Algorithmic Stability.pdf` (42 pp.).  
**Ceiling (writeup):** selected object is only $\hat\theta$ from constrained opt (2); validity is (1); goal (iii) = data-randomize selection, **not** recalibrate $\mathcal{C}$. No CREDO/CREME as problem objects.

---

## 1. Stability definition(s) — paper-native notation

### Definition 1 (Indistinguishability) — PDF p.6, Def. 1

A random variable $Q$ is $(\eta,\tau)$-indistinguishable from $W$, written
$$
Q \approx_{\eta,\tau} W,
$$
if for all measurable sets $O$,
$$
\mathbb{P}\{Q\in O\} \le e^\eta\,\mathbb{P}\{W\in O\} + \tau.
$$
($\tau$ bounds the mass of “very different” events; $\eta$ is a max-divergence / DP-style closeness parameter.)

### Definition 2 (Stability) — PDF p.6, Def. 2

Let $A:\mathbb{R}^n\to\mathcal{S}$ be a randomized algorithm. $A$ is **$(\eta,\tau,\nu)$-stable** w.r.t. a distribution $P$ on $\mathbb{R}^n$ if there exists a random variable $A_0$ (possibly depending on $P$, **not** on the realized data) such that
$$
\mathbb{P}\bigl\{\omega\in\mathbb{R}^n : A(\omega)\approx_{\eta,\tau} A_0\bigr\} \ge 1-\nu.
$$
Special case of Bassily–Freund typical stability. Reference distribution in the paper is the data law $P_y$; when they say “$(\eta,\tau,\nu)$-stable” they mean w.r.t. $P_y$.

**Selection notation (PDF p.6–7, §4):** $\hat S(\cdot)$ is a (possibly randomized) selection map $y\mapsto\hat S(y)\in\mathcal{S}$ that determines the inferential target. Abuse: $\hat S\equiv\hat S(y)$. Intuition: $\hat S$ is stable if the law of $\hat S(y)\mid y$ can be guessed from $P_y$ alone (oracle $\hat S_0$), up to $(\eta,\tau)$ indistinguishability on a $1-\nu$ set.

**Building-block mechanism (Example 1, PDF p.7):** for fixed $w$, $y\sim N(\mu,\sigma^2 I)$,
$$
A(y)=w^\top y+\xi,\qquad \xi\sim\mathrm{Lap}\Bigl(\frac{z_{1-\nu/2}\,\sigma\|w\|_2}{\eta}\Bigr)
$$
is $(\eta,0,\nu)$-stable with oracle $A_0=A(\mu)$.

**Algorithmic properties (PDF §8.1, p.13–14):** closure under post-processing; adaptive / non-adaptive composition (Supplement Lemmas 3–4, PDF p.25–26).

**Not their notion:** classical leave-one-out / uniform stability of ERM (Bousquet–Elisseeff). Stability here is **distributional indistinguishability of the selection law**, enforced by randomization.

---

## 2. Main theorems: stability → post-selection CI / coverage correction

### Informal Theorem 1 (PDF p.1–2)

For every fixed selection $S$, classical intervals $\mathrm{CI}^{(\alpha)}_S$ satisfy $\mathbb{P}\{\beta_S\notin\mathrm{CI}^{(\alpha)}_S\}\le\alpha$. If $\hat S$ is $\eta$-stable (informal), then
$$
\mathbb{P}\bigl\{\beta_{\hat S}\notin\mathrm{CI}^{(\alpha e^{-\eta})}_{\hat S}\bigr\}\le\alpha.
$$
Correction = **inflate the nominal miscoverage** by $e^\eta$ (equivalently: use a more conservative classical quantile).

### Lemma 1 (PDF p.7, formal Eq. (1); proof A.5, PDF p.26–27)

If $\hat S$ is $(\eta,\tau,\nu)$-stable with oracle $\hat S_0$, then
$$
(y,\hat S(y))\approx_{\eta,\,\tau+\nu}(y,\hat S_0).
$$

### Theorem 2 (PDF p.7–8; key result; proof A.6, PDF p.27)

Fix $\delta\in(0,1)$. Let $\hat S$ be $(\eta,\tau,\nu)$-stable. Suppose for every fixed $S$, $\mathrm{CI}^{(\alpha)}_S$ are classical valid intervals at level $1-\alpha$. Then
$$
\mathbb{P}\bigl\{\beta_{\hat S}\notin\mathrm{CI}^{(\delta e^{-\eta})}_{\hat S}\bigr\}\le\delta+\tau+\nu.
$$
**Operational recipe:** to target overall error $\alpha$, take e.g. $\tau=\nu=\alpha/3$ and build classical intervals at level $\delta e^{-\eta}$ with $\delta=\alpha/3$ (PDF p.8).

### Corollaries (linear regression PoSI) — PDF §6, p.10–11

- **Corollary 1:** $(\eta,\tau,\nu)$-stable model selection $\hat M$ $\Rightarrow$ use PoSI constant $K_{\hat M,\,\delta e^{-\eta}}$ instead of $K_{\hat M,\delta}$; miscoverage $\le\delta+\tau+\nu$.
- **Corollary 2 (Gaussian):** Bonferroni-$z$/$t$ with level $\delta/(2|\hat M|e^\eta)$ (i.e. $e^\eta$ inflation inside the quantile argument).
- **Proposition 1 (PDF p.11):** arbitrary $s$-sparse selection admits indistinguishability with $\eta=O(s\log(d/s))+\log(1/\tau)$, recovering Scheffé-scale PoSI.

### Conditional flavor — Lemma 2 (PDF §7, p.11–12; proof A.8)

$(\eta,0,\nu)$-stability w.r.t. oracle $\hat S(y'_E)$ yields
$$
\mathbb{P}\{y\in O_S\mid\hat S(y)=S,\,y\in E\}\le e^\eta\,\mathbb{P}\{y\in O_S\mid y\in E\},
$$
with $\mathbb{P}\{y\in E\}\ge 1-\nu$ (conditioning also on high-probability set $E$).

### Design theorems (how stability is achieved) — PDF §8

- **Proposition 2:** Stable LASSO (Alg. 2, Frank–Wolfe + Lap noise) is $(\tfrac12 k\eta^2+\sqrt{2k\log(1/\delta)}\,\eta,\,\delta,\,\delta)$-stable and $(k\eta,0,\delta)$-stable.
- **Proposition 4:** Stable marginal screening (Alg. 3) — same stability rates.
- Utility Propositions 3, 5 quantify excess risk / ranking error as $\tilde O(1/\eta)$ (randomization cost).

---

## 3. Proof outline (≤15 bullets) — Lemma 1 + Theorem 2

1. **Def. 2:** existence of oracle $\hat S_0$ (indep. of $y$) and set $E=\{\omega:\hat S(\omega)\approx_{\eta,\tau}\hat S_0\}$ with $\mathbb{P}\{y\in E\}\ge 1-\nu$.
2. **Lemma 1 setup:** for measurable $O\subseteq\mathbb{R}^n\times\mathcal{S}$, write $O_\omega=\{S:(\omega,S)\in O\}$; indicator of $(y,\hat S(y))\in O$ is $1\{\hat S(y)\in O_y\}$.
3. On $E$, Def. 1 gives $\mathbb{P}\{\hat S(y)\in O_y\mid y\}\le e^\eta\mathbb{P}\{\hat S_0\in O_y\mid y\}+\tau$.
4. Take expectation over $y\in E$: $\mathbb{P}\{(y,\hat S)\in O,\,y\in E\}\le e^\eta\mathbb{P}\{(y,\hat S_0)\in O,\,y\in E\}+\tau$.
5. Add the $\nu$-mass of $E^c$: $\mathbb{P}\{(y,\hat S)\in O\}\le e^\eta\mathbb{P}\{(y,\hat S_0)\in O\}+\tau+\nu$ $\Rightarrow$ Lemma 1.
6. **Thm 2:** apply Lemma 1 to the miscoverage event $\{\beta_{\hat S}\notin\mathrm{CI}^{(\delta e^{-\eta})}_{\hat S}\}$.
7. Right-hand side becomes $e^\eta\mathbb{P}\{\beta_{\hat S_0}\notin\mathrm{CI}^{(\delta e^{-\eta})}_{\hat S_0}\}+\tau+\nu$.
8. Condition on oracle $\hat S_0$: classical validity of $\mathrm{CI}^{(\delta e^{-\eta})}_S$ for fixed $S$ gives conditional miscoverage $\le\delta e^{-\eta}$.
9. Multiply by $e^\eta$: $e^\eta\cdot\delta e^{-\eta}=\delta$; add $\tau+\nu$ $\Rightarrow$ Theorem 2.
10. **Achieving Def. 2 (vignettes / Algs 2–3):** high-prob. concentration set (e.g. $\|y-\mu\|_\infty$ or gradient/score max-norm); Lap noise scaled so density ratio $\le e^\eta$ on that set; “report noisy max” / Frank–Wolfe step arguments; composition (Lemma 3) across $k$ steps.
11. **Post-processing:** any function of a stable output (e.g. support of $\hat\theta_{\mathrm{LASSO}}$) inherits the same $(\eta,\tau,\nu)$.
12. **Corollary 1:** instantiate Thm 2 with $\mathrm{CI}$ = OLS intervals with PoSI constant $K_{M,\alpha}$, set $\alpha=\delta e^{-\eta}$.
13. **Conditional path (Lemma 2):** same indistinguishability restricted to $E$, normalize by $\mathbb{P}\{y\in E\}$, set $O=O_S\times\{S\}$, cancel $\mathbb{P}\{\hat S=S\mid E\}$ using independence of $y$ and $\hat S(y'_E)$.
14. **Scheffé recovery (Prop. 1):** even unstable sparse selectors admit some $\eta=O(s\log(d/s))$ indistinguishability vs i.i.d. copy oracle — Thm 2 still applies, intervals widen accordingly.
15. **Design takeaway:** choosing $\eta$ trades selection fidelity (utility $\sim 1/\eta$) against required classical-level inflation $e^\eta$.

---

## 4. Map to writeup (2)→$\hat\theta$ and inflation for plugging into (1)

| Zrnic–Jordan | Writeup |
|---|---|
| Data $y$, law $P_y$ | Calibration data $\mathcal{D}$ |
| Selection algorithm $A$ / $\hat S$ | Constrained opt (2) producing $\hat\theta(\mathcal{D})$ |
| **$A(D)\leftrightarrow\hat\theta(D)$** | Selected object is **only** $\hat\theta$, not a general selector / co-equal $z$ |
| Inferential target $\beta_S$ after selection $S$ | Plugging $\theta$ into validity (1): $\mathbb{P}(Y\in\mathcal{C}(X;\mathcal{D},\theta))\ge 1-\alpha$ |
| Classical $\mathrm{CI}^{(\alpha)}_S$ valid for fixed $S$ | Classical validity (1) for **prespecified** $\theta$ |
| Oracle $\hat S_0$ indep. of $y$ | Hypothetical selection independent of $\mathcal{D}$ used for $\mathcal{C}$ |

**What plays the role of inflation when plugging $\hat\theta$ into (1):**

Theorem 2’s correction is: replace the classical miscoverage level $\alpha$ by $\delta e^{-\eta}$ inside the classical construction — i.e. **inflate the nominal error by $e^\eta$** (equivalently widen quantiles / PoSI constant $K_{\cdot,\delta e^{-\eta}}$).  

For the writeup’s set-valued validity (1), the analogous statement would be: if $\hat\theta$ is $(\eta,\tau,\nu)$-stable and (1) holds for every fixed $\theta$ at level $1-\alpha$, then
$$
\mathbb{P}\bigl(Y\notin\mathcal{C}(X;\mathcal{D},\hat\theta)\bigr)
$$
is controlled by building $\mathcal{C}$ at the **inflated** classical level $\delta e^{-\eta}$ (plus $\tau+\nu$), **not** by changing the selection rule alone.

**Alignment with goal (iii):** Zrnic–Jordan achieve small inflation by **data-randomizing selection** (Lap / noisy Frank–Wolfe / noisy argmax) so that $\eta$ is user-chosen; as $\eta\to 0$, $\mathrm{CI}^{(\delta e^{-\eta})}\to\mathrm{CI}^{(\delta)}$ and classical intervals need essentially **no** recalibration. That matches Wenbin’s override: restore validity by randomizing selection, not by redesigning $\mathcal{C}$. Using a large $\eta$ and compensating with a more conservative $\mathcal{C}$ is their Thm 2 “correction” path — closer to answering (i)–(ii) / PoSI inflation than to goal (iii).

**Structural echo of (2):** Alg. 2 stabilizes a **constrained** Frank–Wolfe LASSO $\|\theta\|_1\le C_1$ (PDF Eq. (5), p.15) — same “constrained opt → selected object” shape as writeup (2), but their selected object for inference is typically the **model** $\hat M=\mathrm{post}(\hat\theta)$, with $\beta_{\hat M}$ the target; writeup stops at $\hat\theta$ as the sole selected object and asks about plugging into $\mathcal{C}(\cdot;\theta)$.
