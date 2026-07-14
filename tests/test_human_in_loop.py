import os
import json
from src.human_in_loop.intervention_classifier import InterventionClassifier, InterventionLevel
from src.human_in_loop.override_capture import OverrideCapture, EscalationManager

def test_intervention_classifier():
    classifier = InterventionClassifier(max_vix=40.0, max_error_rate=0.01, max_turnover_pct=0.10)
    
    # Test Kill Switch
    assert classifier.check_kill_switch({"vix": 45.0}, {"error_rate": 0.001}) == True
    assert classifier.check_kill_switch({"vix": 20.0}, {"error_rate": 0.001}) == False
    assert classifier.check_kill_switch({"vix": 20.0}, {"error_rate": 0.05}) == True
    
    # Test Trade Turnover Classifications
    # Total portfolio is 100k
    normal_trades = [{"amount": 5000}, {"amount": -4000}] # 9k turnover -> 9% (Advisory)
    extreme_trades = [{"amount": 15000}, {"amount": -2000}] # 17k turnover -> 17% (Approval Required)
    small_trades = [{"amount": 1000}, {"amount": -1000}] # 2k turnover -> 2% (Informational)
    
    assert classifier.classify_decision(normal_trades, 100000.0) == InterventionLevel.ADVISORY
    assert classifier.classify_decision(extreme_trades, 100000.0) == InterventionLevel.APPROVAL_REQUIRED
    assert classifier.classify_decision(small_trades, 100000.0) == InterventionLevel.INFORMATIONAL

def test_override_capture(tmp_path):
    audit_file = str(tmp_path / "overrides.json")
    capture = OverrideCapture(audit_file)
    
    res = capture.capture_override(
        original_trades=[{"asset": "AAPL", "amount": 1000}],
        modified_trades=[],
        reason="Client requested hold",
        advisor_id="adv_001"
    )
    assert res["status"] == "success"
    
    with open(audit_file, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["advisor_id"] == "adv_001"

def test_escalation_manager(tmp_path):
    output_dir = str(tmp_path / "escalations")
    manager = EscalationManager(output_dir)
    
    filepath = manager.generate_briefing_document(
        client_id="client_123",
        context={"vix": 25},
        recommended_trades=[{"asset": "AAPL", "amount": 10000}]
    )
    
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        content = f.read()
        assert "client_123" in content
        assert "AAPL" in content
