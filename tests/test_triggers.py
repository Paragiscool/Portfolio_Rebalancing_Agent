import pytest
import pandas as pd
from src.engine.triggers import (
    ThresholdTrigger,
    CalendarTrigger,
    EventTrigger,
    TriggerConsolidator,
)


def test_threshold_trigger_critical():
    portfolio = pd.Series({"needs_rebalance": True, "drift_severity": 0.06})
    trigger = ThresholdTrigger()
    result = trigger.evaluate(portfolio)

    assert result["fired"] is True
    assert result["severity_label"] == "Critical"
    assert result["priority"] == 3


def test_threshold_trigger_medium():
    portfolio = pd.Series({"needs_rebalance": True, "drift_severity": 0.01})
    trigger = ThresholdTrigger()
    result = trigger.evaluate(portfolio)

    assert result["fired"] is True
    assert result["severity_label"] == "Medium"
    assert result["priority"] == 1


def test_calendar_trigger():
    portfolio = pd.Series({"force_calendar_rebalance": True})
    trigger = CalendarTrigger()
    result = trigger.evaluate(portfolio)

    assert result["fired"]
    assert result["severity_label"] == "Informational"
    assert result["priority"] == 0


def test_event_trigger():
    portfolio = pd.Series({"specific_events": ["TaxHarvesting"]})
    trigger = EventTrigger(active_events=["Crash"])
    result = trigger.evaluate(portfolio)

    assert result["fired"] is True
    # 'Crash' is in active events, so it should be critical
    assert result["severity_label"] == "Critical"
    assert "Crash" in result["events"]
    assert "TaxHarvesting" in result["events"]
    assert result["priority"] == 4


def test_trigger_consolidation():
    # Scenario: Drift is medium, but there's a market crash event.
    portfolio = pd.Series(
        {
            "needs_rebalance": True,
            "drift_severity": 0.015,
            "specific_events": [],
            "force_calendar_rebalance": True,
        }
    )

    t1 = ThresholdTrigger()
    t2 = CalendarTrigger()
    t3 = EventTrigger(active_events=["Crash"])

    consolidator = TriggerConsolidator([t1, t2, t3])
    result = consolidator.evaluate_all(portfolio)

    assert result["rebalance_needed"] is True
    assert len(result["all_triggers"]) == 3

    # Highest priority should be the EventTrigger (priority 4)
    primary = result["primary_trigger"]
    assert primary["trigger_type"] == "Event"
    assert primary["severity_label"] == "Critical"


def test_no_triggers_fired():
    portfolio = pd.Series(
        {
            "needs_rebalance": False,
            "drift_severity": -0.01,
            "specific_events": [],
            "force_calendar_rebalance": False,
        }
    )

    t1 = ThresholdTrigger()
    t2 = CalendarTrigger()
    t3 = EventTrigger(active_events=[])

    consolidator = TriggerConsolidator([t1, t2, t3])
    result = consolidator.evaluate_all(portfolio)

    assert result["rebalance_needed"] is False
    assert len(result["triggers"]) == 0
