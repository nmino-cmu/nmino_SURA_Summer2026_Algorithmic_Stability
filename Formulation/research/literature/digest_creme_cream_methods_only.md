# METHODS ONLY — NOT PROBLEM SCOPE

Do not import $\pi_\varepsilon$, inverse region, decision-risk as live problem objects.  
Extract: risk-assessment / conformalized-frontier patterns usable as **analogy** for goal-(ii) deviation bounds; mark Algorithm 1 data-split recalibration as **CONTRAST** (not our (iii) path).

---

# Digest: CREME — methods only (inverse CRC / post-hoc $\Delta$)

**Paper:** Wenbin Zhou & Shixiang Zhu, *Calibrating Decision Robustness via Inverse Conformal Risk Control* (arXiv:2510.07750v2; algorithm name **CREME** = Conformal REgret Miscoverage Estimate).  
**Source PDF:** `context/papers/02_lab_algorithmic/Calibrating Decision Robustness via Inverse Conformal Risk Control.pdf` (20 pp.).  
**Note on filename `creme_cream`:** the PDF’s own acronym is **CREME**; there is no separate “CREAM” paper in the frozen reading queue. Treat “CREAM” as a synonym typo for CREME if it appears in notes.  
**Ceiling:** methods patterns only. Do **not** import robust policy family $\{z^*_\lambda\}$, miscoverage–regret Pareto frontier, or CREME as the live problem. Live objects remain (1)(2) and $\hat\theta$.

---

## 0. Quarantine (OUT of live math)

| Paper object | Status |
| --- | --- |
| Robust PTO (1): $z^*_\lambda(X)=\arg\min_z\max_{y\in U_\lambda(X)}f(y,z)$ | OUT |
| Losses $I_\lambda$, $R_\lambda$; estimators $\hat\alpha_I(\lambda)$, $\hat\alpha_R(\lambda)$ | OUT as problem |
| Certified Pareto frontier (Prop. 3.7, Cor. 3.8) | OUT |
| Majorant consistency Assump. 3.6 as a writeup axiom | OUT (may inspire monotone-in-$\theta$ intuition only) |
| **Algorithm 1 CREME split + post-hoc report** | **CONTRAST** for (iii) — see §3 |

---

## 1. Inverse CRC (methods) — fixed index vs selected index

**Forward CRC** (Angelopoulos et al.; see `digest_angelopoulos_crc.md`): prescribe risk $\alpha$, find $\hat\lambda$.  
**Inverse CRC** (this paper §3.1): prescribe index $\lambda$, estimate risk upper bound
$$
\hat\alpha_\ell(\lambda)=\inf\Bigl\{\alpha\in(0,B):\ B-\bar\ell_n(\lambda)\ge\tfrac{\lceil(n+1)(B-\alpha)\rceil}{n}\Bigr\}
\quad\text{(Def. 3.3 / Eq. (5))},
$$
with practical relaxation $\tilde\alpha_\ell(\lambda)=\tfrac{n}{n+1}\bar\ell_n(\lambda)+\tfrac{B}{n+1}$ (Eq. (6)).

**Theorem 3.4 (Validity):** under Assumps. 3.1 (exchangeability) and 3.2 (loss in $[0,B]$), for **prespecified** $\lambda$,
$$
\mathbb{E}[\hat\alpha_\ell(\lambda)]\ge\mathbb{E}[\ell_\lambda(X_{n+1},Y_{n+1})].
$$
**Proposition 3.5:** i.i.d. finite-sample deviation of order $O(n^{-1/2})$ (Hoeffding-style $\varepsilon$ in (8)).

**Transfer analogy to writeup:** Thm 3.4 is the same logical slot as writeup (1) / CRC Thm 1 — validity when the hyperparameter is **fixed**. Once $\hat\lambda$ (our $\hat\theta$) is chosen from the same data, that slot no longer holds without a correction (their §3.3; our goals (i)–(ii)).

---

## 2. Goal-(ii) analogy — post-hoc deviation bound (Corollary 3.9)

**Corollary 3.9 (Post-hoc validity degradation)** — PDF §3.3: if
$$
\hat\lambda=\arg\max_{\lambda\in\Lambda} g\bigl(\hat\alpha_I(\lambda),\hat\alpha_R(\lambda)\bigr)
$$
is chosen from the same calibration sample used to form $\hat\alpha_\ell$, then
$$
\mathbb{E}\bigl[\hat\alpha_\ell(\hat\lambda)\bigr]
\ge
\mathbb{E}\bigl[\ell_{\hat\lambda}(X_{n+1},Y_{n+1})\bigr]
-\Delta(g,P),
$$
with
$$
\Delta(g,P)
:=\sup_{1\le i\le n}
\Bigl|
\mathbb{E}\bigl[\ell_{\hat\lambda}(X_i,Y_i)\bigr]
-
\mathbb{E}\bigl[\ell_{\hat\lambda}(X_{n+1},Y_{n+1})\bigr]
\Bigr|.
$$
Intuition in paper: data-dependent $\hat\lambda$ breaks exchangeability between calibration points and the test point; $\Delta$ measures the induced asymmetry.

