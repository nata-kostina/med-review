from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class AppConfig:
    database_url: str = f"sqlite:///{Path('./data/documents.db').resolve()}"
    min_field_confidence: float = 0.80
    upload_dir: Path = Path("./data/uploads")
    max_upload_bytes: int = 4 * 1024 * 1024
    
APP_CONFIG = AppConfig()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    allowed_origin: str = "http://localhost:5173"
    
    azure_document_intelligence_endpoint: str
    azure_document_intelligence_key: str
    
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    
    frontend_dist_dir: Path | None = None
    
    def resolve_frontend_dist(self) -> Path | None:
        if self.frontend_dist_dir is not None:
            path = self.frontend_dist_dir
            return path if path.is_dir() else None
        for candidate in (
            BACKEND_ROOT.parent / "frontend" / "dist",
            Path("/app/frontend/dist"),
        ):
            if candidate.is_dir():
                return candidate
        return None

    
@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore