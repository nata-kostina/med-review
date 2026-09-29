from pydantic import BaseModel

from app.schemas.common import (
    ExtractedBloodPressure,
    ExtractedDate,
    ExtractedNumber,
    ExtractedString,
)


class DocumentExtraction(BaseModel):
    model_id: str | None = None
    
    age: ExtractedNumber | None = None
    alcohol_consumption: ExtractedString | None = None
    blood_pressure: ExtractedBloodPressure | None = None
    diagnosis: ExtractedString | None = None
    diet: ExtractedString | None = None
    dob: ExtractedDate | None = None
    doctor_id: ExtractedString | None = None
    doctor_name: ExtractedString | None = None
    exercise_habits: ExtractedString | None = None
    heart_rate: ExtractedNumber | None = None
    hospital: ExtractedString | None = None
    hospital_id: ExtractedString | None = None
    oxygen_saturation_percent: ExtractedNumber | None = None
    patient_name: ExtractedString | None = None
    recorded_date: ExtractedDate | None = None
    respiratory_rate: ExtractedNumber | None = None
    sex: ExtractedString | None = None
    smoking_status: ExtractedString | None = None
    ssn: ExtractedString | None = None
    temperature_celsius: ExtractedNumber | None = None