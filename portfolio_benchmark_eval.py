
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
import asyncio
import json
import time
from datetime import datetime
from langsmith import Client
from langchain_openai import ChatOpenAI
from crew import PortfolioManager

# Future-proof evaluation metrics - no phase-specific configuration needed
# The system will automatically detect capabilities and evaluate accordingly

portfolio_manager = PortfolioManager()
crew = portfolio_manager.portfolio_management_crew()

dataset_name = "Portfolio Manager Benchmark Dataset"


# --- Future-proof target function ---
async def run_portfolio_agent(inputs: dict, phase: str = "Phase-1") -> dict:
    """Run Portfolio Manager Crew and automatically detect capabilities."""
    start_time = time.time()

    try:
        # Extract portfolio data
        portfolio = inputs["portfolio"]
        portfolio_tickers = [h['ticker'] for h in portfolio['holdings']]

        # Prepare input data
        input_data = {
            "portfolio_json": portfolio,
            "portfolio_tickers": portfolio_tickers
        }

        # Run the crew analysis with tracing
        result = await crew.kickoff_async(inputs=input_data)

        # --- Build a simple trace (for capability detection) ---
        trace = {
            "agents_used": [agent.__class__.__name__ for agent in crew.agents],
            "tools_called": [tool.name for agent in crew.agents for tool in getattr(agent, "tools", [])]
        }

        # Calculate runtime metrics
        duration = time.time() - start_time
        estimated_input_tokens = len(str(portfolio)) // 4 + 1000
        estimated_output_tokens = len(str(result)) // 4 if result else 500

        # Detect system capabilities using trace + result
        capabilities = _detect_system_capabilities(result, portfolio_tickers, trace=trace)

        return {
            "analysis_report": result,
            "system_metrics": {
                "phase": phase,
                "duration_seconds": round(duration, 4),
                "input_tokens": estimated_input_tokens,
                "output_tokens": estimated_output_tokens,
                "total_tokens": estimated_input_tokens + estimated_output_tokens,
                "timestamp": datetime.now().isoformat(),
                "detected_capabilities": capabilities,
                "execution_success": "Success",
                "trace": trace  # 👈 include raw trace for debugging
            }
        }

    except Exception as e:
        return {
            "analysis_report": None,
            "system_metrics": {
                "phase": phase,
                "error": str(e),
                "duration_seconds": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
                "detected_capabilities": {},
                "execution_success": "Failed",
                "trace": {}
            }
        }


