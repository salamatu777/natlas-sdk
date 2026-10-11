from typing import Optional, Union, BinaryIO, Dict
from dataclasses import dataclass

@dataclass
class ASRResult:
    text: str
    language: str
    confidence: float

class ASRPipeline:
    MODELS = {
        "ha": "NCAIR1/Hausa-ASR",
        "yo": "NCAIR1/Yoruba-ASR",
        "ig": "NCAIR1/Igbo-ASR",
        "en": "NCAIR1/NigerianAccentedEnglish"
    }

    def __init__(self, hf_token: Optional[str] = None, device: str = "cpu"):
        self.hf_token = hf_token
        self.device = device
        self.pipelines = {}
        self._init_models()

    def _init_models(self):
        # Lazy loading of transformers
        try:
            from transformers import pipeline
            for lang, model_id in self.MODELS.items():
                self.pipelines[lang] = pipeline(
                    "automatic-speech-recognition", 
                    model=model_id, 
                    token=self.hf_token,
                    device=0 if self.device == "cuda" else -1,
                    chunk_length_s=30
                )
        except ImportError:
            pass

    def transcribe(self, audio: Union[str, bytes, BinaryIO], language: Optional[str] = None) -> ASRResult:
        if not self.pipelines:
            raise RuntimeError("Transformers backend is not installed or models failed to load.")
            
        if language and language in self.pipelines:
            res = self.pipelines[language](audio)
            return ASRResult(text=res["text"], language=language, confidence=1.0)
        
        # Auto-detect language by running all and picking the best confidence (heuristic based for now)
        best_text = ""
        best_lang = "en"
        best_conf = 0.0
        
        for lang, pipe in self.pipelines.items():
            res = pipe(audio)
            # In a real implementation, we'd use a language ID model or confidence scores from the Whisper model
            # For simplicity, returning the first non-empty text, or assuming English fallback
            if res and "text" in res and res["text"].strip():
                best_text = res["text"]
                best_lang = lang
                best_conf = 0.8 # Placeholder
                break
                
        return ASRResult(text=best_text, language=best_lang, confidence=best_conf)
