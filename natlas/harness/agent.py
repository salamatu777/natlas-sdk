import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from natlas.harness.tools import SovereignToolRegistry
from natlas.guardrails import SovereignCulturalGuardrail

@dataclass
class AgentStep:
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[Dict[str, Any]] = None

@dataclass
class AgentExecutionResult:
    query: str
    language: str
    steps: List[AgentStep]
    final_response: str
    tools_invoked: List[str]
    guardrail_passed: bool

class SovereignAgentHarness:
    """
    Indigenous Agent Execution Harness for N-ATLAS.
    Inspired by DeepSeek-Harness modular agent loops.
    
    Provides:
    1. Pre-execution Cultural Guardrail Safety Check.
    2. Multi-step reasoning & tool calling against Nigerian environmental databases.
    3. Multilingual indigenous response formulation.
    """

    def __init__(self, client, tool_registry: Optional[SovereignToolRegistry] = None):
        self.client = client
        self.registry = tool_registry or SovereignToolRegistry()

    def run(self, query: str, language: str = "en", max_steps: int = 3) -> AgentExecutionResult:
        # Step 0: Sovereign Safety Verification
        safety = SovereignCulturalGuardrail.check_safety(query)
        if not safety.is_safe:
            return AgentExecutionResult(
                query=query,
                language=language,
                steps=[AgentStep(thought="Query flagged by sovereign safety guardrails.")],
                final_response=safety.mitigated_prompt,
                tools_invoked=[],
                guardrail_passed=False
            )

        steps: List[AgentStep] = []
        tools_invoked: List[str] = []

        # Heuristic intent parser for demonstration across sovereign tools
        lower_q = query.lower()

        # 1. Foreign Currency & FX Rate Benchmark
        if any(w in lower_q for w in ["dollar", "fx", "exchange", "pound", "euro", "cbn rate", "parallel market", "black market", "bdc", "kudin waje", "owo ilu oke"]):
            curr = "USD"
            if "gbp" in lower_q or "pound" in lower_q:
                curr = "GBP"
            elif "eur" in lower_q or "euro" in lower_q:
                curr = "EUR"

            obs = self.registry.execute("get_cbn_fx_rate", {"currency": curr})
            tools_invoked.append("get_cbn_fx_rate")
            steps.append(AgentStep(
                thought=f"Financial query requests Nigerian foreign exchange benchmark for {curr}.",
                action="get_cbn_fx_rate",
                action_input={"currency": curr},
                observation=obs
            ))

            agent_prompt = (
                f"User Question: {query}\n"
                f"Official CBN & Parallel Market FX Benchmark: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Answer concisely in {language} detailing the official vs parallel rate."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        # 2. Agricultural Commodity Prices
        elif any(w in lower_q for w in ["price", "cost", "farashi", "owo", "ego", "bag", "dawanau", "bodija", "market", "maize", "yam", "cassava", "rice", "rogo", "masara", "shinkafa", "doya"]):
            commodity = "maize"
            if "yam" in lower_q or "ji" in lower_q or "doya" in lower_q or "isu" in lower_q:
                commodity = "yam"
            elif "cassava" in lower_q or "rogo" in lower_q or "paki" in lower_q:
                commodity = "cassava"
            elif "rice" in lower_q or "shinkafa" in lower_q or "iresi" in lower_q:
                commodity = "rice"

            obs = self.registry.execute("get_nigerian_market_prices", {"commodity": commodity})
            tools_invoked.append("get_nigerian_market_prices")
            steps.append(AgentStep(
                thought=f"Farmer query asks about agricultural commodity market rates. Executing sovereign market lookup for {commodity}.",
                action="get_nigerian_market_prices",
                action_input={"commodity": commodity},
                observation=obs
            ))

            # Prompt LLM with observation
            agent_prompt = (
                f"User Question: {query}\n"
                f"Verified Market Observation: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Provide a helpful advisory response in {language} explaining the current price trends."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        elif any(w in lower_q for w in ["rain", "weather", "planting", "season", "ruwa", "kasa", "ojo", "ugbo", "climate"]):
            # Trigger agro weather tool
            state = "Kano"
            if "oyo" in lower_q or "ibadan" in lower_q:
                state = "Oyo"
            elif "benue" in lower_q or "makurdi" in lower_q:
                state = "Benue"
            elif "enugu" in lower_q:
                state = "Enugu"

            obs = self.registry.execute("get_agro_weather_advisory", {"state": state})
            tools_invoked.append("get_agro_weather_advisory")
            steps.append(AgentStep(
                thought=f"User requires localized weather and planting season advisory for {state}.",
                action="get_agro_weather_advisory",
                action_input={"state": state},
                observation=obs
            ))

            agent_prompt = (
                f"User Question: {query}\n"
                f"Agro-Climatic Guidance: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Formulate a direct, culturally empathetic answer in {language} for the farmer."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        elif any(w in lower_q for w in ["adp", "extension", "office", "knarda", "oysadep", "bnarda", "kadp", "enadep", "lasada", "hotline", "contact", "ofis", "ọfịs"]):
            # Trigger ADP extension directory tool
            state = "Kano"
            for s in ["Kano", "Oyo", "Benue", "Kaduna", "Enugu", "Lagos"]:
                if s.lower() in lower_q:
                    state = s
                    break

            obs = self.registry.execute("get_adp_extension_contact", {"state": state})
            tools_invoked.append("get_adp_extension_contact")
            steps.append(AgentStep(
                thought=f"Farmer query requires official ADP agricultural extension contact information for {state}.",
                action="get_adp_extension_contact",
                action_input={"state": state},
                observation=obs
            ))

            agent_prompt = (
                f"User Question: {query}\n"
                f"Verified State ADP Directory: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Provide the farmer with clear, official contact and location details in {language}."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        else:
            # Direct reasoning
            steps.append(AgentStep(thought="Direct indigenous reasoning without external tool execution required."))
            llm_response = self.client.chat(query, language=language)
            final_text = llm_response.text

        # Resilient synthesis fallback if remote backend or Ollama is unreachable
        if any(err_kw in (final_text or "") for err_kw in ["[Ollama Error", "[Inference error", "[API Backend Error", "Could not connect"]) and tools_invoked:
            final_text = self._synthesize_tool_observation(tools_invoked[0], steps[0].observation or {}, language)

        return AgentExecutionResult(
            query=query,
            language=language,
            steps=steps,
            final_response=final_text,
            tools_invoked=tools_invoked,
            guardrail_passed=True
        )

    def _synthesize_tool_observation(self, tool_name: str, obs: Dict[str, Any], language: str) -> str:
        lang = language[:2].lower()
        if tool_name == "get_nigerian_market_prices":
            commodity = obs.get("commodity", "amfanin gona")
            rates = obs.get("data", {})
            rate_str = ", ".join([f"{k}: {v}" for k, v in rates.items()]) if isinstance(rates, dict) else str(rates)
            if lang == "ha":
                return f"Bisa ga binciken kasuwannin Najeriya na yanzu:\nFarashin {commodity.capitalize()} shine: {rate_str}. Kudin na iya canzawa dangane da yanayin kasuwa."
            elif lang == "yo":
                return f"Gẹgẹbi iwadii ọja osunwon Naijiria ti ode oni:\nIye {commodity} jẹ: {rate_str}. Awọn owo wọnyi le yipada diẹ da lori agbegbe ati gbigbe."
            elif lang == "ig":
                return f"Dabere na nyocha ahịa n'ofe Naịjirịa:\nỌnụ ego {commodity} bụ: {rate_str}. Ọnụ ahịa nwere ike ịdịtụ iche dabere na oge na ebe a na-ere ya."
            else:
                return f"According to verified Nigerian wholesale market benchmarks:\nPrice of {commodity.capitalize()}: {rate_str}. Rates may vary slightly based on volume and transport."

        elif tool_name == "get_agro_weather_advisory":
            state = obs.get("state", "Nigeria")
            season = obs.get("season", "Seasonal Phase")
            prob = obs.get("rain_probability", "moderate")
            adv = obs.get("planting_advisory", "Consult local extension officer.")
            if lang == "ha":
                return f"Jagoran yanayi na jihar {state}:\nLokaci: {season} (Yiwuwar ruwa: {prob}).\nShawarar noma: {adv}"
            elif lang == "yo":
                return f"Itọsọna oju-ọjọ fun Ipinlẹ {state}:\nAkoko: {season} (O ṣeeṣe ki ojo rọ: {prob}).\nImọran ogbin: {adv}"
            elif lang == "ig":
                return f"Nduzi ihu igwe maka steeti {state}:\nOge: {season} (Ohere mmiri ozuzo: {prob}).\nNdụmọdụ ọrụ ugbo: {adv}"
            else:
                return f"Agro-climatic advisory for {state} State:\nSeason: {season} (Rain probability: {prob}).\nPlanting guidance: {adv}"

        elif tool_name == "get_adp_extension_contact":
            state = obs.get("state", "Nigeria")
            agency = obs.get("agency", f"{state} State ADP")
            hq = obs.get("hq", "State Secretariat")
            hotline = obs.get("extension_hotline", "Contact State Ministry")
            if lang == "ha":
                return f"Ofishin bunkasa aikin gona na jihar {state} (ADP):\nHukuma: {agency}\nWuri: {hq}\nLambar waya: {hotline}"
            elif lang == "yo":
                return f"Ọfiisi iṣẹ-ogbin Ipinlẹ {state} (ADP):\nIle-iṣẹ: {agency}\nIbudo: {hq}\nNọmba iranlọwọ: {hotline}"
            elif lang == "ig":
                return f"Ụlọ ọrụ mmepe ọrụ ugbo steeti {state} (ADP):\nỤlọ ọrụ: {agency}\nEbe: {hq}\nNọmba ekwentị: {hotline}"
            else:
                return f"Official Agricultural Development Programme (ADP) for {state} State:\nAgency: {agency}\nHeadquarters: {hq}\nSupport Contact: {hotline}"

        elif tool_name == "get_cbn_fx_rate":
            curr = obs.get("currency", "USD")
            official = obs.get("cbn_official", "N/A")
            bdc = obs.get("parallel_bdc", "N/A")
            if lang == "ha":
                return f"Matsayin canjin kudin waje na {curr} a Najeriya:\nFarashin CBN na hukuma: {official}\nFarashin kasuwar 'yan canji (Parallel): {bdc}"
            elif lang == "yo":
                return f"Iye owo paṣipaarọ {curr} ni Naijiria loni:\nIye osise ti CBN: {official}\nIye ọja eleto (Parallel BDC): {bdc}"
            elif lang == "ig":
                return f"Ọnụego mgbanwe ego {curr} na Naịjirịa:\nỌnụego gọọmentị CBN: {official}\nỌnụego ahịa n'efu (Parallel BDC): {bdc}"
            else:
                return f"Foreign Exchange Benchmark for {curr}/NGN:\nOfficial CBN Rate: {official}\nParallel Market (BDC) Benchmark: {bdc}"

        return json.dumps(obs, ensure_ascii=False)
