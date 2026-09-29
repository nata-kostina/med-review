import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.services.azure_openai_service import AzureOpenAIService


def main():
    prompt = "What is the capital of France?"
    openai_service = AzureOpenAIService()
    response = openai_service.create_response(prompt)
    
    print(response.output[0].content[0].text) # type: ignore
    
    
if __name__ == "__main__":
    main()