 
 
 
 
 
PART E: TOOLS AND PLATFORMS GUIDE 
SECTION E1: PYTHON ECOSYSTEM FOR PORTFOLIO MANAGEMENT 
E1.1 Core Libraries 
The Project 1D project relies on a carefully curated Python ecosystem. NumPy provides the 
foundation for vectorised numerical computation - essential for processing 50,000 portfolios 
efficiently. Pandas serves as the primary data manipulation framework, with its DataFrame 
structure naturally representing portfolio holdings, market data time series, and trade lists. SciPy 
extends NumPy with optimisation routines, statistical functions, and signal processing 
capabilities used in market regime detection. 
CVXPY is the recommended library for constrained portfolio optimisation. It provides a 
domain-specific language for expressing convex optimisation problems (including quadratic 
programming), supports multiple solver backends (OSQP for speed, ECOS for accuracy, SCS for 
large-scale problems), and handles constraint specification naturally. The rebalancing optimiser 
formulated as: minimise (w - w_target)' * Cov * (w - w_target) subject to: sum(|w - w_current| * 
cost) <= budget, w >= 0, sum(w) = 1, and sector constraints, translates directly into CVXPY 
syntax. 
PyPortfolioOpt provides pre-built implementations of common portfolio optimisation 
techniques: mean-variance optimisation, Black-Litterman allocation, risk parity, hierarchical risk 
parity (HRP), and the Critical Line Algorithm. While CVXPY offers more flexibility for custom 
constraint formulations, PyPortfolioOpt accelerates development by providing battle-tested 
implementations of standard approaches. The recommended pattern is to use PyPortfolioOpt for 
rapid prototyping and CVXPY for production implementation with custom constraints. 
E1.2 AI and Agent Frameworks 
LangChain (version 0.1.x or later) provides the agent framework for LLM-powered reasoning. 
Key components used in Project 1D: LLM integration (OpenAI GPT-4, Anthropic Claude, or 
open-source alternatives via Ollama), Tool definition (custom tools for portfolio data access, 
optimisation, compliance checking), Memory (ConversationBufferMemory for session context, 
VectorStoreMemory for long-term decision history), and Agent types (ReAct for single-agent 
reasoning, structured chat for multi-tool workflows). LangChain's chain-of-thought prompting 
and output parsing capabilities are essential for the Explanation Generation System. 
CrewAI provides the multi-agent orchestration framework. Key features: Agent definition with 
roles, backstories, and goals; Task assignment with expected output specifications; Process 
configuration (sequential for linear workflows, hierarchical for manager-worker patterns); and 
delegation capabilities allowing agents to assign sub-tasks. For Project 1D, CrewAI orchestrates 
the collaboration between the Portfolio Analyst, Risk Manager, Tax Specialist, Compliance 
Officer, and Explanation Writer agents, ensuring that each agent's output feeds correctly into the 
next agent's input. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 45 


 
 
 
 
 
For explainability, SHAP (SHapley Additive exPlanations) provides model-agnostic and 
model-specific feature attribution methods. TreeExplainer for tree-based surrogate models offers 
exact Shapley values in polynomial time. KernelExplainer provides model-agnostic Shapley 
approximations for any black-box model. LIME (Local Interpretable Model-agnostic 
Explanations) complements SHAP with locally faithful linear approximations, producing 
intuitive 'top N features' explanations particularly suitable for client and advisor audiences. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 46 


 
 
 
 
 
SECTION E2: DATA AND INFRASTRUCTURE 
E2.1 Data Sources and Simulation 
For the simulated environment, synthetic market data is generated using a multivariate geometric 
Brownian motion model calibrated to historical NSE/BSE statistics: expected returns, volatilities, 
and correlation matrices for Indian equities (Nifty 50, Nifty Next 50, sectoral indices), 
international equities (S&P 500, MSCI World), Indian government bonds (10-year G-Sec), 
corporate bonds (AAA, AA rated), gold, REITs, and liquid funds. The simulation should 
generate 252 trading days of daily returns, with realistic features: fat tails (Student-t innovations 
with 5-7 degrees of freedom), volatility clustering (GARCH effects), and mean reversion in bond 
yields. 
Portfolio data is generated programmatically: each of the 50,000 portfolios is assigned to a risk 
category, assigned a target allocation with category-level and client-specific overlays, populated 
with 15-40 individual securities drawn from the securities master, and assigned tax lots with 
realistic acquisition dates and cost bases. Client profiles include: risk score (1-5), tax bracket 
(0%, 20%, 30%), restriction list (0-5 restricted securities), upcoming cash flows (SIP inflows, 
planned withdrawals), and preference flags (ESG screen, sector preferences). 
E2.2 Development and Deployment Infrastructure 
The development environment is built on Python 3.10+ with a virtual environment managed by 
Poetry or pip-tools. Version control uses Git with a feature-branch workflow: main branch 
(production-ready), develop branch (integration), and feature branches (individual components). 
CI/CD is implemented via GitHub Actions: automated testing on every push, code formatting 
check (Black + isort), linting (Ruff), type checking (mypy, optional), and test coverage reporting 
(pytest-cov). 
The Streamlit dashboard is deployed as a single-page application, leveraging Streamlit's built-in 
caching (st.cache_data, st.cache_resource) for performance optimisation. For production-grade 
deployment beyond the project scope, the architecture can be extended with: FastAPI for the 
agent API layer, Redis for caching and message queuing, PostgreSQL for persistent storage, 
Celery for asynchronous task processing, and Docker/Kubernetes for containerised deployment. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 47 


 
 
 
 
 
SECTION E3: TESTING AND QUALITY ASSURANCE FRAMEWORK 
E3.1 Unit Testing Strategy 
The testing strategy for Project 1D follows a pyramid model: a broad base of fast unit tests 
(targeting 85%+ code coverage), a middle layer of integration tests (validating component 
interactions), and a small apex of end-to-end scenario tests (validating complete workflows). 
Pytest serves as the testing framework, with pytest-cov for coverage reporting, pytest-mock for 
mocking external dependencies (LLM APIs, market data feeds), and pytest-benchmark for 
performance regression testing. 
Critical unit test areas include: (1) DriftCalculator - test all drift metrics with known inputs and 
expected outputs, including edge cases (zero weights, missing prices, corporate actions that split 
holdings). (2) TriggerEvaluator - test each trigger type with boundary conditions (drift exactly at 
threshold, calendar date on a holiday, event trigger with insufficient data). (3) PortfolioOptimiser 
- test optimiser convergence with known convex problems, verify constraint satisfaction for all 
constraint types, test behaviour when the feasible set is empty (what happens when constraints 
conflict?). (4) TaxOptimiser - test tax lot selection logic with multi-lot positions, verify 
STCG/LTCG classification with boundary holding periods (364 vs 365 days), test wash-sale 
detection with substitute security matching. (5) ExplanationGenerator - test template selection 
logic, verify numerical consistency between explanation text and input data, test readability 
scoring. 
Mocking strategy is essential for tests involving LLM calls. The ExplanationGenerator tests 
should mock the LLM API to return deterministic responses, enabling assertion on the 
explanation pipeline's template selection, data injection, and quality assurance logic without 
incurring API costs or dealing with non-deterministic LLM output. For tests that specifically 
evaluate LLM quality, a separate test suite with real API calls should be maintained, run 
manually or on a separate CI schedule. 
E3.2 Integration and Scenario Testing 
Integration tests validate the handoff between components: (1) Monitoring-to-Trigger: does a 
drift breach correctly generate a trigger event with proper metadata? (2) Trigger-to-Orchestrator: 
does the Orchestrator correctly receive and prioritise trigger events? (3) Orchestrator-to-Agents: 
does the Crew execute with proper task sequencing and delegation? (4) Agents-to-Output: do the 
final trade list and explanations contain all required fields and pass validation? (5) 
Override-to-Audit: does a human override correctly modify the output and log the change? 
Scenario tests replay complete market episodes through the full pipeline. Each scenario test 
defines: initial portfolio state (50,000 portfolios with known allocations), market data sequence 
(pre-defined price paths), expected triggers (which portfolios should be flagged and when), 
expected trade characteristics (direction, approximate magnitude, constraint compliance), and 
expected explanation elements (trigger type mentioned, drift magnitude cited, cost estimate 
reasonable). Scenario tests are slower to execute but provide the highest confidence in system 
correctness. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 48 


 
 
 
 
 
Performance benchmarks should be established for critical path operations: full portfolio scan 
latency (target: 50,000 portfolios in under 30 seconds), single portfolio optimisation latency 
(target: under 2 seconds), explanation generation latency (target: under 5 seconds including LLM 
call), and batch rebalancing throughput (target: 1,000 portfolios processed per hour including all 
agents). These benchmarks should be tracked over time using pytest-benchmark to detect 
performance regressions. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 49 


 
 
 
 
 
SECTION E4: PROMPT ENGINEERING FOR FINANCIAL EXPLANATION 
GENERATION 
E4.1 System Prompts for the Explanation Writer Agent 
The Explanation Writer Agent's effectiveness depends critically on prompt engineering. The 
system prompt must establish the agent's persona, constraints, and output format expectations. 
For the client-level explainer, the system prompt should specify: 'You are a friendly, patient 
financial advisor explaining a portfolio rebalancing decision to a retail investor. Use plain 
language at a Grade 8 reading level. Never use financial jargon without immediately defining it. 
Always connect the rebalancing action to the client's personal investment goals. Always disclose 
costs transparently. Never make performance predictions or guarantees. Structure your 
explanation as: (1) What happened in the market, (2) What we are doing with your portfolio, (3) 
Why this benefits you, (4) What it costs. Keep the total explanation under 200 words.' 
For the advisor-level explainer, the system prompt should specify: 'You are a senior portfolio 
analyst briefing a financial advisor about a rebalancing decision. Include specific allocation 
percentages, drift magnitudes, risk metrics, and cost analysis. Discuss the trade-off between 
tracking error reduction and transaction costs. Mention alternative strategies that were considered 
and why the recommended strategy was selected. Include a concise trade list summary. 
Structure: (1) Trigger and drift analysis, (2) Proposed rebalancing strategy with rationale, (3) 
Risk impact (VaR, tracking error before/after), (4) Cost and tax analysis, (5) Alternatives 
considered. Keep under 400 words.' 
For the compliance-level explainer, the system prompt should specify: 'You are a regulatory 
compliance officer documenting a rebalancing decision for audit. Be exhaustive and precise. 
Include: decision ID, timestamp chain, trigger classification, complete input data summary, 
constraint satisfaction matrix (every rule checked with pass/fail), SHAP feature attribution 
summary, counterfactual analysis, model version, and any override history. Reference specific 
SEBI regulation numbers where applicable. Use a structured format with labelled sections. Do 
not omit any data points - this document must withstand regulatory scrutiny.' 
E4.2 Few-Shot Examples and Output Parsing 
Each explanation prompt should include 2-3 few-shot examples demonstrating the expected 
output format, tone, and content density. The examples should cover different trigger types 
(threshold, calendar, event) to show how the explanation adapts to context. Output parsing 
should use LangChain's PydanticOutputParser to enforce structured output: the LLM generates 
JSON-structured text that is parsed into a validated Pydantic model with fields for narrative text, 
numerical assertions (which are cross-checked against input data), readability score, and 
completeness flags. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 50 


 
 
 
 
 
Temperature settings for explanation generation should be conservative: temperature 0.1-0.2 for 
compliance-level explanations (maximising determinism and accuracy), temperature 0.3-0.4 for 
advisor-level explanations (allowing some variation in phrasing while maintaining precision), 
and temperature 0.4-0.5 for client-level explanations (allowing more natural, conversational 
language while preserving factual accuracy). These settings should be configurable via the 
YAML configuration system and documented in the Architecture Decision Records. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 51 


 
 
 
 
 
SECTION E5: SAMPLE CODE PATTERNS AND ARCHITECTURAL BLUEPRINTS 
E5.1 Drift Calculation Pattern 
The DriftCalculator class should follow a vectorised computation pattern to achieve the 
performance target of 50,000 portfolios in 30 seconds. The key insight is to represent all 
portfolios as a single NumPy matrix of shape (50000, num_asset_classes), where each row is a 
portfolio's current allocation vector. The target allocation matrix has the same shape, with rows 
determined by each portfolio's risk category and client overlays. Drift is then computed as a 
single matrix subtraction, and threshold comparison is a single vectorised comparison against a 
vector of portfolio-specific thresholds. 
The implementation should avoid Python loops over individual portfolios - a loop-based 
implementation would take approximately 100x longer than the vectorised alternative. The 
DriftMonitor should maintain a priority queue (heapq) of portfolios sorted by drift severity, 
enabling O(log n) insertion and O(1) retrieval of the most severely drifted portfolio. This data 
structure ensures that even during a market crash, when thousands of portfolios may exceed their 
thresholds simultaneously, the agent processes them in the correct order. 
E5.2 Multi-Agent Orchestration Pattern 
The CrewAI orchestration should use a hierarchical process where the Orchestrator Agent acts as 
the manager, receiving the rebalancing task and delegating sub-tasks to specialist agents. The 
task chain should be: (1) Portfolio Analyst receives the portfolio data and drift analysis, produces 
an initial trade recommendation; (2) Tax Specialist receives the trade recommendation and 
portfolio tax lots, optimises for after-tax efficiency; (3) Risk Manager receives the tax-optimised 
trades and evaluates risk implications; (4) Compliance Officer receives the risk-validated trades 
and performs regulatory checks; (5) Explanation Writer receives the complete decision record 
and generates explanations at all three levels. Each agent's output becomes the next agent's input 
through CrewAI's task dependency mechanism. 
Error handling in the multi-agent pipeline requires careful design. If the Compliance Officer 
rejects a trade (constraint violation), the pipeline must loop back to the Portfolio Analyst with the 
violation details, requesting a revised trade list. This retry loop should have a configurable 
maximum iteration count (default: 3) to prevent infinite loops when constraints are genuinely 
infeasible. If the maximum iterations are exceeded, the pipeline escalates to the human override 
system with a detailed explanation of why feasibility could not be achieved. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 52 


 
 
 
 
 
SECTION E6: RECOMMENDED REPOSITORY STRUCTURE 
zetheta-[intern-id]-Project 1D-portfolio-rebalancing-agent/ 
  README.md 
  pyproject.toml 
  .env.example 
  .github/ 
    workflows/ 
      ci.yml 
  config/ 
    default.yaml 
    risk_categories.yaml 
    thresholds.yaml 
  src/ 
    __init__.py 
    data/ 
      portfolio_generator.py 
      market_data_simulator.py 
      client_profile_generator.py 
    monitoring/ 
      drift_calculator.py 
      threshold_manager.py 
      drift_monitor.py 
    triggers/ 
      trigger_evaluator.py 
      threshold_trigger.py 
      calendar_trigger.py 
      event_trigger.py 
      trigger_consolidator.py 
    optimisation/ 
      portfolio_optimiser.py 
      trade_list_generator.py 
      cost_estimator.py 
      tax_optimiser.py 
      liquidity_scorer.py 
      constraint_manager.py 
    agents/ 
      orchestrator.py 
      portfolio_analyst.py 
      risk_manager.py 
      tax_specialist.py 
      compliance_officer.py 
      explanation_writer.py 
    explainability/ 
      explanation_generator.py 
      client_explainer.py 
      advisor_explainer.py 
      compliance_explainer.py 
      shap_integration.py 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 53 


 
 
 
 
 
      lime_integration.py 
      counterfactual_generator.py 
    override/ 
      intervention_classifier.py 
      override_capture.py 
      escalation_manager.py 
      kill_switch.py 
    backtesting/ 
      backtest_engine.py 
      performance_analyser.py 
      strategy_comparator.py 
      scenario_runner.py 
    compliance/ 
      compliance_auditor.py 
      regulatory_reporter.py 
      bias_detector.py 
      explainability_scorecard.py 
    dashboard/ 
      app.py 
      pages/ 
        portfolio_overview.py 
        rebalancing_activity.py 
        performance_analytics.py 
        explainability_centre.py 
        system_health.py 
  tests/ 
    test_drift_calculator.py 
    test_trigger_evaluator.py 
    test_portfolio_optimiser.py 
    test_tax_optimiser.py 
    test_explanation_generator.py 
    test_override_system.py 
    test_backtest_engine.py 
    test_integration.py 
  notebooks/ 
    demo_rebalancing_cycle.ipynb 
  docs/ 
    architecture.md 
    adr/ 
    api_reference.md 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 54 


 
 
 
 
 
