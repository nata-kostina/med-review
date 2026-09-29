from datetime import date
from decimal import Decimal

from app.documents.schemas import FieldSource, ReviewData
from app.schemas.common import ExtractedDate, ExtractedNumber, ExtractedString
from app.schemas.document.model import DocumentExtraction


def _string(extracted: ExtractedString | None) -> str | None:
    return extracted.value if extracted is not None else None

def _number(extracted: ExtractedNumber | None) -> Decimal | None:
    return extracted.value if extracted is not None else None

def _date(extracted: ExtractedDate | None) -> date | None:
    return extracted.value if extracted is not None else None

def _confidence(
    field_confidence: dict[str, float],
    field: str,
    extracted: ExtractedString | ExtractedDate | ExtractedNumber | None,
) -> None:
    if extracted is not None and extracted.confidence is not None:
        field_confidence[field] = extracted.confidence

def _source(
    field_sources: dict[str, FieldSource],
    field: str,
    value: object | None,
) -> None:
    if value is not None:
        field_sources[field] = "document_intelligence"        

def project_extraction(extraction: DocumentExtraction) -> ReviewData:
    field_confidence: dict[str, float] = {}
    field_sources: dict[str, FieldSource] = {}
    
    age = _number(extraction.age)
    diagnosis = _string(extraction.diagnosis)
    dob = _date(extraction.dob)
    doctor_id = _string(extraction.doctor_id)
    doctor_name = _string(extraction.doctor_name)
    hospital = _string(extraction.hospital)
    patient_name = _string(extraction.patient_name)
    recorded_date = _date(extraction.recorded_date)
    sex = _string(extraction.sex)
    ssn = _string(extraction.ssn)
    
    _confidence(field_confidence, "age", extraction.age)
    _confidence(field_confidence, "diagnosis", extraction.diagnosis)
    _confidence(field_confidence, "dob", extraction.dob)
    _confidence(field_confidence, "doctor_id", extraction.doctor_id)
    _confidence(field_confidence, "doctor_name", extraction.doctor_name)
    _confidence(field_confidence, "patient_name", extraction.patient_name)
    _confidence(field_confidence, "recorded_date", extraction.recorded_date)
    _confidence(field_confidence, "sex", extraction.sex)
    _confidence(field_confidence, "ssn", extraction.ssn)
    
    for field, value in (
        ("age", age),
        ("diagnosis", diagnosis),
        ("dob", dob),
        ("doctor_id", doctor_id),
        ("doctor_name", doctor_name),
        ("hospital", hospital),
        ("patient_name", patient_name),
        ("recorded_date", recorded_date),
        ("sex", sex),
        ("ssn", ssn),
    ):
        _source(field_sources, field, value)
        
    return ReviewData(
        age=age,
        diagnosis=diagnosis,
        dob=dob,
        doctor_id=doctor_id,
        doctor_name=doctor_name,
        hospital=hospital,
        patient_name=patient_name,
        recorded_date=recorded_date,
        sex=sex,
        ssn=ssn,
        field_confidence=field_confidence,
        field_sources=field_sources,
    )