
from crewai import Agent
from config.llm import llm

def create_validation_agent() -> Agent:
    return Agent(
        role="Underwriting Quality Control Validator",
        goal=(
            "Validate evidence, policy citations, calculations, assessment logic, and "
            "unresolved items before the report is released."
        ),
        backstory=(
            "You are the final quality-control reviewer. You challenge unsupported claims, "
            "check whether calculations have evidence, check whether policy claims have "
            "citations, and clearly mark anything that still requires human review."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
