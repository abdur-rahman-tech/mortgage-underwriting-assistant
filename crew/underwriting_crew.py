
from crewai import Crew, Process

from agents.document_review_agent import create_document_review_agent
from agents.policy_retrieval_agent import create_policy_retrieval_agent
from agents.calculation_review_agent import create_calculation_review_agent
from agents.assessment_agent import create_assessment_agent
from agents.validation_agent import create_validation_agent

from tasks.document_tasks import create_document_task
from tasks.policy_tasks import create_policy_task
from tasks.calculation_tasks import create_calculation_task
from tasks.assessment_tasks import create_assessment_task
from tasks.validation_tasks import create_validation_task


def build_underwriting_crew() -> Crew:
    document_agent = create_document_review_agent()
    policy_agent = create_policy_retrieval_agent()
    calculation_agent = create_calculation_review_agent()
    assessment_agent = create_assessment_agent()
    validation_agent = create_validation_agent()

    document_task = create_document_task(document_agent)
    policy_task = create_policy_task(policy_agent, document_task)
    calculation_task = create_calculation_task(calculation_agent, document_task)
    assessment_task = create_assessment_task(
        assessment_agent,
        document_task,
        policy_task,
        calculation_task,
    )
    validation_task = create_validation_task(
        validation_agent,
        document_task,
        policy_task,
        calculation_task,
        assessment_task,
    )

    return Crew(
        agents=[
            document_agent,
            policy_agent,
            calculation_agent,
            assessment_agent,
            validation_agent,
        ],
        tasks=[
            document_task,
            policy_task,
            calculation_task,
            assessment_task,
            validation_task,
        ],
        process=Process.sequential,
        verbose=False,
    )


def run_underwriting_crew(
    application_text: str,
    loan_program: str,
    property_value: float,
    loan_amount: float,
    proposed_housing_payment: float,
) -> dict:
    crew = build_underwriting_crew()

    result = crew.kickoff(
        inputs={
            "application_text": application_text,
            "loan_program": loan_program,
            "property_value": property_value,
            "loan_amount": loan_amount,
            "proposed_housing_payment": proposed_housing_payment,
        }
    )

    outputs = result.tasks_output

    # CrewAI returns task outputs in task order.
    return {
        "document_review": str(outputs[0]),
        "policy_review": str(outputs[1]),
        "calculation_review": str(outputs[2]),
        "assessment": str(outputs[3]),
        "validation": str(outputs[4]),
        "raw": str(result),
    }
