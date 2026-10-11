from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time
import tempfile
import pathlib

from natlas.client import NAtlasClient
from natlas.orthography import NigerianOrthographyEngine
from natlas.guardrails import SovereignCulturalGuardrail
from natlas.harness.agent import SovereignAgentHarness
from natlas.harness.eval import SovereignBenchmarkHarness

app = FastAPI(title="N-ATLAS Sovereign API & Developer Harness", version="0.2.0")

# Default to the live Kaggle GPU server, or env variable if set
DEFAULT_GPU_URL = os.environ.get("NATLAS_API_URL", "https://86aa-34-170-208-126.ngrok-free.app")
client = NAtlasClient(api_url=DEFAULT_GPU_URL)
agent_harness = SovereignAgentHarness(client)
benchmark_harness = SovereignBenchmarkHarness(client)

class ChatMessageInput(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "NCAIR1/N-ATLaS"
    messages: List[ChatMessageInput]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 512
    stream: Optional[bool] = False

class OrthographyRequest(BaseModel):
    text: str
    language: Optional[str] = "yo"

class GuardrailRequest(BaseModel):
    text: str

class AgentRequest(BaseModel):
    query: str
    language: Optional[str] = "ha"

class MatrixRequest(BaseModel):
    prompt: str
    languages: Optional[List[str]] = ["ha", "yo", "ig", "en"]

class EndpointConfigRequest(BaseModel):
    api_url: str

# Serve the visual developer harness at root and /harness
@app.get("/", response_class=HTMLResponse)
@app.get("/harness", response_class=HTMLResponse)
async def get_harness():
    template_path = pathlib.Path(__file__).parent / "harness" / "templates" / "harness.html"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>N-ATLAS Developer Harness</h1><p>Template not found.</p>"

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
    last_message = req.messages[-1].content
    response = client.chat(last_message)
    
    return {
        "id": "chatcmpl-natlas",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response.text,
            },
            "finish_reason": "stop"
        }]
    }

