import logging

from app.config import APP_CONFIG
from app.documents.validation import validate_review_data
from app.pipeline.base import DuplicateChecker, PipelineContext

logger = logging.getLogger(__name__)

class ValidationStep:
    name = "validation"
    
    def __init__(
        self,
        min_confidence: float | None = None,
        is_duplicate_checker: DuplicateChecker | None = None,
    ) -> None:
        self._min_confidence = (
            min_confidence
            if min_confidence is not None
            else APP_CONFIG.min_field_confidence
        )
        
        self._is_duplicate_checker = is_duplicate_checker or (lambda _v, _n: False)

        
    def run(self, ctx: PipelineContext) -> PipelineContext:
        if ctx.review_data is None:
            raise ValueError(
                "ValidationStep requires ctx.review_data from DocumentReviewStep."
            )

        is_duplicate = self._is_duplicate_checker(
            ctx.review_data.ssn, ctx.review_data.recorded_date
        )
        
        issues = validate_review_data(
            ctx.review_data, 
            min_confidence=self._min_confidence,
            is_duplicate=is_duplicate,
        )
        error_count = sum(1 for issue in issues if issue.severity == "error")
        logger.info(
            "Validation finished with %d finding(s) (%d error(s))",
            len(issues),
            error_count,
        )
        return ctx.model_copy(update={"issues": issues})