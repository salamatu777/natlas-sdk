import os
import io
from typing import Optional, Union, BinaryIO

from .chat import ChatPipeline, ChatMessage
from .asr import ASRPipeline
from .pipeline import VoicePipeline

__version__ = "0.1.0"

class NAtlasClient:
    def __init__(
        self,
        hf_token: Optional[str] = None,
        backend: Optional[str] = None,
        api_url: Optional[str] = None,
        ollama_base_url: str = "http://localhost:11434",
        ollama_model: str = "natlas",
        device: str = "cpu"
    ):
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")
        remote_url = api_url or os.environ.get("NATLAS_API_URL")
        
        if remote_url and not backend:
            self.backend_type = "api"
            base_url = remote_url
        elif backend in ["api", "openai", "openai_compat"]:
            self.backend_type = backend
            base_url = api_url or os.environ.get("NATLAS_API_URL") or "http://localhost:8000/v1"
        else:
            self.backend_type = backend or "ollama"
            base_url = ollama_base_url

        self.chat_pipeline = ChatPipeline(
            backend=self.backend_type,
            hf_token=self.hf_token,
            ollama_base_url=base_url,
            ollama_model=ollama_model,
            device=device
        )
        self.asr_pipeline = None
        self.voice_pipeline_instance = None
        self.device = device

    def _init_asr(self):
        if self.asr_pipeline is None:
            self.asr_pipeline = ASRPipeline(hf_token=self.hf_token, device=self.device)

    def chat(
        self,
        prompt: str,
        language: str = "en",
        isolate: bool = False,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> ChatMessage:
        return self.chat_pipeline.generate(
            prompt,
            language=language,
            isolate=isolate,
            max_tokens=max_tokens,
            system_prompt=system_prompt
        )
        
    def transcribe(self, audio: Union[str, bytes, BinaryIO], language: Optional[str] = None):
        self._init_asr()
        return self.asr_pipeline.transcribe(audio, language=language)
        
    def voice_pipeline(self, audio: Union[str, bytes, BinaryIO]):
        self._init_asr()
        if self.voice_pipeline_instance is None:
            self.voice_pipeline_instance = VoicePipeline(self.asr_pipeline, self.chat_pipeline)
        return self.voice_pipeline_instance.run(audio)
