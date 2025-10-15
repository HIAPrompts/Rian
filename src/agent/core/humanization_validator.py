#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validador de Humanização - Sistema de Pontuação
Avalia texto baseado em características de IA vs. humano
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import Counter

class HumanizationValidator:
    """Validador de humanização baseado em pontuação de características"""
    
    def __init__(self, config_path: str = "config"):
        """Inicializar o validador com regras de pontuação"""
        self.config_path = Path(config_path)
        self.scoring_rules = self._load_yaml("rules/simple_scoring.yaml")
        
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Carregar arquivo YAML"""
        yaml_path = self.config_path / file_path
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analisar texto e retornar pontuação detalhada"""
        
        # Detectar características de IA
        ai_penalties = self._detect_ai_characteristics(text)
        
        # Detectar características humanas
        human_bonuses = self._detect_human_characteristics(text)
        
        # Calcular pontuação total
        total_score = self._calculate_total_score(ai_penalties, human_bonuses)
        
        # Gerar recomendações
        recommendations = self._generate_recommendations(ai_penalties, human_bonuses)
        
        return {
            "total_score": total_score,
            "ai_penalties": ai_penalties,
            "human_bonuses": human_bonuses,
            "ai_traits": ai_penalties,  # Alias para compatibilidade
            "human_traits": human_bonuses,  # Alias para compatibilidade
            "ai_penalty": sum([v for v in ai_penalties.values() if isinstance(v, (int, float))]),
            "human_score": sum([v for v in human_bonuses.values() if isinstance(v, (int, float))]),
            "level": self._get_level(total_score),
            "recommendations": recommendations,
            "analysis": self._get_analysis_summary(total_score),
            "score": total_score  # Adicionar chave 'score' para compatibilidade
        }
    
    def _detect_ai_characteristics(self, text: str) -> Dict[str, Any]:
        """Detectar características de IA no texto"""
        penalties = {}
        ai_rules = self.scoring_rules["ai_penalties"]
        
        for characteristic, rules in ai_rules.items():
            penalty = 0
            occurrences = 0
            
            # Detectar padrões específicos
            for pattern in rules["detection_patterns"]:
                if isinstance(pattern, str):
                    # Padrão de string simples
                    count = len(re.findall(re.escape(pattern), text, re.IGNORECASE))
                    occurrences += count
                    penalty += count * rules["penalty_per_occurrence"]
                elif isinstance(pattern, dict):
                    # Padrão complexo (implementar lógica específica)
                    penalty += self._detect_complex_pattern(text, pattern, rules)
            
            # Aplicar penalidade máxima
            penalty = max(penalty, rules["max_penalty"])
            
            penalties[characteristic] = {
                "penalty": penalty,
                "occurrences": occurrences,
                "description": rules["description"]
            }
        
        return penalties
    
    def _detect_human_characteristics(self, text: str) -> Dict[str, Any]:
        """Detectar características humanas no texto"""
        bonuses = {}
        human_rules = self.scoring_rules["human_bonuses"]
        
        for characteristic, rules in human_rules.items():
            bonus = 0
            occurrences = 0
            
            # Detectar padrões específicos
            for pattern in rules["detection_patterns"]:
                if isinstance(pattern, str):
                    # Padrão de string simples
                    count = len(re.findall(re.escape(pattern), text, re.IGNORECASE))
                    occurrences += count
                    bonus += count * rules["bonus_per_occurrence"]
                elif isinstance(pattern, dict):
                    # Padrão complexo
                    bonus += self._detect_complex_pattern(text, pattern, rules)
            
            # Aplicar bônus máximo
            bonus = min(bonus, rules["max_bonus"])
            
            bonuses[characteristic] = {
                "bonus": bonus,
                "occurrences": occurrences,
                "description": rules["description"]
            }
        
        return bonuses
    
    def _detect_complex_pattern(self, text: str, pattern: Dict, rules: Dict) -> int:
        """Detectar padrões complexos (implementar lógica específica)"""
        # Implementar lógica para padrões complexos
        # Por exemplo: "repetição de conceitos em 3+ frases consecutivas"
        return 0
    
    def _calculate_total_score(self, ai_penalties: Dict, human_bonuses: Dict) -> int:
        """Calcular pontuação total"""
        total_penalty = sum(penalty["penalty"] for penalty in ai_penalties.values())
        total_bonus = sum(bonus["bonus"] for bonus in human_bonuses.values())
        
        # Calcular pontuação final (0-100)
        raw_score = total_bonus + total_penalty
        normalized_score = max(0, min(100, 50 + raw_score))
        
        return int(normalized_score)
    
    def _generate_recommendations(self, ai_penalties: Dict, human_bonuses: Dict) -> List[str]:
        """Gerar recomendações baseadas na análise"""
        recommendations = []
        
        # Recomendações para reduzir características de IA
        for characteristic, penalty in ai_penalties.items():
            if penalty["penalty"] < -10:  # Penalidade significativa
                ai_rules = self.scoring_rules["ai_penalties"][characteristic]
                recommendations.extend(ai_rules["mitigation_strategies"])
        
        # Recomendações para aumentar características humanas
        for characteristic, bonus in human_bonuses.items():
            if bonus["bonus"] < 10:  # Bônus baixo
                human_rules = self.scoring_rules["human_bonuses"][characteristic]
                recommendations.extend(human_rules["enhancement_strategies"])
        
        return list(set(recommendations))  # Remover duplicatas
    
    def _get_analysis_summary(self, total_score: int) -> str:
        """Obter resumo da análise"""
        thresholds = self.scoring_rules["scoring_system"]
        
        if total_score < thresholds["ai_threshold"]:
            return "Texto muito robótico - precisa de mais humanização"
        elif total_score > thresholds["human_threshold"]:
            return "Texto muito humano - pode precisar de mais estrutura"
        elif thresholds["target_range"][0] <= total_score <= thresholds["target_range"][1]:
            return "Texto bem humanizado - equilíbrio ideal"
        else:
            return "Texto moderadamente humanizado - pode melhorar"
    
    def validate_ryan_style(self, text: str) -> Dict[str, Any]:
        """Validação específica para o estilo do Ryan Santos"""
        analysis = self.analyze_text(text)
        
        # Verificar elementos obrigatórios do Ryan
        ryan_requirements = {
            "rapaziada": "rapaziada" in text.lower(),
            "barcelona": "barcelona" in text.lower(),
            "historia_veridica": "história verídica" in text.lower() or "historia veridica" in text.lower(),
            "sabe_o_que": "sabe o que" in text.lower(),
            "eh_cara": "eh, cara" in text.lower() or "eh cara" in text.lower(),
            "tamo_junto": "tamo junto" in text.lower(),
            "absurdo": "absurdo" in text.lower(),
            "brother": "brother" in text.lower() or "meu irmão" in text.lower()
        }
        
        ryan_score = sum(ryan_requirements.values()) / len(ryan_requirements) * 100
        requirements_met = sum(ryan_requirements.values())
        missing_requirements = [req for req, present in ryan_requirements.items() if not present]
        
        if ryan_score >= 75:
            status = "Excelente"
        elif ryan_score >= 50:
            status = "Bom"
        else:
            status = "Precisa Melhorar"
        
        analysis["ryan_style_score"] = ryan_score
        analysis["ryan_requirements"] = ryan_requirements
        analysis["requirements_met"] = requirements_met
        analysis["missing_requirements"] = missing_requirements
        analysis["status"] = status
        
        return analysis
    
    def _get_level(self, score: int) -> str:
        """Determinar o nível de humanização baseado na pontuação"""
        if score >= 80:
            return "Excelente"
        elif score >= 60:
            return "Bom"
        elif score >= 40:
            return "Regular"
        else:
            return "Precisa Melhorar"

