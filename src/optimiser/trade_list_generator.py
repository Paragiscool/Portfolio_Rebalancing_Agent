import numpy as np
import pandas as pd
from typing import List, Dict, Any


class TradeListGenerator:
    """Converts continuous optimized weights into discrete execution trades."""

    def __init__(self, constraint_manager):
        self.constraint_manager = constraint_manager

    def generate_trades(
        self,
        current_weights: np.ndarray,
        optimized_weights: np.ndarray,
        portfolio_value: float,
        current_prices: np.ndarray,
        tickers: List[str],
    ) -> pd.DataFrame:
        """
        Generate a list of actionable trades, handling round lots and minimum trade sizes.
        """
        # Calculate target dollar values
        target_values = optimized_weights * portfolio_value
        current_values = current_weights * portfolio_value

        # Calculate discrete target shares (round to nearest whole share)
        # In reality, round lots might be > 1, assuming 1 for now
        target_shares = np.round(target_values / current_prices)
        current_shares = np.round(current_values / current_prices)

        # Trade shares = Target - Current
        trade_shares = target_shares - current_shares

        trades = []
        min_trade_size = self.constraint_manager.get_min_trade_size()

        for i, ticker in enumerate(tickers):
            shares = trade_shares[i]
            if shares == 0:
                continue

            trade_value = shares * current_prices[i]

            # Apply minimum trade size heuristic (filter out "dust" trades)
            if abs(trade_value) >= min_trade_size:
                trades.append(
                    {
                        "ticker": ticker,
                        "action": "BUY" if shares > 0 else "SELL",
                        "shares": abs(shares),
                        "price": current_prices[i],
                        "trade_value": abs(trade_value),
                    }
                )

        return pd.DataFrame(trades)
