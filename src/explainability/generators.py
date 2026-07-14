import json
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from src.explainability.templates import CLIENT_TEMPLATE, ADVISOR_TEMPLATE, COMPLIANCE_TEMPLATE, REFINEMENT_TEMPLATE
from src.explainability.qa_checker import QAChecker, ReadabilityException, HallucinationException

class ClientExplanationSchema(BaseModel):
    narrative: str = Field(description="The plain-language explanation of the rebalance.")
    cost_summary: str = Field(description="Transparency about costs and taxes.")

class AdvisorExplanationSchema(BaseModel):
    quantitative_metrics: str = Field(description="Discussion of drift and tracking error.")
    allocation_table: str = Field(description="Markdown table of before and after weights.")
    override_invitation: str = Field(description="Must exactly match: 'To override this rebalance or modify the tax-lot selection, click here.'")

class ComplianceExplanationSchema(BaseModel):
    rule_breached: str = Field(description="The mathematical rule that triggered this.")
    wash_sale_status: str = Field(description="Wash sale status for assets sold.")
    audit_trail: str = Field(description="Time-stamped audit trail.")
    shap_summary: str = Field(description="Feature attributions placeholder.")
    counterfactual: str = Field(description="Counterfactual statement placeholder.")


class ExplanationGenerator:
    def __init__(self, llm_model: str = "gpt-4o-mini"):
        # We use gpt-4o-mini as the default model
        self.llm = ChatOpenAI(model=llm_model, temperature=0.1)
        self.qa_checker = QAChecker()
        
    def _validate_hallucinations(self, text: str, metadata: dict):
        """Wrapper for hallucination checks."""
        self.qa_checker.validate_numbers(text, metadata)

    def generate_client_explanation(self, decision_metadata: dict, max_retries: int = 2) -> dict:
        structured_llm = self.llm.with_structured_output(ClientExplanationSchema)
        chain = CLIENT_TEMPLATE | structured_llm
        
        meta_str = json.dumps(decision_metadata)
        current_result = None
        
        for attempt in range(max_retries + 1):
            if attempt == 0:
                result = chain.invoke({"decision_metadata": meta_str})
            else:
                # Refinement loop
                refine_chain = REFINEMENT_TEMPLATE | structured_llm
                result = refine_chain.invoke({
                    "previous_explanation": current_result.narrative + " " + current_result.cost_summary,
                    "score": score
                })
            
            current_result = result
            combined_text = result.narrative + " " + result.cost_summary
            
            try:
                # 1. Readability Check
                score = self.qa_checker.check_flesch_kincaid(combined_text)
                
                # 2. Hallucination Check
                self._validate_hallucinations(combined_text, decision_metadata)
                
                # If we pass both, return successfully
                return result.dict()
                
            except ReadabilityException as e:
                if attempt == max_retries:
                    # Fallback on final failure
                    return {
                        "narrative": "We adjusted your portfolio to keep it aligned with your target risk level.",
                        "cost_summary": "Details on costs and taxes are available in your trade confirmations."
                    }
                # Else loop around and retry
                continue
                
            except HallucinationException as e:
                # For hallucinations, we might just fail entirely or fallback. 
                # For safety, let's fallback if the LLM invents numbers.
                return {
                    "narrative": "We adjusted your portfolio to keep it aligned with your target risk level.",
                    "cost_summary": "Details on costs and taxes are available in your trade confirmations."
                }
                
        return current_result.dict()

    def generate_advisor_explanation(self, decision_metadata: dict) -> dict:
        structured_llm = self.llm.with_structured_output(AdvisorExplanationSchema)
        chain = ADVISOR_TEMPLATE | structured_llm
        
        meta_str = json.dumps(decision_metadata)
        result = chain.invoke({"decision_metadata": meta_str})
        
        combined_text = result.quantitative_metrics + " " + result.allocation_table
        self._validate_hallucinations(combined_text, decision_metadata)
        
        return result.dict()

    def generate_compliance_explanation(self, decision_metadata: dict, shap_summary: str, counterfactual: str) -> dict:
        structured_llm = self.llm.with_structured_output(ComplianceExplanationSchema)
        chain = COMPLIANCE_TEMPLATE | structured_llm
        
        meta_str = json.dumps(decision_metadata)
        result = chain.invoke({
            "decision_metadata": meta_str,
            "shap_summary": shap_summary,
            "counterfactual_statement": counterfactual
        })
        
        # Check hallucinations for compliance as well
        combined_text = result.rule_breached + " " + result.wash_sale_status + " " + result.audit_trail
        self._validate_hallucinations(combined_text, decision_metadata)
        
        return result.dict()
