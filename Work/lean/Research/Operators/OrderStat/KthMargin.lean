import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Research.Operators.OrderStat.Basic
import Research.Operators.Argmax.Basic

noncomputable section

namespace Research.Operators.OrderStat.KthMargin

open Research.Operators.OrderStat.Basic
open Research.Operators.Argmax.Basic

/-- Unique index `i` is the strict `k`-th smallest (0-based). -/
def IsStrictKthSmallest {n : Nat} (s : Fin n → ℝ) (k : Nat) (i : Fin n) : Prop :=
  k < n ∧ countLT s (s i) = k ∧ (∀ j : Fin n, s j = s i → j = i)

/-- Every pair of distinct scores is separated by more than `g`. -/
def AllGapsExceed {n : Nat} (s : Fin n → ℝ) (g : ℝ) : Prop :=
  ∀ i j : Fin n, i ≠ j → g < |s i - s j|

/- STATEMENT_BEGIN -/
def KthMarginInvarianceProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → ℝ) (k : Nat) (ε : ℝ) (i : Fin n),
    0 ≤ ε →
    IsStrictKthSmallest s k i →
    AllGapsExceed s (2 * ε) →
    ∀ δ : Fin n → ℝ, LinfBall δ ε →
      IsStrictKthSmallest (fun j => s j + δ j) k i

def KthMarginSharpnessProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → ℝ) (k : Nat) (ε : ℝ) (i : Fin n),
    0 ≤ ε →
    IsStrictKthSmallest s k i →
    (∃ j : Fin n, j ≠ i ∧ |s i - s j| ≤ 2 * ε) →
    ∃ δ : Fin n → ℝ, LinfBall δ ε ∧
      ¬ IsStrictKthSmallest (fun t => s t + δ t) k i
/- STATEMENT_END -/

theorem strict_lt_preserved (a b δa δb ε : ℝ)
    (hlt : a < b) (hgap : 2 * ε < b - a)
    (ha : |δa| ≤ ε) (hb : |δb| ≤ ε) :
    a + δa < b + δb := by
  have ha' := (abs_le_iff δa ε).mp ha
  have hb' := (abs_le_iff δb ε).mp hb
  linarith

theorem pairwise_lt_iff {n : Nat} (s δ : Fin n → ℝ) (ε : ℝ) (p q : Fin n)
    (hε : 0 ≤ ε) (hball : LinfBall δ ε) (_hne : p ≠ q)
    (hgap : 2 * ε < |s p - s q|) :
    s p < s q ↔ s p + δ p < s q + δ q := by
  have hp := hball p
  have hq := hball q
  constructor
  · intro hlt
    have hpos : 0 < s q - s p := sub_pos.mpr hlt
    have : |s p - s q| = s q - s p := by
      rw [abs_sub_comm]
      exact abs_of_pos hpos
    exact strict_lt_preserved (s p) (s q) (δ p) (δ q) ε hlt (by linarith) hp hq
  · intro hlt'
    have hne_val : s p ≠ s q := by
      intro heq
      have : |s p - s q| = 0 := by simp [heq]
      linarith
    cases lt_or_gt_of_ne hne_val with
    | inl hlt => exact hlt
    | inr hgt =>
      have : |s p - s q| = s p - s q := abs_of_pos (sub_pos.mpr hgt)
      have : s p + δ p > s q + δ q :=
        strict_lt_preserved (s q) (s p) (δ q) (δ p) ε hgt (by linarith) hq hp
      linarith

theorem countLT_of_iff :
    ∀ {n : Nat} (s s' : Fin n → ℝ) (v v' : ℝ),
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

theorem all_gaps_imply_below_iff {n : Nat} (s δ : Fin n → ℝ) (ε : ℝ) (i : Fin n)
    (hε : 0 ≤ ε) (hball : LinfBall δ ε) (hgaps : AllGapsExceed s (2 * ε)) :
    ∀ j : Fin n, s j < s i ↔ s j + δ j < s i + δ i := by
  intro j
  by_cases h : j = i
  · subst h; constructor <;> intro hlt <;> linarith
  · exact pairwise_lt_iff s δ ε j i hε hball h (hgaps j i h)

