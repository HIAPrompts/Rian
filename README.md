# Agente de Escrita Humanizado - Ryan Santos

Projeto para escrita, revisão e análise de conteúdo humanizado usando agentes especializados baseados na identidade do Ryan Santos.

## Estrutura do Projeto

```
agente_escrita_humanizado/
├── src/
│   ├── agent/
│   │   ├── core/
│   │   │   ├── director.py
│   │   │   ├── humanized_writer.py
│   │   │   ├── intelligent_writer.py
│   │   │   ├── automated_reviewer.py
│   │   │   └── insight_analyst.py
│   │   └── identity/
│   │       └── ryan_santos_profile.yaml
│   └── main.py
├── config/
│   ├── prompts/
│   │   ├── writing_prompt.yaml
│   │   ├── intake_prompt.yaml
│   │   ├── review_prompt.yaml
│   │   └── scoring_prompt.yaml
│   ├── rules/
│   │   ├── writing_rules.yaml
│   │   ├── hard_gates.json
│   │   └── stylometry_rules.json
│   ├── style_fewshots/
│   │   ├── cliente1.json (Ryan Santos examples)
│   │   └── cliente2.json
│   └── settings.yaml
├── tests/
│   ├── __init__.py
│   └── integration_test.py
├── base texto ryan.txt
├── run_project.py
└── requirements.txt
```

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o projeto:
   ```bash
   python run_project.py
   ```

3. Execute os testes:
   ```bash
   python -m tests.integration_test
   ```

## Funcionalidades

- **Director**: Coordena o processo de escrita
- **HumanizedWriter**: Processa conteúdo de forma humanizada
- **AutomatedReviewer**: Revisa automaticamente o conteúdo
- **InsightAnalyst**: Analisa insights do conteúdo

## Configuração

O projeto usa arquivos YAML para configuração:
- `config/rules/writing_rules.yaml`: Regras de escrita
- `config/prompts/writing_prompt.yaml`: Templates de prompts
