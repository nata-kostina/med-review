import type { Document } from '@/lib/types'

export const mockValidDocument_0: Document = {
    id: '1',
    original_filename: 'john_smith.pdf',
    content_type: 'application/pdf',
    status: 'ready',
    supplier_action_required: false,
    error_message: null,
    created_at: '2026-09-20T10:00:00Z',
    updated_at: '2026-09-20T10:00:00Z',

    extraction: {
        model_id: 'prebuilt-layout-2026',
        age: {
            value: '20',
            content: '20',
            confidence: 0.9
        },
        alcohol_consumption: {
            value: 'moderate',
            content: 'moderate',
            confidence: 0.82,
        },
        blood_pressure: {
            value: {
                systolic: 120,
                diastolic: 80,
                unit: 'mmHg'
            },
            content: '120/80 mmHg',
            confidence: 0.96,
        },
        diagnosis: {
            value: 'Acute bronchitis',
            content: 'Acute bronchitis',
            confidence: 0.91,
        },
        diet: null,
        dob: {
            value: '2006-05-12',
            content: '12/05/2006',
            confidence: 0.91,
        },
        doctor_id: {
            value: 'DOC-9912',
            content: 'DOC-9912',
            confidence: 0.88,
        },
        doctor_name: {
            value: 'Dr. Gregory House',
            content: 'Dr. Gregory House',
            confidence: 0.94,
        },
        exercise_habits: {
            value: '3 times per week',
            content: 'Runs 3x weekly',
            confidence: 0.8,
        },
        heart_rate: {
            value: '72',
            content: '72 bpm',
            confidence: 0.98
        },
        hospital: {
            value: 'St. Thomas Hospital',
            content: 'St. Thomas Hospital',
            confidence: 0.93,
        },
        hospital_id: {
            value: 'HOSP-4042',
            content: 'HOSP-4042',
            confidence: 0.89,
        },
        oxygen_saturation_percent: {
            value: '98.5',
            content: '98.5%',
            confidence: 0.95,
        },
        patient_name: {
            value: 'John Smith',
            content: 'John Smith',
            confidence: 0.97,
        },
        recorded_date: {
            value: '2026-09-20',
            content: '20.09.2026',
            confidence: 0.95,
        },
        respiratory_rate: {
            value: '16',
            content: '16/min',
            confidence: 0.92
        },
        sex: {
            value: 'male',
            content: 'Male',
            confidence: 0.99
        },
        smoking_status: {
            value: 'never smoked',
            content: 'Never smoked',
            confidence: 0.85,
        },
        ssn: {
            value: '123-456-789',
            content: '123-456-789',
            confidence: 0.95,
        },
        temperature_celsius: {
            value: '36.6',
            content: '36.6 °C',
            confidence: 0.99,
        },
    } as Record<string, unknown>,

    review: {
        extraction: {
            age: '20',
            diagnosis: 'Acute bronchitis',
            dob: '2006-05-12',
            doctor_id: 'DOC-9912',
            doctor_name: 'Dr. Gregory House',
            hospital: 'St. Thomas Hospital',
            patient_name: 'John Smith',
            recorded_date: '2026-09-20',
            sex: 'male',
            ssn: '123-456-789',
        },
        comparisons: [
            {
                field: 'age',
                label: 'Age',
                status: 'match',
                document_intelligence_value: '20',
                llm_value: '20',
            },
            {
                field: 'diagnosis',
                label: 'Diagnosis',
                status: 'match',
                document_intelligence_value: 'Acute bronchitis',
                llm_value: 'Acute bronchitis',
            },
            {
                field: 'dob',
                label: 'Date of Birth',
                status: 'match',
                document_intelligence_value: '2006-05-12',
                llm_value: '2006-05-12',
            },
            {
                field: 'doctor_id',
                label: 'Doctor ID',
                status: 'match',
                document_intelligence_value: 'DOC-9912',
                llm_value: 'DOC-9912',
            },
            {
                field: 'doctor_name',
                label: 'Doctor Name',
                status: 'match',
                document_intelligence_value: 'Dr. Gregory House',
                llm_value: 'Dr. Gregory House',
            },
            {
                field: 'hospital',
                label: 'Hospital',
                status: 'match',
                document_intelligence_value: 'St. Thomas Hospital',
                llm_value: 'St. Thomas Hospital',
            },
            {
                field: 'patient_name',
                label: 'Patient Name',
                status: 'match',
                document_intelligence_value: 'John Smith',
                llm_value: 'John Smith',
            },
            {
                field: 'recorded_date',
                label: 'Recorded Date',
                status: 'match',
                document_intelligence_value: '2026-09-20',
                llm_value: '2026-09-20',
            },
            {
                field: 'sex',
                label: 'Sex',
                status: 'match',
                document_intelligence_value: 'male',
                llm_value: 'male',
            },
            {
                field: 'ssn',
                label: 'SSN',
                status: 'match',
                document_intelligence_value: '123-456-789',
                llm_value: '123-456-789',
            },
        ],
        error_message: null,
        fallback_fields: [],
    },

    validation: {
        findings: [],
        has_errors: false,
    } as Record<string, unknown>,

    review_data: {
        age: '20',
        diagnosis: 'Acute bronchitis',
        dob: '2006-05-12',
        doctor_id: 'DOC-9912',
        doctor_name: 'Dr. Gregory House',
        hospital: 'St. Thomas Hospital',
        patient_name: 'John Smith',
        recorded_date: '2026-09-20',
        sex: 'male',
        ssn: '123-456-789',
        field_confidence: {
            age: 0.9,
            diagnosis: 0.91,
            dob: 0.91,
            doctor_id: 0.88,
            doctor_name: 0.94,
            hospital: 0.93,
            patient_name: 0.97,
            recorded_date: 0.95,
            sex: 0.99,
            ssn: 0.95,
        },
        field_sources: {
            age: 'document_intelligence',
            diagnosis: 'document_intelligence',
            dob: 'document_intelligence',
            doctor_id: 'document_intelligence',
            doctor_name: 'document_intelligence',
            hospital: 'document_intelligence',
            patient_name: 'document_intelligence',
            recorded_date: 'document_intelligence',
            sex: 'document_intelligence',
            ssn: 'document_intelligence',
        },
    },

    issues: [],
}

