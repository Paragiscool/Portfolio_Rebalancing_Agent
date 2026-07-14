import streamlit as st
import plotly.express as px
from src.dashboard.mock_data_generator import (
    get_portfolio_overview_data,
    get_rebalancing_activity_data,
    get_performance_backtest_data,
    get_system_health_data
)

st.set_page_config(page_title="Rebalancing Agent Dashboard", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Navigation")
view = st.sidebar.radio("Select View", [
    "Portfolio Overview", 
    "Rebalancing Activity", 
    "Performance Analytics", 
    "Explainability Centre", 
    "System Health"
])

st.title(f"{view}")

if view == "Portfolio Overview":
    st.markdown("### Aggregate Drift Heatmap")
    df = get_portfolio_overview_data()
    fig = px.density_heatmap(df, x="Asset Class", y="Risk Category", z="Avg Drift (%)", 
                             color_continuous_scale="RdYlGn", title="Average Drift by Risk Category and Asset Class")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Portfolios", "50,000")
    col2.metric("Portfolios > 5% Drift", "1,245", "+12")
    col3.metric("Critical Escapes", "3", "-2")

elif view == "Rebalancing Activity":
    st.markdown("### Recent AI Decisions")
    df = get_rebalancing_activity_data()
    st.dataframe(df, use_container_width=True)
    
    st.markdown("### Pending Approvals Queue")
    pending = df[df["Status"] == "Pending Approval"]
    if not pending.empty:
        st.warning(f"You have {len(pending)} portfolios awaiting human review.")
        st.dataframe(pending, use_container_width=True)
    else:
        st.success("All clear. No pending approvals.")

elif view == "Performance Analytics":
    st.markdown("### Agent Strategy vs Buy & Hold Benchmark")
    df = get_performance_backtest_data()
    st.line_chart(df)
    
    col1, col2 = st.columns(2)
    col1.metric("Agent Sharpe Ratio", "1.45")
    col2.metric("Buy & Hold Sharpe", "0.95")

elif view == "Explainability Centre":
    st.markdown("### Audit Trail & Explanations")
    client_id = st.selectbox("Select Client ID", ["client_123", "client_456", "client_789"])
    
    st.markdown("#### Compliance Report")
    st.info(
        f"**Decision for {client_id}:** REBALANCE_TRIGGERED\n\n"
        "**Key Drivers (SHAP):**\n"
        "- drift_magnitude_pct increased the likelihood of rebalancing (Impact: 0.15)\n"
        "- vix_level increased the likelihood of rebalancing (Impact: 0.08)\n\n"
        "**Counterfactual Analysis (LIME):**\n"
        "If 'drift_magnitude_pct > 0.05' were reversed, the decision would likely have been altered."
    )
    st.markdown("*(Inline SHAP Waterfall plots are available in `reports/plots`)*")

elif view == "System Health":
    health = get_system_health_data()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Uptime", health["Uptime"])
    col2.metric("Error Rate", health["Error Rate"])
    col3.metric("API Latency", health["API Latency"])
    col4.metric("Active Agents", health["Active Agents"])
    
    st.markdown("---")
    st.markdown("### Global Kill-Switch")
    if st.button("🔴 ENGAGE EMERGENCY HALT"):
        st.error("SYSTEM HALTED. All autonomous rebalancing suspended.")