def test_validator():
    """Testar o validador com o texto das eleições 2026"""
    
    # Texto de exemplo
    sample_text = """
    Salve rapaziada, aqui é o Ryan Santos, direto de Barcelona e hoje eu quero falar sobre eleições 2026.
    
    Eh, cara, eleições 2026 é um tema que tá pegando fogo aqui no Brasil. 
    
    Sabe o que é engraçado? Todo mundo fala que eleições 2026 é importante, mas na verdade a galera não entende direito o que tá rolando.
    
    Cara, é impressionante como eleições 2026 pode mudar completamente a vida da gente. Absurdo. Absurdo.
    
    Um amigo meu, história verídica, amigo meu, me falou que eleições 2026 é tipo igual você casar com uma mulher feia. Você vai ter uma mulher feia, mas você vai precisar de uma outra. Então melhor não ter aquela feia.
    
    Olha só, rapaziada, a primeira coisa que você tem que lembrar é que eleições 2026 não é unanimidade. Ele depende de vários fatores.
    
    Vamos olhar esse ano. Esse ano eleições 2026 tá crescendo muito. Uau! Muito mesmo.
    
    E é aqui que a coisa fica interessante... Mas não é só isso não... E o pior (ou melhor) é que... Eh, cara, vamos lá...
    
    Cara, é impressionante o quanto eleições 2026 pode impactar a vida da gente. Absurdo. Absurdo.
    
    Que doideira, né, brother? Assim, olha que doideira, né, cara? eleições 2026 tá mudando tudo.
    
    E aí, o que você acha? Comenta aí! Se você já passou por algo parecido, conta nos comentários! Valeu, rapaziada! Tamo junto!
    """
    
    validator = HumanizationValidator()
    result = validator.validate_ryan_style(sample_text)
    
    print("=== ANÁLISE DE HUMANIZAÇÃO ===")
    print(f"Pontuação Total: {result['total_score']}/100")
    print(f"Análise: {result['analysis']}")
    print(f"Estilo Ryan: {result['ryan_style_score']:.1f}%")
    
    print("\n=== PENALIDADES DE IA ===")
    for char, penalty in result['ai_penalties'].items():
        if penalty['penalty'] < 0:
            print(f"- {char}: {penalty['penalty']} ({penalty['occurrences']} ocorrências)")
    
    print("\n=== BÔNUS HUMANOS ===")
    for char, bonus in result['human_bonuses'].items():
        if bonus['bonus'] > 0:
            print(f"+ {char}: {bonus['bonus']} ({bonus['occurrences']} ocorrências)")
    
    print("\n=== RECOMENDAÇÕES ===")
    for i, rec in enumerate(result['recommendations'][:5], 1):
        print(f"{i}. {rec}")
    
    print("\n=== REQUISITOS RYAN SANTOS ===")
    for req, present in result['ryan_requirements'].items():
        status = "✅" if present else "❌"
        print(f"{status} {req}")

if __name__ == "__main__":
    test_validator()
