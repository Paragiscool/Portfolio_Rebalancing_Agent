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