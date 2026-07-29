"""Argmax operator research package."""

from operators.argmax.math import (
    EVALUATION_METHOD,
    OPERATOR,
    THEOREM_ID,
    THEOREM_STATEMENT,
    ArgmaxInstance,
    adversarial_break,
    invariance_holds,
)
from operators.argmax.verify import verify_margin_theorem
from operators.argmax.workflow import (
    run_argmax_margin_workflow,
    run_argmax_selection_stability_workflow,
)

__all__ = [
    "OPERATOR",
    "THEOREM_ID",
    "EVALUATION_METHOD",
    "THEOREM_STATEMENT",
    "ArgmaxInstance",
    "adversarial_break",
    "invariance_holds",
    "verify_margin_theorem",
    "run_argmax_margin_workflow",
    "run_argmax_selection_stability_workflow",
]
