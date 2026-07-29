import Research.Operators.OrderStat.BasicInt
import Research.Operators.Argmax.BasicInt

namespace Research.Operators.OrderStat.KthMarginInt

open Research.Operators.OrderStat.BasicInt
open Research.Operators.Argmax.BasicInt

/-- Unique index `i` is the strict `k`-th smallest (0-based). -/
def IsStrictKthSmallest {n : Nat} (s : Fin n → Int) (k : Nat) (i : Fin n) : Prop :=
  k < n ∧ countLT s (s i) = k ∧ (∀ j : Fin n, s j = s i → j = i)

/-- Every pair of distinct scores is separated by more than `g`. -/
def AllGapsExceed {n : Nat} (s : Fin n → Int) (g : Nat) : Prop :=
  ∀ i j : Fin n, i ≠ j → Int.natAbs (s i - s j) > g

/- STATEMENT_BEGIN -/
def KthMarginInvarianceProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → Int) (k : Nat) (ε : Nat) (i : Fin n),
    IsStrictKthSmallest s k i →
    AllGapsExceed s (2 * ε) →
    ∀ δ : Fin n → Int, LinfBall δ ε →
      IsStrictKthSmallest (fun j => s j + δ j) k i

def KthMarginSharpnessProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → Int) (k : Nat) (ε : Nat) (i : Fin n),
    IsStrictKthSmallest s k i →
    (∃ j : Fin n, j ≠ i ∧ Int.natAbs (s i - s j) ≤ 2 * ε) →
    ∃ δ : Fin n → Int, LinfBall δ ε ∧
      ¬ IsStrictKthSmallest (fun t => s t + δ t) k i
/- STATEMENT_END -/

private theorem natAbs_coe (ε : Nat) : Int.natAbs (ε : Int) = ε := rfl
private theorem natAbs_neg_coe (ε : Nat) : Int.natAbs (-(ε : Int)) = ε := by
  rw [Int.natAbs_neg, natAbs_coe]

theorem strict_lt_preserved (a b δa δb : Int) (ε : Nat)
    (hlt : a < b) (hgap : Int.natAbs (b - a) > 2 * ε)
    (ha : Int.natAbs δa ≤ ε) (hb : Int.natAbs δb ≤ ε) :
    a + δa < b + δb := by
  have hpos : b - a > 2 * (ε : Int) := by
    have : 0 ≤ b - a := by omega
    have : Int.natAbs (b - a) = b - a := Int.natAbs_of_nonneg this
    omega
  have ha' := (natAbs_le_iff δa ε).mp ha
  have hb' := (natAbs_le_iff δb ε).mp hb
  omega

theorem pairwise_lt_iff {n : Nat} (s δ : Fin n → Int) (ε : Nat) (p q : Fin n)
    (hball : LinfBall δ ε) (_hne : p ≠ q)
    (hgap : Int.natAbs (s p - s q) > 2 * ε) :
    s p < s q ↔ s p + δ p < s q + δ q := by
  have hp := hball p
  have hq := hball q
  constructor
  · intro hlt
    exact strict_lt_preserved (s p) (s q) (δ p) (δ q) ε hlt
      (by rw [natAbs_sub_comm]; exact hgap) hp hq
  · intro hlt'
    have hne_val : s p ≠ s q := by
      intro heq
      have : Int.natAbs (s p - s q) = 0 := by simp [heq]
      omega
    cases Int.lt_or_gt_of_ne hne_val with
    | inl hlt => exact hlt
    | inr hgt =>
      have : s p + δ p > s q + δ q :=
        strict_lt_preserved (s q) (s p) (δ q) (δ p) ε (by omega) hgap hq hp
      omega

