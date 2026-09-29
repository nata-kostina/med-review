from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.document_review.schemas import DocumentReview
from app.schemas.document.model import DocumentExtraction

FieldSource = Literal["document_intelligence", "llm_fallback", "human"]
IssueSeverity = Literal["error", "warning"]
DocumentStatus = Literal[
    "processing",
    "ready",
    "needs_review",
    "approved",
    "rejected",
    "failed",
]

class ReviewData(BaseModel):
    age: Decimal | None
    diagnosis: str | None
    dob: date | None
    doctor_id: str | None
    doctor_name: str | None
    hospital: str | None
    patient_name: str | None
    recorded_date: date | None
    sex: str | None
    ssn: str | None
    field_confidence: dict[str, float] = Field(default_factory=dict)
    field_sources: dict[str, FieldSource] = Field(default_factory=dict)
    
class ValidationIssue(BaseModel):
    code: str
    field: str | None
    severity: IssueSeverity
    message: str
    
class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    original_filename: str
    content_type: str
    status: DocumentStatus
    
    extraction: DocumentExtraction | None = None
    review: DocumentReview | None = None
    validation: dict[str, Any] | None = None
    review_data: ReviewData | None = None
    issues: list[ValidationIssue] = Field(default_factory=list)
    supplier_action_required: bool = False
    error_message: str | None = None
    
    created_at: datetime
    updated_at: datetime
    
class DocumentCorrectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    age: Decimal | None
    diagnosis: str | None
    dob: date | None
    doctor_id: str | None
    doctor_name: str | None
    hospital: str | None
    patient_name: str | None
    recorded_date: date | None
    sex: str | None
    ssn: str | None
    
class DecisionRequest(BaseModel):
    decision: Literal["approved", "rejected"]