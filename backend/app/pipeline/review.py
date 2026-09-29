import logging

from app.document_review.base import DocumentReviewer, DocumentReviewError
from app.document_review.reconcilliation import merge_document_extractions
from app.document_review.schemas import DocumentReview
from app.documents.projection import project_extraction
from app.pipeline.base import PipelineContext

logger = logging.getLogger(__name__)


class ReviewStep:
    name = "review"
    
    def __init__(
        self, 
        *,
        reviewer: DocumentReviewer | None = None,
        content_type: str | None = None
    ) -> None:
        self._reviewer = reviewer
        self._content_type = content_type
        
    def run(self, ctx: PipelineContext) -> PipelineContext:
        if ctx.extraction is None:
            raise ValueError("ReviewStep requires ctx.extraction from ExtractionStep")
    
        review_data = project_extraction(ctx.extraction)
        content_type = self._content_type or ctx.content_type
        if self._reviewer is None or content_type is None:
            logger.info("Skipping LLM document review; using Document Intelligence projection only")
            return ctx.model_copy(
                update={
                    "review_data": review_data,
                    "review": DocumentReview(
                        error_message="Independent LLM review was not configured."
                    )
                }
            )
            
        try:
            llm_extraction = self._reviewer.review(ctx.document_path, content_type)
        except DocumentReviewError as error:
            logger.warning("LLM document review failed: %s", error)
            return ctx.model_copy(
                update={
                    "review_data": review_data,
                    "review": DocumentReview(error_message=str(error)),
                }
            )
            
        merged, document_review = merge_document_extractions(review_data, llm_extraction)
        logger.info(
            "Merged DI and LLM extractions (%d fallback field(s))",
            len(document_review.fallback_fields),
        )
        return ctx.model_copy(
            update={"review_data": merged, "review": document_review}
        )