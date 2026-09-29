import tempfile
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.correction_email.schemas import CorrectionEmailDraft
from app.document_review.schemas import DocumentReview
from app.documents.models import DocumentRecord
from app.documents.routes import get_session
from app.documents.schemas import DocumentResponse, ReviewData, ValidationIssue
from app.main import create_app
from app.schemas.document.model import DocumentExtraction
from tests.documents.fixtures_data import valid_document


@pytest.fixture
def test_env():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test.db"
        engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
        
        DocumentRecord.metadata.create_all(bind=engine)
        
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        app = create_app()

        def override_get_session():
            session = TestingSessionLocal()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_session] = override_get_session

        with TestClient(app, raise_server_exceptions=False) as client:
            yield client, TestingSessionLocal

        app.dependency_overrides.clear()
        engine.dispose()

@pytest.fixture
def create_document(test_env) -> Callable[[dict[Any, Any]], DocumentRecord]:
    _, TestingSessionLocal = test_env

    def _make_document(data: dict) -> DocumentRecord:
        
        for key, value in data.items():
            if isinstance(value, BaseModel):
                data[key] = value.model_dump(mode="json")
                
        doc = DocumentRecord(**data)
        
        with TestingSessionLocal() as db:
            db.add(doc)
            db.commit()
            db.refresh(doc)
            
        return doc

    return _make_document

