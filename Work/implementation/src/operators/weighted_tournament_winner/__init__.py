from operators.weighted_tournament_winner.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT
from operators.weighted_tournament_winner.verify import claim_is_weighted_tournament_winner_margin, verify_weighted_tournament_winner_margin
from operators.weighted_tournament_winner.workflow import run_weighted_tournament_winner_margin_workflow
__all__ = [
    "EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
    "claim_is_weighted_tournament_winner_margin", "verify_weighted_tournament_winner_margin", "run_weighted_tournament_winner_margin_workflow",
]
