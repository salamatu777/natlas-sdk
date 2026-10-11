# 🚀 Quickstart Guide — N-ATLAS Developer Harness (DSH)

Get up and running with Nigeria's sovereign AI developer toolkit in under 2 minutes.

---

## 1. Installation

Install the package via pip:

```bash
pip install natlas-sdk
```

Or clone the repository directly for development:

```bash
git clone https://github.com/lukman155/natlas-sdk.git
cd natlas-sdk
pip install -e .
```

*Zero heavy dependencies required for core usage. Standard library Python 3.10+ supported.*

---

## 2. Initialize the Client

The `NAtlasClient` automatically connects to local Ollama/GGUF instances, your self-hosted vLLM/FastAPI endpoints, or Hugging Face cloud endpoints:

```python
from natlas import NAtlasClient

# 1. Connect to default local or environment URL (NATLAS_API_URL)
client = NAtlasClient()

# 2. Or connect to a remote GPU endpoint
client = NAtlasClient(api_url="https://your-ngrok-or-gpu-host.com")
```

---

## 3. Multilingual Chat Inference

Query `NCAIR1/N-ATLaS` directly across Nigeria's major languages:

```python
# Hausa
res_ha = client.chat("Yaya ake shuka masara a Najeriya?", language="ha")
print(res_ha.text)

# Yorùbá
res_yo = client.chat("Bawo ni mo se le da oko rogo sile?", language="yo")
print(res_yo.text)

# Igbo
res_ig = client.chat("Kedu ka esi akọ ugbo ji?", language="ig")
print(res_ig.text)

# Nigerian English
res_en = client.chat("How do I prevent armyworm infestation?", language="en")
print(res_en.text)
```

---

## 4. Orthography & Token Fertility Optimization

Reduce Yorùbá and Igbo token fragmentation by up to 50%:

```python
from natlas.orthography import NigerianOrthographyEngine

text = "Báwo ni a ṣe lè kọ́ èdè Yorùbá pẹ̀lú àmì ohùn tó tọ́?"

# Analyze token bloat
report = NigerianOrthographyEngine.analyze_token_fertility(text, language="yo")
print(f"Fertility Ratio: {report.fertility_ratio} tokens/word")
print(f"Recommendation: {report.recommendation}")

# Strip/normalize diacritics for low-latency production pipelines
clean_text = NigerianOrthographyEngine.strip_diacritics(text)
print(f"Optimized: {clean_text}")
```

---

## 5. Sovereign Cultural Guardrail Safety Audit

Inspect prompts against Nigerian cultural and legal standards:

```python
from natlas.guardrails import SovereignCulturalGuardrail

prompt = "Send your BVN and NIN to claim the CBN grant approved today."

result = SovereignCulturalGuardrail.check_safety(prompt)
if not result.is_safe:
    print(f"Alert: {result.risk_level} - {result.flagged_categories}")
    print(f"Mitigated Prompt: {result.mitigated_prompt}")
```

---

## 6. DeepSeek-Style Agent Tool Execution

Execute multi-step reasoning with access to verified Nigerian databases:

```python
from natlas.harness.agent import SovereignAgentHarness

agent = SovereignAgentHarness(client)
result = agent.run("Nawa ne farashin buhun masara a Dawanau?", language="ha")

print(f"Tools Invoked: {result.tools_invoked}")
print(f"Final Advisory: {result.final_response}")
```

---

## 7. Launch Visual Developer Workbench

Launch the visual interactive workbench locally:

```bash
natlas serve --port 8000
```

Then open your browser at **`http://localhost:8000/harness`**.
