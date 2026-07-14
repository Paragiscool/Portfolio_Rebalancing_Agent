import sys
import os

# Add project root to python path to allow running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.orchestration.crew_definition import RebalancingCrew

def run_pipeline():
    print("Initializing Multi-Agent Rebalancing Crew...")
    crew = RebalancingCrew()
    
    print("\nStarting pipeline for 'client_1' (Simulated high drift portfolio)...")
    result = crew.run("client_1")
    
    print("\n--- FINAL CREW OUTPUT ---")
    print(result)

if __name__ == "__main__":
    run_pipeline()
