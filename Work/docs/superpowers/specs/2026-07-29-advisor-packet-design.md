# Advisor-Facing Research Packet — Design

**Date:** 2026-07-29  
**Status:** APPROVED  
**Audience:** Professor Zhu, Wenbin Zhou  
**Author of packet materials:** Nicholas Mino (SURA)

**Companion document:** After approval, implementation details live in a separate implementation plan (`Advisor_Packet_Implementation` / dated plan under `Work/docs/superpowers/plans/`). This design stays stable; the implementation plan may evolve without changing approved scope.

## Problem

Two advisor-facing documents already exist or are being produced separately:

1. `Formulation/writeup/Problem_Writeup.pdf` — mathematical problem formulation (intellectual front door).
2. Intellectual timeline (redesigned under `Submission_Only/`; also older copy under `Timeline/`).

The remaining gap is a concise faculty packet that lets advisors understand current research state, review mathematical direction, and prepare for a productive meeting — without forcing them through repository internals.

## Philosophy

When in doubt, prefer omission over speculation.  
The packet should be concise, evidence-backed, and easy for a faculty reader to navigate.

Prioritize, in order:

1. current mathematical problem;
2. intellectual progress;
3. concrete evidence of work;
4. immediate theorem target;
5. specific questions requiring advisor feedback.

Repository, Lean proofs, operator packages, and architecture are **supporting evidence**, not the primary research result.

### Success criterion

A faculty reader should be able to understand the current mathematical problem, evaluate the direction of the research, and prepare for a meeting by reading the packet in approximately 15–20 minutes.

## Document hierarchy

| Level | Document | Purpose |
|-------|----------|---------|
| Primary | `Problem_Writeup` (existing) | Mathematical contribution |
| Primary | `Research_Update_Summary` | Executive overview |
| Secondary | `Intellectual_Timeline` (packet copy) | Research history |
| Secondary | `Questions_for_Advisors` | Meeting preparation |
| Supporting | `Repository_Guide` | Navigation |
| Supporting | `Stabilized_Algorithm_Catalog_Overview` | Evidence of catalog work |

Emphasis stays on the mathematics. Supporting documents must not compete with primary documents for attention or length.

## Locked decisions

| Topic | Choice |
|-------|--------|
| Root directory | `Advisor_Packet/` (repo root, parallel to `Formulation/`, `Work/`, `Submission_Only/`) |
| Combined PDF | **Do not create** |
| Problem write-up | Authoritative; do not overwrite, rewrite, relocate, rename, or regenerate |
| Timeline sources | Authoritative where they live today; do not overwrite/rewrite/relocate originals |
| Timeline in packet | Canonical **copies** under `Advisor_Packet/Intellectual_Timeline/` |
| Shared style | `Advisor_Packet/Assets/packet_style.tex` (required in practice) |
| Effort in summary | At most “approximately 92 hours reconstructed”; full breakdown only in timeline |
| Speculative claims | Qualify or omit |

## Repository scope

`Advisor_Packet/` contains only concise, advisor-facing documents.

Do **not** duplicate implementation artifacts, Lean libraries, operator papers, generated certificates, or research infrastructure. Reference their existing locations where appropriate.

Changes for this deliverable are restricted to `Advisor_Packet/` and any explicitly approved packet assets (plus design/implementation docs under `Work/docs/superpowers/` if needed). Unrelated working-tree modifications must not be touched.

## Target layout

```
Advisor_Packet/
├── README.md
├── PACKET_AUDIT.md
├── Assets/
│   ├── packet_style.tex
│   └── figures/          # only if needed
├── Intellectual_Timeline/
│   ├── Intellectual_Timeline.tex
│   └── Intellectual_Timeline.pdf
├── Research_Update_Summary/
│   ├── Research_Update_Summary.tex
│   └── Research_Update_Summary.pdf
├── Questions_for_Advisors/
│   ├── Questions_for_Advisors.tex
│   └── Questions_for_Advisors.pdf
├── Repository_Guide/
│   ├── Repository_Guide.tex
│   └── Repository_Guide.pdf
└── Stabilized_Algorithm_Catalog_Overview/
    ├── Stabilized_Algorithm_Catalog_Overview.tex
    └── Stabilized_Algorithm_Catalog_Overview.pdf
```

## Authoritative documents (preserve)

These are authoritative source documents.  
**Do not overwrite, rewrite, relocate, rename, or regenerate them. Reference them only.**

| Document | Canonical location |
|----------|-------------------|
| Problem formulation | `Formulation/writeup/Problem_Writeup.{tex,pdf}` |
| Redesigned timeline (current working location) | `Submission_Only/Timeline/intellectual_timeline.{tex,pdf}` |

Packet timeline folder holds **copies** renamed to `Intellectual_Timeline.{tex,pdf}` for consistent packet naming. Original locations remain intact so existing references do not break.

## Visual consistency and maintainability

