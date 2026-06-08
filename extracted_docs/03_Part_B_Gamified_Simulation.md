 
 
 
 
 
PART B: GAMIFIED SIMULATION BUSINESS CONCEPT 
Note on the Simulation Concept: The gamified simulation concept presented in this section is 
provided as a reference framework. Students may choose to follow this concept or design their 
own original gamified simulation - with a different name, structure, narrative, or game 
mechanics - as long as it meets the assessment criteria outlined in Part F. 
 
SECTION B1: SIMULATION NARRATIVE AND ROLE-PLAY SETUP 
B1.1 The Scenario 
You are the AI Agent Lead at WealthPilot AI, a next-generation robo-advisory firm 
headquartered in Mumbai with operations across India, Singapore, and Dubai. WealthPilot AI 
manages INR 25,000 crores across 50,000 client portfolios spanning 5 risk categories: 
Ultra-Conservative, Conservative, Balanced, Aggressive, and Ultra-Aggressive. Each risk 
category has a defined Strategic Asset Allocation (SAA) across 6 asset classes: Indian Equities, 
International Equities, Indian Fixed Income, International Fixed Income, Alternatives (Gold, 
REITs), and Cash/Liquid Instruments. 
The firm has experienced rapid growth - from 5,000 portfolios to 50,000 in 18 months - and the 
existing rule-based rebalancing system is buckling under the strain. The legacy system triggers 
calendar-based quarterly rebalances uniformly, regardless of drift severity, market conditions, or 
client-specific circumstances. This approach results in unnecessary trading (and costs) for 
portfolios with minimal drift, delayed action for portfolios with severe drift, identical treatment 
of a 25-year-old aggressive investor and a 65-year-old retiree, no tax-aware execution, generic 
one-size-fits-all client communications, and zero compliance audit trail beyond trade records. 
The Board of Directors has approved a INR 5 crore budget to build an Autonomous Portfolio 
Rebalancing Agent that will replace the legacy system. Your mandate: design, build, and deploy 
an AI agent that monitors portfolio drift in near-real-time, evaluates rebalancing triggers 
intelligently (threshold-based, calendar-based, and event-driven), generates constraint-aware 
trade lists optimised for after-tax returns, produces human-readable explanations at three 
audience levels (client, advisor, compliance), supports human override with full audit trails, and 
demonstrates measurable improvement over the legacy system in backtesting. 
B1.2 Portfolio Universe And Risk Categories 
The 50,000 portfolios are distributed across the 5 risk categories with the following target 
allocations and rebalancing parameters. Note that each parameter has been carefully calibrated 
based on academic research and industry best practice. 
 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 21 


 
 
 
 
 
 
 
Risk Category 
Portfolios 
Equity 
% 
Fixed 
Income % 
Alternatives 
% 
Cash 
% 
Drift 
Band 
Ultra-Conservative 
5,000 
15% 
60% 
10% 
15% 
2.0% 
Conservative 
12,000 
30% 
45% 
12% 
13% 
2.5% 
Balanced 
18,000 
50% 
30% 
12% 
8% 
3.0% 
Aggressive 
10,000 
70% 
15% 
10% 
5% 
4.0% 
Ultra-Aggressive 
5,000 
85% 
5% 
7% 
3% 
5.0% 
 
