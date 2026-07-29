# Wave 3 — Implementation / patch judge

Agent: [Patch author](285ddf86-28d0-4338-be00-be9b10e9f0ff)

# PATCH SPEC — `Research_Scope_Timeline_and_Authority.tex`

**Judge basis:** SAME-LINEAGE-UNPROVEN (H2 ≠ proven July 2 Overleaf); layered authority; (iii) vs Comment E unresolved mid-edit; idea-status vocabulary; `papers/` packaging; H2 hybrid authorship; \(C(X;D,\alpha)\) vs \(\theta\) bug.

---

## 1. Sections to rewrite (old → new)

### 1.1 `papers/` bullet — context tree (§What this context tree is for)

**OLD:**
```latex
  \item \texttt{papers/} --- reading library (priority / lab / background / tangential); not the
        problem formulation itself.
```

**NEW:**
```latex
  \item \texttt{papers/} --- reading library (priority / lab / background / tangential).
        Priority and pivot papers are in-scope for the evolution story; PDFs live here and are
        not duplicated into \texttt{history/}.
```

---

### 1.2 Out-of-scope `papers/` claim

**OLD:**
```latex
  \item The \texttt{papers/} PDFs themselves beyond citation / role in the timeline
        (they are a library, not formulation history).
```

**NEW:**
```latex
  \item Full-text reproduction of \texttt{papers/} PDFs inside \texttt{history/}
        (library lives in \texttt{papers/}; cite and role-track them here, do not treat absence
        from \texttt{history/} as ``not part of formulation history'').
```

---

### 1.3 Authority hierarchy — replace entire enumerate + central-rule box

**OLD (from `\section{Authority hierarchy...}` through the `\fbox{...}` / Central rule block):**

```latex
\section{Authority hierarchy (read this first)}
When sources conflict, use this order for the \textbf{current mathematical problem}:

\begin{enumerate}[leftmargin=*]
  \item \textcolor{critical}{\textbf{Highest --- Wenbin problem setup}}
        (\texttt{history/Algorithmic\_Stability\_Wenbin\_Problem\_Setup.pdf}).
        Advisor-authored narrowing: post-hoc inference via uncertainty quantification with
        optimization-selected hyperparameter $\hat\theta(D)$; decompose into
        (I)~stability of constrained optimizations and (II)~post-hoc inference on top.
  \item \textbf{Meeting~3 (29 Jun 2026)} --- Woody/Wenbin/Nick: stability of
        optimization-induced policies; AI+optimizer trust as hypothesis testing.
  \item \textbf{Advisor emails} --- especially Wenbin 2~Jul 2026 (Overleaf setup ``aligns closer
        to what we intended'') and June~12 ``post-hoc inference'' terminology.
  \item \textbf{Student working survey}
        (\texttt{history/Algorithmic\_Stability\_Working\_Document.pdf}) --- preserved as the
        stabilized-selection example catalog and primitive taxonomy. It is \emph{not} the
        controlling problem statement where it conflicts with Wenbin's setup.
  \item \textbf{Earlier meetings / student proposals} --- intellectual history only
        (quantization; adaptive regret frontier; sequential-CREAM / solver-error backups).
\end{enumerate}

\medskip
\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%
\textbf{Central rule.} Nick's June~25 primitive-operation / stabilized-selection proposal and the
July~26 working survey motivated discussion and supply raw examples. Wenbin's annotated
problem setup controls what the project is currently trying to prove.
}}
```