def _detect_system_capabilities(result, portfolio_tickers, trace: dict = None):
    """
    Auto-detect system capabilities using:
    1. Execution trace / metadata (preferred)
    2. Output heuristics (fallback)
    """

    # Default structure
    capabilities = {
        "has_market_data": 0,
        "has_news_analysis": 0,
        "has_sentiment_analysis": 0,
        "has_sector_analysis": 0,
        "has_technical_analysis": 0,
        "has_risk_assessment": 0,
        "has_recommendations": 0,
        "has_multiple_agents": 0,
        "has_rag_capabilities": 0,
        "has_mcp_integration": 0,
        "data_accuracy_level": "basic",   # basic, enhanced, advanced
        "analysis_depth": "shallow",      # shallow, moderate, deep
        "hallucination_risk": "high",     # high, medium, low
        "llm_call_efficiency": "low"      # low, medium, high
    }

    # === 1. Execution trace detection (preferred) ===
    if trace:
        # Multi-agent detection
        if "agents_used" in trace and len(trace["agents_used"]) > 1:
            capabilities["has_multiple_agents"] = 1

        # RAG detection
        if "tools_called" in trace and any("retriever" in t for t in trace["tools_called"]):
            capabilities["has_rag_capabilities"] = 1

        # MCP / external API detection
        if "tools_called" in trace and any("mcp" in t or "api" in t for t in trace["tools_called"]):
            capabilities["has_mcp_integration"] = 1

    # === 2. Heuristic fallback (if no trace info) ===
    if result:
        result_str = str(result).lower()

        if any(k in result_str for k in ["current price", "market price", "stock data"]):
            capabilities["has_market_data"] = 1
            capabilities["data_accuracy_level"] = "enhanced"

        if any(k in result_str for k in ["news", "recent events", "headlines"]):
            capabilities["has_news_analysis"] = 1
            capabilities["analysis_depth"] = "moderate"

        if any(k in result_str for k in ["sentiment", "bullish", "bearish"]):
            capabilities["has_sentiment_analysis"] = 1
            capabilities["analysis_depth"] = "moderate"

        if any(k in result_str for k in ["sector", "industry", "sector performance"]):
            capabilities["has_sector_analysis"] = 1
            capabilities["analysis_depth"] = "moderate"

        if any(k in result_str for k in ["moving average", "sma", "technical indicator"]):
            capabilities["has_technical_analysis"] = 1
            capabilities["data_accuracy_level"] = "advanced"

        if any(k in result_str for k in ["risk", "diversification", "volatility", "beta"]):
            capabilities["has_risk_assessment"] = 1
            capabilities["analysis_depth"] = "moderate"

        if any(k in result_str for k in ["recommend", "suggest", "advice", "consider"]):
            capabilities["has_recommendations"] = 1

    # === 3. Adjust overall quality flags ===
    if capabilities["has_technical_analysis"] and capabilities["has_rag_capabilities"]:
        capabilities.update({
            "data_accuracy_level": "advanced",
            "analysis_depth": "deep",
            "hallucination_risk": "low",
            "llm_call_efficiency": "high"
        })
    elif capabilities["has_market_data"] and capabilities["has_news_analysis"]:
        capabilities.update({
            "data_accuracy_level": "enhanced",
            "analysis_depth": "moderate",
            "hallucination_risk": "medium",
            "llm_call_efficiency": "medium"
        })

    return capabilities

# --- Future-proof LLM-as-judge ---
grader_instructions = """You are a comprehensive financial evaluator grading an AI portfolio analysis system.

You will be given:
- PORTFOLIO INPUT (the user's holdings)
- GROUND TRUTH ANALYSIS (the expected structure and logic of the analysis)
- STUDENT ANALYSIS (the agent's generated analysis)
- SYSTEM METRICS (detected capabilities and performance data)

Evaluate the system comprehensively across all dimensions:

## CORE FINANCIAL ANALYSIS (40%)
1. **Performance Calculations** (10%)
   - Accuracy of gain/loss calculations per holding
   - Correctness of total portfolio value and percentages
   - Allow small differences (≤ 1% deviation)

2. **Risk Assessment** (10%)
   - Quality of diversification analysis
   - Appropriateness of risk evaluation
   - Consistency with portfolio characteristics

3. **Recommendations Quality** (10%)
   - Practicality and actionability of advice
   - Alignment with portfolio goals and risk profile
   - Reasonableness of financial recommendations

4. **Financial Concepts** (10%)
   - Accuracy of financial explanations
   - Clarity of complex concepts
   - Factual correctness of information

## SYSTEM CAPABILITIES (30%)
5. **Data Integration Quality** (10%)
   - How well real-time market data is integrated
   - Accuracy and relevance of external data sources
   - Currency and timing of data

6. **Analysis Depth** (10%)
   - Comprehensiveness of analysis
   - Depth of insights provided
   - Multi-dimensional analysis quality

7. **Market Context Integration** (10%)
   - Relevance of market insights
   - Quality of news and sentiment analysis
   - Sector and economic indicator integration

## SYSTEM PERFORMANCE (20%)
8. **Execution Efficiency** (10%)
   - Speed of analysis completion
   - Resource utilization (tokens, calls)
   - System responsiveness

9. **Reliability & Consistency** (10%)
   - Consistency of results across runs
   - Error handling and recovery
   - System stability

## ADVANCED CAPABILITIES (10%)
10. **Multi-Agent Coordination** (5%)
    - Quality of agent collaboration
    - Task distribution efficiency
    - Information sharing between agents

11. **Hallucination Control** (5%)
    - Factual accuracy of generated content
    - Consistency with real data
    - Minimization of made-up information

## OVERALL ASSESSMENT
- "Excellent" = All sections perform well, advanced capabilities present
- "Good" = Most sections correct, some advanced features
- "Satisfactory" = Basic functionality works, limited advanced features
- "Needs Improvement" = Multiple issues, basic functionality problems

Output JSON with all evaluation fields and reasoning.
"""



