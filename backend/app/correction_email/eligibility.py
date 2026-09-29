from app.documents.schemas import ValidationIssue

SUPPLIER_FIXABLE_CODES = {
    "patient_name_required",
    "doctor_name_required",
    "ssn_required",
    "diagnosis_required",
    "hospital_required",
    "recorded_date_required"
}


def supplier_fixable_issues(
    issues: list[ValidationIssue],
) -> list[ValidationIssue]:
    return [issue for issue in issues if issue.code in SUPPLIER_FIXABLE_CODES]
