# MedReview Frontend
## Running locally
Navigate to the frontend directory and start the development server:
```bash
cd frontend
cp .env.example .env
pnpm install --frozen-lockfile
pnpm dev
```
The frontend application will be available at [http://localhost:5173](http://localhost:5173).

Requires the backend on `VITE_API_BASE_URL` (default `http://localhost:8000`).