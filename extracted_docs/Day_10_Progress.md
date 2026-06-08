Day 10: Backtesting Framework 
Objectives: Build the backtesting infrastructure to evaluate agent performance against the legacy 
system and alternative strategies. 
Tasks: (1) Implement the BacktestEngine that replays historical market data (12 months of 
synthetic data calibrated to actual market conditions) through the rebalancing agent, simulating 
portfolio evolution, trade execution, and cost accrual. (2) Build the PerformanceAnalyser that 
computes: annualised return, volatility, Sharpe ratio, maximum drawdown, tracking error, 
turnover, transaction costs, tax efficiency, and rebalancing frequency for both the agent and the 
legacy system. (3) Implement the StrategyComparator that runs parallel backtests of: the new 
agent, the legacy quarterly calendar-based system, a threshold-only system, and a buy-and-hold 
benchmark. (4) Generate comparative performance reports with statistical significance testing 
(paired t-test or bootstrap confidence intervals). (5) Implement the ScenarioRunner that tests 
agent behaviour under extreme scenarios: 2008-like crash, 2020-like V-recovery, 2022-like rate 
shock, and a custom scenario combining equity crash with credit spread widening. 
Deliverables: BacktestEngine, PerformanceAnalyser, StrategyComparator, ScenarioRunner, 
comparative performance report. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 41 


 
 
 
 
 
Checkpoint: Backtest demonstrates measurable improvement over legacy system on at least 4 of 
6 key metrics (Sharpe, drawdown, tracking error, turnover, cost, tax efficiency).