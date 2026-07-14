import pytest
import os
from src.explainability.surrogate_model import RebalanceSurrogateModel
from src.explainability.shap_lime_explainer import ExplainabilityEngine

def test_surrogate_model():
    model = RebalanceSurrogateModel()
    model.train()
    
    assert model.is_trained == True
    
    features_trigger = {
        "drift_magnitude_pct": 0.10,
        "vix_level": 35.0,
        "days_since_last_rebalance": 200,
        "client_risk_score": 3,
        "sector_concentration_pct": 0.15
    }
    
    pred = model.predict(features_trigger)
    assert pred in [0, 1]

def test_explainability_engine():
    model = RebalanceSurrogateModel()
    # Ensure plots dir is created properly
    engine = ExplainabilityEngine(model, plots_dir="reports/plots")
    
    features = {
        "drift_magnitude_pct": 0.10,
        "vix_level": 35.0,
        "days_since_last_rebalance": 200,
        "client_risk_score": 3,
        "sector_concentration_pct": 0.15
    }
    
    shap_summary, counterfactual = engine.generate_explanations(features)
    
    assert "Key drivers for this decision" in shap_summary
    assert "Counterfactual Analysis" in counterfactual
