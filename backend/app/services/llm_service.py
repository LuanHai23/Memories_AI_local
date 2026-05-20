import requests
from app.core.config import settings

# Service để gọi LLM (Ollama)
class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = resquests.post(
                url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return data.get("text", "").strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")