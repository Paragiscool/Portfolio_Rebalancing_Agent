import pandas as pd
from typing import List, Dict


class DriftMonitor:
    """Service to scan portfolios, compute drift, and return prioritized rebalancing queue."""

    def __init__(self, drift_calculator):
        self.drift_calculator = drift_calculator

    def scan_portfolios(self, portfolios_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates drift for all portfolios and filters out those exceeding their drift band.
        Returns them sorted by severity (highest drift first).
        """
        # Calculate drift metrics
        analyzed_df = self.drift_calculator.calculate_drift(portfolios_df)

        # Filter for those needing rebalancing
        breached_df = analyzed_df[analyzed_df["needs_rebalance"]].copy()

        # Calculate a severity score (how much they exceeded the band relative to the band itself or absolute)
        # We use absolute exceedance here for simplicity, but could be proportional
        breached_df["drift_severity"] = (
            breached_df["max_abs_drift"] - breached_df["drift_band"]
        )

        # Sort by severity descending (highest priority first)
        prioritized_queue = breached_df.sort_values(
            by="drift_severity", ascending=False
        )

        return prioritized_queue
