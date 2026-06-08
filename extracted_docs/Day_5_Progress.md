Day 5: Trade Generation Optimiser - Tax And Liquidity 
Objectives: Extend the trade generation engine with tax-aware execution and liquidity constraint 
handling. 
Tasks: (1) Implement the TaxLotManager that tracks cost basis, acquisition date, and holding 
period for every position in every portfolio. (2) Build the TaxOptimiser that selects optimal tax 
lots for sale: prioritising long-term lots (lower tax rate), identifying tax-loss harvesting 
opportunities, implementing wash-sale avoidance logic, and calculating the net after-tax cost of 
each trade. (3) Implement the LiquidityScorer that assigns liquidity scores to each security based 
on average daily volume, bid-ask spread, and historical market impact. (4) Extend the 
PortfolioOptimiser with liquidity constraints: maximum trade size as a percentage of average 
daily volume, multi-day execution scheduling for illiquid positions, and VWAP/TWAP execution 
strategy assignment. (5) Build the TaxHarvestingScanner that proactively identifies portfolios 
with harvestable losses and proposes tax-efficient substitute trades. 
Deliverables: 
TaxLotManager, 
TaxOptimiser, 
LiquidityScorer 
modules, 
extended 
PortfolioOptimiser, TaxHarvestingScanner. 
Checkpoint: Tax-optimised trade lists demonstrating measurable tax savings compared to naive 
FIFO execution, liquidity constraints respected.