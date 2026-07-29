import Research.Operators.MultiThreshold.Preservation

namespace Research.Operators.Projection.Constraint

open Research.Operators.MultiThreshold.Preservation

/- STATEMENT_BEGIN -/
def ConjunctionPreservationProp : Prop := MultiThresholdPreservationProp
def ConjunctionSharpnessProp : Prop := MultiThresholdSharpnessProp
def DisjunctionPreservationProp : Prop := MultiThresholdPreservationProp
def DisjunctionSharpnessProp : Prop := MultiThresholdSharpnessProp
/- STATEMENT_END -/

theorem conjunction_preservation : ConjunctionPreservationProp :=
  multi_threshold_preservation

theorem conjunction_sharpness : ConjunctionSharpnessProp :=
  multi_threshold_sharpness

theorem disjunction_preservation : DisjunctionPreservationProp :=
  multi_threshold_preservation

theorem disjunction_sharpness : DisjunctionSharpnessProp :=
  multi_threshold_sharpness

end Research.Operators.Projection.Constraint
