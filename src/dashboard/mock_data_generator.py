import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_portfolio_overview_data():
    """Generates a mock dataframe for portfolio drift heatmap."""
    np.random.seed(42)
    categories = ["Conservative", "Moderate", "Aggressive"]
    asset_classes = ["Equities", "Fixed Income", "Real Estate", "Commodities"]
    
    data = []
    for cat in categories:
        for ac in asset_classes:
            data.append({
                "Risk Category": cat,
                "Asset Class": ac,
                "Avg Drift (%)": np.random.uniform(-5.0, 5.0)
            })
    return pd.DataFrame(data)

def get_rebalancing_activity_data():
    """Generates a mock dataframe for recent AI decisions."""
    now = datetime.now()
    data = []
    for i in range(1, 11):
        status = np.random.choice(["Completed", "Pending Approval", "Halted"])
        data.append({
            "Client ID": f"client_{i*123}",
            "Date": (now - timedelta(days=i)).strftime("%Y-%m-%d"),
            "Turnover (%)": round(np.random.uniform(1.0, 15.0), 2),
            "Status": status,
            "Intervention Level": "APPROVAL_REQUIRED" if status == "Pending Approval" else "INFORMATIONAL"
        })
    return pd.DataFrame(data)

def get_performance_backtest_data():
    """Generates a mock equity curve comparing Agent vs Buy & Hold."""
    dates = pd.date_range("2023-01-01", periods=100)
    bnh = np.cumprod(1 + np.random.normal(0.0005, 0.01, size=100)) * 10000
    agent = np.cumprod(1 + np.random.normal(0.0007, 0.009, size=100)) * 10000
    
    return pd.DataFrame({
        "Date": dates,
        "Buy & Hold": bnh,
        "Agent": agent
    }).set_index("Date")

def get_system_health_data():
    """Generates system health metrics."""
    return {
        "Uptime": "99.98%",
        "Error Rate": "0.02%",
        "API Latency": "45ms",
        "Active Agents": 3
    }
