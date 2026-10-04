
from datetime import datetime


def build_report(result: dict) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return f"""# Mortgage Underwriting Assistant Report

**Generated:** {timestamp}

> **Human review required.** This report is AI-generated decision support and is not a loan approval or denial.

## 1. Document Review

{result["document_review"]}

## 2. Policy Review

{result["policy_review"]}

## 3. Calculation Review

{result["calculation_review"]}

## 4. Proposed Underwriting Assessment

{result["assessment"]}

## 5. Final Validation

{result["validation"]}

---

## Human Underwriter Checklist

- [ ] Verify all borrower facts against original documents.
- [ ] Verify policy version and applicability.
- [ ] Recheck financial calculations.
- [ ] Resolve all material conflicts and missing documents.
- [ ] Confirm final underwriting decision through the authorized human process.
"""


def save_report(result: dict, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(build_report(result))