**NEW:**
```latex
\section{Authority hierarchy (read this first)}
Do \emph{not} flatten agenda, equations, and methods into one ranked list. Use layers:

\begin{enumerate}[leftmargin=*]
  \item \textcolor{critical}{\textbf{L1 --- Research agenda (Woody / Meeting~3)}}
        Stability of optimization-induced policies; discontinuity; AI predictors into an
        optimizer; end product as hypothesis testing (``should I trust this decision?'').
        Constrains the \emph{class} of problem until Woody revises it.
  \item \textbf{L2 --- Written mathematical problem statement}
        \textbf{Controlling Overleaf text (2~Jul 2026): MISSING from this corpus.}
        Best available stand-in: H2
        (\texttt{history/Algorithmic\_Stability\_Wenbin\_Problem\_Setup.pdf}) ---
        co-authored hybrid draft (Nick / Wenbin / Woody materials) with inline
        \texttt{[Wenbin]:} commentary; CreationDate 26~Jul 2026; Parts~I/II stubs empty;
        \textbf{not proven identical} to the July~2 Overleaf
        (\textbf{SAME-LINEAGE-UNPROVEN}).
        H2's Wenbin UQ block controls live equations when recovered Overleaf is absent:
        $C(X;D,\theta)$ / $\hat\theta(D)$ via constrained opt; goals~(i)--(iii); Part~I/II
        program. UQ narrowing is Wenbin's, not co-approved by Woody in-corpus.
  \item \textbf{L3 --- Methodology authorization}
        Wenbin 2~Jul 2026 email only: brainstorm methods for \emph{that} Overleaf setup
        (not a blank check; does not resurrect H1 as controlling framework).
  \item \textbf{L4 --- Terminology / process}
        ``post-hoc inference'' (12~Jun; Nick-attested Wenbin suggestion). H2 note: setting
        may be modified if a more principal version appears.
  \item \textbf{L5 --- Historical / reference only}
        H1 catalog; June~25 student proposal; Meetings~1--2 plans; quantization; adaptive
        regret; sequential-CREAM / solver-error backups.
\end{enumerate}

\medskip
\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%
\textbf{Conflict rule.} L1 constrains \emph{class}; L2 fills \emph{instance}. If H2 ever
leaves ``policy $=$ opt solution,'' L1 (Woody) wins until Woody accepts the departure. If a
general selector framework is asserted against L2's UQ narrowing, L2 wins for
theorems-in-progress. Methods must target L2 (via L3). H2 is the best available annotated
draft --- not apex law and not proven $=$ July~2 Overleaf.
}}
```

---

### 1.4 H2 inventory row (Status cell)

**OLD:**
```latex
    \textcolor{current}{\textbf{Current with revisions}}
    (highest formulation authority) \\
```

**NEW:**
```latex
    \textcolor{current}{\textbf{Best available annotated draft}}
    (SAME-LINEAGE-UNPROVEN vs July~2 Overleaf;
    mid-edit / stubs) \\
```

---

### 1.5 H2 classification header (Type / Status / Purpose opener)

**OLD:**
```latex
\subsubsection*{H2 --- Wenbin problem setup (most authoritative)}
\Meta{Document}{Algorithmic Stability for Post-Hoc Selection}
\Meta{Date}{Approx.\ early July 2026 setup (aligned with Wenbin email 2 Jul 2026);
compiled/annotated copy in Downloads as \texttt{-8}}
\Meta{Type}{Advisor-authored / co-authored problem setup with inline Wenbin commentary}
\Status{Current with revisions --- controlling formulation}
```

**NEW:**
```latex
\subsubsection*{H2 --- Wenbin-annotated problem setup (best available stand-in)}
\Meta{Document}{Algorithmic Stability for Post-Hoc Selection}
\Meta{Date}{PDF CreationDate 26 Jul 2026 (Downloads \texttt{-8}); lineage relative to
Wenbin's 2~Jul Overleaf rewrite is \textbf{SAME-LINEAGE-UNPROVEN} --- not proven identical}
\Meta{Type}{Co-authored hybrid draft (Nick / Wenbin / Woody materials) with inline
\texttt{[Wenbin]:} commentary; not a pure advisor-authored finished formulation}
\Status{Best available annotated draft --- mid-edit (Abstract TBA; \S3.2--3.4 empty);
controls live UQ equations only as stand-in for missing July~2 Overleaf}
```

---

### 1.6 H2 “Relationship to later work”

**OLD:**
```latex
\paragraph{Relationship to later work.}
This is the formulation methodologies should target unless later advisor text supersedes it.
```

**NEW:**
```latex
\paragraph{Relationship to later work.}
Methodologies (per July~2 email) target Wenbin's Overleaf setup. While that text is missing,
treat H2's Wenbin UQ block and Part~I/II program as the working target --- provisional, and
subject to Woody's Meeting~3 agenda class.
```

