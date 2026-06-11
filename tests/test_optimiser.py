import pytest
import numpy as np
import pandas as pd
from src.optimiser.cost_estimator import CostEstimator
from src.optimiser.constraint_manager import ConstraintManager
from src.optimiser.portfolio_optimiser import PortfolioOptimiser
from src.optimiser.trade_list_generator import TradeListGenerator


class MockConstraintManager:
    def get_max_turnover(self):
        return 0.20

    def get_min_trade_size(self):
        return 1000


def test_cost_estimator():
    ce = CostEstimator()
    # Mocking config
    ce.brokerage_bps = 5
    ce.stt_bps = 10
    ce.market_impact_coeff = 0.1

    trade_val = 100000.0
    explicit = ce.estimate_explicit_costs(trade_val)
    # 15 bps of 100k = 0.0015 * 100000 = 150
    assert explicit == pytest.approx(150.0)

    implicit = ce.estimate_implicit_costs(trade_val, adv=1000000.0, volatility=0.02)
    # sqrt(0.1) * 0.1 * 0.02 * 100000
    # sqrt(0.1) ~ 0.316227
    # impact_fraction = 0.1 * 0.02 * 0.316227 = 0.00063245
    # implicit = 100000 * 0.00063245 = 63.245
    assert implicit > 0


def test_portfolio_optimiser():
    cm = MockConstraintManager()
    po = PortfolioOptimiser(cm)

    # 4 assets
    current_weights = np.array([0.5, 0.5, 0.0, 0.0])
    target_weights = np.array([0.25, 0.25, 0.25, 0.25])

    # Dummy covariance matrix (identity)
    cov = np.eye(4)

    optimized = po.optimize(current_weights, target_weights, cov)

    # Check sum is 1
    assert np.sum(optimized) == pytest.approx(1.0)

    # Check long only
    assert np.all(optimized >= -1e-6)

    # Check turnover limit
    # Turnover from [0.5, 0.5, 0, 0] to [0.25, 0.25, 0.25, 0.25] is exactly 0.25+0.25 = 0.5 for one side, sum(abs)/2 = 0.5
    # But limit is 0.20. So it should not reach target perfectly!
    turnover = 0.5 * np.sum(np.abs(optimized - current_weights))
    assert turnover <= 0.20 + 1e-4


def test_trade_list_generator():
    cm = MockConstraintManager()
    tlg = TradeListGenerator(cm)

    current_w = np.array([0.5, 0.5])
    target_w = np.array([0.6, 0.4])
    port_val = 100000.0
    prices = np.array([100.0, 50.0])
    tickers = ["AAPL", "MSFT"]

    # Target values: AAPL=60k, MSFT=40k
    # Current values: AAPL=50k, MSFT=50k
    # Target shares: AAPL=600, MSFT=800
    # Current shares: AAPL=500, MSFT=1000
    # Expected trades: BUY 100 AAPL, SELL 200 MSFT

    trades = tlg.generate_trades(current_w, target_w, port_val, prices, tickers)

    assert len(trades) == 2
    aapl_trade = trades[trades["ticker"] == "AAPL"].iloc[0]
    assert aapl_trade["action"] == "BUY"
    assert aapl_trade["shares"] == 100
    assert aapl_trade["trade_value"] == 10000.0

    msft_trade = trades[trades["ticker"] == "MSFT"].iloc[0]
    assert msft_trade["action"] == "SELL"
    assert msft_trade["shares"] == 200
    assert msft_trade["trade_value"] == 10000.0
