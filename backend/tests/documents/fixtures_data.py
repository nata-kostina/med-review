from datetime import date
from decimal import Decimal

from app.document_review.schemas import (
    DocumentReview,
    FieldComparison,
    LlmDocumentExtraction,
)
from app.documents.schemas import ReviewData
from app.schemas.common import (
    BloodPressureValue,
    ExtractedBloodPressure,
    ExtractedDate,
    ExtractedNumber,
    ExtractedString,
)
from app.schemas.document.model import DocumentExtraction

valid_document = {
    "id": "1",
    "original_filename": "john_smith.pdf",
    "stored_filename": "1_john_smith.pdf",
    "content_type": "application/pdf",
    "status": "ready",  # DocumentStatus = Literal["processing","ready","needs_review","approved","rejected","failed",]
    "normalized_ssn": "123456789",
    "normalized_recorded_date": "2026-09-20",
    "extraction": DocumentExtraction(
        model_id="prebuilt-layout-2026",
        age=ExtractedNumber(value=Decimal("20"), content="20", confidence=0.9),
        alcohol_consumption=ExtractedString(
            value="moderate", content="moderate", confidence=0.82
        ),
        blood_pressure=ExtractedBloodPressure(
            value=BloodPressureValue(systolic=120, diastolic=80, unit="mmHg"),
            content="120/80 mmHg",
            confidence=0.96,
        ),
        diagnosis=ExtractedString(
            value="Acute bronchitis",
            content="Acute bronchitis",
            confidence=0.91,
        ),
        diet=None,
        dob=ExtractedDate(
            value=date(2006, 5, 12), content="12/05/2006", confidence=0.91
        ),
        doctor_id=ExtractedString(
            value="DOC-9912", content="DOC-9912", confidence=0.88
        ),
        doctor_name=ExtractedString(
            value="Dr. Gregory House",
            content="Dr. Gregory House",
            confidence=0.94,
        ),
        exercise_habits=ExtractedString(
            value="3 times per week",
            content="Runs 3x weekly",
            confidence=0.80,
        ),
        heart_rate=ExtractedNumber(
            value=Decimal("72"), content="72 bpm", confidence=0.98
        ),
        hospital=ExtractedString(
            value="St. Thomas Hospital",
            content="St. Thomas Hospital",
            confidence=0.93,
        ),
        hospital_id=ExtractedString(
            value="HOSP-4042", content="HOSP-4042", confidence=0.89
        ),
        oxygen_saturation_percent=ExtractedNumber(
            value=Decimal("98.5"), content="98.5%", confidence=0.95
        ),
        patient_name=ExtractedString(
            value="John Smith", content="John Smith", confidence=0.97
        ),
        recorded_date=ExtractedDate(
            value=date(2026, 9, 20), content="20.09.2026", confidence=0.95
        ),
        respiratory_rate=ExtractedNumber(
            value=Decimal("16"), content="16/min", confidence=0.92
        ),
        sex=ExtractedString(value="male", content="Male", confidence=0.99),
        smoking_status=ExtractedString(
            value="never smoked", content="Never smoked", confidence=0.85
        ),
        ssn=ExtractedString(
            value="123-456-789", content="123-456-789", confidence=0.95
        ),
        temperature_celsius=ExtractedNumber(
            value=Decimal("36.6"), content="36.6 °C", confidence=0.99
        ),
    ),
    "review": DocumentReview(
        extraction=LlmDocumentExtraction(
            age="20",
            diagnosis="Acute bronchitis",
            dob="2006-05-12",
            doctor_id="DOC-9912",
            doctor_name="Dr. Gregory House",
            hospital="St. Thomas Hospital",
            patient_name="John Smith",
            recorded_date="2026-09-20",
            sex="male",
            ssn="123-456-789",
        ),
        comparisons=[
            FieldComparison(
                field="age",
                label="Age",
                status="match",
                document_intelligence_value="20",
                llm_value="20",
            ),
            FieldComparison(
                field="diagnosis",
                label="Diagnosis",
                status="match",
                document_intelligence_value="Acute bronchitis",
                llm_value="Acute bronchitis",
            ),
            FieldComparison(
                field="dob",
                label="Date of Birth",
                status="match",
                document_intelligence_value="2006-05-12",
                llm_value="2006-05-12",
            ),
            FieldComparison(
                field="doctor_id",
                label="Doctor ID",
                status="match",
                document_intelligence_value="DOC-9912",
                llm_value="DOC-9912",
            ),
            FieldComparison(
                field="doctor_name",
                label="Doctor Name",
                status="match",
                document_intelligence_value="Dr. Gregory House",
                llm_value="Dr. Gregory House",
            ),
            FieldComparison(
                field="hospital",
                label="Hospital",
                status="match",
                document_intelligence_value="St. Thomas Hospital",
                llm_value="St. Thomas Hospital",
            ),
            FieldComparison(
                field="patient_name",
                label="Patient Name",
                status="match",
                document_intelligence_value="John Smith",
                llm_value="John Smith",
            ),
            FieldComparison(
                field="recorded_date",
                label="Recorded Date",
                status="match",
                document_intelligence_value="2026-09-20",
                llm_value="2026-09-20",
            ),
            FieldComparison(
                field="sex",
                label="Sex",
                status="match",
                document_intelligence_value="male",
                llm_value="male",
            ),
            FieldComparison(
                field="ssn",
                label="SSN",
                status="match",
                document_intelligence_value="123-456-789",
                llm_value="123-456-789",
            ),
        ],
        error_message=None,
        fallback_fields=[],
    ),
    "validation": {
        "findings": [],
        "has_errors": False
    },
    "review_data": ReviewData(
        age=Decimal("20"),
        diagnosis="Acute bronchitis",
        dob=date(2006, 5, 12),
        doctor_id="DOC-9912",
        doctor_name="Dr. Gregory House",
        hospital="St. Thomas Hospital",
        patient_name="John Smith",
        recorded_date=date(2026, 9, 20),
        sex="male",
        ssn="123-456-789",
        field_confidence={
            "age": 0.9,
            "diagnosis": 0.91,
            "dob": 0.91,
            "doctor_id": 0.88,
            "doctor_name": 0.94,
            "hospital": 0.93,
            "patient_name": 0.97,
            "recorded_date": 0.95,
            "sex": 0.99,
            "ssn": 0.95,
        },
        field_sources={
            "age": "document_intelligence",
            "diagnosis": "document_intelligence",
            "dob": "document_intelligence",
            "doctor_id": "document_intelligence",
            "doctor_name": "document_intelligence",
            "hospital": "document_intelligence",
            "patient_name": "document_intelligence",
            "recorded_date": "document_intelligence",
            "sex": "document_intelligence",
            "ssn": "document_intelligence",
        }
    ),
    "issues": [],
    "error_message": None,
}
