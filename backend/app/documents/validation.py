import re
from datetime import date

from app.documents.schemas import DocumentStatus, ReviewData, ValidationIssue

CORE_CONFIDENCE_FIELDS = {"patient_name", "doctor_name", "diagnosis", "ssn"}


def normalize_recorded_date(value: date) -> str:
    return value.isoformat()


def normalize_ssn(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def _issue(
    code: str,
    field: str | None,
    message: str,
    *,
    severity: str = "error",
) -> ValidationIssue:
    return ValidationIssue.model_validate(
        {"code": code, "field": field, "severity": severity, "message": message}
    )


def validate_review_data(
    data: ReviewData, *, min_confidence: float, is_duplicate: bool
) -> list[ValidationIssue]:

    issues: list[ValidationIssue] = []

    if not data.patient_name:
        issues.append(
            _issue("patient_name_required", "patient_name", "Patient name is required.")
        )

    if not data.doctor_name:
        issues.append(
            _issue("doctor_name_required", "doctor_name", "Doctor name is required.")
        )

    if not data.ssn:
        issues.append(_issue("ssn_required", "ssn", "SSN is required."))

    if not data.diagnosis:
        issues.append(
            _issue("diagnosis_required", "diagnosis", "Diagnosis is required.")
        )

    if not data.hospital:
        issues.append(_issue("hospital_required", "hospital", "Hospital is required."))

    if not data.recorded_date:
        issues.append(
            _issue(
                "recorded_date_required", "recorded_date", "Recorded date is required."
            )
        )

    if is_duplicate:
        issues.append(
            _issue(
                "duplicate_document",
                "ssn",
                "A non-rejected document with this patient SSN and recorded date already exists.",
            )
        )

    for field, confidence in data.field_confidence.items():
        if (
            field in CORE_CONFIDENCE_FIELDS
            and data.field_sources.get(field) != "human"
            and confidence < min_confidence
        ):
            issues.append(
                _issue(
                    "low_confidence",
                    field,
                    (
                        f"Azure confidence for {field.replace('_', ' ')} "
                        f"is below {min_confidence:.0%}."
                    ),
                    severity="warning",
                )
            )

    return issues


def status_for_issues(issues: list[ValidationIssue]) -> DocumentStatus:
    return (
        "needs_review"
        if any(issue.severity == "error" for issue in issues)
        else "ready"
    )


def issues_have_errors(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity == "error" for issue in issues)
