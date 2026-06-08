Day 2: Drift Monitoring Engine 
Objectives: Build the core drift calculation engine that monitors all 50,000 portfolios and 
identifies those requiring rebalancing attention. 
Tasks: (1) Implement the DriftCalculator class that computes absolute drift, sum of absolute 
drift, root mean square drift, and predicted tracking error for each portfolio. (2) Build the 
ThresholdManager that maintains risk-category-specific and client-overlay-specific thresholds. 
(3) Implement the DriftMonitor service that runs drift calculations across all portfolios and 
returns a prioritised queue of portfolios exceeding their thresholds. (4) Write unit tests for all 
drift calculation functions with edge cases: zero drift, extreme drift, missing price data, corporate 
actions affecting weights. (5) Performance optimisation: ensure the full 50,000-portfolio drift 
scan completes within 30 seconds using vectorised NumPy operations. 
Deliverables: DriftCalculator module, ThresholdManager module, DriftMonitor service, 
comprehensive test suite, performance benchmark results. 
Checkpoint: Drift engine correctly identifies portfolios exceeding thresholds across all 5 risk 
categories, with test coverage above 85%. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 37