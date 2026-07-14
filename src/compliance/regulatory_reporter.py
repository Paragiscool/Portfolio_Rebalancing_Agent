import os
from datetime import datetime
from typing import Dict, Any

class RegulatoryReportGenerator:
    def __init__(self, output_dir: str = "reports/regulatory"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, quarter: str, audit_results: Dict[str, Any]) -> str:
        """
        Generates a Markdown compliance report summarizing the audit results.
        """
        filename = os.path.join(self.output_dir, f"{quarter}_Audit_Report.md")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        bias_flag = "⚠️ FAILED (Bias Detected)" if audit_results.get("bias_detected") else "✅ PASSED"
        explanation_score = audit_results.get("explanation_score", 0.0)
        expl_flag = "✅ PASSED" if explanation_score > 0.95 else "⚠️ WARNING"
        
        doc = f"# Regulatory Audit Report: {quarter}\n\n"
        doc += f"**Generated On:** {timestamp}\n\n"
        doc += "## 1. Executive Summary\n"
        doc += "This document serves as the official compliance record for the Autonomous Portfolio Rebalancing Agent. "
        doc += "A stratified sample of AI decisions was audited for systematic biases and explanation completeness.\n\n"
        
        doc += "## 2. Audit Results\n"
        doc += f"- **Systematic Bias Check:** {bias_flag}\n"
        doc += f"- **Explanation Completeness (Target >95%):** {explanation_score:.2%} {expl_flag}\n\n"
        
        doc += "### 2.1 Turnover by Risk Category\n"
        doc += "| Risk Category | Avg Turnover |\n"
        doc += "|---|---|\n"
        for risk, to in audit_results.get("average_turnovers", {}).items():
            doc += f"| {risk} | {to:.2%} |\n"
            
        if audit_results.get("bias_detected"):
            doc += f"\n**AUDITOR ALERT:** {audit_results.get('alert_message')}\n\n"
            
        doc += "\n## 3. Auditor Sign-off\n"
        doc += "_________________________\n"
        doc += "Chief Compliance Officer\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc)
            
        return filename
