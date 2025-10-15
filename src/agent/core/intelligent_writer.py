import yaml
import json
import random
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import re
from datetime import datetime

class IntelligentWriter:
    """
    Agente de escrita inteligente que usa algoritmos de decisão em vez de templates fixos.
    Analisa o contexto e toma decisões criativas baseadas no tópico e situação.
    """

    def __init__(self, config_path: str = "config"):
        """Initialize the IntelligentWriter with configuration files."""
        self.config_path = Path(config_path)
        self.writing_rules = self._load_yaml("rules/writing_rules.yaml")
        self.prompt_template = self._load_yaml("prompts/writing_prompt_complete.yaml")
        self.few_shots = self._load_json("style_fewshots/cliente1.json")
        self.hard_gates = self._load_json("rules/hard_gates.json")
        
        # Carregar perfil do Ryan Santos
        self.ryan_profile = self._load_yaml("../../src/agent/identity/ryan_santos_profile.yaml")
        
        # Cache frequently used rules
        self._cache_rules()
        
        # Sistema de personalidade e memória
        self.personality_traits = self._initialize_personality()
        self.writing_memory = []
        self.adaptation_level = 0.5  # Nível de adaptação (0-1)

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        # Se for o perfil do Ryan, usar caminho absoluto
        if "ryan_santos_profile.yaml" in file_path:
            yaml_path = Path(__file__).parent.parent.parent / "agent" / "identity" / "ryan_santos_profile.yaml"
        else:
            yaml_path = self.config_path / file_path
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load a JSON configuration file."""
        json_path = self.config_path / file_path
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _cache_rules(self):
        """Cache frequently used rules for better performance."""
        self.max_words = self.writing_rules["linguistic_structure"]["sentence_length"]["max_words"]
        self.avg_words = self.writing_rules["linguistic_structure"]["sentence_length"]["avg_words"]
        self.formality_level = self.writing_rules["tone_adaptation"]["formality_level"]
        self.tone = self.writing_rules["tone"]
        self.banned_words = self.writing_rules["vocabulary_rules"]["banned_words"]
        self.power_words = self.writing_rules["vocabulary_rules"]["power_words"]
        self.colloquial_expressions = self.writing_rules["human_language"]["colloquial_expressions"]

    def _initialize_personality(self) -> Dict[str, Any]:
        """Initialize personality traits that influence writing decisions."""
        return {
            "curiosity_level": random.uniform(0.6, 0.9),
            "storytelling_preference": random.uniform(0.7, 1.0),
            "data_driven": random.uniform(0.5, 0.8),
            "emotional_expressiveness": random.uniform(0.6, 0.9),
            "humor_tendency": random.uniform(0.3, 0.7),
            "controversy_tolerance": random.uniform(0.4, 0.8),
            "personal_revelation": random.uniform(0.5, 0.9)
        }

    def humanize(self, topic: str, audience: str = "geral", context: Optional[Dict] = None) -> str:
        """
        Generate humanized text using intelligent decision-making algorithms.
        
        Args:
            topic (str): The topic to humanize.
            audience (str): Target audience for the text.
            context (Dict, optional): Additional context for decision-making.
            
        Returns:
            str: The humanized text.
        """
        # Análise contextual inteligente
        context_analysis = self._analyze_context(topic, context)
        context_analysis["audience"] = audience
        
        # Decisão de estratégia narrativa
        narrative_strategy = self._choose_narrative_strategy(context_analysis)
        
        # Geração de abertura inteligente
        opening = self._generate_intelligent_opening(topic, context_analysis, narrative_strategy)
        
        # Geração de conteúdo principal
        main_content = self._generate_intelligent_content(topic, context_analysis, narrative_strategy)
        
        # Geração de conclusão inteligente
        conclusion = self._generate_intelligent_conclusion(topic, context_analysis, narrative_strategy)
        
        # Combinação inteligente
        humanized_text = self._combine_intelligently(opening, main_content, conclusion, context_analysis)
        
        # Aplicação de regras de humanização
        humanized_text = self._apply_intelligent_humanization(humanized_text, context_analysis)
        
        # Atualização da memória e personalidade
        self._update_memory_and_personality(topic, humanized_text, context_analysis)
        
        return humanized_text


    def _analyze_context(self, topic: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze the topic and context to make intelligent decisions."""
        analysis = {
            "topic": topic,
            "topic_type": self._classify_topic_type(topic),
            "emotional_tone": self._determine_emotional_tone(topic),
            "complexity_level": self._assess_complexity(topic),
            "audience_interest": self._assess_audience_interest(topic),
            "personal_connection": self._assess_personal_connection(topic),
            "storytelling_potential": self._assess_storytelling_potential(topic),
            "data_availability": self._assess_data_availability(topic),
            "controversy_level": self._assess_controversy_level(topic),
            "time_context": datetime.now().strftime("%H:%M"),
            "mood": self._determine_current_mood()
        }
        
        if context:
            analysis.update(context)
            
        return analysis

    def _classify_topic_type(self, topic: str) -> str:
        """Classify the topic type to inform writing decisions."""
        topic_lower = topic.lower()
        
        # Classificação inteligente baseada em palavras-chave
        if any(word in topic_lower for word in ["tecnologia", "ia", "inteligência", "artificial", "digital", "software"]):
            return "technology"
        elif any(word in topic_lower for word in ["dinheiro", "investimento", "finanças", "economia", "negócio"]):
            return "finance"
        elif any(word in topic_lower for word in ["cidade", "país", "lugar", "rio", "são paulo", "brasil"]):
            return "geography"
        elif any(word in topic_lower for word in ["pessoa", "vida", "relacionamento", "família", "amor"]):
            return "lifestyle"
        elif any(word in topic_lower for word in ["política", "governo", "lei", "direito", "justiça"]):
            return "politics"
        elif any(word in topic_lower for word in ["saúde", "médico", "hospital", "doença", "tratamento"]):
            return "health"
        else:
            return "general"

    def _determine_emotional_tone(self, topic: str) -> str:
        """Determine the appropriate emotional tone for the topic."""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["crise", "problema", "difícil", "desafio"]):
            return "serious_concerned"
        elif any(word in topic_lower for word in ["sucesso", "vitória", "conquista", "feliz"]):
            return "enthusiastic_positive"
        elif any(word in topic_lower for word in ["novo", "inovação", "descoberta", "revolução"]):
            return "curious_excited"
        elif any(word in topic_lower for word in ["pessoal", "minha", "experiência", "lembro"]):
            return "personal_reflective"
        else:
            return "neutral_analytical"

    def _assess_complexity(self, topic: str) -> float:
        """Assess the complexity level of the topic (0-1)."""
        topic_lower = topic.lower()
        
        # Palavras que indicam alta complexidade
        complex_indicators = ["sistema", "algoritmo", "metodologia", "estratégia", "análise", "pesquisa"]
        simple_indicators = ["simples", "básico", "fácil", "rápido", "direto"]
        
        complex_score = sum(1 for word in complex_indicators if word in topic_lower)
        simple_score = sum(1 for word in simple_indicators if word in topic_lower)
        
        if complex_score + simple_score == 0:
            return 0.5  # Neutral complexity
        
        return min(1.0, complex_score / (complex_score + simple_score))

    def _assess_audience_interest(self, topic: str) -> float:
        """Assess how interesting the topic is to the audience (0-1)."""
        topic_lower = topic.lower()
        
        # Tópicos que geram alto interesse
        high_interest = ["dinheiro", "sucesso", "relacionamento", "saúde", "tecnologia", "política"]
        low_interest = ["burocracia", "regulamento", "procedimento", "documento"]
        
        high_score = sum(1 for word in high_interest if word in topic_lower)
        low_score = sum(1 for word in low_interest if word in topic_lower)
        
        if high_score + low_score == 0:
            return 0.6  # Default moderate interest
        
        return min(1.0, high_score / (high_score + low_score + 1))

    def _assess_personal_connection(self, topic: str) -> float:
        """Assess how personally connected the writer feels to the topic (0-1)."""
        topic_lower = topic.lower()
        
        # Tópicos com alta conexão pessoal
        personal_topics = ["brasil", "rio de janeiro", "barcelona", "califórnia", "família", "experiência"]
        
        personal_score = sum(1 for word in personal_topics if word in topic_lower)
        
        # Baseado na personalidade do agente
        base_connection = self.personality_traits["personal_revelation"]
        
        return min(1.0, base_connection + (personal_score * 0.2))

    def _assess_storytelling_potential(self, topic: str) -> float:
        """Assess the storytelling potential of the topic (0-1)."""
        topic_lower = topic.lower()
        
        # Tópicos com alto potencial narrativo
        story_indicators = ["história", "experiência", "viagem", "pessoa", "momento", "época", "vez"]
        
        story_score = sum(1 for word in story_indicators if word in topic_lower)
        
        # Baseado na personalidade
        base_storytelling = self.personality_traits["storytelling_preference"]
        
        return min(1.0, base_storytelling + (story_score * 0.1))

    def _assess_data_availability(self, topic: str) -> float:
        """Assess how much data/statistics are available for the topic (0-1)."""
        topic_lower = topic.lower()
        
        # Tópicos que geralmente têm dados disponíveis
        data_rich = ["economia", "tecnologia", "saúde", "educação", "pesquisa", "estatística"]
        
        data_score = sum(1 for word in data_rich if word in topic_lower)
        
        # Baseado na personalidade
        base_data = self.personality_traits["data_driven"]
        
        return min(1.0, base_data + (data_score * 0.15))

    def _assess_controversy_level(self, topic: str) -> float:
        """Assess the controversy level of the topic (0-1)."""
        topic_lower = topic.lower()
        
        # Tópicos controversos
        controversial = ["política", "religião", "dinheiro", "relacionamento", "saúde", "justiça"]
        
        controversy_score = sum(1 for word in controversial if word in topic_lower)
        
        # Baseado na personalidade
        base_controversy = self.personality_traits["controversy_tolerance"]
        
        return min(1.0, base_controversy + (controversy_score * 0.1))

    def _determine_current_mood(self) -> str:
        """Determine the current mood based on personality and recent interactions."""
        # Simula variação de humor baseada na personalidade
        mood_factors = [
            "energetic" if self.personality_traits["emotional_expressiveness"] > 0.7 else "calm",
            "curious" if self.personality_traits["curiosity_level"] > 0.7 else "focused",
            "playful" if self.personality_traits["humor_tendency"] > 0.6 else "serious"
        ]
        
        return random.choice(mood_factors)

    def _choose_narrative_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Choose the best narrative strategy based on context analysis."""
        strategy = {
            "opening_type": self._choose_opening_type(context),
            "content_approach": self._choose_content_approach(context),
            "storytelling_style": self._choose_storytelling_style(context),
            "data_integration": self._choose_data_integration(context),
            "personal_revelation": self._choose_personal_revelation(context),
            "conclusion_style": self._choose_conclusion_style(context)
        }
        
        return strategy

    def _choose_opening_type(self, context: Dict[str, Any]) -> str:
        """Choose the best opening type based on context."""
        topic_type = context["topic_type"]
        emotional_tone = context["emotional_tone"]
        personal_connection = context["personal_connection"]
        
        if personal_connection > 0.7:
            return "personal_story"
        elif topic_type == "technology" and context["complexity_level"] > 0.6:
            return "data_driven"
        elif emotional_tone in ["enthusiastic_positive", "curious_excited"]:
            return "enthusiastic_announcement"
        elif context["controversy_level"] > 0.6:
            return "thoughtful_analysis"
        else:
            return "conversational_hook"

    def _choose_content_approach(self, context: Dict[str, Any]) -> str:
        """Choose the main content approach."""
        if context["data_availability"] > 0.7 and context["topic_type"] == "finance":
            return "data_analysis"
        elif context["storytelling_potential"] > 0.7:
            return "narrative_driven"
        elif context["personal_connection"] > 0.6:
            return "personal_experience"
        elif context["complexity_level"] > 0.6:
            return "educational_explanation"
        else:
            return "balanced_discussion"

    def _choose_storytelling_style(self, context: Dict[str, Any]) -> str:
        """Choose storytelling style."""
        if context["personal_connection"] > 0.8:
            return "intimate_personal"
        elif context["topic_type"] == "geography":
            return "travel_narrative"
        elif context["emotional_tone"] == "personal_reflective":
            return "reflective_analytical"
        else:
            return "conversational_story"

    def _choose_data_integration(self, context: Dict[str, Any]) -> str:
        """Choose how to integrate data."""
        if context["data_availability"] > 0.8:
            return "detailed_statistics"
        elif context["data_availability"] > 0.5:
            return "selective_data"
        else:
            return "minimal_data"

    def _choose_personal_revelation(self, context: Dict[str, Any]) -> str:
        """Choose level of personal revelation."""
        if context["personal_connection"] > 0.8:
            return "high_revelation"
        elif context["personal_connection"] > 0.5:
            return "moderate_revelation"
        else:
            return "minimal_revelation"

    def _choose_conclusion_style(self, context: Dict[str, Any]) -> str:
        """Choose conclusion style."""
        if context["audience_interest"] > 0.7:
            return "call_to_action"
        elif context["controversy_level"] > 0.6:
            return "thoughtful_summary"
        elif context["personal_connection"] > 0.6:
            return "personal_reflection"
        else:
            return "conversational_close"

    def _generate_intelligent_opening(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate opening using intelligent decision-making with contextual variety."""
        # Obter o tipo de tópico para seleção contextual
        topic_type = context.get("topic_type", "default")
        
        # Mapear tipos de tópico para categorias de abertura
        opening_category = self._map_topic_to_opening_category(topic_type)
        
        # Obter blocos de abertura do prompt template
        opening_blocks = self.prompt_template.get("contextual_openings", {})
        category_openings = opening_blocks.get(opening_category, opening_blocks.get("default", []))
        
        if category_openings:
            # Selecionar uma abertura aleatória da categoria apropriada
            selected_opening = random.choice(category_openings)
            return selected_opening.format(topic=topic)
        else:
            # Fallback para abertura tradicional
            base_greeting = "Salve rapaziada, aqui é o Ryan Santos"
            location = self._select_intelligent_location(context)
            action = self._select_intelligent_action(topic, context, strategy)
            return f"{base_greeting}, direto {location} e hoje eu quero {action} sobre {topic}. Cara, presta atenção que isso é importante..."
    
    def _map_topic_to_opening_category(self, topic_type: str) -> str:
        """Map topic type to opening category."""
        mapping = {
            "technology": "technology",
            "finance": "finance", 
            "geography": "geography",
            "lifestyle": "lifestyle",
            "entertainment": "entertainment"
        }
        return mapping.get(topic_type, "default")

    def _select_intelligent_location(self, context: Dict[str, Any]) -> str:
        """Select location based on context and personality."""
        locations = [
            "do meu apartamento em Barcelona",
            "da praia de Barceloneta",
            "do meu cafofinho na Califórnia",
            "das ruas de Los Angeles",
            "direto aqui de Barcelona"
        ]
        
        # Escolha baseada no contexto
        if context["topic_type"] == "geography" and "rio" in context["topic"].lower():
            return "da praia de Barceloneta"  # Contraste interessante
        elif context["mood"] == "energetic":
            return "das ruas de Los Angeles"
        elif context["personal_connection"] > 0.7:
            return "do meu apartamento em Barcelona"
        else:
            return random.choice(locations)

    def _select_intelligent_action(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Select action based on context and strategy."""
        actions = [
            "falar", "conversar", "compartilhar", "explicar", "debater", 
            "analisar", "discutir", "reagir", "opinar", "trazer uma reflexão interessante"
        ]
        
        # Escolha baseada na estratégia
        if strategy["content_approach"] == "data_analysis":
            return "compartilhar alguns dados interessantes"
        elif strategy["content_approach"] == "personal_experience":
            return "compartilhar uma experiência pessoal"
        elif context["controversy_level"] > 0.6:
            return "trazer uma reflexão interessante"
        else:
            return random.choice(actions)

    def _generate_intelligent_content(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate main content using intelligent decision-making."""
        content_parts = []
        
        # Personal story (if strategy calls for it)
        if strategy["personal_revelation"] != "minimal_revelation":
            story = self._generate_personal_story(topic, context, strategy)
            if story:
                content_parts.append(story)
        
        # Data integration (if strategy calls for it)
        if strategy["data_integration"] != "minimal_data":
            data_content = self._generate_data_content(topic, context, strategy)
            if data_content:
                content_parts.append(data_content)
        
        # Personal opinion (based on personality and context)
        if self.personality_traits["emotional_expressiveness"] > 0.6:
            opinion = self._generate_personal_opinion(topic, context, strategy)
            if opinion:
                content_parts.append(opinion)
        
        return "\n\n".join(content_parts)

    def _generate_personal_story(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate personal story based on context and strategy."""
        if strategy["personal_revelation"] == "minimal_revelation":
            return ""
        
        # Story templates based on context
        if context["topic_type"] == "geography":
            return f"Eu quando tinha {random.randint(18, 35)} anos, eu {random.choice(['mudei', 'viajei', 'morei'])} {random.choice(['para', 'em'])} {topic}. E nessa época era tipo, putz, não tem como explicar hoje."
        
        elif context["topic_type"] == "technology":
            return f"Esses dias, cara, eu {random.choice(['descobri', 'testei', 'usei'])} {topic} e putz, não tem como explicar a diferença que fez na minha vida."
        
        elif context["topic_type"] == "finance":
            return f"Uma vez eu {random.choice(['investi', 'gastei', 'economizei'])} dinheiro em {topic} e cara, a lição que aprendi foi {random.choice(['valiosa', 'difícil', 'importante'])}."
        
        else:
            return f"Eu lembro que quando eu {random.choice(['era mais novo', 'tinha 20 anos', 'comecei'])} e {topic} era tipo, {random.choice(['não existia', 'era diferente', 'era complicado'])}."

    def _generate_data_content(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate data-driven content based on context using contextual blocks."""
        if strategy["data_integration"] == "minimal_data":
            return ""
        
        # Obter o tipo de tópico para seleção contextual
        topic_type = context.get("topic_type", "default")
        
        # Mapear tipos de tópico para categorias de interação
        interaction_category = self._map_topic_to_interaction_category(topic_type)
        
        # Obter blocos de interação do prompt template
        audience_blocks = self.prompt_template.get("audience_interaction", {})
        category_blocks = audience_blocks.get(interaction_category, audience_blocks.get("default", []))
        
        if category_blocks:
            # Selecionar um bloco aleatório da categoria apropriada
            selected_block = random.choice(category_blocks)
            return selected_block.format(topic=topic)
        else:
            # Fallback para dados específicos por tipo
            if context["topic_type"] == "finance":
                return f"E olha que impressionante. Então, a gente começa esse gráfico com {random.randint(100, 500)} e a gente termina esse gráfico com {random.randint(1000, 5000)}. Se você olhar esses números e analisar, você vai perceber que {topic} está crescendo exponencialmente."
            elif context["topic_type"] == "technology":
                return f"De acordo com dados da {random.choice(['Microsoft', 'Google', 'IBM'])}, a {topic} e eles cruzam, eles têm conhecimento e dizer assim: 'Opa, o nosso sistema já substituiu esse trabalho'."
            else:
                return f"Rapaziada, eu separei uma categoria aqui sobre {topic}."
    
    def _map_topic_to_interaction_category(self, topic_type: str) -> str:
        """Map topic type to interaction category."""
        mapping = {
            "technology": "technology",
            "finance": "finance", 
            "geography": "geography",
            "lifestyle": "lifestyle",
            "entertainment": "entertainment"
        }
        return mapping.get(topic_type, "default")

    def _generate_personal_opinion(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate personal opinion based on context and personality."""
        if self.personality_traits["emotional_expressiveness"] < 0.5:
            return ""
        
        opinions = [
            f"Cara, eu sou suspeito em falar, eu fiz muito isso, muito. Meu patrimônio hoje em dia poderia ter sido muito maior do que ele é se eu não tivesse {random.choice(['essa necessidade de ostentar', 'medo de arriscar', 'preguiça de estudar'])}.",
            f"E me fez tipo ter o clique, cara. Basicamente, {topic} é uma ferramenta poderosa que pode transformar sua vida.",
            f"Olha só, vamos lá. {topic} não é só uma {random.choice(['tendência', 'moda', 'coisa passageira'])}, é uma {random.choice(['revolução', 'mudança', 'transformação'])} que está acontecendo agora."
        ]
        
        return random.choice(opinions)

    def _generate_intelligent_conclusion(self, topic: str, context: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """Generate conclusion using intelligent decision-making."""
        conclusion_style = strategy["conclusion_style"]
        
        if conclusion_style == "call_to_action":
            return f"E aí, o que você acha sobre {topic}? Deixa aí nos comentários. E eu faço questão de ler os comentários porque o público aqui é extremamente qualificado."
        
        elif conclusion_style == "thoughtful_summary":
            return f"Basicamente, {topic} é {random.choice(['complexo', 'interessante', 'importante'])}, mas entendeu? A chave é {random.choice(['entender', 'estudar', 'praticar'])} e não ter medo de {random.choice(['tentar', 'errar', 'aprender'])}."
        
        elif conclusion_style == "personal_reflection":
            return f"Cara, o que aprendemos sobre {topic} é que {random.choice(['nada é impossível', 'tudo é possível', 'a vida é uma jornada'])}. Beleza? Então, vamos continuar explorando esse assunto juntos."
        
        else:  # conversational_close
            return f"Então é isso. Valeu, tamo junto. Direto de {random.choice(['Barcelona', 'Los Angeles', 'Califórnia'])}."

    def _combine_intelligently(self, opening: str, main_content: str, conclusion: str, context: Dict[str, Any]) -> str:
        """Combine all parts intelligently based on context."""
        parts = [opening]
        
        if main_content:
            parts.append(main_content)
        
        parts.append(conclusion)
        
        return "\n\n".join(parts)

    def _apply_intelligent_humanization(self, text: str, context: Dict[str, Any]) -> str:
        """Apply humanization rules intelligently based on context."""
        # Apply colloquial expressions based on personality
        if self.personality_traits["emotional_expressiveness"] > 0.7:
            text = self._add_colloquial_expressions(text, context)
        
        # Apply transitions based on complexity
        if context["complexity_level"] > 0.5:
            text = self._add_intelligent_transitions(text, context)
        
        # Apply rhetorical questions based on audience interest
        if context["audience_interest"] > 0.6:
            text = self._add_rhetorical_questions(text, context)
        
        return text

    def _add_colloquial_expressions(self, text: str, context: Dict[str, Any]) -> str:
        """Add colloquial expressions intelligently."""
        if random.random() < 0.3:
            text = text.replace("você", "cara, você", 1)
        
        if random.random() < 0.2:
            text += " Entendeu?"
        
        if random.random() < 0.15:
            text += " Beleza?"
        
        return text

    def _add_intelligent_transitions(self, text: str, context: Dict[str, Any]) -> str:
        """Add transitions intelligently based on context."""
        transitions = ["Então", "E aí", "Tipo", "Basicamente"]
        
        if random.random() < 0.4:
            transition = random.choice(transitions)
            text = f"{transition} {text}"
        
        return text

    def _add_rhetorical_questions(self, text: str, context: Dict[str, Any]) -> str:
        """Add rhetorical questions intelligently."""
        questions = ["Beleza?", "Entendeu?", "Tá ligado?"]
        
        if random.random() < 0.3:
            question = random.choice(questions)
            text += f" {question}"
        
        return text

    def _update_memory_and_personality(self, topic: str, text: str, context: Dict[str, Any]):
        """Update memory and adapt personality based on experience."""
        # Store in memory
        self.writing_memory.append({
            "topic": topic,
            "context": context,
            "text_length": len(text.split()),
            "timestamp": datetime.now()
        })
        
        # Adapt personality based on success
        if len(text.split()) > 50:  # Successful generation
            self.adaptation_level = min(1.0, self.adaptation_level + 0.01)
        
        # Keep only recent memory
        if len(self.writing_memory) > 10:
            self.writing_memory = self.writing_memory[-10:]

    def validate_text(self, text: str) -> bool:
        """Validate text using the same logic as before."""
        # Use the same validation logic from the original class
        text_lower = text.lower()
        
        # Check banned words
        for banned_word in self.banned_words:
            if banned_word in text_lower:
                return False
        
        # Check sentence length
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        for sentence in sentences:
            if len(sentence.split()) > self.max_words:
                return False
        
        return True

    def get_writing_metrics(self, text: str) -> Dict[str, Any]:
        """Get detailed metrics about the text."""
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        return {
            "total_words": len(words),
            "total_sentences": len(sentences),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "personality_traits": self.personality_traits,
            "adaptation_level": self.adaptation_level,
            "memory_size": len(self.writing_memory)
        }
