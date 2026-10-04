
from crewai import Agent
from config.llm import llm

def create_document_review_agent() -> Agent:
    return Agent(
        role="Mortgage Document Review Specialist",
        goal=(
            "Extract borrower facts from supplied application documents, identify "
            "missing information and conflicts, and attach precise evidence references."
        ),
        backstory=(
            "You are a meticulous mortgage document reviewer. You never invent a fact. "
            "You distinguish stated facts from assumptions and always identify the source "
            "document and page when that information is available."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
