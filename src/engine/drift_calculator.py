import numpy as np
import pandas as pd
from typing import Dict, Any


class DriftCalculator:
    """Calculates various drift metrics for a DataFrame of portfolios."""

    def __init__(self, threshold_manager):
        self.threshold_manager = threshold_manager
        # Mapping columns to config keys
        self.asset_classes = ["Equity", "Fixed Income", "Alternatives", "Cash"]
        self.weight_cols = {
            "Equity": "equity_weight",
            "Fixed Income": "fixed_income_weight",
            "Alternatives": "alternatives_weight",
            "Cash": "cash_weight",
        }

    def calculate_drift(self, portfolios_df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes absolute drift, sum of absolute drift, and RMS drift.
        Uses vectorised Pandas operations for high performance.
        """
        # Make a copy to avoid SettingWithCopyWarning
        df = portfolios_df.copy()

        # Initialize target columns
        for ac in self.asset_classes:
            df[f"target_{self.weight_cols[ac]}"] = 0.0

        # Map target allocations based on risk category
        risk_cats = df["risk_category"].unique()
        for cat in risk_cats:
            target_allocs = self.threshold_manager.get_target_allocation(cat)
            mask = df["risk_category"] == cat
            for ac in self.asset_classes:
                if ac in target_allocs:
                    df.loc[mask, f"target_{self.weight_cols[ac]}"] = target_allocs[ac]

        # Calculate Absolute Drift per asset class
        for ac in self.asset_classes:
            current_col = self.weight_cols[ac]
            target_col = f"target_{current_col}"
            df[f"{current_col}_drift"] = df[current_col] - df[target_col]
            df[f"{current_col}_abs_drift"] = df[f"{current_col}_drift"].abs()

        # Sum of Absolute Drift (SAD)
        abs_drift_cols = [
            f"{self.weight_cols[ac]}_abs_drift" for ac in self.asset_classes
        ]
        df["sum_absolute_drift"] = df[abs_drift_cols].sum(axis=1)

        # Root Mean Square Drift (RMSD)
        squared_drift_cols = [
            df[f"{self.weight_cols[ac]}_drift"] ** 2 for ac in self.asset_classes
        ]
        df["rms_drift"] = np.sqrt(sum(squared_drift_cols) / len(self.asset_classes))

        # Map the allowable drift band
        df["drift_band"] = df["risk_category"].apply(
            self.threshold_manager.get_drift_band
        )

        # Max Absolute Drift across asset classes
        df["max_abs_drift"] = df[abs_drift_cols].max(axis=1)

        # Determine if rebalance is needed (if max absolute drift > drift band)
        df["needs_rebalance"] = df["max_abs_drift"] > df["drift_band"]

        return df
