 
 
 
 
 
PART A: TRAINING MATERIAL & LEARNING RESOURCES 
 
SECTION A1: PORTFOLIO MANAGEMENT FUNDAMENTALS 
A1.1 Modern Portfolio Theory And Asset Allocation 
Modern Portfolio Theory (MPT), introduced by Harry Markowitz in 1952, remains the 
foundational framework upon which virtually all institutional portfolio management is built. The 
central insight of MPT is deceptively simple yet profoundly powerful: investors can construct 
portfolios that maximise expected return for a given level of risk, or equivalently, minimise risk 
for a given expected return, by carefully selecting the proportions of various assets. This set of 
optimal portfolios forms the Efficient Frontier - a curve in risk-return space that represents the 
best achievable trade-offs between volatility and return. 
In practice, constructing an efficient portfolio requires three critical inputs: the expected return of 
each asset class, the standard deviation (volatility) of each asset class, and the correlation matrix 
describing how asset returns co-move. The expected return of a portfolio is a weighted average 
of individual asset returns, expressed mathematically as E(Rp) = Sigma(wi * E(Ri)), where wi 
represents the portfolio weight of asset i. Portfolio variance, however, is not simply a weighted 
average of individual variances - it incorporates the covariance structure, expressed as Var(Rp) = 
Sigma(Sigma(wi * wj * Cov(Ri, Rj))). This non-linear relationship between portfolio weights 
and portfolio risk is precisely what enables diversification to reduce overall portfolio volatility 
below the weighted average of individual asset volatilities. 
Strategic Asset Allocation (SAA) represents the long-term, policy-driven allocation across major 
asset classes - equities, fixed income, alternatives, cash - determined by the investor's risk 
tolerance, investment horizon, liquidity needs, and return objectives. SAA typically accounts for 
85-95% of long-term portfolio return variation, as demonstrated by the landmark studies of 
Brinson, 
Hood, and Beebower (1986). Tactical Asset Allocation (TAA) involves 
short-to-medium term deviations from SAA to exploit perceived market mispricings or regime 
changes. The tension between maintaining disciplined SAA and implementing opportunistic 
TAA is one of the central challenges that an autonomous rebalancing agent must navigate. 
The Capital Asset Pricing Model (CAPM) extends MPT by introducing the concept of a risk-free 
asset, enabling the construction of the Capital Market Line (CML) and the identification of the 
Market Portfolio as the single optimal risky portfolio. Under CAPM, the expected return of any 
asset is determined by its beta - its sensitivity to the market portfolio - expressed as E(Ri) = Rf + 
Beta_i * (E(Rm) - Rf). While CAPM has known limitations (single-factor, assumes 
homogeneous expectations), it provides the conceptual foundation for understanding systematic 
versus idiosyncratic risk, and for evaluating whether an asset is overpriced or underpriced 
relative to its risk contribution. 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 3 


 
 
 
 
 
Multi-factor models, including the Fama-French Three-Factor Model (adding size and value 
factors) and the more recent Five-Factor Model (adding profitability and investment factors), 
provide a richer framework for understanding return drivers. The Arbitrage Pricing Theory 
(APT) generalises this further, allowing for multiple systematic risk factors without specifying 
what they are. An autonomous rebalancing agent must be cognisant of these factor exposures 
when making allocation decisions, as seemingly diversified portfolios may harbour concentrated 
factor bets that expose the portfolio to correlated drawdowns during factor rotation events. 
A1.2 Risk Measurement And Management Frameworks 
Risk measurement in portfolio management operates across multiple dimensions: market risk 
(price movements), credit risk (counterparty default), liquidity risk (inability to execute at fair 
prices), operational risk (system or process failures), and model risk (errors in quantitative 
models). Each dimension requires distinct measurement methodologies and contributes 
differently to overall portfolio risk. 
Value at Risk (VaR) quantifies the maximum expected loss over a specified time horizon at a 
given confidence level. A 1-day 95% VaR of INR 10 lakhs means that, under normal market 
conditions, the portfolio is expected to lose no more than INR 10 lakhs on 95% of trading days. 
Three primary methodologies exist for VaR calculation: the Historical Simulation method, which 
uses actual historical returns without distributional assumptions; the Variance-Covariance 
(Parametric) method, which assumes returns follow a normal or Student-t distribution; and the 
Monte Carlo Simulation method, which generates thousands of simulated return paths using 
statistical models of asset dynamics. 
Conditional Value at Risk (CVaR), also known as Expected Shortfall, addresses a critical 
limitation of VaR: it answers 'Given that losses exceed VaR, what is the expected loss?' CVaR is 
a coherent risk measure (satisfying sub-additivity, monotonicity, positive homogeneity, and 
translation invariance), making it mathematically superior to VaR for portfolio optimisation. 
Maximum Drawdown (MDD) measures the largest peak-to-trough decline in portfolio value, 
capturing the worst cumulative loss experience - a metric that resonates deeply with actual 
investor psychology. The Ulcer Index extends this by measuring the depth and duration of 
drawdowns, providing a more comprehensive view of 'pain' experienced by the portfolio holder. 
The Sharpe Ratio, defined as (Rp - Rf) / Sigma_p, remains the most widely used risk-adjusted 
return measure, quantifying the excess return earned per unit of total risk. The Sortino Ratio 
improves upon this by penalising only downside deviation, recognising that investors are 
primarily concerned with negative volatility. The Information Ratio measures active return 
(alpha) per unit of tracking error, evaluating the consistency of active management decisions. 
The Calmar Ratio divides annualised return by maximum drawdown, providing a return-to-pain 
ratio that is particularly relevant for evaluating rebalancing strategies over multi-year periods. 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 4 


 
 
 
 
 
Stress testing and scenario analysis complement statistical risk measures by examining portfolio 
behaviour under extreme but plausible scenarios - historical crises (2008 Global Financial Crisis, 
2020 COVID crash, 2022 rate shock), hypothetical scenarios (sudden 200 basis point rate hike, 
30% equity correction with flight-to-quality, emerging market contagion), and reverse stress tests 
(what combination of market moves would cause a specified loss). An autonomous rebalancing 
agent must incorporate these dimensions to avoid the trap of optimising for normal conditions 
while remaining blind to tail risks. 
A1.3 Transaction Costs, Tax Implications And Liquidity Constraints 
Transaction costs in portfolio management are multifaceted and often underestimated. Explicit 
costs include brokerage commissions, exchange fees, stamp duties (Securities Transaction Tax in 
India at 0.1% on equity delivery), regulatory fees, and custody charges. Implicit costs encompass 
the bid-ask spread (the immediate cost of executing at market), market impact (the price 
movement caused by the trade itself, particularly for large orders), and opportunity cost (the 
return foregone while waiting to execute). For institutional portfolios, market impact often 
dominates, following a square-root model: Impact is approximately proportional to Sigma * 
sqrt(V_trade / V_daily), where Sigma is daily volatility and V represents volume measures. 
Tax implications profoundly affect rebalancing decisions. In the Indian context, short-term 
capital gains (STCG) on equity held less than 12 months are taxed at 20% (post-Union Budget 
2024-25), while long-term capital gains (LTCG) on equity exceeding INR 1.25 lakhs per annum 
are taxed at 12.5%. Debt instruments face STCG at the applicable income tax slab rate and 
LTCG at 12.5% without indexation benefit for instruments acquired after April 2023. An 
intelligent rebalancing agent must conduct tax-lot-level analysis, implementing strategies such as 
tax-loss harvesting (realising losses to offset gains), gain deferral (delaying sales of appreciated 
positions), and asset location optimisation (placing tax-inefficient assets in tax-advantaged 
accounts where applicable). 
Liquidity constraints impose hard boundaries on rebalancing execution. An asset may be 
theoretically mispriced but practically untradeable at desired sizes. Liquidity is measured across 
multiple dimensions: market depth (order book thickness), bid-ask spread (tightness), trading 
volume (activity), and resilience (speed of price recovery after large trades). In the Indian 
market, large-cap NSE stocks typically exhibit spreads of 2-5 basis points with daily volumes 
supporting trades up to INR 50 crores with minimal impact, while mid-cap stocks may show 
spreads of 10-30 basis points with meaningful impact above INR 5 crores. Corporate bonds and 
structured products may have even more severe liquidity constraints. The rebalancing agent must 
model these constraints as hard limits in its optimisation, potentially implementing trades over 
multiple days using time-weighted average price (TWAP) or volume-weighted average price 
(VWAP) algorithms. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 5 


 
 
 
 
 
SECTION A2: PORTFOLIO REBALANCING THEORY AND PRACTICE 
A2.1 Rebalancing Philosophies And Approaches 
Portfolio rebalancing is the disciplined process of realigning portfolio weights back to target 
allocations after market movements cause drift. Three fundamental rebalancing philosophies 
dominate 
practice: 
calendar-based 
rebalancing, 
threshold-based 
rebalancing, 
and 
optimisation-based rebalancing, each with distinct trade-offs between tracking precision, 
transaction costs, and implementation complexity. 
Calendar-based rebalancing triggers portfolio adjustments at fixed intervals - monthly, quarterly, 
semi-annually, or annually - regardless of how far the portfolio has drifted from targets. This 
approach is simple to implement, produces predictable trading patterns, and is easy to audit and 
explain to clients. However, it is insensitive to market conditions: it rebalances unnecessarily 
when drift is trivial (incurring costs without benefit) and fails to rebalance quickly enough during 
volatile periods when drift is extreme. Empirical studies across US and Indian equity markets 
suggest that quarterly rebalancing captures approximately 80-85% of the risk-reduction benefit 
of continuous rebalancing, while annual rebalancing captures approximately 60-70%. 
Threshold-based rebalancing triggers trades when any asset class deviates from its target weight 
by more than a predetermined band - typically 1-5 percentage points for equities and 0.5-2 
percentage points for fixed income, depending on the asset's volatility and transaction cost 
profile. This approach is inherently adaptive: it rebalances more frequently during volatile 
markets (when drift is rapid) and less frequently during calm markets (when drift is slow). The 
key design decisions are the band width (narrower bands mean tighter tracking but higher costs) 
and whether bands are absolute (e.g., plus/minus 3%) or relative (e.g., plus/minus 20% of the 
target weight). Optimal band width depends on the interaction between expected return 
differences, covariance structure, and transaction costs - a problem first formalised by Leland 
(1999) and extended by Masters (2003). 
Event-driven rebalancing responds to specific triggers beyond routine drift: significant market 
events (index drops exceeding 5% in a single session), client life events (retirement, inheritance, 
divorce), regulatory changes (tax law modifications, new investment restrictions), rating 
migrations (credit downgrade of a held bond), or corporate actions (mergers, spin-offs, 
delistings). This category also encompasses tactical rebalancing, where the agent adjusts 
allocations in response to changing macroeconomic regimes - shifting from overweight equities 
to overweight bonds when leading indicators signal recession, for example. 
Optimisation-based rebalancing treats every rebalancing decision as a constrained optimisation 
problem: minimise expected tracking error (or maximise expected utility) subject to transaction 
cost budgets, tax constraints, liquidity limits, and sector/issuer concentration caps. This 
approach, while theoretically optimal, requires robust optimisation infrastructure and careful 
handling of estimation error in input parameters. Mean-Variance Optimisation (MVO) is the 
classical framework, but practitioners increasingly use robust optimisation techniques (shrinkage 
estimators, resampled efficiency, Black-Litterman model) to mitigate sensitivity to input errors. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 6 


 
 
 
 
 
A2.2 Drift Measurement And Monitoring 
Portfolio drift is the divergence between current portfolio weights and target weights, arising 
from differential asset returns. Several drift metrics serve different purposes. Absolute Drift for 
each asset class is simply: Drift_i = w_actual_i - w_target_i. The Sum of Absolute Drift (SAD) 
aggregates this across the portfolio: SAD = Sigma(|Drift_i|). A SAD of 10% means that 5% of 
the portfolio needs to be sold and 5% needs to be bought to restore target weights (since sells and 
buys must balance). The Root Mean Square Drift (RMSD) provides a volatility-weighted 
measure: RMSD = sqrt(Sigma(Drift_i^2) / n), giving greater weight to large deviations. 
Tracking error, defined as the standard deviation of the difference between portfolio returns and 
benchmark returns, provides an ex-post measure of how closely the portfolio follows its target. 
Predicted (ex-ante) tracking error uses the covariance matrix to estimate future tracking error 
given current drift: TE = sqrt(d' * Cov * d), where d is the vector of drift values. This 
forward-looking measure is particularly useful for the rebalancing agent because it accounts for 
the correlation structure - concentrated drift in highly correlated assets may produce less tracking 
error than diversified drift across uncorrelated assets. 
Continuous monitoring requires a robust data pipeline. The agent must ingest real-time or 
near-real-time portfolio holdings data, market prices for all held securities, reference data (index 
compositions, corporate actions, ex-dividend dates), and client account attributes (risk category, 
tax status, restriction lists). For a firm managing 50,000 portfolios across 5 risk categories, this 
monitoring system must process millions of data points daily, flag portfolios requiring attention, 
and prioritise them based on drift severity, client sensitivity, and market conditions. 
A2.3 Trade List Generation With Constraint Handling 
Generating an executable trade list from a rebalancing decision involves translating target weight 
changes into specific security-level orders while respecting a complex web of constraints. The 
process begins with the portfolio-level rebalancing decision (increase equity by 3%, decrease 
bonds by 3%) and drills down through asset class, sub-asset class, and individual security 
selection. 
Hard constraints are inviolable: regulatory limits (SEBI mutual fund concentration limits of 10% 
per issuer for diversified equity funds), client-specific restrictions (ethical screens, excluded 
sectors, restricted securities lists), minimum lot sizes (derivatives contracts, bond minimum 
denominations), and account-level constraints (margin requirements, cash reserve minimums). 
Soft constraints are optimisation targets that can be violated at a penalty: sector deviation limits, 
tracking error targets, factor exposure targets, and turnover budgets. The optimisation problem is 
typically formulated as a Quadratic Programming (QP) problem with linear constraints, solvable 
using interior-point methods or active-set methods. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 7 


 
 
 
 
 
Wash-sale rules (or the Indian equivalent - the concept of 'speculative transactions' and 
'same-security' rules for tax-loss harvesting) must be incorporated to prevent the agent from 
selling a security at a loss and immediately repurchasing it. The agent must maintain a wash-sale 
calendar, track substantially identical securities, and implement substitution logic - for example, 
selling Nifty 50 ETF at a loss and simultaneously purchasing Nifty Next 50 ETF to maintain 
similar market exposure while observing the 30-day wash-sale window applicable in several 
jurisdictions. 
Round-lot optimization is critical for practical implementation. A theoretically optimal trade of 
147.3 shares must be rounded to a tradeable quantity, and this rounding must be performed 
jointly across all trades in the portfolio to ensure that the net cash impact remains within 
acceptable bounds. For accounts with small balances, rounding errors can introduce meaningful 
tracking error, requiring the agent to prioritise which trades to round up versus down based on 
marginal impact on the objective function. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 8 


 
 
 
 
 
SECTION A3: AGENTIC AI ARCHITECTURE FOR FINANCE 
A3.1 Foundations Of AI Agents And Multi-Agent Systems 
An AI agent, in the context of autonomous financial systems, is a software entity that perceives 
its environment through sensors (data feeds), reasons about the perceived state using an internal 
model (decision engine), and acts upon the environment through effectors (order execution, 
report generation). The defining characteristic of an agent, as distinguished from a simple 
automated script, is its capacity for autonomous decision-making under uncertainty - the ability 
to evaluate multiple possible actions, anticipate their consequences, and select the action that 
best satisfies its objectives given incomplete and evolving information. 
The Belief-Desire-Intention (BDI) architecture provides a natural framework for financial 
agents. Beliefs represent the agent's current understanding of the world (portfolio state, market 
conditions, client preferences). Desires represent the agent's objectives (maintain target 
allocation, minimise tracking error, optimise tax efficiency). Intentions represent the agent's 
committed plans of action (specific trade lists, scheduled reviews, pending explanations). The 
BDI framework naturally accommodates the kind of deliberative reasoning required in portfolio 
management, where the agent must balance competing objectives and update its plans as new 
information arrives. 
Multi-agent systems (MAS) enable the decomposition of complex portfolio management tasks 
into specialised agent roles. A Portfolio Monitoring Agent continuously tracks drift and flags 
portfolios requiring attention. A Market Analysis Agent processes market data, news sentiment, 
and macroeconomic indicators to identify regime changes or event-driven triggers. A Trade 
Generation Agent formulates optimal trade lists given constraints. An Explanation Agent 
translates decisions into human-readable narratives at multiple abstraction levels. A Compliance 
Agent validates every proposed action against regulatory rules and client restrictions. An 
Orchestrator Agent coordinates the workflow, manages conflicts between agents, and escalates 
decisions requiring human intervention. 
Communication between agents follows the Agent Communication Language (ACL) paradigm, 
with standardised message types: inform (sharing beliefs), request (asking for action), propose 
(suggesting a course of action), accept/reject (responding to proposals), and escalate (flagging 
issues for human review). In a LangChain or CrewAI implementation, these communication 
patterns are realised through structured tool calls, shared memory stores, and event-driven 
orchestration pipelines. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 9 


 
 
 
 
 
A3.2 LangChain And CrewAI Frameworks For Financial Agents 
LangChain provides the foundational toolkit for building LLM-powered agents with tool-use 
capabilities. The core abstraction is the Agent, which combines an LLM (for reasoning), a set of 
Tools (for interacting with external systems), and a Memory (for maintaining conversation and 
decision context). For the portfolio rebalancing use case, Tools include: portfolio data retrieval 
(querying holdings databases), market data access (fetching real-time and historical prices), 
optimisation solvers (invoking mean-variance or Black-Litterman optimisers), compliance 
checkers (validating proposed trades against rule engines), and report generators (producing 
formatted explanations). 
LangChain's ReAct (Reasoning and Acting) pattern is particularly well-suited for rebalancing 
decisions. The agent iterates through a loop of: Thought (reasoning about the current portfolio 
state and what action to take), Action (invoking a tool to gather data or compute a result), and 
Observation (processing the tool's output). For example: Thought - 'Portfolio XYZ has drifted 
4.2% in equity allocation, exceeding the 3% threshold. I need to check current market conditions 
before proposing trades.' Action - 'Call market_data_tool to fetch current VIX, recent sector 
performance, and liquidity scores.' Observation - 'VIX at 22 (elevated), technology sector down 
8% this week, liquidity scores normal for large caps.' Thought - 'Given elevated volatility, I 
should implement the rebalance in two tranches to minimise market impact.' 
CrewAI extends this pattern to multi-agent orchestration, defining Crews of specialised Agents 
with distinct roles, backstories, and goals. Each Agent in the Crew can be assigned specific Tasks 
and can delegate sub-tasks to other Agents. For the rebalancing system, a natural Crew structure 
assigns: a Senior Portfolio Analyst (monitors drift and proposes rebalancing actions), a Risk 
Manager (evaluates proposed trades for risk implications), a Tax Specialist (optimises trade 
execution for tax efficiency), a Compliance Officer (validates regulatory adherence), and an 
Explanation Writer (generates human-readable justifications). The Crew's Process (sequential or 
hierarchical) determines how these agents coordinate. 
A3.3 Agentic Workflow Patterns For Portfolio Management 
The Autonomous Rebalancing Agent employs several standard agentic workflow patterns, each 
suited to different aspects of the decision process. The Reflection Pattern is used for 
self-evaluation: after generating a trade list, the agent reviews its own output against quality 
criteria (Does the proposed trade list satisfy all hard constraints? Is the expected tracking error 
reduction proportional to the transaction costs incurred? Are the explanations clear and 
complete?) and iterates if deficiencies are found. 
The Planning Pattern decomposes complex rebalancing tasks into structured sub-goals. When a 
market crash triggers event-driven rebalancing across thousands of portfolios simultaneously, the 
agent cannot process them all in parallel with equal priority. It must plan: (1) Identify portfolios 
with the most severe drift, (2) Among those, prioritise portfolios with upcoming client reviews or 
cash withdrawals, (3) Group portfolios by similar rebalancing needs to achieve block-trading 
efficiencies, (4) Sequence execution to minimise aggregate market impact, (5) Generate 
explanations in batch where rebalancing rationale is identical. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 10 


 
 
 
 
 
The Tool-Use Pattern enables the agent to invoke external capabilities: calling optimisation 
APIs, querying compliance databases, fetching tax-lot information, and generating visualisations. 
The Human-in-the-Loop Pattern is critical for high-stakes decisions: when the agent's proposed 
rebalancing involves selling more than a specified threshold (e.g., 20% of portfolio value in a 
single session), or when the client has a 'prior approval required' flag, the agent pauses, presents 
its recommendation with full explanations, and awaits human approval before proceeding. This 
pattern preserves the efficiency of automation while maintaining the safety of human oversight. 
The Memory Pattern maintains both short-term working memory (current session's decisions, 
pending trades, active conversations) and long-term episodic memory (past rebalancing decisions 
for each portfolio, outcomes of previous recommendations, client feedback history). Long-term 
memory enables the agent to learn from experience - for example, recognising that a particular 
client consistently overrides recommendations to reduce equity exposure, and proactively 
adjusting future recommendations to align with revealed preferences. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 11 


 
 
 
 
 
SECTION A4: EXPLAINABLE AI (XAI) FOR FINANCIAL DECISIONS 
A4.1 The Explainability Imperative In Wealth Management 
Explainable AI (XAI) in financial services is not merely a desirable feature - it is a regulatory 
necessity 
and 
a 
commercial 
imperative. 
SEBI's 
circular 
on 
algorithmic 
trading 
(SEBI/HO/MRD/DOP1/CIR/P/2024/69) requires that all automated trading decisions be 
auditable and explainable. The European Union's AI Act classifies financial AI systems as 
'high-risk,' mandating transparency, human oversight, and the ability to provide meaningful 
explanations to affected individuals. MiFID II's suitability requirements demand that investment 
recommendations be accompanied by clear rationale demonstrating alignment with the client's 
investment objectives, risk tolerance, and financial situation. 
Beyond regulatory compliance, explainability drives client trust and adoption. Research by 
Vanguard (2023) found that 73% of investors are more likely to follow investment 
recommendations when they understand the reasoning behind them. Conversely, unexplained 
recommendations - even if objectively superior - face rejection rates 2-3 times higher than 
explained recommendations. The 'explainability premium' is real and measurable: advisors who 
provide clear explanations of rebalancing decisions experience 40% lower client attrition rates 
compared to those who do not. 
The 'black box' problem in AI-driven portfolio management manifests at three levels. At the 
model level, complex optimisation algorithms produce allocations that may be mathematically 
optimal but intuitively counter-intuitive (e.g., recommending increased equity allocation during a 
market downturn because mean reversion signals dominate). At the data level, the agent may 
incorporate alternative data sources (sentiment, satellite imagery, web traffic) whose influence on 
the decision is opaque. At the system level, the interaction between multiple agents, each with 
their own reasoning process, creates emergent behaviours that no single agent's explanation can 
fully capture. 
A4.2 SHAP, LIME And Feature Attribution Methods 
SHAP (SHapley Additive exPlanations) values, rooted in cooperative game theory, provide a 
principled method for attributing model outputs to input features. For a portfolio rebalancing 
model, SHAP values answer the question: 'How much did each factor (equity drift magnitude, 
VIX level, client risk score, days since last rebalance, tax lot status) contribute to the decision to 
rebalance this portfolio today?' The theoretical foundation is the Shapley value, which distributes 
the total 'payout' (the rebalancing decision score) among all 'players' (input features) based on 
their marginal contributions across all possible coalitions. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 12 


 
 
 
 
 
In practice, Tree SHAP provides exact Shapley values for tree-based models (Random Forests, 
XGBoost, LightGBM) in polynomial time, making it computationally feasible for real-time 
explanation generation. Kernel SHAP provides model-agnostic approximate Shapley values for 
any black-box model, at higher computational cost. For the rebalancing agent, SHAP values can 
be visualised as waterfall charts showing how each factor pushes the rebalancing probability 
above or below the base rate, summary plots showing feature importance across many portfolios, 
and dependency plots revealing non-linear interactions between features. 
LIME (Local Interpretable Model-agnostic Explanations) takes a complementary approach: it 
approximates the behaviour of a complex model in the local neighbourhood of a specific 
prediction using a simple, interpretable model (typically a linear model or decision tree). For a 
particular portfolio's rebalancing decision, LIME would identify: 'The three factors most 
influential in this specific decision were: (1) equity allocation drifted 4.7% above target, (2) 
recent market volatility increased the predicted tracking error to 2.1%, and (3) the client's risk 
category is Conservative, which has a tighter rebalancing threshold.' Unlike SHAP, LIME does 
not guarantee global consistency, but it produces intuitive, locally faithful explanations that are 
well-suited for client-facing communications. 
Counterfactual explanations answer 'What would need to be different for the decision to change?' 
For example: 'If the equity drift were below 2.8% (instead of the current 4.7%), the agent would 
not have triggered a rebalance.' This form of explanation is particularly powerful for compliance 
officers who need to understand decision boundaries, and for clients who want to understand 
under what conditions the agent would have recommended a different course of action. 
Implementing counterfactual explanation generation requires maintaining a model of the 
decision boundary and searching for the minimal perturbation that crosses it - a constrained 
optimisation problem itself. 
A4.3 Multi-Audience Explanation Generation 
The rebalancing agent must generate explanations at three distinct levels of abstraction, each 
tailored to a specific audience with different information needs, technical literacy, and 
decision-making roles. 
Client Level (Investor): Plain-language explanation focusing on what is being done, why it 
matters for the client's goals, and what the expected impact is. No jargon, no formulas, no 
reference to technical concepts. Example: 'Your portfolio has gradually shifted towards stocks 
over the past quarter as stock prices rose. We are selling some stock positions and buying bonds 
to bring your portfolio back to the balance that matches your moderate risk comfort level. This 
adjustment helps protect your portfolio from being too exposed to a potential stock market 
decline, keeping you on track for your retirement goal in 2035. The estimated cost of these trades 
is approximately INR 2,400, which we believe is well justified by the risk reduction achieved.' 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 13 


 
 
 
 
 
Advisor Level (Financial Advisor): Technical but accessible explanation including specific 
allocation changes, drift magnitudes, key metrics, and decision rationale. Example: 'Portfolio 
ALPHA-7792 triggered threshold-based rebalancing: equity allocation drifted to 67.3% versus 
60% target (drift: +7.3%, exceeding 5% band). Proposed trades reduce equity by 7.3% and 
increase fixed income by 5.1% and cash by 2.2%. Key driver: technology sector rally 
concentrated equity gains in IT stocks, increasing sector concentration to 28% (limit: 25%). 
Expected tracking error reduction from 2.8% to 0.4%. Transaction cost estimate: 12 bps. Tax 
impact: STCG of INR 45,000 offset by harvested LTCL of INR 38,000. Net tax-adjusted 
rebalancing benefit: positive.' 
Compliance Level (Regulatory And Audit): Full decision audit trail including model inputs, 
constraint satisfaction verification, regulatory rule checks, and exception handling. Example: 
'Decision ID: REB-2026-03-1847. Trigger: Threshold breach on asset class EQUITY at 
T=2026-03-15T09:30:00Z. Pre-trade compliance check: PASSED - all proposed trades satisfy 
SEBI concentration limits (Reg 44(1)), client restriction list (0 conflicts), minimum holding 
period requirements (all lots exceed 365 days), and suitability score threshold (client risk score: 
4, proposed portfolio risk score: 3.8). SHAP attribution: equity_drift (0.47), vix_level (0.18), 
days_since_rebalance 
(0.12), 
tax_lot_maturity 
(0.11), 
client_risk_category 
(0.08), 
sector_concentration (0.04). Counterfactual: decision boundary at equity_drift = 4.2%. Override 
history: none. Explanation generation model: GPT-4-Turbo via LangChain, temperature 0.1.' 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 14 


 
 
 
 
 
SECTION A5: REGULATORY AND COMPLIANCE FRAMEWORK 
A5.1 SEBI Regulations Applicable To Automated Portfolio Management 
The Securities and Exchange Board of India (SEBI) has established a comprehensive regulatory 
framework that governs automated portfolio management and algorithmic decision-making. 
SEBI (Portfolio Managers) Regulations, 2020 mandate that portfolio managers maintain detailed 
records of all investment decisions, including the rationale for each transaction, the research 
basis, and the client suitability assessment. Regulation 22 specifically requires that portfolio 
managers act in a fiduciary capacity, ensuring that every investment decision serves the client's 
best interest - a requirement that applies equally to AI-driven and human-driven decisions. 
SEBI's framework for algorithmic trading (Circular SEBI/HO/MRD/DOP1/CIR/P/2024/69 and 
subsequent amendments) requires: pre-trade risk controls (order-level limits, position limits, 
price band checks), real-time monitoring of algorithmic orders, kill-switch functionality to halt 
all automated trading in emergencies, and comprehensive audit trails of all algorithmic decisions. 
While these regulations primarily target high-frequency trading, their principles of transparency, 
controllability, and auditability apply directly to autonomous rebalancing agents. 
The Investment Advisers Regulations, 2013 (as amended) establish suitability obligations 
requiring that investment advice be appropriate to the client's financial situation, investment 
objectives, and risk tolerance. An autonomous rebalancing agent providing recommendations 
must demonstrate compliance with these suitability requirements for every recommendation 
generated. This creates a direct linkage between the agent's decision-making process and the 
explanation generation system: the agent must not only make the right decision but also prove 
that it made the right decision for the right reasons. 
Data protection requirements under the Digital Personal Data Protection Act, 2023 (DPDP Act) 
impose additional obligations on autonomous agents processing investor data. The agent must 
implement data minimisation (processing only data necessary for the rebalancing decision), 
purpose limitation (using data only for the stated purpose of portfolio management), storage 
limitation (retaining decision data only for the regulatory mandated period), and individual rights 
(enabling investors to access, correct, and port their data). These requirements influence the 
agent's architecture, particularly its memory and logging systems. 
A5.2 Global Regulatory Perspectives 
The European Union's Markets in Financial Instruments Directive II (MiFID II) and the AI Act 
together create the most comprehensive regulatory framework for AI-driven financial services. 
MiFID II's suitability requirements (Article 25) mandate that firms assess whether a 
recommended transaction is suitable for the client, considering their knowledge, experience, 
financial situation, and investment objectives. The EU AI Act classifies AI systems used for 
creditworthiness assessment and investment recommendation as 'high-risk,' requiring conformity 
assessments, technical documentation, human oversight, and transparency obligations. 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 15 


 
 
 
 
 
The United States regulatory landscape is fragmented across multiple agencies. The SEC's 
Regulation Best Interest (Reg BI) requires broker-dealers to act in the client's best interest when 
making recommendations, with specific disclosure, care, conflict of interest, and compliance 
obligations. The Investment Advisers Act of 1940 imposes fiduciary duties on registered 
investment advisers. The SEC has issued guidance on robo-advisors (IM Guidance Update 
2017-02) emphasising the importance of adequate disclosure, effective questionnaire design, and 
appropriate oversight of automated investment advice. FINRA's algorithmic trading supervision 
requirements add further layers of control and monitoring obligations. 
These global regulatory frameworks converge on several common themes that the autonomous 
rebalancing agent must address: transparency (the ability to explain decisions), fairness 
(non-discriminatory treatment of clients), accountability (clear allocation of responsibility for 
automated decisions), contestability (the right of affected parties to challenge decisions), and 
human oversight (the ability of qualified humans to monitor, intervene, and override automated 
decisions). The agent's architecture must be designed to satisfy these requirements by 
construction, not as an afterthought. 
 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 16 


 
 
 
 
 
