import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Projection.ClampInt

open Research.Operators.Argmax.BasicInt

def clamp (x lo hi : Int) : Int :=
  max lo (min x hi)

def ClampNonexpansiveProp : Prop :=
  ∀ (x y lo hi : Int),
    lo ≤ hi →
    Int.natAbs (clamp x lo hi - clamp y lo hi) ≤ Int.natAbs (x - y)

def ClampStabilityProp : Prop :=
  ∀ (x lo hi : Int) (ε : Nat) (x' : Int),
    lo ≤ hi →
    Int.natAbs (x' - x) ≤ ε →
    Int.natAbs (clamp x' lo hi - clamp x lo hi) ≤ ε

def ClampSharpnessProp : Prop :=
  ∀ (ε : Nat),
    1 ≤ ε →
    ∃ (x y lo hi : Int),
      lo ≤ hi ∧
      Int.natAbs (x - y) = ε ∧
      Int.natAbs (clamp x lo hi - clamp y lo hi) = ε

theorem clamp_nonexpansive : ClampNonexpansiveProp := by
  intro x y lo hi hle
  simp only [clamp]
  omega

theorem clamp_stability : ClampStabilityProp := by
  intro x lo hi ε x' hle hball
  have hne := clamp_nonexpansive x' x lo hi hle
  omega

theorem clamp_sharpness : ClampSharpnessProp := by
  intro ε hε
  refine ⟨(ε : Int), (0 : Int), (0 : Int), (ε : Int), ?hle, ?hdiff, ?hclamp⟩
  · omega
  · simp [Int.natAbs]
  · have hx : clamp (ε : Int) 0 (ε : Int) = (ε : Int) := by
      simp [clamp]; omega
    have hy : clamp (0 : Int) 0 (ε : Int) = (0 : Int) := by
      simp [clamp]; omega
    simp [hx, hy, Int.natAbs]

end Research.Operators.Projection.ClampInt
