# Client brief

## The company

LabTest Diagnostics is a fictional healthcare and medical diagnostics company. It receives medical records, lab test reports, and patient files from partner clinics, diagnostic labs, and medical practitioners across Europe.

Anna works in medical administration. Incoming medical documents arrive exclusively as digital PDF files. Before any document can be ingested into the clinical database, Anna must ensure that key information — specifically patient details, clinic information, and diagnostic data — is accurately extracted from the files so the records can be reviewed and verified.

All source code, documentation, and interface text is in English.

## User story

> As a healthcare compliance administrator at a medical organization, I want to upload a patient document or lab report in PDF format and receive structured patient, clinic, and diagnostic data extracted from it so I can quickly review and verify accurate clinical records.

## What's included in the build

- One PDF file per upload, with a 4 MB limit.
- Azure AI Document Intelligence extraction for structured text, tables, and key-value fields.
- An independent Azure OpenAI extraction of the same PDF to detect unstructured clinical parameters and sensitive patient identifiers.
- A deterministic merge that keeps Document Intelligence layout and table values while filling missing fields from the LLM, complete with source provenance and conflict tracking.
- Offline clinical policy validation (e.g., missing mandatory fields).
- Separate deterministic privacy and validation policies, duplicate detection, human corrections, approval, and rejection workflows.
- SQLite, local file storage for raw and redacted PDFs, and a guided welcome → upload/preview → process → review flow.
- Review history with explicit local deletion to allow reproducible testing.
- An on-demand Azure OpenAI issue-report draft for clinic suppliers sending incomplete documents with Copy and Close; the app never sends mail.
- A fictional medical corpus containing compliant lab reports, incomplete diagnostic notes in PDF format.
