from datetime import date
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.document_review.schemas import DocumentReview
from app.documents.models import DocumentRecord
from app.documents.schemas import DocumentStatus, ReviewData, ValidationIssue
from app.documents.validation import normalize_recorded_date, normalize_ssn
from app.schemas.document.model import DocumentExtraction


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get(self, record_id: str) -> DocumentRecord | None:
        return self.session.get(DocumentRecord, record_id)
    
    def list(self) -> list[DocumentRecord]:
        statement = select(DocumentRecord).order_by(
            DocumentRecord.created_at.desc(), DocumentRecord.id.desc()
        )
        return list(self.session.scalars(statement))
    
    def create_processing_document(
        self,
        *,
        record_id: str,
        original_filename: str,
        stored_filename: str,
        content_type: str,
    ) -> DocumentRecord:
        record = DocumentRecord(
            id=record_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            content_type=content_type,
            status="processing",
            issues=[],
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record
    
    def save_result(
        self,
        record_id: str,
        *,
        status: DocumentStatus,
        extraction: DocumentExtraction | None,
        validation: dict[str, Any] | None,
        review: DocumentReview | None,
        review_data: ReviewData | None,
        issues: list[ValidationIssue],
    ) -> DocumentRecord:
        record = self._require(record_id)
        record.status = status
        record.extraction = extraction.model_dump(mode="json") if extraction else None
        record.review = review.model_dump(mode="json") if review is not None else None
        record.validation = {
                "findings": [
                    issue.model_dump(mode="json") for issue in validation.get("issues", [])
                    ],
                "has_errors": validation.get("has_errors", False),
            } if validation else {}
        record.review_data = (
            review_data.model_dump(mode="json") 
                              if review_data is not None 
                              else None
            )
        record.issues = [issue.model_dump(mode="json") for issue in issues]
        record.error_message = None
        
        if review_data is not None:
            record.normalized_ssn = (
                normalize_ssn(review_data.ssn) if review_data.ssn else None
            )
            record.normalized_recorded_date = (
                normalize_recorded_date(review_data.recorded_date)
                if review_data.recorded_date
                else None
            )
        
        self._commit(record)
        return record
            
    def delete(self, record_id: str) -> None:
        record = self._require(record_id)
        self.session.delete(record)
        self.session.commit()
    
    def _require(self, record_id: str) -> DocumentRecord:
        record = self.get(record_id)
        if record is None:
            raise KeyError(record_id)
        return record
    
    def save_failure(self, record_id: str, message: str) -> DocumentRecord:
        record = self._require(record_id)
        record.status = "failed"
        record.error_message = message
        self._commit(record)
        return record
    
    def duplicate_exists(
        self,
        ssn: str,
        recorded_date: date,
        *,
        exclude_id: str | None = None
    ) -> bool:
        statement: Select[tuple[DocumentRecord]] = select(DocumentRecord).where(
            DocumentRecord.normalized_ssn == normalize_ssn(ssn),
            DocumentRecord.normalized_recorded_date == normalize_recorded_date(recorded_date),
            DocumentRecord.status != "rejected"
        )
        if exclude_id is not None:
            statement = statement.where(DocumentRecord.id != exclude_id)
        return self.session.scalar(statement.limit(1)) is not None
    
    def save_review(
        self,
        record_id: str,
        *,
        review_data: ReviewData,
        issues: list[ValidationIssue],
        status: DocumentStatus,
        review: DocumentReview | None = None,
    ) -> DocumentRecord:
        record = self._require(record_id)
        record.review_data = review_data.model_dump(mode="json")
        record.issues = [issue.model_dump(mode="json") for issue in issues]
        record.status = status
        record.validation = {
            "findings": [issue.model_dump(mode="json") for issue in issues],
            "has_errors": any(issue.severity == "error" for issue in issues),
        }
        if review is not None:
            record.review = review.model_dump(mode="json")
        record.error_message = None
        record.normalized_ssn = (
            normalize_ssn(review_data.ssn) if review_data.ssn else None
        )
        record.normalized_recorded_date = (
            normalize_recorded_date(review_data.recorded_date) 
            if review_data.recorded_date 
            else None
        )
        self._commit(record)
        return record
    
    def set_status(self, record_id: str, status: DocumentStatus) -> DocumentRecord:
        record = self._require(record_id)
        record.status = status
        self._commit(record)
        return record
        
    def _commit(self, record: DocumentRecord) -> None:
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)