from openai import OpenAI
from openai.types.responses import Response

from app.config import Settings, get_settings


class AzureOpenAIService:
    def __init__(self, settings: Settings | None = None) -> None:
        resolved_settings = settings or get_settings()
        self._client = OpenAI(
            base_url=resolved_settings.azure_openai_endpoint,
            api_key=resolved_settings.azure_openai_api_key
        )
        self._deployment = resolved_settings.azure_openai_deployment
        
    def create_response(self, input: str) -> Response:
        return self._client.responses.create(
            model=self._deployment,
            input=input,
        )