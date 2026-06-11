# Autonomous Portfolio Rebalancing Agent - Architecture and Progress Report

## 1. Architecture Overview
This system replaces legacy rule-based engines with a multi-agent AI architecture built using LangChain and CrewAI.
The system is designed to autonomously manage portfolio drift across 50,000 heterogeneous client portfolios.
Key components include:
- Orchestrator Agent: Central router managing task delegation and flow.
- Portfolio Analyst Agent: Analyzes current allocations and calculates drift.
- Risk Assessment Agent: Ensures allocations remain within defined risk parameters.
- Tax Optimisation Agent: Handles tax-loss harvesting and tax-aware routing.
- Explanation Generation Agent: Uses SHAP and LIME to generate human-readable explanations.

These agents coordinate via a shared event bus. Decisions are explainable using SHAP and LIME, serving multiple audience levels (Client, Advisor, Compliance).

## Executive Summary

 
 
 
 
 
AGENTIC AI - AUTONOMOUS PORTFOLIO 
REBALANCING AGENT WITH EXPLAINABLE 
DECISIONS 
Category: Portfolio Rebalancing | Agentic AI Engineer 
Timeline: 15 Days | AI-Accelerated Innovation & Research Project  
Target: Undergraduate / MBA / Engineering Students  
 
TASK: 
Design and build a fully autonomous, multi-agent portfolio rebalancing system that replaces a 
rule-based legacy system at a fictional robo-advisory firm - WealthPilot AI - which manages INR 
25,000 crores across 50,000 client portfolios spanning five risk categories. The agent must monitor 
portfolio drift in near-real-time, intelligently evaluate rebalancing triggers (threshold-based, 
calendar-based, and event-driven), generate constraint-aware trade lists optimised for after-tax 
returns, produce human-readable explanations at three audience levels (client, advisor, and 
compliance), support human override with full audit trails, and demonstrate measurable 
improvement over the legacy system through backtesting 
 
PART A: TRAINING MATERIAL & LEARNING RESOURCES 
PART B: GAMIFIED SIMULATION BUSINESS CONCEPT 
PART C: CASE STUDIES & REAL-WORLD APPLICATIONS 
PART D: 15-DAY PROJECT METHODOLOGY & DELIVERABLES 
PART E: NO-CODE TOOLS & PLATFORMS GUIDE 
PART F: SUBMISSION PROTOCOL 
 
Important Note: 
This Project is designed, developed, and administered solely by Zetheta Algorithms Private Limited 
("Zetheta") for the purpose of assessing candidates, students, or event participants on behalf of engaging 
employers, institutes, or event organisers. Completion of this Project does not guarantee employment, 
academic outcomes, awards, or any other result - all such decisions remain at the sole discretion of the 
respective engaging party. Zetheta may use AI-assisted tools to evaluate submissions; such outputs are 
indicative in nature and may be inaccurate or incomplete. By participating, you consent to your 
performance data, scores, and submissions being shared with relevant engaging parties for assessment and 
decision-making purposes. 
 
 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 1 


 
 
 
 
 
EXECUTIVE SUMMARY 
This project positions students as AI Agent Leads at a fictional next-generation robo-advisory 
firm - WealthPilot AI - requiring them to master the convergence of quantitative portfolio 
management, multi-agent AI orchestration, and explainable AI design. Unlike traditional data 
science projects that operate within a single domain, this project demands simultaneous fluency 
in Modern Portfolio Theory, constraint optimisation, and tax-aware trade execution on one side, 
and agentic AI frameworks, SHAP/LIME feature attribution, and SEBI regulatory compliance on 
the other. 
The core challenge students must solve: How can an AI system autonomously manage portfolio 
drift across 50,000 heterogeneous client portfolios - each with unique risk tolerances, tax 
positions, and liquidity constraints - while generating decisions that are not just mathematically 
optimal but also fully explainable to clients, advisors, and compliance teams? The answer lies in 
a purpose-built multi-agent architecture built using LangChain and CrewAI, where specialist 
agents - an Orchestrator, a Portfolio Analyst, a Risk Assessment Agent, a Tax Optimisation 
Agent, and an Explanation Generation Agent - coordinate through a shared event bus to deliver 
intelligent, context-aware rebalancing recommendations at scale. 
Students will build a complete Autonomous Portfolio Rebalancing Agent validated across 
real-world market scenarios including the March 2020 COVID crash, calibrated against industry 
benchmarks from Wealthfront, Betterment, Vanguard, and BlackRock's Aladdin platform, and 
backtested against historical Indian and global market data. The agent must achieve measurable 
improvements over the legacy calendar-based system across cost efficiency, drift management, 
tax savings, and client communication quality - with every decision logged in a full compliance 
audit trail. 
The global robo-advisory market is projected to exceed $2.5 trillion in assets under management 
by 2027, while the wealth management industry spends an estimated $15+ billion annually on 
manual portfolio rebalancing operations that are slow, inconsistent, and unable to scale 
personalisation at the individual client level. Yet the vast majority of automated rebalancing 
systems remain rule-based and opaque, incapable of adapting to market regimes, client life 
events, or tax circumstances in real time. This project closes this intelligence gap - equipping 
students to build the next generation of explainable, autonomous wealth management 
infrastructure directly applicable to robo-advisors, asset managers, and fintech platforms 
operating across Indian and global markets. 
 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 2 