Match the redesigned intellectual timeline and problem write-up as closely as practical:

- restrained academic palette: navy, blue-gray, light gray, one muted accent;
- clean section titles; readable tables; consistent headers/footers;
- subtle tcolorbox callouts where useful;
- body text 10.5pt or 11pt unless consistency requires otherwise;
- no bright decorative colors, marketing graphics, excessive icons, tiny fonts, or dashboard layouts.

**Future maintenance.** The packet structure should be maintainable. Shared formatting belongs in `Assets/packet_style.tex`; avoid duplicating style definitions across documents.

## Notation and terminology

Use consistent mathematical notation, terminology, capitalization, and naming conventions across all packet documents. When in doubt, follow the Problem_Writeup.

For the research-question statement in particular: preserve terminology and notation from the existing Problem_Writeup wherever possible. Do not introduce alternate notation or reformulate definitions unless necessary for brevity.

## Document purposes (no substantial cross-duplication)

Each document has a distinct job and should cross-reference the others rather than re-summarizing the whole project.

### 1. Research_Update_Summary (≤2 pages; aim 1) — Primary

First document advisors should read. Faculty-facing; readable in under three minutes.

Required content:

- **Current research question** — accurate Formulation II wording aligned with the Problem_Writeup: when an uncertainty set remains valid after its hyperparameter is selected by constrained optimization on the same calibration data; how coverage/risk can deteriorate; whether guarantees can be recovered by stabilizing selection while retaining the fixed-hyperparameter construction of \(\mathcal{C}\). Be precise: construction rule for fixed \(\theta\) unchanged; selected \(\theta\) may change; do not imply the final set is literally unchanged after changing selected \(\theta\). Preserve writeup terminology/notation.
- **Intellectual progression** (compact): adaptive certified regret → stabilized-algorithm catalog → broad optimization-based selection stability framework → current optimization-selected UQ formulation. Do not reproduce the full timeline.
- **Main accomplishments** in order of intellectual development. Reference the intellectual timeline for detailed effort reconstruction. At most mention approximately 92 hours of reconstructed work (June 1–July 29 per timeline). **Do not** include the workstream hour breakdown (20/20/10/…).
- **Current theorem agenda** — Part I: replace-one stability under explicit assumptions; Part II: translate to finite-sample validity/coverage/risk after adaptive selection.
- **Immediate next step** — complete Part I under explicit assumptions, obtain advisor feedback, only then broaden.
- **What I Would Like to Discuss** — short pointer to `Questions_for_Advisors.pdf`; do not duplicate every question.

### 2. Questions_for_Advisors (1 page) — Secondary

Organize by priority; make each question answerable; highlight top three visually.

- **A. Mathematical formulation** — closeness of UQ formulation; Part I/II decomposition; replace-one stability; assumptions; one motivating instance vs general first theorem.
- **B. Novelty and literature** — distinctness vs CRC / decision-focused UQ / post-selection inference; closest baselines; Part II aim (coverage vs risk vs transfer theorem).
- **C. Research sequencing** — pause operator expansion until Part I; useful special case; meaningful progress before next meeting.
- **D. Continued collaboration** — cadence; post-SURA continuation; milestones for paper / longer collaboration.

Exclude private medical information and email-apology / communication explanations.

### 3. Repository_Guide (1 page) — Supporting

Heading: How to Review This Project.

- Recommended reading order (5 minutes; 15–20 minutes).
- Supporting evidence paths with one-sentence relevance each.
- Neutral note that the repo contains substantial implementation/verification infrastructure; the reading order foregrounds the mathematical question.

**Path rule:** Every repository path must be verified against the current repository tree. If a referenced artifact does not exist, omit it rather than inventing or guessing a location.

Expected candidates to verify (omit if missing):

- stabilized-algorithm catalog / literature sources as they actually exist;
- `Work/research-results/primitive-library/FINAL-VERDICT.md`;
- operator / human-readable papers under `Work/research-results/`;
- architecture docs under `Work/architecture-discovery/` (reference only if useful);
- `Formulation/writeup/Problem_Writeup.pdf`.

Do not list every implementation folder.

### 4. Stabilized_Algorithm_Catalog_Overview (≈2–4 pages) — Supporting

The overview should summarize the intellectual contribution of the catalog, not reproduce the catalog itself.

- **Purpose** — identify recurring structures in how data-dependent algorithms/selection procedures are stabilized.
- **What was extracted** — fields such as source/citation; algorithm/selection rule; selected object; stability notion; assumptions; stabilization mechanism; noise/perturbation/randomization/regularization; primitive decomposition; proof strategy; composition rule; utility cost; downstream inference/generalization guarantee; limitations; relevance to current project.
- **Representative entries** — select entries that collectively illustrate **distinct stabilization mechanisms**, not merely the “best” papers. Target mechanisms such as:
  - randomized selection / noisy max;
  - algorithmic stability;
  - regularization;
  - conformal risk control;
  - differential privacy or max-information;
  - optimization robustness.
  Do not fabricate entries. Each entry: paper/method; selected object; mechanism; guarantee; relevance.
