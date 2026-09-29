from typing import Any

from app.schemas.common import (
    parse_blood_pressure_field,
    parse_date_field,
    parse_number_field,
    parse_string_field,
)
from app.schemas.document.model import DocumentExtraction

ALIASES: dict[str, list[str]] = {
    "age": ["age", "patient age", "yrs"],
    "alcohol_consumption": ["alcohol_consumption"],
    "blood_pressure": ["blood pressure", "bp"],
    "diagnosis": ["diagnosis"],
    "diet": ["diet"],
    "dob": ["dob", "date of birth", "birth date", "born on"],
    "doctor_id": ["doctor unique id", "doctor id", "provider id", "npi"],
    "doctor_name": ["doctor name", "physician name", "provider name", "provider"],
    "exercise_habits": ["exercise habits", "exercise"],
    "heart_rate": ["heart rate", "hr", "pulse"],
    "hospital_id": ["hospital id", "patient id", "hosp id", "mrn"],
    "oxygen_saturation_percent": ["spo2", "oxygen saturation"],
    "patient_name": ["name", "patient name", "pt name", "patient", "client name"],
    "recorded_data": ["recorded date", "visit date", "date"],
    "respiratory_rate": ["respiratory rate", "rr"],
    "sex": ["sex", "gender", "patient sex"],
    "smoking_status": ["smoking status", "smoking"],
    "ssn": ["ssn", "social security number", "social security"],
    "temperature_celsius": ["temperature", "temp"],
}

REVERSED_ALIASES: dict[str, str] = {
    alias: standard_name 
    for standard_name, alias_list in ALIASES.items()
    for alias in alias_list
}

def map_document_result(document: dict[str, Any]) -> DocumentExtraction:
    kv_dict: dict[str, dict[str, Any]] = {}

    for pair in document.get("keyValuePairs", []) or []:
        key_info = pair.get("key")
        val_info = pair.get("value")

        if not key_info or not key_info.get("content"):
            continue

        raw_key = key_info["content"].strip(":").strip().lower()
        content = val_info.get("content") if val_info else None
        confidence = pair.get("confidence", 0.0)

        if raw_key not in kv_dict or confidence > kv_dict[raw_key].get("confidence", 0.0):
            kv_dict[raw_key] = {
                "content": content,
                "confidence": confidence,
            }
    
    normalized_kv_dict: dict[str, dict[str, Any]] = {}
    for old_key, value in kv_dict.items():
        if old_key in REVERSED_ALIASES:
            standard_key = REVERSED_ALIASES[old_key]
            if (
                standard_key not in normalized_kv_dict
                or value.get("confidence", 0.0)
                > normalized_kv_dict[standard_key].get("confidence", 0.0)
            ):
                normalized_kv_dict[standard_key] = value
 
    
    return DocumentExtraction(
            model_id=document.get("modelId"),
            age=parse_number_field(normalized_kv_dict.get("age")),
            alcohol_consumption=parse_string_field(normalized_kv_dict.get("alcohol_consumption")),
            blood_pressure=parse_blood_pressure_field(normalized_kv_dict.get("blood_pressure")),
            diet=parse_string_field(normalized_kv_dict.get("diet")),
            dob=parse_date_field(normalized_kv_dict.get("dob")),
            doctor_id=parse_string_field(normalized_kv_dict.get("doctor_id")),
            doctor_name=parse_string_field(normalized_kv_dict.get("doctor_name")),
            exercise_habits=parse_string_field(normalized_kv_dict.get("exercise_habits")),
            heart_rate=parse_number_field(normalized_kv_dict.get("heart_rate")),
            hospital_id=parse_string_field(normalized_kv_dict.get("hospital_id")),
            oxygen_saturation_percent=parse_number_field(normalized_kv_dict.get("oxygen_saturation_percent")),
            patient_name=parse_string_field(normalized_kv_dict.get("patient_name")),
            recorded_date=parse_date_field(normalized_kv_dict.get("recorded_data")),
            respiratory_rate=parse_number_field(normalized_kv_dict.get("respiratory_rate")),
            sex=parse_string_field(normalized_kv_dict.get("sex")),
            smoking_status=parse_string_field(normalized_kv_dict.get("smoking_status")),
            ssn=parse_string_field(normalized_kv_dict.get("ssn")),
            temperature_celsius=parse_number_field(normalized_kv_dict.get("temperature_celsius")),
        )

def document_to_manifest_view(extraction: DocumentExtraction) -> dict[str, str | None]:
    ...
    
