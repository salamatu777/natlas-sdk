from typing import Optional, List, Dict
from dataclasses import dataclass
import os

@dataclass
class ChatMessage:
    role: str
    content: str
    
@dataclass
class ChatResponse:
    text: str
    language: str

SYSTEM_PROMPT = "you are a large language model trained by Awarri AI technologies. You are a friendly assistant and you are here to help."

class ChatPipeline:
    def __init__(self, backend="ollama", hf_token=None, ollama_base_url="http://localhost:11434", ollama_model="natlas", device="cpu"):
        self.backend_type = backend
        self.hf_token = hf_token
        self.system_prompt = SYSTEM_PROMPT
        self.history = [{"role": "system", "content": self.system_prompt}]
        
        if self.backend_type == "transformers":
            from .backends.transformers import TransformersBackend
            self.backend = TransformersBackend(model_id="NCAIR1/N-ATLaS", hf_token=self.hf_token, device=device)
        elif self.backend_type == "ollama":
            from .backends.ollama import OllamaBackend
            self.backend = OllamaBackend(base_url=ollama_base_url, model_name=ollama_model)
        elif self.backend_type in ["openai", "openai_compat", "api"]:
            from .backends.openai_compat import OpenAICompatBackend
            self.backend = OpenAICompatBackend(base_url=ollama_base_url)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def reset_history(self):
        """Reset conversational history to initial system prompt."""
        self.history = [{"role": "system", "content": self.system_prompt}]

    def generate(
        self,
        prompt: str,
        language: str = "en",
        stream: bool = False,
        isolate: bool = False,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> ChatResponse:
        sys_msg = system_prompt or self.system_prompt
        if isolate:
            messages = [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": prompt}
            ]
        else:
            self.history.append({"role": "user", "content": prompt})
            messages = self.history

        # Call backend with max_tokens if supported
        kwargs = {"stream": stream}
        if max_tokens is not None and hasattr(self.backend, "generate"):
            try:
                response_text = self.backend.generate(messages, stream=stream, max_tokens=max_tokens)
            except TypeError:
                response_text = self.backend.generate(messages, stream=stream)
        else:
            response_text = self.backend.generate(messages, stream=stream)

        if not isolate:
            self.history.append({"role": "assistant", "content": response_text})

        return ChatResponse(text=response_text, language=language)
