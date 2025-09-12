from crewai import Agent, Crew, Task
from crewai.project import CrewBase,agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from langsmith import traceable
from eval import EvalListener
from tools import FinanceTools

EvalListener()  # Initialize the evaluation listener

tools = FinanceTools()

@CrewBase
class PortfolioManager():
    """
    Portfolio Manager Agent for managing investment portfolios.
    """
    agent: List[BaseAgent]
    task: List[Task]

    @traceable(run_type="chain")
    @agent
    def analyze_portfolio(self) -> Agent:
        """
        Analyze the given portfolio and provide insights.
        """
        return Agent(
            config = self.agents_config["PortfolioAnalyzer"],
            verbose=True,
            memory=True,
            tools=[tools.stock_price_tool, tools.portfolio_analysis_tool],
         )
    
    @traceable(run_type="chain")
    @task
    def analyze_portfolio_task(self) -> Task:
        """
        Task to analyze the portfolio.
        Returns:
            Task: A task that performs portfolio analysis.
        """
        return Task(
            name="AnalyzePortfolioTask",
            agent=self.analyze_portfolio(),
            config = self.tasks_config["AnalyzePortfolioTask"],
            input_variables=["portfolio"],
            output_variables=["analysis_report"],
        )
    
    @traceable(run_type="chain")
    @crew
    def portfolio_management_crew(self) -> Crew:
        """
        Crew to manage the portfolio analysis process.
        Returns:
            Crew: A crew that manages the portfolio analysis task.
        """
        return Crew(
            name="PortfolioManagementCrew",
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )
