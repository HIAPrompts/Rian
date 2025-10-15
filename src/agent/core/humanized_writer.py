import yaml
import json
import random
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HumanizedWriter:
    """
    A class to handle the humanization of text based on predefined rules and examples.
    Now enhanced with comprehensive rules from analysis of 33 real texts.

    Attributes:
        writing_rules (Dict[str, Any]): Comprehensive rules for writing style and tone.
        prompt_template (str): Template for generating humanized text.
        few_shots (Dict[str, Any]): Examples of humanized text for reference.
        hard_gates (Dict[str, Any]): Strict rules for humanization.
    """

    def __init__(self, config_path: str = "config"):
        """
        Initialize the HumanizedWriter with configuration files.

        Args:
            config_path (str): Path to the directory containing configuration files.
        """
        logger.debug("Inicializando HumanizedWriter")
        self.config_path = Path(config_path)
        logger.debug(f"Carregando configurações do diretório: {self.config_path}")
        
        logger.debug("Carregando regras de escrita...")
        self.writing_rules = self._load_yaml("rules/writing_rules.yaml")
        logger.debug("Carregando template de prompt...")
        self.prompt_template = self._load_yaml("prompts/writing_prompt_complete.yaml")
        logger.debug("Carregando exemplos de estilo...")
        self.few_shots = self._load_json("style_fewshots/cliente1.json")
        logger.debug("Carregando regras rígidas...")
        self.hard_gates = self._load_json("rules/hard_gates.json")
        
        # Carregar perfil do Ryan Santos
        logger.debug("Carregando perfil do Ryan Santos...")
        self.ryan_profile = self._load_yaml("../../src/agent/identity/ryan_santos_profile.yaml")
        
        # Sistema preventivo para evitar problemas de IA
        self.problematic_patterns = self._load_problematic_patterns()
        self.human_patterns = self._load_human_patterns()
        
        # Cache frequently used rules for performance
        self._cache_rules()

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file with error handling.

        Args:
            file_path (str): Path to the YAML file.

        Returns:
            Dict[str, Any]: The loaded YAML content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the YAML is invalid.
        """
        try:
            if "ryan_santos_profile.yaml" in file_path:
                yaml_path = Path(__file__).parent.parent.parent / "agent" / "identity" / "ryan_santos_profile.yaml"
            else:
                yaml_path = self.config_path / file_path

            with open(yaml_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo YAML não encontrado: {yaml_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Erro ao carregar YAML: {e}")

    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load a JSON configuration file with error handling.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            Dict[str, Any]: The loaded JSON content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON is invalid.
        """
        try:
            json_path = self.config_path / file_path
            with open(json_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo JSON não encontrado: {json_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao carregar JSON: {e}")

    def _cache_rules(self):
        """Cache frequently used rules for better performance."""
        self.max_words = self.writing_rules["linguistic_structure"]["sentence_length"]["max_words"]
        self.avg_words = self.writing_rules["linguistic_structure"]["sentence_length"]["avg_words"]
        self.formality_level = self.writing_rules["tone_adaptation"]["formality_level"]
        self.tone = self.writing_rules["tone"]
        self.banned_words = self.writing_rules["vocabulary_rules"]["banned_words"]
        self.power_words = self.writing_rules["vocabulary_rules"]["power_words"]
        self.transition_words = self.writing_rules["text_flow"]["transition_words"]
        self.colloquial_expressions = self.writing_rules["human_language"]["colloquial_expressions"]

    def humanize(self, topic: str, client_id: str = "cliente1") -> str:
        """
        PIPELINE UNIFICADO E ITERATIVO - Geração com autenticidade desde o início
        Implementação baseada nas sugestões do especialista.

        Args:
            topic (str): The topic to humanize.
            client_id (str): Identifier for client-specific few-shots.

        Returns:
            str: The humanized text with high authenticity.
        """
        # PIPELINE UNIFICADO: Gerar texto com autenticidade desde o início
        humanized_text = self._generate_unified_text(topic, client_id)
        
        # Validação em tempo real e ajuste dinâmico
        humanized_text = self._validate_and_adjust_realtime(humanized_text, topic)
        
        # Validar elementos autênticos incluídos
        self._validar_elementos_autenticos(humanized_text)
        
        # MELHORIAS DE AUTENTICIDADE - Prioridade 1
        print(f"[DEBUG] Aplicando melhorias de autenticidade...")
        
        # 1. Enriquecer vocabulário com gírias e expressões do Ryan Santos
        humanized_text = self._enriquecer_vocabulario(humanized_text)
        print(f"[DEBUG] Vocabulário enriquecido")
        
        # 2. Adicionar transições naturais e ruídos humanos
        humanized_text = self._adicionar_transicoes_naturais(humanized_text)
        print(f"[DEBUG] Transições naturais adicionadas")
        
        # 3. Adicionar complexidade sintática
        humanized_text = self._adicionar_complexidade_sintatica(humanized_text)
        print(f"[DEBUG] Complexidade sintática adicionada")
        
        # 4. Remover repetições excessivas
        humanized_text = self._remover_repeticoes_excessivas(humanized_text)
        print(f"[DEBUG] Repetições excessivas removidas")
        
        # Expansão automática para atingir tamanho desejado
        humanized_text = self._expandir_para_tamanho_desejado(humanized_text, topic, tamanho_desejado=3000)
        
        # Correção final apenas de problemas críticos
        humanized_text = self._fix_critical_issues(humanized_text)
        
        return humanized_text

    def _generate_unified_text(self, topic: str, client_id: str) -> str:
        """
        ABORDAGEM MODULAR: Gerar texto em blocos lógicos com autenticidade desde o início
        Implementação baseada nas sugestões do especialista.
        """
        # 1. ABERTURA - Template autêntico do base texto ryan.txt
        opening = self._generate_modular_opening(topic)
        
        # 2. DESENVOLVIMENTO - Bloco com elementos autênticos incorporados
        development = self._generate_modular_development(topic)
        
        # 3. CONCLUSÃO - Padrões autênticos do Ryan Santos
        conclusion = self._generate_modular_conclusion(topic)
        
        # Combinar blocos com transições naturais
        print(f"[DEBUG] Abertura: {opening}")
        print(f"[DEBUG] Desenvolvimento: {development}")
        print(f"[DEBUG] Conclusão: {conclusion}")
        unified_text = f"{opening}\n\n{development}\n\n{conclusion}"
        print(f"[DEBUG] Texto unificado: {unified_text}")  # Log do texto final
        
        return unified_text

    def _validar_elementos_autenticos(self, texto: str) -> dict:
        """
        Validação detalhada de elementos autênticos no texto.
        Verifica a presença de histórias pessoais, dados específicos, analogias e reflexões.

        Args:
            texto (str): Texto a ser validado.

        Returns:
            dict: Dicionário com os elementos autênticos encontrados.
        """
        texto_lower = texto.lower()
        elementos = {
            "historia_pessoal": bool(
                any(frase in texto_lower for frase in [
                    "amigo meu", "história verídica", "eu fui ver os comentários",
                    "número de pessoas que me seguem", "aconteceu comigo"
                ])
            ),
            "dados_especificos": bool(
                any(frase in texto_lower for frase in [
                    "segundo dados da", "fgv", "biden", "bilhões",
                    "estados unidos", "elon musk", "tesla", "subsídio",
                    "10 milhões", "carros elétricos", "ano passado"
                ])
            ),
            "analogias": bool(
                any(frase in texto_lower for frase in [
                    "é tipo igual", "autocracia", "china", "alguém manda",
                    "gangue", "trabalham pra eles", "hollywood", "filmes que parecem reais",
                    "super fakes"
                ])
            ),
            "reflexoes": bool(
                any(frase in texto_lower for frase in [
                    "impressionante", "respeito maior", "acontecendo por aí",
                    "o que me choca", "o que me impressiona"
                ])
            ),
        }

        # Adicionar validação de coerência temática (exemplo simples)
        if "tecnologia" in texto_lower:
            elementos["coerencia_tematica"] = bool(
                any(palavra in texto_lower for palavra in ["ia", "inteligência artificial", "inova", "futuro"])
            )
        else:
            elementos["coerencia_tematica"] = True  # Pular se não for sobre tecnologia

        logger.debug(f"Validação de elementos autênticos: {elementos}")
        return elementos

    def _enriquecer_vocabulario(self, texto: str) -> str:
        """
        Enriquecer vocabulário com gírias e expressões do Ryan Santos,
        substituindo palavras genéricas com base em probabilidade.

        Args:
            texto (str): Texto a ser enriquecido.

        Returns:
            str: Texto com vocabulário enriquecido.
        """
        logger.debug(f"Iniciando enriquecimento de vocabulário para texto de {len(texto)} caracteres")
        replacements = {
            "interessante": ["doido", "maluco", "absurdo", "impressionante", "louco", "daora", "massa", "top", "foda", "incrível", "sensacional"],
            "pessoas": ["galera", "pessoal", "rapaziada", "turma", "gente", "povo", "massa", "turminha", "galerinha"],
            "verdade": ["papo reto", "sem mentira", "na moral", "de verdade", "papo sério", "na real", "de fato", "realmente"],
            "muito": ["pra caramba", "demais", "pra cacete", "muito mesmo", "pra caralho", "pra porra", "pra dedéu", "pra valer"],
            "legal": ["daora", "massa", "top", "foda", "bacana", "maneiro", "show", "irado", "animal"],
            "problema": ["rolo", "pepino", "barriga", "encrenca"],
            "dinheiro": ["grana", "verba", "tutu", "dinheiro mesmo", "grana mesmo"],
            "trabalho": ["trampo", "labuta", "serviço", "trabalho mesmo"],
            "casa": ["lar", "casa mesmo", "apê", "moradia"],
            "carro": ["veículo", "carro mesmo", "automóvel", "máquina"],
            "comida": ["comida mesmo", "alimentação", "comida", "refeição"],
            "tecnologia": ["tech", "tecnologia mesmo", "parada tecnológica", "inovação"],
            "empresa": ["firma", "empresa mesmo", "negócio", "companhia"],
            "governo": ["governo mesmo", "gestão pública", "administração", "poder público"],
            "mercado": ["mercado mesmo", "setor", "área", "segmento"],
            "investimento": ["investimento mesmo", "aplicação", "colocação", "grana aplicada"],
            "resultado": ["resultado mesmo", "desfecho", "consequência", "final"],
            "oportunidade": ["oportunidade mesmo", "chance", "possibilidade", "abertura"],
            "desafio": ["desafio mesmo", "pepino", "rolo", "encrenca"],
            "sucesso": ["sucesso mesmo", "vitória", "conquista", "realização"],
            "importante": ["importante mesmo", "fundamental", "essencial", "crucial"],
            "difícil": ["difícil mesmo", "complicado", "trampo", "pepino"],
            "fácil": ["fácil mesmo", "simples", "tranquilo", "de boa"],
            "grande": ["grande mesmo", "enorme", "gigante", "monstro"],
            "pequeno": ["pequeno mesmo", "pequeninho", "minúsculo", "tiquinho"],
            "novo": ["novo mesmo", "novinho", "recente", "atual"],
            "velho": ["velho mesmo", "antigo", "antiquado", "ultrapassado"],
            "bom": ["bom mesmo", "bão", "daora", "massa", "top", "foda"],
            "ruim": ["ruim mesmo", "péssimo", "horrível", "terrível"],
            "certo": ["certo mesmo", "correto"],
            "errado": ["errado mesmo", "incorreto"],
            "sim": ["sim mesmo", "é", "é isso", "isso aí"],
            "não": ["não mesmo", "não é", "não é isso", "não é isso aí"],
        }

        # Dividir o texto em palavras e substituir com probabilidade de 30%
        palavras = texto.split()
        substituicoes = 0
        for i, palavra in enumerate(palavras):
            palavra_lower = palavra.lower()
            for generic, slangs in replacements.items():
                if palavra_lower == generic:
                    if random.random() < 0.3:  # 30% de chance de substituir
                        palavras[i] = random.choice(slangs)
                        substituicoes += 1
                        logger.debug(f"Substituindo '{palavra}' por '{palavras[i]}'")
                        break  # Evita substituir a mesma palavra múltiplas vezes

        logger.debug(f"Enriquecimento concluído: {substituicoes} substituições realizadas")
        return ' '.join(palavras)

    def _adicionar_transicoes_naturais(self, texto: str) -> str:
        """
        Adicionar transições naturais e ruídos humanos
        Implementação baseada nas sugestões do especialista.
        """
        # Transições naturais mais específicas do Ryan Santos
        transitions = [
            "mas antes de continuar, ",
            "e aqui vem o pulo do gato: ",
            "só que tem um detalhe que ninguém fala: ",
            "e é aí que a coisa fica interessante... ",
            "mas não para por aí, ",
            "e o pior é que ",
            "sabe o que é louco? ",
            "peraí, deixa eu te contar: ",
            "olha só que absurdo: ",
            "e adivinha só: ",
            "mas tem uma parada que ",
            "e o que me choca é que ",
            "só que tem um porém: ",
            "e aqui que fica doido: ",
            "mas não é só isso, ",
            "e aí que fica interessante: ",
            "mas olha só: ",
            "e o que me impressiona é que ",
            "só que tem uma pegada: ",
            "e é aí que a parada fica doida: ",
            "mas tem um detalhe: ",
            "e o que ninguém conta é que ",
            "só que tem uma parada que ",
            "e é aí que a coisa desanda: "
        ]
        
        # Conectores coloquiais mais variados
        conectores = [
            "aí", "daí", "mas ó", "só que", "e o pior", "e adivinha", 
            "mas não para por aí", "e aí", "mas olha", "só que tem uma pegada",
            "e é aí que", "mas tem um detalhe", "e o que me choca",
            "só que", "e daí", "mas peraí", "e olha só", "mas tem uma parada"
        ]
        
        # Dividir em parágrafos
        paragraphs = texto.split("\n\n")
        
        # Adicionar transições naturais entre parágrafos (reduzir frequência)
        for i in range(1, len(paragraphs)):
            if random.random() < 0.2:  # 20% chance (reduzido de 40%)
                transition = random.choice(transitions)
                paragraphs[i] = transition + paragraphs[i]
        
        # Adicionar conectores coloquiais dentro dos parágrafos (reduzir frequência)
        for i, paragraph in enumerate(paragraphs):
            sentences = paragraph.split(". ")
            for j in range(1, len(sentences)):
                if random.random() < 0.1:  # 10% chance (reduzido de 20%)
                    conector = random.choice(conectores)
                    sentences[j] = f"{conector}, {sentences[j]}"
            paragraphs[i] = ". ".join(sentences)
        
        return "\n\n".join(paragraphs)

    def _adicionar_complexidade_sintatica(self, texto: str) -> str:
        """
        Adicionar complexidade sintática e estruturas gramaticais variadas
        Implementação baseada nas sugestões do especialista.
        """
        # Templates com variação sintática mais natural e menos repetitiva
        templates_complexos = [
            "Sabe o que é louco? {frase_original}... mas não foi fácil, não!",
            "Peraí, deixa eu te contar: {frase_original}... e o pior é que {contexto_inesperado}!",
            "Olha só que absurdo: {frase_original}... é ou não é impressionante?",
            "Cara, {frase_original}... e adivinha só? {resultado_surpreendente}!",
            "Mas ó, {frase_original}... e o que me choca é que {detalhe_chocante}!",
            "Só que tem um detalhe que ninguém fala: {frase_original}... e é aí que a coisa fica interessante!",
            "E aqui vem o pulo do gato: {frase_original}... mas não para por aí!",
            "Aí que fica doido: {frase_original}... e o pior é que {complicacao}!",
            "Mas antes de continuar, {frase_original}... e o que me impressiona é que {impressao}!",
            "E é aí que a parada fica interessante: {frase_original}... mas tem um porém!",
            "E olha só que coisa: {frase_original}... e o que ninguém conta é que {contexto_inesperado}!",
            "Mas tem uma pegada: {frase_original}... e é aí que a parada desanda!",
            "E aí que fica interessante: {frase_original}... mas tem um detalhe que ",
            "Só que tem uma parada: {frase_original}... e o que me impressiona é que ",
            "E é aí que a coisa fica doida: {frase_original}... mas não é só isso!"
        ]
        
        # Contextos inesperados mais variados e específicos
        contextos_inesperados = [
            "ninguém esperava que isso fosse acontecer",
            "a coisa desandou de um jeito que ninguém previa",
            "o resultado foi completamente diferente do que todo mundo pensava",
            "a parada tomou um rumo que ninguém imaginava",
            "o negócio evoluiu de uma forma que surpreendeu todo mundo",
            "a situação se desenrolou de um jeito inesperado",
            "o desfecho foi muito mais interessante do que parecia",
            "a coisa se complicou de uma forma que ninguém via chegando",
            "o negócio tomou uma direção que ninguém esperava",
            "a parada evoluiu de um jeito que surpreendeu geral",
            "o resultado foi muito mais impactante do que parecia",
            "a situação se desenrolou de uma forma inesperada",
            "o desfecho foi bem mais interessante do que todo mundo pensava",
            "a coisa se complicou de um jeito que ninguém via vindo",
            "o negócio tomou um rumo que surpreendeu todo mundo"
        ]
        
        # Dividir em frases e aplicar complexidade (reduzir frequência)
        sentences = texto.split(". ")
        sentences_complexas = []
        
        for sentence in sentences:
            if len(sentence) > 25 and random.random() < 0.25:  # 25% chance (reduzido de 40%)
                template = random.choice(templates_complexos)
                contexto = random.choice(contextos_inesperados)
                
                # Preencher o template
                frase_complexa = template.format(
                    frase_original=sentence,
                    contexto_inesperado=contexto,
                    resultado_surpreendente=contexto,
                    detalhe_chocante=contexto,
                    complicacao=contexto,
                    impressao=contexto
                )
                sentences_complexas.append(frase_complexa)
            else:
                sentences_complexas.append(sentence)
        
        return ". ".join(sentences_complexas)

    def _remover_repeticoes_excessivas(self, texto: str) -> str:
        """
        Remover repetições excessivas de frases e palavras
        Implementação baseada nas sugestões do especialista.
        """
        # Dividir em frases
        sentences = texto.split(". ")
        sentences_unicas = []
        frases_ja_vistas = set()
        
        for sentence in sentences:
            # Normalizar frase para comparação (remover espaços extras, converter para minúsculas)
            frase_normalizada = sentence.strip().lower()
            
            # Se a frase não foi vista antes, adicionar (ser menos restritivo)
            if frase_normalizada not in frases_ja_vistas and len(frase_normalizada) > 5:
                sentences_unicas.append(sentence)
                frases_ja_vistas.add(frase_normalizada)
            # Se for uma frase muito curta mas importante, manter
            elif len(frase_normalizada) <= 5 and any(palavra in frase_normalizada for palavra in ["valeu", "tamo", "junto", "galera", "rapaziada"]):
                sentences_unicas.append(sentence)
        
        return ". ".join(sentences_unicas)

    def _expandir_para_tamanho_desejado(self, texto: str, topic: str, tamanho_desejado: int = 3000) -> str:
        """
        Expande o texto de forma contextualizada, adicionando conteúdo relevante ao tópico.

        Args:
            texto (str): Texto a ser expandido.
            topic (str): Tópico do texto.
            tamanho_desejado (int): Tamanho desejado em caracteres.

        Returns:
            str: Texto expandido.
        """
        tamanho_atual = len(texto)
        if tamanho_atual >= tamanho_desejado:
            return texto

        logger.debug(f"Expandindo texto de {tamanho_atual} para {tamanho_desejado} caracteres")

        # Conteúdo adicional contextualizado
        conteudo_adicional = [
            f"E aí, o que vocês acham? O {topic} não é só uma ferramenta, é uma revolução que está mudando a forma como a gente vive e trabalha. É impressionante como isso impacta desde o dia a dia até grandes indústrias.",
            f"Olha só, rapaziada, eu mesmo vejo isso na prática. Quando estou pesquisando sobre {topic}, fico impressionado com como as coisas estão evoluindo rápido. É uma parada que merece atenção.",
            f"Mas não é só isso. O {topic} está transformando áreas que a gente nem imagina. Na saúde, na educação, nos transportes... é uma revolução silenciosa que está acontecendo agora.",
            f"Entre nós, isso me deixa pensativo. O {topic} não é só uma tecnologia, é uma ferramenta que pode democratizar o acesso ao conhecimento. Mas também traz desafios que a gente precisa discutir.",
            f"E aí, o que vocês pensam sobre isso? Como o {topic} está impactando a vida de vocês? Se vocês já tiveram alguma experiência, conta nos comentários! Valeu, galera!",
            f"Cara, é impressionante como o {topic} está presente em tudo hoje em dia. Desde aplicativos até grandes sistemas, essa tecnologia está mudando o jogo.",
            f"Sabe o que é louco? O {topic} não é só uma tendência, é uma realidade que veio para ficar. E a gente precisa estar preparado para aproveitar o melhor disso.",
            f"E aí, o que vocês acham? O {topic} é uma parada que vai impactar todo mundo. Se isso faz sentido para vocês, compartilha com quem precisa saber!",
        ]

        while len(texto) < tamanho_desejado:
            paragrafo = random.choice(conteudo_adicional)
            texto += f"\n\n{paragrafo}"

            # Evitar loop infinito
            if len(texto) > tamanho_desejado * 1.5:
                break

        logger.debug(f"Texto expandido para {len(texto)} caracteres")
        return texto

    def _generate_modular_opening(self, topic: str) -> str:
        """
        ABORDAGEM MODULAR: Gerar abertura usando templates autênticos
        Implementação baseada nas sugestões do especialista.
        """
        # Templates autênticos extraídos do base texto ryan.txt
        templates_abertura = [
            "Salve rapaziada, aqui é o Ryan Santos, direto de Barcelona, direto da minha base aqui na Europa e hoje a gente vai conversar sobre {topic}",
            "E aí, galera! Aqui é o Ryan Santos, direto de Barcelona e hoje eu quero trazer um ângulo diferente sobre {topic}",
            "Olha só, rapaziada, aqui é o Ryan Santos, direto de Barcelona e hoje a gente vai falar sobre {topic}",
            "Cara, galera, aqui é o Ryan Santos, direto de Barcelona e hoje eu quero discutir sobre {topic}",
            "E aí, o que vocês acham? Aqui é o Ryan Santos, direto de Barcelona e hoje a gente vai conversar sobre {topic}",
            "Vou contar uma história que aconteceu comigo semana passada sobre {topic}",
            "Para quem entende do assunto, isso aqui é impressionante... {topic} é uma parada que mexe comigo de verdade"
        ]
        
        template = random.choice(templates_abertura)
        return template.format(topic=topic)

    def _generate_modular_development(self, topic: str) -> str:
        """
        ABORDAGEM MODULAR: Gerar desenvolvimento com templates dinâmicos
        Implementação baseada nas sugestões do especialista.
        """
        # Templates modulares conforme sugerido pelo especialista
        templates_desenvolvimento = {
            "historia_pessoal": [
                "Um amigo meu, história verídica, ele {acao} e {resultado}...",
                "Cara, um amigo meu de confiança me falou uma coisa interessante sobre {topic}...",
                "E sabe o que que eu escutei aí na rua? É impressionante como {contexto}...",
                "Um amigo meu que foi muito comedor, esse amigo meu, ele mudou o estilo de vida...",
                "E é impressionante, eu fui ver os comentários, é impressionante o número de pessoas que me seguem..."
            ],
            "dados_especificos": [
                "Segundo dados da {fonte}, {dado}...",
                "A {fonte} e do Insper, cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço...",
                "Porque sem subsídio, o próprio {pessoa}, sem subsídio a {empresa} não seria nem 10% do que é...",
                "O ano passado se vendeu no planeta Terra {numero} de {produto}. E aí, por que que você acha que vai cair?...",
                "Os Estados Unidos, o {politico}, tá, você digita, você vê, colocou uma linha de {valor} para {acao}..."
            ],
            "analogias": [
                "É tipo igual você casar com uma mulher feia, você vai ter uma mulher feia, mas você vai precisar de uma outra. Então melhor não ter aquela feia...",
                "A China é uma autocracia. Que que é uma autocracia? Alguém manda, todo mundo obedece...",
                "É impressionante como Hollywood consegue fazer filmes que parecem reais, mas são super fakes...",
                "É impressionante como eles têm uma gangue de pessoas que trabalham pra eles..."
            ],
            "reflexoes": [
                "Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço...",
                "É impressionante como eu parei de gastar dinheiro com coisas que não precisava...",
                "É impressionante como o respeito maior vem das pessoas que não me conhecem...",
                "Eh, cara, é impressionante o que está acontecendo por aí..."
            ]
        }
        
        # Dados dinâmicos para preenchimento
        dados_dinamicos = {
            "acao": "trabalhava com IA",
            "resultado": "conseguiu aumentar a produtividade em 40%",
            "contexto": "as coisas mudaram rapidamente",
            "fonte": "FGV",
            "dado": "a adoção de IA deve crescer 30% nos próximos anos",
            "pessoa": "Elon Musk",
            "empresa": "Tesla",
            "numero": "10 milhões",
            "produto": "carros elétricos",
            "politico": "Biden",
            "valor": "5 bilhões de dólares",
            "acao": "colocar carregador, uma estrutura de carregamento a cada 40 milhas em todas as estradas"
        }
        
        development_parts = []
        
        # 1. INTRODUÇÃO DO TEMA (sempre presente)
        intro_patterns = [
            f"Eh, por que que eu digo isso, rapaziada? {topic} é uma parada que mexe comigo de verdade.",
            f"Cara, {topic} é algo que eu venho acompanhando há um tempo e preciso compartilhar com vocês.",
            f"Olha só, rapaziada, {topic} é um tema que está mudando tudo e vocês precisam saber disso.",
            f"Sabe o que é interessante? {topic} é uma revolução silenciosa que está acontecendo agora.",
            f"Vamos olhar esse ano. {topic} está transformando a forma como pensamos sobre tecnologia."
        ]
        intro = random.choice(intro_patterns)
        development_parts.append(intro)
        
        # 2. HISTÓRIA PESSOAL (70% chance) - FORÇAR INCLUSÃO
        if True:  # Sempre incluir para garantir autenticidade
            template_historia = random.choice(templates_desenvolvimento["historia_pessoal"])
            print(f"[DEBUG] Template de história selecionado: {template_historia}")
            historia = self._preencher_template(template_historia, topic=topic, **dados_dinamicos)
            print(f"[DEBUG] História gerada: {historia}")  # Log da história gerada
            development_parts.append(historia)
            print(f"[DEBUG] development_parts após adição da história: {development_parts}")  # Log da lista
        
        # 3. DADOS ESPECÍFICOS (60% chance) - FORÇAR INCLUSÃO
        if True:  # Sempre incluir para garantir autenticidade
            template_dados = random.choice(templates_desenvolvimento["dados_especificos"])
            print(f"[DEBUG] Template de dados selecionado: {template_dados}")
            dados = self._preencher_template(template_dados, topic=topic, **dados_dinamicos)
            print(f"[DEBUG] Dados gerados: {dados}")  # Log dos dados gerados
            development_parts.append(dados)
            print(f"[DEBUG] development_parts após adição dos dados: {development_parts}")  # Log da lista
        
        # 4. ANALOGIA (50% chance) - FORÇAR INCLUSÃO
        if True:  # Sempre incluir para garantir autenticidade
            template_analogia = random.choice(templates_desenvolvimento["analogias"])
            print(f"[DEBUG] Template de analogia selecionado: {template_analogia}")
            analogia = self._preencher_template(template_analogia, topic=topic, **dados_dinamicos)
            print(f"[DEBUG] Analogia gerada: {analogia}")  # Log da analogia gerada
            development_parts.append(analogia)
            print(f"[DEBUG] development_parts após adição da analogia: {development_parts}")  # Log da lista
        
        # 5. REFLEXÃO PESSOAL (60% chance) - FORÇAR INCLUSÃO
        if True:  # Sempre incluir para garantir autenticidade
            template_reflexao = random.choice(templates_desenvolvimento["reflexoes"])
            print(f"[DEBUG] Template de reflexão selecionado: {template_reflexao}")
            reflexao = self._preencher_template(template_reflexao, topic=topic, **dados_dinamicos)
            print(f"[DEBUG] Reflexão gerada: {reflexao}")  # Log da reflexão gerada
            development_parts.append(reflexao)
            print(f"[DEBUG] development_parts após adição da reflexão: {development_parts}")  # Log da lista
        
        print(f"[DEBUG] development_parts antes da concatenação: {development_parts}")
        resultado = "\n\n".join(development_parts)
        print(f"[DEBUG] Resultado da concatenação do desenvolvimento: {resultado}")
        return resultado
    
    def _preencher_template(self, template: str, **kwargs) -> str:
        """
        Preencher template com conteúdo dinâmico
        Implementação baseada nas sugestões do especialista.
        """
        print(f"[DEBUG] Template selecionado: {template}")  # Log do template
        print(f"[DEBUG] Dados dinâmicos: {kwargs}")  # Log dos dados
        try:
            resultado = template.format(**kwargs)
            print(f"[DEBUG] Resultado do preenchimento: {resultado}")  # Log do resultado
            return resultado
        except KeyError as e:
            print(f"[DEBUG] Erro ao preencher template: {e}")  # Log de erro
            return template.format(topic=kwargs.get('topic', 'este assunto'), **kwargs)

    def _generate_modular_conclusion(self, topic: str) -> str:
        """
        ABORDAGEM MODULAR: Gerar conclusão usando templates autênticos
        Implementação baseada nas sugestões do especialista.
        """
        # Templates de conclusão conforme sugerido pelo especialista
        templates_conclusao = [
            f"E aí, o que vocês acham? {topic} é uma parada que vai impactar a vida de todos nós. Se isso ressonou com vocês, compartilha com quem precisa ouvir. Valeu, rapaziada! Tamo junto!",
            f"Qual a opinião de vocês sobre {topic}? É algo que mexe comigo de verdade e acho que vocês também vão se interessar. Comenta aí! Valeu, rapaziada! Tamo junto!",
            f"Entre nós, {topic} é uma questão séria que merece nossa atenção. E aí, o que vocês pensam sobre isso? Se você já teve alguma experiência, conta nos comentários! Valeu, rapaziada! Tamo junto!",
            f"Cara, {topic} é uma parada que vai mudar tudo e vocês precisam estar preparados. E aí, o que vocês acham? Comenta aí! Valeu, rapaziada! Tamo junto!",
            f"Olha só, rapaziada, {topic} é uma revolução silenciosa que está acontecendo agora. E aí, o que vocês pensam sobre isso? Se isso ressonou com vocês, compartilha com quem precisa ouvir. Valeu, rapaziada! Tamo junto!",
            "Faz sentido para vocês? Deixa nos comentários!",
            "Isso é só o começo, a revolução está apenas começando...",
            "E aí, o que vocês pensam sobre isso? Comenta aí! Valeu, rapaziada! Tamo junto!"
        ]
        
        return random.choice(templates_conclusao)

    def _validate_and_adjust_realtime(self, text: str, topic: str) -> str:
        """
        VALIDAÇÃO EM TEMPO REAL: Ajustar dinamicamente a autenticidade
        Implementação baseada nas sugestões do especialista.
        """
        # Verificar se o texto tem elementos autênticos suficientes
        authenticity_score = self._calculate_authenticity_score(text)
        
        # Se o score for baixo, adicionar elementos autênticos
        if authenticity_score < 70:
            text = self._add_missing_authentic_elements(text, topic)
        
        return text

    def _calculate_authenticity_score(self, text: str) -> float:
        """Calcular score de autenticidade em tempo real"""
        elements_found = {
            "histories": 0,
            "data": 0,
            "analogies": 0,
            "reflections": 0,
            "questions": 0,
            "exclamations": 0
        }
        
        # Detectar histórias pessoais
        if "amigo meu" in text.lower() or "história verídica" in text.lower():
            elements_found["histories"] = 1
        
        # Detectar dados específicos
        if any(word in text.lower() for word in ["fvg", "elon musk", "tesla", "10 milhões", "300 km", "5 bilhões"]):
            elements_found["data"] = 1
        
        # Detectar analogias
        if "casar com uma mulher feia" in text.lower() or "china é uma autocracia" in text.lower():
            elements_found["analogies"] = 1
        
        # Detectar reflexões
        if "impressionante" in text.lower() and "número de pessoas que me seguem" in text.lower():
            elements_found["reflections"] = 1
        
        # Detectar perguntas
        if any(phrase in text.lower() for phrase in ["sabe o que", "e aí", "faz sentido", "entendeu"]):
            elements_found["questions"] = 1
        
        # Detectar exclamações
        if "!" in text and any(word in text.lower() for word in ["impressionante", "demais", "pra caramba"]):
            elements_found["exclamations"] = 1
        
        # Calcular score
        total_elements = sum(elements_found.values())
        max_elements = len(elements_found)
        score = (total_elements / max_elements) * 100
        
        return score

    def _add_missing_authentic_elements(self, text: str, topic: str) -> str:
        """Adicionar elementos autênticos que estão faltando"""
        # Verificar quais elementos estão faltando e adicionar
        if "amigo meu" not in text.lower():
            # Adicionar história pessoal
            stories = [
                "Um amigo meu, história verídica, me contou que isso é impressionante.",
                "Cara, um amigo meu de confiança me falou uma coisa interessante sobre isso.",
                "E sabe o que que eu escutei aí na rua? É impressionante como as coisas mudaram."
            ]
            story = random.choice(stories)
            text = f"{text}\n\n{story}"
        
        if "impressionante" not in text.lower():
            # Adicionar reflexão
            reflections = [
                "Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
                "É impressionante como as coisas estão mudando rapidamente.",
                "Eh, cara, é impressionante o que está acontecendo por aí."
            ]
            reflection = random.choice(reflections)
            text = f"{text}\n\n{reflection}"
        
        return text

    def _fix_critical_issues(self, text: str) -> str:
        """
        CORREÇÃO FINAL: Apenas problemas críticos
        Implementação baseada nas sugestões do especialista.
        """
        import re
        
        # 1. Corrigir repetições excessivas
        text = re.sub(r'(\w+)\s+\1', r'\1', text)  # Remover palavras repetidas consecutivas
        
        # 2. Corrigir pontuação básica
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)  # Adicionar ponto antes de maiúscula
        
        # 3. Corrigir espaços duplos
        text = re.sub(r'\s+', ' ', text)
        
        # 4. Capitalizar tópico
        text = re.sub(r'\bmpc na ia\b', 'MPC na IA', text, flags=re.IGNORECASE)
        
        return text

    def _create_main_content(self, topic: str) -> str:
        """Create the main content section using storytelling patterns."""
        
        # ESTRUTURA COERENTE E LÓGICA
        content_parts = []
        
        # 1. INTRODUÇÃO DO TEMA (sempre presente)
        intro_patterns = [
            f"Eh, por que que eu digo isso, rapaziada? {topic} é uma parada que mexe comigo de verdade.",
            f"Cara, {topic} é algo que eu venho acompanhando há um tempo e preciso compartilhar com vocês.",
            f"Olha só, rapaziada, {topic} é um tema que está mudando tudo e vocês precisam saber disso.",
            f"Sabe o que é interessante? {topic} é uma revolução silenciosa que está acontecendo agora.",
            f"Vamos olhar esse ano. {topic} está transformando a forma como pensamos sobre tecnologia."
        ]
        intro = random.choice(intro_patterns)
        content_parts.append(intro)
        
        # 2. HISTÓRIA PESSOAL OU EXPERIÊNCIA (70% chance)
        if random.random() < 0.7:
            story_patterns = [
                f"Um amigo meu, história real, me contou que {topic} é tipo igual você casar com uma mulher feia. Você vai ter uma mulher feia, mas vai descobrir que precisa de uma outra.",
                f"Sabe o que é engraçado? Eu estava aqui em Barcelona quando descobri que {topic} é muito mais complexo do que eu imaginava.",
                f"Cara, é impressionante como {topic} está mudando a vida das pessoas. Um colega meu começou a usar e os resultados são surpreendentes.",
                f"Eh, por que que eu digo isso? Porque {topic} não é unanimidade, mas quando funciona, é impressionante.",
                f"Olha só, rapaziada, {topic} é uma parada que me deixa pensativo, sabe? É algo que vale a pena refletir."
            ]
            story = random.choice(story_patterns)
            content_parts.append(story)
        
        # 3. DESENVOLVIMENTO TÉCNICO (sempre presente)
        technical_patterns = [
            f"O que mais me impressiona é como {topic} está revolucionando a forma como pensamos sobre tecnologia.",
            f"Cara, {topic} representa uma mudança fundamental na forma como as coisas funcionam.",
            f"É impressionante como {topic} está sendo aplicado em diferentes setores e os resultados são surpreendentes.",
            f"O interessante é que {topic} não é apenas uma tendência, é uma transformação real que está acontecendo agora.",
            f"Entre nós, {topic} é uma parada que vai mudar tudo e vocês precisam estar preparados."
        ]
        technical = random.choice(technical_patterns)
        content_parts.append(technical)
        
        # 4. DADOS OU EVIDÊNCIAS (50% chance)
        if random.random() < 0.5:
            data_patterns = [
                f"Vamos olhar esse ano. {topic} está crescendo de forma impressionante e os números não mentem.",
                f"Olha só, rapaziada, {topic} está sendo adotado por empresas ao redor do mundo e os resultados são surpreendentes.",
                f"Cara, é impressionante como {topic} está transformando diferentes indústrias e criando novas oportunidades.",
                f"O que mais me chama atenção é como {topic} está sendo implementado em diferentes contextos e os resultados são consistentes.",
                f"É notável como {topic} está evoluindo rapidamente e criando novas possibilidades que antes eram impensáveis."
            ]
            data = random.choice(data_patterns)
            content_parts.append(data)
        
        # 5. REFLEXÃO PESSOAL (60% chance)
        if random.random() < 0.6:
            reflection_patterns = [
                f"Cara, quando penso em {topic}, fico realmente reflexivo sobre o futuro que estamos construindo.",
                f"É algo que mexe comigo de verdade, sabe? {topic} é uma parada que vai impactar a vida de todos nós.",
                f"Entre nós, {topic} é uma questão séria que merece nossa atenção e reflexão.",
                f"Olha só, rapaziada, {topic} é uma parada que vai mudar tudo e vocês precisam estar preparados.",
                f"É impressionante como {topic} está transformando a forma como pensamos sobre o mundo."
            ]
            reflection = random.choice(reflection_patterns)
            content_parts.append(reflection)
        
        return "\n\n".join(content_parts)

    def _create_conclusion(self, topic: str) -> str:
        """Create conclusion using patterns from the analysis."""
        
        # CONCLUSÕES COERENTES E LÓGICAS
        conclusion_patterns = [
            f"E aí, o que vocês acham? {topic} é uma parada que vai impactar a vida de todos nós. Se isso ressonou com vocês, compartilha com quem precisa ouvir. Valeu, rapaziada! Tamo junto!",
            f"Qual a opinião de vocês sobre {topic}? É algo que mexe comigo de verdade e acho que vocês também vão se interessar. Comenta aí! Valeu, rapaziada! Tamo junto!",
            f"Entre nós, {topic} é uma questão séria que merece nossa atenção. E aí, o que vocês pensam sobre isso? Se você já teve alguma experiência, conta nos comentários! Valeu, rapaziada! Tamo junto!",
            f"Cara, {topic} é uma parada que vai mudar tudo e vocês precisam estar preparados. E aí, o que vocês acham? Comenta aí! Valeu, rapaziada! Tamo junto!",
            f"Olha só, rapaziada, {topic} é uma revolução silenciosa que está acontecendo agora. E aí, o que vocês pensam sobre isso? Se isso ressonou com vocês, compartilha com quem precisa ouvir. Valeu, rapaziada! Tamo junto!"
        ]
        
        conclusion = random.choice(conclusion_patterns)
        return conclusion

    def _apply_humanization_rules(self, text: str) -> str:
        """Apply comprehensive humanization rules to the text."""
        # Apply sentence length rules
        text = self._apply_sentence_length_rules(text)
        
        # Apply colloquial expressions
        text = self._apply_colloquial_expressions(text)
        
        # Apply transition words
        text = self._apply_transition_words(text)
        
        # Apply rhetorical questions
        text = self._apply_rhetorical_questions(text)
        
        # Apply power words
        text = self._apply_power_words(text)
        
        # Remove banned words
        text = self._remove_banned_words(text)
        
        return text

    def _apply_sentence_length_rules(self, text: str) -> str:
        """Apply sentence length rules from the configuration."""
        sentences = text.split('. ')
        processed_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > self.max_words:
                # Split long sentences
                mid_point = len(words) // 2
                first_part = ' '.join(words[:mid_point])
                second_part = ' '.join(words[mid_point:])
                processed_sentences.append(f"{first_part}. {second_part}")
            else:
                processed_sentences.append(sentence)
        
        return '. '.join(processed_sentences)

    def _apply_colloquial_expressions(self, text: str) -> str:
        """Apply colloquial expressions based on frequency analysis."""
        # High frequency expressions (add more often)
        if random.random() < 0.3:  # 30% chance
            text = text.replace("você", "cara, você", 1)
        
        if random.random() < 0.2:  # 20% chance
            text += " Entendeu?"
        
        if random.random() < 0.15:  # 15% chance
            text += " Beleza?"
        
        return text

    def _apply_transition_words(self, text: str) -> str:
        """Apply transition words based on frequency analysis."""
        # Add high frequency transitions
        if random.random() < 0.4:  # 40% chance
            transitions = self.transition_words["high_frequency"]
            transition = random.choice(transitions)
            text = f"{transition} {text}"
        
        return text

    def _apply_rhetorical_questions(self, text: str) -> str:
        """Apply rhetorical questions based on the rules."""
        if random.random() < 0.3:  # 30% chance
            questions = self.prompt_template["rhetorical_questions"]["confirmation"]
            question = random.choice(questions)
            text += f" {question}"
        
        return text

    def _apply_power_words(self, text: str) -> str:
        """Apply power words to increase engagement."""
        for word in self.power_words:
            if random.random() < 0.1:  # 10% chance per word
                text = text.replace("pode", f"{word}", 1)
                break
        
        return text

    def _remove_banned_words(self, text: str) -> str:
        """Remove banned words from the text."""
        text_lower = text.lower()
        for banned_word in self.banned_words:
            if banned_word in text_lower:
                # Replace with alternative
                alternatives = {
                    "compre já": "conheça",
                    "oferta imperdível": "oportunidade especial",
                    "clique aqui": "acesse",
                    "não perca": "confira",
                    "última chance": "oportunidade"
                }
                if banned_word in alternatives:
                    text = text.replace(banned_word, alternatives[banned_word])
        
        return text

    def validate_text(self, text: str) -> bool:
        """
        Validate if the text meets the hard gates and writing rules.
        Now uses comprehensive validation based on the enhanced rules.

        Args:
            text (str): The text to validate.

        Returns:
            bool: True if the text meets all rules, False otherwise.
        """
        # Check banned words
        text_lower = text.lower()
        for banned_word in self.banned_words:
            if banned_word in text_lower:
                return False
        
        # Check sentence length
        sentences = text.split('.')
        for sentence in sentences:
            words = sentence.split()
            if len(words) > self.max_words:
                return False
        
        # Check required elements from hard gates
        required_elements = self.hard_gates.get("required_elements", {})
        
        if required_elements.get("second_person", False):
            if "você" not in text_lower and "cara" not in text_lower:
                return False
        
        if required_elements.get("sensory_detail", False):
            sensory_words = ["imagine", "sinta", "veja", "ouça", "cheiro", "sabor"]
            if not any(word in text_lower for word in sensory_words):
                return False
        
        if required_elements.get("mini_anecdote", False):
            anecdote_indicators = ["eu quando", "uma vez", "essas dias", "lembro que"]
            if not any(phrase in text_lower for phrase in anecdote_indicators):
                return False
        
        # Check style consistency
        style_consistency = self.hard_gates.get("style_consistency", {})
        min_similarity = style_consistency.get("min_similarity_score", 0.85)
        
        # Simple similarity check based on colloquial expressions
        colloquial_count = sum(1 for expr in self.colloquial_expressions["ultra_high"] 
                              if expr in text_lower)
        total_words = len(text.split())
        similarity_score = colloquial_count / max(total_words, 1)
        
        if similarity_score < min_similarity:
            return False
        
        return True

    def get_writing_metrics(self, text: str) -> Dict[str, Any]:
        """
        Get detailed metrics about the text based on the writing rules.
        
        Args:
            text (str): The text to analyze.
            
        Returns:
            Dict[str, Any]: Metrics about the text.
        """
        words = text.split()
        sentences = text.split('.')
        
        metrics = {
            "total_words": len(words),
            "total_sentences": len(sentences),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "max_sentence_length": max(len(s.split()) for s in sentences) if sentences else 0,
            "colloquial_expressions_count": sum(1 for expr in self.colloquial_expressions["ultra_high"] 
                                              if expr in text.lower()),
            "rhetorical_questions_count": text.count('?'),
            "second_person_usage": text.lower().count("você") + text.lower().count("cara"),
            "power_words_count": sum(1 for word in self.power_words if word in text.lower()),
            "banned_words_found": [word for word in self.banned_words if word in text.lower()],
            "formality_score": self._calculate_formality_score(text),
            "readability_score": self._calculate_readability_score(text)
        }
        
        return metrics

    def _calculate_formality_score(self, text: str) -> float:
        """Calculate formality score based on the text content."""
        formal_indicators = ["portanto", "consequentemente", "adicionalmente", "furthermore"]
        informal_indicators = ["cara", "beleza", "entendeu", "tipo", "putz"]
        
        formal_count = sum(1 for word in formal_indicators if word in text.lower())
        informal_count = sum(1 for word in informal_indicators if word in text.lower())
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.5
        
        formality_score = (formal_count - informal_count) / total_words
        return max(0, min(1, formality_score + 0.5))  # Normalize to 0-1

    def _calculate_readability_score(self, text: str) -> float:
        """Calculate a simple readability score."""
        words = text.split()
        sentences = text.split('.')
        
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
    
    def _load_problematic_patterns(self) -> Dict[str, List[str]]:
        """Carregar padrões problemáticos que devem ser EVITADOS"""
        return {
            # SISTEMA DINÂMICO - NÃO MAIS LISTA FIXA
            "simplicidade_artificial": [],  # Será detectada dinamicamente
            
            # PADRÕES QUE CAUSAM "FOCO ESPECULATIVO"
            "foco_especulativo": [
                "é tipo igual",
                "pode impactar",
                "seria interessante",
                "pode ser",
                "talvez",
                "provavelmente",
                "é possível que",
                "pode acontecer",
                "seria bom",
                "pode ser que"
            ],
            
            # PADRÕES QUE CAUSAM "CALOR DESAPEGADO"
            "calor_desapegado": [
                "seria fascinante conhecer",
                "merece uma reflexão profunda",
                "diferentes perspectivas e experiências",
                "Esta questão complexa",
                "Até a próxima",
                "considerando essa perspectiva",
                "É realmente impressionante como",
                "é interessante observar",
                "transformações profundas",
                "impacto significativo"
            ],
            
            # PADRÕES QUE CAUSAM "ESTRUTURAS FORMALS"
            "estruturas_formais": [
                "Quando analisamos",
                "observamos que",
                "representa um tema",
                "de grande relevância",
                "O resultado depende de uma complexa interação",
                "considerando que",
                "é importante notar que",
                "deve-se considerar que"
            ]
        }
    
    def _load_human_patterns(self) -> Dict[str, List[str]]:
        """Carregar padrões humanos que devem ser USADOS"""
        return {
            # PADRÕES DE CALOR EMOCIONAL AUTÊNTICO
            "calor_emocional": [
                "Cara, quando penso nisso, fico realmente reflexivo",
                "Isso me toca profundamente, você sabe?",
                "Confesso que fiquei genuinamente impressionado",
                "Fiquei com uma sensação estranha quando vi",
                "É algo que mexe comigo de verdade"
            ],
            
            # PADRÕES DE PROXIMIDADE EMOCIONAL
            "proximidade_emocional": [
                "Entre nós, isso é uma questão séria",
                "Vou compartilhar algo pessoal com vocês",
                "Vocês me entendem, né?",
                "A gente já passou por situações assim",
                "Nós sabemos que isso é complicado"
            ],
            
            # PADRÕES DE LINGUAGEM CORPORAL TEXTUAL
            "linguagem_corporal": [
                "Fiquei com arrepios quando ele explicou",
                "Me levantei da cadeira de tanta emoção",
                "Bati na mesa de tanta empolgação",
                "Fiquei com frio na barriga",
                "Meus olhos brilharam quando vi"
            ],
            
            # PADRÕES DE HESITAÇÕES NATURAIS
            "hesitacoes_naturais": [
                "É... como posso explicar isso...",
                "Não, não é exatamente isso... é mais como",
                "Ele falou... espera, deixe-me reformular",
                "Acho que... não, tenho certeza absoluta",
                "Deixe-me pensar em como dizer isso melhor"
            ],
            
            # PADRÕES DE REFERÊNCIAS CULTURAIS
            "referencias_culturais": [
                "Aqui em Barcelona, onde estou morando",
                "Lá no Brasil, a situação é diferente",
                "Meu amigo João, que mora em São Paulo",
                "Minha mãe sempre dizia",
                "Naquela época que morei no Rio"
            ],
            
            # PADRÕES DE VARIAÇÃO DE VELOCIDADE
            "variacao_velocidade": [
                "E aí, rapidinho, ele me explicou...",
                "E aí... devagar... ele foi me contando",
                "E aí... (pausa)... ele revelou",
                "Rápido, devagar, rápido - assim foi a conversa",
                "De repente... parou tudo"
            ],
            
            # PADRÕES DE ENTONAÇÃO TEXTUAL
            "entonacao_textual": [
                "Compreendem a questão?",
                "Nossa! Que descoberta!",
                "Entre nós...",
                "CARAMBA! Que revelação!",
                "Ah, agora entendi!"
            ]
        }
    
    def _prevent_ai_patterns(self, text: str) -> str:
        """Prevenir padrões de IA no texto gerado usando perfil Ryan"""
        corrected_text = text
        
        # NOVA ESTRATÉGIA: DETECÇÃO DINÂMICA DE SIMPLICIDADE ARTIFICIAL
        corrected_text = self._combat_artificial_simplicity_dynamic(corrected_text)
        
        # Usar padrões anti-IA do perfil Ryan se disponível
        if hasattr(self, 'ryan_profile') and 'signature_patterns' in self.ryan_profile:
            anti_patterns = self.ryan_profile['signature_patterns'].get('anti_ai_patterns', {})
            
            # Aplicar opiniões assertivas (combate foco especulativo)
            if 'assertive_opinions' in anti_patterns:
                for pattern in anti_patterns['assertive_opinions']:
                    if "pode ser" in corrected_text.lower() or "talvez" in corrected_text.lower():
                        corrected_text = corrected_text.replace("pode ser", "é")
                        corrected_text = corrected_text.replace("talvez", "tenho certeza que")
            
            # Aplicar interrupções naturais (combate precisão mecânica)
            if 'natural_interruptions' in anti_patterns:
                interruptions = anti_patterns['natural_interruptions']
                if len(interruptions) > 0:
                    import random
                    interruption = random.choice(interruptions)
                    # Adicionar interrupção em posição estratégica
                    if "é impressionante" in corrected_text.lower():
                        corrected_text = corrected_text.replace("é impressionante", f"{interruption} é impressionante")
            
            # Aplicar gramática criativa (combate falta de criatividade)
            if 'creative_grammar' in anti_patterns:
                creative_patterns = anti_patterns['creative_grammar']
                if len(creative_patterns) > 0:
                    import random
                    creative = random.choice(creative_patterns)
                    # Adicionar em posição estratégica
                    if "isso é" in corrected_text.lower():
                        corrected_text = corrected_text.replace("isso é", f"{creative} isso é")
            
            # Aplicar proximidade emocional (combate tom impessoal)
            if 'emotional_proximity' in anti_patterns:
                emotional_patterns = anti_patterns['emotional_proximity']
                if len(emotional_patterns) > 0:
                    import random
                    emotional = random.choice(emotional_patterns)
                    # Adicionar proximidade emocional
                    if "nós sabemos" in corrected_text.lower():
                        corrected_text = corrected_text.replace("nós sabemos", f"{emotional}, nós sabemos")
            
            # Aplicar variação natural (combate formalidade robótica)
            if 'natural_variation' in anti_patterns:
                variation_patterns = anti_patterns['natural_variation']
                if len(variation_patterns) > 0:
                    import random
                    variation = random.choice(variation_patterns)
                    # Adicionar variação de velocidade
                    if "ele falou" in corrected_text.lower():
                        corrected_text = corrected_text.replace("ele falou", f"{variation}")
        
        # Fallback para padrões problemáticos básicos
        for category, patterns in self.problematic_patterns.items():
            for pattern in patterns:
                if pattern.lower() in corrected_text.lower():
                    # Substituir por versão humana
                    if "Galera, isso me deixa pensativo, sabe?" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Cara, quando penso nisso, fico realmente reflexivo, você sabe?")
                    elif "Vou te contar uma coisa, é tipo igual" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Vou compartilhar uma perspectiva interessante:")
                    elif "Arrepiei aqui quando ele falou" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Fiquei genuinamente impressionado quando ele explicou")
                    elif "Olha só, pessoal, Isso é, isso é, isso é incrível!" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Observem, pessoal, isso é realmente impressionante!")
                    elif "Acho que... não, tenho certeza melhor não ter" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Acho que... não, tenho certeza absoluta que é melhor não ter")
                    elif "Sabe o que é isso?, Cara, galera" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Compreendem a questão? Pessoal")
                    elif "é tipo igual" in pattern:
                        corrected_text = corrected_text.replace(pattern, "é similar a")
                    elif "Muito mesmo." in pattern:
                        corrected_text = corrected_text.replace(pattern, "Extremamente significativo.")
                    elif "Nossa!!" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Impressionante!")
                    elif "Cara, vamos lá..." in pattern:
                        corrected_text = corrected_text.replace(pattern, "Vamos analisar esta questão...")
                    elif "E aí, galera" in pattern:
                        corrected_text = corrected_text.replace(pattern, "Pessoal")
        
        return corrected_text
    
    def _add_human_patterns(self, text: str) -> str:
        """Adicionar padrões humanos ao texto"""
        # Adicionar calor emocional se não estiver presente
        if not any(pattern.lower() in text.lower() for pattern in self.human_patterns["calor_emocional"]):
            # Adicionar calor emocional em posição estratégica
            if "Isso me deixa pensativo" in text:
                text = text.replace("Isso me deixa pensativo", "Cara, quando penso nisso, fico realmente reflexivo")
        
        # Adicionar proximidade emocional se não estiver presente
        if not any(pattern.lower() in text.lower() for pattern in self.human_patterns["proximidade_emocional"]):
            if "Nós sabemos que isso é complicado" in text:
                text = text.replace("Nós sabemos que isso é complicado", "Entre nós, isso é uma questão séria")
        
        return text
    
    def _combat_artificial_simplicity_dynamic(self, text: str) -> str:
        """
        NOVA ESTRATÉGIA: ELIMINAÇÃO DE SIMPLICIDADE ARTIFICIAL
        
        Baseado nas dicas do especialista:
        1. TRANSFORMAR estruturas "X é Y" em estruturas complexas
        2. ELIMINAR simplicidade subjacente (não apenas adicionar)
        3. QUEBRAR padrões previsíveis de IA
        """
        import random
        import re
        
        corrected_text = text
        
        # 1. ELIMINAR ESTRUTURAS "X é Y" SIMPLES
        corrected_text = self._eliminate_simple_structures(corrected_text)
        
        # 2. TRANSFORMAR CONJUNÇÕES COLOCIAIS
        corrected_text = self._transform_colloquial_conjunctions(corrected_text)
        
        # 3. APLICAR INVERSÃO E INTERRUPÇÃO
        corrected_text = self._apply_inversion_and_interruption(corrected_text)
        
        # 4. ADICIONAR PERGUNTAS RETÓRICAS E EXCLAMAÇÕES
        corrected_text = self._add_rhetorical_questions_and_exclamations(corrected_text)
        
        # 5. ADICIONAR CONTEXTO E EXEMPLOS (DICA 2 DO ESPECIALISTA)
        corrected_text = self._add_context_and_examples(corrected_text)
        
        # 6. ADICIONAR PERGUNTAS RETÓRICAS E EXCLAMAÇÕES (DICA 3 DO ESPECIALISTA)
        corrected_text = self._add_rhetorical_questions_and_exclamations_advanced(corrected_text)
        
        # 7. CORRIGIR PROBLEMAS ESPECÍFICOS
        corrected_text = self._fix_specific_problems(corrected_text)
        
        return corrected_text
    
    def _eliminate_simple_structures(self, text: str) -> str:
        """
        ELIMINAR estruturas "X é Y" simples transformando-as em estruturas complexas
        
        Baseado na dica do especialista e no estilo natural do Ryan:
        Antes: "ICP na IA é uma revolução silenciosa"
        Depois: "Quando analisamos o ICP na IA, fica claro que não se trata apenas de uma tendência, mas de uma revolução silenciosa em curso"
        """
        import re
        
        # Padrões mais específicos para evitar transformações inadequadas
        # EXCLUIR aberturas do Ryan das transformações
        simple_patterns = [
            # Padrão "X é uma revolução/transformação" (mais específico, excluir aberturas)
            (r'(?<!Sabe o que é )(?<!E aí, o que )(?<!Salve rapaziada, )(\w+(?:\s+\w+)*)\s+é\s+uma\s+(revolução|transformação|mudança|inovação)(?:\s+\w+)*', 
             r'Quando analisamos \1, fica claro que não se trata apenas de uma tendência, mas de uma \2 em curso'),
            
            # Padrão "X é uma parada que" (estilo Ryan, excluir aberturas)
            (r'(?<!Sabe o que é )(?<!E aí, o que )(?<!Salve rapaziada, )(\w+(?:\s+\w+)*)\s+é\s+uma\s+parada\s+que\s+(\w+(?:\s+\w+)*)', 
             r'Para quem entende do assunto, \1 representa um divisor de águas que \2'),
            
            # Padrão "X é interessante/impressionante" (mais específico, excluir aberturas)
            (r'(?<!Sabe o que é )(?<!E aí, o que )(?<!Salve rapaziada, )(\w+(?:\s+\w+){2,})\s+é\s+(interessante|impressionante|notável)(?:\s+\w+)*', 
             r'O que realmente me chama atenção é como \1 se mostra \2, especialmente considerando'),
            
            # Padrão "X é uma questão/assunto" (mais específico, excluir aberturas)
            (r'(?<!Sabe o que é )(?<!E aí, o que )(?<!Salve rapaziada, )(\w+(?:\s+\w+)*)\s+é\s+uma\s+(questão|assunto|tema)(?:\s+\w+)*', 
             r'Entre nós, \1 representa uma \2 séria que merece nossa atenção'),
            
            # Padrão "X é algo que" (mais específico, excluir aberturas)
            (r'(?<!Sabe o que é )(?<!E aí, o que )(?<!Salve rapaziada, )(\w+(?:\s+\w+)*)\s+é\s+algo\s+que\s+(\w+(?:\s+\w+)*)', 
             r'Confesso que \1 me deixa pensativo, sabe? É algo que \2'),
        ]
        
        for pattern, replacement in simple_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _transform_colloquial_conjunctions(self, text: str) -> str:
        """
        TRANSFORMAR conjunções coloquiais por conectores naturais
        
        Baseado na dica do especialista e no estilo natural do Ryan:
        Antes: "O que mais me impressiona é que olha só, rapaziada, ICP na IA é uma parada que me deixa pensativo, sabe"
        Depois: "Confesso que fico pensativo ao analisar o ICP na IA. Não é só uma tendência; é uma mudança que está redefinindo o jogo"
        """
        import random
        import re
        
        # Substituições mais específicas e contextuais
        conjunction_replacements = [
            # "O que mais me impressiona é que" → "Confesso que" (mais específico)
            (r'O que mais me impressiona é que', 'Confesso que'),
            
            # "Olha só, rapaziada" → "Para quem entende do assunto" (mais específico)
            (r'Olha só, rapaziada', 'Para quem entende do assunto'),
            
            # "é uma parada que" → "representa um divisor de águas que" (mais específico)
            (r'é uma parada que', 'representa um divisor de águas que'),
            
            # "sabe" → "você sabe" (mais específico, não no meio de palavras)
            (r'\bsabe\b', 'você sabe'),
            
            # "Cara, é" → "Entre nós," (mais específico)
            (r'Cara, é', 'Entre nós,'),
            
            # "Galera, é" → "Pessoal," (mais específico)
            (r'Galera, é', 'Pessoal,'),
            
            # "E aí, o que" → "E aí, o que" (manter estilo Ryan)
            (r'E aí, o que', 'E aí, o que'),
            
            # "Sabe o que é interessante?" → "Sabe o que é interessante?" (manter estilo Ryan)
            (r'Sabe o que é interessante\?', 'Sabe o que é interessante?'),
        ]
        
        for pattern, replacement in conjunction_replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_inversion_and_interruption(self, text: str) -> str:
        """
        APLICAR inversão e interrupção de frases
        
        Baseado na dica do especialista e no estilo natural do Ryan:
        Antes: "ICP na IA é impressionante"
        Depois: "Impressionante mesmo é como o ICP na IA está mudando tudo"
        """
        import random
        import re
        
        # Padrões mais específicos para inversão (evitar transformações inadequadas)
        inversion_patterns = [
            # "X é impressionante/incrível" → "Impressionante mesmo é X"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+(impressionante|incrível|notável)', 
             r'\2 mesmo é \1'),
            
            # "X é uma revolução" → "Uma revolução mesmo é X"
            (r'(\w+(?:\s+\w+)*)\s+é\s+uma\s+(revolução|transformação|mudança)', 
             r'Uma \2 mesmo é \1'),
        ]
        
        for pattern, replacement in inversion_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Adicionar interrupções com travessões (mais naturais e contextuais)
        interruption_phrases = [
            "— e isso é fato —",
            "— e não estou exagerando —", 
            "— até padaria tá usando —",
            "— e eu falo por experiência —",
            "— e olha que não é pouco —",
            "— e olha que não é brincadeira —",
            "— e isso é real —"
        ]
        
        # Adicionar interrupção em frases longas (mais criterioso)
        sentences = text.split('. ')
        processed_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            # Só adicionar interrupção em frases realmente longas e que não sejam aberturas do Ryan
            if (len(words) > 12 and 
                not sentence.startswith(('Salve rapaziada', 'E aí', 'Olha só')) and
                'é' in sentence.lower()):
                
                # Encontrar posição natural para interrupção (após vírgula ou antes de "que")
                mid_point = len(words) // 2
                interruption = random.choice(interruption_phrases)
                words.insert(mid_point, interruption)
                sentence = ' '.join(words)
            
            processed_sentences.append(sentence)
        
        return '. '.join(processed_sentences)
    
    def _add_rhetorical_questions_and_exclamations(self, text: str) -> str:
        """
        ADICIONAR perguntas retóricas e exclamações
        
        Baseado na dica do especialista e no estilo natural do Ryan:
        Antes: "ICP na IA é algo que está acontecendo agora"
        Depois: "Você já parou para pensar no impacto do ICP na IA? Está acontecendo agora, e poucas pessoas perceberam"
        """
        import random
        import re
        
        # Transformar afirmações em perguntas retóricas (mais específicas)
        question_patterns = [
            # "X é uma revolução/transformação" → "Você já parou para pensar em X? É uma revolução"
            (r'(\w+(?:\s+\w+)*)\s+é\s+uma\s+(revolução|transformação|mudança)', 
             r'Você já parou para pensar em \1? É uma \2'),
            
            # "X é interessante" → "O que você acha de X? É interessante"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+interessante', 
             r'O que você acha de \1? É interessante'),
            
            # "X é impressionante" → "Sabe o que é impressionante? X"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+impressionante', 
             r'Sabe o que é impressionante? \1'),
        ]
        
        for pattern, replacement in question_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Adicionar exclamações (mais específicas e naturais)
        exclamation_patterns = [
            # "X é incrível" → "X é incrível demais!"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+incrível', r'\1 é incrível demais!'),
            
            # "X é impressionante" → "X é impressionante pra caramba!"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+impressionante', r'\1 é impressionante pra caramba!'),
            
            # "X é notável" → "X é notável mesmo!"
            (r'(\w+(?:\s+\w+){2,})\s+é\s+notável', r'\1 é notável mesmo!'),
        ]
        
        for pattern, replacement in exclamation_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_context_and_examples(self, text: str) -> str:
        """
        ADICIONAR contexto e exemplos para aumentar complexidade e naturalidade
        
        Baseado na dica 2 do especialista e no estilo autêntico do Ryan Santos:
        - Histórias pessoais ou casos reais
        - Detalhes específicos (números, nomes, lugares)
        - Comparações com situações cotidianas
        - Explicações adicionais que vão além do óbvio
        """
        import random
        import re
        
        # 1. HISTÓRIAS PESSOAIS E CASOS REAIS (100% autênticas do Ryan Santos)
        personal_stories = [
            "Um amigo meu, história verídica, amigo meu, ele eu tava tomando café da manhã numa padaria e chegou um uma pessoa que eu nunca vi na minha vida e falou: 'Você é o Sérgio Habibe, eu sigo você. Eu aconteceu comigo exatamente o que você conta'.",
            "Um amigo meu que foi muito comedor, esse amigo meu, ele mudou o estilo de vida. Antes esse amigo meu era assim, ó. O problema que esse amigo meu encontrou, ele não conseguia mais comer.",
            "Um amigo meu de muitíssima confiança, cara, era um amigo meu de muitíssima confiança, me contou uma história de amigo meu, não. Eu mesmo fui.",
            "E sabe o que que eu escutei aí na rua? É impressionante como os russos são organizados.",
            "E é impressionante, eu fui ver os comentários, é impressionante o número de pessoas que me seguem.",
            "E olha que impressionante. Então, a gente vê que o problema não é só aqui no Brasil.",
            "Eh, cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço."
        ]
        
        # 2. DETALHES ESPECÍFICOS E DADOS (100% autênticos do Ryan Santos)
        specific_data = [
            "A FGV e do Insper, cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "Porque sem subsídio, o próprio Elon Musk, sem subsídio a Tesla não seria nem 10% do que é.",
            "O ano passado se vendeu no planeta Terra 10 milhões de carros elétricos. E aí, por que que você acha que vai cair?",
            "O carro elétrico, o carro com o carro que a gente vende tem 300 km de autonomia. O Bed Dolphin ou o Milid Dolphin tem 300 350 km de autonomia. Na estrada tem 200 e pouco. 230 240.",
            "Os Estados Unidos, o Biden, tá, você digita, você vê, colocou uma linha de 5 bilhões de dólares para colocar carregador, uma estrutura de carregamento a cada 40 milhas em todas as estradas.",
            "É impressionante como Hollywood consegue fazer filmes que parecem reais, mas são super fakes. É impressionante.",
            "É impressionante como eles têm uma gangue de pessoas que trabalham pra eles, é impressionante quando as pessoas me param na rua.",
            "O Tesla, o Tesla mais básico, ele é um ativo. Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "Eu aluguei um Tesla Play. O Tesla, o Tesla mais básico, ele é um ativo. Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "Já dirigi Tesla, aluguei Tesla no Brasil. O Tesla, o Tesla mais básico, ele é um ativo. Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço."
        ]
        
        # 3. COMPARAÇÕES E ANALOGIAS (100% autênticas do Ryan Santos)
        analogies = [
            "É tipo igual você casar com uma mulher feia, você vai ter uma mulher feia, mas você vai precisar de uma outra. Então melhor não ter aquela feia.",
            "A China é uma autocracia. Que que é uma autocracia? Alguém manda, todo mundo obedece. Lá o governo fala: 'Eu vou pôr 1 milhão de carregador nos próximos do anos.' Eles colocam 1 milhão de carregador nos próximos do anos porque alguém decidiu e todo mundo obedece.",
            "É impressionante como Hollywood consegue fazer filmes que parecem reais, mas são super fakes. É impressionante.",
            "É impressionante como eles têm uma gangue de pessoas que trabalham pra eles, é impressionante quando as pessoas me param na rua.",
            "Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "É impressionante como eu parei de gastar dinheiro com coisas que não precisava.",
            "É impressionante como o respeito maior vem das pessoas que não me conhecem."
        ]
        
        # 4. CENÁRIOS "E SE..." E EXEMPLOS PRÁTICOS (100% autênticos do Ryan Santos)
        scenarios = [
            "E se você pega, por exemplo, mano, o irmão da Carol Dias não parece o Neymar Mato Grosso? Neymar Mato Grosso na dos secos e molhados.",
            "E se você seguir regras de mercado, oferta e demanda, não faz sentido colocar tantos carregadores aí, porque a conta não fecha.",
            "E se ele pode operar hospitais com mais baixo custo do que ele pode hoje e ainda ganhar um dinheirinho com a pessoa",
            "E se você parar para pensar, a mulher normal não vai chegar em homem. A mulher bonita, atraente, não vai chegar em homem.",
            "E se estão consumindo. E se estão consumindo, a gente vê que o problema não é só aqui no Brasil.",
            "E se o governo não banca todo mundo. E se o governo não banca todo mundo, a gente vê que o problema não é só aqui no Brasil.",
            "E se eles não estão circulando na rua, a gente vê que o problema não é só aqui no Brasil.",
            "E se você olhar aí a Bolsonarista influente. E se é se é Bolsonarista influente, a gente vê que o problema não é só aqui no Brasil.",
            "E se você for para uma escola e faculdade muito menos. E aí o que que acontece? Ele vira um alvo para mulheres que chegam nele.",
            "E se ele fosse solteiro, ele ia para uma escola e faculdade muito menos. E aí o que que acontece? Ele vira um alvo para mulheres que chegam nele."
        ]
        
        # 5. REFLEXÕES PESSOAIS E OPINIÕES (100% autênticas do Ryan Santos)
        personal_reflections = [
            "Cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "É impressionante como eu parei de gastar dinheiro com coisas que não precisava.",
            "É impressionante como o respeito maior vem das pessoas que não me conhecem.",
            "Eh, cara, é impressionante o número de pessoas que me seguem e não sabem nem o que eu faço.",
            "E é impressionante, eu fui ver os comentários, é impressionante o número de pessoas que me seguem.",
            "E olha que impressionante. Então, a gente vê que o problema não é só aqui no Brasil.",
            "E sabe o que que eu escutei aí na rua? É impressionante como os russos são organizados."
        ]
        
        # Aplicar adições contextuais de forma mais inteligente
        sentences = text.split('. ')
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            enhanced_sentences.append(sentence)
            
            # Adicionar contexto em pontos estratégicos (condição mais flexível)
            if i % 2 == 0 and len(sentence) > 30:  # A cada 2 frases, frases maiores que 30 chars
                # Detectar se a frase menciona IA ou temas relacionados
                if any(keyword in sentence.lower() for keyword in ["ia", "inteligência artificial", "tecnologia", "revolução", "mudança", "transformação", "mpc"]):
                    # Escolher tipo de contexto baseado no conteúdo
                    if any(word in sentence.lower() for word in ["revolução", "mudança", "transformação"]):
                        context = random.choice(personal_stories)
                    elif any(word in sentence.lower() for word in ["empresas", "negócio", "mercado", "economia", "produtividade", "custos"]):
                        context = random.choice(specific_data)
                    elif any(word in sentence.lower() for word in ["fácil", "simples", "usar", "funciona", "como"]):
                        context = random.choice(analogies)
                    else:
                        context = random.choice(scenarios)
                    
                    enhanced_sentences.append(context)
        
        # Adicionar dados específicos adicionais (forçar adição)
        if len(enhanced_sentences) > 3:
            # Adicionar dados específicos em posições estratégicas
            data_positions = [1, 3, 5]  # Posições para adicionar dados
            for pos in data_positions:
                if pos < len(enhanced_sentences):
                    specific_data_item = random.choice(specific_data)
                    enhanced_sentences.insert(pos, specific_data_item)
        
        # Adicionar reflexão pessoal no final (sempre)
        if enhanced_sentences and len(enhanced_sentences) > 1:
            reflection = random.choice(personal_reflections)
            enhanced_sentences.append(reflection)
        
        return '. '.join(enhanced_sentences)
    
    def _add_rhetorical_questions_and_exclamations_advanced(self, text: str) -> str:
        """
        ADICIONAR perguntas retóricas e exclamações avançadas (DICA 3 DO ESPECIALISTA)
        
        Baseado no estilo autêntico do Ryan Santos do base texto ryan.txt:
        - Perguntas retóricas que quebram o fluxo linear
        - Exclamações que transmitem emoção e surpresa
        - Interjeições e expressões coloquiais
        - Variação rítmica entre afirmações e questionamentos
        """
        import random
        import re
        
        # 1. PERGUNTAS RETÓRICAS AUTÊNTICAS (estilo Ryan Santos)
        rhetorical_questions = [
            "Você já parou pra pensar no quanto isso pode ajudar?",
            "Por que será que todo mundo não usa isso ainda?",
            "Quem não quer reduzir custos com uma ferramenta dessas?",
            "O que é mais fácil do que usar uma tecnologia que funciona?",
            "Será que existe algo melhor que isso no mercado?",
            "Sabe qual é o recurso que ninguém fala? Vou te contar...",
            "Por que pagar mais se a solução é barata e eficiente?",
            "Você já viu algo tão revolucionário quanto isso?",
            "E aí, o que vocês acham disso?",
            "Faz sentido pra vocês?",
            "Entendeu?",
            "Compreendem a questão?",
            "Sabe o que é engraçado?",
            "Cara, é impressionante, né?",
            "Olha só, pessoal, vocês já viram isso?",
            "E aí, rapidinho, vocês sabiam disso?",
            "Cara, vocês me entendem, né?",
            "Sabe o que é isso?",
            "E aí, o que eu ia falar...",
            "Eh, por que que eu digo isso?"
        ]
        
        # 2. EXCLAMAÇÕES AUTÊNTICAS (estilo Ryan Santos)
        exclamations = [
            "Isso é demais!",
            "Cara, é impressionante pra caramba!",
            "Nossa, é eficiente demais!",
            "Fácil de usar? É uma mão na roda!",
            "Nossa, isso é absurdo!",
            "Cara, é foda!",
            "Isso é top!",
            "É brabo demais!",
            "É massa pra caramba!",
            "Cara, é doido!",
            "É louco demais!",
            "Nossa!!",
            "Muito mesmo!",
            "Cara, vamos lá!",
            "E aí, galera!",
            "Olha só!",
            "Cara, é impressionante!",
            "É incrível demais!",
            "É notável mesmo!",
            "É absurdo pra caramba!"
        ]
        
        # 3. INTERJEIÇÕES E EXPRESSÕES COLOQUIAIS (estilo Ryan Santos)
        interjections = [
            "Cara,",
            "Galera,",
            "Rapaziada,",
            "Pessoal,",
            "Olha só,",
            "Sabe o que é engraçado?",
            "Eh, por que que eu digo isso?",
            "Cara, é impressionante",
            "Olha só, rapaziada",
            "E aí, o que",
            "Sabe o que é isso?",
            "Cara, vamos lá",
            "E aí, rapidinho",
            "Cara, é impressionante",
            "Olha só, pessoal",
            "E aí, galera",
            "Cara, é foda",
            "Nossa, é demais",
            "Cara, é doido",
            "É louco demais"
        ]
        
        # 4. EXPRESSÕES DE SURPRESA E ÊNFASE (estilo Ryan Santos)
        surprise_expressions = [
            "Pode acreditar?",
            "Não é à toa!",
            "E olha que não estou exagerando!",
            "E não é pouco não!",
            "E olha que não é brincadeira!",
            "E isso é real!",
            "E não estou mentindo!",
            "E olha que não é pouco!",
            "E olha que não é brincadeira!",
            "E isso é fato!",
            "E não estou exagerando!",
            "E olha que não é pouco!",
            "E olha que não é brincadeira!",
            "E isso é real!",
            "E não estou mentindo!"
        ]
        
        # Aplicar transformações de forma inteligente
        sentences = text.split('. ')
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            enhanced_sentences.append(sentence)
            
            # Adicionar perguntas retóricas em pontos estratégicos
            if i % 3 == 0 and len(sentence) > 40:  # A cada 3 frases
                if any(keyword in sentence.lower() for keyword in ["ia", "tecnologia", "revolução", "mudança", "transformação", "mpc"]):
                    # Escolher tipo de pergunta baseado no conteúdo
                    if "revolução" in sentence.lower() or "mudança" in sentence.lower():
                        question = random.choice([
                            "Você já parou pra pensar no quanto isso pode ajudar?",
                            "Por que será que todo mundo não usa isso ainda?",
                            "Sabe qual é o recurso que ninguém fala? Vou te contar..."
                        ])
                    elif "fácil" in sentence.lower() or "simples" in sentence.lower():
                        question = random.choice([
                            "O que é mais fácil do que usar uma tecnologia que funciona?",
                            "Faz sentido pra vocês?",
                            "Entendeu?"
                        ])
                    else:
                        question = random.choice(rhetorical_questions)
                    
                    enhanced_sentences.append(question)
            
            # Adicionar exclamações em frases de benefício
            if i % 4 == 0 and len(sentence) > 30:
                if any(keyword in sentence.lower() for keyword in ["impressionante", "incrível", "revolucionário", "transformando", "mudando"]):
                    exclamation = random.choice(exclamations)
                    enhanced_sentences.append(exclamation)
            
            # Adicionar interjeições no início de frases longas
            if i % 5 == 0 and len(sentence) > 50:
                if not any(interjection in sentence.lower() for interjection in ["cara,", "galera,", "rapaziada,", "olha só,"]):
                    interjection = random.choice(interjections)
                    enhanced_sentences.append(f"{interjection} {sentence}")
                    enhanced_sentences.remove(sentence)  # Remove a frase original
                    enhanced_sentences.append(sentence)  # Adiciona de volta
                else:
                    enhanced_sentences.append(sentence)
        
        # Adicionar expressões de surpresa no final
        if enhanced_sentences and len(enhanced_sentences) > 2:
            surprise = random.choice(surprise_expressions)
            enhanced_sentences.append(surprise)
        
        return '. '.join(enhanced_sentences)
    
    def _fix_specific_problems(self, text: str) -> str:
        """
        CORRIGIR problemas específicos identificados:
        1. Repetições excessivas
        2. Falta de pontuação
        3. Preservar aberturas do Ryan
        """
        import re
        
        # 1. CORRIGIR REPETIÇÕES EXCESSIVAS
        # "Entre nós, Entre nós" → "Entre nós"
        text = re.sub(r'Entre nós,\s*Entre nós,', 'Entre nós,', text, flags=re.IGNORECASE)
        
        # "para quem entende do assunto, para quem entende do assunto" → "para quem entende do assunto"
        text = re.sub(r'para quem entende do assunto,\s*para quem entende do assunto', 'para quem entende do assunto', text, flags=re.IGNORECASE)
        
        # "olha só, olha só" → "olha só"
        text = re.sub(r'olha só,\s*olha só', 'olha só', text, flags=re.IGNORECASE)
        
        # "Cara, vamos lá" repetido → "Cara, vamos lá"
        text = re.sub(r'Cara, vamos lá\s*Cara, vamos lá', 'Cara, vamos lá', text, flags=re.IGNORECASE)
        
        # "impressionante" repetido → "impressionante"
        text = re.sub(r'impressionante\s*impressionante', 'impressionante', text, flags=re.IGNORECASE)
        
        # "A FGV e do Insper" repetido → "A FGV e do Insper"
        text = re.sub(r'A FGV e do Insper,\s*A FGV e do Insper,', 'A FGV e do Insper,', text, flags=re.IGNORECASE)
        
        # "Salve rapaziada" repetido → "Salve rapaziada"
        text = re.sub(r'Salve rapaziada\s*Salve rapaziada', 'Salve rapaziada', text, flags=re.IGNORECASE)
        
        # 2. CORRIGIR PONTUAÇÃO
        # Adicionar pontos onde faltam
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)  # Adicionar ponto antes de maiúscula
        text = re.sub(r'([a-z])(Vamos)', r'\1. \2', text)  # Adicionar ponto antes de "Vamos"
        text = re.sub(r'([a-z])(O que)', r'\1. \2', text)  # Adicionar ponto antes de "O que"
        text = re.sub(r'([a-z])(Entre)', r'\1. \2', text)  # Adicionar ponto antes de "Entre"
        text = re.sub(r'([a-z])(Cara)', r'\1. \2', text)  # Adicionar ponto antes de "Cara"
        text = re.sub(r'([a-z])(Olha)', r'\1. \2', text)  # Adicionar ponto antes de "Olha"
        text = re.sub(r'([a-z])(E aí)', r'\1. \2', text)  # Adicionar ponto antes de "E aí"
        
        # Corrigir pontuação dupla
        text = re.sub(r'\.\s*\.', '.', text)  # Remover pontos duplos
        text = re.sub(r'\?\s*\?', '?', text)  # Remover interrogações duplas
        text = re.sub(r'!\s*!', '!', text)  # Remover exclamações duplas
        
        # 3. PRESERVAR ABERTURAS DO RYAN
        # Restaurar "Sabe o que é interessante?" se foi transformado incorretamente
        text = re.sub(r'O que realmente me chama atenção é como você sabe o que se mostra interessante, especialmente considerando\?', 
                     'Sabe o que é interessante?', text, flags=re.IGNORECASE)
        
        # Garantir que aberturas do Ryan sejam preservadas
        ryan_openings = [
            "Salve rapaziada",
            "E aí, o que",
            "Sabe o que é interessante",
            "Olha só, rapaziada",
            "Cara, galera"
        ]
        
        # Se alguma abertura foi transformada incorretamente, restaurar
        for opening in ryan_openings:
            if opening not in text and opening.lower() in text.lower():
                # Encontrar e restaurar a abertura
                text = re.sub(rf'({opening.lower()})', opening, text, flags=re.IGNORECASE)
        
        # 4. CORRIGIR ESTRUTURAS MALFORMADAS
        # "mpc na ia" → "MPC na IA" (capitalizar adequadamente)
        text = re.sub(r'\bmpc na ia\b', 'MPC na IA', text, flags=re.IGNORECASE)
        
        # Corrigir espaços duplos
        text = re.sub(r'\s+', ' ', text)
        
        # Corrigir pontuação no final de frases
        text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)
        
        # 5. CORRIGIR FRASES MALFORMADAS
        # "E aí..de repente..ele revelou" → "E aí, de repente, ele revelou"
        text = re.sub(r'\.\.', ',', text)  # Substituir .. por ,
        text = re.sub(r',,', ',', text)  # Remover vírgulas duplas
        
        # "sabe o que E aí" → "sabe o que, E aí"
        text = re.sub(r'sabe o que E aí', 'sabe o que, E aí', text, flags=re.IGNORECASE)
        
        return text
    
    def _is_artificially_simple(self, sentence: str) -> bool:
        """Detectar se uma frase é artificialmente simples"""
        import re
        sentence_lower = sentence.lower()
        
        # Critérios de simplicidade artificial
        criteria = [
            # Frases muito curtas com padrões simples
            len(sentence.split()) <= 8 and any(word in sentence_lower for word in [
                "é uma parada", "é algo que", "é interessante", "é impressionante"
            ]),
            
            # Estruturas repetitivas
            sentence_lower.count("é") >= 3 and len(sentence.split()) <= 15,
            
            # Padrões coloquiais excessivos
            sum(1 for word in ["né", "sabe", "cara", "galera", "rapaziada"] if word in sentence_lower) >= 3,
            
            # Frases que começam com conjunções simples
            any(sentence_lower.startswith(phrase) for phrase in [
                "e aí", "olha só", "sabe o que", "cara, é", "galera, é"
            ]) and len(sentence.split()) <= 10,
            
            # Estruturas "X é Y" muito simples
            re.match(r'^[A-Za-z\s,]+é\s+[a-z\s]+\.?$', sentence) and len(sentence.split()) <= 6
        ]
        
        return any(criteria)
    
    def _add_dynamic_complexity(self, sentence: str) -> str:
        """Adicionar complexidade dinâmica a uma frase simples"""
        import random
        
        # Estratégias de complexificação
        strategies = [
            self._add_subordinate_clause,
            self._add_qualifying_phrase,
            self._add_contrastive_element,
            self._add_temporal_reference,
            self._add_causal_connection,
            self._add_conditional_structure
        ]
        
        # Aplicar 1-2 estratégias aleatórias
        num_strategies = random.randint(1, 2)
        selected_strategies = random.sample(strategies, num_strategies)
        
        complexified = sentence
        for strategy in selected_strategies:
            complexified = strategy(complexified)
        
        return complexified
    
    def _add_subordinate_clause(self, sentence: str) -> str:
        """Adicionar oração subordinada"""
        connectors = [
            "que", "quando", "onde", "como", "porque", "embora", "enquanto"
        ]
        connector = random.choice(connectors)
        
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        additions = [
            f", {connector} está transformando a forma como pensamos",
            f", {connector} representa uma mudança fundamental",
            f", {connector} está revolucionando diferentes setores",
            f", {connector} merece nossa atenção especial",
            f", {connector} está criando novas possibilidades"
        ]
        
        return sentence + random.choice(additions) + "."
    
    def _add_qualifying_phrase(self, sentence: str) -> str:
        """Adicionar frase qualificadora"""
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        qualifiers = [
            ", especialmente considerando o contexto atual",
            ", particularmente em relação às tendências emergentes",
            ", principalmente quando analisamos os dados recentes",
            ", sobretudo quando consideramos as implicações práticas",
            ", especialmente se observarmos o panorama geral"
        ]
        
        return sentence + random.choice(qualifiers) + "."
    
    def _add_contrastive_element(self, sentence: str) -> str:
        """Adicionar elemento contrastivo"""
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        contrasts = [
            ", embora muitos ainda não percebam",
            ", diferentemente do que se pensava anteriormente",
            ", contrariamente às expectativas iniciais",
            ", ao contrário das abordagens tradicionais",
            ", em contraste com os métodos convencionais"
        ]
        
        return sentence + random.choice(contrasts) + "."
    
    def _add_temporal_reference(self, sentence: str) -> str:
        """Adicionar referência temporal"""
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        temporal_refs = [
            ", especialmente nos últimos meses",
            ", particularmente neste momento",
            ", principalmente considerando a evolução recente",
            ", sobretudo quando observamos as tendências atuais",
            ", especialmente se analisarmos o cenário presente"
        ]
        
        return sentence + random.choice(temporal_refs) + "."
    
    def _add_causal_connection(self, sentence: str) -> str:
        """Adicionar conexão causal"""
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        causal_connectors = [
            ", o que explica por que",
            ", razão pela qual",
            ", motivo pelo qual",
            ", fator que justifica",
            ", elemento que demonstra"
        ]
        
        return sentence + random.choice(causal_connectors) + " isso é tão relevante."
    
    def _add_conditional_structure(self, sentence: str) -> str:
        """Adicionar estrutura condicional"""
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        
        conditionals = [
            ", especialmente se considerarmos",
            ", particularmente quando analisamos",
            ", principalmente se observarmos",
            ", sobretudo se levarmos em conta",
            ", especialmente se pensarmos em"
        ]
        
        return sentence + random.choice(conditionals) + " as implicações futuras."
    
    def _fix_excessive_repetitions(self, text: str) -> str:
        """Corrigir repetições excessivas"""
        # Detectar repetições de palavras
        words = text.split()
        word_count = {}
        
        for word in words:
            word_lower = word.lower().strip('.,!?')
            if len(word_lower) > 3:  # Ignorar palavras muito curtas
                word_count[word_lower] = word_count.get(word_lower, 0) + 1
        
        # Substituir palavras repetidas excessivamente
        for word, count in word_count.items():
            if count > 3:  # Mais de 3 ocorrências
                synonyms = self._get_synonyms(word)
                if synonyms:
                    # Substituir algumas ocorrências
                    replacements = 0
                    for synonym in synonyms:
                        if replacements >= count // 2:  # Substituir metade
                            break
                        text = text.replace(word, synonym, 1)
                        replacements += 1
        
        return text
    
    def _get_synonyms(self, word: str) -> list:
        """Obter sinônimos para uma palavra"""
        synonyms_dict = {
            "interessante": ["fascinante", "curioso", "notável", "relevante"],
            "impressionante": ["surpreendente", "extraordinário", "notável", "excepcional"],
            "importante": ["relevante", "significativo", "crucial", "essencial"],
            "grande": ["enorme", "vasto", "extenso", "considerável"],
            "mudança": ["transformação", "evolução", "alteração", "modificação"],
            "tecnologia": ["inovação", "avanço", "desenvolvimento", "progresso"],
            "pessoas": ["indivíduos", "cidadãos", "usuários", "público"],
            "vida": ["existência", "cotidiano", "realidade", "experiência"]
        }
        
        return synonyms_dict.get(word.lower(), [])
    
    def _fix_predictable_structures(self, text: str) -> str:
        """Corrigir estruturas previsíveis"""
        import random
        
        # Padrões previsíveis comuns
        predictable_patterns = [
            (r"É\s+([a-z\s]+)\s+que\s+([a-z\s]+)\.", r"O que realmente me chama atenção é como \1 \2, especialmente considerando"),
            (r"([A-Z][a-z]+)\s+é\s+([a-z\s]+)\.", r"\1 representa uma \2 que está transformando"),
            (r"Olha\s+só,\s+([a-z\s]+)\.", r"Observem, pessoal, \1, e isso é particularmente relevante porque"),
            (r"Cara,\s+([a-z\s]+)\.", r"Entre nós, \1, e isso me faz pensar em"),
            (r"Sabe\s+o\s+que\s+é\s+([a-z\s]+)\?", r"Compreendem a questão? \1, e isso é especialmente importante quando")
        ]
        
        import re
        for pattern, replacement in predictable_patterns:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
        
        return text
    
    def _add_syntactic_variation(self, text: str) -> str:
        """Adicionar variação sintática"""
        import random
        
        # Variações de início de frase
        sentence_starters = [
            "O que mais me impressiona é que",
            "É notável como",
            "Particularmente interessante é o fato de que",
            "O aspecto mais relevante é que",
            "Sobretudo, é importante destacar que"
        ]
        
        # Dividir em frases e variar algumas
        sentences = text.split('. ')
        varied_sentences = []
        
        for i, sentence in enumerate(sentences):
            if i > 0 and random.random() < 0.3:  # 30% chance de variar
                starter = random.choice(sentence_starters)
                varied_sentences.append(f"{starter} {sentence.lower()}")
            else:
                varied_sentences.append(sentence)
        
        return '. '.join(varied_sentences)
    
    def _apply_ryan_humanization(self, text: str) -> str:
        """Aplicar humanização Ryan em TODO o texto, incluindo partes expandidas"""
        
        # Dividir texto em parágrafos (usar quebras de linha duplas ou pontos finais)
        paragraphs = []
        current_paragraph = ""
        
        # Dividir por quebras de linha duplas primeiro
        if '\n\n' in text:
            paragraphs = text.split('\n\n')
        else:
            # Se não há quebras duplas, dividir por frases longas
            sentences = text.split('. ')
            current_paragraph = ""
            for sentence in sentences:
                current_paragraph += sentence
                if len(current_paragraph) > 200:  # Parágrafo com mais de 200 caracteres
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = ""
            if current_paragraph.strip():
                paragraphs.append(current_paragraph.strip())
        
        humanized_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            # Pular parágrafos que já são do Ryan (abertura, hook, conclusão)
            if i == 0 or "Salve rapaziada" in paragraph or "Tamo junto" in paragraph:
                humanized_paragraphs.append(paragraph)
                continue
            
            # Humanizar parágrafos técnicos/acadêmicos
            humanized_paragraph = self._humanize_technical_paragraph(paragraph)
            humanized_paragraphs.append(humanized_paragraph)
        
        return '\n\n'.join(humanized_paragraphs)
    
    def _humanize_technical_paragraph(self, paragraph: str) -> str:
        """Humanizar parágrafo técnico/acadêmico para estilo Ryan"""
        
        # Se o parágrafo já tem estilo Ryan, não modificar
        if any(phrase in paragraph.lower() for phrase in ["cara", "rapaziada", "galera", "olha só", "e aí"]):
            return paragraph
        
        # Aplicar transformações Ryan
        humanized = paragraph
        
        # 1. Adicionar interrupção natural no início
        interruptions = [
            "Cara, é impressionante como",
            "Olha só, rapaziada,",
            "E aí, o que é interessante é que",
            "Sabe o que é legal?",
            "Cara, o que me chama atenção é que"
        ]
        import random
        interruption = random.choice(interruptions)
        humanized = f"{interruption} {humanized.lower()}"
        
        # 2. Substituir linguagem formal por coloquial
        replacements = {
            "representa uma revolução": "é uma revolução mesmo",
            "permite que os algoritmos": "faz com que os algoritmos",
            "está sendo aplicada": "tá sendo aplicada",
            "pode prever": "consegue prever",
            "está otimizando": "tá otimizando",
            "seria impossível": "seria impossível mesmo",
            "está atingindo": "tá atingindo",
            "já estão implementando": "já tão implementando",
            "promete aplicações": "promete umas aplicações",
            "surgem questões": "surgem umas questões",
            "está evoluindo": "tá evoluindo",
            "está acontecendo": "tá acontecendo",
            "é impressionante": "é impressionante mesmo",
            "merece nossa atenção": "merece nossa atenção, né?",
            "vale a pena refletir": "vale a pena a gente refletir",
            "está transformando": "tá transformando",
            "é notável": "é notável mesmo",
            "está mudando": "tá mudando",
            "é enorme": "é enorme mesmo",
            "está sendo explorado": "tá sendo explorado",
            "é fascinante": "é fascinante mesmo",
            "está acontecendo": "tá acontecendo",
            "é importante": "é importante mesmo",
            "representa um marco": "é um marco mesmo",
            "ou model predictive control": "ou MPC",
            "diferente dos sistemas tradicionais": "diferente dos sistemas que a gente conhece",
            "imagine um carro autônomo": "imagina um carro que dirige sozinho",
            "essa tecnologia": "essa parada",
            "na indústria": "na indústria mesmo",
            "o que mais impressiona": "o que mais me impressiona",
            "pesquisadores estão descobrindo": "os pesquisadores tão descobrindo",
            "a precisão desses sistemas": "a precisão desses sistemas, cara",
            "empresas como tesla": "empresas como a Tesla",
            "o futuro promete": "o futuro promete, galera",
            "mas também surgem": "mas também surgem, né?",
            "especialistas alertam": "os especialistas alertam",
            "a velocidade com que": "a velocidade que",
            "investidores estão colocando": "os investidores tão colocando",
            "universidades ao redor": "as universidades ao redor"
        }
        
        for formal, informal in replacements.items():
            humanized = humanized.replace(formal, informal)
        
        # 3. Adicionar proximidade emocional
        emotional_additions = [
            "Entre nós, ",
            "A gente sabe que ",
            "Nós sabemos que ",
            "Cara, é isso que ",
            "Olha só, "
        ]
        emotional = random.choice(emotional_additions)
        humanized = f"{emotional}{humanized.lower()}"
        
        # 4. Adicionar hesitação natural
        if "." in humanized and "..." not in humanized:
            sentences = humanized.split(".")
            if len(sentences) > 1:
                sentences[1] = f"...{sentences[1].strip()}"
                humanized = ".".join(sentences)
        
        # 5. Adicionar pergunta retórica
        questions = [
            "Faz sentido para vocês?",
            "Entendeu?",
            "Compreendem a questão?",
            "E aí, o que vocês acham?",
            "Faz sentido?"
        ]
        question = random.choice(questions)
        humanized = f"{humanized} {question}"
        
        return humanized