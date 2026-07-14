import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class BacktestEngine:
    def __init__(self, initial_capital: float = 100000.0, transaction_cost_bps: float = 10.0):
        self.initial_capital = initial_capital
        self.transaction_cost_rate = transaction_cost_bps / 10000.0
        
    def generate_synthetic_prices(self, tickers: List[str], days: int = 252, mu: float = 0.08, sigma: float = 0.20) -> pd.DataFrame:
        """
        Generates synthetic Geometric Brownian Motion (GBM) prices for backtesting.
        """
        dt = 1 / 252
        prices = {}
        for ticker in tickers:
            returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=days))
            price_path = 100.0 * np.cumprod(np.insert(returns, 0, 1.0))[:-1]
            prices[ticker] = price_path
            
        dates = pd.date_range(start="2023-01-01", periods=days, freq="B")
        return pd.DataFrame(prices, index=dates)

    def run_backtest(self, prices_df: pd.DataFrame, target_weights: Dict[str, float], strategy: str = "buy_and_hold", threshold: float = 0.05) -> pd.DataFrame:
        """
        Runs a backtest of a strategy.
        strategy: 'buy_and_hold' or 'threshold_rebalance'
        Returns a DataFrame with portfolio value over time.
        """
        days = len(prices_df)
        tickers = list(target_weights.keys())
        
        # Initialize
        cash = 0.0
        shares = {t: 0.0 for t in tickers}
        
        # Day 0: Initial Allocation
        for t in tickers:
            alloc = self.initial_capital * target_weights[t]
            shares_bought = alloc / prices_df.iloc[0][t]
            shares[t] = shares_bought
            
        portfolio_values = []
        turnover = 0.0
        
        for i in range(days):
            current_prices = prices_df.iloc[i]
            
            # Calculate current weights
            holdings_value = {t: shares[t] * current_prices[t] for t in tickers}
            total_value = sum(holdings_value.values()) + cash
            current_weights = {t: holdings_value[t] / total_value for t in tickers}
            
            # Check rebalance logic
            rebalance_needed = False
            if strategy == "threshold_rebalance":
                for t in tickers:
                    if abs(current_weights[t] - target_weights[t]) > threshold:
                        rebalance_needed = True
                        break
                        
            if rebalance_needed:
                for t in tickers:
                    target_alloc = total_value * target_weights[t]
                    current_alloc = holdings_value[t]
                    diff = target_alloc - current_alloc
                    
                    if abs(diff) > 1.0: # Minimum trade size
                        shares_to_trade = diff / current_prices[t]
                        shares[t] += shares_to_trade
                        cost = abs(diff) * self.transaction_cost_rate
                        cash -= cost
                        turnover += abs(diff)
                        
                # Recalculate total value after costs
                holdings_value = {t: shares[t] * current_prices[t] for t in tickers}
                total_value = sum(holdings_value.values()) + cash

            portfolio_values.append({
                "date": prices_df.index[i],
                "total_value": total_value,
                "turnover": turnover
            })
            
        df_results = pd.DataFrame(portfolio_values).set_index("date")
        return df_results