## 2. What We Have Done

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

Day 3: Trigger Evaluation System 
Objectives: Implement the three-tier trigger taxonomy (threshold, calendar, event-driven) and 
the trigger consolidation logic. 
Tasks: (1) Implement the TriggerEvaluator base class with subclasses: ThresholdTrigger, 
CalendarTrigger, EventTrigger. (2) Build the ThresholdTrigger evaluator that classifies drift 
breaches into Critical, High, Medium severity based on magnitude and trend. (3) Build the 
CalendarTrigger evaluator that manages monthly, quarterly, and annual review schedules with 
business-day-aware date handling. (4) Build the EventTrigger evaluator with event detection 
logic for market crashes (configurable index decline thresholds), regulatory changes (manual 
input with affected portfolio identification), client life events (API endpoint for advisor input), 
and tax harvesting windows (date-range-based activation). (5) Implement trigger consolidation 
logic: when multiple triggers fire for the same portfolio, merge them into a single rebalancing 
event with the highest priority and a combined audit record. (6) Write integration tests simulating 
multi-trigger scenarios. 
Deliverables: Trigger evaluation framework, all trigger type implementations, consolidation 
logic, integration test suite. 
Checkpoint: Trigger system correctly classifies and prioritises at least 10 test scenarios covering 
all trigger types and combinations.

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

## 3. What We Will Do

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

Day 6: Explanation Generation System 
Objectives: Build the three-tier explanation generation framework using LangChain and 
structured templates. 
Tasks: (1) Design explanation templates for each audience level (client, advisor, compliance) 
and each trigger type (threshold, calendar, event), yielding a matrix of 9+ distinct templates. (2) 
Implement the ExplanationGenerator class that takes decision metadata as input, selects the 
appropriate template, and uses an LLM (via LangChain) to generate contextualised 
natural-language explanations. (3) Build the ClientExplanationGenerator with: plain-language 
narrative, goal-relevance framing, cost transparency, and Flesch-Kincaid readability scoring 
(target: Grade 8). (4) Build the AdvisorExplanationGenerator with: quantitative metrics, 
allocation change tables, alternative strategy discussion, and override invitation. (5) Build the 
ComplianceExplanationGenerator with: full audit trail, SHAP feature attributions, constraint 
satisfaction matrix, counterfactual analysis, and regulatory rule references. (6) Implement quality 
assurance checks: numerical consistency (explanation numbers match decision data), 
completeness (all required sections present), and readability verification. 
Deliverables: ExplanationGenerator framework, 3 audience-level generators, template library, 
QA pipeline, sample explanations for all trigger types. 
Checkpoint: Generated explanations pass all QA checks, readability appropriate for each 
audience, sample explanations reviewed and approved. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 39

