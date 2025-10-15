import sys
import os
import yaml

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent.core.director import Director
from agent.core.humanized_writer import HumanizedWriter
from agent.core.automated_reviewer import AutomatedReviewer
from agent.core.insight_analyst import InsightAnalyst

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    print("Executando teste de integracao dos agentes...")

    # Carregar configuracoes
    writing_rules = load_config("config/rules/writing_rules.yaml")
    prompt_template = load_config("config/prompts/writing_prompt.yaml")

    print(f"Regras de escrita carregadas: {writing_rules}")
    print(f"Template de prompt carregado: {prompt_template['prompt_template']}")

    # Inicializar agentes
    writer = HumanizedWriter()
    reviewer = AutomatedReviewer()
    analyst = InsightAnalyst()
    director = Director(writer, reviewer, analyst)

    # Conteudo de teste
    test_content = "Inteligencia Artificial esta transformando industrias."

    # Processar conteudo
    processed_content = director.coordinate_process(test_content)

    print("\nTestes concluidos com sucesso!")
    print(f"Conteudo final: {processed_content}")