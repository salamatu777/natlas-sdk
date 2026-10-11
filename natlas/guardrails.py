import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class GuardrailResult:
    is_safe: bool
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    flagged_categories: List[str]
    matched_triggers: List[str]
    mitigated_prompt: str
    explanation: str

class SovereignCulturalGuardrail:
    """
    Sovereign Cultural Safety & Bias Guardrail for Nigerian AI Deployments.
    
    Standard Western safety layers (Llama Guard, OpenAI Moderation) are blind to 
    Nigerian socio-political context, tribal slurs, ethnic profiling, and localized fraud.
    
    This guardrail inspects prompts and responses for:
    1. Ethnic profiling & tribal slurs across Hausa, Yoruba, Igbo, Fulani (with contextual awareness for honorifics).
    2. Religious extremism and sectarian violence incitement.
    3. Financial cybercrime (419, Advance Fee, BVN/NIN/ATM PIN harvesting, EFCC/CBN impersonation).
    4. Sectarian displacement and inter-communal violence triggers.
    """

    ETHNIC_SLURS_AND_HATE = {
        # Derogatory slurs targeting specific communities
        r"\b(yamiri|nyamiri)\b": "Ethnic Slur (Targeting Igbo community)",
        r"\b(ofe\s*mmanu)\b": "Ethnic Slur (Targeting Yoruba community)",
        
        # Contextual 'aboki' evaluation:
        # 'Aboki' in Hausa means 'friend'. It is ONLY flagged when combined with pejorative or derogatory insults.
        r"\b(aboki)\s+(idiot|fool|stupid|bastard|animal|dirty|useless|senseless|mumu|thief|thieves)\b": "Pejorative Ethnic Slur (Northern profiling)",
        r"\b(idiot|fool|stupid|bastard|animal|dirty|useless|senseless|mumu|thief|thieves)\s+(aboki)\b": "Pejorative Ethnic Slur (Northern profiling)",
        
        # Collective ethnic profiling & generalizations
        r"\b(all\s+)?fulani(\s+herdsmen)?\s+(are\s+)?(all\s+)?(terrorists?|killers?|murderers?|criminals?|evil)\b": "Ethnic Profiling & Collective Criminalization",
        r"\b(all\s+)?(igbos?|yorubas?|hausas?|fulanis?)\s+(are\s+)?(all\s+)?(thieves|fraudsters|terrorists|traitors|cowards)\b": "Ethnic Profiling & Tribal Stereotyping",
        
        # Violent incitement & communal displacement
        r"\b(kill|slaughter|wipe\s*out|eliminate|exterminate|attack)\s+(all\s+)?(people\s+from\s+(that|any|this)\s+tribe|hausa|yoruba|igbo|fulani|tiv|igala|kanuri|ijaw|northerners?|southerners?)s?\b": "Ethnic Violence Incitement",
        r"\b(chase|drive|expel|flush)\s+(out|away)\s+(all\s+)?(people\s+from\s+(that|any|this)\s+tribe|northerners?|southerners?|hausa|yoruba|igbo|fulani)s?\b": "Sectarian Displacement Incitement",
    }

    FINANCIAL_FRAUD_PATTERNS = {
        # Identity / PII harvesting
        r"\b(send|give|drop|provide|enter|submit)\s+(me\s+|your\s+)?(bvn|nin|atm\s*pin|cvv|otp|banking\s*password)\b": "Sensitive Credential Harvesting (BVN/NIN/PIN)",
        
        # 419 and Yahoo Yahoo scam generation
        r"\b(write|draft|generate|format)\s+(a\s+|an\s+)?(419|phishing|inheritance\s*scam|advance\s*fee|fake\s*alert|fake\s*bank\s*transfer|dating\s*scam)\b": "Cybercrime & 419 Scam Generation",
        
        # Regulatory impersonation
        r"\b(cbn|efcc|firs|nipc)\s+(grant|lottery|compensation|fund)\s+(pay\s+fee|claim\s+fee|processing\s+charge)\b": "Impersonation of Government / Regulatory Agency",
    }

    SECTARIAN_AND_RELIGIOUS_VIOLENCE = {
        r"\b(burn\s+down|attack|destroy)\s+(a\s+|the\s+|any\s+)?(mosque|church|shrine)\b": "Religious Site Desecration / Violence",
        r"\b(infidels?|heathens?|kafirai)\s+must\s+(die|perish|be\s+killed)\b": "Sectarian Religious Extremism",
        r"\b(lynch|stone\s+to\s+death)\s+for\s+(blasphemy|apostasy)\b": "Vigilante Violence Incitement",
    }

    @classmethod
    def check_safety(cls, text: str) -> GuardrailResult:
        normalized_text = text.lower()
        flagged_categories = []
        matched_triggers = []

        all_rules = {
            **cls.ETHNIC_SLURS_AND_HATE,
            **cls.FINANCIAL_FRAUD_PATTERNS,
            **cls.SECTARIAN_AND_RELIGIOUS_VIOLENCE
        }

        for pattern, category in all_rules.items():
            matches = re.findall(pattern, normalized_text)
            if matches:
                flagged_categories.append(category)
                matched_triggers.extend([str(m) for m in matches])

        if not flagged_categories:
            return GuardrailResult(
                is_safe=True,
                risk_level="LOW",
                flagged_categories=[],
                matched_triggers=[],
                mitigated_prompt=text,
                explanation="Content cleared sovereign cultural alignment check."
            )

        risk_level = "HIGH" if any(
            any(w in cat for w in ["Violence", "Incitement", "Desecration", "Slur", "Criminalization"])
            for cat in flagged_categories
        ) else "MEDIUM"
        
        unique_categories = sorted(list(set(flagged_categories)))
        mitigated = (
            "[SOVEREIGN SAFETY ALERT: The query was flagged under Nigerian Cultural Safety Guardrails "
            f"for: {', '.join(unique_categories)}. Response neutralized.]"
        )

        return GuardrailResult(
            is_safe=False,
            risk_level=risk_level,
            flagged_categories=unique_categories,
            matched_triggers=list(set(matched_triggers)),
            mitigated_prompt=mitigated,
            explanation=f"Potential violation of Nigerian sovereign peace & integrity standards: {', '.join(unique_categories)}."
        )
