from typing import List, Dict
from .workflow_state import WorkflowState, WorkflowStatus
from .agents import (
    PortfolioAnalystAgent,
    RiskOptimisationAgent,
    TaxAgent,
    ExplanationAgent,
)


class Orchestrator:
    """Manages the lifecycle of WorkflowStates and executes the chunked pipeline."""

    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size
        # The agent pipeline
        self.pipeline = [
            PortfolioAnalystAgent(),
            RiskOptimisationAgent(),
            TaxAgent(),
            ExplanationAgent(),
        ]
        # In-memory mock for state persistence (mapping workflow_id -> state)
        self.state_store: Dict[str, WorkflowState] = {}

    def get_state(self, workflow_id: str) -> WorkflowState:
        return self.state_store.get(workflow_id)

    def process_event(self, event_id: str, affected_portfolio_ids: List[str]):
        """
        Main entry point for handling an event affecting many portfolios.
        Implements chunking (Option B).
        """
        # 1. Initialize State in Store (simulating DB insert)
        workflow_ids = []
        for pid in affected_portfolio_ids:
            state = WorkflowState(event_id=event_id, portfolio_id=pid)
            self.state_store[state.workflow_id] = state
            workflow_ids.append(state.workflow_id)

        # 2. Process in chunks
        chunks = [
            workflow_ids[i : i + self.chunk_size]
            for i in range(0, len(workflow_ids), self.chunk_size)
        ]

        for chunk in chunks:
            self._process_chunk(chunk)

        return workflow_ids

    def _process_chunk(self, chunk_workflow_ids: List[str]):
        """Processes a single chunk through the agent pipeline sequentially."""
        # In a real system, this would be distributed via Celery or Ray
        for wid in chunk_workflow_ids:
            # Fetch from "DB"
            state = self.state_store[wid]

            # Pass through agent pipeline
            for agent in self.pipeline:
                # If a previous agent marked it FAILED or COMPLETED, we stop passing it
                if state.status in [WorkflowStatus.FAILED, WorkflowStatus.COMPLETED]:
                    break

                # The agent processes the state and returns the updated state
                try:
                    state = agent.process(state)
                except Exception as e:
                    state.transition(
                        WorkflowStatus.FAILED,
                        "Orchestrator",
                        f"Unhandled Exception: {str(e)}",
                    )

                # Re-save to "DB" after every agent (simulating persistence)
                self.state_store[wid] = state
