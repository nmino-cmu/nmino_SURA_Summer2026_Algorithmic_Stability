import Mathlib.Algebra.Order.Group.MinMax
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.Projection.Clamp

open Research.Operators.Argmax.Basic

/-- Absolute-value projection onto a closed interval `[lo, hi]` (`max lo (min x hi)`). -/
def clamp (x lo hi : ℝ) : ℝ :=
  max lo (min x hi)

/- STATEMENT_BEGIN -/
/-- Clamp is 1-Lipschitz (nonexpansive) on `ℝ` when `lo ≤ hi`. -/
def ClampNonexpansiveProp : Prop :=
  ∀ (x y lo hi : ℝ),
    lo ≤ hi →
    |clamp x lo hi - clamp y lo hi| ≤ |x - y|

/-- Stability form: `|x' - x| ≤ ε` ⇒ `|clamp x' - clamp x| ≤ ε`. -/
def ClampStabilityProp : Prop :=
  ∀ (x lo hi ε x' : ℝ),
    lo ≤ hi →
    0 ≤ ε →
    |x' - x| ≤ ε →
    |clamp x' lo hi - clamp x lo hi| ≤ ε

/-- Lipschitz constant 1 is sharp. -/
def ClampSharpnessProp : Prop :=
  ∀ (ε : ℝ),
    1 ≤ ε →
    ∃ (x y lo hi : ℝ),
      lo ≤ hi ∧
      |x - y| = ε ∧
      |clamp x lo hi - clamp y lo hi| = ε
/- STATEMENT_END -/

theorem clamp_nonexpansive : ClampNonexpansiveProp := by
  intro x y lo hi _hle
  -- |max lo (min x hi) - max lo (min y hi)| ≤ |min x hi - min y hi| ≤ |x - y|
  have hmin : |min x hi - min y hi| ≤ |x - y| := by
    have := abs_min_sub_min_le_max x hi y hi
    simpa [max_self] using this
  have hmax : |max lo (min x hi) - max lo (min y hi)| ≤ |min x hi - min y hi| := by
    have := abs_max_sub_max_le_max lo (min x hi) lo (min y hi)
    simpa [max_self] using this
  calc
    |clamp x lo hi - clamp y lo hi| = |max lo (min x hi) - max lo (min y hi)| := by
      simp [clamp]
    _ ≤ |min x hi - min y hi| := hmax
    _ ≤ |x - y| := hmin

theorem clamp_stability : ClampStabilityProp := by
  intro x lo hi ε x' hle _hε hball
  exact le_trans (clamp_nonexpansive x' x lo hi hle) hball

theorem clamp_sharpness : ClampSharpnessProp := by
  intro ε hε
  refine ⟨ε, 0, 0, ε, ?_, ?_, ?_⟩
  · linarith
  · simp [abs_of_nonneg (by linarith : (0 : ℝ) ≤ ε)]
  · have hx : clamp ε 0 ε = ε := by
      simp [clamp, min_self, max_eq_right (by linarith : (0 : ℝ) ≤ ε)]
    have hy : clamp (0 : ℝ) 0 ε = 0 := by
      simp [clamp, min_eq_left (by linarith : (0 : ℝ) ≤ ε)]
    simp [hx, hy, abs_of_nonneg (by linarith : (0 : ℝ) ≤ ε)]

end Research.Operators.Projection.Clamp
