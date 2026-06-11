import yaml
import os
from typing import Dict, Any


class ConstraintManager:
    """Manages rules and limits for portfolio optimization."""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")

        filepath = os.path.join(config_dir, "thresholds.yaml")
        try:
            with open(filepath, "r") as f:
                config = yaml.safe_load(f)
                self.constraints_config = config.get("constraints", {})
        except FileNotFoundError:
            self.constraints_config = {}

        self.max_turnover = self.constraints_config.get("max_turnover", 0.20)
        self.min_trade_size = self.constraints_config.get("minimum_trade_size", 1000)

    def get_max_turnover(self) -> float:
        """Maximum allowed turnover (e.g., 0.20 means 20% of portfolio value)."""
        return self.max_turnover

    def get_min_trade_size(self) -> float:
        """Minimum trade size in base currency to avoid dust trades."""
        return self.min_trade_size

    def get_sector_concentration_limit(self) -> float:
        """Maximum allowed weight in a single sector."""
        # Typically sourced from thresholds or config, assuming 10% here
        return 0.10
