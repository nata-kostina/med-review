import re
from collections.abc import Callable
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from dateutil import parser

from app.document_review.parsers import parse_date, parse_integer_decimal, parse_string
from app.document_review.schemas import DocumentReview, FieldComparison, LlmDocumentExtraction
from app.documents.schemas import ReviewData

FIELDS = (
    ("age", "Patient age", "number"),
    ("diagnosis", "Diagnosis", "text"),
    ("dob", "Date of birth", "date"),
    ("doctor_id", "Doctor ID", "identifier"),
    ("doctor_name", "Doctor name", "text"),
    ("hospital", "Hospital", "text"),
    ("patient_name", "Patient name", "text"),
    ("recorded_date", "Recorded date", "date"),
    ("sex", "Sex", "text"),
    ("ssn", "Social Security Number", "identifier"),
)

def _shown(value: object | None) -> str | None:
    if value is None:
        return None
    return str(value).strip() or None

def _text(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())

def _identifier(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())

def _date(value: date | str) -> str:
    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, str):
        clean_str = value.strip()
        if not clean_str:
            return ""

        try:
            return date.fromisoformat(clean_str).isoformat()
        except ValueError:
            pass

        try:
            return parser.parse(clean_str, dayfirst=True).date().isoformat()
        except Exception:
            return clean_str.casefold()

    return str(value).strip().casefold()

def _number(value: Decimal | str) -> str:
    if isinstance(value, Decimal):
        return str(value.normalize())

    if isinstance(value, (int, float)):
        return str(Decimal(str(value)).normalize())

    if isinstance(value, str):
        clean_str = value.strip()
        if not clean_str:
            return ""
        
        try:
            sanitized = clean_str.replace(" ", "").replace(",", ".")
            return str(Decimal(sanitized).normalize())
        except InvalidOperation:
            return clean_str.casefold()

    return str(value).strip().casefold()


NORMALIZERS: dict[str, Callable[[str], str]] = {
    "text": _text,
    "identifier": _identifier,
    "date": _date,
    "number": _number,
}

def reconcile_document_extractions(
    review_data: ReviewData,
    extraction: LlmDocumentExtraction,
) -> DocumentReview:
    comparisons: list[FieldComparison] = []
    for field, label, normalizer_name in FIELDS:
        document_intelligence_value = _shown(getattr(review_data, field, None))
        llm_value = _shown(getattr(extraction, field, None))
        if document_intelligence_value is None and llm_value is None:
            comparison_status = "missing_in_both"
        elif llm_value is None:
            comparison_status = "missing_in_llm"
        elif document_intelligence_value is None:
            comparison_status = "missing_in_document_intelligence"
        else:
            normalizer = NORMALIZERS[normalizer_name]
            comparison_status = (
                "match"
                if normalizer(document_intelligence_value) == normalizer(llm_value)
                else "different"
            )
        comparisons.append(
            FieldComparison(
                field=field,
                label=label,
                status=comparison_status,
                document_intelligence_value=document_intelligence_value,
                llm_value=llm_value,
            )
        )
        
    return DocumentReview(
        extraction=extraction,
        comparisons=comparisons,
    )

FIELD_PARSERS: dict[str, Callable[[Any], Any]] = {
    "dob": parse_date,
    "recorded_date": parse_date,
    "age": parse_integer_decimal,
}

def _fallback_value(field: str, value: str) -> object | None:
    parse_func = FIELD_PARSERS.get(field, parse_string)
    return parse_func(value)



def merge_document_extractions(
    primary: ReviewData,
    extraction: LlmDocumentExtraction,
) -> tuple[ReviewData, DocumentReview]:
    review = reconcile_document_extractions(primary, extraction)
    merged_values = primary.model_dump()
    field_sources = dict(primary.field_sources)
    fallback_fields: list[FieldComparison] = []
    
    for field, _label, _normalizer_name in FIELDS:
        primary_value = getattr(primary, field, None)
        if _shown(primary_value) is not None:
            continue
        
        llm_value = _shown(getattr(extraction, field, None))
        if llm_value is None:
            continue
        parsed_value = _fallback_value(field, llm_value)
        if parsed_value is None:
            continue
        merged_values[field] = parsed_value
        field_sources[field] = "llm_fallback"
        fallback_fields.append(
            next(item for item in review.comparisons if item.field == field)
        )
    
    merged_values["field_sources"] = field_sources
    review.fallback_fields = fallback_fields
    return ReviewData.model_validate(merged_values), review