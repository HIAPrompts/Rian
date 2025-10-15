import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
import re

class AutomatedReviewer:
    """
    Automated reviewer that validates humanized text against comprehensive rules.
    Now enhanced with detailed validation based on analysis of 33 real texts.
    """

    def __init__(self, config_path: str = "config"):
        """
        Initialize the AutomatedReviewer with configuration files.

        Args:
            config_path (str): Path to the directory containing configuration files.
        """
        self.config_path = Path(config_path)
        self.writing_rules = self._load_yaml("rules/writing_rules.yaml")
        self.hard_gates = self._load_json("rules/hard_gates.json")
        
        # Cache frequently used rules for performance
        self._cache_rules()

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
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
        # Linguistic structure rules
        self.max_words = self.writing_rules["linguistic_structure"]["sentence_length"]["max_words"]
        self.avg_words = self.writing_rules["linguistic_structure"]["sentence_length"]["avg_words"]
        self.min_words = self.writing_rules["linguistic_structure"]["sentence_length"]["min_words"]
        
        # Paragraph rules
        self.max_sentences_per_paragraph = self.writing_rules["linguistic_structure"]["paragraph_length"]["max_sentences"]
        
        # Vocabulary rules
        self.banned_words = self.writing_rules["vocabulary_rules"]["banned_words"]
        self.power_words = self.writing_rules["vocabulary_rules"]["power_words"]
        
        # Human language rules
        self.use_second_person = self.writing_rules["human_language"]["use_second_person"]
        self.use_contractions = self.writing_rules["human_language"]["use_contractions"]
        self.include_sensory_details = self.writing_rules["human_language"]["include_sensory_details"]
        self.include_rhetorical_questions = self.writing_rules["human_language"]["include_rhetorical_questions"]
        
        # Colloquial expressions
        self.colloquial_expressions = self.writing_rules["human_language"]["colloquial_expressions"]
        
        # Engagement rules
        self.rhetorical_question_frequency = self.writing_rules["engagement_rules"]["rhetorical_questions"]["frequency"]
        
        # Success metrics
        self.success_metrics = self.writing_rules["success_metrics"]

    def review(self, content: str) -> Dict[str, Any]:
        """
        Comprehensive review of the content against all writing rules.
        
        Args:
            content (str): The content to review.
            
        Returns:
            Dict[str, Any]: Detailed review results with scores and recommendations.
        """
        print("AutomatedReviewer: Revisando conteudo...")
        
        # Perform all validation checks
        validation_results = self._perform_comprehensive_validation(content)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(validation_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(validation_results)
        
        # Create detailed report
        review_report = {
            "overall_score": overall_score,
            "validation_results": validation_results,
            "recommendations": recommendations,
            "metrics": self._calculate_detailed_metrics(content),
            "passed_hard_gates": self._check_hard_gates(content),
            "humanization_level": self._calculate_humanization_level(content)
        }
        
        return review_report

    def _perform_comprehensive_validation(self, content: str) -> Dict[str, Any]:
        """Perform comprehensive validation against all rules."""
        results = {}
        
        # Linguistic structure validation
        results["sentence_length"] = self._validate_sentence_length(content)
        results["paragraph_structure"] = self._validate_paragraph_structure(content)
        results["punctuation"] = self._validate_punctuation(content)
        
        # Vocabulary validation
        results["banned_words"] = self._validate_banned_words(content)
        results["power_words"] = self._validate_power_words(content)
        results["jargon_usage"] = self._validate_jargon_usage(content)
        
        # Human language validation
        results["second_person_usage"] = self._validate_second_person(content)
        results["contractions"] = self._validate_contractions(content)
        results["sensory_details"] = self._validate_sensory_details(content)
        results["rhetorical_questions"] = self._validate_rhetorical_questions(content)
        
        # Engagement validation
        results["colloquial_expressions"] = self._validate_colloquial_expressions(content)
        results["transition_words"] = self._validate_transition_words(content)
        results["storytelling_elements"] = self._validate_storytelling_elements(content)
        
        # Tone and style validation
        results["tone_consistency"] = self._validate_tone_consistency(content)
        results["formality_level"] = self._validate_formality_level(content)
        
        return results

    def _validate_sentence_length(self, content: str) -> Dict[str, Any]:
        """Validate sentence length against rules."""
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        sentence_lengths = [len(s.split()) for s in sentences]
        
        violations = []
        for i, length in enumerate(sentence_lengths):
            if length > self.max_words:
                violations.append(f"Sentence {i+1}: {length} words (max: {self.max_words})")
            elif length < self.min_words:
                violations.append(f"Sentence {i+1}: {length} words (min: {self.min_words})")
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "average_length": avg_length,
            "max_length": max(sentence_lengths) if sentence_lengths else 0,
            "min_length": min(sentence_lengths) if sentence_lengths else 0,
            "score": max(0, 1 - (len(violations) / len(sentences))) if sentences else 0
        }

    def _validate_paragraph_structure(self, content: str) -> Dict[str, Any]:
        """Validate paragraph structure."""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        violations = []
        
        for i, paragraph in enumerate(paragraphs):
            sentences = [s.strip() for s in paragraph.split('.') if s.strip()]
            if len(sentences) > self.max_sentences_per_paragraph:
                violations.append(f"Paragraph {i+1}: {len(sentences)} sentences (max: {self.max_sentences_per_paragraph})")
        
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "score": max(0, 1 - (len(violations) / len(paragraphs))) if paragraphs else 0
        }

    def _validate_punctuation(self, content: str) -> Dict[str, Any]:
        """Validate punctuation usage."""
        exclamation_count = content.count('!')
        question_count = content.count('?')
        ellipsis_count = content.count('...')
        
        word_count = len(content.split())
        exclamation_ratio = exclamation_count / word_count if word_count > 0 else 0
        
        # Check if exclamation usage is appropriate (sparingly)
        exclamation_ok = exclamation_ratio <= 0.01  # Max 1% of words
        
        return {
            "passed": exclamation_ok,
            "exclamation_count": exclamation_count,
            "question_count": question_count,
            "ellipsis_count": ellipsis_count,
            "exclamation_ratio": exclamation_ratio,
            "score": 1.0 if exclamation_ok else 0.5
        }

    def _validate_banned_words(self, content: str) -> Dict[str, Any]:
        """Validate against banned words."""
        content_lower = content.lower()
        found_banned = [word for word in self.banned_words if word in content_lower]
        
        return {
            "passed": len(found_banned) == 0,
            "found_banned_words": found_banned,
            "score": 1.0 if len(found_banned) == 0 else 0.0
        }

    def _validate_power_words(self, content: str) -> Dict[str, Any]:
        """Validate power word usage."""
        content_lower = content.lower()
        found_power_words = [word for word in self.power_words if word in content_lower]
        
        # Expect at least one power word for engagement
        has_power_words = len(found_power_words) > 0
        
        return {
            "passed": has_power_words,
            "found_power_words": found_power_words,
            "count": len(found_power_words),
            "score": min(1.0, len(found_power_words) / 3)  # Normalize to 0-1
        }

    def _validate_jargon_usage(self, content: str) -> Dict[str, Any]:
        """Validate jargon usage (should be minimal)."""
        jargon_words = self.writing_rules["vocabulary_rules"]["avoid_jargon"]
        content_lower = content.lower()
        found_jargon = [word for word in jargon_words if word in content_lower]
        
        word_count = len(content.split())
        jargon_ratio = len(found_jargon) / word_count if word_count > 0 else 0
        
        # Low jargon usage is good
        jargon_ok = jargon_ratio <= 0.02  # Max 2% of words
        
        return {
            "passed": jargon_ok,
            "found_jargon": found_jargon,
            "jargon_ratio": jargon_ratio,
            "score": 1.0 if jargon_ok else max(0, 1 - jargon_ratio * 10)
        }

    def _validate_second_person(self, content: str) -> Dict[str, Any]:
        """Validate second person usage."""
        if not self.use_second_person:
            return {"passed": True, "score": 1.0}
        
        content_lower = content.lower()
        second_person_indicators = ["você", "cara", "vocês", "rapaziada"]
        found_indicators = [word for word in second_person_indicators if word in content_lower]
        
        has_second_person = len(found_indicators) > 0
        
        return {
            "passed": has_second_person,
            "found_indicators": found_indicators,
            "count": len(found_indicators),
            "score": 1.0 if has_second_person else 0.0
        }

    def _validate_contractions(self, content: str) -> Dict[str, Any]:
        """Validate contraction usage."""
        if not self.use_contractions:
            return {"passed": True, "score": 1.0}
        
        contractions = ["você tá", "não", "tá", "vou", "vamos", "está", "é"]
        content_lower = content.lower()
        found_contractions = [cont for cont in contractions if cont in content_lower]
        
        has_contractions = len(found_contractions) > 0
        
        return {
            "passed": has_contractions,
            "found_contractions": found_contractions,
            "count": len(found_contractions),
            "score": 1.0 if has_contractions else 0.0
        }

    def _validate_sensory_details(self, content: str) -> Dict[str, Any]:
        """Validate sensory details inclusion."""
        if not self.include_sensory_details:
            return {"passed": True, "score": 1.0}
        
        sensory_words = ["imagine", "sinta", "veja", "ouça", "cheiro", "sabor", "tato", "visual"]
        content_lower = content.lower()
        found_sensory = [word for word in sensory_words if word in content_lower]
        
        has_sensory = len(found_sensory) > 0
        
        return {
            "passed": has_sensory,
            "found_sensory_words": found_sensory,
            "count": len(found_sensory),
            "score": 1.0 if has_sensory else 0.0
        }

    def _validate_rhetorical_questions(self, content: str) -> Dict[str, Any]:
        """Validate rhetorical question usage."""
        if not self.include_rhetorical_questions:
            return {"passed": True, "score": 1.0}
        
        question_count = content.count('?')
        word_count = len(content.split())
        question_ratio = question_count / word_count if word_count > 0 else 0
        
        # Check if question frequency is appropriate
        expected_ratio = self.rhetorical_question_frequency
        ratio_ok = abs(question_ratio - expected_ratio) <= 0.05  # Within 5% tolerance
        
        return {
            "passed": ratio_ok,
            "question_count": question_count,
            "question_ratio": question_ratio,
            "expected_ratio": expected_ratio,
            "score": max(0, 1 - abs(question_ratio - expected_ratio) * 10)
        }

    def _validate_colloquial_expressions(self, content: str) -> Dict[str, Any]:
        """Validate colloquial expression usage."""
        content_lower = content.lower()
        
        # Check ultra-high frequency expressions
        ultra_high = self.colloquial_expressions["ultra_high"]
        found_ultra_high = [expr for expr in ultra_high if expr in content_lower]
        
        # Check high frequency expressions
        high = self.colloquial_expressions["high"]
        found_high = [expr for expr in high if expr in content_lower]
        
        total_found = len(found_ultra_high) + len(found_high)
        has_colloquial = total_found > 0
        
        return {
            "passed": has_colloquial,
            "found_ultra_high": found_ultra_high,
            "found_high": found_high,
            "total_count": total_found,
            "score": min(1.0, total_found / 5)  # Normalize to 0-1
        }

    def _validate_transition_words(self, content: str) -> Dict[str, Any]:
        """Validate transition word usage."""
        transition_words = self.writing_rules["text_flow"]["transition_words"]
        all_transitions = []
        for category in transition_words.values():
            all_transitions.extend(category)
        
        content_lower = content.lower()
        found_transitions = [word for word in all_transitions if word in content_lower]
        
        has_transitions = len(found_transitions) > 0
        
        return {
            "passed": has_transitions,
            "found_transitions": found_transitions,
            "count": len(found_transitions),
            "score": 1.0 if has_transitions else 0.0
        }

    def _validate_storytelling_elements(self, content: str) -> Dict[str, Any]:
        """Validate storytelling elements."""
        storytelling_patterns = [
            "eu quando", "uma vez", "essas dias", "lembro que", 
            "nessa época", "era tipo", "imagine", "cara, eu"
        ]
        
        content_lower = content.lower()
        found_patterns = [pattern for pattern in storytelling_patterns if pattern in content_lower]
        
        has_storytelling = len(found_patterns) > 0
        
        return {
            "passed": has_storytelling,
            "found_patterns": found_patterns,
            "count": len(found_patterns),
            "score": 1.0 if has_storytelling else 0.0
        }

    def _validate_tone_consistency(self, content: str) -> Dict[str, Any]:
        """Validate tone consistency."""
        # Simple tone consistency check based on formality indicators
        formal_indicators = ["portanto", "consequentemente", "adicionalmente"]
        informal_indicators = ["cara", "beleza", "entendeu", "tipo", "putz"]
        
        content_lower = content.lower()
        formal_count = sum(1 for word in formal_indicators if word in content_lower)
        informal_count = sum(1 for word in informal_indicators if word in content_lower)
        
        # Check if tone is consistent (not mixing formal and informal heavily)
        total_indicators = formal_count + informal_count
        if total_indicators == 0:
            consistency_score = 1.0
        else:
            dominant_style = max(formal_count, informal_count)
            consistency_score = dominant_style / total_indicators
        
        return {
            "passed": consistency_score >= 0.7,  # At least 70% consistency
            "formal_count": formal_count,
            "informal_count": informal_count,
            "consistency_score": consistency_score,
            "score": consistency_score
        }

    def _validate_formality_level(self, content: str) -> Dict[str, Any]:
        """Validate formality level."""
        expected_formality = self.writing_rules["tone_adaptation"]["formality_level"]
        
        # Calculate actual formality level
        actual_formality = self._calculate_formality_score(content)
        
        # Convert to 1-10 scale
        actual_formality_scale = actual_formality * 10
        
        # Check if within acceptable range
        tolerance = 2
        formality_ok = abs(actual_formality_scale - expected_formality) <= tolerance
        
        return {
            "passed": formality_ok,
            "expected_formality": expected_formality,
            "actual_formality": actual_formality_scale,
            "difference": abs(actual_formality_scale - expected_formality),
            "score": max(0, 1 - abs(actual_formality_scale - expected_formality) / 10)
        }

    def _calculate_formality_score(self, content: str) -> float:
        """Calculate formality score (0-1 scale)."""
        formal_indicators = ["portanto", "consequentemente", "adicionalmente", "furthermore"]
        informal_indicators = ["cara", "beleza", "entendeu", "tipo", "putz"]
        
        content_lower = content.lower()
        formal_count = sum(1 for word in formal_indicators if word in content_lower)
        informal_count = sum(1 for word in informal_indicators if word in content_lower)
        
        total_words = len(content.split())
        if total_words == 0:
            return 0.5
        
        formality_score = (formal_count - informal_count) / total_words
        return max(0, min(1, formality_score + 0.5))

    def _calculate_overall_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall validation score."""
        scores = []
        for result in validation_results.values():
            if isinstance(result, dict) and "score" in result:
                scores.append(result["score"])
        
        return sum(scores) / len(scores) if scores else 0.0

    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        for check_name, result in validation_results.items():
            if isinstance(result, dict) and not result.get("passed", True):
                if check_name == "sentence_length" and result.get("violations"):
                    recommendations.append(f"Reduza o comprimento das frases: {', '.join(result['violations'][:3])}")
                elif check_name == "banned_words" and result.get("found_banned_words"):
                    recommendations.append(f"Remova palavras proibidas: {', '.join(result['found_banned_words'])}")
                elif check_name == "second_person_usage" and not result.get("passed"):
                    recommendations.append("Use mais segunda pessoa ('você', 'cara') para criar conexão")
                elif check_name == "sensory_details" and not result.get("passed"):
                    recommendations.append("Adicione detalhes sensoriais ('imagine', 'sinta', 'veja')")
                elif check_name == "colloquial_expressions" and not result.get("passed"):
                    recommendations.append("Use mais expressões coloquiais para humanizar o texto")
                elif check_name == "storytelling_elements" and not result.get("passed"):
                    recommendations.append("Inclua elementos de storytelling ('eu quando', 'uma vez', 'essas dias')")
        
        return recommendations

    def _calculate_detailed_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate detailed metrics about the content."""
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "avg_sentences_per_paragraph": len(sentences) / len(paragraphs) if paragraphs else 0,
            "readability_score": self._calculate_readability_score(content),
            "humanization_score": self._calculate_humanization_level(content)
        }

    def _calculate_readability_score(self, content: str) -> float:
        """Calculate readability score."""
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if not sentences or not words:
            return 0
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Simple readability: shorter sentences = higher score
        if avg_words_per_sentence <= 10:
            return 1.0
        elif avg_words_per_sentence <= 15:
            return 0.8
        elif avg_words_per_sentence <= 20:
            return 0.6
        else:
            return 0.4

    def _calculate_humanization_level(self, content: str) -> float:
        """Calculate humanization level based on various factors."""
        content_lower = content.lower()
        
        # Factors that indicate humanization
        humanization_factors = {
            "second_person": content_lower.count("você") + content_lower.count("cara"),
            "colloquial": sum(1 for expr in self.colloquial_expressions["ultra_high"] if expr in content_lower),
            "questions": content.count('?'),
            "contractions": content_lower.count("tá") + content_lower.count("não"),
            "storytelling": sum(1 for pattern in ["eu quando", "uma vez", "essas dias"] if pattern in content_lower),
            "sensory": sum(1 for word in ["imagine", "sinta", "veja", "ouça"] if word in content_lower)
        }
        
        # Calculate score based on factors
        total_score = sum(humanization_factors.values())
        max_possible = len(humanization_factors) * 5  # Assume max 5 of each factor
        
        return min(1.0, total_score / max_possible) if max_possible > 0 else 0.0

    def _check_hard_gates(self, content: str) -> bool:
        """Check if content passes hard gates."""
        # Check banned words
        content_lower = content.lower()
        for banned_word in self.banned_words:
            if banned_word in content_lower:
                return False
        
        # Check sentence length
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        for sentence in sentences:
            if len(sentence.split()) > self.max_words:
                return False
        
        # Check required elements
        required_elements = self.hard_gates.get("required_elements", {})
        
        if required_elements.get("second_person", False):
            if "você" not in content_lower and "cara" not in content_lower:
                return False
        
        if required_elements.get("sensory_detail", False):
            sensory_words = ["imagine", "sinta", "veja", "ouça", "cheiro", "sabor"]
            if not any(word in content_lower for word in sensory_words):
                return False
        
        if required_elements.get("mini_anecdote", False):
            anecdote_indicators = ["eu quando", "uma vez", "essas dias", "lembro que"]
            if not any(phrase in content_lower for phrase in anecdote_indicators):
                return False
        
        return True