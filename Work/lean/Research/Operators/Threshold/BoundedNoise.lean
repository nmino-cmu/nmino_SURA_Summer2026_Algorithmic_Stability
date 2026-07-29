import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Threshold.Preservation

namespace Research.Operators.Threshold.BoundedNoise

open Research.Operators.Threshold.Preservation

/- STATEMENT_BEGIN -/
/--
Pathwise reading of a.s. bounded noise: if `|ξ| ≤ η`, then
`Ã_T(x)=1{x+ξ≥T}` is determined outside the unstable band.
(Measure-theoretic a.s. quantification deferred: `PATHWISE_NOT_MEASURE_THEORETIC_AS`.)
-/
def BoundedNoisePreservationProp : Prop :=
  ∀ (x T η ξ : ℝ),
    0 ≤ η →
    |ξ| ≤ η →
    ((x ≥ T + η → aboveThreshold (x + ξ) T) ∧
     (x < T - η → ¬ aboveThreshold (x + ξ) T))

/--
Sharpness for the unstable band: there exist admissible bounded noises that
flip the output relative to the clean decision on each half of the band.
-/
def BoundedNoiseSharpnessProp : Prop :=
  ∀ (x T η : ℝ),
    0 ≤ η →
    ((T ≤ x ∧ x < T + η) →
      ∃ ξ : ℝ, |ξ| ≤ η ∧ ¬ aboveThreshold (x + ξ) T) ∧
    ((T - η ≤ x ∧ x < T) →
      ∃ ξ : ℝ, |ξ| ≤ η ∧ aboveThreshold (x + ξ) T)
/- STATEMENT_END -/

theorem bounded_noise_preservation : BoundedNoisePreservationProp := by
  intro x T η ξ hη hball
  have hx' : |(x + ξ) - x| ≤ η := by
    simpa [add_sub_cancel_left] using hball
  exact (threshold_preservation x T η (x + ξ) hη hx')

theorem bounded_noise_sharpness : BoundedNoiseSharpnessProp := by
  intro x T η hη
  refine And.intro ?passBand ?failBand
  · intro ⟨_hxlo, hxhi⟩
    refine ⟨-η, ?_, ?_⟩
    · simp [abs_neg, abs_of_nonneg hη]
    · have : x + -η < T := by linarith
      intro hpass
      have : x + -η ≥ T := hpass
      linarith
  · intro ⟨hxlo, _hxhi⟩
    refine ⟨η, ?_, ?_⟩
    · simp [abs_of_nonneg hη]
    · have : x + η ≥ T := by linarith
      exact this

end Research.Operators.Threshold.BoundedNoise
