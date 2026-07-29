# Digest: A Flexible Defense Against the Winner’s Curse

**Source (read-only):** `context/papers/01_priority_current/A Flexible Defense Against the Winner's Curse.pdf`  
**Authors:** Tijana Zrnic, William Fithian (arXiv:2411.18569v1, Nov 2024)  
**Scope for this project:** methods relative to UQ plug-in \(\hat\theta(\mathcal{D})\) into frozen (1); goal (iii) = data-randomize **selection** of \(\hat\theta\), **not** recalibration of \(\mathcal{C}\).

---

## One-line takeaway for our UQ problem

The paper’s **primary method (zoom correction)** keeps **exact** winner selection \(\hat\imath = \arg\max_i X_i\) and restores validity by **redesigning / projecting a simultaneous confidence region** — i.e. it corrects the *inference set*, not the *selector*. That path is **contrast-only** for W5 goal (iii). The W5-relevant material is the paper’s own placement of **randomized / noise-addition** methods as a competing family: inject noise (or split data) into selection → pick a “noisy winner” → buy easier validity at the cost of selection quality.

---

## Problem they solve (map to ours)

| Their object | Ours (Wenbin UQ) |
| --- | --- |
| Candidates \(X_1,\ldots,X_m\) with means \(\theta = \mathbb{E}[X]\) | Competing \(\theta\)-values; data-driven \(\hat\theta(\mathcal{D})\) from constrained opt (2) |
| Empirical winner \(\hat\imath = \arg\max_i X_i\) | Data-driven selection of \(\hat\theta\) |
| CI for \(\theta_{\hat\imath}\) after selection (winner’s curse) | Validity of \(\mathcal{C}\) in (1) after plugging \(\hat\theta\) |
| Simultaneous region \(\widehat{\mathcal{C}}^\alpha\) then project | **Their answer:** recalibrate / reshape the inferential set |
| Related: “noisy winner” via noise / splitting | **Our W5 answer class:** randomize selection; leave \(\mathcal{C}\) alone |

---

## 1. How randomization / noise / stabilization is injected

### A. Main method — **no selection randomization** (stabilization via adaptive simultaneous test)

Pipeline (§2–3):

1. Pointwise null \(H_0(\theta): \mathbb{E}[X]=\theta\).
2. **Zoom test** acceptance region \(A_\alpha(\theta)\): rectangle centered at \(\theta\) with coordinate-\(j\) half-width
   \[
   r_\alpha(\theta)\vee \frac{\Delta_j(\theta)}{2},\qquad
   \Delta_j(\theta)=\theta^\star-\theta_j,\quad \theta^\star=\max_i\theta_i.
   \]
   Active radius
   \[
   r_\alpha(\theta)=\min\Bigl\{r:\; S\bigl(r\vee\tfrac{\Delta}{2}\bigr)\le\alpha\Bigr\}
   \]
   where \(S(v)\) is a known tail bound on errors \(\xi=X-\theta\) (§1.1): \(P(\exists i:|\xi_i|>v_i)\le S(v)\).
3. Invert to simultaneous region \(\widehat{\mathcal{C}}^\alpha=\{\theta: X\in A_\alpha(\theta)\}\).
4. Project onto winning coordinate: \(\widehat{\mathcal{C}}^\alpha_{\hat\imath}=\{\theta_{\hat\imath}:\theta\in\widehat{\mathcal{C}}^\alpha\}\).

**What is “stabilized”?** Not the selector. The **error budget** is concentrated on **active** (near-optimal) coordinates \(I_\alpha=\{j:\Delta_j\le 2r_\alpha\}\); inactive coordinates get forced wide boxes and stop consuming multiplicity. As gaps \(\to\infty\), \(r_\alpha\) recovers a **marginal** (uncorrected) radius; as \(\Delta\equiv 0\), \(r_\alpha\) recovers **full simultaneous** radius (§2).

**Observational “noise” role:** \(\xi\) enters only through \(S\) (exact joint law if known — Prop. 2.2 via quantile of \(M(\xi,\Delta)\); else Bonferroni union of marginals). This is **noise modeling for CI construction**, not injected selection noise.

