
import json
import sys
from pathlib import Path

from app.services.document_intelligence_service import DocumentIntelligenceService

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from rich import print

from app.schemas.document.mapping import map_document_result

SAMPLE_DOCUMENT = PROJECT_DIR / "samples" / "Hard" / "PDF_Deid_Deidentification_Hard_0.pdf"

def main():
    service = DocumentIntelligenceService()
    result = service.analyze_medical_document(SAMPLE_DOCUMENT)

    with open(Path(r".\tmp\result_with_kv_hard_0.md"), "w") as f:
        f.write(result.content)

    with open(Path(r".\tmp\result_with_kv_hard_0.json"), "w", encoding="utf-8") as f:
        json.dump(service.to_dict(result), f, indent=2, default=str, ensure_ascii=False)
        
    data = map_document_result(service.to_dict(result))
    
    
    print(data)
        
    with open(Path(r".\tmp\easy_0\di_easy_0.json"), "w", encoding="utf-8") as f:
        json.dump(data.model_dump(), f, indent=2, default=str, ensure_ascii=False)

if __name__ == "__main__":
    main()