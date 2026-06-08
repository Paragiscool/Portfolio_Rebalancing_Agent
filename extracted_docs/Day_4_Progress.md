Day 4: Trade Generation Optimiser - Core 
Objectives: Build the constrained optimisation engine that generates executable trade lists from 
rebalancing decisions. 
Tasks: (1) Implement the PortfolioOptimiser class using CVXPY for constrained quadratic 
programming. The objective function minimises tracking error (post-rebalance allocation vs 
target allocation) subject to: transaction cost budget, turnover limit, long-only constraint, sector 
concentration limits, single-issuer limits, and minimum trade size. (2) Implement the 
TradeListGenerator that converts optimiser output (target weights) into security-level trades with 
round-lot handling. (3) Build the CostEstimator module that estimates explicit costs (brokerage, 
STT, stamp duty, GST) and implicit costs (market impact using the square-root model). (4) 
Implement the ConstraintManager that maintains the full constraint set and provides constraint 
violation reports. (5) Write unit tests for optimiser accuracy and constraint satisfaction. 
Deliverables: PortfolioOptimiser module, TradeListGenerator module, CostEstimator module, 
ConstraintManager module, optimiser test suite. 
Checkpoint: Optimiser generates valid, constraint-satisfying trade lists for portfolios across all 5 
risk categories with verifiable cost estimates. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 38