# Wave 1 — Wenbin H2 problem setup (complete)

Agent: [Wenbin H2](506c309d-2ff4-4265-b217-9405867fcd87)

## Five [Wenbin]: comments (authoritative)

1. Intersection: post-hoc inference + algorithmic stability + optimization theory.
2. Narrow: one specific objective (UQ example Wenbin wrote).
3. Decompose: (I) stability of constrained opts (one-point change; assumptions on f̂,ĝ); (II) post-hoc inference on top.
4. May modify setting if more principal version appears.
5. Strategy: data-driven policy (e.g. PTO); **no recalibration**; data-randomize answers (iii); structured noise via inverse optimization; Tijana / winner’s curse / algorithm stability.

## Formal goals

- (1) Validity for fixed θ: P(Y∈C(X;D,θ))≥1−α
- (2) θ̂(D)=argmin f̂ s.t. ĝ≤0
- Goals (i) when (1) survives θ̂(D); (ii) miscoverage deviation; (iii) restore validity

## Absolute truths from this PDF

- Live problem ≠ universal stabilize-any-selector framework.
- Part I/II bodies EMPTY; abstract TBA; mid-edit (Nick general framework prose still on pp.1–2).
- Notation bug: C(X;D,α) vs C(X;D,θ).
- Tension: (iii) says “recalibrate” but Comment E prefers no recalibration / data-randomize.
- PDF CreationDate 2026-07-26 21:11 UTC; H1 same day ~5.5h earlier — H2 is later file, NOT proven = July 2 Overleaf.

## Next Nick actions (from Wenbin words)

Fill Part I then Part II; pursue i–iii; structured noise / inverse opt direction; stay flexible.
