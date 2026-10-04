
import json
from typing import Optional

from crewai.tools import tool


def calculate_financial_metrics(
    gross_monthly_income: float,
    other_monthly_income: float = 0.0,
    existing_monthly_obligations: float = 0.0,
    proposed_housing_payment: float = 0.0,
    property_value: Optional[float] = None,
    loan_amount: Optional[float] = None,
    estimated_closing_costs: float = 0.0,
    borrower_cash_available: Optional[float] = None,
) -> dict:
    income = float(gross_monthly_income) + float(other_monthly_income)
    obligations = (
        float(existing_monthly_obligations)
        + float(proposed_housing_payment)
    )

    dti = None if income <= 0 else (obligations / income) * 100

    ltv = None
    if property_value and property_value > 0 and loan_amount is not None:
        ltv = (float(loan_amount) / float(property_value)) * 100

    estimated_cash_needed = None
    cash_gap = None
    if loan_amount is not None:
        # This is intentionally a simplified estimate for the prototype.
        down_payment = max(float(property_value or 0) - float(loan_amount), 0.0)
        estimated_cash_needed = down_payment + float(estimated_closing_costs)
        if borrower_cash_available is not None:
            cash_gap = estimated_cash_needed - float(borrower_cash_available)

    return {
        "gross_monthly_income": round(float(gross_monthly_income), 2),
        "other_monthly_income": round(float(other_monthly_income), 2),
        "total_monthly_income": round(income, 2),
        "existing_monthly_obligations": round(float(existing_monthly_obligations), 2),
        "proposed_housing_payment": round(float(proposed_housing_payment), 2),
        "total_monthly_obligations": round(obligations, 2),
        "dti_percent": None if dti is None else round(dti, 2),
        "property_value": property_value,
        "loan_amount": loan_amount,
        "ltv_percent": None if ltv is None else round(ltv, 2),
        "estimated_closing_costs": round(float(estimated_closing_costs), 2),
        "estimated_cash_needed": (
            None if estimated_cash_needed is None else round(estimated_cash_needed, 2)
        ),
        "borrower_cash_available": borrower_cash_available,
        "cash_gap": None if cash_gap is None else round(cash_gap, 2),
    }


@tool("calculate_financial_metrics")
def calculate_financial_metrics_tool(
    gross_monthly_income: float,
    other_monthly_income: float = 0.0,
    existing_monthly_obligations: float = 0.0,
    proposed_housing_payment: float = 0.0,
    property_value: Optional[float] = None,
    loan_amount: Optional[float] = None,
    estimated_closing_costs: float = 0.0,
    borrower_cash_available: Optional[float] = None,
) -> str:
    """Calculate deterministic mortgage financial metrics. Never use this tool for policy decisions."""
    return json.dumps(
        calculate_financial_metrics(
            gross_monthly_income=gross_monthly_income,
            other_monthly_income=other_monthly_income,
            existing_monthly_obligations=existing_monthly_obligations,
            proposed_housing_payment=proposed_housing_payment,
            property_value=property_value,
            loan_amount=loan_amount,
            estimated_closing_costs=estimated_closing_costs,
            borrower_cash_available=borrower_cash_available,
        ),
        indent=2,
    )
