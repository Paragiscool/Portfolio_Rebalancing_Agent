from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import date
import pandas as pd


class TriggerEvaluator(ABC):
    """Base class for rebalancing triggers."""

    @abstractmethod
    def evaluate(self, portfolio_data: pd.Series) -> Dict[str, Any]:
        """Returns trigger information including whether it fired and severity."""
        pass


class ThresholdTrigger(TriggerEvaluator):
    """Evaluates threshold breaches and assigns severity."""

    def evaluate(self, portfolio_data: pd.Series) -> Dict[str, Any]:
        drift_severity = portfolio_data.get("drift_severity", 0.0)
        fired = portfolio_data.get("needs_rebalance", False)

        severity_label = "Low"
        if drift_severity > 0.05:
            severity_label = "Critical"
        elif drift_severity > 0.02:
            severity_label = "High"
        elif drift_severity > 0.0:
            severity_label = "Medium"

        return {
            "trigger_type": "Threshold",
            "fired": fired,
            "severity_label": severity_label,
            "drift_severity": drift_severity,
            "priority": (
                3
                if severity_label == "Critical"
                else (2 if severity_label == "High" else 1)
            ),
        }


class CalendarTrigger(TriggerEvaluator):
    """Manages scheduled review triggers."""

    def __init__(self, review_schedule: str = "Quarterly"):
        self.review_schedule = review_schedule

    def evaluate(self, portfolio_data: pd.Series) -> Dict[str, Any]:
        # For simulation, we check if there's a forced calendar flag in the data
        fired = portfolio_data.get("force_calendar_rebalance", False)
        return {
            "trigger_type": "Calendar",
            "fired": fired,
            "severity_label": "Informational",
            "priority": 0,
        }


class EventTrigger(TriggerEvaluator):
    """Detects external events like market crashes or tax harvesting windows."""

    def __init__(self, active_events: List[str] = None):
        self.active_events = active_events or []

    def evaluate(self, portfolio_data: pd.Series) -> Dict[str, Any]:
        # Both global active events and portfolio-specific events
        portfolio_events = portfolio_data.get("specific_events", [])
        all_events = list(set(self.active_events + portfolio_events))

        fired = len(all_events) > 0
        return {
            "trigger_type": "Event",
            "fired": fired,
            "severity_label": "Critical" if "Crash" in all_events else "High",
            "events": all_events,
            "priority": 4 if fired else 0,
        }


class TriggerConsolidator:
    """Merges multiple triggers for the same portfolio."""

    def __init__(self, triggers: List[TriggerEvaluator]):
        self.triggers = triggers

    def evaluate_all(self, portfolio_data: pd.Series) -> Dict[str, Any]:
        results = []
        for t in self.triggers:
            res = t.evaluate(portfolio_data)
            if res.get("fired"):
                results.append(res)

        if not results:
            return {"rebalance_needed": False, "triggers": []}

        # Consolidate by picking the highest priority trigger as the primary reason
        results.sort(key=lambda x: x.get("priority", 0), reverse=True)
        primary_trigger = results[0]

        return {
            "rebalance_needed": True,
            "primary_trigger": primary_trigger,
            "all_triggers": results,
        }
