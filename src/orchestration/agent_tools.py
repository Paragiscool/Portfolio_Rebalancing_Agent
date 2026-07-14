import json
from crewai.tools import tool
from src.engine.drift_calculator import DriftCalculator
from src.engine.triggers import TriggerEvaluator
from src.optimiser.portfolio_optimiser import PortfolioOptimiser
from src.explainability.generators import ExplanationGenerator
from src.explainability.shap_lime_explainer import ExplainabilityEngine
from src.explainability.surrogate_model import RebalanceSurrogateModel

# Mock data store for pipeline integration
PORTFOLIO_DB = {
    "client_1": {
        "current_weights": {"AAPL": 0.40, "GOOGL": 0.60},
        "target_weights": {"AAPL": 0.50, "GOOGL": 0.50},
        "thresholds": {"AAPL": 0.05, "GOOGL": 0.05}
    }
}

@tool("Calculate Portfolio Drift")
def calculate_drift_tool(client_id: str) -> str:
    """Calculates drift for a given client_id and returns the summary."""
    data = PORTFOLIO_DB.get(client_id)
    if not data:
        return "Client not found."
    
    calc = DriftCalculator(data["target_weights"], data["thresholds"])
    drift_details = calc.calculate_drift(data["current_weights"])
    
    evaluator = TriggerEvaluator()
    trigger = evaluator.evaluate(drift_details, None, None)
    
    return json.dumps({
        "status": "rebalance_needed" if trigger else "no_action",
        "details": drift_details
    })

@tool("Generate Optimized Trades")
def generate_optimized_trades_tool(client_id: str) -> str:
    """Runs the optimizer to generate a trade list to fix the drift for a client_id."""
    data = PORTFOLIO_DB.get(client_id)
    if not data:
        return "Client not found."
        
    opt = PortfolioOptimiser(data["target_weights"], {})
    trades = opt.optimize(data["current_weights"], 10000)
    
    return json.dumps(trades)

@tool("Generate Explanations")
def generate_explanations_tool(decision_metadata_json: str) -> str:
    """Generates compliance explanations based on decision metadata JSON."""
    try:
        decision_metadata = json.loads(decision_metadata_json)
    except:
        decision_metadata = {"error": "Invalid JSON"}
        
    surrogate = RebalanceSurrogateModel()
    surrogate.train()
    engine = ExplainabilityEngine(surrogate, plots_dir="reports/plots")
    
    features = {
        "drift_magnitude_pct": 0.10,
        "vix_level": 20.0,
        "days_since_last_rebalance": 100,
        "client_risk_score": 3,
        "sector_concentration_pct": 0.10
    }
    shap_sum, counter = engine.generate_explanations(features)
    
    generator = ExplanationGenerator()
    comp = generator.generate_compliance_explanation(decision_metadata, shap_sum, counter)
    
    return json.dumps(comp)