def test_list_documents_returns_empty_list(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env
    
    response = client.get("/api/documents")

    assert response.status_code == 200
    assert response.json() == []


def test_list_documents_with_data(test_env: tuple[TestClient, sessionmaker[Session]], create_document):
    client, _ = test_env
    
    _ = create_document(valid_document)

    response = client.get("/api/documents")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    

def test_get_valid_document(test_env: tuple[TestClient, sessionmaker[Session]], create_document):
    client, _ = test_env
    
    _ = create_document(valid_document)    
    
    response = client.get(f"/api/documents/{valid_document.get('id')}")

    assert response.status_code == 200
    
    data = response.json()
    actual_response = DocumentResponse.model_validate(data)
    assert actual_response.id == valid_document["id"]
    assert actual_response.original_filename == valid_document["original_filename"]
    assert actual_response.content_type == valid_document["content_type"]
    assert actual_response.status == valid_document["status"]
    
    if valid_document.get("extraction") is not None:
        assert actual_response.extraction == DocumentExtraction.model_validate(valid_document["extraction"])
    else:
        assert actual_response.extraction is None
        
    if valid_document.get("review") is not None:
        assert actual_response.review == DocumentReview.model_validate(valid_document["review"])
    else:
        assert actual_response.review is None

    if valid_document.get("review_data") is not None:
        assert actual_response.review_data == ReviewData.model_validate(valid_document["review_data"])
    else:
        assert actual_response.review_data is None
        
    assert actual_response.validation == valid_document.get("validation")
    
    expected_issues = [
        ValidationIssue.model_validate(issue) 
        for issue in valid_document.get("issues", [])
    ]
    assert actual_response.issues == expected_issues
    assert actual_response.error_message == valid_document.get("error_message")
    
    assert actual_response.supplier_action_required is False

def test_get_non_existing_document(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env
    non_existing_id = "non-existent-uuid-123"
    response = client.get(f"/api/documents/{non_existing_id}")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()
    
def test_get_document_file_doc_not_found(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env

    response = client.get("/api/documents/non-existent-id/file")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
    
    
def test_get_document_file_missing_on_disk(
    test_env: tuple[TestClient, sessionmaker[Session]], 
    create_document
):
    client, _ = test_env

    doc = create_document(valid_document)

    response = client.get(f"/api/documents/{doc.id}/file")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Stored document file was not found."

  
def test_get_document_file_success(
    test_env: tuple[TestClient, sessionmaker[Session]], 
    create_document,
    tmp_path
):
    client, _ = test_env

    client.app.state.config = replace(client.app.state.config, upload_dir=tmp_path) # type: ignore
    doc = create_document(valid_document)

    file_path = tmp_path / doc.stored_filename
    file_content = b"Fake PDF binary content"
    file_path.write_bytes(file_content)

    response = client.get(f"/api/documents/{doc.id}/file")

    assert response.status_code == 200
    assert response.content == file_content 
    assert response.headers["content-type"] == doc.content_type
    
    assert f'filename="{doc.original_filename}"' in response.headers["content-disposition"]
    
def test_delete_document_not_found(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env

    response = client.delete("/api/documents/non-existent-id")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
    
    
def test_delete_document_success(
    test_env: tuple[TestClient, sessionmaker[Session]], 
    create_document
):
    client, _ = test_env

    doc = create_document(valid_document)

    response = client.delete(f"/api/documents/{doc.id}")

    assert response.status_code == 204
    assert not response.content

    get_response = client.get(f"/api/documents/{doc.id}")
    assert get_response.status_code == 404
    
def test_correct_document_not_found(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env

    valid_payload = {
        "age": "25.5",
        "diagnosis": "diagnosis",
        "dob": None,
        "doctor_id": None,
        "doctor_name": None,
        "hospital": None,
        "patient_name": "Name Surname",
        "recorded_date": None,
        "sex": None,
        "ssn": None
    }

    response = client.put("/api/documents/non-existent-id", json=valid_payload)

    assert response.status_code == 404

    data = response.json()
    assert "not found" in data["detail"].lower()
    
@pytest.mark.parametrize("status", ["approved", "rejected"])
def test_correct_document_conflict_decided_status(
    test_env: tuple[TestClient, sessionmaker[Session]], 
    create_document,
    status: str
):
    client, _ = test_env

    doc_data = valid_document.copy()
    doc_data["status"] = status
    doc = create_document(doc_data)

    payload = {
        "patient_name": "New Name",
        "diagnosis": None,
        "age": None,
        "dob": None,
        "doctor_id": None,
        "doctor_name": None,
        "hospital": None,
        "recorded_date": None,
        "sex": None,
        "ssn": None
    }

    response = client.put(f"/api/documents/{doc.id}", json=payload)

    assert response.status_code == 409
    data = response.json()
    assert "cannot be edited" in data["detail"].lower()
    
    
def test_correct_document_success(
    test_env: tuple[TestClient, sessionmaker[Session]], 
    create_document
):
    client, _ = test_env

    editable_doc = valid_document.copy()
    editable_doc["status"] = "needs_review"
    doc = create_document(editable_doc)

    new_patient_name = "New Name"

    payload = {
        "patient_name": new_patient_name,
        "diagnosis": None,
        "age": None,
        "dob": None,
        "doctor_id": None,
        "doctor_name": None,
        "hospital": None,
        "recorded_date": None,
        "sex": None,
        "ssn": None
    }

    response = client.put(f"/api/documents/{doc.id}", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == doc.id
    
    assert data["review_data"]["patient_name"] == new_patient_name
    
    get_response = client.get(f"/api/documents/{doc.id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == doc.id
    assert data["review_data"]["patient_name"] == new_patient_name
    
    
def test_decide_document_not_found(test_env: tuple[TestClient, sessionmaker[Session]]):
    client, _ = test_env

    payload = {"decision": "approved"}
    response = client.post("/api/documents/non-existent-id/decision", json=payload)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.parametrize("status", ["approved", "rejected", "processing", "failed"])
def test_decide_document_conflict_invalid_status(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document,
    status: str
):
    client, _ = test_env

    doc_data = valid_document.copy()
    doc_data["status"] = status
    doc = create_document(doc_data)

    payload = {"decision": "approved"}
    response = client.post(f"/api/documents/{doc.id}/decision", json=payload)

    assert response.status_code == 409


def test_decide_document_conflict_with_errors(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document
):
    client, _ = test_env

    doc_data = valid_document.copy()
    doc_data["status"] = "ready"
    doc_data["issues"] = [{"severity": "error", "message": "Invalid SSN"}]
    doc = create_document(doc_data)

    payload = {"decision": "approved"}
    response = client.post(f"/api/documents/{doc.id}/decision", json=payload)

    assert response.status_code == 409
    assert "resolve all validation errors" in response.json()["detail"].lower()


def test_decide_document_invalid_decision_value(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document
):
    client, _ = test_env

    doc_data = valid_document.copy()
    doc_data["status"] = "ready"
    doc_data["issues"] = []
    doc = create_document(doc_data)

    payload = {"decision": "maybe"}
    response = client.post(f"/api/documents/{doc.id}/decision", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("decision", ["approved", "rejected"])
def test_decide_document_success(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document,
    decision: str
):
    client, _ = test_env

    doc_data = valid_document.copy()
    doc_data["status"] = "ready"
    doc_data["issues"] = []
    doc = create_document(doc_data)

    payload = {"decision": decision}

    response = client.post(f"/api/documents/{doc.id}/decision", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == decision

    get_response = client.get(f"/api/documents/{doc.id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == decision
 
 
class FakeCorrectionEmailDrafter:
    def draft(self, data: ReviewData, issues: list[ValidationIssue]) -> CorrectionEmailDraft:
        return CorrectionEmailDraft(
            subject="Subject",
            body="Body.",
            recipient_name="Recipient Name"
        )
            
def test_draft_correction_email_success(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document
):
    client, _ = test_env

    client.app.state.correction_email_drafter = FakeCorrectionEmailDrafter() # type: ignore

    doc_data = valid_document.copy()
    doc_data["status"] = "ready"
    issue = ValidationIssue(
        code="ssn_required", 
        field="ssn", 
        severity="error", 
        message="SSN required"
    )

    doc_data["issues"] = [issue.model_dump(mode="json")]
    doc = create_document(doc_data)

    response = client.post(f"/api/documents/{doc.id}/correction-email")

    assert response.status_code == 200
    
    data = response.json()
    assert data["subject"] == "Subject"
    assert data["body"] == "Body."
    assert data["recipient_name"] == "Recipient Name"

def test_draft_correction_email_not_found(
    test_env: tuple[TestClient, sessionmaker[Session]]
):
    client, _ = test_env
    client.app.state.correction_email_drafter = FakeCorrectionEmailDrafter() # type: ignore

    response = client.post("/api/documents/non-existent-id/correction-email")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
    
def test_draft_correction_email_conflict_not_configured(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document
):
    client, _ = test_env

    client.app.state.correction_email_drafter = None # type: ignore

    doc = create_document(valid_document)

    response = client.post(f"/api/documents/{doc.id}/correction-email")

    assert response.status_code == 409
    assert "not configured" in response.json()["detail"].lower()
    
@pytest.mark.parametrize("invalid_status", ["processing", "failed"])
def test_draft_correction_email_conflict_invalid_status(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document,
    invalid_status: str
):
    client, _ = test_env
    client.app.state.correction_email_drafter = FakeCorrectionEmailDrafter() # type: ignore

    doc_data = valid_document.copy()
    doc_data["status"] = invalid_status
    doc = create_document(doc_data)

    response = client.post(f"/api/documents/{doc.id}/correction-email")

    assert response.status_code == 409
    assert "completed review" in response.json()["detail"].lower()
    
def test_draft_correction_email_conflict_no_fixable_issues(
    test_env: tuple[TestClient, sessionmaker[Session]],
    create_document
):
    client, _ = test_env
    client.app.state.correction_email_drafter = FakeCorrectionEmailDrafter() # type: ignore

    doc_data = valid_document.copy()
    doc_data["status"] = "ready"
    doc_data["issues"] = []

    doc = create_document(doc_data)

    response = client.post(f"/api/documents/{doc.id}/correction-email")

    assert response.status_code == 409
    assert "no supplier-fixable" in response.json()["detail"].lower()