theorem countLT_of_iff :
    ∀ {n : Nat} (s s' : Fin n → Int) (v v' : Int),
      (∀ j : Fin n, s j < v ↔ s' j < v') → countLT s v = countLT s' v' := by
  intro n
  induction n with
  | zero =>
    intro s s' v v' h
    rfl
  | succ n ih =>
    intro s s' v v' h
    change
      countLT (fun j : Fin n => s j.castSucc) v +
          (if s (Fin.last n) < v then 1 else 0) =
      countLT (fun j : Fin n => s' j.castSucc) v' +
          (if s' (Fin.last n) < v' then 1 else 0)
    have hpref : ∀ j : Fin n, s j.castSucc < v ↔ s' j.castSucc < v' :=
      fun j => h j.castSucc
    have hih := ih (fun j => s j.castSucc) (fun j => s' j.castSucc) v v' hpref
    rw [hih]
    by_cases hsl : s (Fin.last n) < v
    · have hsl' : s' (Fin.last n) < v' := (h (Fin.last n)).mp hsl
      simp [hsl, hsl']
    · have hsl' : ¬ s' (Fin.last n) < v' := fun h' => hsl ((h (Fin.last n)).mpr h')
      simp [hsl, hsl']

theorem all_gaps_imply_below_iff {n : Nat} (s δ : Fin n → Int) (ε : Nat) (i : Fin n)
    (hball : LinfBall δ ε) (hgaps : AllGapsExceed s (2 * ε)) :
    ∀ j : Fin n, s j < s i ↔ s j + δ j < s i + δ i := by
  intro j
  by_cases h : j = i
  · subst h; constructor <;> intro hlt <;> omega
  · exact pairwise_lt_iff s δ ε j i hball h (hgaps j i h)

theorem uniqueness_preserved {n : Nat} (s δ : Fin n → Int) (ε : Nat) (i : Fin n)
    (hball : LinfBall δ ε) (hgaps : AllGapsExceed s (2 * ε)) :
    ∀ j : Fin n, s j + δ j = s i + δ i → j = i := by
  intro j hj
  by_cases h : j = i
  · exact h
  · have hgapji := hgaps j i h
    have hp := hball i
    have hq := hball j
    have hne_val : s j ≠ s i := by
      intro heq
      have : Int.natAbs (s j - s i) = 0 := by simp [heq]
      omega
    have : s j + δ j ≠ s i + δ i := by
      cases Int.lt_or_gt_of_ne hne_val with
      | inl hlt =>
        have := strict_lt_preserved (s j) (s i) (δ j) (δ i) ε hlt
          (by rw [natAbs_sub_comm]; exact hgapji) hq hp
        omega
      | inr hgt =>
        have := strict_lt_preserved (s i) (s j) (δ i) (δ j) ε (by omega) hgapji hp hq
        omega
    exact (this hj).elim

theorem kth_margin_invariance : KthMarginInvarianceProp := by
  intro n _hn s k ε i ⟨hk, hcount, _⟩ hgaps δ hball
  refine And.intro hk (And.intro ?count ?uniq)
  · have hiff := all_gaps_imply_below_iff s δ ε i hball hgaps
    have hcongr := countLT_of_iff s (fun j => s j + δ j) (s i) (s i + δ i) hiff
    exact hcongr.symm.trans hcount
  · exact uniqueness_preserved s δ ε i hball hgaps

/-- Component of the tie adversary at index `i`. -/
def tieAtI (ε : Nat) (d : Int) : Int :=
  if 0 ≤ d then
    if d ≤ (ε : Int) then -d else -((ε : Int))
  else
    if -d ≤ (ε : Int) then -d else (ε : Int)

/-- Component of the tie adversary at index `j`. -/
def tieAtJ (ε : Nat) (d : Int) : Int :=
  if 0 ≤ d then
    if d ≤ (ε : Int) then 0 else d - (ε : Int)
  else
    if -d ≤ (ε : Int) then 0 else d + (ε : Int)

def tieDelta {n : Nat} (i j : Fin n) (ε : Nat) (s : Fin n → Int) : Fin n → Int :=
  fun t =>
    if t = i then tieAtI ε (s i - s j)
    else if t = j then tieAtJ ε (s i - s j)
    else 0

theorem tieAtI_abs (ε : Nat) (d : Int) (hgap : Int.natAbs d ≤ 2 * ε) :
    Int.natAbs (tieAtI ε d) ≤ ε := by
  have ⟨hlo, hhi⟩ := (natAbs_le_iff d (2 * ε)).mp hgap
  dsimp [tieAtI]
  by_cases hd : 0 ≤ d
  · by_cases hde : d ≤ (ε : Int)
    · simp [hd, hde]
      have : Int.natAbs (-d) = d := by rw [Int.natAbs_neg, Int.natAbs_of_nonneg hd]
      omega
    · simp [hd, hde, natAbs_neg_coe]
  · by_cases hde : -d ≤ (ε : Int)
    · simp [hd, hde]
      -- tieAtI = -d with d < 0, so value is positive `-d`
      have hnn : 0 ≤ -d := by omega
      have : Int.natAbs (-d) = -d := Int.natAbs_of_nonneg hnn
      omega
    · simp [hd, hde, natAbs_coe]

theorem tieAtJ_abs (ε : Nat) (d : Int) (hgap : Int.natAbs d ≤ 2 * ε) :
    Int.natAbs (tieAtJ ε d) ≤ ε := by
  have ⟨hlo, hhi⟩ := (natAbs_le_iff d (2 * ε)).mp hgap
  dsimp [tieAtJ]
  by_cases hd : 0 ≤ d
  · by_cases hde : d ≤ (ε : Int)
    · simp [hd, hde]
    · simp [hd, hde]
      have hnn : 0 ≤ d - (ε : Int) := by omega
      have : Int.natAbs (d - (ε : Int)) = d - (ε : Int) := Int.natAbs_of_nonneg hnn
      omega
  · by_cases hde : -d ≤ (ε : Int)
    · simp [hd, hde]
    · simp [hd, hde]
      have hnn : d + (ε : Int) ≤ 0 := by omega
      have hr : 0 ≤ -(d + (ε : Int)) := by omega
      have : Int.natAbs (d + (ε : Int)) = -(d + (ε : Int)) := by
        rw [← Int.natAbs_neg]
        exact Int.natAbs_of_nonneg hr
      omega

theorem tieDelta_in_ball {n : Nat} (i j : Fin n) (ε : Nat) (s : Fin n → Int)
    (_hne : j ≠ i) (hgap : Int.natAbs (s i - s j) ≤ 2 * ε) :
    LinfBall (tieDelta i j ε s) ε := by
  intro t
  dsimp [tieDelta]
  by_cases ht_i : t = i
  · rw [if_pos ht_i]
    exact tieAtI_abs ε (s i - s j) hgap
  · by_cases ht_j : t = j
    · rw [if_neg ht_i, if_pos ht_j]
      exact tieAtJ_abs ε (s i - s j) hgap
    · rw [if_neg ht_i, if_neg ht_j]
      simp

theorem tie_eq (ε : Nat) (d : Int) : d + tieAtI ε d = tieAtJ ε d := by
  dsimp [tieAtI, tieAtJ]
  by_cases hd : 0 ≤ d
  · by_cases hde : d ≤ (ε : Int) <;> (simp [hd, hde]; try omega)
  · by_cases hde : -d ≤ (ε : Int) <;> (simp [hd, hde]; try omega)

theorem tieDelta_ties {n : Nat} (i j : Fin n) (ε : Nat) (s : Fin n → Int)
    (hne : j ≠ i) :
    s i + tieDelta i j ε s i = s j + tieDelta i j ε s j := by
  simp [tieDelta, hne]
  have := tie_eq ε (s i - s j)
  omega

theorem kth_margin_sharpness : KthMarginSharpnessProp := by
  intro n _hn s k ε i _hk ⟨j, hjne, hgaple⟩
  refine ⟨tieDelta i j ε s, tieDelta_in_ball i j ε s hjne hgaple, ?_⟩
  intro hkeep
  have ht := tieDelta_ties i j ε s hjne
  exact hjne (hkeep.2.2 j ht.symm)

end Research.Operators.OrderStat.KthMarginInt
