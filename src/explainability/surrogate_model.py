import numpy as np
import pandas as pd
import xgboost as xgb
from typing import Dict, Any, Tuple

class RebalanceSurrogateModel:
    """
    Trains a surrogate gradient boosted tree (XGBoost) to predict if a portfolio rebalance
    will be triggered, allowing SHAP/LIME explainability on the decision.
    """
    def __init__(self):
        self.model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
        self.is_trained = False
        
        # Define the feature columns we expect
        self.feature_names = [
            "drift_magnitude_pct",
            "vix_level",
            "days_since_last_rebalance",
            "client_risk_score",
            "sector_concentration_pct"
        ]
        
    def generate_synthetic_training_data(self, n_samples: int = 1000) -> Tuple[pd.DataFrame, pd.Series]:
        """Generates synthetic data for the surrogate model training."""
        np.random.seed(42)
        
        # Features
        drift = np.random.uniform(0.0, 0.15, n_samples)
        vix = np.random.uniform(10.0, 40.0, n_samples)
        days = np.random.randint(1, 400, n_samples)
        risk = np.random.randint(1, 6, n_samples)
        concentration = np.random.uniform(0.0, 0.25, n_samples)
        
        df = pd.DataFrame({
            "drift_magnitude_pct": drift,
            "vix_level": vix,
            "days_since_last_rebalance": days,
            "client_risk_score": risk,
            "sector_concentration_pct": concentration
        })
        
        # Target logic: rebalance likely if high drift, high VIX, or long time since last rebalance
        logit = (
            (drift - 0.05) * 50 + 
            (vix - 20) * 0.1 + 
            (days - 180) * 0.01
        )
        prob = 1 / (1 + np.exp(-logit))
        
        # Add random noise
        random_prob = np.random.uniform(0, 1, n_samples)
        y = (prob > random_prob).astype(int)
        
        return df, pd.Series(y)
        
    def train(self, X: pd.DataFrame = None, y: pd.Series = None):
        """Train the XGBoost model. If X, y are not provided, uses synthetic data."""
        if X is None or y is None:
            X, y = self.generate_synthetic_training_data()
            
        self.model.fit(X[self.feature_names], y)
        self.X_train = X[self.feature_names] # Save for SHAP/LIME baseline
        self.is_trained = True
        
    def predict(self, features: Dict[str, float]) -> int:
        """Predict rebalance trigger (1) or not (0) for a single instance."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
            
        df = pd.DataFrame([features])[self.feature_names]
        return self.model.predict(df)[0]
