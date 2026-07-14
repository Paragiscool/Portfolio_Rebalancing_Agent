import json
import os
from typing import Dict, Any, List
from datetime import datetime

class OverrideCapture:
    def __init__(self, audit_file: str = "reports/overrides_audit.json"):
        self.audit_file = audit_file
        os.makedirs(os.path.dirname(self.audit_file), exist_ok=True)
        if not os.path.exists(self.audit_file):
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def capture_override(self, original_trades: List[Dict], modified_trades: List[Dict], reason: str, advisor_id: str) -> Dict[str, Any]:
        """
        Simulates an API endpoint capturing an advisor's manual override.
        """
        override_record = {
            "timestamp": datetime.now().isoformat(),
            "advisor_id": advisor_id,
            "original_trades": original_trades,
            "modified_trades": modified_trades,
            "reason": reason
        }

        with open(self.audit_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        data.append(override_record)
        
        with open(self.audit_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        return {"status": "success", "record_id": len(data)}

class EscalationManager:
    def __init__(self, output_dir: str = "reports/escalations"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_briefing_document(self, client_id: str, context: Dict[str, Any], recommended_trades: List[Dict]) -> str:
        """
        Generates a Markdown briefing for human advisors to review highly escalated decisions.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{client_id}_escalation_{timestamp}.md"
        
        doc = f"# ESCALATION BRIEFING: {client_id}\n\n"
        doc += "## Situation Summary\n"
        doc += f"The AI engine has halted autonomous execution and requested human judgment.\n"
        doc += f"Reason: High Portfolio Turnover / Risk Limits Exceeded.\n\n"
        
        doc += "## Context\n"
        doc += json.dumps(context, indent=2) + "\n\n"
        
        doc += "## AI Recommended Actions\n"
        doc += json.dumps(recommended_trades, indent=2) + "\n\n"
        
        doc += "## Questions for Advisor\n"
        doc += "- Does the client's current liquidity situation permit this volume of trades?\n"
        doc += "- Are there overriding tax constraints not captured in the system?\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc)
            
        return filename
