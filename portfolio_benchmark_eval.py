
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
import asyncio
from langsmith import Client
from langchain_openai import ChatOpenAI
from crew import PortfolioManager

portfolio_manager = PortfolioManager()
crew = portfolio_manager.portfolio_management_crew()

dataset_name = "Portfolio Manager Benchmark Dataset"

# --- Target function ---
async def run_portfolio_agent(inputs: dict) -> dict:
    """Run Portfolio Manager Crew and track the final response."""
    result = await crew.kickoff_async(inputs={"portfolio_json": inputs["portfolio"]})

    
    return {"analysis_report": result}

# --- LLM-as-judge ---
grader_instructions = """You are a financial evaluator grading an AI portfolio analysis.

You will be given:
- PORTFOLIO INPUT (the user's holdings),
- GROUND TRUTH ANALYSIS (the expected structure and logic of the analysis),
- STUDENT ANALYSIS (the agent's generated analysis).

Evaluate section by section:

1. **Performance (calculations)**  
   - Verify per-holding gain/loss and percentage are correct.  
   - Verify total portfolio value, total gain/loss, and gain/loss percentage.  
   - Allow small differences (≤ 1% deviation).  
   - Mark False only if there are significant or repeated miscalculations.

2. **Risk Assessment**  
   - Check if diversification and risk are consistent with the input.  
   - Extra commentary is fine if factually correct.

3. **Recommendations**  
   - Should be reasonable financial advice.  
   - Wording may differ.

4. **Market Insights**  
   - Should include trends and economic indicators relevant to the portfolio.  
   - Reasonable commentary is acceptable.

5. **Financial Concepts**  
   - Should explain gain/loss, diversification, or similar relevant concepts.  
   - Must be factually correct.

6. **Overall Judgment**  
   - "Excellent" = All or nearly all sections correct.  
   - "Good" = Most sections correct, one has errors.  
   - "Needs Improvement" = Multiple sections incorrect or contradictory.

Output JSON with fields: performance, risk, recommendations, insights, concepts, overall, reasoning.
"""



class SectionGrade(TypedDict):
    performance: Annotated[bool, ..., "True if performance calculations are correct, False otherwise."]
    risk: Annotated[bool, ..., "True if risk/diversification assessment is correct, False otherwise."]
    recommendations: Annotated[bool, ..., "True if recommendations are reasonable, False otherwise."]
    insights: Annotated[bool, ..., "True if market insights are reasonable, False otherwise."]
    concepts: Annotated[bool, ..., "True if financial concepts are explained correctly."]
    overall: Annotated[str, ..., "A summary judgment like 'Excellent', 'Good', 'Needs Improvement' based on section-level results."]
    reasoning: Annotated[str, ..., "Step-by-step reasoning showing how each section was evaluated."]



grader_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(
    SectionGrade, method="json_schema", strict=True
)


# --- Evaluator ---
async def analysis_multiscore(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """Evaluate CrewAI analysis section by section."""
    user = f"""PORTFOLIO INPUT: {inputs['portfolio']}
GROUND TRUTH ANALYSIS: {reference_outputs['analysis_report']}
STUDENT ANALYSIS: {outputs['analysis_report']}"""

    grade = await grader_llm.ainvoke(
        [{"role": "system", "content": grader_instructions}, {"role": "user", "content": user}]
    )
    results = [
        {"key": "performance", "score": 1.0 if grade["performance"] else 0.0},
        {"key": "risk", "score": 1.0 if grade["risk"] else 0.0},
        {"key": "recommendations", "score": 1.0 if grade["recommendations"] else 0.0},
        {"key": "insights", "score": 1.0 if grade["insights"] else 0.0},
        {"key": "concepts", "score": 1.0 if grade["concepts"] else 0.0},
        {"key": "overall", "value": grade["overall"]},
        {"key": "reasoning", "value": grade["reasoning"]},
    ]
    return results

async def main():
    client = Client()

    experiment_results = await client.aevaluate(
        run_portfolio_agent,
        data="Portfolio Manager Benchmark Dataset",  # dataset name you registered earlier
        evaluators=[analysis_multiscore],
        experiment_prefix="portfolio-Manager-Phaese-1",
        num_repetitions=1,
        max_concurrency=4,
    )

    # Optional: inspect results
    df = experiment_results.to_pandas()
    print(df.head())


    # --- Convert results to DataFrame ---
    df_results = experiment_results.to_pandas()
    print(df_results)
    # Save to CSV
    df_results.to_csv("portfolio_benchmark_results.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())