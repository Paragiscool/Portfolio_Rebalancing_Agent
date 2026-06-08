Day 12: Compliance Audit And Regulatory Reporting 
Objectives: Build the compliance audit module and regulatory reporting system. 
Tasks: (1) Implement the ComplianceAuditor that performs automated quarterly audits: sample 
100 decisions (stratified by trigger type and risk category), evaluate explanation quality using 
automated metrics (accuracy, completeness, readability), check for systematic biases 
(over/under-rebalancing by risk category, systematic cost under/over-estimation), and generate 
the Audit Report. (2) Build the RegulatoryReporter that generates SEBI-compliant reports: 
complete transaction history with decision rationale, suitability assessment documentation for 
each recommendation, algorithmic trading audit trail, and exception reports (any compliance 
check failures or overrides). (3) Implement the BiasDetector that analyses agent decisions for 
systematic patterns: does the agent rebalance Conservative portfolios more frequently than 
justified? Does it systematically favour certain securities? Does it exhibit momentum or 
contrarian bias? (4) Build the ExplainabilityScorecard that rates each explanation on: accuracy 
(numbers match), completeness (all sections present), readability (grade level appropriate), 
Strictly Private and Confidential - Not for Circulation                                                                          Page number: 42 


 
 
 
 
 
actionability (client can understand what to do), and regulatory sufficiency (meets audit 
requirements). 
Deliverables: 
ComplianceAuditor 
module, 
RegulatoryReporter, 
BiasDetector, 
ExplainabilityScorecard, sample audit report. 
Checkpoint: Automated audit of 100 sample decisions completed, bias analysis report 
generated, all regulatory reports exportable.