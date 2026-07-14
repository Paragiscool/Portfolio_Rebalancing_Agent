# Autonomous Portfolio Rebalancing Agent 🤖📈

An enterprise-grade, multi-agent AI system designed to automate quantitative portfolio rebalancing, ensure tax/liquidity efficiency, and generate regulatory-compliant explanations for every trade.

## Overview

Traditional portfolio rebalancing is a static, calendar-based process. This project leverages **CrewAI** to orchestrate specialized AI personas (Quantitative Optimizers, Compliance Officers, Portfolio Analysts) that continuously monitor portfolios for drift, calculate optimal tax-loss harvesting maneuvers using **CVXPY**, and generate human-readable SHAP/LIME audits for compliance sign-off.

## Key Features
- **Multi-Agent Orchestration**: Sequential CrewAI pipeline wrapping deterministic Python engines.
- **Convex Optimization**: CVXPY engine minimizing transaction costs while adhering to risk constraints.
- **Regulatory Explainability**: SHAP (global feature importance) and LIME (local counterfactuals) generation.
- **Human-in-the-Loop Safeguards**: VIX-based global kill-switches and turnover escalation triggers.
- **Performance Dashboard**: Real-time Streamlit visualization of drift heatmaps and backtested strategy comparisons.

## Installation

```bash
# Clone the repository
git clone https://github.com/Paragiscool/Portfolio_Rebalancing_Agent.git
cd Portfolio_Rebalancing_Agent

# Install requirements
pip install -r requirements.txt
```

## Usage

### 1. Run the Multi-Agent Rebalancing Pipeline
Execute the end-to-end autonomous flow:
```bash
python src/orchestration/pipeline_runner.py
```

### 2. Launch the Performance Dashboard
View the live metrics and audit explanations in your browser:
```bash
streamlit run src/dashboard/app.py
```

### 3. Run the Strategy Backtester
Compare the Agent's performance against a standard Buy-and-Hold:
```bash
python -m src.backtesting.strategy_comparator
```

## Architecture Decision Records (ADRs)
Please refer to the `Architecture_Decision_Records.md` file for an in-depth justification of the technology stack choices (e.g., CrewAI vs LangChain, CVXPY vs SciPy).

## Testing
Run the full test suite (with coverage) using pytest:
```bash
pytest --cov=src tests/
```

---
*Built as a state-of-the-art demonstration of agentic AI in quantitative finance.*
