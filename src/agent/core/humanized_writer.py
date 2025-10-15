import random
from textblob import TextBlob

class HumanizedWriter:
    def __init__(self):
        pass

    def humanize(self, topic, client_id="default", tamanho_desejado=3000):
        # 1. Gera o texto com o prompt aprimorado
        raw_text = self._generate_text(topic, client_id, tamanho_desejado)

        # 2. Aplica imperfeições humanas
        humanized_text = self._add_colloquial_errors(raw_text)

        # 3. Valida repetições e tom humano
        self._check_repetition(humanized_text)
        self._validate_human_like(humanized_text)

        return humanized_text

    def _add_colloquial_errors(self, text):
        # Adiciona erros intencionais e gírias
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

    def _check_repetition(self, text):
        # Verifica repetições de palavras ou frases
        blob = TextBlob(text)
        repeated_phrases = []
        for phrase in blob.ngrams(n=3):
            if text.count(" ".join(phrase)) > 2:
                repeated_phrases.append(" ".join(phrase))
        if repeated_phrases:
            raise ValueError(f"Repetições detectadas: {repeated_phrases}. Reformule o texto.")
        return text

    def _validate_human_like(self, text):
        # Valida se o texto parece humano
        if "É impressionante" in text and text.count("É impressionante") > 1:
            raise ValueError("Evite repetir 'É impressionante'. Use sinônimos.")
        if not any(word in text for word in ["caramba", "doidera", "rsrs", "tá ligado"]):
            raise ValueError("Adicione gírias ou expressões coloquiais.")
        return True

    def _generate_text(self, topic, client_id, tamanho_desejado):
        # Simulação: substitua pela lógica real de geração de texto
        return f"Texto gerado sobre {topic} com {tamanho_desejado} caracteres."