Day 7: SHAP/LIME Integration For Explainability 
Objectives: Integrate SHAP and LIME to provide model-level explainability for rebalancing 
decisions. 
Tasks: (1) Train a gradient boosted decision tree (XGBoost/LightGBM) as a surrogate model 
that predicts rebalancing probability given input features (drift magnitude, VIX, days since last 
rebalance, client risk score, tax lot maturity, sector concentration). (2) Implement SHAP 
integration: compute Tree SHAP values for the surrogate model, generate waterfall plots for 
individual decisions, summary plots for aggregate feature importance, and dependency plots for 
key feature interactions. (3) Implement LIME integration: generate local explanations for 
individual rebalancing decisions showing the top 5 contributing features with direction and 
magnitude. (4) Implement counterfactual explanation generation: for each decision, find the 
minimal feature perturbation that would change the decision, and express this in natural language 
('If equity drift were below 3.2% instead of 4.7%, the agent would not have triggered a 
rebalance'). (5) Integrate SHAP/LIME outputs into the Compliance-level explanation template. 
(6) Write tests verifying SHAP value consistency and LIME fidelity. 
Deliverables: Surrogate model training pipeline, SHAP integration module, LIME integration 
module, counterfactual generator, integrated compliance explanations. 
Checkpoint: SHAP waterfall plots correctly attribute decision to input features, LIME 
explanations faithful to surrogate model, counterfactuals logically correct.

Day 8: Mid-Sprint Review And Multi-Agent Orchestration 
Objectives: Conduct mid-sprint review, integrate all components into the multi-agent 
framework, and demonstrate end-to-end workflow. 
Tasks: (1) Mid-sprint review: present progress to date, demonstrate each component 
individually, identify gaps and risks for the remaining 7 days. (2) Implement the multi-agent 
orchestration using CrewAI: define agent roles (Orchestrator, Portfolio Analyst, Risk Manager, 
Tax Specialist, Compliance Officer, Explanation Writer), configure agent backstories and goals, 
define task dependencies, and set up the sequential/hierarchical process flow. (3) Build the 
end-to-end pipeline: Monitoring triggers a portfolio, Trigger Evaluator classifies it, Orchestrator 
assigns it to the Crew, agents collaborate to produce trade list + explanations, output is stored and 
logged. (4) Test the full pipeline with a single portfolio going through a threshold-triggered 
rebalance. (5) Identify and resolve integration issues between components. 
Deliverables: Mid-sprint review presentation, multi-agent orchestration implementation, 
end-to-end pipeline demonstration, integration test results. 
Checkpoint: Full pipeline executes for a single portfolio: from drift detection through trade 
generation through explanation production, with all agents contributing. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 40

Day 9: Override And Human-In-The-Loop System 
Objectives: Implement the graduated intervention model and override capture system. 
Tasks: (1) Implement the InterventionClassifier that assigns each rebalancing decision to an 
intervention level (Informational, Advisory, Approval Required, Escalation) based on trade 
impact and decision confidence. (2) Build the OverrideCapture module: API endpoint for 
advisors to submit overrides, structured override form (original recommendation, modified 
recommendation, reason category, free-text explanation), timestamp and identity logging. (3) 
Implement the EscalationManager that generates briefing documents for edge cases requiring 
human judgment, including: situation summary, agent's analysis, options considered, 
recommended action, and specific questions for the human. (4) Build the OverrideFeedback 
loop: track outcomes of overridden decisions, compare against what would have happened 
without the override, and generate quarterly override quality reports. (5) Implement the 
kill-switch mechanism: a manual or automated circuit-breaker that halts all autonomous 
rebalancing activity, with configurable activation criteria (e.g., VIX exceeds 40, system error rate 
exceeds 1%). 
Deliverables: 
InterventionClassifier, 
OverrideCapture 
API, 
EscalationManager, 
OverrideFeedback tracker, kill-switch mechanism. 
Checkpoint: Override system correctly classifies 20 test scenarios, captures overrides with full 
audit trail, kill-switch activates and deactivates correctly.

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

Day 11: Performance Dashboard 
Objectives: Build the Streamlit-based agent performance evaluation dashboard with real-time 
monitoring and historical analytics. 
Tasks: (1) Design dashboard layout with 5 main views: Portfolio Overview (aggregate drift 
heatmap across 50,000 portfolios), Rebalancing Activity (recent decisions, pending approvals, 
execution status), Performance Analytics (backtest results, rolling metrics, strategy comparison), 
Explainability Centre (browse and search generated explanations), and System Health (agent 
uptime, error rates, processing latency). (2) Implement the Portfolio Overview page: heatmap 
showing drift by risk category and asset class, drill-down to individual portfolio detail, and 
real-time drift trend charts. (3) Implement the Rebalancing Activity page: decision log with 
filtering and sorting, pending approval queue for advisors, and execution status tracker. (4) 
Implement the Performance Analytics page: rolling 1/3/6/12 month performance metrics, 
strategy comparison charts (agent vs legacy vs benchmarks), and factor attribution analysis. (5) 
Implement the Explainability Centre: browse explanations by portfolio, date, and trigger type; 
display SHAP plots inline; and provide explanation quality metrics. 
Deliverables: Streamlit dashboard with all 5 views, interactive visualisations, drill-down 
capabilities, and responsive layout. 
Checkpoint: Dashboard displays real data from the backtest, all 5 views functional, drill-down 
from aggregate to individual portfolio working.

Day 12: Compliance Audit And Regulatory Reporting 
Objectives: Build the compliance audit module and regulatory reporting system. 
Tasks: (1) Implement the ComplianceAuditor that performs automated quarterly audits: sample 
100 decisions (stratified by trigger type and risk category), evaluate explanation quality using 
automated metrics (accuracy, completeness, readability), check for systematic biases 
(over/under-rebalancing by risk category, systematic cost under/over-estimation), and generate 
the Audit Report. (2) Build the RegulatoryReporter that generates SEBI-compliant reports: 
complete transaction history with decision rationale, suitability assessment documentation for 
each recommendation, algorithmic trading audit trail, and exception reports (any compliance 
check failures or overrides). (3) Implement the BiasDetector that analyses agent decisions for 
systematic patterns: does the agent rebalance Conservative portfolios more frequently than 
justified? Does it systematically favour certain securities? Does it exhibit momentum or 
contrarian bias? (4) Build the ExplainabilityScorecard that rates each explanation on: accuracy 
(numbers match), completeness (all sections present), readability (grade level appropriate), 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 42 


 
 
 
 
 
actionability (client can understand what to do), and regulatory sufficiency (meets audit 
requirements). 
Deliverables: 
ComplianceAuditor 
module, 
RegulatoryReporter, 
BiasDetector, 
ExplainabilityScorecard, sample audit report. 
Checkpoint: Automated audit of 100 sample decisions completed, bias analysis report 
generated, all regulatory reports exportable.

Day 13: Integration Testing And Scenario Simulation 
Objectives: Execute comprehensive integration testing across all 5 market scenarios and validate 
end-to-end system behaviour. 
Tasks: (1) Run Scenario 1 (Normal Drift): process 50,000 portfolios through a 3-month equity 
rally, verify appropriate threshold-based rebalancing, validate cost efficiency. (2) Run Scenario 2 
(Market Crash): simulate a 22% equity correction, verify crisis response (prioritisation, batch 
processing, crisis communication), measure system performance under load. (3) Run Scenario 3 
(Sector Rotation): test intra-equity rebalancing when sector concentrations breach limits without 
overall allocation drift. (4) Run Scenario 4 (Regulatory Event): simulate a new SEBI circular, 
verify affected portfolio identification, trade list compliance, and regulatory-driven explanations. 
(5) Run Scenario 5 (Tax Harvesting): execute March FY-end tax-loss harvesting scan, verify tax 
savings quantification, substitute security logic, and wash-sale avoidance. (6) Document results, 
identify edge cases, and resolve any remaining bugs. 
Deliverables: Scenario test results for all 5 scenarios, edge case documentation, bug fixes, 
integration test report. 
Checkpoint: All 5 scenarios execute successfully, agent behaviour matches expected outcomes, 
no critical bugs remaining.

Day 14: Documentation, Code Quality And Repository Preparation 
Objectives: Complete all documentation, achieve code quality standards, and prepare the 
repository for submission. 
Tasks: (1) Write comprehensive README.md: project overview, architecture diagram 
(Mermaid), installation instructions, usage guide, API documentation, configuration reference, 
and contribution guidelines. (2) Generate API documentation using Sphinx or MkDocs with code 
examples for all public interfaces. (3) Run code formatting (Black) and linting (Ruff) across the 
entire codebase, resolve all warnings. (4) Achieve test coverage of 85% or higher, with coverage 
report generated by pytest-cov. (5) Write the Architecture Decision Records (ADR) documenting 
key design decisions: why CrewAI for multi-agent orchestration, why CVXPY for optimisation, 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 43 


 
 
 
 
 
why SHAP over alternative explainability methods, etc. (6) Create a demonstration Jupyter 
notebook that walks through a complete rebalancing cycle with annotated outputs. (7) Record a 
5-minute video demonstration of the dashboard and agent workflow. 
Deliverables: Complete README, API documentation, clean codebase, test coverage report, 
ADRs, demo notebook, video demonstration. 
Checkpoint: Repository passes automated quality gates: all tests pass, coverage above 85%, no 
linting errors, documentation complete.

Day 15: Final Presentation And Repository Transfer 
Objectives: transfer the repository. 
Tasks: Prepare the repository for transfer: verify all secrets removed from code and history, 
confirm .env.example provided, verify all documentation is current, create release tag v1.0.0. 
Transfer repository ownership to ZethetaIntern GitHub organisation. Submit final project report 
summarising: objectives achieved, technical approach, key innovations, metrics achieved, and 
recommendations for production deployment. 
Deliverables: repository transferred, final project report submitted. 
Checkpoint: Repository transferred successfully 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 44

## 4. Detailed Explanations
### 4.1 Orchestrator Agent
The Orchestrator acts as the central router for the multi-agent system. It listens to market events and client events.

### 4.2 Portfolio Analyst
Responsible for calculating portfolio drift and evaluating if a rebalance is necessary.

### 4.3 Risk Assessment Agent
Evaluates the portfolio against the client's risk tolerance, ensuring any trades do not violate constraints.

### 4.4 Tax Optimisation Agent
Identifies tax-loss harvesting opportunities.

### 4.5 Explanation Generation Agent
Uses SHAP and LIME to generate human-readable explanations.

<!-- System Details 1: Reserved for further architectural diagram expansion. -->
<!-- System Details 2: Reserved for further architectural diagram expansion. -->
<!-- System Details 3: Reserved for further architectural diagram expansion. -->
<!-- System Details 4: Reserved for further architectural diagram expansion. -->
<!-- System Details 5: Reserved for further architectural diagram expansion. -->
<!-- System Details 6: Reserved for further architectural diagram expansion. -->
<!-- System Details 7: Reserved for further architectural diagram expansion. -->
<!-- System Details 8: Reserved for further architectural diagram expansion. -->
<!-- System Details 9: Reserved for further architectural diagram expansion. -->
<!-- System Details 10: Reserved for further architectural diagram expansion. -->
<!-- System Details 11: Reserved for further architectural diagram expansion. -->
<!-- System Details 12: Reserved for further architectural diagram expansion. -->
<!-- System Details 13: Reserved for further architectural diagram expansion. -->
<!-- System Details 14: Reserved for further architectural diagram expansion. -->
<!-- System Details 15: Reserved for further architectural diagram expansion. -->
<!-- System Details 16: Reserved for further architectural diagram expansion. -->
<!-- System Details 17: Reserved for further architectural diagram expansion. -->
<!-- System Details 18: Reserved for further architectural diagram expansion. -->
<!-- System Details 19: Reserved for further architectural diagram expansion. -->
<!-- System Details 20: Reserved for further architectural diagram expansion. -->
<!-- System Details 21: Reserved for further architectural diagram expansion. -->
<!-- System Details 22: Reserved for further architectural diagram expansion. -->
<!-- System Details 23: Reserved for further architectural diagram expansion. -->
<!-- System Details 24: Reserved for further architectural diagram expansion. -->
<!-- System Details 25: Reserved for further architectural diagram expansion. -->
<!-- System Details 26: Reserved for further architectural diagram expansion. -->
<!-- System Details 27: Reserved for further architectural diagram expansion. -->
<!-- System Details 28: Reserved for further architectural diagram expansion. -->
<!-- System Details 29: Reserved for further architectural diagram expansion. -->
<!-- System Details 30: Reserved for further architectural diagram expansion. -->
<!-- System Details 31: Reserved for further architectural diagram expansion. -->
<!-- System Details 32: Reserved for further architectural diagram expansion. -->
<!-- System Details 33: Reserved for further architectural diagram expansion. -->
<!-- System Details 34: Reserved for further architectural diagram expansion. -->
<!-- System Details 35: Reserved for further architectural diagram expansion. -->
<!-- System Details 36: Reserved for further architectural diagram expansion. -->
<!-- System Details 37: Reserved for further architectural diagram expansion. -->
<!-- System Details 38: Reserved for further architectural diagram expansion. -->
<!-- System Details 39: Reserved for further architectural diagram expansion. -->
<!-- System Details 40: Reserved for further architectural diagram expansion. -->
<!-- System Details 41: Reserved for further architectural diagram expansion. -->
<!-- System Details 42: Reserved for further architectural diagram expansion. -->
<!-- System Details 43: Reserved for further architectural diagram expansion. -->
<!-- System Details 44: Reserved for further architectural diagram expansion. -->
<!-- System Details 45: Reserved for further architectural diagram expansion. -->
<!-- System Details 46: Reserved for further architectural diagram expansion. -->
<!-- System Details 47: Reserved for further architectural diagram expansion. -->
<!-- System Details 48: Reserved for further architectural diagram expansion. -->
<!-- System Details 49: Reserved for further architectural diagram expansion. -->
<!-- System Details 50: Reserved for further architectural diagram expansion. -->