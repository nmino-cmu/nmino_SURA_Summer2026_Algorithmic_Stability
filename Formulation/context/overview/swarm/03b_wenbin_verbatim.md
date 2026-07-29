# Wave 1 — Wenbin verbatim extract

Agent: [Wenbin H2 intent](ed36c74f-274b-4158-90ef-9e2fc1b609de)

# Forensic Report: Wenbin Problem Setup

**Sources only:** `Algorithmic_Stability_Wenbin_Problem_Setup.pdf` (7 pages) + Wenbin July 2 email in `Advisor_Email_Record_Research_Direction.tex`. Nothing else used.

---

## Verbatim Wenbin comments

Exact `[Wenbin]:` strings from the PDF (cyan/blue attribution tags):

**W1 (p.1, §1 Introduction)**
> `[Wenbin]: The problem we study falls in the intersection of post-hoc inference, algorithm stability, and optimization theory.`

**W2 (p.3, before Figure 1 / UQ writeup)**
> `[Wenbin]: The post-hoc inference problem is itself very general. We need to narrow the structure of the problem by focusing on one specific objective (e.g., uncertainty quantification). See below for an example setting that I wrote.`

**W3 (p.3, after goals (i)/(ii)/(iii))**
> `[Wenbin]: This objective is a mix of algorithm stability, post-hoc inference, and optimization theory. I believe that we should decompose the question into two main parts: first, study the stability of constrained optimizations (i.e., if the dataset changes by one data point, how much does the output of the optimization change? Do we need to make any structural assumptions on the optimization problems, like how ˆf and ˆg are learned from the data D?). Second, study post-hoc inference on top of these results.`

**W4 (p.3)**
> `[Wenbin]: We may modify the problem setting along the way if we find there are more principal versions of it.`

**W5 (p.3, above footnote)**
> `[Wenbin]: Data-driven policy (e.g., PTO), no recalibration, strategy: data-randomize to achieve validity guarantee, this answers (iii). Our paper: structured noise, depends on inverse optimization. Post-inference Tijana (Winner’s Curse, Algorithm Stability).`

No other `[Wenbin]:` tags appear on pages 2, 4, 5, 6, or 7.

---

## Formal problem (equations transcribed carefully)

### A. Broad selection / stabilization framing (§2, pp.1–2; not tagged `[Wenbin]`)

Observed data:
\[
D = (Z_1,\ldots,Z_n),\qquad Z_1,\ldots,Z_n \overset{\text{i.i.d.}}{\sim} P,
\]
with \(P\) “an unknown population distribution.”

Selection:
\[
\hat{S} = A(D)
\]
(“\(A\) be a data-dependent selection algorithm”; “selected object”).

Stabilized selection:
\[
\tilde{S} = \tilde{A}(D;\xi)
\]
where “\(\tilde{A}\) is the stabilized selection algorithm, \(\tilde{S}\) is the stabilized selected object, and \(\xi\) represents additional randomness or another stabilizing device.”  
Quote on \(\xi\): “noise, subsampling randomness, randomized optimization perturbation, privacy randomness, or another source of algorithmic randomization.”

Target guarantee (displayed, unnumbered):
\[
\mathbb{P}\big(\theta_{\tilde{S}} \in C_{\tilde{S}}(D)\big) \ge 1-\alpha
\]
In words (quote): “after using the data to select an object, the confidence set reported for that selected object should contain its true parameter with probability at least \(1-\alpha\)”.

Framework aim (quote): “finding a general framework for post-hoc selection algorithms to convert a selection algorithm into a stable selection algorithm” / “sufficiently and certifiably stable for valid downstream inference or evaluation.”

### B. Wenbin’s UQ example setting (p.3; introduced by W2 as “an example setting that I wrote”)

Setting (quote): “a post hoc inference setting in uncertainty quantification problems, where the hyperparameter \(\theta\) is determined via optimization using shared calibration data.”

Uncertainty set notation as written:
> “Let \(\mathcal{C}(X; \mathcal{D}, \alpha)\) denote an uncertainty set constructed with dataset \(\mathcal{D}\) and input hyperparameter \(\theta\).”

**Validity assumption / Eq. (1):**
\[
\mathbb{P}\big(Y \in \mathcal{C}(X; \mathcal{D}, \theta)\big) \ge 1-\alpha. \tag{1}
\]
Quote: “Assume that the uncertainty set satisfies validity, i.e., for any given \(\mathcal{D}\) and prespecified \(\theta\), there is [Eq. (1)].”

