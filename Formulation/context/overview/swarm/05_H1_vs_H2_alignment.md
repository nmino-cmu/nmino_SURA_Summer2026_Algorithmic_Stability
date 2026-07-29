# Wave 1 — H1 vs H2 alignment

Agent: [H1 vs Wenbin](ea67839c-8d87-46b2-adcd-491ce02eb2b6)

# H1 vs Wenbin H2: Alignment Report

**Verdict:** H1 is a broad *example harvest* toward a hoped-for modular stability calculus. Wenbin H2 already **rejects that breadth** and pins the problem to **UQ + constrained-opt hyperparameter selection**. Treating H1 as a “universal composable framework” draft overclaims what the survey itself carefully denies—and what the advisor has already narrowed away from.

---

## 1. What H1 claims the research aim is

From Abstract + Intro + Scope:

- **Not** a full survey of algorithmic stability, DP, or selective inference.
- **Aim:** identify concrete patterns  
  `original selector → stabilized selector → formal certificate → utility/inference cost`
- These examples are **raw material for a possible** composable stability-certification framework for post-hoc selection.
- H1 **explicitly disclaims** that the literature already contains a universal composable framework (“may be possible”).

**Harsh read:** The aim is cataloguing + pattern extraction, not a theorem program. The “framework” is aspirational scaffolding, not the research object Wenbin defined.

---

## 2. Unifying template / notation / “best first theorem”

**Notation (shared surface with Wenbin):**
- \(\widehat S = A(D)\)
- \(\widetilde S = \widetilde A(D;\xi)\) with \(\xi\) = noise / subsample / opt perturbation / privacy randomness / other stabilizer

**Certificate types (heterogeneous, not unified):**
- Algorithmic stability: \(\mathrm{Cert}(\widetilde A)\le\eta\)
- Privacy: \((\varepsilon,\delta)\)-DP
- Post-selection inference: \(\Pr\{\theta_{\widetilde S}\in C_{\widetilde S}(D)\}\ge 1-\alpha\)

**Repeated pattern:**
```
primitive + mechanism + proof strategy  ⇒  certificate  @  utility/inference cost
```

**Proposed “best first theorem” (H1 §8.4 — proposed, not proved):**  
A **heterogeneous / gap-aware noisy argmax / top-\(k\)** bound that maps candidate-specific sensitivity, gaps, and noise scales → \(\eta\)-style stability → plug into a post-selection CI correction (Zrnic–Jordan + private top-\(k\) + GAP-MAX).

**Harsh read:** That “first theorem” optimizes a **DP/winner-selection** unification story. Wenbin’s first theorems should be about **stability of constrained programs** \(\min \hat f\) s.t. \(\hat g\le 0\) and **UQ validity / recalibration** when \(\hat\theta(D)\) is plugged in—not gap-aware noisy max.

---

## 3. Taxonomy of primitives / mechanisms

### Primitives (H1 §8.1)
1. Noisy scalar release  
2. Noisy argmax  
3. Noisy top-\(k\)  
4. Noisy threshold  
5. Validation comparison for selective inference  
6. DP validation / tuning  
7. Support / model selection  
8. Randomized optimization / ERM  
9. Subsample aggregation  
10. Private candidate selection  
11. Reusable holdout  
12. Iterative atom selection  
13. Best-arm selection  

### Mechanisms (H1 §8.2)
1. Laplace noise  
2. Gaussian noise  
3. Gumbel noise  
4. Exponential mechanism  
5. Objective perturbation  
6. Output perturbation  
7. Subsampling / frequency  
8. Sparse vector  
9. Private candidates  
10. Regularization  

### Proof-strategy taxonomy (H1 §8.3)
Density-ratio bounds; sensitivity calibration; EM utility analysis; coupling (one-shot top-\(k\)); sparse-vector accounting; adaptive composition / post-processing; max-information transfer; selective likelihood conditioning; strong convexity / optimizer sensitivity; selection-frequency bounds.

---

## 4. Where H1 alignment with Wenbin H2 is **strong**

| Shared idea | Evidence |
|---|---|
| Same high-level story | Data → data-dependent selection → reuse induces dependence → stabilize to reduce/avoid splitting |
| Same objects | \(A(D)\), \(\widetilde A(D;\xi)\), post-selection coverage target |
| Same triangle | Post-hoc inference ∩ algorithmic stability ∩ optimization |
| Closest literature match | Zrnic & Jordan (2023): stability certificate → CI correction; Wenbin flags “Post-inference Tijana (Winner’s Curse, Algorithm Stability)” |
| Randomize-to-validity strategy | Wenbin: data-randomize for validity (answers (iii)); H1’s core examples are randomized selectors |
| Optimization-touched examples | Tian–Taylor, Huang (randomized objectives), Markovic (randomized quality vectors), Chaudhuri ERM perturbation, Bousquet/Hardt stability as opt primitives |
| Decomposition intuition | Wenbin: Part I stability of constrained opt, Part II post-hoc inference; H1’s “certificate then inference bridge” is the same *shape* (even if wrong *object*) |

