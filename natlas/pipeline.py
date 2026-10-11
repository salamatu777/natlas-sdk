from typing import Union, BinaryIO
from dataclasses import dataclass

@dataclass
class VoicePipelineResult:
    transcript: str
    response: str
    language: str

class VoicePipeline:
    def __init__(self, asr_pipeline, chat_pipeline):
        self.asr_pipeline = asr_pipeline
        self.chat_pipeline = chat_pipeline

    def run(self, audio: Union[str, bytes, BinaryIO]) -> VoicePipelineResult:
        # 1. Transcribe audio
        asr_result = self.asr_pipeline.transcribe(audio)
        transcript = asr_result.text
        language = asr_result.language
        
        # 2. Feed transcript to chat
        chat_response = self.chat_pipeline.generate(transcript, language=language)
        
        # TTS will go here in the future
        
        return VoicePipelineResult(
            transcript=transcript,
            response=chat_response.text,
            language=language
        )
