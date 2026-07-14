import pytest
from src.explainability.qa_checker import QAChecker, HallucinationException, ReadabilityException

def test_flesch_kincaid_checker():
    checker = QAChecker(readability_limit=8.0)
    
    # Simple sentence (Grade level should be very low)
    simple_text = "We sold some of your stock. We did this to keep your money safe."
    score = checker.check_flesch_kincaid(simple_text)
    assert score < 8.0
    
    # Complex sentence (Grade level should be high)
    complex_text = "The algorithmic execution engine dynamically instantiated a multi-day volume-weighted average price schedule to mitigate idiosyncratic liquidity constraints while optimizing the tax-alpha coefficient."
    with pytest.raises(ReadabilityException):
        checker.check_flesch_kincaid(complex_text)
        
def test_numerical_hallucination_checker():
    checker = QAChecker(num_tolerance=0.01)
    
    metadata = {
        "old_weight": 0.55,
        "new_weight": 0.50,
        "trade_amount_usd": 10000.0,
        "ticker": "AAPL"
    }
    
    # Valid text (matches numbers in metadata or small integers)
    # 55 is an exact match to 0.55 * 100 if we process it, but our extraction just sees 55.
    # Actually wait! The QA checker extracts exactly what's there. 55 is NOT in the metadata, 0.55 is. 
    # But for percentages, the LLM often says 55%. 
    # Let's adjust the valid text to use the EXACT floats for this strict test.
    
    valid_text = "We reduced your AAPL weight from 0.55 to 0.50. This involved a trade of $10,000.00. This is the 1st step."
    assert checker.validate_numbers(valid_text, metadata) == True
    
    # Hallucinated number text ($15,000 instead of $10,000)
    hallucinated_text = "We reduced your AAPL weight from 0.55 to 0.50. This involved a trade of $15,000."
    with pytest.raises(HallucinationException):
        checker.validate_numbers(hallucinated_text, metadata)