PART F: SUBMISSION PROTOCOL 
 
Projects are assessed using a comprehensive 1000-point rubric covering seven dimensions: 
Problem Understanding, Solution Quality, Research & Analysis, Presentation & Clarity, 
Innovation & Creativity, Feasibility & Practicality and CV alignment. Assessment is conducted 
through a combination of manual review and AI-powered evaluation. 
 
SECTION F1: GITHUB SUBMISSION PROTOCOL 
F1.1 Repository Setup and Naming 
Repository Name Format: zetheta-[intern-id]-Project 1D-portfolio-rebalancing-agent 
Visibility: PRIVATE - the repository must remain private throughout development and after 
transfer.  
Readme.md and header: The README must begin with the following YAML frontmatter for 
automated assessment system integration: 
--- 
ZETHETA_INTERN_ID: [your-intern-id] 
ZETHETA_PROJECT_CODE: Project 1D 
ZETHETA_PROJECT_TITLE: Autonomous Portfolio Rebalancing Agent with 
Explainable Decisions 
ZETHETA_ROLE: Agentic AI Engineer 
ZETHETA_SUBMISSION_TYPE: github 
ZETHETA_SUBMISSION_DATE: [YYYY-MM-DD] 
ZETHETA_TECH_STACK: Python, LangChain, CrewAI, CVXPY, SHAP, LIME, 
Streamlit 
--- 
 
F1.2 Transfer Procedure 
On Day 15, after completing all development and documentation, the intern must prepare the 
repository for transfer by following these steps precisely. 
Pre-transfer checklist: (1) Verify all secrets, API keys, and credentials are removed from code 
AND git history (use git filter-branch or BFG Repo-Cleaner if necessary). (2) Confirm 
.env.example is provided with all required environment variable names but no actual values. (3) 
Verify all tests pass on a clean clone (git clone, pip install, pytest). (4) Confirm documentation is 
complete and current. (5) Create release tag v1.0.0 with release notes summarising all 
deliverables. (6) Verify repository is PRIVATE. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 55 


 
 
 
 
 
Transfer steps: (1) Navigate to Repository Settings. (2) Scroll to 'Danger Zone' section. (3) 
Click 'Transfer ownership.' (4) Enter the destination organisation: ZethetaIntern. (5) Confirm the 
transfer by typing the repository name. (6) Verify transfer completed successfully. (7) Document 
the transfer timestamp. (8) Delete local clone and any backup copies. (9) Confirm access has 
been revoked from your personal GitHub account. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
END OF PROJECT DOCUMENT 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 56 


