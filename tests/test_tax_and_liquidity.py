import pytest
from datetime import date, timedelta
import numpy as np
from src.data.models import TaxLot
from src.optimiser.tax_lot_manager import TaxLotManager
from src.optimiser.tax_optimiser import TaxOptimiser
from src.optimiser.liquidity_scorer import LiquidityScorer
from src.optimiser.portfolio_optimiser import PortfolioOptimiser
from src.optimiser.constraint_manager import ConstraintManager

def test_partial_lot_split():
    # Setup
    manager = TaxLotManager()
    today = date.today()
    
    # Lot A: 100 shares, Cost Basis $150 (Higher cost basis, should be HIFO'd first)
    lot_a = TaxLot(security_ticker="AAPL", shares=100, cost_basis=150.0, acquisition_date=today - timedelta(days=400))
    # Lot B: 100 shares, Cost Basis $100
    lot_b = TaxLot(security_ticker="AAPL", shares=100, cost_basis=100.0, acquisition_date=today - timedelta(days=100))
    
    manager.add_lot("PORT_001", "AAPL", lot_a)
    manager.add_lot("PORT_001", "AAPL", lot_b)
    
    # Action: Sell 150 shares
    sold_lots = manager.allocate_sell_hifo("PORT_001", "AAPL", 150)
    
    # Assert
    assert len(sold_lots) == 2
    # Lot A should be exhausted completely (100 shares)
    assert sold_lots[0][0].cost_basis == 150.0
    assert sold_lots[0][1] == 100
    
    # Lot B should be partially consumed (50 shares)
    assert sold_lots[1][0].cost_basis == 100.0
    assert sold_lots[1][1] == 50
    
    # Check remaining inventory in manager
    remaining_lots = manager.get_lots("PORT_001", "AAPL")
    assert remaining_lots[0].shares == 0
    assert remaining_lots[1].shares == 50

def test_wash_sale_block():
    manager = TaxLotManager()
    tax_opt = TaxOptimiser(tax_lot_manager=manager, wash_sale_window_days=30)
    today = date.today()
    
    # Simulate a realized loss 15 days ago
    loss_date = today - timedelta(days=15)
    tax_opt.record_realized_loss("PORT_001", "TSLA", loss_date)
    
    # Proposed trades: buying TSLA (100 shares), buying AAPL (50 shares)
    proposed_trades = {
        "TSLA": 100,
        "AAPL": 50,
        "MSFT": -200 # Selling is allowed
    }
    
    blocked_tickers = tax_opt.block_pending_target_buys("PORT_001", proposed_trades, today)
    
    # Only TSLA should be blocked because of the recent loss
    assert "TSLA" in blocked_tickers
    assert "AAPL" not in blocked_tickers
    assert "MSFT" not in blocked_tickers

def test_liquidity_cap_and_slicing():
    # 1. Test CVXPY Cap
    cm = ConstraintManager()
    cm.max_adv_participation = 0.05 # 5% limit
    # Need to override turnover limit so it doesn't artificially bound the test
    cm.max_turnover = 1.0 
    
    opt = PortfolioOptimiser(constraint_manager=cm)
    
    # 2 assets. Asset 0 is highly liquid, Asset 1 is illiquid.
    current_weights = np.array([0.5, 0.5])
    target_weights = np.array([0.2, 0.8]) # Wants to buy 0.3 of Asset 1
    cov_matrix = np.eye(2) * 0.01
    
    # Total portfolio value $1,000,000. 
    # Wants to buy $300,000 of Asset 1.
    # Price = $10. So wants to buy 30,000 shares.
    # ADV of Asset 1 = 200,000.
    # 5% of ADV = 10,000 shares max per day = $100,000 = 0.1 weight change max.
    
    market_data = {
        "prices": np.array([100.0, 10.0]),
        "adv": np.array([1000000.0, 200000.0])
    }
    
    optimized_weights = opt.optimize(
        current_weights=current_weights,
        target_weights=target_weights,
        covariance_matrix=cov_matrix,
        market_data=market_data,
        total_portfolio_value=1_000_000.0
    )
    
    # Check that Asset 1 weight didn't exceed current + max_change
    # Current = 0.5. Max change = 0.1. So max optimized weight = 0.6.
    assert np.isclose(optimized_weights[1], 0.6, atol=1e-4)
    
    # 2. Test Slicing algorithm
    scorer = LiquidityScorer(max_adv_participation_rate=0.05, illiquid_schedule_threshold=0.10)
    
    # We want to buy 50,000 shares, ADV is 200,000
    # Participation rate = 50,000 / 200,000 = 25% (0.25)
    # This exceeds illiquid_schedule_threshold (10%), so it should trigger TWAP
    strategy = scorer.get_execution_strategy(trade_shares=50000, adv_30d=200000)
    
    assert strategy["strategy"] == "TWAP"
    # days needed = ceil(0.25 / 0.05) = 5 days
    assert strategy["days"] == 5
    assert len(strategy["daily_shares"]) == 5
    assert np.isclose(sum(strategy["daily_shares"]), 50000)
    assert np.isclose(strategy["daily_shares"][0], 10000)
