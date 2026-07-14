import os
import shap
import lime
import lime.lime_tabular
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple
from src.explainability.surrogate_model import RebalanceSurrogateModel

class ExplainabilityEngine:
    def __init__(self, surrogate: RebalanceSurrogateModel, plots_dir: str = "reports/plots"):
        self.surrogate = surrogate
        if not self.surrogate.is_trained:
            self.surrogate.train()
            
        self.plots_dir = plots_dir
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Initialize SHAP explainer
        self.shap_explainer = shap.TreeExplainer(self.surrogate.model)
        
        # Initialize LIME explainer
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=self.surrogate.X_train.values,
            feature_names=self.surrogate.feature_names,
            class_names=['No Rebalance', 'Rebalance Triggered'],
            mode='classification'
        )
        
    def generate_explanations(self, features: Dict[str, float]) -> Tuple[str, str]:
        """
        Generates SHAP and LIME text explanations, and saves plots.
        Returns:
            (shap_summary_str, counterfactual_str)
        """
        df_instance = pd.DataFrame([features])[self.surrogate.feature_names]
        
        # 1. SHAP Explanation
        shap_values = self.shap_explainer.shap_values(df_instance)
        
        # TreeExplainer for xgboost binary usually returns a single array or a list
        if isinstance(shap_values, list):
            vals = shap_values[1][0] 
            expected = self.shap_explainer.expected_value[1]
        else:
            # Depending on shap version, it might be 2D array or 1D array
            vals = shap_values[0] if len(shap_values.shape) > 1 else shap_values
            expected = self.shap_explainer.expected_value
            if isinstance(expected, (list, np.ndarray)):
                expected = expected[0]
            
        # Top 3 features by absolute SHAP value
        feature_impacts = [(name, val) for name, val in zip(self.surrogate.feature_names, vals)]
        feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)
        
        shap_str = "Key drivers for this decision:\n"
        for i, (fname, fval) in enumerate(feature_impacts[:3]):
            direction = "increased" if fval > 0 else "decreased"
            shap_str += f"- {fname} {direction} the likelihood of rebalancing (Impact: {fval:.4f})\n"
            
        # Save Waterfall plot
        try:
            shap_exp = shap.Explanation(
                values=vals, 
                base_values=expected, 
                data=df_instance.iloc[0].values, 
                feature_names=self.surrogate.feature_names
            )
            plt.figure(figsize=(10, 6))
            shap.plots.waterfall(shap_exp, show=False)
            plt.savefig(os.path.join(self.plots_dir, "shap_waterfall.png"), bbox_inches='tight')
            plt.close()
        except Exception as e:
            print(f"Plotting failed: {e}")
            pass
            
        # 2. LIME / Counterfactual logic
        def predict_fn(x):
            df_x = pd.DataFrame(x, columns=self.surrogate.feature_names)
            return self.surrogate.model.predict_proba(df_x)
            
        exp = self.lime_explainer.explain_instance(
            data_row=df_instance.iloc[0].values,
            predict_fn=predict_fn,
            num_features=5
        )
        
        lime_list = exp.as_list()
        top_feature = lime_list[0][0]
        
        counterfactual_str = f"Counterfactual Analysis: If '{top_feature}' were reversed, the rebalancing decision would likely have been altered."
        
        return shap_str, counterfactual_str
