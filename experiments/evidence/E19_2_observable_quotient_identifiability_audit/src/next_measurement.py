"""Next measurement selection for OQCI.

Given the current ambiguity analysis, recommends which next measurement
would most reduce ambiguity among hypotheses.

Candidate next experiments:
- second sensor height
- third sensor height
- alternative load/excitation state
- additional field component
- restricted high-resolution local scan
"""

from __future__ import annotations

import numpy as np


def score_next_measurement(
    current_nullspace: dict,
    candidate_heights: list[float],
    current_height: float,
    near_null_threshold: float = 0.01,
) -> dict:
    """Score candidate next measurements by predicted ambiguity reduction.

    For each candidate height, estimate how many near-null modes would become
    observable based on the geometric change in the forward operator.

    This is a geometric heuristic: adding a second height changes the Biot-Savart
    kernel, so modes that are degenerate at one height may become distinguishable.
    """
    recommendations = []

    for h in candidate_heights:
        if abs(h - current_height) < 0.01:
            continue

        # Heuristic: standoff change ratio estimates new information
        height_ratio = h / max(current_height, 1e-6)
        new_information_estimate = min(1.0, abs(height_ratio - 1.0) * 5.0)

        # Predicted near-null reduction
        current_nn = current_nullspace["near_null_count"]
        predicted_nn = max(0, int(current_nn * (1.0 - new_information_estimate * 0.5)))
        nn_reduction = current_nn - predicted_nn

        # Predicted effective rank increase
        current_er = current_nullspace["effective_rank"]
        predicted_er = min(current_nullspace["total_rank"], current_er + int(nn_reduction * 0.6))
        rank_increase = predicted_er - current_er

        score = new_information_estimate + 0.3 * nn_reduction / max(current_nn, 1) + 0.2 * rank_increase / max(current_er, 1)

        recommendations.append({
            "candidate": f"add_height_{h:.1f}um",
            "height_um": h,
            "new_information_estimate": new_information_estimate,
            "predicted_near_null_reduction": nn_reduction,
            "predicted_rank_increase": rank_increase,
            "score": score,
        })

    # Also recommend multi-state if applicable
    recommendations.append({
        "candidate": "add_second_excitation_state",
        "rationale": "A different current injection pattern changes which current paths are excited",
        "predicted_near_null_reduction": "unknown",
        "predicted_rank_increase": "unknown",
        "score": 0.5,
    })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return {
        "current_heights": [current_height],
        "candidates_evaluated": len(recommendations),
        "top_recommendation": recommendations[0]["candidate"] if recommendations else "none",
        "recommendation_score": recommendations[0]["score"] if recommendations else 0.0,
        "all_recommendations": recommendations,
    }
