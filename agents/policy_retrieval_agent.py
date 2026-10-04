
from crewai import Agent
from config.llm import llm

from tools.policy_search import policy_search_tool

def create_policy_retrieval_agent() -> Agent:
    return Agent(
        role="Mortgage Policy Retrieval Specialist",
        goal=(
            "Retrieve and interpret only relevant policy evidence from the supplied "
            "FAISS policy library. Identify requirements, exceptions, coverage gaps, "
            "and policy conflicts."
        ),
        backstory=(
            "You are a policy research specialist. You never invent a lending rule. "
            "If the policy library does not provide enough evidence, you explicitly say "
            "that policy evidence is insufficient."
        ),
        tools=[policy_search_tool],
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
