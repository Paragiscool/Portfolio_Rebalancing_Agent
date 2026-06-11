import pytest
import pandas as pd
import numpy as np
import time
from src.engine.threshold_manager import ThresholdManager
from src.engine.drift_calculator import DriftCalculator
from src.engine.drift_monitor import DriftMonitor


class MockThresholdManager:
    def get_drift_band(self, risk_category: str) -> float:
        return 0.05

    def get_target_allocation(self, risk_category: str) -> dict:
        return {
            "Equity": 0.50,
            "Fixed Income": 0.30,
            "Alternatives": 0.10,
            "Cash": 0.10,
        }


@pytest.fixture
def sample_portfolios():
    # Create a small dataset with known drift amounts
    data = [
        # Zero drift
        {
            "portfolio_id": "P1",
            "risk_category": "Balanced",
            "equity_weight": 0.50,
            "fixed_income_weight": 0.30,
            "alternatives_weight": 0.10,
            "cash_weight": 0.10,
        },
        # Small drift (within band of 0.05)
        {
            "portfolio_id": "P2",
            "risk_category": "Balanced",
            "equity_weight": 0.52,
            "fixed_income_weight": 0.28,
            "alternatives_weight": 0.10,
            "cash_weight": 0.10,
        },
        # Extreme drift (needs rebalance)
        {
            "portfolio_id": "P3",
            "risk_category": "Balanced",
            "equity_weight": 0.60,
            "fixed_income_weight": 0.20,
            "alternatives_weight": 0.10,
            "cash_weight": 0.10,
        },
    ]
    return pd.DataFrame(data)


def test_zero_drift(sample_portfolios):
    tm = MockThresholdManager()
    dc = DriftCalculator(tm)
    analyzed = dc.calculate_drift(sample_portfolios)

    p1 = analyzed[analyzed["portfolio_id"] == "P1"].iloc[0]
    assert p1["max_abs_drift"] == 0.0
    assert not p1["needs_rebalance"]


def test_extreme_drift(sample_portfolios):
    tm = MockThresholdManager()
    dc = DriftCalculator(tm)
    dm = DriftMonitor(dc)

    queue = dm.scan_portfolios(sample_portfolios)
    # Only P3 should be in the queue
    assert len(queue) == 1
    assert queue.iloc[0]["portfolio_id"] == "P3"
    assert queue.iloc[0]["max_abs_drift"] == pytest.approx(0.10)


def test_performance():
    tm = MockThresholdManager()
    dc = DriftCalculator(tm)
    dm = DriftMonitor(dc)

    # Generate 50,000 random portfolios
    num_ports = 50000
    df = pd.DataFrame(
        {
            "portfolio_id": [f"P_{i}" for i in range(num_ports)],
            "risk_category": ["Balanced"] * num_ports,
            "equity_weight": np.random.uniform(0.40, 0.60, num_ports),
            "fixed_income_weight": np.random.uniform(0.20, 0.40, num_ports),
            "alternatives_weight": np.random.uniform(0.05, 0.15, num_ports),
            "cash_weight": np.random.uniform(0.05, 0.15, num_ports),
        }
    )

    start_time = time.time()
    queue = dm.scan_portfolios(df)
    end_time = time.time()

    execution_time = end_time - start_time
    assert (
        execution_time < 30.0
    ), f"Performance test failed! Execution took {execution_time} seconds"