---

## 5. Where H1 **diverges** or is **too general** vs Wenbin’s UQ + constrained-opt setup

Wenbin’s narrowed object (H2 p.3):

1. UQ set \(C(X;D,\theta)\) with **validity for fixed \(\theta\)**.
2. Hyperparameter \(\hat\theta(D)\) from **constrained opt**  
   \(\pi:\ \min_\theta \hat f(\cdot;\theta)\ \mathrm{s.t.}\ \hat g(\theta)\le 0\).
3. Questions: (i) does validity survive \(\hat\theta(D)\)? (ii) miscoverage deviation? (iii) recalibration / stabilization procedure?
4. Explicit two-part program: **stability of constrained optimizations** (leave-one-out change of \(\hat\theta\)), then **post-hoc inference**.
5. Preferred lever: **structured noise / inverse optimization** for data-driven policies (e.g. PTO), not a zoo of generic selectors.

**H1 failures relative to that:**

| Wenbin needs | H1 actually does |
|---|---|
| One application class: UQ + constrained hyperparameter selection | Dozens of selectors: winners, features, top-\(k\), arms, leaderboards, holdouts, DP candidates… |
| Stability theory for \(\hat f,\hat g\) learned from \(D\) and the constrained map \(\theta\mapsto\hat\theta\) | Almost no constrained-opt LOO sensitivity; “randomized optimization” appears as SI gadgets, not Part-I theory |
| Recalibration of uncertainty sets after data-driven \(\theta\) | Mostly selection certificates (DP / PFER / \(\eta\)-stability); UQ-after-hyperparameter-opt is not the organizing target |
| Structured / inverse-opt noise | Mostly Laplace/Gaussian/EM/Gumbel on scores or objectives |
| Narrow scope by design | Explicitly flirts with a **modular calculus for heterogeneous pipelines** |

**Harsh:** H1’s “composable framework” language is exactly the generality Wenbin told you to cut (“post-hoc inference is itself very general… narrow… uncertainty quantification”). If H1 is treated as research direction rather than literature scrapbook, it is **misaligned**.

---

## 6. What remains useful under Wenbin’s program vs what is distraction

### Keep (high value under H2)
- **Zrnic–Jordan:** \(\eta\)-stability → CI inflation / correction. Best existing *inference bridge* for “stabilize selector → valid coverage.”
- **Randomized selective inference** (Tian–Taylor, Huang, Markovic): closest to “perturb optimization / selection statistics, then do valid post-selection inference.”
- **Objective / output perturbation + regularized-ERM / SGD stability:** templates for **optimizer sensitivity** (Part I raw material)—even though H1 demotes them as non-selectors.
- **Composition / post-processing language:** useful once you have a constrained-opt stability certificate.
- **Shared notation + “avoid splitting by stabilizing selection” motivation.**
- **Baselines:** sample splitting; non-randomized winner/PoSI corrections as alternatives to randomizing the selector.

### Keep lightly (maybe later, not core)
- Private candidate / HPO privacy accounting (Liu–Talwar, Papernot–Steinke, Chaudhuri–Vinterbo): only if the selected object is literally a hyperparameter *and* privacy is a goal—Wenbin’s stated goal is **validity of UQ**, not DP.
- Gap-aware selection analyses: only if your constrained program has identifiable score/gap structure.

### Distraction under Wenbin’s program (cut or quarantine)
- **Entire DP top-\(k\) / EM / permute-and-flip / GAP-MAX / Lipschitz-mechanism zoo** — mature selection primitives for privacy, not constrained-opt UQ.
- **Stability selection / CPSS / Bolasso / cluster SS** — feature-set error control (PFER etc.), not hyperparameter-UQ validity.
- **Best-arm identification** — wrong object class.
- **Ladder / Thresholdout / Sparse Vector as main story** — adaptive analytics / holdout reuse, not \(\hat\theta\) from constrained calibration.
- **“Best first theorem = gap-aware noisy argmax/top-\(k\)”** — wrong first theorem for Wenbin.
- **“Modular calculus for broad heterogeneous pipelines”** — overclaim; advisor already narrowed.

---

## Bottom line

| Document | Role |
|---|---|
| **H1** | Useful **literature inventory** of how people stabilize selectors and bridge to inference. |
| **Wenbin H2** | Actual **problem definition**: UQ validity after constrained, data-dependent \(\hat\theta\); Part I = constrained-opt stability; Part II = post-hoc inference / recalibration; mechanism bias toward structured / inverse-opt noise. |

H1 aligns on **surface formalism** and on **Zrnic–Jordan-style bridges**. It **fails as a research plan** if read as building a universal composable stability framework: that is broader than Wenbin’s setup, and most of H1’s taxonomy is orthogonal filler relative to constrained-opt UQ.