
from crewai import Task

def create_document_task(agent) -> Task:
    return Task(
        description="""
Review the following mortgage application material.

LOAN PROGRAM:
{loan_program}

APPLICATION TEXT:
{application_text}

Produce a concise but detailed document-review result containing:
1. Borrower facts.
2. Financial facts.
3. Property and loan facts.
4. Missing information.
5. Conflicts or discrepancies.
6. Evidence references (document name/page/section when available).
7. Facts that could not be verified.

Rules:
- Never invent a fact.
- Do not make an approval/denial decision.
- Clearly distinguish evidence from inference.
- If a page is unavailable, say so.
""",
        expected_output="A structured markdown document-review report.",
        agent=agent,
    )
