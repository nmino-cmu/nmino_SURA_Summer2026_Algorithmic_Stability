# Pattern: noise ⇒ stability ⇒ validity

**Sources mined here:** Zrnic & Fithian, *A Flexible Defense Against the Winner’s Curse* (arXiv:2411.18569) — especially §1.3 randomized approaches + main zoom pipeline as **contrast**; pointers [18,22,16,13,15] therein. Companion stability paper (Zrnic & Jordan 2023) is the formal “stability ⇒ validity” engine cited as [22].

**Project ceiling:** goal (iii) = data-randomize the **selection** of \(\hat\theta\); **no** recalibration of uncertainty set \(\mathcal{C}\).

---

## Pattern card

### Pattern: Noise ⇒ stability ⇒ validity (selection-side)

| Slot | Content |
| --- | --- |
| **(a) Inputs / hypotheses** | Data \(\mathcal{D}\); a selection map \(A\) producing a chosen object (winner index, model, or — for us — \(\hat\theta\)); optional independent noise \(\xi\) or a data split/thinning; a baseline inferential set \(\mathcal{C}\) that is valid when the target is **prespecified** (not data-dependent). |
| **(b) Stability notion** | Selection that is **insensitive** to small data perturbations (algorithmic stability), or **softened** by explicit noise / splitting so the selected object is a “noisy winner” rather than hard \(\arg\max\) (Zrnic–Fithian §1.3). Stability may be LOO / neighboring-dataset, or induced by the law of \(\xi\). |
| **(c) Inference / validity conclusion** | If selection is stable (or randomized enough), post-selection coverage of a **fixed** \(\mathcal{C}\) (or a mild inflation derived from the stability parameters) holds; alternatively, randomized-response / split designs restore selective-inference validity without polyhedral conditioning. Certificate form depends on the cited tool ([22] stability; [18] randomized response; [16,13,15] split/fission/thin). |
| **(d) Transfer to (2) → \(\hat\theta\)** | Replace hard \(\hat\theta(\mathcal{D})=\mathrm{argmin}\) of constrained opt (2) by a **randomized selection** \(\tilde\theta(\mathcal{D};\xi)\) (or split-based analogue) so that plugging into **unchanged** \(\mathcal{C}(\cdot,\alpha)\) in (1) recovers a validity guarantee. Noise may be isotropic or **structured** (later: inverse-opt pattern). Part I LOO stability of (2) quantifies how much noise is needed when competitors are close. |
| **(e) Non-transfer / do-not-import** | Do **not** import zoom / LSI / hybrid / Bonferroni **reallocation of the inferential budget** as the answer to (iii). Do **not** redefine the live problem as “CI for the winner among \(m\) means.” Do **not** expand to general \(\hat S\) selection frameworks as co-equal problem statements. |

**One-line chain:**
\[
\underbrace{\xi\text{ or split on selector}}_{\text{noise}}
\;\Longrightarrow\;
\underbrace{\text{soft / stable }\tilde\theta}_{\text{stability}}
\;\Longrightarrow\;
\underbrace{P(\text{truth}\in\mathcal{C}(\cdot;\tilde\theta))\ge 1-\alpha}_{\text{validity, }\mathcal{C}\text{ frozen}}.
\]

---

## Hooks for W5: data-randomize **selection** (not \(\mathcal{C}\))

Concrete hooks extractable from the Winner’s Curse paper **as pointers**, not as zoom-method imports:

1. **Noisy winner (explicit).** Zrnic–Fithian §1.3: add noise or split data → select a noisy analogue of \(\arg\max\) → trade selection quality for inferential power. Map: \(\tilde\theta(\mathcal{D};\xi)\) instead of \(\hat\theta(\mathcal{D})\); report validity of the **same** \(\mathcal{C}\) at \(\tilde\theta\).

2. **Stability bridge ([22] cited).** Algorithmic stability of the selection map is the measurable intermediate between noise and coverage. For us: prove / enforce LOO (or noise-induced) stability of the map \(\mathcal{D}\mapsto\theta\) from (2), then lift to (1) without touching \(\mathcal{C}\)’s scores/thresholds.

3. **Split / fission / thin ([16],[13],[15]).** Use one share of data (or a thinned view) to **select** \(\tilde\theta\), the other to justify that \(\mathcal{C}\) remains valid — again selection-side randomization / information partition, not recalibrating \(\mathcal{C}\).

4. **Cost accounting (keep visible).** Expected cost of W5 path: \(\tilde\theta\) may be suboptimal relative to hard \(\hat\theta\) (selection quality ↓). That is the legitimate price; **width of \(\mathcal{C}\)** should not be the dial we turn for (iii).

5. **Effective multiplicity (diagnostic only).** Zoom’s adaptivity message — hard when many near-ties, easy when one clear winner — is a **Part I diagnostic**: when gaps in (2)’s objective are large, little randomization may suffice; when many \(\theta\) compete, need more noise / stronger stability. Do not implement zoom radii as the fix.

---

## RED LINE (goal (iii)) — contrast only

Procedures that **recalibrate scores, thresholds, radii, or \(\alpha\)-splits of \(\mathcal{C}\)** (or of a simultaneous parent region that defines \(\mathcal{C}\)) are **OUT** as answers to goal (iii).

| Method (in Winner’s Curse paper) | Why it is OUT for (iii) | Allowed use here |
| --- | --- | --- |
| **Zoom correction** (Thm. 3.1, 4.1) | Exact \(\arg\max\); validity via inverting zoom test / projecting simultaneous region — **inference recalibration** | Contrast exemplar of the forbidden dual path |
| Bonferroni / full simultaneous | Widens all intervals (union-bound \(\alpha/m\)) | Contrast: multiplicity paid inside \(\mathcal{C}\) |
| LSI [21], hybrid [2], SoS [3] | Error-budget splits / conditional corrections of intervals | Contrast / related-work only |
| Near-winner outer sets (Prop. 5.3) | Still projections of the simultaneous \(\widehat{\mathcal{C}}\) | Contrast: softens *reporting*, not selection of \(\hat\theta\) from (2) |

**Author quote locking the fork (§1.3):** randomized methods select a noisy winner (selection-side); *“We focus on exact, non-randomized selection of the winner”* (inference-side correction). W5 chooses the **other** fork.

---

## Minimal glossary (paper → our notation)

| Zrnic–Fithian | Our use |
| --- | --- |
| \(X_i\), \(\theta_i\), \(\hat\imath\) | Competing scores / candidate \(\theta\); data-driven choice |
| Simultaneous \(\widehat{\mathcal{C}}^\alpha\), projected \(\widehat{\mathcal{C}}^\alpha_{\hat\imath}\) | **Not** our frozen \(\mathcal{C}\) — different object; do not rename |
| Noisy winner via \(\xi\) / split | \(\tilde\theta(\mathcal{D};\xi)\) — W5 selection randomization |
| Active radius \(r_\alpha(\Delta)\) | Width dial on inference — **OUT** for (iii) |

---

## Citation anchors

- Zrnic & Fithian (2024), arXiv:2411.18569 — zoom method (contrast); randomized-family paragraph §1.3.
- Zrnic & Jordan (2023), AoS — stability ⇒ post-selection inference [22].
- Tian & Taylor (2018); Rasines & Young (2023); Leiner et al. (2023); Neufeld et al. (2024) — noise / split mechanisms [18,16,13,15].
