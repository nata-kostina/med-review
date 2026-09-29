from app.document_review.base import DocumentReviewer
from app.pipeline.base import DuplicateChecker, Pipeline
from app.pipeline.extraction import ExtractionStep
from app.pipeline.review import ReviewStep
from app.pipeline.validation import ValidationStep
from app.services.document_intelligence_service import DocumentIntelligenceService


def build_default_pipeline(
    *,
    service: DocumentIntelligenceService | None = None,
    reviewer: DocumentReviewer | None = None,
    content_type: str | None = None,
    min_confidence: float | None = None,
    is_duplicate_checker: DuplicateChecker | None = None
) -> Pipeline:
    return Pipeline(
        [
            ExtractionStep(service=service),
            ReviewStep(content_type=content_type, reviewer=reviewer),
            ValidationStep(min_confidence=min_confidence,is_duplicate_checker=is_duplicate_checker)
        ]
    )
    
__all__ = [
    "build_default_pipeline",
    "ExtractionStep",
    "ReviewStep",
    "ValidationStep"
]