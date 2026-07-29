# METHODS ONLY — NOT PROBLEM SCOPE

Do not import $\pi_\varepsilon$, inverse region, decision-risk as live problem objects.  
Extract: structured noise / inverse conformal ideas usable to randomize $\hat\theta$ selection.

---

# Digest: CREDO — methods only (inverse CP / IO geometry)

**Paper:** *Conformalized Decision Risk Assessment* (CREDO; preprint in `context/papers/02_lab_algorithmic/`).  
**Source PDF:** `context/papers/02_lab_algorithmic/Conformalized Decision Risk Assessment.pdf` (41 pp.).  
**Ceiling:** extract **techniques** that suggest how to **data-randomize selection** of $\hat\theta$ from (2). Do **not** enlarge the problem to decision $z$, $\pi_\varepsilon$, $\pi^{-1}$, or decision-risk $\alpha(z)$. Validity target remains (1) at $\hat\theta$; goal (iii) = randomize selection, **no** $\mathcal{C}$ recalibration.

---

## 0. Quarantine (OUT of live math)

| Paper object | Status |
| --- | --- |
| $\pi_\varepsilon(y)$, $\varepsilon$-optimal decision rule (Eq. (1)) | OUT — not co-equal to $\hat\theta$ |
| Inverse feasible region $\pi^{-1}_\varepsilon(z)$ (Eq. (4)); Lemma 1 | OUT as problem statement |
| Decision risk $\alpha(z)=\mathbb{P}\{z\notin\pi(Y)\}$ / CREDO estimator $\hat\alpha(z)$ | OUT |
| Generative balls $C(x;\alpha)$, Algo 1 CREDO, Algo 2 DCA | OUT as deliverables |
| Thm 1 / Cor 1 as guarantees **on decision risk** | OUT |

Keep only the **geometry / selection-randomization patterns** below.

---

## 1. Inverse view usable for randomizing $\hat\theta$ (not for new equations)

### Pattern A — Flip the argmin question (Lemma 1, methods analogy only)

CREDO Lemma 1: $\mathbb{P}\{z\in\pi(Y)\}\equiv\mathbb{P}\{Y\in\pi^{-1}(z)\}$.  
**Transferable idea (selection only):** instead of asking “which $\theta$ does (2) pick?”, ask “in which directions of the data-dependent maps $(\hat f,\hat g)$ does the **optimizer of (2) flip**?” Those directions are the natural support of **structured** noise on the selection map $\mathcal{D}\mapsto\hat\theta(\mathcal{D})$. Isotropic noise in $\theta$-space ignores that geometry.

### Pattern B — Soft / near-optimal selection (Eq. (1) $\varepsilon$-argmin; quarantine symbols)

CREDO’s $\varepsilon$-optimal set is a **thickened argmin**.  
**Transferable idea:** randomize among **near-minimizers** of (2),
$$
\tilde\theta\in\bigl\{\theta:\ \hat f(y;\theta)\le \hat f(y;\hat\theta)+\varepsilon,\ \hat g(\theta)\le 0\bigr\}
$$
(or sample with weights decreasing in suboptimality), rather than adding isotropic Gaussian noise in ambient $\theta$. This is a **selection** randomization; it does not retune $\mathcal{C}$.

### Pattern C — Halfspace / constraint geometry of flips (Corollary 2, LP closed form)

For linear objectives, CREDO Cor. 2 reduces containment to halfspaces indexed by extreme-point competitors $v$: flips along directions $z-v$.  
**Transferable idea for (2):** if $\hat f,\hat g$ are locally smooth, first-order flip directions for $\hat\theta$ are spanned by $\nabla_\theta\hat f$ and active $\nabla_\theta\hat g_j$ (KKT / critical cone). Structured noise $\xi$ should live in that **sensitivity subspace** (or be shaped by the inverse Hessian / reduced Hessian of the Lagrangian of (2)), not $N(0,\sigma^2 I)$ in full $\theta$.

### Pattern D — Multi-draw softening of brittle selection (Algo 1 generative $K$-draws; Prop. 2 TPR)

CREDO Prop. 2: true-positive rate increases in $K$ (more generative draws).  
**Transferable idea:** replace a single hard $\mathrm{argmin}$ of (2) by a **randomized draw** among several perturbed solves (bootstrap / leave-some-out / noisy $\hat f,\hat g$), then pick $\tilde\theta$ from that cloud. Again: perturbs **selection**, leaves $\mathcal{C}(\cdot;\mathcal{D},\theta)$’s fixed-$\theta$ rule alone.

### Pattern E — Post-hoc exchangeability damage (Corollary 1 TV term) — contrast hook only

Cor. 1 adds a total-variation / swap term when post-hoc selection breaks exchangeability (vs Thm 1 $e$-value radius with cleaner expectation bound).  
**Use:** analogy for **goal (ii)** deviation size under data-dependent $\hat\theta$; **not** a license to import $e$-value recalibration of $\mathcal{C}$ as goal (iii). Our (iii) path is randomize $\tilde\theta(D;\xi)$, not switch radius functions of $\mathcal{C}$.

---

## 2. Inverse conformal idea (stripped of CREDO risk)

Inverse CP (cited: Prinster et al., Singh et al.; used inside CREDO §4.2): for a **fixed** set, find the smallest $\alpha$ such that a conformal ball sits inside that set.  
**What we may borrow:** the **inverse** mindset — given a candidate selection rule / near-optimal set for (2), certify how fragile $\hat\theta$ is to structured perturbations of $\mathcal{D}$ or $(\hat f,\hat g)$.  
**What we must not borrow:** using that $\alpha$ as a new coverage level to **rebuild** $\mathcal{C}$ (recalibration; forbidden for (iii)).

---

## 3. Explicit non-goals

- Do not set live estimand to $\mathbb{P}\{\hat\theta\in\pi(Y)\}$ or any decision-risk clone.  
- Do not add $\pi_\varepsilon$, $\pi^{-1}$, or CREDO Algo 1/2 to `formal/`.  
- Do not treat generative models for $Y\mid X$ as required for (iii).  
- Structured noise candidates that **only** touch selection belong in `patterns_inverse_opt_structured_noise.md` and later `notes/method_candidates_w5.md`.