SECTION A6: BEHAVIOURAL FINANCE AND INVESTOR PSYCHOLOGY IN 
REBALANCING 
A6.1 Cognitive Biases Affecting Rebalancing Decisions 
Understanding behavioural finance is critical for the autonomous rebalancing agent - not because 
the agent itself is subject to cognitive biases, but because the investors and advisors it serves 
certainly are. The agent must anticipate, accommodate, and sometimes gently counteract these 
biases in its explanation generation and override handling. Loss aversion, the most extensively 
documented bias in financial decision-making (Kahneman and Tversky, 1979), causes investors 
to feel the pain of losses approximately 2.0-2.5 times more intensely than the pleasure of 
equivalent gains. In a rebalancing context, this manifests as resistance to selling winning 
positions ('why would you sell something that is going up?') and reluctance to buy declining 
positions ('you want me to throw more money at a losing investment?'). The agent's client-level 
explanations must directly address this bias, reframing rebalancing not as 'selling winners and 
buying losers' but as 'maintaining the risk level you chose for your goals.' 
The disposition effect - the tendency to sell winners too early and hold losers too long - directly 
conflicts with disciplined rebalancing. Investors who exhibit strong disposition effect may 
override the agent's recommendations to sell appreciated positions, or conversely, may eagerly 
approve selling underperformers even when the agent recommends holding them for tax or 
diversification reasons. The agent's override system should track disposition-effect-consistent 
overrides and, over time, adjust its explanation strategy to proactively address this bias before the 
investor encounters the decision. 
Status quo bias and inertia cause investors to prefer no action over action, even when action is 
objectively beneficial. This is particularly problematic for rebalancing, which always requires 
trades (and therefore effort, cost, and the possibility of regret). The agent should quantify the 
'cost of inaction' - the expected deterioration in risk-adjusted returns from failing to rebalance - 
and present this to the investor alongside the cost of rebalancing, making the comparison 
tangible. For example: 'Not rebalancing today is expected to increase your portfolio risk by 15% 
over the next quarter, equivalent to being in a risk category one level above what you selected.' 
Recency bias leads investors to overweight recent experience when forming expectations. After a 
prolonged equity bull market, investors perceive equities as 'safe' and resist selling them; after a 
crash, they perceive equities as 'dangerous' and resist buying them. In both cases, the rebalancing 
agent's recommendation contradicts the investor's intuition. The agent's explanations should 
include historical context: 'In the 12 months following the 5 worst equity declines in Nifty 50 
history, investors who rebalanced earned an average of 35% more than those who did not.' This 
evidence-based framing leverages the same recency bias (recent historical data) in service of the 
correct action. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 17 


 
 
 
 
 
Anchoring causes investors to fixate on arbitrary reference points - particularly purchase prices - 
when evaluating current positions. An investor who purchased a stock at INR 500 may resist 
selling it at INR 480 (a small loss) but eagerly sell at INR 520 (a small gain), regardless of 
whether the stock's current valuation and risk profile warrant holding or selling. The agent's tax 
optimisation module interacts with anchoring: by presenting trades in terms of tax impact rather 
than gain/loss relative to purchase price, the agent can defuse anchoring-driven resistance. 
A6.2 Prospect Theory And Framing Effects In Explanation Design 
Prospect Theory (Kahneman and Tversky, 1979) provides the theoretical foundation for 
understanding how investors evaluate rebalancing outcomes. The theory's four key insights have 
direct implications for explanation design. First, people evaluate outcomes as gains and losses 
relative to a reference point, not in terms of final wealth states - the agent must carefully choose 
its reference point when framing rebalancing outcomes (relative to current allocation? relative to 
target allocation? relative to a peer benchmark?). Second, the value function is concave for gains 
and convex for losses, with steeper slope for losses - the agent should present gains and losses 
separately rather than netting them, as the psychological impact differs. Third, people overweight 
small probabilities and underweight large probabilities - the agent should present tail risk 
probabilities carefully, neither dismissing them nor amplifying fear. 
Framing effects dictate that the same rebalancing decision can be perceived as attractive or 
unattractive depending on how it is presented. A rebalance that reduces equity from 67% to 60% 
can be framed as: (a) 'We are reducing your equity exposure by 7 percentage points' (loss frame - 
triggers loss aversion), (b) 'We are restoring your target balance of 60% equity' (restoration frame 
- triggers status quo preference), (c) 'We are locking in a 12% equity gain from the past quarter' 
(gain frame - triggers gain realisation satisfaction), or (d) 'We are reducing your downside risk by 
an estimated 15%' (protection frame - triggers safety motivation). The agent's Explanation 
Generator should select the frame most likely to align with each client's motivational profile, 
which can be inferred from their risk questionnaire responses and override history. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 18 


 
 
 
 
 
SECTION A7: ADVANCED CONSTRAINT OPTIMISATION TECHNIQUES 
A7.1 Mathematical Formulation Of The Rebalancing Problem 
The portfolio rebalancing problem, when formulated rigorously, is a constrained quadratic 
programming (QP) problem. The standard formulation minimises the post-trade tracking error 
subject to a set of linear constraints. Let w_current denote the current portfolio weight vector, 
w_target the target weight vector, and w_trade the vector of trades (positive for buys, negative 
for sells). The objective is to find w_trade that minimises: (w_current + w_trade - w_target)' * 
Cov * (w_current + w_trade - w_target), where Cov is the covariance matrix of asset returns. 
This quadratic objective measures the expected tracking error variance of the rebalanced 
portfolio relative to the target. 
The constraint set includes: (1) Budget constraint - the net cash flow from trades must equal zero 
(or equal the known cash inflow/outflow): sum(w_trade * Price) = CashFlow. (2) Long-only 
constraint - no short selling is permitted: w_current + w_trade >= 0. (3) Turnover limit - the total 
value of trades must not exceed a specified fraction of portfolio value: sum(|w_trade|) <= 
TurnoverBudget. (4) Sector concentration - the post-trade allocation to any sector must not 
exceed the specified limit: sum(w_current_sector_j + w_trade_sector_j) <= SectorLimit_j for all 
sectors j. (5) Single-issuer limit - the post-trade allocation to any single issuer must not exceed 
the specified limit: w_current_i + w_trade_i <= IssuerLimit for all securities i. (6) Minimum 
trade size - any non-zero trade must exceed the minimum tradeable value: |w_trade_i| = 0 or 
|w_trade_i| >= MinTradeSize. 
The minimum trade size constraint introduces binary decision variables (trade or do not trade for 
each security), transforming the problem from a continuous QP into a Mixed-Integer Quadratic 
Programming (MIQP) problem, which is NP-hard in general. Practical approaches include: (a) 
solving the continuous relaxation first, then rounding small trades to zero; (b) using 
branch-and-bound methods for exact solutions (feasible for portfolios with fewer than 100 
securities); (c) applying heuristic methods such as greedy rounding or genetic algorithms for 
large portfolios. The choice between these approaches should be configurable in the agent's 
optimisation module, with the solver selection driven by portfolio size and latency requirements. 
Transaction cost modelling adds non-linearity to the optimisation. While fixed costs (brokerage 
commissions, STT) are linear in trade value, market impact costs follow a concave square-root 
model: Impact_i = k_i * Sigma_i * sqrt(|w_trade_i| / ADV_i), where k_i is an impact coefficient, 
Sigma_i is daily volatility, and ADV_i is average daily volume. This non-linear cost function can 
be approximated by piecewise-linear segments (enabling linear programming solutions) or 
handled directly by second-order cone programming (SOCP) solvers available in CVXPY. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 19 


 
 
 
 
 
A7.2 Robust Optimisation And Parameter Uncertainty 
Classical mean-variance optimisation is notoriously sensitive to estimation errors in expected 
returns and covariances. A small change in the expected return of a single asset can produce 
dramatically different optimal allocations - a phenomenon that undermines the reliability of any 
automated rebalancing system. Robust optimisation techniques address this sensitivity by 
explicitly modelling parameter uncertainty and optimising for the worst-case scenario within a 
defined uncertainty set. 
The Shrinkage Estimator approach (Ledoit and Wolf, 2003) improves covariance matrix 
estimation by shrinking the sample covariance matrix toward a structured target (such as the 
identity matrix or the single-factor model covariance). The optimal shrinkage intensity is 
determined analytically, producing a covariance estimate that is more stable and 
better-conditioned than the raw sample covariance. For the rebalancing agent, shrinkage 
covariance estimation should be the default approach, with the shrinkage intensity logged as part 
of the decision audit trail. 
The Black-Litterman Model (1992) provides a Bayesian framework for combining market 
equilibrium expected returns (derived from the CAPM and current market capitalisation weights) 
with investor views (expressed as expected excess returns for specific assets or portfolios). This 
approach produces more stable and intuitive allocation recommendations than pure MVO, and 
naturally accommodates the rebalancing agent's need to incorporate macroeconomic views (from 
the Market Analysis Agent) without abandoning the discipline of equilibrium-based allocation. 
Resampled Efficient Frontier (Michaud, 1998) addresses estimation error by: (1) generating 
multiple bootstrapped samples of the return distribution, (2) computing the efficient frontier for 
each sample, (3) averaging the optimal portfolios across all samples. The resulting 'resampled' 
portfolio is more robust to estimation error and exhibits lower turnover over time, as its weights 
are less sensitive to small changes in input parameters. For the backtesting framework, the agent 
should compare the performance of classical MVO, shrinkage-estimated MVO, Black-Litterman, 
and resampled efficient frontier approaches to identify the most suitable method for each risk 
category. 
 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 20 


