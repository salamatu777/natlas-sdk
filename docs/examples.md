# 💡 Developer Examples — N-ATLAS Developer Harness

Real-world code patterns for building production applications with `natlas-sdk`.

---

## 1. Multilingual Customer Support Bot (Hausa, Yorùbá, Igbo)

```python
from natlas import NAtlasClient
from natlas.guardrails import SovereignCulturalGuardrail

client = NAtlasClient()

def handle_user_inquiry(user_message: str, user_language: str = "ha") -> str:
    # 1. Cultural safety audit
    safety = SovereignCulturalGuardrail.check_safety(user_message)
    if not safety.is_safe:
        return "Gargadi: Sakonka ya keta ka'idojin tsaro."
        
    # 2. Generate response with clean session isolation
    response = client.chat(user_message, language=user_language, isolate=True, max_tokens=150)
    return response.text
```

---

## 2. Agricultural Commodity Price Bot with Agent Tools

```python
from natlas import NAtlasClient
from natlas.harness.agent import SovereignAgentHarness

client = NAtlasClient()
agent = SovereignAgentHarness(client)

# Ask about commodity prices in native vernacular
query = "Nawa ne farashin buhun masara a Dawanau a yau?"
result = agent.run(query, language="ha")

print("--- Agent Execution Trace ---")
for step in result.steps:
    print(f"Thought: {step.thought}")
    if step.action:
        print(f"Action: {step.action}({step.action_input})")
        print(f"Observation: {step.observation}")

print("\n--- Final Advice to Farmer ---")
print(result.final_response)
```

---

## 3. High-Throughput Yorùbá Text Ingestion Pipeline

```python
from natlas.orthography import NigerianOrthographyEngine

articles = [
    "Báwo ni a ṣe lè kọ́ èdè Yorùbá pẹ̀lú àmì ohùn tó tọ́?",
    "Àwọn àrùn tí ń kọlu irugbin rogo ní ilẹ̀ Naijiria."
]

for text in articles:
    report = NigerianOrthographyEngine.analyze_token_fertility(text, language="yo")
    print(f"Original Text: {text}")
    print(f"Fertility Ratio: {report.fertility_ratio} tokens/word")
    
    # Strip diacritics for cost-effective embedding or search indexing
    clean_text = NigerianOrthographyEngine.strip_diacritics(text)
    print(f"Stripped (42% savings): {clean_text}\n")
```

---

## 4. Automated CI/CD Model Evaluation Gate

```python
from natlas import NAtlasClient
from natlas.harness.eval import SovereignBenchmarkHarness

client = NAtlasClient()
harness = SovereignBenchmarkHarness(client)

# Run benchmark suite
report = harness.run_suite(live=False)
print(report.summary_markdown)

# Check quality gate
if report.overall_score < 3.5:
    print("❌ Quality Gate Failed: Model performance does not meet national standards.")
    exit(1)
else:
    print("✅ Quality Gate Passed: Ready for national deployment.")
```
