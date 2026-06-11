import yaml
import os
from typing import Dict, Any


class ThresholdManager:
    """Manages risk-category-specific and client-overlay thresholds for portfolio rebalancing."""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")

        self.config_dir = config_dir
        self.risk_categories: Dict[str, Any] = self._load_config(
            "risk_categories.yaml"
        ).get("risk_categories", {})
        self.system_thresholds: Dict[str, Any] = self._load_config("thresholds.yaml")

    def _load_config(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.config_dir, filename)
        try:
            with open(filepath, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def get_drift_band(self, risk_category: str) -> float:
        """Get the drift band threshold for a given risk category."""
        category_data = self.risk_categories.get(risk_category, {})
        # Default to a safe 0.02 (2%) if not found
        return category_data.get("drift_band", 0.02)

    def get_target_allocation(self, risk_category: str) -> Dict[str, float]:
        """Get the target asset allocation for a given risk category."""
        category_data = self.risk_categories.get(risk_category, {})
        return category_data.get("target_allocations", {})

    def get_system_trigger_threshold(self, trigger_key: str) -> float:
        """Get a system-wide trigger threshold (e.g., factor_tilt_std_dev)."""
        return self.system_thresholds.get("triggers", {}).get(trigger_key, 0.0)

    def get_client_overlay_threshold(
        self, client_id: str, default_band: float
    ) -> float:
        """
        In a real system, this would query a database for client-specific overrides.
        For now, returns the default band.
        """
        return default_band