@app.post("/v1/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...), model: str = "whisper-1"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        
        result = client.transcribe(tmp.name)
        
    os.unlink(tmp.name)
    return {"text": result.text, "language": result.language}

# HARNESS DIAGNOSTIC API ENDPOINTS (CONNECTED TO LIVE DATA)

@app.get("/harness/status")
async def harness_status():
    backend_info = client.backend_type
    current_url = getattr(client.chat_pipeline.backend, "base_url", "local")
    return {
        "status": "online",
        "backend": backend_info,
        "target_model": "NCAIR1/N-ATLaS (8B SFT)",
        "api_endpoint": current_url,
        "is_live_gpu": "ngrok" in current_url or "http" in current_url
    }

@app.post("/harness/set-endpoint")
async def set_endpoint(req: EndpointConfigRequest):
    global client, agent_harness, benchmark_harness
    client = NAtlasClient(api_url=req.api_url)
    agent_harness = SovereignAgentHarness(client)
    benchmark_harness = SovereignBenchmarkHarness(client)
    return {"status": "updated", "new_endpoint": req.api_url}

LANGUAGE_PROMPTS = {
    "ha": "Amsa wannan tambaya a harshen Hausa a takaice (cikin kalmomi 60 zuwa 80): ",
    "yo": "Dahun ibeere yi ni ede Yoruba ni soki (laarin gbolohun kukuru): ",
    "ig": "Zaa ajụjụ a n'asụsụ Igbo nkenke (n'okwu 60 ruo 80): ",
    "en": "Answer this question concisely in clear Nigerian English (under 75 words): ",
}

class SingleQueryRequest(BaseModel):
    prompt: str
    language: str = "ha"
    max_tokens: Optional[int] = 140

@app.post("/harness/query-single")
async def query_single(req: SingleQueryRequest):
    """Execute live query for a single language with threadpool execution."""
    import asyncio
    t0 = time.time()
    lang = req.language.lower()
    prefix = LANGUAGE_PROMPTS.get(lang, "")
    full_prompt = f"{prefix}{req.prompt}" if prefix else req.prompt
    max_toks = req.max_tokens or 140
    
    try:
        resp = await asyncio.to_thread(
            client.chat,
            full_prompt,
            language=lang,
            isolate=True,
            max_tokens=max_toks
        )
        text = resp.text
    except Exception as e:
        text = f"[Inference error: {str(e)}]"
        
    duration_ms = round((time.time() - t0) * 1000, 1)
    words = len(text.split())
    tokens = int(words * 1.4)
    tps = round(tokens / max(duration_ms / 1000, 0.1), 1)
    return {
        "language": req.language,
        "text": text,
        "latency_ms": duration_ms,
        "tokens_per_sec": tps,
        "tokens": tokens
    }

@app.post("/harness/matrix-query")
async def matrix_query(req: MatrixRequest):
    """Execute live query across Hausa, Yoruba, Igbo, and English concurrently."""
    import asyncio
    t0 = time.time()
    results = {}
    
    async def fetch_one(lang):
        try:
            prefix = LANGUAGE_PROMPTS.get(lang.lower(), "")
            full_prompt = f"{prefix}{req.prompt}" if prefix else req.prompt
            resp = await asyncio.to_thread(
                client.chat,
                full_prompt,
                language=lang,
                isolate=True,
                max_tokens=140
            )
            return lang, resp.text
        except Exception as e:
            return lang, f"[Inference error for {lang}: {str(e)}]"
            
    tasks = [fetch_one(lang) for lang in req.languages]
    completed = await asyncio.gather(*tasks)
    for lang, txt in completed:
        results[lang] = txt
        
    duration_ms = round((time.time() - t0) * 1000, 1)
    total_words = sum(len(txt.split()) for txt in results.values())
    est_tokens = int(total_words * 1.4)
    tps = round(est_tokens / max(duration_ms / 1000, 0.1), 1)
    
    return {
        "results": results,
        "latency_ms": duration_ms,
        "tokens_per_sec": tps,
        "estimated_tokens": est_tokens,
        "gpu_endpoint": getattr(client.chat_pipeline.backend, "base_url", "local")
    }

@app.post("/harness/analyze-tokens")
async def analyze_tokens(req: OrthographyRequest):
    report = NigerianOrthographyEngine.analyze_token_fertility(req.text, req.language)
    return report

@app.post("/harness/guardrail-check")
async def guardrail_check(req: GuardrailRequest):
    result = SovereignCulturalGuardrail.check_safety(req.text)
    return result

@app.post("/harness/agent-run")
async def agent_run(req: AgentRequest):
    """Execute real multi-step agent reasoning against live GPU and sovereign tools."""
    t0 = time.time()
    result = agent_harness.run(req.query, req.language)
    duration_ms = round((time.time() - t0) * 1000, 1)
    
    steps_data = [
        {
            "thought": s.thought,
            "action": s.action,
            "action_input": s.action_input,
            "observation": s.observation
        }
        for s in result.steps
    ]
    
    return {
        "query": result.query,
        "language": result.language,
        "steps": steps_data,
        "final_response": result.final_response,
        "tools_invoked": result.tools_invoked,
        "guardrail_passed": result.guardrail_passed,
        "execution_time_ms": duration_ms
    }

@app.get("/harness/eval-suite")
async def run_eval_suite(live: Optional[bool] = False):
    import asyncio
    report = await asyncio.to_thread(benchmark_harness.run_suite, live=live)
    return report

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "NCAIR1/N-ATLaS", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Hausa-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Yoruba-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Igbo-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/NigerianAccentedEnglish", "object": "model", "owned_by": "ncair"}
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "ok", 
        "version": "0.2.0-harness",
        "gpu_endpoint": getattr(client.chat_pipeline.backend, "base_url", "local")
    }
