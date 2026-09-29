import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from dateutil import parser
from pydantic import BaseModel


class ExtractedString(BaseModel):
    value: str | None = None
    content: str | None = None
    confidence: float | None = None
    
class ExtractedDate(BaseModel):
    value: date | None = None
    content: str | None = None
    confidence: float | None = None
    
class ExtractedNumber(BaseModel):
    value: Decimal | None = None
    content: str | None = None
    confidence: float | None = None
    
class BloodPressureValue(BaseModel):
    systolic: int | None = None
    diastolic: int | None = None
    unit: str | None

class ExtractedBloodPressure(BaseModel):
    value: BloodPressureValue | None = None
    content: str | None = None 
    confidence: float | None = None


def _field_confidence(field: dict[str, Any] | None) -> float | None:
    if not field:
        return None
    confidence = field.get("confidence")
    return float(confidence) if confidence is not None else None


def parse_number_field(field: dict[str, Any] | None) -> ExtractedNumber | None:
    if not field:
        return None
    raw_value = field.get("content")
    parsed_decimal: Decimal | None = None
    
    if raw_value is not None:
        digits_only = re.sub(r"\D", "", str(raw_value))
        
        if digits_only:
            try:
                parsed_decimal = Decimal(digits_only)
            except (InvalidOperation, TypeError, ValueError):
                parsed_decimal = None
                
    return ExtractedNumber(
        value=parsed_decimal,
        content=field.get("content"),
        confidence=_field_confidence(field),
    )
    
def parse_string_field(field: dict[str, Any] | None) -> ExtractedString | None:
    if not field:
        return None
    raw_content = field.get("content")
    clean_value = raw_content.strip() if isinstance(raw_content, str) else None
    value = clean_value if clean_value else None

    return ExtractedString(
        value=value,
        content=raw_content,
        confidence=_field_confidence(field),
    )
    
    
def parse_date_field(field: dict[str, Any] | None) -> ExtractedDate | None:
    if not field:
        return None

    raw_value = field.get("content")
    parsed: date | None = None

    if raw_value:
        try:
            dt = parser.parse(str(raw_value), dayfirst=True)
            parsed = dt.date()
        except (ValueError, TypeError):
            parsed = None

    return ExtractedDate(
        value=parsed,
        content=raw_value,
        confidence=_field_confidence(field),
    )


def parse_blood_pressure_field(field: dict[str, Any] | None) -> ExtractedBloodPressure | None:
    if not field:
        return None
    raw_value = field.get("content")
    if not raw_value:
        return ExtractedBloodPressure(value=None, content=None, confidence=_field_confidence(field))

    pattern = r"(?P<systolic>\d+)\s*/\s*(?P<diastolic>\d+)(?:\s*(?P<unit>[a-zA-Z]+))?"
    
    match = re.search(pattern, raw_value)
    if match:
        data = match.groupdict()
            
        value = BloodPressureValue(
            systolic=int(data["systolic"]),
            diastolic=int(data["diastolic"]),
            unit=data["unit"],
        )
        
        return ExtractedBloodPressure(
            value=value,
            content=field.get("content"),
            confidence=_field_confidence(field),
        )
    else:
        return ExtractedBloodPressure(
            value=None,
            content=field.get("content"),
            confidence=_field_confidence(field),
        )