
from crewai import Task

def create_validation_task(agent, document_task, policy_task, calculation_task, assessment_task) -> Task:
    return Task(
        description="""
Perform final quality control over all previous outputs.

Validate:
- borrower facts against evidence
- missing information
- conflicts
- financial calculations
- policy citations
- whether policy claims are actually supported
- whether the proposed assessment follows the evidence
- whether conditions address unresolved items

Return:
1. VALIDATION STATUS: PASS, REVIEW REQUIRED, or FAIL.
2. Evidence checks.
3. Calculation checks.
4. Policy/citation checks.
5. Assessment consistency checks.
6. Unresolved items.
7. Exact corrections needed, if any.

A PASS does not mean loan approval. It means the AI-generated report passed this
prototype's internal consistency checks.
""",
        expected_output="A final validation report suitable for human underwriting review.",
        agent=agent,
        context=[document_task, policy_task, calculation_task, assessment_task],
    )
