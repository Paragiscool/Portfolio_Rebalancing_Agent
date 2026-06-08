Day 7: SHAP/LIME Integration For Explainability 
Objectives: Integrate SHAP and LIME to provide model-level explainability for rebalancing 
decisions. 
Tasks: (1) Train a gradient boosted decision tree (XGBoost/LightGBM) as a surrogate model 
that predicts rebalancing probability given input features (drift magnitude, VIX, days since last 
rebalance, client risk score, tax lot maturity, sector concentration). (2) Implement SHAP 
integration: compute Tree SHAP values for the surrogate model, generate waterfall plots for 
individual decisions, summary plots for aggregate feature importance, and dependency plots for 
key feature interactions. (3) Implement LIME integration: generate local explanations for 
individual rebalancing decisions showing the top 5 contributing features with direction and 
magnitude. (4) Implement counterfactual explanation generation: for each decision, find the 
minimal feature perturbation that would change the decision, and express this in natural language 
('If equity drift were below 3.2% instead of 4.7%, the agent would not have triggered a 
rebalance'). (5) Integrate SHAP/LIME outputs into the Compliance-level explanation template. 
(6) Write tests verifying SHAP value consistency and LIME fidelity. 
Deliverables: Surrogate model training pipeline, SHAP integration module, LIME integration 
module, counterfactual generator, integrated compliance explanations. 
Checkpoint: SHAP waterfall plots correctly attribute decision to input features, LIME 
explanations faithful to surrogate model, counterfactuals logically correct.