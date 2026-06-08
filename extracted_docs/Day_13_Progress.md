Day 13: Integration Testing And Scenario Simulation 
Objectives: Execute comprehensive integration testing across all 5 market scenarios and validate 
end-to-end system behaviour. 
Tasks: (1) Run Scenario 1 (Normal Drift): process 50,000 portfolios through a 3-month equity 
rally, verify appropriate threshold-based rebalancing, validate cost efficiency. (2) Run Scenario 2 
(Market Crash): simulate a 22% equity correction, verify crisis response (prioritisation, batch 
processing, crisis communication), measure system performance under load. (3) Run Scenario 3 
(Sector Rotation): test intra-equity rebalancing when sector concentrations breach limits without 
overall allocation drift. (4) Run Scenario 4 (Regulatory Event): simulate a new SEBI circular, 
verify affected portfolio identification, trade list compliance, and regulatory-driven explanations. 
(5) Run Scenario 5 (Tax Harvesting): execute March FY-end tax-loss harvesting scan, verify tax 
savings quantification, substitute security logic, and wash-sale avoidance. (6) Document results, 
identify edge cases, and resolve any remaining bugs. 
Deliverables: Scenario test results for all 5 scenarios, edge case documentation, bug fixes, 
integration test report. 
Checkpoint: All 5 scenarios execute successfully, agent behaviour matches expected outcomes, 
no critical bugs remaining.