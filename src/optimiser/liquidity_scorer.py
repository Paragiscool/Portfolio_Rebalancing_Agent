import numpy as np

class LiquidityScorer:
    """Scores liquidity and assigns execution strategies based on average daily volume."""
    
    def __init__(self, max_adv_participation_rate: float = 0.05, illiquid_schedule_threshold: float = 0.10):
        self.max_adv_participation_rate = max_adv_participation_rate
        self.illiquid_schedule_threshold = illiquid_schedule_threshold
        
    def score_liquidity(self, adv_30d: float, bid_ask_spread_pct: float) -> float:
        """
        Returns a liquidity score between 0 (illiquid) and 1 (highly liquid).
        Simple heuristic: higher volume and tighter spread = higher score.
        """
        adv_score = min(adv_30d / 1_000_000.0, 1.0)
        spread_score = max(0.0, 1.0 - (bid_ask_spread_pct / 0.05))
        
        return 0.7 * adv_score + 0.3 * spread_score
        
    def get_execution_strategy(self, trade_shares: float, adv_30d: float) -> dict:
        """
        Determine if the trade needs multi-day slicing and which algorithm to use.
        """
        participation_rate = abs(trade_shares) / adv_30d if adv_30d > 0 else float('inf')
        
        if participation_rate <= self.max_adv_participation_rate:
            return {
                "strategy": "MOC", # Market on Close
                "days": 1,
                "daily_shares": [trade_shares]
            }
            
        elif participation_rate <= self.illiquid_schedule_threshold:
            # Slice it to respect max participation
            days_needed = int(np.ceil(participation_rate / self.max_adv_participation_rate))
            daily_trade = trade_shares / days_needed
            return {
                "strategy": "VWAP",
                "days": days_needed,
                "daily_shares": [daily_trade] * days_needed
            }
        else:
            # Highly illiquid or massive trade requires more conservative TWAP scheduling
            days_needed = int(np.ceil(participation_rate / self.max_adv_participation_rate))
            daily_trade = trade_shares / days_needed
            return {
                "strategy": "TWAP",
                "days": days_needed,
                "daily_shares": [daily_trade] * days_needed
            }