**Constrained optimization / Eq. (2):**
> “Suppose there exist two functions \(\hat{f}\) and \(\hat{g}\) that are dependent on \(\mathcal{D}\), and that they jointly form a constrained optimization problem that determines a hyperparameter \(\theta\):”
\[
\pi:\quad \min_{\theta}\ \hat{f}(y;\theta)\quad\text{s.t.}\quad \hat{g}(\theta)\le 0. \tag{2}
\]
> “Let \(\hat{\theta}(\mathcal{D})\) denote the output of (2).”

**Footnote 1 (quote):**
> “Using filtration notations, \(\sigma(\hat{f})\subseteq\sigma(\mathcal{D})\) and \(\sigma(\hat{g})\subseteq\sigma(\mathcal{D})\).”

**Goals (i)/(ii)/(iii) — exact quote:**
> “Our goal is to investigate: (i) the conditions when (1) still holds when \(\hat{\theta}(\mathcal{D})\) is plugged in for \(\theta\) and (ii) if not, what is the deviation between the nominal miscoverage and the actual miscoverage, and (iii) what kind of procedure can be deployed to recalibrate the uncertainty set to satisfy (1).”

**Figure 1 labels (as printed):** “Validity”, “Dataset”, “Hyperparameter”, “Uncertainty set”, “Optimization”; caption: “Figure 1: Illustration of the problem setting.”

### C. Section 3 scaffolding (pp.4–7; empty bodies except 3.1)

Headings only (mirroring W3’s two-part split):
- `3 Working Formalization: Stable Post-Hoc Inference for Optimization-Selected Policies`
- `3.1 Introduction` — filled paragraph (optimization-based variant of §2 prose; typo “genedoral”)
- `3.2 Common Setup` — empty
- `3.3 Part I: Stability of the constrained optimizations` / `3.3.1 Problem Formulation` — empty
- `3.4 Part II: Post-hoc inference after stable selection` / `3.4.1 Problem Formulation` — empty

---

## Explicit directives

### From `[Wenbin]:` comments (PDF)

| Directive | Exact quote |
|---|---|
| Narrow scope | “We need to narrow the structure of the problem by focusing on one specific objective (e.g., uncertainty quantification).” |
| Treat UQ writeup as his example | “See below for an example setting that I wrote.” |
| Decompose into two parts | “I believe that we should decompose the question into two main parts: first, study the stability of constrained optimizations … Second, study post-hoc inference on top of these results.” |
| Stability question to study | “if the dataset changes by one data point, how much does the output of the optimization change?” |
| Structural assumptions question | “Do we need to make any structural assumptions on the optimization problems, like how \(\hat{f}\) and \(\hat{g}\) are learned from the data \(D\)?” |
| Setting may change | “We may modify the problem setting along the way if we find there are more principal versions of it.” |
| Path for (iii) (his note) | “Data-driven policy (e.g., PTO), no recalibration, strategy: data-randomize to achieve validity guarantee, this answers (iii).” |
| Paper / method pointer | “Our paper: structured noise, depends on inverse optimization.” |
| Related pointer | “Post-inference Tijana (Winner’s Curse, Algorithm Stability).” |

### From July 2 email (cross-check)

Wenbin → Nick, Thu Jul 2, 2026 12:53 PM (exact):

> “I drafted a version of the problem setup in the Overleaf project, which aligns closer to what we intended. Please feel free to give it a read and let me know if you have any questions. If not, you may begin brainstorming the methodologies we could use to approach this problem and write them down in the draft. We can discuss them next time we meet.”

Also exact: “Nice talking to you on Monday, and I am glad to see that we are making good progress.”

Nick’s Jul 3 reply (context only, not Wenbin want): “Thank you for drafting the problem setup. I will read through it carefully and start brainstorming possible methodologies to add to the draft.”

---

## Incomplete stubs

