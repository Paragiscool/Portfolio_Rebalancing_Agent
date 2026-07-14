# Strategy Backtest Comparison

This report compares the autonomous Threshold-based Rebalancing Agent against a simple Buy & Hold strategy over a 1-year synthetic market simulation.

| Metric | Buy & Hold | Agent (Rebalanced) |
|---|---|---|
| Total Return | 31.18% | 32.57% |
| Annualized Return | 31.18% | 32.57% |
| Annualized Vol | 15.08% | 15.22% |
| Sharpe Ratio | 2.07 | 2.14 |
| Max Drawdown | -16.14% | -15.58% |
| Total Turnover | $0.00 | $23,674.08 |

## Conclusion
The Agent successfully executed rebalancing trades to maintain target drift constraints.