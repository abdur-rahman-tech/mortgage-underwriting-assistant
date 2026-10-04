
from crewai import Agent
from config.llm import llm

from tools.financial_calculator import calculate_financial_metrics_tool

def create_calculation_review_agent() -> Agent:
    return Agent(
        role="Mortgage Financial Calculation Reviewer",
        goal=(
            "Review financial inputs and use the deterministic Python calculation tool "
            "to compute income, obligations, DTI, LTV, and estimated closing funds."
        ),
        backstory=(
            "You are a careful financial analyst. You never rely on mental arithmetic. "
            "You use the calculation tool, show the inputs, identify missing values, and "
            "flag inconsistencies."
        ),
        tools=[calculate_financial_metrics_tool],
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
