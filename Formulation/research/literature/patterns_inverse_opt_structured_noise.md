# Pattern: Inverse opt ⇒ structured (not isotropic) noise on selection

- **Inputs**
  - Constrained selection (2): $\hat\theta(\mathcal{D})=\arg\min\{\hat f(y;\theta):\hat g(\theta)\le 0\}$ with $\sigma(\hat f),\sigma(\hat g)\subseteq\sigma(\mathcal{D})$.
  - Fixed-$\theta$ validity (1) for $\mathcal{C}(X;\mathcal{D},\theta)$ (CRC Thm 1 / split conformal as template; `digest_angelopoulos_crc.md`).
  - Goal (iii) instrument: randomized map $\tilde\theta(\mathcal{D};\xi)$ that restores (1) **without** recalibrating $\mathcal{C}$ (W5).
  - Inverse-opt / inverse-CRC literature as **geometry hints only** (CREDO Lemma 1 / Cor. 2; CREME inverse CRC — methods digests). Do not import $\pi_\varepsilon$, $\pi^{-1}$, $z^*_\lambda$, decision-risk, or CREME Algo 1 as live objects.

- **Stability notion (target for Part I → (iii))**
  - Need the **selection law** $\mathcal{D}\mapsto\tilde\theta(\mathcal{D};\xi)$ to be stable enough that plugging $\tilde\theta$ into (1) does not inflate miscoverage (Zrnic–Jordan Def. 2 / Thm 2 pattern; or LOO displacement of (2) small in Part I).
  - Noise $\xi$ is the design lever. **Isotropic** noise in ambient $\theta$ wastes budget on directions that never flip the argmin of (2). **Structured** noise concentrates mass on directions that change active constraints / first-order optimality of (2).

- **Conclusion (pattern claim)**
  - Inverse optimization flips the map: optimality of a point $\Leftrightarrow$ data/parameters lie in a region defined by competitors (CREDO Lemma 1 analogy; LP halfspaces in CREDO Cor. 2). For (2), the analogous object is the **critical cone / sensitivity subspace** of the KKT system of (2) w.r.t. perturbations of $(\hat f,\hat g)$ or of $\mathcal{D}$.
  - Therefore: sample $\xi$ in that structured subspace (or soft-argmin thickening), solve a randomized version of (2), report $\mathcal{C}(X;\mathcal{D},\tilde\theta)$ with the **same** fixed-$\theta$ construction as in (1).
  - Goal (ii) foil: CREME Cor. 3.9 $\Delta(g,P)$ — size of post-hoc gap tracks how aggressively selection couples to $\mathcal{D}$; structured randomization aims to shrink that coupling **at the selector**, not by re-estimating risk on a split (CREME Algo 1 = CONTRAST).

- **Transfer to (2)→$\hat\theta$ — candidate forms affecting selection only**

  | Candidate $\tilde\theta(\mathcal{D};\xi)$ | Structure (vs isotropic) | Touches $\mathcal{C}$? |
  | --- | --- | --- |
  | **Noisy objective:** $\min_\theta \hat f(y;\theta)+\langle\xi,\theta\rangle$ s.t. $\hat g(\theta)\le 0$, with $\xi$ supported on span of $\nabla\hat f$ / reduced Hessian eigenvectors of large curvature | Linear functionals that move the argmin; scale $\|\xi\|$ from Part I LOO Lipschitz | No |
  | **Noisy constraints:** $\hat g_j(\theta)\le \xi_j$ or $\hat g(\theta)+\xi\le 0$ with $\xi$ on active-set normals | Perturbs binding constraints of (2) only | No |
  | **Soft / $\varepsilon$-near argmin sample:** draw $\tilde\theta$ from $\{\theta:\hat f\le\hat f(\hat\theta)+\varepsilon,\hat g\le 0\}$ (CREDO $\varepsilon$-argmin analogy; quarantine $\pi_\varepsilon$ symbol) | Uniform / exp weights on suboptimality; $\varepsilon$ = stability budget | No |
  | **Structured bootstrap of $(\hat f,\hat g)$:** resample / reweight $\mathcal{D}$ along directions that change empirical risk gradients of $\hat f,\hat g$, then re-solve (2) | Noise in **data functional** space that (2) actually sees | No |
  | **Inverse-sensitivity shaping:** estimate local inverse map $\delta\hat\theta \approx J^\dagger \delta u$ for perturbation $u$ of $(\hat f,\hat g)$; set $\xi\sim$ law pushed through $J^\dagger$ | Explicit inverse-opt linearization; anisotropic in $\theta$ | No |
  | Isotropic $\tilde\theta=\hat\theta+\xi$, $\xi\sim N(0,\sigma^2 I)$ | **Baseline / often wasteful** — keep only as ablation | No |
  | Recompute conformal quantile / CRC $\hat\lambda$ / CREME split $\hat\alpha^{(2)}$ after seeing $\hat\theta$ | — | **YES → forbidden for (iii)** |

- **Non-transfer (do-not-import)**
  - Do **not** import CREDO decision-risk $\hat\alpha(z)$, inverse feasible region, or generative conformal balls as equations in `formal/`.
  - Do **not** import CREME Pareto frontier, $I_\lambda$/$R_\lambda$, or Algo 1 holdout recalibration as the (iii) mechanism (`digest_creme_cream_methods_only.md` §3 CONTRAST).
  - Do **not** treat inverse CRC Def. 3.3 as a replacement for (1); it estimates risk at a fixed index, it does not define our $\mathcal{C}$.
  - Do **not** answer (iii) by inflating $\alpha$ inside $\mathcal{C}$ (Zrnic–Jordan $e^\eta$ CI widening is a **certificate**, not the W5 procedure).
  - Do **not** expand the selected object beyond $\hat\theta$ from (2).