### Map to goal (ii) (analogy only — do not import $\Delta(g,P)$ as a writeup symbol)

| CREME | Our Part II (ii) |
| --- | --- |
| Fixed $\lambda$ $\Rightarrow$ Thm 3.4 exact | Fixed $\theta$ $\Rightarrow$ (1) |
| Post-hoc $\hat\lambda$ $\Rightarrow$ gap $\Delta(g,P)$ | Post-hoc $\hat\theta(\mathcal{D})$ from (2) $\Rightarrow$ deviation between nominal $\alpha$ and actual miscoverage of $\mathcal{C}(\cdot;\mathcal{D},\hat\theta)$ |
| $\Delta$ large when selection $g$ couples strongly to the loss on $\mathcal{D}$ | Unstable / highly data-dependent $\hat\theta$ (Part I LOO) should inflate the gap |

**Proposition 3.5’s $\varepsilon$** is a different object (estimation error of $\hat\alpha$ at **fixed** $\lambda$); useful only as a reminder that finite-sample slack exists even without selection. Goal (ii) concerns **selection-induced** inflation, closer to Cor. 3.9’s $\Delta$.

---

## 3. Algorithm 1 split — CONTRAST (not our (iii) path)

**Algorithm 1 CREME** (PDF p.5): randomly split indices into $I_1,I_2$; build frontier $\hat F^{(1)}$ on $I_1$; decision-maker picks $\hat\lambda$ from $\hat F^{(1)}$; **report** risks $(\hat\alpha_I^{(2)}(\hat\lambda),\hat\alpha_R^{(2)}(\hat\lambda))$ from the held-out split $I_2$.

Paper’s own framing (§3.3): split **restores finite-sample validity of the reported risk estimates** after post-hoc selection — i.e. a **recalibration / re-estimation** of the conformalized risk functionals on fresh data.

| | CREME Algo 1 | Writeup goal (iii) / W5 |
| --- | --- | --- |
| What is randomized / split? | Calibration used to **estimate risk** of a chosen $\lambda$ | Data used to **select** $\hat\theta$ via (2) |
| What stays fixed? | Often the RO family $\{U_\lambda\}$ | Construction of $\mathcal{C}(\cdot;\mathcal{D},\theta)$ for each fixed $\theta$ |
| Restores validity by… | Second-split **re-estimation** of $\hat\alpha$ (recalibration of the reported conformal risk) | **Data-randomizing the selection map** $\tilde\theta(D;\xi)$ so (1) holds **without** recalibrating $\mathcal{C}$ |

**CONTRAST verdict:** Algo 1 is explicitly a **recalibration-after-selection** repair. It is valuable as a foil and as motivation that post-hoc selection breaks Thm 3.4, but it is **out** as an answer to (iii). Do not list split-recalibration of conformal scores / risk levels of $\mathcal{C}$ under method candidates for (iii).

Related-work nod in the paper (Zrnic–Jordan stability; e-values) points to the **alternative** family we actually want for (iii): randomize/stabilize the **selector**, not the reported risk of a fixed robust policy.

---

## 4. Minor transferable scraps (still methods-only)

- **Monotone nested index** (larger $\lambda\Rightarrow$ larger $U_\lambda$) + Assump. 3.6 majorant consistency $\Rightarrow$ Prop. 3.7 monotone risk tradeoff. Echoes CRC monotonicity; for us, prefer monotone nesting of $\theta\mapsto\mathcal{C}(\cdot;\theta)$ already assumed by (1), not RO regret frontiers.  
- **Inverse CRC estimator shape** (6): empirical risk $+\,B/(n+1)$ — same finite-sample spirit as CRC (4); not a new problem equation.

---

## 5. Citation map

| Claim | Location |
| --- | --- |
| Inverse risk estimator | **Definition 3.3**, Eqs. (5)–(6) |
| Validity at fixed $\lambda$ | **Theorem 3.4** |
| Finite-sample error at fixed $\lambda$ | **Proposition 3.5** |
| Majorant consistency | **Assumption 3.6** |
| True / certified Pareto | **Proposition 3.7**, **Corollary 3.8** |
| Post-hoc gap $\Delta(g,P)$ | **Corollary 3.9** |
| Split recalibration procedure | **Algorithm 1 (CREME)** — CONTRAST for (iii) |
