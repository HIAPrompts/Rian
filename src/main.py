from agent.core.director import Director
from agent.core.humanized_writer import HumanizedWriter
from agent.core.automated_reviewer import AutomatedReviewer
from agent.core.insight_analyst import InsightAnalyst

if __name__ == '__main__':
    print('Iniciando Agente de Escrita Humanizado')

    writer = HumanizedWriter()
    reviewer = AutomatedReviewer()
    analyst = InsightAnalyst()
    director = Director(writer, reviewer, analyst)

    sample_content = 'Exemplo de conteudo para processamento.'
    processed_content = director.coordinate_process(sample_content)

    print('Processo concluido com sucesso!')
    print(f'Conteudo processado: {processed_content}')