export const mockValidDocument_1: Document = {
    id: '2',
    original_filename: 'sarah_connor_scan.pdf',
    content_type: 'application/pdf',
    status: 'ready',
    supplier_action_required: false,
    error_message: null,
    created_at: '2026-09-20T11:15:00Z',
    updated_at: '2026-09-20T11:15:00Z',

    extraction: {
        model_id: 'prebuilt-layout-2026',
        age: {
            value: '34',
            content: '34',
            confidence: 0.95
        },
        alcohol_consumption: {
            value: 'none',
            content: 'non-drinker',
            confidence: 0.89,
        },
        blood_pressure: {
            value: {
                systolic: 118,
                diastolic: 75,
                unit: 'mmHg'
            },
            content: '118/75 mmHg',
            confidence: 0.97,
        },
        diagnosis: {
            value: 'Type 1 Diabetes Mellitus',
            content: 'Type 1 Diabetes',
            confidence: 0.93,
        },
        diet: {
            value: 'low-carb',
            content: 'Low carb diet',
            confidence: 0.85,
        },
        dob: {
            value: '1992-03-24',
            content: '24/03/1992',
            confidence: 0.98,
        },
        doctor_id: {
            value: 'DOC-3301',
            content: 'DOC-3301',
            confidence: 0.92,
        },
        doctor_name: {
            value: 'Dr. Meredith Grey',
            content: 'Dr. Meredith Grey',
            confidence: 0.96,
        },
        exercise_habits: {
            value: '5 times per week',
            content: 'Gym 5x/week',
            confidence: 0.88,
        },
        heart_rate: {
            value: '68',
            content: '68 bpm',
            confidence: 0.99
        },
        hospital: {
            value: 'Mayo Clinic Medical Center',
            content: 'Mayo Clinic',
            confidence: 0.95,
        },
        hospital_id: {
            value: 'HOSP-1088',
            content: 'HOSP-1088',
            confidence: 0.91,
        },
        oxygen_saturation_percent: {
            value: '99.0',
            content: '99%',
            confidence: 0.98,
        },
        patient_name: {
            value: 'Sarah Connor',
            content: 'Sarah Connor',
            confidence: 0.99,
        },
        recorded_date: {
            value: '2026-09-20',
            content: '20/09/2026',
            confidence: 0.97,
        },
        respiratory_rate: {
            value: '14',
            content: '14/min',
            confidence: 0.94
        },
        sex: {
            value: 'female',
            content: 'Female',
            confidence: 0.99
        },
        smoking_status: {
            value: 'former smoker',
            content: 'Quit 5 yrs ago',
            confidence: 0.87,
        },
        ssn: {
            value: '987-654-321',
            content: '987-654-321',
            confidence: 0.96,
        },
        temperature_celsius: {
            value: '36.8',
            content: '36.8 °C',
            confidence: 0.98,
        },
    } as Record<string, unknown>,

    review: {
        extraction: {
            age: '34',
            diagnosis: 'Type 1 Diabetes Mellitus',
            dob: '1992-03-24',
            doctor_id: 'DOC-3301',
            doctor_name: 'Dr. Meredith Grey',
            hospital: 'Mayo Clinic Medical Center',
            patient_name: 'Sarah Connor',
            recorded_date: '2026-09-20',
            sex: 'female',
            ssn: '987-654-321',
        },
        comparisons: [
            {
                field: 'age',
                label: 'Age',
                status: 'match',
                document_intelligence_value: '34',
                llm_value: '34',
            },
            {
                field: 'diagnosis',
                label: 'Diagnosis',
                status: 'match',
                document_intelligence_value: 'Type 1 Diabetes Mellitus',
                llm_value: 'Type 1 Diabetes Mellitus',
            },
            {
                field: 'dob',
                label: 'Date of Birth',
                status: 'match',
                document_intelligence_value: '1992-03-24',
                llm_value: '1992-03-24',
            },
            {
                field: 'doctor_id',
                label: 'Doctor ID',
                status: 'match',
                document_intelligence_value: 'DOC-3301',
                llm_value: 'DOC-3301',
            },
            {
                field: 'doctor_name',
                label: 'Doctor Name',
                status: 'match',
                document_intelligence_value: 'Dr. Meredith Grey',
                llm_value: 'Dr. Meredith Grey',
            },
            {
                field: 'hospital',
                label: 'Hospital',
                status: 'match',
                document_intelligence_value: 'Mayo Clinic Medical Center',
                llm_value: 'Mayo Clinic Medical Center',
            },
            {
                field: 'patient_name',
                label: 'Patient Name',
                status: 'match',
                document_intelligence_value: 'Sarah Connor',
                llm_value: 'Sarah Connor',
            },
            {
                field: 'recorded_date',
                label: 'Recorded Date',
                status: 'match',
                document_intelligence_value: '2026-09-20',
                llm_value: '2026-09-20',
            },
            {
                field: 'sex',
                label: 'Sex',
                status: 'match',
                document_intelligence_value: 'female',
                llm_value: 'female',
            },
            {
                field: 'ssn',
                label: 'SSN',
                status: 'match',
                document_intelligence_value: '987-654-321',
                llm_value: '987-654-321',
            },
        ],
        error_message: null,
        fallback_fields: [],
    },

    validation: {
        findings: [],
        has_errors: false,
    } as Record<string, unknown>,

    review_data: {
        age: '34',
        diagnosis: 'Type 1 Diabetes Mellitus',
        dob: '1992-03-24',
        doctor_id: 'DOC-3301',
        doctor_name: 'Dr. Meredith Grey',
        hospital: 'Mayo Clinic Medical Center',
        patient_name: 'Sarah Connor',
        recorded_date: '2026-09-20',
        sex: 'female',
        ssn: '987-654-321',
        field_confidence: {
            age: 0.95,
            diagnosis: 0.93,
            dob: 0.98,
            doctor_id: 0.92,
            doctor_name: 0.96,
            hospital: 0.95,
            patient_name: 0.99,
            recorded_date: 0.97,
            sex: 0.99,
            ssn: 0.96,
        },
        field_sources: {
            age: 'document_intelligence',
            diagnosis: 'document_intelligence',
            dob: 'document_intelligence',
            doctor_id: 'document_intelligence',
            doctor_name: 'document_intelligence',
            hospital: 'document_intelligence',
            patient_name: 'document_intelligence',
            recorded_date: 'document_intelligence',
            sex: 'document_intelligence',
            ssn: 'document_intelligence',
        },
    },

    issues: [],
}

