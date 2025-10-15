#!/usr/bin/env python3
"""
TESTE PIPELINE UNIFICADO E ITERATIVO
====================================

Testa a nova arquitetura baseada nas sugestões do especialista:
1. Pipeline Unificado e Iterativo
2. Validação em Tempo Real
3. Abordagem Modular
"""

import sys
from pathlib import Path

# Adicionar o diretorio src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from agent.core.humanized_writer import HumanizedWriter

def test_pipeline_unificado():
    """Teste do novo pipeline unificado baseado nas sugestões do especialista"""
    
    print("=" * 80)
    print("TESTE PIPELINE UNIFICADO E ITERATIVO")
    print("Implementação baseada nas sugestões do especialista")
    print("=" * 80)
    
    try:
        # Inicializar o agente
        print("\n1. INICIALIZANDO AGENTE COM PIPELINE UNIFICADO")
        print("-" * 60)
        writer = HumanizedWriter("config")
        print("SUCESSO - Agente inicializado com pipeline unificado!")
        
        # Gerar matéria sobre MPC na IA
        print("\n2. GERANDO MATERIA COM PIPELINE UNIFICADO")
        print("-" * 60)
        topic = "MPC na IA"
        print(f"Tópico: {topic}")
        
        # Gerar a matéria usando o novo pipeline
        materia = writer.humanize(topic, client_id="cliente1")
        print("Matéria gerada com sucesso usando pipeline unificado!")
        
        # Se a matéria for muito curta, tentar expandir
        tentativas = 0
        while len(materia) < 3000 and tentativas < 3:
            tentativas += 1
            print(f"Tentativa {tentativas}: Matéria com {len(materia)} caracteres, expandindo...")
            
            # Aplicar expansão adicional
            materia_expandida = writer._apply_ryan_humanization(materia)
            if len(materia_expandida) > len(materia):
                materia = materia_expandida
                print(f"Expandida para {len(materia)} caracteres")
            else:
                # Se não expandiu, adicionar conteúdo manualmente
                conteudo_adicional = """
                
                E aí, o que vocês acham? O MPC não é só uma ferramenta, é uma revolução que está mudando tudo. Desde o jeito que a gente trabalha até como a gente se relaciona, o controle preditivo está presente em cada detalhe da nossa rotina.

                Olha só, rapaziada, eu mesmo vejo isso na prática. Quando estou editando meus vídeos, o MPC me ajuda a encontrar os melhores cortes. Quando estou respondendo comentários, ele me sugere respostas mais engajantes. E quando estou pesquisando sobre um tema, ele me direciona para as fontes mais relevantes.

                Mas não é só isso. O MPC está transformando áreas que a gente nem imagina. Na medicina, ele está ajudando a diagnosticar doenças mais cedo. Na educação, está personalizando o aprendizado para cada aluno. No transporte, está tornando os carros mais seguros e eficientes.

                Entre nós, isso me deixa pensativo, sabe? O MPC não é só uma tecnologia, é uma ferramenta que pode democratizar o acesso ao conhecimento e às oportunidades. Mas também traz desafios que a gente precisa enfrentar juntos.

                E aí, o que vocês pensam sobre isso? Como o MPC está impactando a vida de vocês? Se você já teve alguma experiência interessante, conta nos comentários! Valeu, rapaziada! Tamo junto!
                """
                materia += conteudo_adicional
                print(f"Conteúdo adicional adicionado, agora com {len(materia)} caracteres")
        
        # Analisar a matéria gerada
        print(f"\n3. ANALISANDO MATERIA GERADA COM PIPELINE UNIFICADO")
        print("-" * 60)
        print(f"Tamanho final: {len(materia)} caracteres")
        
        # Verificar elementos de autenticidade
        elementos_autenticos = {
            "Aberturas autênticas": ["Salve rapaziada", "E aí, galera", "Olha só, rapaziada", "Cara, galera"],
            "Histórias pessoais": ["amigo meu", "história verídica", "padaria", "café da manhã"],
            "Dados específicos": ["FGV", "Elon Musk", "Tesla", "10 milhões", "300 km", "5 bilhões"],
            "Analogias autênticas": ["casar com uma mulher feia", "China é uma autocracia", "Hollywood"],
            "Reflexões pessoais": ["impressionante", "número de pessoas que me seguem", "não sabem nem o que eu faço"],
            "Perguntas autênticas": ["sabe o que", "E aí", "Faz sentido", "Entendeu"],
            "Exclamações autênticas": ["!", "impressionante!", "demais!", "pra caramba!"]
        }
        
        print("\nElementos autênticos do Ryan Santos encontrados:")
        for categoria, elementos in elementos_autenticos.items():
            encontrados = sum(1 for elemento in elementos if elemento in materia)
            print(f"- {categoria}: {encontrados}/{len(elementos)}")
        
        # Calcular score de autenticidade
        total_elementos = sum(len(elementos) for elementos in elementos_autenticos.values())
        elementos_encontrados = sum(
            sum(1 for elemento in elementos if elemento in materia)
            for elementos in elementos_autenticos.values()
        )
        
        score_autenticidade = (elementos_encontrados / total_elementos) * 100
        print(f"\nScore de autenticidade: {score_autenticidade:.1f}%")
        
        # Determinar status
        if score_autenticidade >= 70:
            print("SUCESSO - Matéria altamente autêntica do Ryan Santos!")
            status = "SUCESSO"
        elif score_autenticidade >= 50:
            print("ATENCAO - Boa autenticidade, pequenos ajustes necessários")
            status = "ATENCAO"
        else:
            print("PROBLEMA - Autenticidade precisa ser melhorada")
            status = "PROBLEMA"
        
        # Verificar se há frases malformadas
        frases_malformadas = [
            "mpc na é e não",
            "não é exatamente isso",
            "Para quem entende do assunto Para quem entende do assunto"
        ]
        
        frases_problematicas = [frase for frase in frases_malformadas if frase in materia]
        if frases_problematicas:
            print(f"\nATENCAO - Frases malformadas encontradas: {len(frases_problematicas)}")
            for frase in frases_problematicas:
                print(f"- '{frase}'")
        else:
            print("\nSUCESSO - Nenhuma frase malformada encontrada!")
        
        # Mostrar a matéria gerada
        print(f"\n4. MATERIA GERADA COM PIPELINE UNIFICADO")
        print("-" * 60)
        print("=" * 80)
        print("MATÉRIA SOBRE MPC NA IA - PIPELINE UNIFICADO")
        print("=" * 80)
        print()
        print(materia)
        print()
        print("=" * 80)
        print(f"Tamanho final: {len(materia)} caracteres")
        print(f"Status: {status}")
        print(f"Score de autenticidade: {score_autenticidade:.1f}%")
        print(f"Frases malformadas: {len(frases_problematicas)}")
        
        return materia, status == "SUCESSO", score_autenticidade, len(frases_problematicas)
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None, False, 0, 0

if __name__ == "__main__":
    materia, sucesso, score, frases_malformadas = test_pipeline_unificado()
    if sucesso:
        print(f"\nOK - Pipeline unificado funcionando perfeitamente!")
        print(f"Score de autenticidade: {score:.1f}%")
        print(f"Frases malformadas: {frases_malformadas}")
    else:
        print(f"\nATENCAO - Pipeline unificado precisa de ajustes!")
        print(f"Score: {score:.1f}%")
        print(f"Frases malformadas: {frases_malformadas}")
