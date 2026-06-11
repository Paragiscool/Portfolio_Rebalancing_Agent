import yaml
import os
import numpy as np
from typing import Dict, Any


class CostEstimator:
    """Estimates transaction costs including explicit (fees) and implicit (market impact)."""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")

        filepath = os.path.join(config_dir, "thresholds.yaml")
        try:
            with open(filepath, "r") as f:
                config = yaml.safe_load(f)
                self.costs_config = config.get("costs", {})
        except FileNotFoundError:
            self.costs_config = {}

        # Standard explicit costs in bps (basis points)
        self.brokerage_bps = self.costs_config.get("brokerage_bps", 5)
        self.stt_bps = self.costs_config.get("stt_bps", 10)
        self.market_impact_coeff = self.costs_config.get(
            "market_impact_coefficient", 0.1
        )

    def estimate_explicit_costs(self, trade_value: float) -> float:
        """Calculate direct trading fees like brokerage and STT."""
        bps_total = self.brokerage_bps + self.stt_bps
        return abs(trade_value) * (bps_total / 10000.0)

    def estimate_implicit_costs(
        self, trade_value: float, adv: float = 1000000.0, volatility: float = 0.02
    ) -> float:
        """
        Calculate market impact using a simplified square root model:
        Cost = coeff * volatility * sqrt(|trade_value| / ADV) * |trade_value|
        ADV = Average Daily Volume (mocked to 1M if not provided)
        """
        if adv <= 0:
            return 0.0

        ratio = abs(trade_value) / adv
        impact_fraction = self.market_impact_coeff * volatility * np.sqrt(ratio)
        return abs(trade_value) * impact_fraction

    def estimate_total_costs(
        self, trade_value: float, adv: float = 1000000.0, volatility: float = 0.02
    ) -> float:
        """Combine explicit and implicit costs."""
        explicit = self.estimate_explicit_costs(trade_value)
        implicit = self.estimate_implicit_costs(trade_value, adv, volatility)
        return explicit + implicit
