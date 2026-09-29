import sys
from pathlib import Path

from rich import print as rprint

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import APP_CONFIG
from app.database import build_database
from app.documents.models import DocumentRecord
from app.documents.repository import DocumentRepository


def main():
    config = APP_CONFIG
    database_path = config.database_url.removeprefix("sqlite:///")
    if config.database_url.startswith("sqlite:///"):
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    
    engine, session_factory = build_database(config.database_url)
    DocumentRecord.metadata.create_all(engine)    
    
    with session_factory() as session:
        repository = DocumentRepository(session)
        document = repository.create_processing_document(
            record_id="test-id",
            content_type="application/pdf",
            original_filename="test.pdf",
            stored_filename="test_stored.pdf",
        )
        
    rprint(document.__dict__)
    
if __name__ == "__main__":
    main()