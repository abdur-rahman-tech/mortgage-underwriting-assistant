
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Evidence:
    fact: str
    source: str
    page: Optional[int] = None
    confidence: Optional[float] = None


@dataclass
class UnderwritingResult:
    document_review: str
    policy_review: str
    calculation_review: str
    assessment: str
    validation: str
    raw: str = field(repr=False)
