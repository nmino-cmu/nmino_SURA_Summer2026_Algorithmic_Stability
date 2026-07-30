"""System B verification engines — honest PASS/PARTIAL/FAIL; no fabricated proofs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from art_int.crp import CandidateResearchPackage
from art_int.enums import AuditVerdict, ObligationStatus
from art_int.receipt import IntakeReceipt
from system_b.feedback import build_feedback_export
from system_b.obligations import ProofObligation, claim_digest


class OutcomeKind(str, Enum):
    PROOF_SUCCESS = "PROOF_SUCCESS"
    PROOF_INCOMPLETE = "PROOF_INCOMPLETE"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    UNSUPPORTED_METHOD = "UNSUPPORTED_METHOD"
    INFRA_FAILURE = "INFRA_FAILURE"
    INVALID_CANDIDATE = "INVALID_CANDIDATE"
    INVALID_ASSUMPTIONS = "INVALID_ASSUMPTIONS"


@dataclass(frozen=True)
class ObligationResult:
    obligation_digest: str
    draft_claim_digest: str
    status: ObligationStatus
    kind: OutcomeKind
    detail: str = ""


@dataclass
class VerificationRun:
    run_id: str
    crp_digest: str
    results: list[ObligationResult] = field(default_factory=list)
    audit_verdict: AuditVerdict | None = None
    limitations: list[str] = field(default_factory=list)
    counterexamples: list[dict[str, Any]] = field(default_factory=list)
    superseded_by: str | None = None
    _frozen: bool = False

    def synthesize(self) -> AuditVerdict | None:
        if any(r.kind == OutcomeKind.INFRA_FAILURE for r in self.results):
            if "INFRA_FAILURE" not in self.limitations:
                self.limitations.append("INFRA_FAILURE")
            self.audit_verdict = None
            return None
        if any(r.kind == OutcomeKind.COUNTEREXAMPLE for r in self.results):
            self.audit_verdict = AuditVerdict.FAIL
            return AuditVerdict.FAIL
        if any(r.status == ObligationStatus.FAILED for r in self.results):
            self.audit_verdict = AuditVerdict.FAIL
            return AuditVerdict.FAIL
        if all(r.status == ObligationStatus.DISCHARGED for r in self.results) and self.results:
            self.audit_verdict = AuditVerdict.PASS
            return AuditVerdict.PASS
        self.audit_verdict = AuditVerdict.ESCALATE_HUMAN
        return AuditVerdict.ESCALATE_HUMAN

    def freeze(self) -> None:
        self._frozen = True


class VerificationEngine:
    def __init__(self):
        self.runs: dict[str, VerificationRun] = {}
        self.history: list[str] = []  # run_ids in order

    def _claim_map(self, crp: CandidateResearchPackage) -> dict[str, dict[str, Any]]:
        return {claim_digest(c): c for c in crp.payload.claims}

    def _eval_statement(self, claim: dict[str, Any]) -> tuple[ObligationStatus, OutcomeKind, str]:
        """Honest evaluation: never invent proofs.

        PASS/FAIL demos require explicit claim['evaluation'] markers
        (DEMO_TAUTOLOGY / DEMO_COUNTEREXAMPLE). Unmarked statements → incomplete.
        Operator theorems use dedicated computational dischargers (e.g. argmax margin).
        """
        from operators.absolute_value_threshold.verify import (
            claim_is_abs_threshold_preservation,
            verify_abs_threshold_preservation,
        )
        from operators.argmax.verify import claim_is_argmax_margin, verify_margin_theorem
        from operators.constraint_threshold_disjunction.verify import claim_is_constraint_threshold_disjunction_preservation, verify_constraint_threshold_disjunction_preservation
        from operators.constraint_threshold_conjunction.verify import claim_is_constraint_threshold_conjunction_preservation, verify_constraint_threshold_conjunction_preservation
        from operators.feasibility_indicator.verify import claim_is_feasibility_indicator_preservation, verify_feasibility_indicator_preservation
        from operators.projection_l1_ball.verify import claim_is_projection_l1_ball_preservation, verify_projection_l1_ball_preservation
        from operators.projection_l2_ball.verify import claim_is_projection_l2_ball_preservation, verify_projection_l2_ball_preservation
        from operators.projection_simplex.verify import claim_is_projection_simplex_preservation, verify_projection_simplex_preservation
        from operators.coordinate_clipping.verify import claim_is_coordinate_clipping_preservation, verify_coordinate_clipping_preservation
        from operators.projection_box.verify import claim_is_projection_box_preservation, verify_projection_box_preservation
        from operators.projection_interval.verify import claim_is_projection_interval_preservation, verify_projection_interval_preservation
        from operators.penalized_score_selection.verify import claim_is_penalized_score_selection_margin, verify_penalized_score_selection_margin
        from operators.weighted_score_selection.verify import claim_is_weighted_score_selection_margin, verify_weighted_score_selection_margin
        from operators.groupwise_then_global_maximum.verify import claim_is_groupwise_then_global_maximum_margin, verify_groupwise_then_global_maximum_margin
        from operators.two_stage_maximum.verify import claim_is_two_stage_maximum_margin, verify_two_stage_maximum_margin
        from operators.hierarchical_maximum.verify import claim_is_hierarchical_maximum_margin, verify_hierarchical_maximum_margin
        from operators.feasible_subset_maximum.verify import claim_is_feasible_subset_maximum_margin, verify_feasible_subset_maximum_margin
        from operators.masked_maximum.verify import claim_is_masked_maximum_margin, verify_masked_maximum_margin
        from operators.filter_then_max.verify import claim_is_filter_then_max_margin, verify_filter_then_max_margin
        from operators.nms_finite.verify import claim_is_nms_finite_margin, verify_nms_finite_margin
        from operators.lexicographic_best_first.verify import claim_is_lexicographic_best_first_margin, verify_lexicographic_best_first_margin
        from operators.best_first_node_selection.verify import claim_is_best_first_node_selection_margin, verify_best_first_node_selection_margin
        from operators.greedy_choice_tie_break.verify import claim_is_greedy_choice_tie_break_margin, verify_greedy_choice_tie_break_margin
        from operators.greedy_maximum_selection.verify import claim_is_greedy_maximum_selection_margin, verify_greedy_maximum_selection_margin
        from operators.priority_queue_maximum.verify import claim_is_priority_queue_maximum_margin, verify_priority_queue_maximum_margin
        from operators.heap_extract_max.verify import claim_is_heap_extract_max_margin, verify_heap_extract_max_margin
        from operators.heap_top.verify import claim_is_heap_top_margin, verify_heap_top_margin
        from operators.tie_broken_winner.verify import claim_is_tie_broken_winner_margin, verify_tie_broken_winner_margin
        from operators.weighted_tournament_winner.verify import claim_is_weighted_tournament_winner_margin, verify_weighted_tournament_winner_margin
        from operators.tournament_winner.verify import claim_is_tournament_winner_margin, verify_tournament_winner_margin
        from operators.interval_membership.verify import (
            claim_is_interval_membership_preservation,
            verify_interval_membership_preservation,
        )
        from operators.multi_threshold.verify import (
            claim_is_multi_threshold_preservation,
            verify_multi_threshold_preservation,
        )
        from operators.quantile.verify import claim_is_quantile_margin, verify_quantile_margin
        from operators.kth_order_statistic.verify import claim_is_kth_order_statistic_margin, verify_kth_order_statistic_margin
        from operators.percentile.verify import claim_is_percentile_margin, verify_percentile_margin
        from operators.top_k.verify import claim_is_top_k_margin, verify_top_k_margin
        from operators.bucket_assignment.verify import claim_is_bucket_assignment_margin, verify_bucket_assignment_margin
        from operators.stable_partition_threshold.verify import claim_is_stable_partition_threshold_margin, verify_stable_partition_threshold_margin
        from operators.top_k_then_threshold.verify import claim_is_top_k_then_threshold_margin, verify_top_k_then_threshold_margin
        from operators.threshold_then_top_k.verify import claim_is_threshold_then_top_k_margin, verify_threshold_then_top_k_margin
        from operators.multi_criteria_lexicographic.verify import claim_is_multi_criteria_lexicographic_margin, verify_multi_criteria_lexicographic_margin
        from operators.masked_top_k.verify import claim_is_masked_top_k_margin, verify_masked_top_k_margin
        from operators.beam_pruning.verify import claim_is_beam_pruning_margin, verify_beam_pruning_margin
        from operators.lexicographic_ordering.verify import claim_is_lexicographic_ordering_margin, verify_lexicographic_ordering_margin
        from operators.rank.verify import claim_is_rank_margin, verify_rank_margin
        from operators.partial_sorting.verify import claim_is_partial_sorting_margin, verify_partial_sorting_margin
        from operators.stable_sorting.verify import claim_is_stable_sorting_margin, verify_stable_sorting_margin
        from operators.sorting.verify import claim_is_sorting_margin, verify_sorting_margin
        from operators.median.verify import claim_is_median_margin, verify_median_margin
        from operators.sign.verify import claim_is_sign_preservation, verify_sign_preservation
        from operators.thresholding.verify import (
            claim_is_bounded_noise_threshold,
            claim_is_threshold_preservation,
            verify_bounded_noise_threshold,
            verify_threshold_preservation,
        )


        if claim_is_tournament_winner_margin(claim):
            vr = verify_tournament_winner_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_weighted_tournament_winner_margin(claim):
            vr = verify_weighted_tournament_winner_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_tie_broken_winner_margin(claim):
            vr = verify_tie_broken_winner_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_heap_top_margin(claim):
            vr = verify_heap_top_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_heap_extract_max_margin(claim):
            vr = verify_heap_extract_max_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_priority_queue_maximum_margin(claim):
            vr = verify_priority_queue_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_greedy_maximum_selection_margin(claim):
            vr = verify_greedy_maximum_selection_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_greedy_choice_tie_break_margin(claim):
            vr = verify_greedy_choice_tie_break_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_best_first_node_selection_margin(claim):
            vr = verify_best_first_node_selection_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_lexicographic_best_first_margin(claim):
            vr = verify_lexicographic_best_first_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_nms_finite_margin(claim):
            vr = verify_nms_finite_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_filter_then_max_margin(claim):
            vr = verify_filter_then_max_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_masked_maximum_margin(claim):
            vr = verify_masked_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_feasible_subset_maximum_margin(claim):
            vr = verify_feasible_subset_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_hierarchical_maximum_margin(claim):
            vr = verify_hierarchical_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_two_stage_maximum_margin(claim):
            vr = verify_two_stage_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_groupwise_then_global_maximum_margin(claim):
            vr = verify_groupwise_then_global_maximum_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_weighted_score_selection_margin(claim):
            vr = verify_weighted_score_selection_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_penalized_score_selection_margin(claim):
            vr = verify_penalized_score_selection_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_projection_interval_preservation(claim):
            vr = verify_projection_interval_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_projection_box_preservation(claim):
            vr = verify_projection_box_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_coordinate_clipping_preservation(claim):
            vr = verify_coordinate_clipping_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_projection_simplex_preservation(claim):
            vr = verify_projection_simplex_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_projection_l2_ball_preservation(claim):
            vr = verify_projection_l2_ball_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_projection_l1_ball_preservation(claim):
            vr = verify_projection_l1_ball_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_feasibility_indicator_preservation(claim):
            vr = verify_feasibility_indicator_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_constraint_threshold_conjunction_preservation(claim):
            vr = verify_constraint_threshold_conjunction_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_constraint_threshold_disjunction_preservation(claim):
            vr = verify_constraint_threshold_disjunction_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_argmax_margin(claim):
            vr = verify_margin_theorem(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_threshold_preservation(claim):
            vr = verify_threshold_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_bounded_noise_threshold(claim):
            vr = verify_bounded_noise_threshold(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_multi_threshold_preservation(claim):
            vr = verify_multi_threshold_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_sign_preservation(claim):
            vr = verify_sign_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_abs_threshold_preservation(claim):
            vr = verify_abs_threshold_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_interval_membership_preservation(claim):
            vr = verify_interval_membership_preservation(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_quantile_margin(claim):
            vr = verify_quantile_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_kth_order_statistic_margin(claim):
            vr = verify_kth_order_statistic_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_percentile_margin(claim):
            vr = verify_percentile_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_sorting_margin(claim):
            vr = verify_sorting_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_stable_sorting_margin(claim):
            vr = verify_stable_sorting_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_partial_sorting_margin(claim):
            vr = verify_partial_sorting_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_rank_margin(claim):
            vr = verify_rank_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_lexicographic_ordering_margin(claim):
            vr = verify_lexicographic_ordering_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_beam_pruning_margin(claim):
            vr = verify_beam_pruning_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_masked_top_k_margin(claim):
            vr = verify_masked_top_k_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_multi_criteria_lexicographic_margin(claim):
            vr = verify_multi_criteria_lexicographic_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_threshold_then_top_k_margin(claim):
            vr = verify_threshold_then_top_k_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_top_k_then_threshold_margin(claim):
            vr = verify_top_k_then_threshold_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_stable_partition_threshold_margin(claim):
            vr = verify_stable_partition_threshold_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail


        if claim_is_bucket_assignment_margin(claim):
            vr = verify_bucket_assignment_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_top_k_margin(claim):
            vr = verify_top_k_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        if claim_is_median_margin(claim):
            vr = verify_median_margin(claim)
            if vr.ok:
                return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, vr.detail
            if vr.counterexamples:
                return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, vr.detail
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, vr.detail

        stmt = str(claim.get("statement", ""))
        mode = claim.get("evaluation")
        if mode == "DEMO_TAUTOLOGY" and stmt in ("1+1=2", "true"):
            return ObligationStatus.DISCHARGED, OutcomeKind.PROOF_SUCCESS, "demo_tautology"
        if mode == "DEMO_COUNTEREXAMPLE":
            return ObligationStatus.FAILED, OutcomeKind.COUNTEREXAMPLE, "demo_counterexample"
        if mode == "DEMO_INCOMPLETE" or stmt == "incomplete":
            return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, ""
        return ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, "no_verified_method"

    def run_from_package(
        self,
        *,
        crp: CandidateResearchPackage,
        receipt: IntakeReceipt,
        obligations: list[ProofObligation],
        assumptions: list[dict[str, Any]] | None = None,
        force_infra: bool = False,
    ) -> VerificationRun:
        """Evaluate obligations against sealed CRP payload only (no caller claim side-channel)."""
        from art_int.crp import compute_crp_digest

        run = VerificationRun(run_id=str(uuid4()), crp_digest=receipt.crp_digest)
        recomputed = compute_crp_digest(crp)
        if crp.crp_digest is not None and crp.crp_digest != recomputed:
            for o in obligations:
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.INFRA_FAILURE,
                        "crp_stated_digest_mismatch",
                    )
                )
            if "PROVENANCE_BINDING_MISMATCH" not in run.limitations:
                run.limitations.append("PROVENANCE_BINDING_MISMATCH")
            run.synthesize()
            run.freeze()
            self.runs[run.run_id] = run
            self.history.append(run.run_id)
            return run
        if recomputed != receipt.crp_digest:
            for o in obligations:
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.INFRA_FAILURE,
                        "crp_receipt_digest_mismatch",
                    )
                )
            if "PROVENANCE_BINDING_MISMATCH" not in run.limitations:
                run.limitations.append("PROVENANCE_BINDING_MISMATCH")
            run.synthesize()
            run.freeze()
            self.runs[run.run_id] = run
            self.history.append(run.run_id)
            return run
        if any(o.crp_digest != receipt.crp_digest for o in obligations):
            for o in obligations:
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.INFRA_FAILURE,
                        "obligation_receipt_digest_mismatch",
                    )
                )
            if "PROVENANCE_BINDING_MISMATCH" not in run.limitations:
                run.limitations.append("PROVENANCE_BINDING_MISMATCH")
            run.synthesize()
            run.freeze()
            self.runs[run.run_id] = run
            self.history.append(run.run_id)
            return run

        claims = self._claim_map(crp)
        assumptions = assumptions or []
        mech = bool(crp.payload.mechanism_proposals)

        if force_infra:
            for o in obligations:
                run.results.append(
                    ObligationResult(
                        o.obligation_digest, o.draft_claim_digest, ObligationStatus.OPEN, OutcomeKind.INFRA_FAILURE
                    )
                )
            run.synthesize()
            run.freeze()
            self.runs[run.run_id] = run
            self.history.append(run.run_id)
            return run

        if any(a.get("contradictory") for a in assumptions):
            for o in obligations:
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.FAILED,
                        OutcomeKind.INVALID_ASSUMPTIONS,
                    )
                )
            run.synthesize()
            run.freeze()
            self.runs[run.run_id] = run
            self.history.append(run.run_id)
            return run

        for o in obligations:
            claim = claims.get(o.draft_claim_digest)
            if claim is None:
                # characterization placeholder (no formal claims) or unknown — incomplete, never fabricate PASS
                stmt = ""
                if crp.payload.examples or not crp.payload.claims:
                    status, kind, detail = ObligationStatus.OPEN, OutcomeKind.PROOF_INCOMPLETE, "characterization"
                    run.results.append(
                        ObligationResult(o.obligation_digest, o.draft_claim_digest, status, kind, detail)
                    )
                    continue
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.INVALID_CANDIDATE,
                        "missing claim",
                    )
                )
                continue
            stmt = str(claim.get("statement", ""))

            if "unsupported" in (o.method_hint or ""):
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.UNSUPPORTED_METHOD,
                    )
                )
                continue
            if not mech and str(crp.profile.value).endswith("STABILIZATION"):
                run.results.append(
                    ObligationResult(
                        o.obligation_digest,
                        o.draft_claim_digest,
                        ObligationStatus.OPEN,
                        OutcomeKind.INVALID_CANDIDATE,
                    )
                )
                continue

            status, kind, detail = self._eval_statement(claim)
            if kind == OutcomeKind.COUNTEREXAMPLE:
                run.counterexamples.append({"claim_digest": o.draft_claim_digest, "statement": stmt})
            run.results.append(
                ObligationResult(o.obligation_digest, o.draft_claim_digest, status, kind, detail)
            )
            if (claim.get("evaluation") or "").startswith("DEMO_"):
                tag = f"DEMO_EVALUATION:{claim.get('evaluation')}"
                if tag not in run.limitations:
                    run.limitations.append(tag)
            if (
                claim.get("operator") == "argmax"
                and claim.get("theorem_id") == "bounded-perturbation-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "FINITE_SCORE_VECTORS_ONLY",
                    "ARGMAX_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "constraint-threshold-disjunction"
                and claim.get("theorem_id") == "constraint-threshold-disjunction-disjunction-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "CONSTRAINT_THRESHOLD_DISJUNCTION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "constraint-threshold-conjunction"
                and claim.get("theorem_id") == "constraint-threshold-conjunction-conjunction-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "CONSTRAINT_THRESHOLD_CONJUNCTION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "feasibility-indicator"
                and claim.get("theorem_id") == "feasibility-indicator-feasible-ball-identity"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "FEASIBILITY_INDICATOR_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "projection-l1-ball"
                and claim.get("theorem_id") == "projection-l1-ball-feasible-ball-identity"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PROJECTION_L1_BALL_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "projection-l2-ball"
                and claim.get("theorem_id") == "projection-l2-ball-feasible-ball-identity"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PROJECTION_L2_BALL_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "projection-simplex"
                and claim.get("theorem_id") == "projection-simplex-feasible-ball-identity"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PROJECTION_SIMPLEX_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "coordinate-clipping"
                and claim.get("theorem_id") == "coordinate-clipping-clamp-stability"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "COORDINATE_CLIPPING_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "projection-box"
                and claim.get("theorem_id") == "projection-box-clamp-stability"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PROJECTION_BOX_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "projection-interval"
                and claim.get("theorem_id") == "projection-interval-clamp-stability"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PROJECTION_INTERVAL_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "penalized-score-selection"
                and claim.get("theorem_id") == "penalized-score-selection-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PENALIZED_SCORE_SELECTION_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "weighted-score-selection"
                and claim.get("theorem_id") == "weighted-score-selection-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "WEIGHTED_SCORE_SELECTION_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "groupwise-then-global-maximum"
                and claim.get("theorem_id") == "groupwise-then-global-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "GROUPWISE_THEN_GLOBAL_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "two-stage-maximum"
                and claim.get("theorem_id") == "two-stage-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "TWO_STAGE_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "hierarchical-maximum"
                and claim.get("theorem_id") == "hierarchical-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "HIERARCHICAL_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "feasible-subset-maximum"
                and claim.get("theorem_id") == "feasible-subset-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "FEASIBLE_SUBSET_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "masked-maximum"
                and claim.get("theorem_id") == "masked-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "MASKED_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "filter-then-max"
                and claim.get("theorem_id") == "filter-then-max-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "FILTER_THEN_MAX_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "nms-finite"
                and claim.get("theorem_id") == "nms-finite-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "NMS_FINITE_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "lexicographic-best-first"
                and claim.get("theorem_id") == "lexicographic-best-first-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "LEXICOGRAPHIC_BEST_FIRST_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "best-first-node-selection"
                and claim.get("theorem_id") == "best-first-node-selection-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "BEST_FIRST_NODE_SELECTION_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "greedy-choice-tie-break"
                and claim.get("theorem_id") == "greedy-choice-tie-break-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "GREEDY_CHOICE_TIE_BREAK_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "greedy-maximum-selection"
                and claim.get("theorem_id") == "greedy-maximum-selection-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "GREEDY_MAXIMUM_SELECTION_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "priority-queue-maximum"
                and claim.get("theorem_id") == "priority-queue-maximum-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PRIORITY_QUEUE_MAXIMUM_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "heap-extract-max"
                and claim.get("theorem_id") == "heap-extract-max-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "HEAP_EXTRACT_MAX_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "heap-top"
                and claim.get("theorem_id") == "heap-top-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "HEAP_TOP_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "tie-broken-winner"
                and claim.get("theorem_id") == "tie-broken-winner-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "TIE_BROKEN_WINNER_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "weighted-tournament-winner"
                and claim.get("theorem_id") == "weighted-tournament-winner-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "WEIGHTED_TOURNAMENT_WINNER_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "tournament-winner"
                and claim.get("theorem_id") == "tournament-winner-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "TOURNAMENT_WINNER_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "thresholding"
                and claim.get("theorem_id") == "threshold-output-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "SCALAR_FINITE_SCORES_ONLY",
                    "THRESHOLD_PRESERVATION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "thresholding"
                and claim.get("theorem_id") == "bounded-noise-threshold"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "SCALAR_FINITE_SCORES_ONLY",
                    "BOUNDED_NOISE_NOT_FULL_SVT",
                    "THRESHOLD_BOUNDED_NOISE_COMPUTATIONAL_V1",
                    "LAPLACE_CDF_IDENTITY_NOT_DP_PROOF",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "multi-threshold"
                and claim.get("theorem_id") == "multi-threshold-count-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "FINITE_THRESHOLD_LISTS_ONLY",
                    "MULTI_THRESHOLD_PRESERVATION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "sign"
                and claim.get("theorem_id") == "sign-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "SCALAR_FINITE_SCORES_ONLY",
                    "SIGN_PRESERVATION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "absolute-value-threshold"
                and claim.get("theorem_id") == "abs-threshold-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "T_NONNEGATIVE",
                    "ABS_THRESHOLD_PRESERVATION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "interval-membership"
                and claim.get("theorem_id") == "interval-membership-preservation"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "INTERVAL_MEMBERSHIP_PRESERVATION_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "quantile"
                and claim.get("theorem_id") == "quantile-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "QUANTILE_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "kth-order-statistic"
                and claim.get("theorem_id") == "kth-order-statistic-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "KTH_ORDER_STATISTIC_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "percentile"
                and claim.get("theorem_id") == "percentile-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PERCENTILE_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)
            if (
                claim.get("operator") == "top-k"
                and claim.get("theorem_id") == "top-k-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "TOP_K_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "bucket-assignment"
                and claim.get("theorem_id") == "bucket-assignment-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "BUCKET_ASSIGNMENT_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "stable-partition-threshold"
                and claim.get("theorem_id") == "stable-partition-threshold-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "STABLE_PARTITION_THRESHOLD_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "top-k-then-threshold"
                and claim.get("theorem_id") == "top-k-then-threshold-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "TOP_K_THEN_THRESHOLD_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "threshold-then-top-k"
                and claim.get("theorem_id") == "threshold-then-top-k-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "THRESHOLD_THEN_TOP_K_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "multi-criteria-lexicographic"
                and claim.get("theorem_id") == "multi-criteria-lexicographic-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "MULTI_CRITERIA_LEXICOGRAPHIC_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "masked-top-k"
                and claim.get("theorem_id") == "masked-top-k-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "MASKED_TOP_K_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "beam-pruning"
                and claim.get("theorem_id") == "beam-pruning-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "BEAM_PRUNING_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "lexicographic-ordering"
                and claim.get("theorem_id") == "lexicographic-ordering-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "LEXICOGRAPHIC_ORDERING_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "rank"
                and claim.get("theorem_id") == "rank-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "RANK_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "partial-sorting"
                and claim.get("theorem_id") == "partial-sorting-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "PARTIAL_SORTING_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "stable-sorting"
                and claim.get("theorem_id") == "stable-sorting-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "STABLE_SORTING_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "sorting"
                and claim.get("theorem_id") == "sorting-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "SORTING_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

            if (
                claim.get("operator") == "median"
                and claim.get("theorem_id") == "median-margin"
                and status == ObligationStatus.DISCHARGED
            ):
                for lim in (
                    "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
                    "MEDIAN_MARGIN_COMPUTATIONAL_V1",
                ):
                    if lim not in run.limitations:
                        run.limitations.append(lim)

        run.synthesize()
        run.freeze()
        self.runs[run.run_id] = run
        self.history.append(run.run_id)
        return run

    # Back-compat thin wrappers used by older tests — still require sealed claims via crp when provided
    def run_phase_a(self, *, receipt, obligations, crp, **_ignored):
        if crp is None:
            raise ValueError("crp sealed package required; claim side-channel forbidden")
        return self.run_from_package(crp=crp, receipt=receipt, obligations=obligations)

    def run_theorem_pipeline(self, *, receipt, obligations, crp, assumptions=None, force_infra=False, **_ignored):
        if crp is None:
            raise ValueError("crp sealed package required; claim side-channel forbidden")
        return self.run_from_package(
            crp=crp,
            receipt=receipt,
            obligations=obligations,
            assumptions=assumptions,
            force_infra=force_infra,
        )

    def supersede(self, old_run_id: str, new_run: VerificationRun) -> VerificationRun:
        old = self.runs[old_run_id]
        if old._frozen is False:
            old.freeze()
        old.superseded_by = new_run.run_id
        if new_run.run_id not in self.runs:
            self.runs[new_run.run_id] = new_run
        if new_run.run_id not in self.history:
            self.history.append(new_run.run_id)
        return new_run

    def export(self, receipt: IntakeReceipt, obligations: list[ProofObligation], run: VerificationRun):
        discharged = [r.obligation_digest for r in run.results if r.status == ObligationStatus.DISCHARGED]
        failed = [r.obligation_digest for r in run.results if r.status == ObligationStatus.FAILED]
        unresolved = [r.obligation_digest for r in run.results if r.status == ObligationStatus.OPEN]
        # Align obligation wire statuses with evaluation
        status_map = {r.obligation_digest: r.status for r in run.results}
        wired = []
        for o in obligations:
            w = o.to_wire()
            if o.obligation_digest in status_map:
                w["status"] = status_map[o.obligation_digest].value
            wired.append(w)
        ex = build_feedback_export(
            receipt=receipt,
            obligations=obligations,
            profile=obligations[0].profile if obligations else "PHASE_A_CHARACTERIZATION",
            audit_verdict=run.audit_verdict,
            verification_run_id=run.run_id,
            counterexamples=run.counterexamples,
            failed=failed,
            unresolved=unresolved,
            discharged=discharged,
            limitations=run.limitations,
            supersedes_run_id=run.superseded_by,
        )
        ex.obligations = wired
        # re-finalize after status rewrite
        from art_int.feedback import finalize_export

        return finalize_export(ex)
