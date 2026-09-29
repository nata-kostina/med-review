
# MedReview Backend
## Stack
* **Python 3.14** or newer.
* **uv** for dependency and project management.
* **FastAPI** and **uvicorn** for the HTTP service.
* **Pydantic** and **pydantic-settings** for typed boundaries and provider settings.
* **SQLAlchemy** with local SQLite persistence.
* **Azure AI Document Intelligence** and **Azure OpenAI** behind provider adapters.
* **Ruff** for linting and import/style checks.

## Running locally

Navigate to the backend directory and start the server:
   ```bash
   cd backend
   cp .env.example .env
   uv run --locked --no-sync uvicorn app.main:create_app --factory --reload
   ```
   The backend API will be available at [http://localhost:8000](http://localhost:8000).

## API endpoints and pipeline

This document describes the MedReview HTTP API and how `POST /api/documents` runs the document pipeline.

Base URL (local): `http://localhost:8000`

Interactive docs while the API is running:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

CORS allows the Vite app at `http://localhost:5173`.

---

### Endpoint summary

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/documents` | Upload a document and run the full pipeline |
| `GET` | `/api/documents` | List saved reviews (newest first) |
| `GET` | `/api/documents/{document_id}` | Fetch one review |
| `GET` | `/api/documents/{document_id}/file` | Serve the stored upload bytes |
| `PUT` | `/api/documents/{document_id}` | Apply field corrections and revalidate |
| `POST` | `/api/documents/{document_id}/decision` | Approve or reject |
| `POST` | `/api/documents/{document_id}/correction-email` | Draft a supplier correction email |
| `DELETE` | `/api/documents/{document_id}` | Delete a saved review and its upload file |

---

### Shared response shape

Document endpoints return `DocumentResponse`:

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string (UUID) | Stable review id |
| `original_filename` | string | Filename from the upload |
| `content_type` | string | `application/pdf` |
| `status` | string | `processing`, `ready`, `needs_review`, `approved`, `rejected`, or `failed` |
| `extraction` | object \| null | Mapped Document Intelligence fields (evidence) |
| `validation` | object \| null | Compact findings summary for the teaching UI |
| `review_data` | object \| null | Flat editable projection |
| `document_review` | object \| null | LLM cross-check comparisons and fallbacks |
| `issues` | array | `ValidationIssue` list |
| `supplier_action_required` | bool | True when supplier-fixable issues exist |
| `error_message` | string \| null | Set when status is `failed` |
| `created_at` / `updated_at` | ISO datetime | Persistence timestamps |

Status after a successful pipeline run:

- `needs_review` — validation reported at least one error
- `ready` — pipeline finished without validation errors (warnings allowed)

Decided records use `approved` or `rejected` and become immutable. A pipeline exception is persisted as `failed`, then the HTTP handler returns **502**. Unsupported documents from the LLM review return **422**.

---

### Pipeline steps

`build_default_pipeline()` runs:

1. **Extraction** — Document Intelligence `prebuilt-layout`.
2. **Document review** — project DI → `ReviewData`, run independent LLM extraction, merge gaps only (DI wins on conflict).
3. **Validation** — pure LabTest Diagnostics document policy + duplicate detection.

---

### Review actions

- `PUT /api/documents/{id}` — body is `DocumentCorrectionRequest` (scalar fields only). Changed fields are marked `human` in `field_sources`, then policy re-runs.
- `POST /api/documents/{id}/decision` — `{ "decision": "approved" | "rejected" }`. Approval requires no error issues.
- `POST /api/documents/{id}/correction-email` — drafts only; the app never sends mail. Requires supplier-fixable issues.

