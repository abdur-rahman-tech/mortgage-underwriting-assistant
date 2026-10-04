
from crewai import Task

def create_calculation_task(agent, document_task) -> Task:
    return Task(
        description="""
Review the borrower facts from the document review.

Use the Python financial calculation tool with the values supported by the evidence.
Calculate, when possible:
- gross monthly income
- other monthly income
- total monthly obligations
- DTI
- LTV
- estimated closing funds

Required behavior:
- Use the calculation tool instead of mental arithmetic.
- If an input is missing, leave that metric unavailable and explain why.
- Show calculation inputs and outputs.
- Flag contradictory source values.
- Do not decide loan approval.

The optional UI inputs are:
Property value: {property_value}
Loan amount: {loan_amount}
Proposed housing payment: {proposed_housing_payment}
""",
        expected_output="A deterministic calculation review with inputs, outputs, and flags.",
        agent=agent,
        context=[document_task],
    )
