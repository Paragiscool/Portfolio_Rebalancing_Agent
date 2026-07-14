import os
from src.compliance.compliance_auditor import ComplianceAuditor
from src.compliance.regulatory_reporter import RegulatoryReportGenerator

def test_compliance_auditor():
    auditor = ComplianceAuditor(sample_size=5)
    
    decisions = [
        {"risk_category": "Conservative", "turnover_pct": 0.25, "explanation": {"shap_summary": "x", "counterfactual_statement": "y"}},
        {"risk_category": "Conservative", "turnover_pct": 0.22, "explanation": {"shap_summary": "x"}}, # Missing LIME
        {"risk_category": "Aggressive", "turnover_pct": 0.05, "explanation": {"shap_summary": "x", "counterfactual_statement": "y"}},
    ]
    
    # Test sampling
    sampled = auditor.sample_decisions(decisions)
    assert len(sampled) == 3
    
    # Test bias (Conservative has > 20% average)
    bias_res = auditor.check_for_bias(sampled)
    assert bias_res["bias_detected"] == True
    assert bias_res["average_turnovers"]["Conservative"] == 0.235
    
    # Test explanation completeness (2 out of 3 are complete)
    expl_score = auditor.evaluate_explanation_completeness(sampled)
    assert round(expl_score, 2) == 0.67

def test_regulatory_reporter(tmp_path):
    output_dir = str(tmp_path)
    reporter = RegulatoryReportGenerator(output_dir)
    
    audit_results = {
        "bias_detected": False,
        "explanation_score": 1.0,
        "average_turnovers": {"Conservative": 0.05, "Aggressive": 0.15},
        "alert_message": ""
    }
    
    filepath = reporter.generate_report("Q3_2026", audit_results)
    
    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Q3_2026" in content
        assert "✅ PASSED" in content
        assert "Conservative" in content
