from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import APP_CONFIG, get_settings
from app.database import build_database
from app.documents.models import DocumentRecord
from app.documents.routes import router as document_router
from app.providers.azure_openai import build_azure_openai_client
from app.providers.azure_openai_correction_email import AzureOpenAICorrectionEmailDrafter
from app.providers.azure_openai_document_review import AzureOpenAIDocumentReviewer
from app.services.document_intelligence_service import DocumentIntelligenceService


def create_app() -> FastAPI:
    config = APP_CONFIG
    config.upload_dir.mkdir(parents=True, exist_ok=True)
    
    database_path = config.database_url.removeprefix("sqlite:///")
    if config.database_url.startswith("sqlite:///"):
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    
    engine, session_factory = build_database(config.database_url)
    DocumentRecord.metadata.create_all(engine)   
    
    settings = get_settings()
    openai_client = build_azure_openai_client(settings) 
    
    app = FastAPI(title="Med Review API", version="0.1.0")
    app.state.config = config
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.service = DocumentIntelligenceService(settings=settings)
    app.state.reviewer = AzureOpenAIDocumentReviewer(
        client=openai_client,
        deployment_name=settings.azure_openai_deployment,
    )
    app.state.correction_email_drafter = AzureOpenAICorrectionEmailDrafter(
        client=openai_client, 
        deployment_name=settings.azure_openai_deployment,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.allowed_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(document_router)
    
    frontend_dist = settings.resolve_frontend_dist()
    if frontend_dist is not None:
        assets_dir = frontend_dist / "assets"
        if assets_dir.is_dir():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/{full_path:path}")
        def spa_fallback(full_path: str) -> FileResponse:
            candidate = frontend_dist / full_path
            if full_path and candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(frontend_dist / "index.html")

    return app