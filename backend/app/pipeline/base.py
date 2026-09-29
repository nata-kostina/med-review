import logging
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from app.document_review.schemas import DocumentReview
from app.documents.schemas import ReviewData, ValidationIssue
from app.schemas.document.model import DocumentExtraction

logger = logging.getLogger(__name__)


class PipelineContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    document_path: Path
    content_type: str | None = None
    extraction: DocumentExtraction | None = None
    review: DocumentReview | None = None
    review_data: ReviewData | None = None
    issues: list[ValidationIssue] | None = None

    
class PipelineStep(Protocol):
    name: str
    
    def run(self, ctx: PipelineContext) -> PipelineContext: ...
    

class Pipeline:
    
    def __init__(self, steps: Sequence[PipelineStep]) -> None:
        self.steps = tuple(steps)
        
    def run(self, document_path: Path) -> PipelineContext:
        logger.info("Pipeline started for %s (%d steps)", document_path.name, len(self.steps))
        ctx = PipelineContext(document_path=document_path)
        for index, step in enumerate(self.steps, start=1):
            logger.info("[%d/%d] Starting step: %s", index, len(self.steps), step.name)
            ctx = step.run(ctx)
            logger.info("[%d/%d] Finished step: %s", index, len(self.steps), step.name)
        logger.info("Pipeline completed for %s", document_path.name)
        return ctx
    
DuplicateChecker = Callable[[str | None, date | None], bool]
