import base64
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.document_review.base import DocumentReviewer, DocumentReviewError
from app.document_review.schemas import LlmDocumentExtraction

INSTRUCTIONS = """
You are an independent medical-document extraction assistant. 
Extract all requested patient and clinical values directly from the source document. 
When converting dates to YYYY-MM-DD format, assume the source dates use the DD/MM/YYYY format
(day first) unless the text explicitly states otherwise or includes spelled-out month names.
Use null whenever a value is absent, 
unstated, or unreadable. Strictly extract only facts explicitly mentioned 
in the text without inferring, speculating, or adding diagnostic interpretations.
""".strip()

class AzureOpenAIDocumentReviewer(DocumentReviewer):
    def __init__(self, *, client: Any, deployment_name: str) -> None:
        self.client = client
        self.deployment_name = deployment_name
        
    def review(self, path: Path, content_type: str) -> LlmDocumentExtraction:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        if content_type == "application/pdf":
            document_part = {
                "type": "input_file",
                "filename": path.name,
                "file_data": f"data:application/pdf;base64,{encoded}"
            }
        else:
            raise DocumentReviewError(
                "The independent LLM review supports only PDF files. "
                "Document Intelligence and deterministic checks still completed."
            )
            
        schema = LlmDocumentExtraction.model_json_schema()
        try:
            response = self.client.responses.create(
                model=self.deployment_name,
                instructions=INSTRUCTIONS,
                input=[
                    {
                        "role": "user",
                        "content": [
                            document_part,
                            {
                                "type": "input_text",
                                "text": (
                                    "Independently extract and review this medical document."
                                ),
                            },
                        ],
                    }
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "medical_document_review",
                        "strict": True,
                        "schema": schema,
                    }
                },
            )
        except Exception as error:
            raise DocumentReviewError(
                "Azure OpenAI document review failed. The deterministic review can continue."
            ) from error
            
        try:
            return LlmDocumentExtraction.model_validate(json.loads(response.output_text))
        except (json.JSONDecodeError, ValidationError, TypeError) as error:
            raise DocumentReviewError(
                "Azure OpenAI did not return valid structured document-review output."
            ) from error
