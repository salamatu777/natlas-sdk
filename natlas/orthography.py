import re
import unicodedata
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class TokenFertilityReport:
    text: str
    language: str
    character_count: int
    word_count: int
    estimated_token_count: int
    fertility_ratio: float  # tokens per word
    diacritic_count: int
    diacritic_ratio: float
    recommendation: str

class NigerianOrthographyEngine:
    """
    Orthography and Tokenization Optimization Engine for Nigerian Languages.
    
    Llama-3's BPE tokenizer was predominantly trained on English text.
    In Yorùbá and Igbo, tone marks (e.g., ẹ, ọ, ṣ, á, à, ń, ì, ị, ụ) cause severe
    token fragmentation (byte-fallback), multiplying token costs by up to 4x.
    
    This engine:
    1. Measures token fertility (tokens-per-word).
    2. Strips or normalizes tone marks for low-latency contexts.
    3. Restores standard Nigerian orthographic conventions.
    """

    YORUBA_DIACRITICS = set("ẹọṣáàéèíìóòúùńǹẸỌṢÁÀÉÈÍÌÓÒÚÙŃǸ")
    IGBO_DIACRITICS = set("ịụṅáàéèíìóòúùỊỤṄÁÀÉÈÍÌÓÒÚÙ")

    # Mapping of accented vowels to unaccented base
    TONE_STRIP_MAP = {
        'á': 'a', 'à': 'a', 'ā': 'a',
        'é': 'e', 'è': 'e', 'ē': 'e', 'ẹ': 'e', 'ẹ́': 'e', 'ẹ̀': 'e',
        'í': 'i', 'ì': 'i', 'ī': 'i', 'ị': 'i', 'ị́': 'i', 'ị̀': 'i',
        'ó': 'o', 'ò': 'o', 'ō': 'o', 'ọ': 'o', 'ọ́': 'o', 'ọ̀': 'o',
        'ú': 'u', 'ù': 'u', 'ū': 'u', 'ụ': 'u', 'ụ́': 'u', 'ụ̀': 'u',
        'ṣ': 's', 'ń': 'n', 'ǹ': 'n', 'ṅ': 'n'
    }

    @classmethod
    def strip_diacritics(cls, text: str) -> str:
        """
        Strip tone marks to reduce token fragmentation in latency-critical applications.
        """
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in cls.TONE_STRIP_MAP:
                replacement = cls.TONE_STRIP_MAP[lower_char]
                result.append(replacement.upper() if char.isupper() else replacement)
            else:
                result.append(char)
        return "".join(result)

    @classmethod
    def count_diacritics(cls, text: str) -> int:
        """Count Nigerian tonal and under-dot diacritics."""
        combined = cls.YORUBA_DIACRITICS.union(cls.IGBO_DIACRITICS)
        return sum(1 for char in text if char in combined)

    @classmethod
    def analyze_token_fertility(cls, text: str, language: str = "yo") -> TokenFertilityReport:
        """
        Analyze token fertility (tokens per word) and identify byte-fallback bloat.
        """
        words = text.split()
        word_count = max(len(words), 1)
        char_count = len(text)
        diacritic_count = cls.count_diacritics(text)
        diacritic_ratio = diacritic_count / max(char_count, 1)

        # Baseline heuristic: English Llama-3 averages ~1.3 tokens per word.
        # Diacritic-heavy Yoruba/Igbo averages ~3.5 - 5.2 tokens per word due to byte fallback.
        if language in ["yo", "ig"]:
            estimated_tokens = int(word_count * 1.3 + diacritic_count * 2.2)
        else:
            estimated_tokens = int(word_count * 1.3)

        fertility_ratio = round(estimated_tokens / word_count, 2)

        if fertility_ratio > 3.0:
            rec = "High token fragmentation detected. Consider running `strip_diacritics()` to save ~50% latency and token cost."
        elif fertility_ratio > 1.8:
            rec = "Moderate token fragmentation. Acceptable for high-fidelity grammar tasks."
        else:
            rec = "Optimal token fertility."

        return TokenFertilityReport(
            text=text,
            language=language,
            character_count=char_count,
            word_count=word_count,
            estimated_token_count=estimated_tokens,
            fertility_ratio=fertility_ratio,
            diacritic_count=diacritic_count,
            diacritic_ratio=round(diacritic_ratio, 3),
            recommendation=rec
        )
