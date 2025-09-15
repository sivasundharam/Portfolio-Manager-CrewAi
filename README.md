# Portfolio-Manager-CrewAi

---

## AI-Powered Portfolio Management System

## Phase 2: Few Agents + Tools
### Overview
An advanced AI-powered portfolio management system using CrewAI with multiple specialized agents, real-time market data integration, news analysis, and comprehensive evaluation capabilities.

### Features

#### Multi-Agent Architecture
- **PortfolioAnalyzer**: Analyzes investment portfolios, assesses performance and risk
- **MarketTrendAnalyzer**: Analyzes market trends, news sentiment, and market conditions

#### Real-Time Market Data
- Enhanced stock price API with technical indicators
- Market sentiment analysis
- Sector performance analysis
- News fetching and analysis

#### Advanced Tools
- `enhanced_stock_data_tool`: Comprehensive stock data with technical indicators
- `market_news_tool`: Financial news fetching and analysis
- `market_sentiment_tool`: Multi-ticker sentiment analysis
- `sector_analysis_tool`: Sector performance and trend analysis
- `portfolio_analysis_tool`: Portfolio summary and analysis

#### Comprehensive Evaluation
- **LangSmith Integration**: Centralized evaluation and phase comparison
- **Future-Proof Design**: Works for any phase without modification
- **Automatic Capability Detection**: Detects system capabilities automatically
- **Multi-Dimensional Metrics**: 11 comprehensive evaluation categories
- **Phase Comparison**: Easy comparison across different system versions

### Configuration

#### Agents (`config/agents.yaml`)
- **PortfolioAnalyzer**: Portfolio analysis and investment advice
- **MarketTrendAnalyzer**: Market trends and news analysis

#### Tasks (`config/tasks.yaml`)
- **AnalyzePortfolioTask**: Comprehensive portfolio analysis
- **AnalyzeMarketTrendsTask**: Market trend and sentiment analysis

### API Integration

#### News API (Optional)
To enable news fetching features, get a free API key from [NewsAPI](https://newsapi.org/) and add it to your `.env` file.

#### Stock Data
Uses Yahoo Finance (yfinance) for real-time stock data - no API key required.

### Evaluation & Phase Comparison

The system includes a **future-proof evaluation framework** with LangSmith integration:

#### **Future-Proof Design**
- **No Phase-Specific Code**: Works for any phase without modification
- **Automatic Capability Detection**: Detects what the system can do
- **Comprehensive Metrics**: 11 evaluation categories covering all aspects
- **LangSmith Integration**: Centralized storage and visualization

#### **Evaluation Categories (11 Total)**
- **Core Financial Analysis (40%)**: Performance, Risk, Recommendations, Concepts
- **System Capabilities (30%)**: Data Integration, Analysis Depth, Market Context
- **System Performance (20%)**: Execution Efficiency, Reliability
- **Advanced Capabilities (10%)**: Multi-Agent Coordination, Hallucination Control

#### **Automatic Detection**
- Market data integration
- News analysis capabilities
- Sentiment analysis
- Sector analysis
- Technical analysis
- Risk assessment
- Multiple agents
- RAG capabilities
- MCP integration

### Tech Stack
- **Python 3.10+**
- **CrewAI**: Multi-agent orchestration
- **LangChain**: LLM integration and tracing
- **OpenAI**: GPT models for analysis
- **yfinance**: Real-time stock data
- **NewsAPI**: Financial news integration
- **pandas**: Data analysis and reporting

### Evaluation Metrics

The system provides comprehensive evaluation across 11 categories:

#### **Core Financial Analysis (40%)**
- **Performance Calculations**: Accuracy of financial calculations
- **Risk Assessment**: Quality of risk evaluation and diversification analysis
- **Recommendations Quality**: Practicality and actionability of advice
- **Financial Concepts**: Accuracy of financial explanations

#### **System Capabilities (30%)**
- **Data Integration Quality**: How well external data is integrated
- **Analysis Depth**: Comprehensiveness of analysis
- **Market Context Integration**: Relevance of market insights

#### **System Performance (20%)**
- **Execution Efficiency**: Speed and resource usage
- **Reliability & Consistency**: System stability and consistency

#### **Advanced Capabilities (10%)**
- **Multi-Agent Coordination**: How well agents work together
- **Hallucination Control**: Factual accuracy and consistency

### Future-Proof Benefits

#### **Zero Maintenance for New Phases**
- Add Phase 6, 7, 8+ without touching evaluation code
- New capabilities automatically detected
- Evaluation adapts to new features

#### **Comprehensive Coverage**
- Covers all aspects of portfolio analysis
- Includes advanced AI capabilities
- Tracks system performance metrics

#### **LangSmith Integration**
- Centralized storage and visualization
- Team collaboration features
- Historical analysis capabilities
- Real-time monitoring

#### **Scalable Design**
- Handles any number of phases
- Adapts to new technologies
- Future-proof architecture

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Update tests and documentation
5. Submit a pull request

### License

This project is licensed under the MIT License.

---
