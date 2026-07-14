import pytest
import pandas as pd
import os
from src.backtesting.backtest_engine import BacktestEngine
from src.backtesting.performance_analyser import PerformanceAnalyser
from src.backtesting.strategy_comparator import StrategyComparator

def test_backtest_engine():
    engine = BacktestEngine(initial_capital=10000.0)
    prices = pd.DataFrame({
        "AAPL": [100.0, 105.0, 110.0, 115.0],
        "GOOGL": [200.0, 190.0, 180.0, 170.0]
    }, index=pd.date_range("2023-01-01", periods=4))
    
    target = {"AAPL": 0.5, "GOOGL": 0.5}
    
    res_bnh = engine.run_backtest(prices, target, strategy="buy_and_hold")
    assert len(res_bnh) == 4
    assert res_bnh["turnover"].iloc[-1] == 0.0
    
    res_reb = engine.run_backtest(prices, target, strategy="threshold_rebalance", threshold=0.01)
    assert res_reb["turnover"].iloc[-1] > 0.0

def test_performance_analyser():
    analyser = PerformanceAnalyser()
    
    res = pd.DataFrame({
        "total_value": [10000.0, 10100.0, 10200.0, 10150.0, 10300.0],
        "turnover": [0.0, 0.0, 1000.0, 1000.0, 1000.0]
    })
    metrics = analyser.analyze(res)
    
    assert "Total Return" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Max Drawdown" in metrics
    assert round(metrics["Total Return"], 4) == 0.03
    assert metrics["Total Turnover"] == 1000.0

def test_strategy_comparator(tmp_path):
    output_dir = str(tmp_path)
    comp = StrategyComparator(output_dir)
    comp.run_comparison()
    
    assert os.path.exists(os.path.join(output_dir, "backtest_report.md"))
