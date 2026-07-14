import json
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from src.orchestration.agent_tools import calculate_drift_tool, generate_optimized_trades_tool, generate_explanations_tool

class RebalancingCrew:
    def __init__(self, llm_model="gpt-4o-mini"):
        # Pass LLM model name directly; modern CrewAI handles the litellm routing
        self.llm_model_name = llm_model

    def _create_agents(self):
        analyst = Agent(
            role='Portfolio Analyst',
            goal='Analyze portfolio drift and identify if rebalancing is required.',
            backstory='You are a meticulous quantitative analyst who strictly monitors portfolios against their target allocations.',
            verbose=True,
            allow_delegation=False,
            tools=[calculate_drift_tool],
            llm=self.llm_model_name
        )

        optimizer = Agent(
            role='Quantitative Optimizer',
            goal='Generate tax-aware, liquidity-constrained trade lists to resolve portfolio drift.',
            backstory='You are an expert mathematical optimizer. You rely purely on your tools to produce the final trade allocations.',
            verbose=True,
            allow_delegation=False,
            tools=[generate_optimized_trades_tool],
            llm=self.llm_model_name
        )

        compliance = Agent(
            role='Compliance & Explanation Officer',
            goal='Generate deterministic, human-readable explanations of the optimization trades for compliance audits.',
            backstory='You are a strict compliance officer. You ensure all trades are accompanied by explainable metrics and counterfactuals.',
            verbose=True,
            allow_delegation=False,
            tools=[generate_explanations_tool],
            llm=self.llm_model_name
        )
        return analyst, optimizer, compliance

    def _create_tasks(self, analyst, optimizer, compliance, client_id: str):
        drift_task = Task(
            description=f'Use the Calculate Portfolio Drift tool for client: {client_id}. Determine if a rebalance is needed. Return only "Proceed" or "Stop" along with the drift details JSON.',
            expected_output='A summary stating whether to Proceed or Stop, plus drift metrics.',
            agent=analyst
        )

        optimize_task = Task(
            description=f'If the previous task said "Proceed", use the Generate Optimized Trades tool for client: {client_id}. Otherwise, say "No trades required".',
            expected_output='A JSON list of proposed trades.',
            agent=optimizer
        )

        report_task = Task(
            description='Take the trade list and drift details, and format them into a flat JSON decision metadata object mapping strings to numbers (e.g. {{"trade_value": 10000}}). Pass this exact JSON string to the Generate Explanations tool to generate the compliance report.',
            expected_output='A JSON object containing the full compliance explanation.',
            agent=compliance
        )
        return [drift_task, optimize_task, report_task]

    def run(self, client_id: str):
        analyst, optimizer, compliance = self._create_agents()
        tasks = self._create_tasks(analyst, optimizer, compliance, client_id)

        crew = Crew(
            agents=[analyst, optimizer, compliance],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()
