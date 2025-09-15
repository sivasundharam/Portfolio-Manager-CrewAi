import json
from dotenv import load_dotenv
import os
load_dotenv()
from crew import PortfolioManager

print(os.getenv("OPENAI_MODEL_NAME"))
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "stock-analyst-bot")

with open("portfolio.json") as f:
    portfolio = json.load(f)

def run_portfolio_analysis():
    manager = PortfolioManager()
    crew = manager.portfolio_management_crew()

    # Extract tickers from portfolio for market analysis
    portfolio_tickers = [holding['ticker'] for holding in portfolio['holdings']]
    
    input_data = {
        "portfolio_json": portfolio,
        "portfolio_tickers": portfolio_tickers
    }
    result = crew.kickoff(input_data)
    
    print("=== PORTFOLIO ANALYSIS ===")
    print(result)

if __name__ == "__main__":
    run_portfolio_analysis()