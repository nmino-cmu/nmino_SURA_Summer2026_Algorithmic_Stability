# Assumption ledger

| id | assumption | warrant | used in | risk if false | status |
|----|------------|---------|---------|---------------|--------|
| A1 | Fixed-θ validity (1) for prespecified θ | Wenbin UQ body | Part II baseline | post-hoc analysis vacuous | LOCKED (problem hyp) |
| A2 | θ̂ from constrained opt (2); σ(f̂),σ(ĝ)⊆σ(D) | Wenbin UQ + footnote | Part I/II | wrong selection map | LOCKED |
| A3 | Live object = θ̂ only (not z, not general Ŝ) | W2 narrowing | all formal | scope creep | LOCKED |
| A4 | (iii) via data-randomize selection; no C recalibration | W5 | Part II (iii) | wrong repair class | LOCKED |
| A5 | Local reading of y in f̂(y;θ) | quarantine note | (2) | wrong dependence structure | OPEN |
| A6 | LOO neighbor model (replace vs delete) | W3 “one data point” | Part I | wrong stability metric | OPEN — pick per lemma |
| A7 | (η,τ,ν)-stability (Zrnic–Jordan Def.2) of θ̂ map | digest_zrnic Thm2 | Part II | wrong stability notion for (iii) | ADOPT as Part II certificate |
| A8 | e^η classical-level inflation | ZJ Thm2 | goals (i)(ii) only | mistaken as (iii) | LOCKED: NOT goal (iii) |
| A9 | Drive η→0 via randomized selection; keep C fixed-θ map | W5 + ZJ design | goal (iii) | under-randomize | LOCKED (iii) path |
| A10 | Winner’s Curse “zoom” = reshape CI | digest_winners | contrast only | scope creep into recalibration | FORBIDDEN as (iii) |

Add rows only with warrant. Unwarranted CREDO/CREME regularity assumptions = FORBIDDEN in formal/.

| A11 | diam(Θ0)≤D, Lip L, conc ε,ν, uniq | part_i_randomized_design | RNM/soft rates | OPEN for concrete f̂ | ADOPT as design hyps |
| A13 | Nested instance: ε=√(log(2/ν)/(2n)) DKW; ĝ box | instance_nested_uq | Ass conc for design | hard argmin degenerate | ADOPT + caveat |
| A14 | Hard argmin of (2_nest)=1 a.s.; live (iii)=randomized on f̂ | instance remark | honesty | vacuous if ignore | LOCKED caveat |
| A13 | Nested score-threshold: ε(n,ν)=√(log(2/ν)/(2n)), ν(n)=ν (DKW); box ĝ | instance_nested_uq Lem.dkw | Ass.conc for design | scores must be iid on calib fold | LOCKED for this instance |
| A15 | Tradeoff (2_trade): f̂=θ, ĝ=misĉ-α0; θ̂=emp. quantile; DKW on ĝ | instance_tradeoff_uq | Ass.conc nontrivial ĝ | Ass.conc Θ0={g*≤0} needs Hausdorff/conservative | ADOPT + Hausdorff caveat |
