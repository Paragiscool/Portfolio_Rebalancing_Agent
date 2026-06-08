Day 1: Project Setup And Data Architecture 
Objectives: Establish the development environment, initialise the GitHub repository, design the 
data model, and set up the portfolio simulation data pipeline. 
Tasks: 
(1) 
Create 
a 
private 
GitHub 
repository 
named 
'zetheta-[intern-id]-Project 
1D-portfolio-rebalancing-agent' with proper README.md header containing ZETHETA 
metadata fields. (2) Set up Python virtual environment with core dependencies: langchain, 
crewai, pandas, numpy, scipy, cvxpy, shap, lime, streamlit, pytest, black, ruff. (3) Design the data 
model for portfolios (50,000 simulated portfolios across 5 risk categories), securities master 
(500+ securities across equity, fixed income, alternatives), market data (12 months of daily 
prices), and client profiles (risk category, tax status, restrictions). (4) Write data generation 
scripts to create synthetic but realistic portfolio data, including correlated market returns using a 
multivariate normal distribution calibrated to historical NSE/BSE data. (5) Implement the 
configuration management system (YAML-based config for all thresholds, parameters, and 
feature flags). 
Deliverables: Initialised repository with proper structure, data model documentation, synthetic 
data generation scripts, and configuration framework. 
Checkpoint: Repository accessible, at least 50,000 synthetic portfolios generated with realistic 
allocation distributions, all tests passing.