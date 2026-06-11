import pytest
from src.orchestration.workflow_state import WorkflowState, WorkflowStatus
from src.orchestration.orchestrator import Orchestrator


def test_workflow_state_transitions():
    state = WorkflowState(portfolio_id="P_123")
    assert state.status == WorkflowStatus.PENDING

    state.transition(WorkflowStatus.DRIFT_ANALYZED, "Analyst", "Calculated drift")
    assert state.status == WorkflowStatus.DRIFT_ANALYZED
    assert len(state.audit_trail) == 1
    assert state.audit_trail[0].agent_name == "Analyst"


def test_orchestrator_chunking():
    # We set a small chunk size of 100
    orchestrator = Orchestrator(chunk_size=100)

    # 250 portfolios affected by an event
    portfolios = [f"P_{i}" for i in range(250)]

    workflow_ids = orchestrator.process_event("MARKET_CRASH_01", portfolios)

    assert len(workflow_ids) == 250
    assert len(orchestrator.state_store) == 250

    # Verify that they were processed
    state_0 = orchestrator.get_state(workflow_ids[0])
    # Based on our mock agents, if needs_rebalance is True it goes to COMPLETED
    # If needs_rebalance is False it stays at DRIFT_ANALYZED
    assert state_0.status in [
        WorkflowStatus.COMPLETED,
        WorkflowStatus.DRIFT_ANALYZED,
        WorkflowStatus.FAILED,
    ]


def test_resume_from_failure():
    orchestrator = Orchestrator(chunk_size=10)

    # Pre-seed the state store to simulate a crash at TAX_ANALYZED
    state = WorkflowState(portfolio_id="P_TEST_FAIL")
    state.status = WorkflowStatus.TAX_ANALYZED

    orchestrator.state_store[state.workflow_id] = state

    # Run process_chunk directly to test resumption
    orchestrator._process_chunk([state.workflow_id])

    # It should skip Analyst, Optimiser, and Tax agents, going straight to ExplanationAgent
    final_state = orchestrator.get_state(state.workflow_id)
    assert final_state.status == WorkflowStatus.COMPLETED
    assert final_state.explanation is not None