Within each risk category, individual portfolios may deviate from the category-level SAA based 
on 
client-specific 
overlays: 
ethical 
screens 
(ESG 
exclusions), 
sector 
preferences 
(overweight/underweight specific sectors), single-stock restrictions (concentrated positions from 
ESOP holdings), liquidity requirements (upcoming cash needs), and tax situation (high-income 
bracket requiring aggressive tax-loss harvesting versus low-income bracket where harvesting has 
marginal value). 
B1.3 Market Scenarios And Event Triggers 
The simulation presents a series of market scenarios that the agent must navigate over a 
simulated 12-month period. These scenarios are designed to test the agent's behaviour under 
normal conditions, stressed conditions, and ambiguous conditions where the optimal action is 
unclear. 
SCENARIO 1 - NORMAL DRIFT: Gradual equity market appreciation of 12-15% over 3 
months causes equity allocations to drift above targets across all risk categories. The agent must 
demonstrate intelligent threshold monitoring and cost-efficient rebalancing. 
SCENARIO 2 - MARKET CRASH: A sudden 22% equity market correction over 5 trading 
sessions triggers severe drift across all portfolios simultaneously. The agent must prioritise 
rebalancing across 50,000 portfolios, manage execution under stress, and communicate clearly 
with panicked investors. This scenario tests the agent's scalability, prioritisation logic, and crisis 
communication capabilities. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 22 


 
 
 
 
 
SCENARIO 3 - SECTOR ROTATION: A sharp rotation from growth to value stocks over 6 
weeks causes intra-equity drift (sector concentrations exceed limits) without significant overall 
equity allocation drift. The agent must demonstrate sub-asset-class monitoring and targeted 
rebalancing within asset classes. 
SCENARIO 4 - REGULATORY EVENT: SEBI announces new rules restricting international 
equity allocation for retail investors to 15% of portfolio (previously 25%). The agent must 
identify affected portfolios, generate compliant trade lists, and explain the regulatory-driven 
changes to clients within the compliance deadline. 
SCENARIO 5 - TAX HARVESTING OPPORTUNITY: March end-of-financial-year creates 
a window for tax-loss harvesting. The agent must identify portfolios with harvestable losses, 
generate trades that realise losses while maintaining target exposures (using substitute securities), 
and quantify the tax benefit for each client. The agent must balance tax efficiency against 
tracking error and transaction costs. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 23 


 
 
 
 
 
SECTION B2: AGENT DECISION ARCHITECTURE 
B2.1 System Architecture Overview 
The Autonomous Portfolio Rebalancing Agent follows a modular, event-driven architecture with 
six core components: the Data Ingestion Layer, the Drift Monitoring Engine, the Trigger 
Evaluation Module, the Trade Generation Optimiser, the Explanation Generation System, and the 
Execution and Audit Layer. Each component operates as a semi-autonomous agent within a 
multi-agent framework, communicating through a shared event bus and a centralised state store. 
The Data Ingestion Layer continuously pulls portfolio holdings data from the custody system, 
market 
prices 
from 
the 
exchange 
data 
feed 
(NSE/BSE 
for Indian instruments, 
Bloomberg/Reuters for international instruments), reference data from the master security 
database, client profile data from the CRM system, and regulatory rule updates from the 
compliance database. Data quality checks - stale price detection, missing holdings reconciliation, 
corporate action processing - are performed at ingestion, with anomalies flagged for the 
Monitoring Engine. 
The Drift Monitoring Engine computes drift metrics for every portfolio at configurable intervals 
(real-time during market hours, end-of-day for batch processing). For each portfolio, it 
calculates: asset class level drift, sub-asset class level drift (sector, geography, duration), factor 
exposure drift (beta, value, momentum, quality), risk metric drift (VaR, tracking error, Sharpe 
ratio), and concentration metrics (issuer, sector, geography). Drift values are compared against 
portfolio-specific thresholds (determined by risk category and client overlays), and portfolios 
exceeding any threshold are queued for the Trigger Evaluation Module. 
The Trigger Evaluation Module applies a multi-criteria decision framework to determine whether 
a flagged portfolio should be rebalanced immediately, scheduled for near-term rebalancing, or 
monitored with increased frequency. The decision criteria include: drift severity and trend (is 
drift increasing or mean-reverting?), market regime (normal, stressed, or transitional?), 
cost-benefit analysis (does the expected benefit of rebalancing exceed the estimated cost?), 
client-specific factors (upcoming cash flows, tax status, restriction changes?), and operational 
capacity (how many portfolios can be rebalanced in the current session without exceeding 
market impact limits?). 
B2.2 Multi-Agent Coordination Model 
The multi-agent system for the rebalancing agent is structured as a hierarchical Crew with the 
following roles and responsibilities. The Orchestrator Agent serves as the central coordinator, 
receiving triggers from the Monitoring Engine, assigning tasks to specialist agents, resolving 
conflicts between agents, and managing the overall workflow. The Orchestrator implements a 
priority queue, processing the most urgent rebalancing tasks first (event-driven triggers take 
precedence over threshold triggers, which take precedence over calendar triggers). 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 24 


 
 
 
 
 
The Portfolio Analyst Agent is responsible for deep analysis of each flagged portfolio: 
computing optimal target trades, evaluating multiple rebalancing strategies (full rebalance to 
target, partial rebalance to band edge, phased rebalance over multiple days), and recommending 
the strategy with the best cost-benefit profile. This agent invokes the portfolio optimiser tool, 
which solves the constrained quadratic programming problem to minimise tracking error subject 
to transaction cost budgets, tax constraints, liquidity limits, and client-specific restrictions. 
The Risk Assessment Agent evaluates the risk implications of every proposed trade list: 
computing pre-trade and post-trade VaR, stress-testing the proposed portfolio against historical 
crisis scenarios, checking for factor concentration risks, and verifying that the rebalanced 
portfolio remains within the client's risk category bounds. If the proposed trades would move a 
portfolio outside acceptable risk parameters, the Risk Assessment Agent flags the issue and 
requests the Portfolio Analyst Agent to revise the trade list. 
The Tax Optimisation Agent analyses the tax implications of each proposed trade at the tax-lot 
level: identifying lots eligible for long-term capital gains treatment, calculating the tax cost of 
each sell order, identifying opportunities to harvest losses, and proposing alternative execution 
strategies that achieve the same rebalancing objective with lower tax impact. In the Indian 
context, this agent must account for the grandfathering provisions for pre-2018 equity gains, the 
different treatment of debt fund gains post-2023, and the indexation versus non-indexation 
trade-off for applicable instruments. 
The Compliance Verification Agent performs pre-trade compliance checks against the full rule 
set: SEBI regulatory limits, exchange-specific limits, client-specific restrictions, and internal risk 
management policies. Every proposed trade is validated, and any violation is flagged with a 
specific rule reference and remediation suggestion. The Compliance Agent also generates the 
regulatory audit trail, documenting the decision chain from trigger to execution. 
The Explanation Generation Agent produces human-readable explanations at three audience 
levels (client, advisor, compliance) for every rebalancing decision. This agent takes as input the 
decision metadata (trigger type, drift values, proposed trades, constraint satisfaction, risk metrics, 
tax implications) and generates tailored narratives using structured templates enhanced by 
LLM-powered natural language generation. The Explanation Agent also generates visualisations: 
portfolio allocation before/after pie charts, drift trend line charts, and SHAP waterfall plots for 
the compliance audience. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 25 


 
 
 
 
 
SECTION B3: REBALANCING TRIGGER TAXONOMY 
B3.1 Comprehensive Trigger Classification 
The rebalancing trigger system operates as a three-tier hierarchy with distinct evaluation logic, 
priority levels, and response timelines for each trigger type. 
Trigger Type 
Evaluation Logic 
Priority 
Response Timeline 
Threshold - Asset 
Class Drift 
Absolute drift 
exceeds 
risk-category-specific 
band 
HIGH 
Within 1 trading 
session 
Threshold - Factor 
Exposure Drift 
Factor tilt exceeds 
1.5 standard 
deviations from 
target 
MEDIUM 
Within 3 trading 
sessions 
Threshold - 
Concentration Breach 
Single issuer/sector 
exceeds hard limit 
CRITICAL 
Immediate (same 
session) 
Calendar - Monthly 
Review 
First business day of 
each month 
LOW 
Within 5 trading 
sessions 
Calendar - Quarterly 
Full Review 
First week of each 
quarter 
MEDIUM 
Within 5 trading 
sessions 
Calendar - Annual 
Strategic Review 
Client anniversary 
date 
MEDIUM 
Within 10 trading 
sessions 
Event - Market Crash 
(>10% drop) 
Index decline 
exceeds 10% from 
recent high 
CRITICAL 
Immediate 
assessment 
Event - Regulatory 
Change 
New SEBI circular 
affecting allocations 
CRITICAL 
Within compliance 
deadline 
Event - Client Life 
Event 
Retirement, 
inheritance, large 
deposit/withdrawal 
HIGH 
Within 2 trading 
sessions 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 26 


 
 
 
 
 
Event - Corporate 
Action 
Merger, spin-off, 
delisting of held 
security 
HIGH 
Before ex-date 
Event - Tax 
Harvesting Window 
March FY-end 
tax-loss harvesting 
opportunity 
MEDIUM 
Within 
tax-optimisation 
window 
Event - Cash Flow 
Dividend/coupon 
reinvestment, SIP 
inflow 
LOW 
Within 3 trading 
sessions 
 
