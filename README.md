# 🤖 Agente de Escrita Humanizada - Ryan Santos

Um sistema avançado de geração de texto que imita o estilo autêntico do Ryan Santos, desenvolvido para criar conteúdo humanizado que evita detecção por ferramentas de IA.

## 🎯 **Objetivo**

Gerar textos no estilo autêntico do Ryan Santos com alta qualidade e naturalidade, capazes de passar por ferramentas de detecção de IA como GPTZero.

## ✨ **Características Principais**

- **Geração Modular**: Sistema de blocos (abertura, desenvolvimento, conclusão)
- **Elementos Autênticos**: Histórias pessoais, dados específicos, analogias e reflexões
- **Vocabulário Enriquecido**: Gírias e expressões características do Ryan Santos
- **Transições Naturais**: Conectores coloquiais e ruídos humanos
- **Complexidade Sintática**: Estruturas gramaticais variadas e naturais
- **Validação em Tempo Real**: Verificação de autenticidade durante a geração

## 🚀 **Instalação**

### Pré-requisitos
- Python 3.8+
- pip

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agente-escrita-humanizada.git
cd agente-escrita-humanizada

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 📁 **Estrutura do Projeto**

```
agente_escrita_humanizado/
├── src/
│   ├── agent/
│   │   ├── core/
│   │   │   ├── humanized_writer.py    # Gerador principal
│   │   │   ├── automated_reviewer.py  # Revisor automático
│   │   │   └── director.py            # Coordenador
│   │   ├── identity/
│   │   │   └── ryan_santos_profile.yaml
│   │   └── tools/
│   ├── main.py
├── config/
│   ├── prompts/                       # Templates de prompts
│   ├── rules/                         # Regras de humanização
│   └── style_fewshots/               # Exemplos de estilo
├── data/
│   ├── inputs/                       # Entradas de exemplo
│   └── outputs/                      # Saídas geradas
├── textos/                           # Base de textos do Ryan Santos
├── tests/                            # Testes automatizados
└── scripts/                          # Scripts utilitários
```

## 🎮 **Como Usar**

### Uso Básico
```python
from src.agent.core.humanized_writer import HumanizedWriter

# Inicializar o agente
writer = HumanizedWriter()

# Gerar texto sobre um tópico
topic = "Inteligência Artificial"
texto_gerado = writer.humanize(topic)

print(texto_gerado)
```

### Uso Avançado
```python
# Com cliente específico
texto_gerado = writer.humanize(
    topic="Painel solar",
    client_id="cliente_especifico"
)

# Com tamanho personalizado
texto_gerado = writer.humanize(
    topic="Tecnologia",
    client_id="default",
    tamanho_desejado=5000
)
```

## 🧪 **Testes**

Execute os testes para verificar o funcionamento:

```bash
# Teste básico
python test_painel_solar.py

# Teste completo
python test_pipeline_unificado.py

# Teste de autenticidade
python test_autentico_ryan.py
```

## 📊 **Métricas de Qualidade**

O sistema avalia a qualidade do texto gerado através de:

- **Score de Autenticidade**: Percentual de elementos autênticos do Ryan Santos
- **Elementos Incluídos**: Histórias pessoais, dados específicos, analogias, reflexões
- **Validação Gramatical**: Detecção de frases malformadas
- **Tamanho do Texto**: Controle de comprimento desejado

## 🔧 **Configuração**

### Personalizar Estilo
Edite os arquivos em `config/` para ajustar:
- Regras de humanização (`rules/`)
- Templates de prompts (`prompts/`)
- Exemplos de estilo (`style_fewshots/`)

### Adicionar Novos Clientes
1. Crie um arquivo de perfil em `src/agent/identity/`
2. Adicione exemplos em `config/style_fewshots/`
3. Configure as regras específicas

## 🚧 **Status do Projeto**

### ✅ **Implementado**
- Sistema modular de geração
- Elementos autênticos garantidos
- Vocabulário enriquecido
- Transições naturais
- Complexidade sintática
- Validação básica

### 🔄 **Em Desenvolvimento**
- Validação avançada com spaCy
- Fine-tuning de modelo de linguagem
- Métricas de autenticidade precisas
- Otimização do pipeline

### 📈 **Métricas Atuais**
- **Score de Autenticidade**: 31.8% (meta: 70%+)
- **Elementos Autênticos**: 100% inclusão
- **Tamanho**: 3000+ caracteres
- **Frases Malformadas**: < 2 por execução

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 **Autores**

- **Ângelo Guimarães** - *Desenvolvimento Principal* - [GitHub](https://github.com/seu-usuario)

## 🙏 **Agradecimentos**

- Ryan Santos pela inspiração e base de textos
- Comunidade Python pela excelente documentação
- Hugging Face pelos modelos de linguagem

## 📞 **Contato**

- **Email**: angelopintoguimaraes@gmail.com
- **GitHub**: [@seu-usuario](https://github.com/seu-usuario)

---

**Desenvolvido com ❤️ para criar conteúdo autêntico e humanizado**