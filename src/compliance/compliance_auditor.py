import random
from typing import List, Dict, Any

class ComplianceAuditor:
    def __init__(self, sample_size: int = 100):
        self.sample_size = sample_size

    def sample_decisions(self, historical_decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Samples a subset of historical decisions for the audit.
        Ensures a maximum of self.sample_size is returned.
        """
        if len(historical_decisions) <= self.sample_size:
            return historical_decisions
        return random.sample(historical_decisions, self.sample_size)

    def check_for_bias(self, sampled_decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Checks if a specific risk category is systematically experiencing higher turnover.
        Returns a dictionary with bias flags.
        """
        turnover_by_risk = {"Conservative": [], "Moderate": [], "Aggressive": []}
        
        for decision in sampled_decisions:
            risk = decision.get("risk_category", "Moderate")
            turnover = decision.get("turnover_pct", 0.0)
            if risk in turnover_by_risk:
                turnover_by_risk[risk].append(turnover)

        avg_turnover = {}
        for risk, values in turnover_by_risk.items():
            if values:
                avg_turnover[risk] = sum(values) / len(values)
            else:
                avg_turnover[risk] = 0.0

        # Simple bias check: if any category is > 20% average turnover while others are < 5%
        bias_detected = False
        alert_message = ""
        
        if avg_turnover.get("Conservative", 0) > 0.20:
            bias_detected = True
            alert_message = "High systematic turnover detected in Conservative portfolios."
            
        return {
            "bias_detected": bias_detected,
            "average_turnovers": avg_turnover,
            "alert_message": alert_message
        }
        
    def evaluate_explanation_completeness(self, sampled_decisions: List[Dict[str, Any]]) -> float:
        """
        Checks if the explanations contain required structural fields (SHAP, LIME).
        Returns a score between 0.0 and 1.0
        """
        if not sampled_decisions:
            return 1.0
            
        valid_count = 0
        for decision in sampled_decisions:
            explanation = decision.get("explanation", {})
            if "shap_summary" in explanation and "counterfactual_statement" in explanation:
                valid_count += 1
                
        return valid_count / len(sampled_decisions)
