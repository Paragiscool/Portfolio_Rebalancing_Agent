import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    """Return current UTC time in a non-deprecated way."""
    return datetime.now(timezone.utc)


class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    DRIFT_ANALYZED = "DRIFT_ANALYZED"
    OPTIMIZED = "OPTIMIZED"
    TAX_ANALYZED = "TAX_ANALYZED"
    EXPLAINED = "EXPLAINED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AuditLog(BaseModel):
    timestamp: datetime = Field(default_factory=_utc_now)
    agent_name: str
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)


class WorkflowState(BaseModel):
    """
    The persistent source of truth for a single portfolio's rebalancing workflow.
    This replaces passing massive contexts in memory between agents.
    """

    workflow_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_id: Optional[str] = None
    portfolio_id: str
    client_id: Optional[str] = None

    status: WorkflowStatus = Field(default=WorkflowStatus.PENDING)

    # Intermediate Results
    drift_results: Dict[str, Any] = Field(default_factory=dict)
    risk_results: Dict[str, Any] = Field(default_factory=dict)
    tax_results: Dict[str, Any] = Field(default_factory=dict)

    # Final Output
    trade_recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: Optional[str] = None

    # Tracking
    audit_trail: List[AuditLog] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    def transition(
        self,
        new_status: WorkflowStatus,
        agent_name: str,
        action: str,
        details: Dict[str, Any] = None,
    ):
        """Transition the workflow to a new status and log the action."""
        self.status = new_status
        self.updated_at = _utc_now()

        self.audit_trail.append(
            AuditLog(agent_name=agent_name, action=action, details=details or {})
        )