Explicit author stance (§1.3): *“We focus on exact, non-randomized selection of the winner.”*

### B. Related family they cite — **selection randomization** (W5 hook)

§1.3 *Randomized approaches* (contrast they decline for their main theory):

> data splitting and noise addition … trading off the selection quality for an increase in statistical power. Instead of picking the exact winner, these methods select a “noisy winner.”

**Citations they give for that family:**

| Ref | Paper | Mechanism (as classified by Zrnic–Fithian) |
| --- | --- | --- |
| [18] | Tian & Taylor, *Selective inference with a randomized response*, AoS 2018 | Noise / randomized response in selection |
| [22] | Zrnic & Jordan, *Post-selection inference via algorithmic stability*, AoS 2023 | Stability certificates (noise ⇒ stability ⇒ corrected inference) |
| [16] | Rasines & Young, *Splitting strategies for post-selection inference*, Biometrika 2023 | Data splitting |
| [13] | Leiner et al., *Data fission*, JASA 2023 | Split a single observation |
| [15] | Neufeld et al., *Data thinning*, JMLR 2024 | Thinning / convolution-closed splits |

**Injection pattern (their words):** randomize or split so the selected index is a **noisy** analogue of \(\arg\max\); validity becomes easier / power improves relative to exact-winner post-selection; **cost is degraded selection quality**.

### C. Near-winners / soft selection of *inferential target* (not of \(\hat\theta\) procedure)

§5.3: after seeing data, may want CIs for indices other than \(\hat\imath\) (“near-winners”). Projection of the **same** simultaneous \(\widehat{\mathcal{C}}^\alpha\) onto any (possibly data-dependent) coordinate \(j\) remains valid; Prop. 5.3 gives a conservative outer set \(\widetilde{\mathcal{C}}^\alpha_j\). This softens **which parameters get reported**, still by **reusing / shaping \(\widehat{\mathcal{C}}\)** — not by randomizing the optimization that produced \(\hat\theta\).

---

## 2. Certificate bought; cost (power / width)

### Certificate (main method)

- **Prop. 2.1 (Zoom test):** \(P(X\in A_\alpha(\theta))\ge 1-\alpha\) under \(H_0(\theta)\).
- Simultaneous coverage \(\Rightarrow\) coverage of **any** data-dependent functional of \(\theta\) obtained by projection (§1.2), including \(\theta_{\hat\imath}\).
- **Thm. 3.1 (Zoom correction):** with \(\widehat{\mathcal{C}}^\alpha_{\hat\imath}=\{t:|X_{\hat\imath}-t|\le r_\alpha(\theta^t)\}\) and \([t_l,t_u]=\mathrm{conv}(\widehat{\mathcal{C}}^\alpha_{\hat\imath})\),
  \[
  P(\theta_{\hat\imath}\in[t_l,t_u])\ge 1-\alpha.
  \]
- Same set covers **population** max \(\theta^\star\) under symmetry of \(S\) (**Prop. 5.1**).
- Index set for population winner: **Prop. 5.2** — \(\widehat{\mathcal{I}}^\alpha=\{i:X_i\ge X_{\hat\imath}-2r_\alpha(\theta^{t_l})\}\).
- Top-\(k\): **Thm. 5.1 / 5.2**; variance-adaptive radii: §5.4, **Lemma 5.4**.

**Computational lemmas:** **Lemma 3.1** — \(t\in\widehat{\mathcal{C}}^\alpha_{\hat\imath}\) iff \(|X_{\hat\imath}-t|\le r_\alpha(\theta^t)\) for the worst-case vector (3); appendix **Lemmas B.1–B.3** (winner active; only inactive gaps matter; inactive-coordinate monotonicity).  
**Lemma 4.1 / Thm. 4.1:** Bonferroni-\(S\) closed form + **step-down** Algorithms 1–2 (slightly conservative radii \(\hat r_l,\hat r_u\)).

### Cost

