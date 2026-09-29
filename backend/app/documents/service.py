from pathlib import Path
from uuid import uuid4

from app.correction_email.base import CorrectionEmailDrafter
from app.correction_email.eligibility import supplier_fixable_issues
from app.correction_email.schemas import CorrectionEmailDraft
from app.document_review.base import DocumentReviewer
from app.document_review.schemas import DocumentReview
from app.documents.models import DocumentRecord
from app.documents.repository import DocumentRepository
from app.documents.schemas import (
    DocumentCorrectionRequest,
    ReviewData,
    ValidationIssue,
)
from app.documents.validation import status_for_issues, validate_review_data
from app.pipeline import build_default_pipeline
from app.services.document_intelligence_service import DocumentIntelligenceService


class DocumentNotFoundError(RuntimeError):
    pass

class DocumentProcessingError(RuntimeError):
    pass

class DocumentReviewConflictError(RuntimeError):
    pass


class DocumentService:
    def __init__(
        self,
        *,
        repository: DocumentRepository,
        min_confidence: float,
        upload_dir: Path,
        service: DocumentIntelligenceService,
        reviewer: DocumentReviewer,
        correction_email_drafter: CorrectionEmailDrafter | None = None,
    ) -> None:
        self.repository = repository
        self.min_confidence = min_confidence
        self.upload_dir = upload_dir
        self.service = service
        self.reviewer = reviewer
        self.correction_email_drafter = correction_email_drafter
        
    def get(self, record_id: str) -> DocumentRecord:
        record = self.repository.get(record_id)
        if record is None:
            raise DocumentNotFoundError("Document not found")
        return record
    
    def delete(self, record_id: str) -> None:
        record = self.repository.get(record_id)
        if record is None:
            raise DocumentNotFoundError(f"Document {record_id} was not found.")
        stored_path = self.upload_dir / Path(record.stored_filename).name
        self.repository.delete(record_id)
        stored_path.unlink(missing_ok=True)
        
    def process(
        self,
        *,
        original_filename: str,
        content_type: str,
        content: bytes,
        suffix: str
    ) -> DocumentRecord:
        record_id = str(uuid4())
        stored_filename = f"{record_id}{suffix}"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        stored_path = self.upload_dir / stored_filename
        stored_path.write_bytes(content)
        self.repository.create_processing_document(
            record_id=record_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            content_type=content_type
        )
        
        try:
            context = build_default_pipeline(
                service=self.service,
                reviewer=self.reviewer,
                content_type=content_type,
                min_confidence=self.min_confidence,
                is_duplicate_checker=lambda ssn, recorded_date: bool(
                    ssn 
                    and recorded_date
                    and self.repository.duplicate_exists(ssn, recorded_date)
                )
            ).run(stored_path)
        except Exception as error:
            message = str(error) or error.__class__.__name__
            self.repository.save_failure(record_id, message)
            raise DocumentProcessingError(message) from error
        
        issues = context.issues or []
        return self.repository.save_result(
            record_id,
            status=status_for_issues(issues),
            extraction=context.extraction,
            review=context.review,
            validation={
                "findings": issues,
                "has_errors": any(issue.severity == "error" for issue in issues),
            },
            review_data=context.review_data,
            issues=issues
        )

    def revalidate(self, record_id: str, corrections: DocumentCorrectionRequest) -> DocumentRecord:
        record = self.repository.get(record_id)
        if record is None:
            raise DocumentNotFoundError("Document not found")
        if record.status in {"approved", "rejected"}:
            raise DocumentReviewConflictError("A decided document cannot be edited.")
        
        saved_data = ReviewData.model_validate(record.review_data or {})
        corrected_fields = corrections.model_dump(exclude_unset=True)
        data = saved_data.model_copy(update=corrected_fields)
        field_sources = dict(saved_data.field_sources)
        for field, value in corrected_fields.items():
            if value != getattr(saved_data, field):
                field_sources[field] = "human"
        data = data.model_copy(update={"field_sources": field_sources})
        
        is_duplicate = bool(
            data.recorded_date
            and data.ssn
            and self.repository.duplicate_exists(
                data.ssn, data.recorded_date, exclude_id=record_id
            )
        )
        
        issues = validate_review_data(
            data,
            min_confidence=self.min_confidence,
            is_duplicate=is_duplicate
        )
        
        document_review = DocumentReview.model_validate(record.review)
        
        return self.repository.save_review(
            record_id,
            review_data=data,
            issues=issues,
            status=status_for_issues(issues),
            review=document_review,
        )
        
    def decide(self, record_id: str, decision: str) -> DocumentRecord:
        record = self.repository.get(record_id)
        if record is None:
            raise DocumentNotFoundError("Document not found")
        if record.status in {"approved", "rejected"}:
            raise DocumentReviewConflictError("This document already has a decision.")
        if record.status in {"processing", "failed"}:
            raise DocumentReviewConflictError(
                "Only a completed review can receive a decision."
            )  
        if decision == "approved" and any(
            issue.get("severity") == "error" for issue in (record.issues or [])
        ):
            raise DocumentReviewConflictError(
                "Resolve all validation errors before approval."
            )

        return self.repository.set_status(record_id, decision) # type: ignore
    
    def draft_correction_email(self, record_id: str) -> CorrectionEmailDraft:
        if self.correction_email_drafter is None:
            raise DocumentReviewConflictError(
                "Correction-email drafting is not configured."
            )
        record = self.repository.get(record_id)
        if record is None:
            raise DocumentNotFoundError("Document not found")
        if record.status in {"processing", "failed"} or record.review_data is None:
            raise DocumentReviewConflictError(
                "Only a completed review can generate a correction email."
            )
        data = ReviewData.model_validate(record.review_data)
        issues = [ValidationIssue.model_validate(item) for item in (record.issues or [])]
        eligible_issues = supplier_fixable_issues(issues)
        if not eligible_issues:
            raise DocumentReviewConflictError(
                "This review has no supplier-fixable business issues."
            )
        return self.correction_email_drafter.draft(data, eligible_issues)
