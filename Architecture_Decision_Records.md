# Architecture Decision Records (ADR)

This document records the major architectural decisions made during the development of the Autonomous Portfolio Rebalancing Agent.

## ADR 1: Multi-Agent Orchestration Engine
- **Decision:** Use **CrewAI**.
- **Context:** The system requires different specialized "personas" (e.g., Quantitative Optimizer, Compliance Officer, Portfolio Analyst) to hand off tasks in a sequential flow.
- **Consequences:** CrewAI natively supports role-based delegation and sequential processing out-of-the-box, significantly reducing the boilerplate required to manage prompt chains compared to raw LangChain.

## ADR 2: Convex Optimization Engine
- **Decision:** Use **CVXPY**.
- **Context:** Finding optimal trade amounts that minimize transaction costs while adhering to risk and target weight constraints is a classic quadratic programming problem.
- **Consequences:** CVXPY is the industry standard for Python-based convex optimization, providing immense mathematical stability and speed compared to heuristic algorithms or manual gradient descent.

## ADR 3: Explainability Framework
- **Decision:** Use a hybrid of **SHAP (Shapley Additive exPlanations)** and **LIME**.
- **Context:** Black-box AI decisions are illegal in financial contexts without proper auditing and explainability.
- **Consequences:** SHAP provides structural, global feature importance (e.g., "Drift Magnitude" is the primary driver). LIME provides local counterfactuals ("If VIX was 10 points lower, we would not have traded"). This hybrid approach guarantees regulatory compliance.

## ADR 4: Frontend Visualization
- **Decision:** Use **Streamlit**.
- **Context:** Need a fast, interactive way to visualize performance metrics and heatmaps without building a heavy React/Node stack.
- **Consequences:** Streamlit allowed us to build the entire 5-page Performance Dashboard entirely in Python, utilizing `plotly` for interactive heatmaps and metrics in a fraction of the time.
