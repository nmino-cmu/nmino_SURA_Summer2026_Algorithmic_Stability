from operators.tournament_winner.math import EVALUATION_METHOD, OPERATOR, THEOREM_ID, THEOREM_STATEMENT
from operators.tournament_winner.verify import claim_is_tournament_winner_margin, verify_tournament_winner_margin
from operators.tournament_winner.workflow import run_tournament_winner_margin_workflow
__all__ = [
    "EVALUATION_METHOD", "OPERATOR", "THEOREM_ID", "THEOREM_STATEMENT",
    "claim_is_tournament_winner_margin", "verify_tournament_winner_margin", "run_tournament_winner_margin_workflow",
]
