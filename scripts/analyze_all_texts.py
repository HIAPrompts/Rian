import os
import re
from collections import Counter
import json

def analyze_all_texts(directory):
    """Analisa todos os arquivos de texto e extrai padrões"""
    
    # Contadores para padrões
    opening_patterns = []
    locations = []
    transitions = []
    colloquial_expressions = []
    questions = []
    storytelling_phrases = []
    calls_to_action = []
    
    # Regex patterns
    salve_pattern = r"Salve.*?(?:e hoje|E hoje|e no dia|E no dia)"
    direto_pattern = r"direto\s+(?:de|da|das|do|dos)\s+([^,\n\.]+)"
    cara_pattern = r"\bcara\b"
    beleza_pattern = r"\bbeleza\b|\bBeleza\b"
    entendeu_pattern = r"\bentendeu\b|\bEntendeu\b"
    
    # Ler todos os arquivos
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    print(f"Analisando {len(files)} arquivos...")
    
    all_text = ""
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                all_text += content + "\n\n"
                
                # Extrair primeiras linhas (abertura)
                first_lines = content[:500]
                opening_patterns.append(first_lines)
                
                # Extrair localizações
                locs = re.findall(direto_pattern, content, re.IGNORECASE)
                locations.extend(locs)
                
        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")
    
    # Análise de padrões
    print("\n=== ANALISE COMPLETA ===\n")
    
    # Localizações mais comuns
    location_counts = Counter(locations)
    print("TOP 20 LOCALIZACOES:")
    for loc, count in location_counts.most_common(20):
        print(f"  - {loc.strip()} ({count}x)")
    
    # Contar palavras-chave
    cara_count = len(re.findall(cara_pattern, all_text, re.IGNORECASE))
    beleza_count = len(re.findall(beleza_pattern, all_text))
    entendeu_count = len(re.findall(entendeu_pattern, all_text))
    
    print(f"\nEXPRESSOES COLOQUIAIS:")
    print(f"  - 'cara': {cara_count} vezes")
    print(f"  - 'beleza': {beleza_count} vezes")
    print(f"  - 'entendeu': {entendeu_count} vezes")
    
    # Buscar padrões de transição
    transition_patterns = [
        r"E aí",
        r"Basicamente",
        r"Só que",
        r"Tipo,",
        r"Então",
        r"Olha só",
        r"Rapaziada",
        r"OK\?",
        r"Beleza\?"
    ]
    
    print(f"\nTRANSICOES E CONECTORES:")
    for pattern in transition_patterns:
        count = len(re.findall(pattern, all_text, re.IGNORECASE))
        if count > 0:
            print(f"  - '{pattern.replace(chr(92), '')}': {count} vezes")
    
    # Buscar padrões de storytelling
    story_patterns = [
        r"Eu quando tinha \d+ anos",
        r"Nessa época",
        r"Era tipo",
        r"Eu lembro que",
        r"Uma vez",
        r"Esses dias"
    ]
    
    print(f"\nPADROES DE STORYTELLING:")
    for pattern in story_patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        if matches:
            print(f"  - '{pattern}': {len(matches)} vezes")
    
    # Salvar primeiras 100 linhas de cada arquivo para referência
    print(f"\nAnalise completa de {len(files)} arquivos!")
    
    return {
        'total_files': len(files),
        'locations': dict(location_counts.most_common(30)),
        'cara_count': cara_count,
        'beleza_count': beleza_count,
        'entendeu_count': entendeu_count
    }

if __name__ == "__main__":
    directory = "textos"
    results = analyze_all_texts(directory)
    
    # Salvar resultados em JSON
    with open('data/outputs/text_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\nResultados salvos em: data/outputs/text_analysis.json")