---

### 1.7 H2 goals / recalibration sentence + flag notation in “Important ideas”

**OLD:**
```latex
\paragraph{Important ideas introduced.}
Validity assumption (1); optimization (2) defining $\hat\theta(D)$; goals (i)--(iii): when
plugging $\hat\theta(D)$ preserves validity, what is the miscoverage deviation, and what
recalibration restores validity.
```

**NEW:**
```latex
\paragraph{Important ideas introduced.}
Validity assumption (1); optimization (2) defining $\hat\theta(D)$; goals (i)--(iii) as
written. \textbf{Notation bug in H2:} introducer writes $C(X;D,\alpha)$ then uses
hyperparameter $\theta$ and $C(X;D,\theta)$ in~(1) --- record the inconsistency; do not
silently ``fix'' it in this overview. \textbf{Goal~(iii) mid-edit:} body asks what
procedure can \emph{recalibrate} $C$ to restore~(1); Wenbin Comment~E says
\emph{no recalibration}, data-randomize / structured noise answers~(iii). Treat as
unresolved mid-edit (see Council Verdicts), not a settled refinement.
```

---

### 1.8 Timeline July 2 row

**OLD:**
```latex
2 Jul 2026 & Wenbin: Overleaf problem setup ``aligns closer to what we intended''; Nick to
  brainstorm methodologies. & E1; companion = H2 \\
```

**NEW:**
```latex
2 Jul 2026 & Wenbin: Overleaf problem setup ``aligns closer to what we intended''; Nick to
  brainstorm methodologies. Exact Overleaf text \textbf{missing}. H2 (26~Jul Downloads
  \texttt{-8}) is later hybrid stand-in --- \textbf{SAME-LINEAGE-UNPROVEN}, not identity.
  & E1; H2 stand-in only \\
```

---

### 1.9 Idea A status

**OLD:**
```latex
\textbf{Status:} \textcolor{superseded}{Superseded / abandoned as primary plan}.\\
```

**NEW:**
```latex
\textbf{Status:} \textcolor{superseded}{Redirected / no longer primary}
(Woody redirected; remnant as model-error special case).\\
```

---

### 1.10 Idea B status + historical note

**OLD:**
```latex
\textbf{Status:} \textcolor{superseded}{No longer the plan} as of Meeting~3.\\
\textbf{Why:} Project pivoted to stability of optimization-induced policies and post-selection
stability literature.\\
\textbf{Historical note.} This idea was later abandoned as the active agenda; retain for
intellectual history and for any notation borrowed from CREAM during the Overleaf attempt
(Overleaf text itself is missing from this corpus --- see Missing evidence).
```

**NEW:**
```latex
\textbf{Status:} \textcolor{superseded}{No longer the active plan} as of Meeting~3
(explicit permanent abandonment not spoken in-corpus).\\
\textbf{Why:} Project pivoted to stability of optimization-induced policies and post-selection
stability literature.\\
\textbf{Historical note.} Retain for intellectual history and for any notation borrowed from
CREAM during the Meeting~2 Overleaf attempt (that Overleaf text is missing --- see Missing
evidence). Do not label bare ``Abandoned'' without the active-plan caveat.
```

---

### 1.11 Idea C status

**OLD:**
```latex
\textbf{Status:} Backup only; not adopted as Meeting~3 direction.\\
\textbf{Status label:} Abandoned as active plan / Unknown if permanently discarded.
```

**NEW:**
```latex
\textbf{Status:} Backup only; not active; not adopted as Meeting~3 direction.\\
\textbf{Status label:} Backup / revive status unknown (do not use bare ``Abandoned'').
```

---

### 1.12 Idea E current form (recalibrate clause)

**OLD:**
```latex
\textbf{Current form:} H2 --- validity of $C(X;D,\hat\theta(D))$ when $\hat\theta$ solves
constrained opt on shared data; recalibration if needed.\\
```

