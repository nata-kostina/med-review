from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LlmDocumentExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    age: str | None
    diagnosis: str | None
    dob: str | None
    doctor_id: str | None
    doctor_name: str | None
    hospital: str | None
    patient_name: str | None
    recorded_date: str | None
    sex: str | None
    ssn: str | None

ComparisonStatus = Literal[
    "match",
    "different",
    "missing_in_llm",
    "missing_in_document_intelligence",
    "missing_in_both",
]


class FieldComparison(BaseModel):
    field: str
    label: str
    status: ComparisonStatus
    document_intelligence_value: str | None
    llm_value: str | None


class DocumentReview(BaseModel):
    extraction: LlmDocumentExtraction | None = None
    comparisons: list[FieldComparison] = Field(default_factory=list)
    fallback_fields: list[FieldComparison] = Field(default_factory=list)
    error_message: str | None = None