from crewai import Agent, Crew, Task
from crewai.project import CrewBase,agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
from langsmith import traceable
from eval import EvalListener
from tools import FinanceTools

EvalListener()  # Initialize the evaluation listener

# Create tool instances
tools = FinanceTools()
portfolio_tool = tools.portfolio_analysis_tool
stock_data_tool = tools.enhanced_stock_data_tool
news_tool = tools.market_news_tool
sentiment_tool = tools.market_sentiment_tool
sector_tool = tools.sector_analysis_tool

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
            tools=[
                portfolio_tool, 
                stock_data_tool,
                sector_tool
            ],
         )
    
    @traceable(run_type="chain")
    @agent
    def analyze_market_trends(self) -> Agent:
        """
        Analyze market trends, news sentiment, and market conditions.
        """
        return Agent(
            config = self.agents_config["MarketTrendAnalyzer"],
            verbose=True,
            memory=True,
            tools=[news_tool, sentiment_tool, sector_tool],
         )
    
    @traceable(run_type="chain")
    @task
    def analyze_market_trends_task(self) -> Task:
        """
        Task to analyze market trends and news sentiment.
        Returns:
            Task: A task that performs market trend analysis.
        """
        return Task(
            name="AnalyzeMarketTrendsTask",
            agent=self.analyze_market_trends(),
            config = self.tasks_config["AnalyzeMarketTrendsTask"],
            input_variables=["portfolio_tickers"],
            output_variables=["market_analysis_report"],
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