**NEW:**
```latex
\textbf{Current form:} H2 (stand-in) --- validity of $C(X;D,\hat\theta(D))$ when $\hat\theta$
solves constrained opt on shared data; goals~(i)--(ii) live; (iii)~as written $=$ recalibrate
$C$, Comment~E override $=$ no recalibration / data-randomize (unresolved mid-edit).\\
```

---

### 1.13 Evolution overlapping — “Earlier version (H1)” and “Why / Current”

**OLD:**
```latex
\textbf{Earlier version (H1 / June~25):}
general composable stability-certification for post-hoc selectors;
template $\tilde S=\tilde A(D;\xi)$; certificates DP / $(\eta,\tau,\nu)$-stability /
selective CIs.
```

**NEW:**
```latex
\textbf{Earlier framing (June~25 email + Meeting~3 survey materials; July~26 H1 PDF is a
later writeup of that line, not ``earlier than'' H2's compile date):}
general composable stability-certification for post-hoc selectors;
template $\tilde S=\tilde A(D;\xi)$; certificates DP / $(\eta,\tau,\nu)$-stability /
selective CIs.
```

**OLD:**
```latex
\textbf{Why it changed:}
Wenbin (H2): ``The post-hoc inference problem is itself very general. We need to narrow\ldots''
Woody (Meeting~3): policy is solution to an optimization problem; define stability for that
class first.
```

**NEW:**
```latex
\textbf{Why it changed:}
Woody (Meeting~3): policy is solution to an optimization problem; define stability for that
class first (agenda). Wenbin (H2 comments): ``The post-hoc inference problem is itself very
general. We need to narrow\ldots'' --- UQ example is Wenbin's specialization, not ``advisors''
plural endorsing UQ in a primary.
```

**OLD:**
```latex
\textbf{Current understanding (H2 + Meeting~3):}
study when optimization-selected $\hat\theta(D)$ preserves uncertainty-set validity; if not,
quantify deviation and recalibrate; possibly via structured / data randomization informed by
inverse optimization and algorithmic-stability post-selection tools.
```

**NEW:**
```latex
\textbf{Current understanding (Meeting~3 agenda + H2 stand-in math):}
study when optimization-selected $\hat\theta(D)$ preserves uncertainty-set validity; if not,
quantify deviation~(ii); for restoring~(1), prefer Comment~E's no-recalibration /
data-randomize / structured-noise path over treating ``recalibrate $C$'' as settled method
language (unresolved mid-edit).
```

---

### 1.14 Math framework — H2 controlling block + notation

**OLD:**
```latex
\subsection{Wenbin / current setup (H2) --- controlling}
Uncertainty set $C(X;D,\theta)$ with validity for fixed $\theta$:
```

**NEW:**
```latex
\subsection{Wenbin / current setup (H2) --- best available stand-in}
\textbf{Source caveat.} H2 is not proven $=$ July~2 Overleaf (SAME-LINEAGE-UNPROVEN).
\textbf{Notation bug.} H2 introduces $C(X;D,\alpha)$ with hyperparameter $\theta$, then
writes~(1) with $C(X;D,\theta)$ --- flagged, not silently normalized away.
Uncertainty set $C(X;D,\theta)$ (as used in~(1)) with validity for fixed $\theta$:
```

**OLD:**
```latex
Goals: (i)~when does (1) still hold for $\hat\theta(D)$; (ii)~miscoverage deviation if not;
(iii)~recalibration procedure.
```

**NEW:**
```latex
Goals: (i)~when does (1) still hold for $\hat\theta(D)$; (ii)~miscoverage deviation if not;
(iii)~as written, recalibration of $C$ --- \emph{but} Wenbin Comment~E: no recalibration;
data-randomize answers~(iii). Unresolved mid-edit.
```

---

### 1.15 Advisor feedback — Comment E line

**OLD:**
```latex
          \item Strategy notes: data-driven policy (e.g.\ PTO); no recalibration vs data-randomize
                for validity; structured noise / inverse optimization; post-inference line
                (Tijana; winner's curse; algorithmic stability).
```

**NEW:**
```latex
          \item Strategy notes (Comment~E): data-driven policy (e.g.\ PTO); \emph{no
                recalibration}; data-randomize to achieve validity (``this answers~(iii)'');
                structured noise / inverse optimization; post-inference line (Tijana; winner's
                curse; algorithmic stability). Conflicts with goal~(iii) body wording ---
                unresolved mid-edit.
```

---

### 1.16 Open problems table — Abandoned rows

**OLD:**
```latex
Adaptive regret frontier formulation & Abandoned as active plan \\
\addlinespace
Quantization risk-profile primary project & Abandoned \\
\addlinespace
Sequential CREAM; solver-error accommodation & Abandoned as active /
Unknown if revive \\
```

**NEW:**
```latex
Adaptive regret frontier formulation & No longer the active plan (as of M3);
explicit permanent abandonment not spoken \\
\addlinespace
Quantization risk-profile primary project & Redirected / no longer primary
(Woody); remnant as model-error case \\
\addlinespace
Sequential CREAM; solver-error accommodation & Backup only; not active;
revive status unknown \\
```

Optional companion open-problem row (insert after H2 (iii) / stabilization row if desired):

```latex
Goal~(iii) wording (recalibrate $C$) vs Comment~E (no recalibration /
data-randomize) & Unresolved mid-edit \\
\addlinespace
```

---

### 1.17 Current state item 1

**OLD:**
```latex
  \item \textbf{Problem (controlling text):} H2 --- post-hoc UQ with optimization-selected
        hyperparameter; two-part program (constrained-opt stability, then post-hoc inference).
```

**NEW:**
```latex
  \item \textbf{Problem (written math, stand-in):} H2 --- post-hoc UQ with
        optimization-selected hyperparameter; two-part program; mid-edit hybrid, not proven
        $=$ July~2 Overleaf. Agenda class still Meeting~3 (Woody).
```

---

### 1.18 Missing companion evidence — first bullet

**OLD:**
```latex
  \item Exact July~2 Overleaf problem setup text (H2 is the best available stand-in).
```

**NEW:**
```latex
  \item Exact July~2 Overleaf problem setup text (H2 is the best available stand-in;
        lineage \textbf{SAME-LINEAGE-UNPROVEN} --- do not treat as identical).
```

---

### 1.19 Meeting 2 “H2 replaces” weasel

**OLD:**
```latex
  \item \textbf{Later documents:} E1 (June emails); T1 Meeting~3 plan-status table; H2 replaces
        this formulation path.
```

**NEW:**
```latex
  \item \textbf{Later documents:} E1 (June emails); T1 Meeting~3 plan-status table. The
        \emph{Meeting~3 pivot} (not H2 text) supersedes the Meeting~2 regret/CREAM path; H2
        never mentions CREAM/regret.
```

---

### 1.20 Final audit — adjust overclaim

**OLD:**
```latex
  \item[\checkmark] Current formulation identified (H2 + Meeting~3).
```

**NEW:**
```latex
  \item[\checkmark] Layered current state identified (Meeting~3 agenda; H2 stand-in math;
        July~2 methods auth; Overleaf text missing).
```

---

### 1.21 INSERT — new section before `\section{How to use these folders}`

Insert after Missing companion evidence (before How to use):

```latex
\section{Council Verdicts}
% Convert from swarm consensus; keep short. See markdown source in patch spec §2 if regenerating.
```

Paste LaTeXized version of §2 below (or keep §2 as the conversion source).

---

## 2. New “Council Verdicts” section (markdown-ready → convert to LaTeX)

### Council Verdicts

**V1 — H2 vs July 2 Overleaf = SAME-LINEAGE-UNPROVEN.**  
A July 2 Overleaf rewrite existed and was preferred (Wenbin email). That text is missing. H2 (Downloads `-8`, CreationDate 26 Jul 2026) is a later mid-edit hybrid with empty Parts I/II and Abstract TBA. Same *story* (Wenbin rewrite after June 29); same *document* — unproven. Stop writing `companion = H2` or treating H2 as the July 2 Overleaf.

