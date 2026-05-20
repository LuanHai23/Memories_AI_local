import requests
from app.core.config import settings

# Service để gọi LLM (Ollama)
class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are MemoRAG Agent, a helpful AI assistant. "
                        "Answer clearly and directly. "
                        "Do not return an empty response."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            # stream=False để đợi model trả lời xong một lần
            "stream": False,

            # options giúp kiểm soát output
            "options": {
                "temperature": 0.3,
                "num_predict": 512
            }
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=180
            )

            response.raise_for_status()

            data = response.json()

            message = data.get("message", {})
            content = message.get("content", "")

            # Clean response
            content = content.strip()

            # Nếu model trả rỗng thì báo lỗi rõ ràng
            if not content:
                raise RuntimeError(
                    f"Ollama returned empty response. Raw response: {data}"
                )

            return content

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {str(e)}")