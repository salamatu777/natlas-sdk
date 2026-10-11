import json
import urllib.request
import urllib.error
from typing import List, Dict, Any

class OllamaBackend:
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "natlas"):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name

    def generate(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream
        }
        
        if not stream:
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, 
                data=data_bytes, 
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    return res_json.get("message", {}).get("content", "")
            except urllib.error.URLError as e:
                return f"[Ollama Error: Could not connect to {url} - {e.reason}]"
            except Exception as e:
                return f"[Ollama Error: {e}]"
        else:
            raise NotImplementedError("Streaming is not fully implemented in OllamaBackend yet.")