| Location | What is empty / unfinished | Exact remnant |
|---|---|---|
| Abstract | Stub | “TBA” |
| p.2 after guarantee | Informal todo dump (typos intact) | “Define more formally, including \(\theta_S\) Define the policy as the solution to an optimziation problem Policy: take input (context variable) ,... Formally define the stability of the policy induced by the optmization problem find stabilization mechnaism” |
| p.2 | Application stub | “Application: ask any AI system what is the prediciton of a certain quantitiy: \"I want to know what ht stock price is for apple tomorrow\"" |
| p.2 | Truncated line | “Think of an application: se” |
| §3.2 | Heading only | “3.2 Common Setup” |
| §3.3 / 3.3.1 | Heading only | “Part I: Stability of the constrained optimizations” / “Problem Formulation” |
| §3.4 / 3.4.1 | Heading only | “Part II: Post-hoc inference after stable selection” / “Problem Formulation” |
| Eq. (1) definition vs use | Notation unfinished / inconsistent | def uses \(\mathcal{C}(X;\mathcal{D},\alpha)\); Eq. (1) uses \(\mathcal{C}(X;\mathcal{D},\theta)\) |

---

## Authority notes

### (A) Wenbin-authored requirements

- All five `[Wenbin]:` comments (W1–W5).
- The UQ formal block he attributes to himself: “an example setting that I wrote.”
- July 2 email: Overleaf setup “aligns closer to what we intended”; Nick may “begin brainstorming the methodologies… and write them down in the draft.”

### (B) Shared draft text (unattributed body; not tagged `[Wenbin]`)

- Title/authors/affiliation.
- §2 broad selection/stabilization prose and \(\hat{S}/\tilde{S}/\xi\) mathematics through the \(\mathbb{P}(\theta_{\tilde{S}}\in C_{\tilde{S}}(D))\ge 1-\alpha\) display.
- The black-text UQ paragraphs and Eqs. (1)–(2) / goals (i)–(iii) (presented as the body under W2’s “example setting that I wrote,” so content-authority is Wenbin’s claim, but the prose is not cyan-tagged).
- §3.1 paragraph (near-copy of §2 with “optimization-based” inserted; “genedoral”).
- Empty §3 section titles.

### (C) Nick-like leftover notes (if any)

Strongest candidates on **p.2** only — informal, typo-dense, truncated, no `[Wenbin]:` tag:
- “optimziation” / “optmization” / “mechnaism” / “prediciton” / “quantitiy” / “ht stock price” / “Think of an application: se”
- Abstract “TBA”
- Empty §3.2–3.4 bodies (structure exists; content does not)

PDF does **not** label those p.2 lines as Nick’s. Attribution is inferential from style/typos vs cyan `[Wenbin]:` tags — stated as such, not as proven authorship.

---

## Open ambiguities in Wenbin’s own text

1. **Goal (iii) vs W5 — direct conflict (do not soften)**  
   - Body: “(iii) what kind of procedure can be deployed to **recalibrate** the uncertainty set to satisfy (1).”  
   - W5: “**no recalibration**, strategy: data-randomize to achieve validity guarantee, **this answers (iii)**.”

2. **Uncertainty-set argument slot**  
   Definition: “\(\mathcal{C}(X; \mathcal{D}, \alpha)\)” … “input hyperparameter \(\theta\)”.  
   Eq. (1): “\(\mathcal{C}(X; \mathcal{D}, \theta)\)”.  
   Third argument is \(\alpha\) in the definition sentence and \(\theta\) in (1).

3. **How binding is the UQ example?**  
   W2: “focusing on one specific objective **(e.g., uncertainty quantification)**” + “**example** setting that I wrote” + W4: “We may modify the problem setting… more principal versions.”  
   UQ is framed as narrowing example, not as irrevocable final problem.

4. **\(\hat{f}(y;\theta)\) lowercase \(y\) vs \(Y\) in (1)** — unresolved in Wenbin’s equations.

5. **W5 fragments without expansion**  
   “Data-driven policy (e.g., PTO)”, “Our paper: structured noise, depends on inverse optimization”, “Post-inference Tijana (Winner’s Curse, Algorithm Stability)” — named, not defined in this PDF.

6. **Two parallel framings left side-by-side**  
   Broad \(\tilde{A}(D;\xi)\) / \(\theta_{\tilde{S}}\in C_{\tilde{S}}(D)\) setup (pp.1–2) vs UQ \(\hat{\theta}(\mathcal{D})\) / \(\mathcal{C}(X;\mathcal{D},\theta)\) setup (p.3). W2 says to narrow; the broad §2 text is not deleted.

7. **§3 titles vs empty bodies**  
   Headings encode W3’s two-part decomposition (“Part I: Stability of the constrained optimizations”; “Part II: Post-hoc inference after stable selection”) but contain no formulations.

8. **July 2 vs PDF**  
   Email authorizes methodology brainstorming for “this problem” / Overleaf setup; it does **not** resolve the recalibration vs no-recalibration conflict or fill §3 stubs.