- **Recurring patterns** — distinguish literature-supported observations from hypotheses motivating the broader framework.
- **Relation to current formulation** — catalog motivated the broader primitive framework; immediate target is the narrower Part I theorem. Do not claim the catalog proves a universal framework.
- **Link to full data** — actual verified path(s); if the full structured database is not in-repo, state that explicitly and point to the best available sources (e.g. overview/H1 notes, digests, paper index).

### 5. Intellectual_Timeline (packet copy) — Secondary

Canonical packet copies of the redesigned timeline. Content ownership remains with the existing timeline workstream; this packet job does not redesign or rewrite the timeline beyond copy + consistent naming for the packet folder.

### 6. README.md (landing page)

Must be readable on GitHub without opening any PDFs.

Include:

- purpose of the packet;
- document hierarchy (or equivalent navigation cues);
- recommended reading order;
- links to all packet files;
- links to existing Problem_Writeup and intellectual timeline (packet copy + note of authoritative originals);
- repository locations of supporting evidence (verified);
- date of packet generation.

Recommended reading order:

1. `Research_Update_Summary.pdf`
2. existing `Problem_Writeup.pdf`
3. `Questions_for_Advisors.pdf`
4. `Intellectual_Timeline.pdf` (packet copy)
5. `Stabilized_Algorithm_Catalog_Overview.pdf`
6. `Repository_Guide.pdf` (navigation aid; not required in the mathematical narrative)

### 7. PACKET_AUDIT.md

Report:

- every file created;
- whether each PDF compiled successfully;
- page count for each PDF;
- whether material overfull boxes remain;
- whether all repository paths were verified;
- whether the problem write-up was left unchanged;
- whether original intellectual timeline locations were left unchanged;
- whether the packet contains unsupported factual claims;
- that no combined PDF was created (by design);
- packet reading order;
- recommended email attachments.

Recommended email attachments (limited):

1. `Research_Update_Summary.pdf`
2. `Problem_Writeup.pdf`
3. `Intellectual_Timeline.pdf` (packet copy or equivalent)
4. `Questions_for_Advisors.pdf`
5. optionally `Stabilized_Algorithm_Catalog_Overview.pdf`

Repository link in the email body. Do not recommend attaching the repository guide unless navigation is likely difficult.

## Evidence and claims

### Evidence inventory (design requirement)

Before drafting, an evidence inventory must record every repository artifact that will be cited or referenced. If an expected artifact is missing, record its absence rather than substituting another source.

Primary sources to inventory:

- `Formulation/writeup/Problem_Writeup.{tex,pdf}`
- redesigned timeline under `Submission_Only/Timeline/`
- root / Formulation / Work READMEs
- `Work/research-results/primitive-library/FINAL-VERDICT.md`
- catalog / H1 / overview / literature digests / paper index
- advisor-facing notes, meeting notes, emails, transcripts already in the repo (e.g. `Formulation/context/`)

Use repository evidence rather than inventing accomplishments, dates, claims, or research conclusions. File creation/modification dates and timeline effort reconstructions may inform careful wording; they do not authorize new theorems.

### Hard claims rules

Every substantive factual statement should be traceable to either the repository, the existing timeline, the problem write-up, or the cited literature. Where evidence is incomplete, explicitly qualify the statement.

Do **not** claim:

- that the main theorem has been proved;
- that the general framework has been validated;
- that all operator results apply to the current UQ theorem;
- that the advisor approved the June 25 framework;
- that infrastructure work is itself the final research contribution.

Prefer careful wording such as: “approximately”; “current formulation”; “student-developed”; “supporting infrastructure”; “subject to advisor feedback.”

Do not substantially duplicate material across packet documents.

## Quality bar (design acceptance)

The packet meets this design when:

- Every PDF has a distinct purpose aligned with the document hierarchy.
- Cross-references are accurate.
- Repository paths were verified (missing ones omitted).
- No duplicated major sections across packet docs.
- No unsupported factual claims.
- Existing authoritative documents remain unchanged.
- Notation and terminology follow the Problem_Writeup.
- A faculty reader can complete the ~15–20 minute success criterion.
- Packet can be attached immediately to an advisor email.
- Audit complete; recommended attachment list recorded.

## Out of scope

- Another full problem formulation.
- Another intellectual timeline redesign.
- Combined packet PDF.
- Copying entire sections from write-up/timeline into new files.
- Email apology / communication explanation inside the packet.
- Expanding operator library or proving Part I as part of this packet task.
- Detailed build/compile step lists (belong in the implementation plan).

## After approval

After approval, implementation should follow this design without changing the approved scope unless new requirements are explicitly added. Build steps, compilation commands, visual QA checklists, and task sequencing belong in the separate implementation plan.
