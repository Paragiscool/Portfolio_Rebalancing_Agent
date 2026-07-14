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
                self.tax_liquidity_config = config.get("tax_and_liquidity", {})
        except FileNotFoundError:
            self.constraints_config = {}
            self.tax_liquidity_config = {}

        self.max_turnover = self.constraints_config.get("max_turnover", 0.20)
        self.min_trade_size = self.constraints_config.get("minimum_trade_size", 1000)
        self.max_adv_participation = self.tax_liquidity_config.get("max_adv_participation_rate", 0.05)

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

    def get_max_adv_participation(self) -> float:
        return self.max_adv_participation
        
    def get_liquidity_bounds_weights(self, total_portfolio_value: float, market_data: Dict[str, Any]):
        """
        Convert ADV limits into maximum allowable weight changes per security.
        market_data should contain:
        - "prices": np.ndarray (current prices)
        - "adv": np.ndarray (average daily volume)
        Returns np.ndarray of max weight change, or None if data missing.
        """
        prices = market_data.get("prices")
        adv = market_data.get("adv")
        
        if prices is None or adv is None:
            return None
            
        # Max shares allowed to trade in a day
        max_shares = adv * self.max_adv_participation
        
        # Dollar value of max shares
        max_dollar_trade = max_shares * prices
        
        # As a percentage of total portfolio value
        max_weight_change = max_dollar_trade / total_portfolio_value
        
        return max_weight_change
