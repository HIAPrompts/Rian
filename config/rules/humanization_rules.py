import random
from textblob import TextBlob

def add_colloquial_errors(text):
    replacements = {
        "estou": "tô",
        "você": "vc",
        "para": "pra",
        "que": "q",
        "impressionante": random.choice(["doido", "inacreditável", "maluco", "absurdo"]),
        "realmente": "real",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def check_repetition(text):
    blob = TextBlob(text)
    repeated_phrases = []
    for phrase in blob.ngrams(n=3):
        if text.count(" ".join(phrase)) > 2:
            repeated_phrases.append(" ".join(phrase))
    if repeated_phrases:
        raise ValueError(f"Repetições detectadas: {repeated_phrases}. Reformule o texto.")
    return text

def validate_human_like(text):
    if "É impressionante" in text and text.count("É impressionante") > 1:
        raise ValueError("Evite repetir 'É impressionante'. Use sinônimos.")
    if not any(word in text for word in ["caramba", "doidera", "rsrs", "tá ligado"]):
        raise ValueError("Adicione gírias ou expressões coloquiais.")
    return True
