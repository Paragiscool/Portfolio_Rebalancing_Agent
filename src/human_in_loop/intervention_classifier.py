from typing import Dict, Any, List

class InterventionLevel:
    INFORMATIONAL = "INFORMATIONAL"
    ADVISORY = "ADVISORY"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    ESCALATION = "ESCALATION"
    HALT = "HALT"

class KillSwitchException(Exception):
    pass

class InterventionClassifier:
    def __init__(self, max_vix: float = 40.0, max_error_rate: float = 0.01, max_turnover_pct: float = 0.10):
        self.max_vix = max_vix
        self.max_error_rate = max_error_rate
        self.max_turnover_pct = max_turnover_pct

    def check_kill_switch(self, market_context: Dict[str, Any], system_metrics: Dict[str, Any]) -> bool:
        """
        Evaluates global panic / error triggers.
        Returns True if the system must be halted.
        """
        if market_context.get("vix", 0) > self.max_vix:
            return True
        if system_metrics.get("error_rate", 0) > self.max_error_rate:
            return True
        return False

    def classify_decision(self, proposed_trades: List[Dict[str, Any]], portfolio_total_value: float) -> str:
        """
        Evaluates a proposed trade list and assigns an intervention tier.
        """
        if not proposed_trades:
            return InterventionLevel.INFORMATIONAL

        total_trade_value = sum(abs(trade.get("amount", 0)) for trade in proposed_trades)
        turnover_pct = total_trade_value / portfolio_total_value if portfolio_total_value else 0.0

        if turnover_pct > self.max_turnover_pct:
            return InterventionLevel.APPROVAL_REQUIRED
        elif turnover_pct > (self.max_turnover_pct / 2):
            return InterventionLevel.ADVISORY
        
        return InterventionLevel.INFORMATIONAL
