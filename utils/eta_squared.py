"""Utility functions for calculating eta-squared effect size."""
import numpy as np


def eta_squared_anova(groups: list[np.ndarray]) -> float:
    """Compute eta-squared effect size from groups used in ANOVA.
    Args:
        groups (list of np.ndarray): List of arrays, each containing values
            for a different group.
    Returns:
        float: Eta-squared effect size.
    """
    all_values = np.concatenate(groups)  # Combine all group values
    grand_mean = np.mean(all_values)  # Overall mean

    # Sum of squares calculations

    # Between-group sum of squares
    ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)

    # Total sum of squares
    ss_total = np.sum((all_values - grand_mean) ** 2)

    # Eta-squared calculation
    return ss_between / ss_total if ss_total > 0 else np.nan