| Regime | Width / power behavior |
| --- | --- |
| Many close competitors (\(\Delta\) small) | \(r_\alpha\) near full simultaneous / Bonferroni — **wide** intervals (pays multiplicity) |
| Clear winner (gaps large) | \(r_\alpha\to\) marginal uncorrected radius — **recovers standard CI** (stated goal of adaptivity; intro + §2) |
| vs polyhedral conditional [12] | Avoids infinite expected length pathology of [11] |
| vs hybrid [2] / LSI [21] | No error-budget split \(\beta,\nu\); hybrid often strongest under known-Gaussian Σ (§7); zoom competitive and more nonparametric |
| Step-down vs grid | Step-down slightly conservative; grid preferred under strong dependence (exp. §6) |
| Randomized family (§1.3) | **Cost on selection:** noisy winner may not be the empirical argmax; **payoff:** more power / simpler validity for the selected object |

**Asymmetric protection:** under union-bound \(S\), lower radius \(r_l\) (protects against upward winner’s-curse bias) is typically larger than upper \(r_u\) (Lemma 4.1 discussion).

---

## 3. Theorem / lemma checklist (for citations in formal notes)

| ID | Content |
| --- | --- |
| Prop. 2.1 | Zoom test valid at level \(1-\alpha\) |
| Prop. 2.2 | \(r_\alpha=\) \((1-\alpha)\)-quantile of \(M(\xi,\Delta)\) when joint noise law known |
| Lemma 3.1 | Projection membership \(\Leftrightarrow\) active-radius check at \(\theta^t\) |
| **Thm. 3.1** | Zoom correction CI for \(\theta_{\hat\imath}\) |
| Lemma 4.1 | Explicit \(r_l,r_u\) under Bonferroni \(S\) |
| **Thm. 4.1** | Step-down zoom correction validity |
| Lemmas 5.1–5.3, Thm. 5.1–5.2 | Top-\(k\) |
| Prop. 5.1–5.3 | Population winner value/index; near-winner outer sets |
| Lemma 5.4 | Variance-adaptive projection characterization |
| Lemmas B.1–B.3 | Technical engine for Lemma 3.1 |

---

## 4. Transfer to \(\hat\theta(\mathcal{D})\) / goal (iii) — what to take vs leave

### Take (W5-aligned)

- Framing: **selection quality ↔ inferential ease** tradeoff when noise is put on the **selector**.
- Pointers into the randomized / stability line ([18],[22],[16],[13],[15]) for constructing \(\tilde\theta(\mathcal{D};\xi)\) or split-based selection while **keeping \(\mathcal{C}\) fixed**.
- Intuition that **effective multiplicity** (how many near-competitors) drives how hard post-selection validity is — motivates needing Part I stability of (2) when competitors are close in objective value.

### Leave / contrast-only (RED LINE for goal (iii))

- Building a simultaneous region and **projecting / widening** intervals for the selected coordinate.
- Step-down / Bonferroni / zoom **reallocation of \(\alpha\)-budget** across candidates.
- Hybrid “correct the CI conditional on selection” (they discuss combining hybrid with zoom in §7).
- Any procedure that **recalibrates scores, thresholds, or radii of \(\mathcal{C}\)** so that (1) holds at \(\hat\theta\).

> **Project freeze (W5):** goal (iii) answers validity by **data-randomizing the selection of \(\hat\theta\)**; **no recalibration of \(\mathcal{C}\)**. Zoom correction is the clean exemplar of the *forbidden* dual path (exact selection + corrected \(\mathcal{C}\)).

---

## 5. Citation block

Zrnic, T., & Fithian, W. (2024). *A Flexible Defense Against the Winner’s Curse*. arXiv:2411.18569.

Related (cited therein for randomization / stability): Tian & Taylor (2018); Zrnic & Jordan (2023); Rasines & Young (2023); Leiner et al. (2023); Neufeld et al. (2024). Simultaneous / focusing baselines: Zrnic & Fithian LSI (2024); Andrews et al. hybrid (2024); Lee et al. polyhedral (2016).
