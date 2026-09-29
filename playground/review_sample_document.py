import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import get_settings
from app.providers.azure_openai import build_azure_openai_client
from app.providers.azure_openai_document_review import (
    AzureOpenAIDocumentReviewer,
)

SAMPLE = Path(
    r"C:\Users\Nata\Desktop\Projects\med-review\samples\Hard\PDF_Deid_Deidentification_Hard_0.pdf"
)
OUTPUT_JSON = Path(r"C:\Users\Nata\Desktop\Projects\med-review\tmp\review_hard_0.json")

def main():
    settings = get_settings()
    openai_client = build_azure_openai_client(settings)
    openai_review_provider = AzureOpenAIDocumentReviewer(
        client=openai_client,
        deployment_name=settings.azure_openai_deployment
    )
    
    result = openai_review_provider.review(SAMPLE, "application/pdf")
    
    json_data = result.model_dump_json(indent=2)
    
    OUTPUT_JSON.write_text(json_data, encoding="utf-8")
    print(f"Result saved at: {OUTPUT_JSON.resolve()}")


if __name__ == "__main__":
    main()