theorem uniqueness_preserved {n : Nat} (s δ : Fin n → ℝ) (ε : ℝ) (i : Fin n)
    (hε : 0 ≤ ε) (hball : LinfBall δ ε) (hgaps : AllGapsExceed s (2 * ε)) :
    ∀ j : Fin n, s j + δ j = s i + δ i → j = i := by
  intro j hj
  by_cases h : j = i
  · exact h
  · have hgapji := hgaps j i h
    have hp := hball i
    have hq := hball j
    have hne_val : s j ≠ s i := by
      intro heq
      have : |s j - s i| = 0 := by simp [heq]
      linarith
    have : s j + δ j ≠ s i + δ i := by
      cases lt_or_gt_of_ne hne_val with
      | inl hlt =>
        have := strict_lt_preserved (s j) (s i) (δ j) (δ i) ε hlt (by
          have habs : |s j - s i| = s i - s j := by
            rw [abs_sub_comm]; exact abs_of_pos (sub_pos.mpr hlt)
          linarith) hq hp
        linarith
      | inr hgt =>
        have := strict_lt_preserved (s i) (s j) (δ i) (δ j) ε hgt (by
          have habs : |s j - s i| = s j - s i := abs_of_pos (sub_pos.mpr hgt)
          linarith) hp hq
        linarith
    exact (this hj).elim

theorem kth_margin_invariance : KthMarginInvarianceProp := by
  intro n _hn s k ε i hε ⟨hk, hcount, _⟩ hgaps δ hball
  refine And.intro hk (And.intro ?count ?uniq)
  · have hiff := all_gaps_imply_below_iff s δ ε i hε hball hgaps
    have hcongr := countLT_of_iff s (fun j => s j + δ j) (s i) (s i + δ i) hiff
    exact hcongr.symm.trans hcount
  · exact uniqueness_preserved s δ ε i hε hball hgaps

/-- Midpoint collision adversary for a close pair. -/
def tieDelta {n : Nat} (i j : Fin n) (s : Fin n → ℝ) : Fin n → ℝ :=
  fun t =>
    let d := s i - s j
    if t = i then -d / 2 else if t = j then d / 2 else 0

theorem tieDelta_in_ball {n : Nat} (i j : Fin n) (ε : ℝ) (s : Fin n → ℝ)
    (hε : 0 ≤ ε) (hgap : |s i - s j| ≤ 2 * ε) :
    LinfBall (tieDelta i j s) ε := by
  intro t
  have hhalf : |s i - s j| / 2 ≤ ε := by linarith
  have hhalf' : |(s i - s j) / 2| ≤ ε := by
    simpa [abs_div, abs_two] using hhalf
  dsimp [tieDelta]
  by_cases ht_i : t = i
  · simp only [ht_i, ↓reduceIte, abs_neg]
    -- goal: |(s i - s j)/2| ≤ ε after abs_neg turns -d/2 into ...
    convert hhalf' using 1
    · simp [abs_div, abs_neg, abs_sub_comm, abs_two]
  · by_cases ht_j : t = j
    · simp only [ht_i, ht_j, ↓reduceIte]
      split_ifs with hji
      · -- j = i impossible with ht_i false and ht_j; still handle
        subst hji
        simp [abs_zero, hε] at *
      · exact hhalf'
    · simp [ht_i, ht_j, abs_zero, hε]

theorem tieDelta_ties {n : Nat} (i j : Fin n) (s : Fin n → ℝ)
    (hne : j ≠ i) :
    s i + tieDelta i j s i = s j + tieDelta i j s j := by
  dsimp [tieDelta]
  simp [hne]
  ring

theorem kth_margin_sharpness : KthMarginSharpnessProp := by
  intro n _hn s k ε i hε _hk ⟨j, hjne, hgaple⟩
  refine ⟨tieDelta i j s, tieDelta_in_ball i j ε s hε hgaple, ?_⟩
  intro hkeep
  have ht := tieDelta_ties i j s hjne
  exact hjne (hkeep.2.2 j ht.symm)

end Research.Operators.OrderStat.KthMargin
