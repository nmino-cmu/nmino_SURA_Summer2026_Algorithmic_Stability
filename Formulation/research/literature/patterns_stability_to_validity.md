## Pattern: Stable selector ⇒ valid post-selection inference

- **Inputs**
  - Data $y\sim P_y$ (writeup: calibration $\mathcal{D}$).
  - Classical family of inferential objects indexed by a *fixed* selection / hyperparameter $S$ (resp. $\theta$): intervals $\mathrm{CI}^{(\alpha)}_S$ with $\mathbb{P}\{\beta_S\notin\mathrm{CI}^{(\alpha)}_S\}\le\alpha$ (Zrnic–Jordan, PDF p.7), or validity (1) $\mathbb{P}(Y\in\mathcal{C}(X;\mathcal{D},\theta))\ge 1-\alpha$ for prespecified $\theta$.
  - A (possibly randomized) selection map $\hat S=A(y)$ that chooses the index of the target (writeup: $\hat\theta(\mathcal{D})$ from constrained opt (2) only).
  - User-chosen stability budget $(\eta,\tau,\nu)$ and error split $\delta$ (Thm 2: overall bound $\delta+\tau+\nu$).

- **Stability notion**
  - **Def. 1 (PDF p.6):** $(\eta,\tau)$-indistinguishability $Q\approx_{\eta,\tau}W$ via max-divergence: $\mathbb{P}\{Q\in O\}\le e^\eta\mathbb{P}\{W\in O\}+\tau$.
  - **Def. 2 (PDF p.6):** $A$ is $(\eta,\tau,\nu)$-stable w.r.t. $P_y$ if $\exists$ oracle $A_0$ (may depend on $P_y$, not on realized $y$) with $\mathbb{P}\{\omega:A(\omega)\approx_{\eta,\tau}A_0\}\ge 1-\nu$.
  - Achieved by **randomizing the selection** (Laplace / report-noisy-max / noisy Frank–Wolfe; PDF §2 Claims 1–4, §8 Algs 2–3), not by leave-one-out loss stability.
  - Closed under post-processing and composition (PDF §8.1; Suppl. Lemmas 3–4).

- **Conclusion**
  - **Lemma 1 (PDF p.7, Eq. (1)):** $(y,\hat S(y))\approx_{\eta,\tau+\nu}(y,\hat S_0)$ with $\hat S_0\perp y$.
  - **Theorem 2 (PDF p.7–8):** $\mathbb{P}\{\beta_{\hat S}\notin\mathrm{CI}^{(\delta e^{-\eta})}_{\hat S}\}\le\delta+\tau+\nu$.
  - Equivalently: classical construction remains valid after selection iff the **nominal miscoverage is inflated by $e^\eta$** (PoSI: use $K_{\hat M,\delta e^{-\eta}}$, Cor. 1–2, PDF p.10–11).
  - Informal Thm 1 (PDF p.1–2): same pattern with $\tau=\nu=0$ packaging.
  - Conditional cousin: Lemma 2 (PDF p.11–12) — law of $y\mid\hat S=S$ on high-prob. $E$ is at most $e^\eta$-tilted vs law of $y\mid E$.

- **Transfer to (2)→$\hat\theta$**
  - Identify $A(\mathcal{D})\leftrightarrow\hat\theta(\mathcal{D})$: the only selected object is the optimizer of (2); post-process only if the writeup later treats a function of $\hat\theta$ (Zrnic–Jordan post-processing: PDF p.13–14).
  - Part I of the writeup asks leave-one-out movement of $\hat\theta$; this pattern instead asks for **Def. 2 stability of the (randomized) map $\mathcal{D}\mapsto\hat\theta$**. Bridging requires either (a) designing a randomized version of (2) with explicit $(\eta,\tau,\nu)$, or (b) proving that a given randomized policy for (2) meets Def. 2.
  - **Inflation role when plugging $\hat\theta$ into (1):** Thm 2 says the classical object at fixed $\theta$ must be run at level $\delta e^{-\eta}$ (more conservative $\mathcal{C}$ / wider intervals). That is the precise analog of $K_{M,\delta e^{-\eta}}$ and of $\mathrm{CI}^{(\delta e^{-\eta})}$.
  - **Goal (iii) alignment:** keep the *form* of $\mathcal{C}$ fixed (no recalibration) by driving $\eta\to 0$ via **heavier data-randomization of selection**, so $\delta e^{-\eta}\approx\delta$ and (1) with the classical construction remains approximately valid for $\hat\theta$ (PDF p.2–3, p.8: $\eta\downarrow 0$ recovers non-selective intervals). Randomization is the instrument; CI inflation is the certificate when $\eta$ is not negligible.
  - Constrained-opt echo: Stable LASSO (Alg. 2 / Eq. (5), PDF p.15) is itself a randomized constrained program — useful template for randomizing (2), not a license to treat $\hat\theta_{\mathrm{LASSO}}$ as the writeup’s $\hat\theta$ without remapping.

- **Non-transfer (do-not-import)**
  - Do **not** import CREDO/CREME (or other lab decision-risk objects) as the selected target; writeup selected object is only $\hat\theta$ from (2).
  - Do **not** treat Thm 2’s $e^\eta$-inflated / widened $\mathrm{CI}$ as the answer to goal (iii): that is recalibrating the inferential object. Goal (iii) insists on data-randomizing **selection**, leaving $\mathcal{C}$’s calibration rule alone.
  - Do **not** equate Def. 2 with Part I leave-one-out stability of deterministic (2); different metric (max-divergence of selection laws vs $\hat\theta$ movement under LOO).
  - Do **not** import PoSI simultaneity over all models / Scheffé protection (Berk et al.; Prop. 1) as the problem statement — writeup is validity of $\mathcal{C}$ after plugging one $\hat\theta$.
  - Do **not** import OLS sandwich / $t$-PoSI constants, model-support selection $\hat M$, or $\beta_{\hat M}$ as the live estimand unless the writeup is later broadened.
  - Do **not** import MCMC selective pivots / conditional exact LASSO pivots (Lee et al., Tian–Taylor sampling) as required machinery — the pattern’s point is sampling-free corrections via stability parameters alone.
  - Do **not** assume Gaussian $y$ or known $\sigma$ are part of the pattern core; they are instantiation assumptions for Algs 2–3 and Cor. 2. Def. 2 + Thm 2 are distribution-agnostic given classical fixed-$S$ validity.
  - Do **not** treat data splitting’s $f\leftrightarrow\eta$ dictionary (PDF §5.1, Eq. (2)) as mandatory; it is a comparison, not the writeup mechanism.
