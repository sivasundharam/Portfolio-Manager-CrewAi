from crewai.tools import tool
import yfinance as yf
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os


class FinanceTools:
    @staticmethod
    @tool("portfolio_analysis_tool")
    def portfolio_analysis_tool(portfolio: dict):
        """ Analyze the portfolio and provide a summary. """
        try:
            # Handle nested portfolio structure
            if 'portfolio' in portfolio:
                portfolio_data = portfolio['portfolio']
            else:
                portfolio_data = portfolio
            
            # Handle different possible structures
            if 'holdings' in portfolio_data:
                holdings = portfolio_data['holdings']
            elif 'description' in portfolio_data and 'holdings' in portfolio_data['description']:
                holdings = portfolio_data['description']['holdings']
            else:
                holdings = portfolio_data
            
            total_value = sum(item['quantity'] * item['purchase_price'] for item in holdings)
            diversification = len(holdings)
            return f"Total Portfolio Value: ${total_value:.2f}, Number of Different Holdings: {diversification}"
        except Exception as e:
            return f"Error analyzing portfolio: {str(e)}"
    
    @staticmethod
    @tool("enhanced_stock_data_tool")
    def enhanced_stock_data_tool(ticker: str, period: str = "5d"):
        """ Get comprehensive stock data including price, volume, and technical indicators. """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                return f"No data available for {ticker}"
            
            latest = data.iloc[-1]
            previous = data.iloc[-2] if len(data) > 1 else latest
            
            # Calculate technical indicators
            price_change = latest['Close'] - previous['Close']
            price_change_pct = (price_change / previous['Close']) * 100
            volume_change = latest['Volume'] - previous['Volume']
            
            # Calculate simple moving averages
            sma_5 = data['Close'].tail(5).mean()
            sma_20 = data['Close'].tail(20).mean() if len(data) >= 20 else data['Close'].mean()
            
            result = {
                "ticker": ticker,
                "current_price": round(latest['Close'], 2),
                "price_change": round(price_change, 2),
                "price_change_pct": round(price_change_pct, 2),
                "volume": int(latest['Volume']),
                "volume_change": int(volume_change),
                "sma_5": round(sma_5, 2),
                "sma_20": round(sma_20, 2),
                "high_52w": round(data['High'].max(), 2),
                "low_52w": round(data['Low'].min(), 2),
                "timestamp": latest.name.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error fetching enhanced data for {ticker}: {str(e)}"
    
    @staticmethod
    @tool("market_news_tool")
    def market_news_tool(ticker: str = None, limit: int = 10):
        """ Fetch recent financial news for a specific ticker or general market news. """
        try:
            api_key = os.getenv("NEWS_API_KEY")
            if not api_key:
                return "News API key not found. Please set NEWS_API_KEY in your environment variables."
            
            base_url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": limit
            }
            
            if ticker:
                params["q"] = f"{ticker} stock OR {ticker} earnings OR {ticker} financial"
            else:
                params["q"] = "stock market OR financial news OR market analysis"
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                return f"No recent news found for {ticker if ticker else 'market'}"
            
            news_summary = []
            for article in articles[:limit]:
                news_item = {
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "source": article.get("source", {}).get("name", "")
                }
                news_summary.append(news_item)
            
            return json.dumps(news_summary, indent=2)
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    
    @staticmethod
    @tool("market_sentiment_tool")
    def market_sentiment_tool(tickers: List[str]):
        """ Analyze market sentiment for multiple tickers using news and price data. """
        try:
            sentiment_data = []
            
            for ticker in tickers:
                # Get recent price data
                stock = yf.Ticker(ticker)
                data = stock.history(period="5d")
                
                if data.empty:
                    continue
                
                # Calculate price momentum
                latest_price = data['Close'].iloc[-1]
                price_5d_ago = data['Close'].iloc[0]
                momentum = ((latest_price - price_5d_ago) / price_5d_ago) * 100
                
                
                sentiment_item = {
                    "ticker": ticker,
                    "current_price": round(latest_price, 2),
                    "momentum_5d": round(momentum, 2),
                    "sentiment_score": "positive" if momentum > 2 else "negative" if momentum < -2 else "neutral"
                }
                sentiment_data.append(sentiment_item)
            
            return json.dumps(sentiment_data, indent=2)
        except Exception as e:
            return f"Error analyzing market sentiment: {str(e)}"
    
    @staticmethod
    @tool("sector_analysis_tool")
    def sector_analysis_tool(sector: str = None):
        """ Analyze sector performance and trends. """
        try:
            # Define sector ETFs for analysis
            sector_etfs = {
                "technology": "XLK",
                "healthcare": "XLV", 
                "financial": "XLF",
                "consumer_discretionary": "XLY",
                "consumer_staples": "XLP",
                "energy": "XLE",
                "industrials": "XLI",
                "materials": "XLB",
                "utilities": "XLU",
                "real_estate": "XLRE",
                "communication": "XLC"
            }
            
            if sector and sector.lower() in sector_etfs:
                ticker = sector_etfs[sector.lower()]
            else:
                # Analyze all sectors
                ticker = "SPY"  # S&P 500 as baseline
            
            stock = yf.Ticker(ticker)
            data = stock.history(period="30d")
            
            if data.empty:
                return f"No data available for sector analysis"
            
            # Calculate sector metrics
            current_price = data['Close'].iloc[-1]
            month_ago_price = data['Close'].iloc[0]
            monthly_return = ((current_price - month_ago_price) / month_ago_price) * 100
            
            volatility = data['Close'].pct_change().std() * 100
            
            sector_analysis = {
                "sector": sector or "overall_market",
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "monthly_return": round(monthly_return, 2),
                "volatility": round(volatility, 2),
                "trend": "bullish" if monthly_return > 2 else "bearish" if monthly_return < -2 else "sideways"
            }
            
            return json.dumps(sector_analysis, indent=2)
        except Exception as e:
            return f"Error analyzing sector: {str(e)}"