class ComprehensiveGrade(TypedDict):
    # Core Financial Analysis (40%)
    performance_calculations: Annotated[float, ..., "Score 0-1 for performance calculation accuracy"]
    risk_assessment: Annotated[float, ..., "Score 0-1 for risk assessment quality"]
    recommendations_quality: Annotated[float, ..., "Score 0-1 for recommendations quality"]
    financial_concepts: Annotated[float, ..., "Score 0-1 for financial concepts explanation"]
    
    # System Capabilities (30%)
    data_integration_quality: Annotated[float, ..., "Score 0-1 for data integration quality"]
    analysis_depth: Annotated[float, ..., "Score 0-1 for analysis depth and comprehensiveness"]
    market_context_integration: Annotated[float, ..., "Score 0-1 for market context integration"]
    
    # System Performance (20%)
    execution_efficiency: Annotated[float, ..., "Score 0-1 for execution efficiency"]
    reliability_consistency: Annotated[float, ..., "Score 0-1 for reliability and consistency"]
    
    # Advanced Capabilities (10%)
    multi_agent_coordination: Annotated[float, ..., "Score 0-1 for multi-agent coordination"]
    hallucination_control: Annotated[float, ..., "Score 0-1 for hallucination control"]
    
    # Overall Assessment
    overall_score: Annotated[float, ..., "Overall weighted score 0-1"]
    overall_grade: Annotated[str, ..., "Overall grade: Excellent, Good, Satisfactory, Needs Improvement"]
    reasoning: Annotated[str, ..., "Comprehensive reasoning for all scores"]
    phase_analysis: Annotated[str, ..., "Analysis of phase-specific strengths and weaknesses"]
    improvement_suggestions: Annotated[str, ..., "Specific suggestions for improvement"]



grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(
    ComprehensiveGrade, method="json_schema", strict=True
)


