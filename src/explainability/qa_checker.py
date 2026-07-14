import re
import textstat
from typing import Dict, Any, List

class QAException(Exception):
    pass

class HallucinationException(QAException):
    pass

class ReadabilityException(QAException):
    pass

class QAChecker:
    def __init__(self, readability_limit: float = 8.0, num_tolerance: float = 0.01):
        self.readability_limit = readability_limit
        self.num_tolerance = num_tolerance
        
    def check_flesch_kincaid(self, text: str) -> float:
        """
        Calculates Flesch-Kincaid grade level. 
        Raises ReadabilityException if it exceeds the limit.
        """
        score = textstat.flesch_kincaid_grade(text)
        if score > self.readability_limit:
            raise ReadabilityException(f"Flesch-Kincaid score {score} exceeds limit {self.readability_limit}")
        return score
        
    def extract_numbers(self, text: str) -> List[float]:
        """Extract all floating point numbers and currency strings from text."""
        # Matches numbers with optional commas and decimals
        pattern = r'-?\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|-?\b\d+\.\d+\b|-?\b\.\d+\b|-?\b\d+\b'
        matches = re.findall(pattern, text)
        
        extracted = []
        for m in matches:
            clean_num = m.replace(',', '')
            try:
                extracted.append(float(clean_num))
            except ValueError:
                continue
        return extracted
        
    def validate_numbers(self, text: str, input_metadata: Dict[str, Any]) -> bool:
        """
        Extracts numbers from text and asserts they exist within input_metadata within tolerance.
        Raises HallucinationException if a number in the text isn't in the metadata.
        """
        extracted_nums = self.extract_numbers(text)
        
        # Flatten input metadata into a list of reference numbers
        ref_nums = []
        def extract_refs(obj):
            if isinstance(obj, (int, float)):
                ref_nums.append(float(obj))
            elif isinstance(obj, dict):
                for v in obj.values():
                    extract_refs(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_refs(item)
                    
        extract_refs(input_metadata)
        
        # Add *100 equivalents to handle percentages (e.g., 0.55 -> 55)
        percentage_refs = [r * 100.0 for r in ref_nums if abs(r) <= 1.0]
        ref_nums.extend(percentage_refs)
                        
        if not ref_nums:
            ref_nums = [0.0, 1.0, 2.0]
            
        for num in extracted_nums:
            # Ignore small integers often used for formatting/lists or years (e.g. 2026)
            if num in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] or (2000 < num < 2100):
                continue
                
            # Check if num is close to any ref_num
            is_valid = False
            for ref in ref_nums:
                if abs(ref) < 1e-6:
                    if abs(num) < 1e-6:
                        is_valid = True
                        break
                else:
                    if abs(num - ref) / abs(ref) <= self.num_tolerance:
                        is_valid = True
                        break
            
            if not is_valid:
                raise HallucinationException(
                    f"Hallucination detected: Number {num} found in text but not found in input metadata (Tolerance: {self.num_tolerance*100}%). Ref numbers: {ref_nums}"
                )
                
        return True
