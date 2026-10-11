import os
import json
import ssl
import urllib.request
import urllib.error
from typing import List, Dict

class OpenAICompatBackend:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "NCAIR1/N-ATLaS"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "dummy")
        url = base_url or os.environ.get("NATLAS_API_URL") or os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1")
        self.base_url = url.rstrip("/")
        if not self.base_url.endswith("/v1") and not self.base_url.endswith("/chat/completions"):
            self.base_url += "/v1"
        self.model = model
        self.ssl_ctx = ssl._create_unverified_context()

    def generate(self, messages: List[Dict[str, str]], stream: bool = False, max_tokens: int = 512, temperature: float = 0.1) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "ngrok-skip-browser-warning": "1",
            "User-Agent": "NAtlasClient/0.2.0"
        }
        req = urllib.request.Request(url, data=data_bytes, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120, context=self.ssl_ctx) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                return res_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except urllib.error.URLError as e:
            return f"[API Backend Error: Could not connect to {url} - {e.reason}]"
        except Exception as e:
            return f"[API Backend Error: {e}]"
