import numpy as np
import pandas as pd
from typing import Dict

class PerformanceAnalyser:
    def __init__(self, risk_free_rate: float = 0.0):
        self.rf = risk_free_rate
        
    def analyze(self, results_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculates performance metrics from a backtest results DataFrame.
        """
        if results_df.empty:
            return {}
            
        values = results_df["total_value"]
        daily_returns = values.pct_change().dropna()
        
        # Annualized Return (assuming 252 trading days)
        total_return = (values.iloc[-1] / values.iloc[0]) - 1
        days = len(values)
        annualized_return = (1 + total_return) ** (252 / days) - 1 if days > 0 else 0
        
        # Annualized Volatility
        annualized_vol = daily_returns.std() * np.sqrt(252)
        
        # Sharpe Ratio
        if annualized_vol > 0:
            sharpe_ratio = (annualized_return - self.rf) / annualized_vol
        else:
            sharpe_ratio = 0.0
            
        # Maximum Drawdown
        rolling_max = values.cummax()
        drawdowns = (values - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # Turnover (Total traded value over period)
        total_turnover = results_df["turnover"].iloc[-1] if "turnover" in results_df.columns else 0.0
        
        return {
            "Total Return": total_return,
            "Annualized Return": annualized_return,
            "Annualized Vol": annualized_vol,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Total Turnover": total_turnover
        }
