from .workflow_state import WorkflowState, WorkflowStatus
import random


class PortfolioAnalystAgent:
    """Agent responsible for calculating drift and identifying if a rebalance is needed."""

    def process(self, state: WorkflowState) -> WorkflowState:
        if state.status != WorkflowStatus.PENDING:
            return state  # Skip if already processed

        try:
            # Wrap Day 2 DriftCalculator and Day 3 TriggerEvaluator here
            # Mocking for architectural skeleton
            drift = random.uniform(0.01, 0.08)
            needs_rebalance = drift > 0.05
            state.drift_results = {
                "needs_rebalance": needs_rebalance,
                "max_drift": round(drift, 6),
            }
            state.transition(
                WorkflowStatus.DRIFT_ANALYZED,
                "PortfolioAnalystAgent",
                "Calculated drift",
                {"max_drift": round(drift, 6), "needs_rebalance": needs_rebalance},
            )

            # If no rebalancing is needed, mark as completed immediately
            if not needs_rebalance:
                state.transition(
                    WorkflowStatus.COMPLETED,
                    "PortfolioAnalystAgent",
                    "No rebalance needed — drift within acceptable band",
                )
        except Exception as e:
            state.transition(
                WorkflowStatus.FAILED, "PortfolioAnalystAgent", f"Error: {str(e)}"
            )

        return state


class RiskOptimisationAgent:
    """Agent responsible for running CVXPY to generate the trade list."""

    def process(self, state: WorkflowState) -> WorkflowState:
        if state.status != WorkflowStatus.DRIFT_ANALYZED:
            return state

        try:
            # Wrap Day 4 PortfolioOptimiser and TradeListGenerator here
            state.trade_recommendations = [
                {"ticker": "AAPL", "action": "BUY", "shares": 100},
                {"ticker": "MSFT", "action": "SELL", "shares": 50},
            ]
            state.transition(
                WorkflowStatus.OPTIMIZED,
                "RiskOptimisationAgent",
                "Generated optimal trade list",
            )
        except Exception as e:
            state.transition(
                WorkflowStatus.FAILED, "RiskOptimisationAgent", f"Error: {str(e)}"
            )

        return state


class TaxAgent:
    """Agent responsible for evaluating tax impact and harvesting losses."""

    def process(self, state: WorkflowState) -> WorkflowState:
        if state.status != WorkflowStatus.OPTIMIZED:
            return state

        try:
            # Wrap Day 5 TaxOptimiser here (Mocked for now)
            state.tax_results = {
                "tax_liability_estimated": 250.0,
                "harvested_losses": 0.0,
            }
            state.transition(
                WorkflowStatus.TAX_ANALYZED, "TaxAgent", "Estimated tax implications"
            )
        except Exception as e:
            state.transition(WorkflowStatus.FAILED, "TaxAgent", f"Error: {str(e)}")

        return state


class ExplanationAgent:
    """Agent responsible for generating the LLM explanation for compliance/clients."""

    def process(self, state: WorkflowState) -> WorkflowState:
        if state.status != WorkflowStatus.TAX_ANALYZED:
            return state

        try:
            # Wrap Day 6 LangChain logic here
            state.explanation = (
                "Rebalanced portfolio due to threshold drift. "
                "Executed trades minimizing tracking error."
            )
            state.transition(
                WorkflowStatus.EXPLAINED,
                "ExplanationAgent",
                "Generated natural language explanation",
            )

            # Final state transition for success
            state.transition(
                WorkflowStatus.COMPLETED, "System", "Workflow finished successfully"
            )
        except Exception as e:
            state.transition(
                WorkflowStatus.FAILED, "ExplanationAgent", f"Error: {str(e)}"
            )

        return state
