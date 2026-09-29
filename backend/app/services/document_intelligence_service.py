from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential

from app.config import Settings, get_settings

endpoint = "https://<my-custom-subdomain>.cognitiveservices.azure.com/"
credential = AzureKeyCredential("<api_key>")
document_intelligence_client = DocumentIntelligenceClient(endpoint, credential)

PREBUILT_LAYOUT_MODEL = "prebuilt-layout"

class DocumentIntelligenceService:
    def __init__(self, settings: Settings | None = None) -> None:
        resolved_settings = settings or get_settings()
        self._client = DocumentIntelligenceClient(
            endpoint=resolved_settings.azure_document_intelligence_endpoint,
            credential=AzureKeyCredential(resolved_settings.azure_document_intelligence_key)
        )
        
    def analyze_medical_document(self, document_path: Path) -> AnalyzeResult:        
        poller = self._client.begin_analyze_document(
            PREBUILT_LAYOUT_MODEL,
            AnalyzeDocumentRequest(bytes_source=document_path.read_bytes()),
            output_content_format="markdown",
            locale="en",
            features=["keyValuePairs"],
        )
        
        return poller.result()
    
    @staticmethod
    def to_dict(result: AnalyzeResult) -> dict:
        return result.as_dict()