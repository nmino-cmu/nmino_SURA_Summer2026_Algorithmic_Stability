# Part I: LOO under strong convexity — proof sketch (tighten)

## Lemma (candidate)
Assume $\Theta\subset\mathbb{R}^d$ convex compact, $\hat f(\cdot)$ $\mu$-strongly convex and $L$-smooth on $\Theta$, unique unconstrained minimizer in the relative interior of the feasible set $\{\hat g\le 0\}$ (or active-set stable under LOO), and
\[
\sup_{\theta}\|\nabla\hat f_D(\theta)-\nabla\hat f_{D^{(i)}}(\theta)\|\le L_{\mathrm{LOO}}.
\]
Then $\Delta_{\mathrm{LOO}}:=\max_i\|\hat\theta(D)-\hat\theta(D^{(i)})\|\le (2/\mu) L_{\mathrm{LOO}}$.

## Sketch
1. Let $\theta=\hat\theta(D)$, $\theta'=\hat\theta(D^{(i)})$.
2. Strong convexity: $\langle\nabla\hat f_D(\theta)-\nabla\hat f_D(\theta'),\theta-\theta'\rangle\ge\mu\|\theta-\theta'\|^2$.
3. First-order optimality (interior case): $\nabla\hat f_D(\theta)=0$, $\nabla\hat f_{D^{(i)}}(\theta')=0$.
4. Then $\langle\nabla\hat f_D(\theta')-\nabla\hat f_{D^{(i)}}(\theta'),\theta-\theta'\rangle\ge\mu\|\theta-\theta'\|^2$ after algebra using $\nabla\hat f_D(\theta)=0=\nabla\hat f_{D^{(i)}}(\theta')$.
5. Bound LHS by $L_{\mathrm{LOO}}\|\theta-\theta'\|$ ⇒ claim.
6. **Gap:** constrained case needs active-set stability / KKT residual bound (OPEN). Soft-argmin / noisy-objective versions replace hard FOC (agent in flight).

## Status
Interior unconstrained sketch OK; constrained (2) needs active-set hyp. Demo: deferred until noisy-obj rates land.
