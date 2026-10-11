# 📖 API Reference — N-ATLAS Developer Harness (DSH v0.2.0)

Complete class and method specifications for `natlas-sdk`.

---

## 1. `natlas.NAtlasClient`
The primary client interface unifying text generation, speech recognition, and agent execution.

```python
from natlas import NAtlasClient

client = NAtlasClient(
    hf_token: Optional[str] = None,
    backend: Optional[str] = None,
    api_url: Optional[str] = None,
    ollama_base_url: str = "http://localhost:11434",
    ollama_model: str = "natlas",
    device: str = "cpu"
)
```

### Methods
- `chat(prompt: str, language: str = "en", isolate: bool = False, max_tokens: Optional[int] = None, system_prompt: Optional[str] = None) -> ChatResponse`
  - Generates text from the N-ATLAS 8B model.
  - `isolate=True` creates an ephemeral context session (preventing conversation history bloat).
- `transcribe(audio: Union[str, bytes, BinaryIO], language: Optional[str] = None) -> ASRResult`
  - Transcribes audio using N-ATLAS Whisper Small models (`Hausa-ASR`, `Yoruba-ASR`, `Igbo-ASR`, `NigerianAccentedEnglish`).
- `voice_pipeline(audio: Union[str, bytes, BinaryIO]) -> VoicePipelineResult`
  - Executes end-to-end voice loop: Speech $\rightarrow$ ASR $\rightarrow$ LLM generation.

---

## 2. `natlas.orthography.NigerianOrthographyEngine`
Orthographic analysis and token fertility optimization.

### Methods
- `analyze_token_fertility(text: str, language: str = "yo") -> TokenFertilityReport`
  - Returns word count, estimated BPE tokens, fertility ratio, and optimization recommendations.
- `strip_diacritics(text: str) -> str`
  - Normalizes tonal accents and under-dot diacritics into unaccented base characters, reducing token bloat by ~42%.
- `count_diacritics(text: str) -> int`
  - Scans for Nigerian diacritics in Yorùbá (`ẹ, ọ, ṣ`) and Igbo (`ị, ụ, ṅ`).

---

## 3. `natlas.guardrails.SovereignCulturalGuardrail`
Sovereign content moderation and socio-cultural alignment.

### Methods
- `check_safety(text: str) -> GuardrailResult`
  - Evaluates text against ethnic slur patterns, religious incitement, and financial scams (BVN/NIN/CBN fraud).
  - Returns `is_safe` (bool), `risk_level` ("LOW", "MEDIUM", "HIGH"), `flagged_categories`, and `mitigated_prompt`.

---

## 4. `natlas.harness.agent.SovereignAgentHarness`
DeepSeek-Harness inspired agent reasoning loop with sovereign tool calling.

```python
from natlas.harness.agent import SovereignAgentHarness

agent = SovereignAgentHarness(client, tool_registry=None)
```

### Methods
- `run(query: str, language: str = "en", max_steps: int = 3) -> AgentExecutionResult`
  - Performs: Safety Pre-check $\rightarrow$ Intent Reasoner $\rightarrow$ Tool Invocation $\rightarrow$ Indigenous Response Formulation.
  - Returns `query`, `language`, `steps` (list of thoughts/actions/observations), `final_response`, and `tools_invoked`.

---

## 5. `natlas.harness.eval.SovereignBenchmarkHarness`
Automated benchmark and bias evaluation suite.

```python
from natlas.harness.eval import SovereignBenchmarkHarness

harness = SovereignBenchmarkHarness(client)
```

### Methods
- `run_suite(suite_name: str = "all", live: bool = False) -> SovereignEvaluationReport`
  - Executes standardized tests across Hausa Cultural Bias, Yorùbá Token Fertility, Igbo Reasoning, and Nigerian English Acoustics.
  - Returns composite scores, pass/fail indicators, and a formatted Markdown report card.
