Day 3: Trigger Evaluation System 
Objectives: Implement the three-tier trigger taxonomy (threshold, calendar, event-driven) and 
the trigger consolidation logic. 
Tasks: (1) Implement the TriggerEvaluator base class with subclasses: ThresholdTrigger, 
CalendarTrigger, EventTrigger. (2) Build the ThresholdTrigger evaluator that classifies drift 
breaches into Critical, High, Medium severity based on magnitude and trend. (3) Build the 
CalendarTrigger evaluator that manages monthly, quarterly, and annual review schedules with 
business-day-aware date handling. (4) Build the EventTrigger evaluator with event detection 
logic for market crashes (configurable index decline thresholds), regulatory changes (manual 
input with affected portfolio identification), client life events (API endpoint for advisor input), 
and tax harvesting windows (date-range-based activation). (5) Implement trigger consolidation 
logic: when multiple triggers fire for the same portfolio, merge them into a single rebalancing 
event with the highest priority and a combined audit record. (6) Write integration tests simulating 
multi-trigger scenarios. 
Deliverables: Trigger evaluation framework, all trigger type implementations, consolidation 
logic, integration test suite. 
Checkpoint: Trigger system correctly classifies and prioritises at least 10 test scenarios covering 
all trigger types and combinations.