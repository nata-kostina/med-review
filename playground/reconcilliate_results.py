import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from rich import print

from app.document_review.reconcilliation import merge_document_extractions
from app.document_review.schemas import LlmDocumentExtraction
from app.documents.projection import project_extraction
from app.schemas.document.model import DocumentExtraction

DI_RESULTS_PATH = Path(r"C:\Users\Nata\Desktop\Projects\med-review\tmp\hard_0\di_hard_0.json")
LLM_RESULTS_PATH = Path(r"C:\Users\Nata\Desktop\Projects\med-review\tmp\hard_0\llm_hard_0.json")

def main():
    
    document_intelligent_results = json.loads(DI_RESULTS_PATH.read_bytes())
    llm_results = json.loads(LLM_RESULTS_PATH.read_bytes())
    
    document_extraction = DocumentExtraction.model_validate(document_intelligent_results)
    llm_extraction = LlmDocumentExtraction.model_validate(llm_results)
    print(document_extraction)
    
    document_review = project_extraction(document_extraction)
    print(document_review)
    
    review, document_review = merge_document_extractions(document_review, llm_extraction)
    print(review)
    print(document_review)

if __name__ == "__main__":
    main()