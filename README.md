# 📋 MedReview

MedReview is a medical document review application developed for a fictional medical laboratory to accelerate patient document processing through automated field population, data validation, and manual review or correction prior to saving the finalized documents in the database.

Built as a full-stack Single Page Application (SPA), MedReview integrates Microsoft Azure AI services to handle document processing: Azure Document Intelligence automatically parses incoming PDF reports to extract structured text, while Azure OpenAI processes and refines the extracted clinical context to ensure high-accuracy data mapping.

## Deployment

Here is the link to the fully working deployment: [MedReview](https://ca-med-review.graybush-2f55aa52.northeurope.azurecontainerapps.io/)

Sample documents for testing the application can be found in the `./samples` directory.

![App Demo](./demo.gif)

## Key Features

* **Document Upload & Preview:** Allows users to upload patient documents.
* **Automated Data Extraction:** Processes documents using Azure Document Intelligence and Azure OpenAI to automatically extract relevant field data.
* **Manual Review & Editing:** Enables human operators to verify, correct, and edit pre-filled fields before final submission.
* **Automated Email Generation:** Generates draft emails via Azure OpenAI to request missing fields or clarify errors directly with the issuing clinic.
* **Document Status Control:** Provides the ability to explicitly approve or reject an entire processed document.
* **History & Storage:** Saves finalized records directly to the database and allows users to browse past processing history.

## Tech Stack

### Backend

* **Python 3.14 or newer**
* **FastAPI** — High-performance web framework for API development
* **SQLAlchemy** — ORM for database interactions
* **SQLite** — Relational database management system
* **Azure Document Intelligence** — AI-powered document processing and field extraction
* **Azure OpenAI** — Generative AI for advanced processing and email drafting
* **uv** — Fast Python package and project manager

### Frontend

* **React** — UI library
* **TypeScript** — Strongly typed programming language for safe and scalable UI development
* **Tailwind CSS** — Utility-first CSS framework
* **shadcn/ui** — Reusable, accessible UI components

### Deployment
* **Docker** — Containerization for consistent build and deployment environments

* **Azure Container Apps** — Serverless container hosting platform for running the application

## Project Structure & Documentation

This repository is structured as a monorepo containing both the frontend and backend applications. For detailed setup guides, architecture decisions, and component specs, please refer to their respective documentation:

* [Client Brief](./client-brief.md)
* [Frontend README](./frontend/README.md)
* [Backend README](./backend/README.md)

## Local Development

### Prerequisites
* Python 3.14+
* Node.js v24.15.0+
* [pnpm](https://pnpm.io/)
* [uv](https://github.com/astral-sh/uv)

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/MedReview.git](https://github.com/your-username/MedReview.git)
   cd MedReview
   ```
2. **Backend Setup:**
   Navigate to the backend directory and start the server:
   ```bash
   cd backend
   cp .env.example .env
   uv run --locked --no-sync uvicorn app.main:create_app --factory --reload
   ```
   The backend API will be available at [http://localhost:8000](http://localhost:8000).
3. **Frontend Setup:**
Navigate to the frontend directory and start the development server:
   ```bash
   cd frontend
   cp .env.example .env
   pnpm install --frozen-lockfile
   pnpm dev
   ```
   The frontend application will be available at [http://localhost:5173](http://localhost:5173).