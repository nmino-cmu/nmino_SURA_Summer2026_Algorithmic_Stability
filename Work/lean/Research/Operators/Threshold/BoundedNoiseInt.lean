import Research.Operators.Threshold.PreservationInt
import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Threshold.BoundedNoiseInt

open Research.Operators.Argmax.BasicInt
open Research.Operators.Threshold.PreservationInt

/- STATEMENT_BEGIN -/
/--
Pathwise reading of a.s. bounded noise: if `|ξ| ≤ η`, then
`Ã_T(x)=1{x+ξ≥T}` is determined outside the unstable band.
(Int archive; measure-theoretic a.s. quantification deferred.)
-/
def BoundedNoisePreservationProp : Prop :=
  ∀ (x T : Int) (η : Nat) (ξ : Int),
    Int.natAbs ξ ≤ η →
    ((x ≥ T + (η : Int) → aboveThreshold (x + ξ) T = true) ∧
     (x < T - (η : Int) → aboveThreshold (x + ξ) T = false))

/--
Sharpness for the unstable band: there exist admissible bounded noises that
flip the output relative to the clean decision on each half of the band.
-/
def BoundedNoiseSharpnessProp : Prop :=
  ∀ (x T : Int) (η : Nat),
    ((T ≤ x ∧ x < T + (η : Int)) →
      ∃ ξ : Int, Int.natAbs ξ ≤ η ∧ aboveThreshold (x + ξ) T = false) ∧
    ((T - (η : Int) ≤ x ∧ x < T) →
      ∃ ξ : Int, Int.natAbs ξ ≤ η ∧ aboveThreshold (x + ξ) T = true)
/- STATEMENT_END -/

theorem bounded_noise_preservation : BoundedNoisePreservationProp := by
  intro x T η ξ hball
  have hx' : Int.natAbs ((x + ξ) - x) ≤ η := by
    have : (x + ξ) - x = ξ := by omega
    simpa [this] using hball
  exact (threshold_preservation x T η (x + ξ)) hx'

theorem bounded_noise_sharpness : BoundedNoiseSharpnessProp := by
  intro x T η
  refine And.intro ?passBand ?failBand
  · intro ⟨hxlo, hxhi⟩
    -- push down by η: x + (-η) < T when x < T+η
    refine ⟨-((η : Int)), ?_, ?_⟩
    · simp [Int.natAbs_neg]
    · have : x + -((η : Int)) < T := by omega
      have hge : ¬ (x + -((η : Int)) ≥ T) := by omega
      simp [aboveThreshold, hge]
  · intro ⟨hxlo, hxhi⟩
    -- push up by η: x + η ≥ T when x ≥ T-η
    refine ⟨(η : Int), ?_, ?_⟩
    · simp
    · have : x + (η : Int) ≥ T := by omega
      simp [aboveThreshold, this]

end Research.Operators.Threshold.BoundedNoiseInt
