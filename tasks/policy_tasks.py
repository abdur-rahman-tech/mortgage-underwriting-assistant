
from crewai import Task

def create_policy_task(agent, document_task) -> Task:
    return Task(
        description="""
Using the document review in the previous task, identify the policy questions that
must be checked for this application.

Loan program: {loan_program}

Use the policy search tool to retrieve the most relevant policy passages.

Return:
1. Applicable requirements.
2. Applicable exceptions.
3. Policy conflicts.
4. Coverage gaps / insufficient evidence.
5. Exact policy citations returned by the policy library.
6. A short explanation of how each policy item relates to the borrower facts.

Rules:
- Use only evidence returned by the policy library.
- Never invent policy.
- If no adequate policy evidence is found, say "INSUFFICIENT POLICY EVIDENCE".
""",
        expected_output="A policy review with citations and evidence gaps.",
        agent=agent,
        context=[document_task],
    )
