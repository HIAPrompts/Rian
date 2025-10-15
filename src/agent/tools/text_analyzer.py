import re
from typing import List

class TextAnalyzer:
    @staticmethod
    def avg_sentence_length(text: str) -> float:
        """Calcula a média de palavras por frase."""
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
        word_counts = [len(s.split()) for s in sentences]
        return sum(word_counts) / len(word_counts) if word_counts else 0

    @staticmethod
    def has_sensory_detail(text: str) -> bool:
        """Verifica se há detalhes sensoriais (visão, som, cheiro, etc.)."""
        sensory_keywords = [
            "cheiro", "aroma", "som", "barulho", "toque", "textura",
            "sabor", "gosto", "visão", "cor", "luz", "brilho"
        ]
        return any(keyword in text.lower() for keyword in sensory_keywords)

    @staticmethod
    def has_mini_anecdote(text: str) -> bool:
        """Verifica se há uma mini-anedota ou exemplo concreto."""
        anecdote_keywords = [
            "uma vez", "por exemplo", "imagine que", "como quando",
            "lembro que", "digamos que", "como se"
        ]
        return any(keyword in text.lower() for keyword in anecdote_keywords)

    @staticmethod
    def compare_style(text: str, few_shots: str) -> float:
        """Comparação simples de estilo (para melhorar: use embeddings)."""
        # Implementação simplificada: conta palavras-chave em comum
        few_shots_words = set(few_shots.lower().split())
        text_words = set(text.lower().split())
        common_words = few_shots_words.intersection(text_words)
        return len(common_words) / len(few_shots_words) if few_shots_words else 0
