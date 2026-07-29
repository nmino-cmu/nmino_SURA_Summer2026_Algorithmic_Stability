"""Registered Lean formalization profiles (fail-closed allowlist)."""

from __future__ import annotations

from types import ModuleType
from typing import Any

from operators.absolute_value_threshold import lean_profile as abs_threshold_profile
from operators.argmax import lean_profile as argmax_profile
from operators.constraint_threshold_disjunction import lean_profile as constraint_threshold_disjunction_profile
from operators.constraint_threshold_conjunction import lean_profile as constraint_threshold_conjunction_profile
from operators.feasibility_indicator import lean_profile as feasibility_indicator_profile
from operators.projection_l1_ball import lean_profile as projection_l1_ball_profile
from operators.projection_l2_ball import lean_profile as projection_l2_ball_profile
from operators.projection_simplex import lean_profile as projection_simplex_profile
from operators.coordinate_clipping import lean_profile as coordinate_clipping_profile
from operators.projection_box import lean_profile as projection_box_profile
from operators.projection_interval import lean_profile as projection_interval_profile
from operators.penalized_score_selection import lean_profile as penalized_score_selection_profile
from operators.weighted_score_selection import lean_profile as weighted_score_selection_profile
from operators.groupwise_then_global_maximum import lean_profile as groupwise_then_global_maximum_profile
from operators.two_stage_maximum import lean_profile as two_stage_maximum_profile
from operators.hierarchical_maximum import lean_profile as hierarchical_maximum_profile
from operators.feasible_subset_maximum import lean_profile as feasible_subset_maximum_profile
from operators.masked_maximum import lean_profile as masked_maximum_profile
from operators.filter_then_max import lean_profile as filter_then_max_profile
from operators.nms_finite import lean_profile as nms_finite_profile
from operators.lexicographic_best_first import lean_profile as lexicographic_best_first_profile
from operators.best_first_node_selection import lean_profile as best_first_node_selection_profile
from operators.greedy_choice_tie_break import lean_profile as greedy_choice_tie_break_profile
from operators.greedy_maximum_selection import lean_profile as greedy_maximum_selection_profile
from operators.priority_queue_maximum import lean_profile as priority_queue_maximum_profile
from operators.heap_extract_max import lean_profile as heap_extract_max_profile
from operators.heap_top import lean_profile as heap_top_profile
from operators.tie_broken_winner import lean_profile as tie_broken_winner_profile
from operators.weighted_tournament_winner import lean_profile as weighted_tournament_winner_profile
from operators.tournament_winner import lean_profile as tournament_winner_profile
from operators.interval_membership import lean_profile as interval_membership_profile
from operators.multi_threshold import lean_profile as multi_threshold_profile
from operators.quantile import lean_profile as quantile_profile
from operators.kth_order_statistic import lean_profile as kth_order_statistic_profile
from operators.percentile import lean_profile as percentile_profile
from operators.median import lean_profile as median_profile
from operators.top_k import lean_profile as top_k_profile
from operators.bucket_assignment import lean_profile as bucket_assignment_profile
from operators.stable_partition_threshold import lean_profile as stable_partition_threshold_profile
from operators.top_k_then_threshold import lean_profile as top_k_then_threshold_profile
from operators.threshold_then_top_k import lean_profile as threshold_then_top_k_profile
from operators.multi_criteria_lexicographic import lean_profile as multi_criteria_lexicographic_profile
from operators.masked_top_k import lean_profile as masked_top_k_profile
from operators.beam_pruning import lean_profile as beam_pruning_profile
from operators.lexicographic_ordering import lean_profile as lexicographic_ordering_profile
from operators.rank import lean_profile as rank_profile
from operators.partial_sorting import lean_profile as partial_sorting_profile
from operators.stable_sorting import lean_profile as stable_sorting_profile
from operators.sorting import lean_profile as sorting_profile
from operators.sign import lean_profile as sign_profile
from operators.thresholding import lean_profile as threshold_profile
from operators.thresholding import lean_profile_noise as threshold_noise_profile

_PROFILES: tuple[ModuleType, ...] = (
    argmax_profile,
    threshold_profile,
    threshold_noise_profile,
    multi_threshold_profile,
    sign_profile,
    abs_threshold_profile,
    interval_membership_profile,
    quantile_profile,
    median_profile,
    percentile_profile,
    kth_order_statistic_profile,
    top_k_profile,
    sorting_profile,
    stable_sorting_profile,
    partial_sorting_profile,
    rank_profile,
    lexicographic_ordering_profile,
    tournament_winner_profile,
    weighted_tournament_winner_profile,
    tie_broken_winner_profile,
    heap_top_profile,
    heap_extract_max_profile,
    priority_queue_maximum_profile,
    greedy_maximum_selection_profile,
    greedy_choice_tie_break_profile,
    best_first_node_selection_profile,
    lexicographic_best_first_profile,
    nms_finite_profile,
    filter_then_max_profile,
    masked_maximum_profile,
    feasible_subset_maximum_profile,
    hierarchical_maximum_profile,
    two_stage_maximum_profile,
    groupwise_then_global_maximum_profile,
    weighted_score_selection_profile,
    penalized_score_selection_profile,
    beam_pruning_profile,
    masked_top_k_profile,
    multi_criteria_lexicographic_profile,
    threshold_then_top_k_profile,
    top_k_then_threshold_profile,
    stable_partition_threshold_profile,
    bucket_assignment_profile,
    projection_interval_profile,
    projection_box_profile,
    coordinate_clipping_profile,
    projection_simplex_profile,
    projection_l2_ball_profile,
    projection_l1_ball_profile,
    feasibility_indicator_profile,
    constraint_threshold_conjunction_profile,
    constraint_threshold_disjunction_profile,
)


def resolve_profile(claim: dict[str, Any]) -> ModuleType | None:
    for p in _PROFILES:
        if p.claim_matches_profile(claim):
            return p
    return None


def all_profiles() -> tuple[ModuleType, ...]:
    return _PROFILES
