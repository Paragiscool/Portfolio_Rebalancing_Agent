import pytest
from unittest.mock import patch
import os
from src.orchestration.crew_definition import RebalancingCrew

os.environ["OPENAI_API_KEY"] = "mock_key_for_testing"

# Since CrewAI does actual LLM calls which take time and cost money, 
# we mock the crew.kickoff() for unit testing to ensure the wiring is correct.
def test_rebalancing_crew_initialization():
    crew_framework = RebalancingCrew(llm_model="gpt-4o-mini")
    analyst, optimizer, compliance = crew_framework._create_agents()
    
    assert analyst.role == 'Portfolio Analyst'
    assert optimizer.role == 'Quantitative Optimizer'
    assert compliance.role == 'Compliance & Explanation Officer'
    
    tasks = crew_framework._create_tasks(analyst, optimizer, compliance, "client_1")
    assert len(tasks) == 3

@patch('src.orchestration.crew_definition.Crew.kickoff')
def test_rebalancing_crew_execution(mock_kickoff):
    mock_kickoff.return_value = "Mocked Explanation Output"
    
    crew_framework = RebalancingCrew()
    result = crew_framework.run("client_1")
    
    assert result == "Mocked Explanation Output"
    mock_kickoff.assert_called_once()