**V2 — Authority is layered, not a flat crown.**  
Woody / Meeting 3 owns research agenda and end product (optimization-induced policy stability; AI→optimizer; trust as hypothesis test). Wenbin owns the live written math instance when Overleaf is absent (H2’s `[Wenbin]:` UQ block and Part I/II program). July 2 email owns methodology authorization for that setup only. H2 is best available annotated draft, not apex law. UQ narrowing is Wenbin’s specialization, not plural “advisors” co-approval of UQ in a primary.

**V3 — Goal (iii) vs Comment E = unresolved mid-edit.**  
Body (iii) asks what procedure can *recalibrate* the uncertainty set. Comment E: *no recalibration*; data-randomize / data-driven policy answers (iii). Not a clean refinement (goal text still says recalibrate) and not a pure contradiction (Wenbin maps E → answers (iii)). Methods intent from Wenbin comments: stabilize/randomize selection, not recalibrate \(C\). Do not collapse into one settled sentence.

**V4 — H2 authorship.**  
H2 is a co-authored hybrid draft (Nick general-framework prose, Meeting 3 notes residue, Wenbin UQ setup + cyan comments), not a pure advisor-authored finished formulation. Nick pp.1–2 “general framework” language is non-authoritative relative to Wenbin’s “narrow” comments.

**V5 — Idea statuses.**  
Match transcript vocabulary: Idea A = redirected / no longer primary; Idea B = no longer the active plan (permanent abandonment not spoken); Idea C = backup only; not active; revive unknown. Drop bare “Abandoned” without caveat.

**V6 — `papers/` packaging.**  
Priority/pivot papers are in-scope for the evolution narrative. Saying they are “not formulation history” because PDFs live under `papers/` rather than `history/` is wrong. Correct boundary: not duplicated into `history/`.

**V7 — Notation bug.**  
H2 introduces \(C(X;D,\alpha)\) with hyperparameter \(\theta\), then uses \(C(X;D,\theta)\) in (1). Flag it; do not silently normalize in the overview.

---

## 3. What NOT to change (preserve)

| Claim / passage | Why keep |
|---|---|
| H1 = Downloads `-5/-6/-7` byte-identical; MD5 triplicate note | Proven |
| H2 = Downloads `-8` (MD5 match) | Proven |
| Meeting 3 = spoken current plan: opt-induced policies; AI+optimizer; trust as HT; PPI + post-selection stability reading | T1 |
| June 12 “post-hoc inference” added (Nick-attested Wenbin suggestion) | E1 — keep attestation framing if touched elsewhere |
| July 2: Overleaf “aligns closer…”; Nick to brainstorm methodologies | E1 |
| Wenbin `[Wenbin]:` five comments (intersection; narrow to one objective; Part I/II decompose; may modify; Comment E strategy) | H2 verbatim |
| H2 goals (i)–(ii) and eqs. (1)–(2) conceptually | Yes, modulo α/θ bug flag |
| §§3.2–3.4 stubs / incomplete | Keep |
| Missing evidence list (Overleaf, July 2 attachments, June 11 notes, CREME/CREAM email if any) | Keep; only strengthen Overleaf≠H2 wording |
| H1 as historical catalog / not controlling vs Wenbin narrowing | Keep subordination |
| §Current state split: Motivation = M3; Immediate work = E1 Jul 2–3; terminology constraint | Already layered correctly — preserve structure |
| Zrnic–Jordan literature claims in theorems table; H1 best-first still open | Keep |
| Out-of-scope Lean/`Work`/early Downloads `-1`–`-4` boundary + historical note on corpus boundary | Keep |
| Idea D as historical methodology / catalog still reference | Keep |
| “Presented in spirit at Meeting 3” for H1 — **optional soft fix later**; not required by this consensus batch unless you want weasel removal |
| Student unifying template math block (H1) | Keep as historical |
| How-to-use ordering (overview → H2 → T1 M3 → E1 → H1 → papers) | Keep; after authority rewrite it remains coherent |

---

**Apply order:** 1.3 (authority) → 1.5–1.7 (H2 headers) → 1.8 (timeline) → 1.1–1.2 (`papers/`) → idea/open-problem status patches → math/(iii) patches → insert Council Verdicts → final-audit / current-state / missing-evidence one-liners.