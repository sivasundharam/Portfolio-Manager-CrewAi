from crewai.tools import tool
import yfinance as yf


class FinanceTools:
    @staticmethod
    @tool("stock_price_tool")
    def stock_price_tool(ticker: str):
        """ Get current stock price for a ticker symbol. """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            price = data['Close'].iloc[-1]
            return f"The current price of {ticker} is ${price:.2f}"
        except Exception as e:
            return f"Error fetching price for {ticker}: {str(e)}"
    
    @staticmethod
    @tool("portfolio_analysis_tool")
    def portfolio_analysis_tool(portfolio: dict):
        """ Analyze the portfolio and provide a summary. """
        try:
            total_value = sum(item['quantity'] * item['purchase_price'] for item in portfolio['holdings'])
            diversification = len(portfolio['holdings'])
            return f"Total Portfolio Value: ${total_value:.2f}, Number of Different Holdings: {diversification}"
        except Exception as e:
            return f"Error analyzing portfolio: {str(e)}"