export const mockProcessingDocument: Document = {
    id: '3',
    original_filename: 'processing_document.pdf',
    content_type: 'application/pdf',
    status: 'processing',
    supplier_action_required: false,
    error_message: null,
    created_at: '2026-09-20T10:00:00Z',
    updated_at: '2026-09-20T10:00:00Z',

    extraction: null,
    review: null,
    validation: null,
    review_data: null,

    issues: [],
}

export const mockNeedsReviewErrorDocument: Document = {
    id: '4',
    original_filename: 'needs_review.pdf',
    content_type: 'application/pdf',
    status: 'needs_review',
    supplier_action_required: true,
    error_message: null,
    created_at: '2026-09-20T10:00:00Z',
    updated_at: '2026-09-20T10:00:00Z',

    extraction: null,
    review: {
        extraction: {
            age: null,
            diagnosis: 'Diagnosis',
            dob: '1993-07-07',
            doctor_id: '647',
            doctor_name: 'Doctor Name',
            hospital: 'Hospital',
            patient_name: null,
            recorded_date: '2026-09-01',
            sex: 'male',
            ssn: 'a1-b2',
        },
        comparisons: [
            {
                field: 'age',
                label: 'Age',
                status: 'missing_in_both',
                document_intelligence_value: null,
                llm_value: null,
            },
            {
                field: 'diagnosis',
                label: 'Diagnosis',
                status: 'missing_in_document_intelligence',
                document_intelligence_value: null,
                llm_value: 'Diagnosis',
            },
            {
                field: 'dob',
                label: 'Date of Birth',
                status: 'match',
                document_intelligence_value: '1993-07-07',
                llm_value: '1993-07-07',
            },
            {
                field: 'doctor_id',
                label: 'Doctor ID',
                status: 'match',
                document_intelligence_value: '647',
                llm_value: '647',
            },
            {
                field: 'doctor_name',
                label: 'Doctor Name',
                status: 'match',
                document_intelligence_value: 'Doctor Name',
                llm_value: 'Doctor Name',
            },
            {
                field: 'hospital',
                label: 'Hospital',
                status: 'match',
                document_intelligence_value: 'Hospital',
                llm_value: 'Hospital',
            },
            {
                field: 'patient_name',
                label: 'Patient Name',
                status: 'missing_in_both',
                document_intelligence_value: null,
                llm_value: null,
            },
            {
                field: 'recorded_date',
                label: 'Recorded Date',
                status: 'missing_in_document_intelligence',
                document_intelligence_value: null,
                llm_value: '2026-09-01',
            },
            {
                field: 'sex',
                label: 'Sex',
                status: 'missing_in_llm',
                document_intelligence_value: 'male',
                llm_value: null,
            },
            {
                field: 'ssn',
                label: 'SSN',
                status: 'match',
                document_intelligence_value: 'a1-b2',
                llm_value: 'a1-b2',
            },
        ],
        error_message: null,
        fallback_fields: [
            {
                field: 'diagnosis',
                label: 'Diagnosis',
                status: 'missing_in_document_intelligence',
                document_intelligence_value: null,
                llm_value: 'Diagnosis',
            },
            {
                field: 'recorded_date',
                label: 'Recorded Date',
                status: 'missing_in_document_intelligence',
                document_intelligence_value: null,
                llm_value: '2026-09-01',
            },
        ],
    },
    validation: null,
    review_data: {
        patient_name: null,
        age: null,
        diagnosis: 'Diagnosis',
        dob: '1993-07-07',
        doctor_id: '647',
        doctor_name: 'Doctor Name',
        hospital: 'Hospital',
        recorded_date: '2026-09-01',
        sex: 'male',
        ssn: 'a1-b2',
        field_confidence: {},
        field_sources: {}
    },

    issues: [
        {
            code: 'patient_name_required',
            severity: 'error',
            field: 'patient_name',
            message: 'Patient name is required.'
        },
        {
            code: 'age_required',
            severity: 'error',
            field: 'age',
            message: 'Age is required.'
        },
    ],
}

export const mockDocuments = [
    mockValidDocument_0,
    mockValidDocument_1,
    mockProcessingDocument,
    mockNeedsReviewErrorDocument
]