# --- Future-proof Comprehensive Evaluator ---
async def analysis_multiscore(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """Comprehensive evaluation that works for all phases without modification."""
    system_metrics = outputs.get("system_metrics", {})
    phase = system_metrics.get("phase", "Unknown")
    capabilities = system_metrics.get("detected_capabilities", {})
    
    user = f"""PORTFOLIO INPUT: {inputs['portfolio']}
GROUND TRUTH ANALYSIS: {reference_outputs.get('analysis_report', 'N/A')}
STUDENT ANALYSIS: {outputs.get('analysis_report', 'N/A')}
SYSTEM METRICS: {system_metrics}
DETECTED CAPABILITIES: {capabilities}

Evaluate this {phase} system comprehensively. The system has the following detected capabilities:
- Market Data: {capabilities.get('has_market_data', False)}
- News Analysis: {capabilities.get('has_news_analysis', False)}
- Sentiment Analysis: {capabilities.get('has_sentiment_analysis', False)}
- Sector Analysis: {capabilities.get('has_sector_analysis', False)}
- Technical Analysis: {capabilities.get('has_technical_analysis', False)}
- Risk Assessment: {capabilities.get('has_risk_assessment', False)}
- Multiple Agents: {capabilities.get('has_multiple_agents', False)}
- RAG Capabilities: {capabilities.get('has_rag_capabilities', False)}
- MCP Integration: {capabilities.get('has_mcp_integration', False)}

Data Accuracy Level: {capabilities.get('data_accuracy_level', 'basic')}
Analysis Depth: {capabilities.get('analysis_depth', 'shallow')}
Hallucination Risk: {capabilities.get('hallucination_risk', 'high')}
LLM Call Efficiency: {capabilities.get('llm_call_efficiency', 'low')}

Evaluate the system based on what it CAN do, not what it should do."""

    grade = await grader_llm.ainvoke(
        [{"role": "system", "content": grader_instructions}, {"role": "user", "content": user}]
    )
    
    results = [
        # Core Financial Analysis (40%)
        {"key": "performance_calculations", "score": grade["performance_calculations"]},
        {"key": "risk_assessment", "score": grade["risk_assessment"]},
        {"key": "recommendations_quality", "score": grade["recommendations_quality"]},
        {"key": "financial_concepts", "score": grade["financial_concepts"]},
        
        # System Capabilities (30%)
        {"key": "data_integration_quality", "score": grade["data_integration_quality"]},
        {"key": "analysis_depth", "score": grade["analysis_depth"]},
        {"key": "market_context_integration", "score": grade["market_context_integration"]},
        
        # System Performance (20%)
        {"key": "execution_efficiency", "score": grade["execution_efficiency"]},
        {"key": "reliability_consistency", "score": grade["reliability_consistency"]},
        
        # Advanced Capabilities (10%)
        {"key": "multi_agent_coordination", "score": grade["multi_agent_coordination"]},
        {"key": "hallucination_control", "score": grade["hallucination_control"]},
        
        # Overall Assessment
        {"key": "overall_score", "score": grade["overall_score"]},
        {"key": "overall_grade", "value": grade["overall_grade"]},
        {"key": "reasoning", "value": grade["reasoning"]},
        {"key": "phase_analysis", "value": grade["phase_analysis"]},
        {"key": "improvement_suggestions", "value": grade["improvement_suggestions"]},
        
        # System Metadata
        {"key": "phase", "value": phase},
        {"key": "duration_seconds", "score": system_metrics.get("duration_seconds", 0)},
        {"key": "total_tokens", "score": system_metrics.get("total_tokens", 0)},
        {"key": "execution_success", "value": system_metrics.get("execution_success", "Failed")},
        
        # Detected Capabilities
        {"key": "has_market_data", "score": capabilities.get("has_market_data", False)},
        {"key": "has_news_analysis", "score": capabilities.get("has_news_analysis", False)},
        {"key": "has_sentiment_analysis", "score": capabilities.get("has_sentiment_analysis", False)},
        {"key": "has_sector_analysis", "score": capabilities.get("has_sector_analysis", False)},
        {"key": "has_technical_analysis", "score": capabilities.get("has_technical_analysis", False)},
        {"key": "has_risk_assessment", "score": capabilities.get("has_risk_assessment", False)},
        {"key": "has_multiple_agents", "score": capabilities.get("has_multiple_agents", False)},
        {"key": "has_rag_capabilities", "score": capabilities.get("has_rag_capabilities", False)},
        {"key": "has_mcp_integration", "score": capabilities.get("has_mcp_integration", False)},
        {"key": "data_accuracy_level", "value": capabilities.get("data_accuracy_level", "basic")},
        {"key": "analysis_depth", "value": capabilities.get("analysis_depth", "shallow")},
        {"key": "hallucination_risk", "value": capabilities.get("hallucination_risk", "high")},
        {"key": "llm_call_efficiency", "value": capabilities.get("llm_call_efficiency", "low")},
    ]
    return results

async def run_phase_evaluation(phase: str = "Phase-1", num_repetitions: int = 3):
    """Run evaluation for a specific phase."""
    client = Client()
    
    print(f"Running {phase} evaluation...")
    
    # Create phase-specific function
    async def run_phase_agent(inputs: dict) -> dict:
        return await run_portfolio_agent(inputs, phase)
    
    experiment_results = await client.aevaluate(
        run_phase_agent,
        data=dataset_name,
        evaluators=[analysis_multiscore],
        experiment_prefix=f"portfolio-manager-{phase.lower().replace('-', '_')}",
        num_repetitions=num_repetitions,
        max_concurrency=2,
    )


async def main():
    """Main function - run single phase evaluation."""
    # Run Phase-2 evaluation (current phase)
    await run_phase_evaluation("Phase-2", num_repetitions=1)


if __name__ == "__main__":
    asyncio.run(main())