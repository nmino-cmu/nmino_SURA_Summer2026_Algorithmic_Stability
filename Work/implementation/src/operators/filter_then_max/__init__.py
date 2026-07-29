from operators.filter_then_max.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT
from operators.filter_then_max.verify import claim_is_filter_then_max_margin, verify_filter_then_max_margin
from operators.filter_then_max.workflow import run_filter_then_max_margin_workflow
__all__ = [
    "EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
    "claim_is_filter_then_max_margin", "verify_filter_then_max_margin", "run_filter_then_max_margin_workflow",
]
