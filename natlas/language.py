import re

LANGUAGE_MAP = {
    "ha": "Hausa",
    "yo": "Yoruba",
    "ig": "Igbo",
    "en": "Nigerian Accented English"
}

def detect_language(text: str) -> str:
    """
    A simple heuristic-based language detection.
    Real production systems might use fasttext or a dedicated language ID model.
    """
    text = text.lower()
    
    # Yoruba specific patterns (diacritics and subdots)
    if re.search(r'[ẹọṣàáèéìíòóùú]', text):
        return "yo"
        
    # Hausa specific patterns (hooked letters)
    if re.search(r'[ɓɗƙƴ]', text):
        return "ha"
        
    # Igbo specific patterns
    if re.search(r'[ịọụṅ]', text):
        return "ig"
        
    # Default to English
    return "en"

def get_language_name(code: str) -> str:
    return LANGUAGE_MAP.get(code, "Unknown")
