# 🇳🇬 N-ATLAS Developer Harness (DSH v0.2.0)

Welcome to the official developer documentation for the **N-ATLAS Developer Harness (DSH)**, built for the National AI Innovation Challenge (NAIC 2026) under Problem Statement 1: Developer Infrastructure.

---

## 📚 Table of Contents

- [Quickstart Guide](quickstart.md) — 2-minute setup and quickstart examples.
- [API Reference](api-reference.md) — Complete class and method definitions.
- [Developer Examples](examples.md) — Real-world code patterns for agents, bots, and pipelines.

---

## 🌟 Key Architecture Modules

1. **`natlas.client.NAtlasClient`**: Unified interface for chat, Whisper speech recognition, and streaming.
2. **`natlas.orthography.NigerianOrthographyEngine`**: Token fertility analyzer and diacritic stripper for Yorùbá and Igbo.
3. **`natlas.guardrails.SovereignCulturalGuardrail`**: Nigerian cultural, ethical, and legal safety moderation.
4. **`natlas.harness.agent.SovereignAgentHarness`**: DeepSeek-style agent execution loop with live Nigerian environmental tools.
5. **`natlas.harness.eval.SovereignBenchmarkHarness`**: Automated AfroBench diagnostic test suite.
6. **Visual Developer Workbench**: Interactive web UI at `http://localhost:8000/harness`.

---

## 🏛️ Attribution & Credits

- **N-ATLAS** is an initiative of the **Federal Ministry of Communications, Innovation and Digital Economy (FMCIDE)**, powered by **Awarri Technologies**.
- Models developed by the **National Centre for Artificial Intelligence and Robotics (NCAIR)**, a special-purpose vehicle of **NITDA**.
- Distributed under the MIT Open Source License.
