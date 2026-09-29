export interface CorrectionEmailDraft {
    recipient_name: string
    subject: string
    body: string
}

export type DocumentStatus =
    | 'processing'
    | 'ready'
    | 'needs_review'
    | 'approved'
    | 'rejected'
    | 'failed'

export type IssueSeverity = 'error' | 'warning'

export type FieldSource = 'document_intelligence' | 'llm_fallback' | 'human'

export type ComparisonStatus =
    | 'match'
    | 'different'
    | 'missing_in_llm'
    | 'missing_in_document_intelligence'
    | 'missing_in_both'

export interface LlmDocumentExtraction {
    age: string | null
    diagnosis: string | null
    dob: string | null
    doctor_id: string | null
    doctor_name: string | null
    hospital: string | null
    patient_name: string | null
    recorded_date: string | null
    sex: string | null
    ssn: string | null

}

export interface FieldComparison {
    field: string
    label: string
    status: ComparisonStatus
    document_intelligence_value: string | null
    llm_value: string | null
}

export interface DocumentReviewArtifact {
    extraction: LlmDocumentExtraction | null
    comparisons: FieldComparison[]
    fallback_fields: FieldComparison[]
    error_message: string | null
}

export interface ValidationIssue {
    code: string
    field: string | null
    severity: IssueSeverity
    message: string
}

export interface ReviewData {
    age: string | null
    diagnosis: string | null
    dob: string | null
    doctor_id: string | null
    doctor_name: string | null
    hospital: string | null
    patient_name: string | null
    recorded_date: string | null
    sex: string | null
    ssn: string | null
    field_confidence: Record<string, number>
    field_sources: Record<string, FieldSource>
}

export interface Document {
    id: string
    original_filename: string
    content_type: string
    status: DocumentStatus
    extraction: Record<string, unknown> | null
    review: DocumentReviewArtifact | null
    review_data: ReviewData | null
    validation: Record<string, unknown> | null
    issues: ValidationIssue[]
    supplier_action_required: boolean
    error_message: string | null
    created_at: string
    updated_at: string

}