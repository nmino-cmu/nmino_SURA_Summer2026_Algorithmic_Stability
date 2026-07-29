# Digest: Conformal Risk Control (Angelopoulos et al.)

**Paper:** Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, Tal Schuster, *Conformal Risk Control* (ICLR 2024).  
**Source PDF:** `context/papers/03_background/Conformal Risk Control.pdf` (21 pp.).  
**Ceiling (writeup):** use only as the **fixed-$\theta$ validity template** behind assumption (1). Selected object remains $\hat\theta$ from (2); goal (iii) = data-randomize selection, **not** recalibrate $\mathcal{C}$. No CREDO/CREME objects.

---

## 1. What justifies fixed-$\theta$ / fixed-$\lambda$ validity like (1)

Writeup (1): for **prespecified** hyperparameter $\theta$,
$$
\mathbb{P}\bigl(Y\in\mathcal{C}(X;\mathcal{D},\theta)\bigr)\ge 1-\alpha.
$$
CRC’s split-style coverage is the special case of their risk control when the loss is miscoverage (paper Abs., §1, App. A).

### Setup (PDF §1.1)

Exchangeable non-increasing, right-continuous losses $L_i:\Lambda\to(-\infty,B]$ with $\lambda_{\max}=\sup\Lambda\in\Lambda$ and $L_i(\lambda_{\max})\le\alpha$ a.s. Goal: choose $\hat\lambda$ from $\{L_1,\ldots,L_n\}$ so
$$
\mathbb{E}\bigl[L_{n+1}(\hat\lambda)\bigr]\le\alpha. \tag{CRC (3)}
$$
Motivating specialization: $L_i(\lambda)=\ell\bigl(C_\lambda(X_i),Y_i\bigr)$ with $\ell$ non-increasing in $\lambda$ (larger $\lambda$ = more conservative set).

### Threshold rule (PDF Eq. (4))

$$
\hat\lambda=\inf\Bigl\{\lambda:\ \tfrac{n}{n+1}\widehat R_n(\lambda)+\tfrac{B}{n+1}\le\alpha\Bigr\}
=\inf\Bigl\{\lambda:\ \widehat R_n(\lambda)\le \alpha-\tfrac{B-\alpha}{n}\Bigr\},
$$
with $\widehat R_n=n^{-1}\sum_{i=1}^n L_i$ and $\hat\lambda=\lambda_{\max}$ if the set is empty. Monotonicity of $\widehat R_n$ $\Rightarrow$ binary search.

### Theorem 1 (Risk control) — PDF §2.1

Under exchangeability, non-increasing right-continuous $L_i$, $L_i(\lambda_{\max})\le\alpha$, and $\sup_\lambda L_i(\lambda)\le B<\infty$ a.s. (condition (5)):
$$
\mathbb{E}\bigl[L_{n+1}(\hat\lambda)\bigr]\le\alpha.
$$
**Proof skeleton (paper):** compare to the full-sample threshold $\hat\lambda'=\inf\{\lambda:\widehat R_{n+1}(\lambda)\le\alpha\}$; show $\hat\lambda'\le\hat\lambda$; then conditional on the multiset $\{L_1,\ldots,L_{n+1}\}$, $\hat\lambda'$ is fixed and $L_{n+1}(\hat\lambda')$ is uniform over the $n+1$ losses, so the average at $\hat\lambda'$ is $\le\alpha$.

**Transfer to (1):** when $\theta$ (CRC’s $\lambda$) is **prespecified**—not chosen from the same $\mathcal{D}$ used to build $\mathcal{C}$—the exchangeability argument that underlies CRC / split conformal applies **without** post-selection correction. That is exactly the writeup’s standing assumption (1). Selecting $\hat\theta(\mathcal{D})$ from (2) on shared $\mathcal{D}$ breaks the “prespecified” premise; CRC does **not** by itself restore (1) after that selection.

### Theorem 2 (Tight lower bound) — PDF §2.2

If additionally $L_i$ are i.i.d., nonnegative, and $P(J(L_i,\lambda)>0)=0$ for every fixed $\lambda$ (no atoms at pre-specified jumps), then
$$
\mathbb{E}\bigl[L_{n+1}(\hat\lambda)\bigr]\ge\alpha-\tfrac{2B}{n+1}.
$$
**Proposition 1:** the $2B/(n+1)$ factor is sharp for general monotone losses.  
**App. A:** for indicator miscoverage loss, CRC $\Leftrightarrow$ split conformal; Lei et al. give $\alpha-1/(n+1)$ lower bound; Thm 2 recovers the same with worse constant $2/(n+1)$.