When multiple triggers fire simultaneously for the same portfolio, the agent applies the 
highest-priority trigger's response timeline and consolidates all triggered actions into a single 
rebalancing event. This prevents cascading trades and reduces transaction costs. The agent logs 
each contributing trigger for the audit trail, enabling compliance review of the multi-trigger 
consolidation logic. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 27 


 
 
 
 
 
SECTION B4: EXPLANATION GENERATION FRAMEWORK 
B4.1 Three-Tier Explanation Architecture 
The Explanation Generation Framework employs a structured approach to producing 
explanations that satisfy the needs of three distinct audiences. At each tier, the explanation is 
generated from the same underlying decision metadata but is transformed through 
audience-specific templates, language models, and formatting rules. 
The generation pipeline follows five stages: (1) Decision Metadata Extraction - collecting all 
relevant data points from the rebalancing decision (trigger type, drift values, proposed trades, 
constraint checks, risk metrics, tax impact, market context); (2) Template Selection - choosing 
the appropriate explanation template based on trigger type and audience; (3) Content Generation 
- using LLM-powered natural language generation to fill templates with contextualised, coherent 
narratives; (4) Quality Assurance - automated checks for accuracy (do the numbers in the 
explanation match the decision data?), completeness (are all required elements present?), and 
readability (Flesch-Kincaid grade level appropriate for the audience?); (5) Formatting and 
Delivery - rendering the explanation in the appropriate format (email for clients, dashboard 
widget for advisors, structured audit record for compliance). 
The client-level explanation follows a four-part structure: What Happened (market context that 
caused portfolio drift), What We Are Doing (plain-language description of the trades), Why This 
Is Good For You (connection to the client's personal goals and risk preferences), and What It 
Costs (transparent disclosure of transaction costs and estimated tax impact). Language is limited 
to Grade 8 reading level, avoids all financial jargon, and uses analogies where helpful ('Think of 
rebalancing like trimming a garden - we cut back the fast-growing plants and give the slower 
ones more room, keeping your garden in the shape you designed.'). 
The advisor-level explanation includes quantitative detail: exact allocation percentages (before 
and after), drift magnitude and trend, key metrics (tracking error, Sharpe ratio, VaR), trade list 
summary with cost and tax analysis, and a brief discussion of alternative strategies considered 
and why the recommended strategy was selected. This level supports the advisor's ability to 
review, understand, and if necessary override the agent's recommendation. 
The compliance-level explanation is the most comprehensive, constituting the formal audit 
record. It includes: unique decision identifier, timestamp chain (from trigger detection to 
explanation generation), complete input data snapshot, full constraint satisfaction matrix (every 
rule checked, with pass/fail status), SHAP or LIME feature attribution values, counterfactual 
analysis ('the decision would have changed if...'), model version and configuration at time of 
decision, and any human override history. This record must be immutable, time-stamped, and 
retained for the regulatory minimum period (8 years under SEBI regulations). 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 28 


 
 
 
 
 
SECTION B5: OVERRIDE AND MANUAL INTERVENTION WORKFLOW 
B5.1 Human-In-The-Loop Design 
The override system implements a graduated intervention model with four levels: (1) 
Informational - the agent notifies the advisor of its autonomous decision post-execution (for 
low-risk, routine rebalances within pre-approved parameters); (2) Advisory - the agent proposes 
a decision and proceeds after a configurable waiting period (4-24 hours) unless the advisor 
objects (for medium-risk rebalances); (3) Approval Required - the agent proposes a decision and 
waits indefinitely for explicit advisor approval before proceeding (for high-risk or unusual 
rebalances); (4) Escalation - the agent flags a situation it cannot resolve autonomously and 
requests human intervention with a detailed briefing (for edge cases, conflicting constraints, or 
novel scenarios outside training distribution). 
The escalation threshold matrix determines which intervention level applies based on the 
intersection of two dimensions: trade impact (measured as a percentage of portfolio value being 
traded) and decision confidence (the agent's self-assessed confidence in its recommendation, 
derived from the spread between the recommended action and the next-best alternative). Low 
trade impact with high confidence triggers Informational mode. High trade impact with low 
confidence triggers Approval Required mode. Any decision involving a compliance exception, 
client restriction override, or novel trigger type defaults to Escalation mode. 
Every human override is captured in the audit trail with: the original agent recommendation, the 
human's modified recommendation, the human's stated reason for the override (free-text with 
suggested categories: 'Client instruction,' 'Market judgment,' 'Compliance concern,' 'Error in 
agent analysis'), the timestamp and identity of the overriding human, and the outcome of the 
overridden decision (tracked retrospectively to evaluate override quality). Override data feeds 
into the agent's learning system, enabling it to adjust its decision boundaries and escalation 
thresholds over time. 
The Explainability Audit is a formal review process conducted quarterly by the Portfolio Review 
Committee. The audit samples 100 rebalancing decisions (stratified by trigger type, risk 
category, and intervention level), evaluates the quality of explanations at all three audience 
levels, checks for systematic biases in the agent's decision-making (e.g., consistently 
over-rebalancing one risk category, or systematically under-estimating transaction costs), and 
produces a Committee Report Card that feeds into the agent's performance evaluation dashboard. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 29 


