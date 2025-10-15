#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para gerar matéria sobre Painel Solar com 3000 caracteres
Verificação completa do sistema modular
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from agent.core.humanized_writer import HumanizedWriter

def test_painel_solar():
    """Teste específico para painel solar com 3000 caracteres"""
    
    print("=" * 80)
    print("TESTE ESPECÍFICO - PAINEL SOLAR (3000 CARACTERES)")
    print("Verificação completa do sistema modular")
    print("=" * 80)
    
    try:
        # 1. Inicializar agente
        print("\n1. INICIALIZANDO AGENTE")
        print("-" * 50)
        writer = HumanizedWriter()
        print("SUCESSO - Agente inicializado!")
        
        # 2. Gerar matéria sobre painel solar
        print("\n2. GERANDO MATÉRIA SOBRE PAINEL SOLAR")
        print("-" * 50)
        topic = "Painel solar"
        print(f"Tópico: {topic}")
        
        # Gerar matéria
        materia = writer.humanize(topic, client_id="cliente1")
        
        print(f"Matéria gerada com sucesso!")
        print(f"Tamanho: {len(materia)} caracteres")
        
        # 3. Análise detalhada
        print("\n3. ANÁLISE DETALHADA DA MATÉRIA")
        print("-" * 50)
        
        # Verificar tamanho
        tamanho = len(materia)
        print(f"Tamanho final: {tamanho} caracteres")
        
        if tamanho >= 3000:
            print("[OK] SUCESSO - Tamanho atingido (3000+ caracteres)")
        else:
            print(f"[ATENCAO] ATENÇÃO - Tamanho abaixo do esperado ({tamanho}/3000)")
        
        # Verificar elementos autênticos
        print("\nElementos autênticos do Ryan Santos encontrados:")
        
        # Aberturas autênticas
        aberturas_autenticas = [
            "salve rapaziada", "e aí galera", "olha só rapaziada", 
            "vou contar uma história", "para quem entende do assunto"
        ]
        aberturas_encontradas = sum(1 for abertura in aberturas_autenticas if abertura in materia.lower())
        print(f"- Aberturas autênticas: {aberturas_encontradas}/{len(aberturas_autenticas)}")
        
        # Histórias pessoais
        historias_autenticas = [
            "amigo meu", "história verídica", "eu fui ver os comentários",
            "número de pessoas que me seguem", "mudou o estilo de vida"
        ]
        historias_encontradas = sum(1 for historia in historias_autenticas if historia in materia.lower())
        print(f"- Histórias pessoais: {historias_encontradas}/{len(historias_autenticas)}")
        
        # Dados específicos
        dados_autenticos = [
            "segundo dados da", "fgv", "biden", "bilhões", "estados unidos",
            "elon musk", "tesla", "subsídio", "10 milhões", "carros elétricos",
            "ano passado"
        ]
        dados_encontrados = sum(1 for dado in dados_autenticos if dado in materia.lower())
        print(f"- Dados específicos: {dados_encontrados}/{len(dados_autenticos)}")
        
        # Analogias
        analogias_autenticas = [
            "é tipo igual", "autocracia", "china", "alguém manda",
            "gangue", "trabalham pra eles", "hollywood", "filmes que parecem reais"
        ]
        analogias_encontradas = sum(1 for analogia in analogias_autenticas if analogia in materia.lower())
        print(f"- Analogias autênticas: {analogias_encontradas}/{len(analogias_autenticas)}")
        
        # Reflexões pessoais
        reflexoes_autenticas = [
            "impressionante", "número de pessoas que me seguem", "respeito maior",
            "acontecendo por aí", "não sabem nem o que eu faço"
        ]
        reflexoes_encontradas = sum(1 for reflexao in reflexoes_autenticas if reflexao in materia.lower())
        print(f"- Reflexões pessoais: {reflexoes_encontradas}/{len(reflexoes_autenticas)}")
        
        # Perguntas autênticas
        perguntas_autenticas = [
            "o que vocês acham", "faz sentido", "compreendem a questão",
            "entendeu", "e aí"
        ]
        perguntas_encontradas = sum(1 for pergunta in perguntas_autenticas if pergunta in materia.lower())
        print(f"- Perguntas autênticas: {perguntas_encontradas}/{len(perguntas_autenticas)}")
        
        # Exclamações autênticas
        exclamacoes_autenticas = [
            "valeu rapaziada", "tamo junto", "cara", "olha só",
            "eh cara"
        ]
        exclamacoes_encontradas = sum(1 for exclamacao in exclamacoes_autenticas if exclamacao in materia.lower())
        print(f"- Exclamações autênticas: {exclamacoes_encontradas}/{len(exclamacoes_autenticas)}")
        
        # Calcular score de autenticidade
        total_elementos = (len(aberturas_autenticas) + len(historias_autenticas) + 
                          len(dados_autenticos) + len(analogias_autenticas) + 
                          len(reflexoes_autenticas) + len(perguntas_autenticas) + 
                          len(exclamacoes_autenticas))
        
        elementos_encontrados = (aberturas_encontradas + historias_encontradas + 
                               dados_encontrados + analogias_encontradas + 
                               reflexoes_encontradas + perguntas_encontradas + 
                               exclamacoes_encontradas)
        
        score_autenticidade = (elementos_encontrados / total_elementos) * 100
        
        print(f"\nScore de autenticidade: {score_autenticidade:.1f}%")
        
        if score_autenticidade >= 70:
            print("[OK] SUCESSO - Autenticidade excelente!")
        elif score_autenticidade >= 50:
            print("[ATENCAO] ATENÇÃO - Autenticidade boa, mas pode melhorar")
        else:
            print("[PROBLEMA] PROBLEMA - Autenticidade precisa ser melhorada")
        
        # Verificar frases malformadas
        print("\nVerificando frases malformadas...")
        frases_malformadas = [
            "cara, vamos lá", "a fgv e do insper", "salve rapaziada",
            "é impressionante mesmo como", "entre nós, olha só"
        ]
        
        malformadas_encontradas = 0
        for frase in frases_malformadas:
            if frase in materia.lower():
                malformadas_encontradas += 1
                print(f"  - Encontrada: '{frase}'")
        
        if malformadas_encontradas == 0:
            print("[OK] SUCESSO - Nenhuma frase malformada encontrada!")
        else:
            print(f"[PROBLEMA] PROBLEMA - {malformadas_encontradas} frases malformadas encontradas")
        
        # 4. Exibir matéria completa
        print("\n4. MATÉRIA GERADA SOBRE PAINEL SOLAR")
        print("-" * 50)
        print("=" * 80)
        print(f"MATÉRIA SOBRE {topic.upper()} - SISTEMA MODULAR")
        print("=" * 80)
        print()
        print(materia)
        print()
        print("=" * 80)
        print(f"Tamanho final: {tamanho} caracteres")
        
        # Status final
        if tamanho >= 3000 and score_autenticidade >= 50 and malformadas_encontradas == 0:
            print("Status: [OK] SUCESSO COMPLETO")
        elif tamanho >= 3000 and malformadas_encontradas == 0:
            print("Status: [ATENCAO] SUCESSO PARCIAL - Autenticidade pode melhorar")
        else:
            print("Status: [PROBLEMA] PROBLEMA - Necessita ajustes")
        
        print(f"Score: {score_autenticidade:.1f}%")
        print(f"Frases malformadas: {malformadas_encontradas}")
        print(f"Tamanho: {tamanho}/3000 caracteres")
        
        return True
        
    except Exception as e:
        print(f"[ERRO] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_painel_solar()
    if success:
        print("\n[SUCESSO] Teste concluído com sucesso!")
    else:
        print("\n[FALHA] Teste falhou!")
