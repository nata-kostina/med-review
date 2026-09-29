import logging

from app.pipeline.base import PipelineContext
from app.schemas.document.mapping import map_document_result
from app.services.document_intelligence_service import (
    PREBUILT_LAYOUT_MODEL,
    DocumentIntelligenceService,
)

logger = logging.getLogger(__name__)

class ExtractionStep:
    name = "extraction"
    
    def __init__(self, service: DocumentIntelligenceService | None = None) -> None:
        self._service = service or DocumentIntelligenceService()
    
    def run(self, ctx: PipelineContext) -> PipelineContext:
        document_path = ctx.document_path
        
        logger.info("Extracting with Document Intelligence model %s", PREBUILT_LAYOUT_MODEL)
        result = self._service.analyze_medical_document(document_path)
        extraction = map_document_result(self._service.to_dict(result))
        
        return ctx.model_copy(update={"extraction": extraction})