---

## 2. Monotone threshold / risk-control structure (what (1) rides on)

| Ingredient | Role for (1)-style validity |
| --- | --- |
| Nested / monotone conservatism in $\lambda$ (or $\theta$) | Larger parameter $\Rightarrow$ weakly larger / safer set; loss non-increasing in $\lambda$ (Thm 1 hyp.) |
| Right-continuity | Needed for conditional average at $\hat\lambda'$ (Thm 1 proof) |
| Exchangeability of calibration + test | Uniform draw of $L_{n+1}\mid\{L_i\}$ (Thm 1) |
| Bounded loss $B$ | Finite-sample $B/(n+1)$ correction in (4) |
| Achievability $L_i(\lambda_{\max})\le\alpha$ | Threshold well-defined |

**Proposition 2 (PDF §2.3):** without monotonicity, the same threshold rule can fail arbitrarily ($\mathbb{E}[L_{n+1}(\hat\lambda)]\ge B-\varepsilon$).  
**Corollary 1:** monotonize $\widetilde L_i(\lambda)=\sup_{\lambda'\ge\lambda}L_i(\lambda')$ and run (4) $\Rightarrow$ Thm 1 applies (possibly conservative if loss is far from monotone).

**Operational reading for our $\mathcal{C}(\cdot;\mathcal{D},\theta)$:** validity (1) for fixed $\theta$ is the CRC/CP guarantee when the construction of $\mathcal{C}$ is a **monotone threshold family** in $\theta$ (or an equivalent nested score threshold) calibrated under exchangeability. Hyperparameter $\theta$ in (1) plays CRC’s $\lambda$ only when it is fixed **before** looking at the calibration used for the set; our (2) makes $\theta$ data-dependent.

---

## 3. What transfers / what must not be imported

### Transfers (methods pattern only)

- **Fixed-$\theta$ baseline for Part II (i):** if $\hat\theta\perp$ the data used to form $\mathcal{C}$ (or $\theta$ is otherwise prespecified), Thm 1 / split conformal justify (1).
- **Monotone nested family:** Part II should treat $\theta\mapsto\mathcal{C}(\cdot;\mathcal{D},\theta)$ as monotone in the CRC sense when stating (1).
- **$O(1/n)$ slack:** Thm 2 / App. A — classical conformal gap is $O(1/n)$, not concentration $O(n^{-1/2})$ (contrast RCPS/LTT, App. B). Useful when quantifying **how small** a post-selection deviation (goal (ii)) must be to matter relative to the usual conformal slack.

### Non-transfer (do-not-import)

- Do **not** treat CRC’s adaptive choice of $\hat\lambda$ from risk target $\alpha$ as our problem: writeup selects $\hat\theta$ via constrained opt (2), not via CRC threshold (4).
- Do **not** answer goal (iii) by re-running CRC / recalibrating scores or thresholds of $\mathcal{C}$ after seeing $\hat\theta$ (W5: data-randomize **selection** only).
- Do **not** import FNR / graph-distance / token-F1 worked examples, U-statistics, adversarial multi-risk extensions (paper §3–4) as live equations.
- Do **not** import RCPS/LTT high-probability risk control (App. B) as the standing form of (1); writeup (1) is a **probability / expectation-style** coverage statement, not a $(\alpha,\delta)$ RCPS bound.

---

## 4. Citation map (theorem numbers)

| Claim | Location |
| --- | --- |
| Risk control under monotone exchangeable losses | **Theorem 1** |
| Matching lower bound (i.i.d., continuous jumps) | **Theorem 2** |
| Sharpness of $2B/(n+1)$ | **Proposition 1** |
| Failure without monotonicity | **Proposition 2** |
| Monotonization fix | **Corollary 1** |
| CP $\Leftrightarrow$ CRC for indicator loss | **Appendix A** |
| Jump control for Thm 2 proof | **Lemma 1** (Jump Lemma, App. E) |
| Asymptotic non-monotone variant | **Theorem C.1** (App. C; not needed for (1)) |
