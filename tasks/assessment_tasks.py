
from crewai import Task

def create_assessment_task(agent, document_task, policy_task, calculation_task) -> Task:
    return Task(
        description="""
Prepare a PROPOSED underwriting assessment using all previous task outputs.

The result must include:
1. Overall proposed status: READY FOR HUMAN REVIEW, CONDITIONAL REVIEW, or INSUFFICIENT INFORMATION.
2. Key strengths supported by evidence.
3. Key risks/concerns.
4. Policy considerations.
5. Conditions required before a human underwriter can finalize the file.
6. Unresolved questions.
7. Evidence and policy citations used.

Never say that the system has approved or denied the mortgage.
Do not introduce facts that are not in the previous task outputs.
""",
        expected_output="A proposed underwriting assessment and conditions.",
        agent=agent,
        context=[document_task, policy_task, calculation_task],
    )
