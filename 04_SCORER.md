# 04_SCORER.md  
> Módulo responsável por **medir, auditar e corrigir o som da fala**.  
> Atua como o "ouvido técnico" do sistema — calcula métricas, aplica gates e propõe reescritas até o texto soar **naturalmente seu**.
> 
> **Versão calibrada para ChatGPT Plus (execução 100% interativa, sem interação externa).**

---

## Tópico 1 — Métricas base e propósito

### 1.1) O que é o SCORER  

O **SCORER** é o avaliador estilométrico do sistema `📁 estilometria-agent/`.  
Ele analisa o texto gerado e mede o quanto ele se mantém fiel ao seu **ritmo, calor e vocabulário característico**, usando como referência os padrões definidos em:

- `01_STYLE_SPEC.md` → DNA da voz (persona, ritmo, whitelist/redlist)  
- `03_RAG_STYLE.md` → amostras reais de cadência e few-shots de estilo  
- `whitelist.txt` e `redlist.txt` → léxico permitido e termos banidos

→ Fonte única de léxico: whitelist.txt e redlist.txt (diretório raiz).  

O SCORER transforma o que seria “intuição estilística” em **métricas quantificáveis** e rastreáveis.  
Ele atua tanto **em tempo real** (no momento da geração) quanto **em pós-avaliação** (para resumo de calibraçãos e calibração).

---

### 1.2) Propósito  

- Garantir **consistência estilométrica** em todas as saídas.  
- **Quantificar** o quanto o texto se aproxima da sua voz real.  
- **Detectar e corrigir** padrões robóticos ou formulaicos.  
- Evitar **drift de voz** entre diferentes formatos (thread, artigo, roteiro).  
- Servir de **ponte entre estilo e qualidade mensurável**, alimentando os módulos de tuning.

---

### 1.3) Entradas e saídas  

**Entrada mínima (contrato padrão):**  
```json
{
  "run_id": "ISO-8601",
  "style_plan": {
    "avg_sentence_len_target": [18,22],
    "burstiness_target": "alto",
    "heat_target": 3,
    "punch_target_per_100w": [2.0,4.0],
    "transitions_whitelist": ["rapaziada", "olha só", "o ponto é:", "sem rodeio:"],
    "redlist_hard": true
  },
  "draft_text": "<texto_gerado>"
}

Saída esperada:
{
  "scores": {
    "StyleScore": 0.00,
    "CadenceScore": 0.00,
    "HeatCurveMatch": 0.00,
    "LexicalCompliance": 0.00,
    "PunctuationFit": 0.00
  },
  "originality": {
    "ngram_overlap_max": 0,
    "cos_sim_max": 0.00,
    "rougeL_max": 0.00
  },
  "violations": ["..."],
  "fix_suggestions": [
    { "mode": "REWRITE_*", "targets": ["secao_n"], "hint": "…" }
  ]
}

### 1.4) Métricas principais
| Métrica               | Mede                                    | Interpretação                                                              |
| --------------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| **CadenceScore**      | Ritmo das frases, variação e respiração | Penaliza uniformidade; recompensa alternância entre frases curtas e longas |
| **HeatCurveMatch**    | Energia emocional por seção             | Mede se o texto respira e esquenta na hora certa                           |
| **PunctuationFit**    | Uso consciente de `:` e `—`             | Verifica se pontuações assinatura foram aplicadas com intenção             |
| **LexicalCompliance** | Fidelidade ao vocabulário próprio       | Garante presença de whitelist e ausência de redlist                        |
| **StyleScore**        | Média ponderada dos fatores de voz      | Reflete o “quão seu” o texto soa                                           |
| **OriginalityFlags**  | Risco de colagem                        | Mede sobreposição léxica e semântica com o corpus                          |

### 1.6) Detecção de Padrões de IA Genérica

O SCORER agora detecta automaticamente padrões típicos de texto gerado por IA genérica:

**Padrões banidos (regex):**
- `é importante (?:notar|ressaltar|destacar) que`
- `em (um|um) mundo cada vez mais`
- `à medida que (?:o|a|os|as)? (?:mundo|tempo|tecnologia)`
- `no cenário (?:atual|contemporâneo)`
- `de (?:forma|maneira) (?:geral|significativa|clara)`
- `por outro lado`
- `em contrapartida`
- `vale (?:ressaltar|destacar) que`
- `dito isso`
- `com base (?:nisso|nestas informações|nestes dados)`
- `portanto,? conclui-se que`
- `é fundamental (?:compreender|entender) que`
- `é evidente que`
- `sem precedentes`
- `no final do dia`
- `em suma|em resumo|em conclusão`
- `nesse sentido|diante (?:disso|do exposto)`
- `observa-se que|evidencia-se que|postula-se que`
- `a era digital`
- `cada vez mais comum`
- `de modo geral`

**Voz passiva inflada:**
- `(?:foi|foram|será|são|seja|são) \\w+ (?:por|pelo|pela)`

**Políticas:**
- **Taxa máxima:** 12% das sentenças com padrões banidos
- **Ação:** Rejeição automática + reescrita
- **Substituições sugeridas:** "Na prática:", "Sem rodeio:", "O ponto é:", "exemplo concreto:", "mostra o rastro:"

### 1.7) Gates de aprovação
| Gate                  | Critério                                 | Ação se falhar                     |
| --------------------- | ---------------------------------------- | ---------------------------------- |
| **StyleScore**        | ≥ 0.80                                   | Reescrever seção inteira           |
| **LexicalCompliance** | ≥ 0.95 e redlist = 0                     | Substituir termos                  |
| **HeatCurveMatch**    | ≥ 0.80                                   | Reequilibrar intensidade emocional |
| **PunctuationGate**   | ':' ≤1, '—' ≤1, punch 2.0–4.0/100w      | REWRITE_PUNCT_MINIMAL              |
| **PunctuationFit**    | ≥ 0.75 (2.0–4.0/100w)                    | Ajustar contrastes e sínteses      |
| **IAStylePatternRate** | ≤ 12% sentenças com padrões banidos      | REWRITE_IA_PATTERNS                |
| **HumanScore**        | ≥ 0.75 (tom conversa + clareza factual)   | REWRITE_HUMANIZE                   |
| **HedgingGate**       | ≤ 10% frases com hedging excessivo        | REWRITE_DECISIVE                   |
| **PassiveVoiceGate**  | ≤ 15% frases em voz passiva               | REWRITE_ACTIVE_VOICE               |
| **PredictableRhythm** | ≤ 18% sentenças no mesmo bucket de tamanho | REWRITE_RHYTHM_VARIETY             |
| **LowWarmth**         | 1-3 ocorrências de 2ª pessoa por bloco (anti-ressonância) | INJECT_DIRECT_ADDRESS              |
| **RoboticFormality**  | ≤ 20% padrões explicativos previsíveis     | REWRITE_SPONTANEOUS                |
| **MechanicalWriting** | ≤ 15% sequência linear sem inflexão       | REWRITE_RHYTHM_VARIETY             |
| **LowCreativity**     | ≥ 0.15 densidade criativa (analogia/contraste) | INJECT_CREATIVE_SPARK            |
| **RigidOrientation**  | ≤ 60% conselhos imperativos sem nuance    | REWRITE_CONSEQUENCE_FOCUS          |
| **FormalidadeRobotica** | ≤ 20% padrões explicativos previsíveis     | REWRITE_SPONTANEOUS                |
| **EscritaMecanica**   | ≤ 25% sequência linear sem inflexão       | REWRITE_RHYTHM_VARIETY             |
| **FaltaCriatividade** | ≥ 0.30 densidade criativa (analogia/contraste) | INJECT_CREATIVE_SPARK            |
| **OrientacaoRigida**  | ≤ 25% conselhos imperativos sem nuance    | REWRITE_CONSEQUENCE_FOCUS          |
| **FraseDeclarativaIsolada** | ≤ 30% frases declarativas sem pergunta | INJECT_QUESTIONS                   |
| **EncadeamentoMecanico** | ≤ 25% sequência linear sem pausa | REWRITE_RHYTHM_VARIETY             |
| **ImperativoConsecutivo** | ≤ 20% imperativos seguidos | REWRITE_CONSEQUENCE_FOCUS          |
| **TomPrescritivoFrio** | ≤ 15% linguagem prescritiva | REWRITE_SPONTANEOUS                |
| **AusenciaMetafora** | ≥ 0.20 densidade de metáforas/consequências | INJECT_CREATIVE_SPARK            |
| **Originalidade**     | ngram < 12 / cos ≤ 0.92 / ROUGE-L ≤ 0.65 | Reestruturar períodos              |

**Regras de originalidade:**
- Originalidade: **não copie frases**; **saída 100% original**.

### 1.7) Mapeamento de violações
| Violação         | Indício                | Modo de reescrita sugerido |
| ---------------- | ---------------------- | -------------------------- |
| `CadenceLow`     | Frases com ritmo igual | `REWRITE_CADENCE`          |
| `HeatFlat`       | Emoção estável         | `REWRITE_HEAT`             |
| `PunchUnderuse`  | Falta de “:” ou “—”    | `REWRITE_PUNCH`            |
| `TransitionSpam` | Conectores repetidos   | `REWRITE_TRANSITIONS`      |
| `RedlistHit`     | Termo proibido         | `REWRITE_LEXICON`          |
| `NearCopy`       | Similaridade alta      | `REWRITE_ORIGINALITY`      |

### 1.8) Por que isso mantém o "som da fala"

Mede o ritmo real (como você respira).
Equilibra emoção e clareza (heat sob controle).
Preserva a musicalidade dos sinais : e —.
Garante léxico próprio, eliminando ruído robótico.
Audita originalidade para que a voz permaneça autêntica.
Resumo: o SCORER é o árbitro da voz.
Ele traduz subjetividade (tom, ritmo, calor) em números auditáveis — e com base neles, orienta a máquina a reescrever até soar humano.

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.  
> Tópico 2 aprofunda o núcleo técnico — **algoritmos, thresholds e normalizações**.

---

## Tópico 2 — Algoritmos e Thresholds

### 2.1) Arquitetura interna  

O SCORER opera em 4 camadas analíticas:

1. **Pré-processamento:**  
   Tokeniza o texto, segmenta por frases e seções (respeitando `STYLE_PLAN.format`).
2. **Análise métrica:**  
   Calcula métricas primárias (cadência, heat, pontuação, léxico, originalidade).
3. **Normalização:**  
   Ajusta cada métrica aos alvos definidos (min–max e z-score local).
4. **Avaliação & decisão:**  
   Compara resultados aos **thresholds** e aplica **modos de reescrita** se necessário.

---

### 2.0 Gates de Volume & Cadência (aplicação por formato)

#### Hard Gate — Massa mínima por formato
- **artigo:** `min_words = 120`, `min_sentences = 5`, `min_paragraphs = 2`
- **thread:** `min_words = 80`, `min_sentences = 5`
- **roteiro:** `min_blocks = 3` (abertura → virada → fecho)

**Se violar**: reprovar com flag `CadenceMassTooLow` e **não** computar StyleScore.

#### Corredor de Cadência (avg_sentence_len)
- **Faixa-alvo (artigo):** 18–22 (passa limpo)
- **Faixa interna tolerada:** 16–24 → cap em `Cadence ≤ 0.75` e `stylescore -= 3`
- **Faixa externa:** <16 ou >24 → cap em `Cadence ≤ 0.55` e `stylescore -= 8` + flag `CadenceOutOfBand`

#### Regras operacionais de cadência:
- **merge_if_lt=14** • **split_if_gt=26** • **one_punch_sentence_per_paragraph=true**

**Penalizações:** CadenceOutOfBand, CadenceMassTooLow, ConnectorSpam

> Observação: manter a penalização cumulativa com `cadence_var` (stdev muito baixo ou muito alto).

---

### 2.2) Pseudocódigo geral  

```python
def scorer_run(style_plan, draft_text):
    doc = preprocess(draft_text)
    results = {}

    results["cadence"] = measure_cadence(doc, style_plan)
    results["heat"] = measure_heat(doc, style_plan)
    results["punct"] = measure_punct(doc, style_plan)
    results["lexicon"] = measure_lexicon(doc, style_plan)
    results["originality"] = measure_originality(doc, corpus_ref)

    normalized = normalize(results, style_plan)
    decisions = apply_gates(normalized, style_plan)
    return {"scores": normalized, "violations": decisions["violations"], "fix_suggestions": decisions["fixes"]}

### 2.3) Cálculo por métrica
a) Cadência (ritmo de frase)
avg_len = mean(sentence_lengths)
stdev_len = stdev(sentence_lengths)
cadence_score = 1 - abs(avg_len - target_mid)/target_span + (0.05 if stdev_len > 5.5 else 0)

target_mid: média do range definido ([18,22] → 20)
bonus: 5% se houver variação saudável de frase (burstiness)
penalidade: -0.1 se ≥3 frases consecutivas tiverem mesmo comprimento
Faixa ideal: CadenceScore ≥ 0.80

b) Curva de calor (HeatCurveMatch)
Cada frase recebe uma pontuação emocional local (0–5) via dicionário de intensidade + densidade de 2ª pessoa, metáforas e imperativos.

curve_pred = model_curve_by_format("thread")   # referência esperada
curve_obs  = measure_heat_by_section(doc)
heat_score = 1 - mse(curve_pred, curve_obs)

Faixa ideal: HeatCurveMatch ≥ 0.80
Pico (4/5) nas viradas de tese.
Heat médio entre 2.8–3.4.

c) Pontuação (PunctuationFit)
punch_density = count([":","—"]) / (words/100)
fit_range = max(0, 1 - abs(punch_density - target_mid)/target_span)
bonus = 0.05 if ":" used_in_synthesis else 0
punct_score = clamp(fit_range + bonus - spam_penalty, 0, 1)

Faixa ideal: 2.0–4.0 punches/100w
: em síntese de ideia
— em contraste ou virada

d) Léxico (LexicalCompliance)
whitelist_ratio = count(whitelist_hits)/total_words
redlist_hits = count(redlist_hits)
lexicon_score = normalize(whitelist_ratio, [0.8,1.0]) - (redlist_hits*0.05)
Faixa ideal: LexicalCompliance ≥ 0.95 e redlist = 0

e) Originalidade (plágio semântico)
Compara o texto a janelas do /CORPUS/ usando embeddings e n-grams.
ngram_overlap_max = max(ngram_overlap(text, corpus))
cos_sim_max = max(cosine_similarity(embeddings(text), embeddings(corpus)))
rougeL_max = rougeL(text, corpus)

Gates mínimos:
ngram_overlap_max < 12
cos_sim_max ≤ 0.92
ROUGE-L ≤ 0.65

### 2.4) Normalização e pesos (com humanização GPTZero)
Após calcular as métricas, o SCORER aplica pesos dinâmicos conforme o formato do texto:
| Formato     | Cadence | Heat | Lexicon | Punct | Human | Creative | Variation | Emotional | CauseEffect | Outros |
| ----------- | ------: | ---: | ------: | ----: | ----: | -------: | --------: | --------: | ----------: | -----: |
| **Thread**  |    0.45 | 0.20 |    0.20 |  0.05 |  0.08 |     0.10 |      0.07 |      0.06 |        0.05 |   0.00 |
| **Artigo**  |    0.40 | 0.25 |    0.20 |  0.05 |  0.08 |     0.10 |      0.07 |      0.06 |        0.05 |   0.00 |
| **Roteiro** |    0.50 | 0.15 |    0.20 |  0.05 |  0.08 |     0.10 |      0.07 |      0.06 |        0.05 |   0.00 |

**Métricas Human (HumanScore) - Versão 5.1:**
- **HumanToneScore:** +0.12 (tom conversa + persuasão informal + tom pessoal)
- **SensoryRatio:** +0.08 (1-2 detalhes sensoriais por bloco; priorizar substantivos concretos + verbos de percepção)
- **2ndPersonRate:** +0.06 (uso de "você", "ele", "ela", "nós")
- **Cadence variety:** +0.12 (variação de comprimentos de frase)
- **Simple grammar:** +0.08 (estrutura SVO, coordenação, poucas subordinadas)
- **Action verb rate:** +0.06 (verbos de ação concretos)
- **CreativeDensity:** +0.10 (analogia, contraste, metáfora leve controlada)
- **SentenceVariation:** +0.07 (desvio padrão de comprimentos de frase)
- **EmotionalColor:** +0.06 (interjeições, exclamações leves, tom espontâneo)
- **CauseEffectRatio:** +0.05 (foco em consequências, não só conselhos)
- **QuestionDensity:** +0.10 (perguntas diretas, "O que acontece?", "Entendeu?")
- **CausalConnectorRatio:** +0.06 (relações causais, "porque", "então", "o resultado")
- **ComparisonUsage:** +0.08 (comparações metafóricas leves, "como um mecânico")
- **RelationalPronounRatio:** +0.05 (pronomes relacionais, "você vê", "você entende")
- **ConcreteMetaphorDensity:** +0.05 (metáforas concretas, "corta barulho", "deixa rastro")
- **SentenceLengthVariety:** +0.06 (variação de comprimentos, frases ultra-curtas)
- **Hedging rate:** cap 0.10 (limita "talvez", "possivelmente", "pode ser")
- **Passive voice rate:** cap 0.15 (limita voz passiva excessiva)
- **Remove formalese:** true (elimina linguagem formal excessiva)

O StyleScore final é a média ponderada dessas normalizações.
Threshold padrão: StyleScore ≥ 0.80.

### 2.5) Thresholds adaptativos
Para evitar falsos negativos, o SCORER usa ajuste dinâmico de tolerância:
if style_score < 0.8 and burstiness > 0.75:
    threshold["cadence"] -= 0.03

Outros exemplos:
| Situação                         | Ajuste automático                          |
| -------------------------------- | ------------------------------------------ |
| Texto muito curto (<150w)        | Relaxa `HeatCurveMatch` em −0.05           |
| Picos de heat muito concentrados | Eleva `PunctuationFit` em +0.05            |
| Formato = “Roteiro”              | Aumenta peso de cadência e reduz pontuação |
| Linguagem emocional alta         | Aumenta peso de HeatCurveMatch             |

### 2.6) Tolerâncias e desvios padrão
CadenceScore → tolerância ±0.05
HeatCurveMatch → ±0.07
PunctuationFit → ±0.05
LexicalCompliance → ±0.02
StyleScore global → ±0.03
Esses valores definem a “zona de ruído natural” do estilo humano,
garantindo que pequenas variações não acionem reescrita desnecessária.

### 2.7) Interação com REWRITER
Cada métrica abaixo do limiar ativa uma sugestão específica:
| Trigger         | Ação                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| `CadenceLow`    | `REWRITE_CADENCE` — alternar ritmos, adicionar 1 frase longa + 1 curta |
| `HeatFlat`      | `REWRITE_HEAT` — redistribuir energia emocional                        |
| `PunchUnderuse` | `REWRITE_PUNCH` — reforçar contrastes e sínteses                       |
| `RedlistHit`    | `REWRITE_LEXICON` — substituição contextual                            |
| `NearCopy`      | `REWRITE_ORIGINALITY` — alterar estrutura ou voz                       |

### 2.8) Relatórios e telemetria
Cada execução gera um registro no formato:
{
  "timestamp": "2025-10-13T09:00:00Z",
  "file": "thread_2025-10-13.md",
  "scores": {"Style":0.83,"Cadence":0.80,"Heat":0.79,"Lexicon":0.97,"Punct":0.76},
  "violations": ["HeatLow"],
  "fixes": ["REWRITE_HEAT"]
}

Esses resumo de calibraçãos são gerados como resumos markdown para colar no seu repositório local e consolidados manualmente para tuning interativo.
### 2.9) Síntese
O SCORER combina métricas quantificáveis, thresholds adaptativos e regras heurísticas para manter a escrita dentro da faixa “humanamente irregular” —
onde o texto soa orgânico, quente e seu, sem se tornar robótico nem caótico.

Resumo do Tópico 2:
A métrica é a partitura.
O threshold é o maestro.
O SCORER garante que a melodia da sua fala nunca desafine.

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.  

---

## Tópico 3 — Modos de Reescrita (REWRITER engine)

> Objetivo: transformar **diagnósticos do SCORER** em **ações específicas de correção**, preservando conteúdo e **originalidade** enquanto ajusta cadência, calor, pontuação, léxico e transições.

---

### 3.1) Contrato do REWRITER

**Entrada**
```json
{
  "run_id": "ISO-8601",
  "draft_text": "<rascunho_v1>",
  "violations": ["CadenceLow","PunchUnderuse", "..."],
  "style_plan": {
    "format": "artigo",
    "avg_sentence_len_target": [18,22],
    "burstiness_target": "alto",
    "heat_target": 3,
    "punch_target_per_100w": [2.0,4.0],
    "transitions_whitelist": ["rapaziada","olha só","o ponto é:","sem rodeio:"],
    "redlist_hard": true
  },
  "targets": {"secao_2":["p2","p3"],"fecho":["p1"]}
}

Saída
{
  "draft_text_rewritten": "<rascunho_v2>",
  "actions_applied": ["REWRITE_CADENCE@secao_2(p2-p3)","REWRITE_PUNCH@fecho(p1)"],
  "notes": "mantido sentido; +1 frase longa e +1 curta por seção; dois-pontos em sínteses"
}

Regras gerais
Preservar sentido e encadeamento lógico.
Não inserir fatos novos.
Não reduzir originalidade (rechecar n-gram/cos_sim após reescrever).
Limitar a densidade de mudanças por passo (evita “overfit” estilístico).

### 3.2) Tabela de mapeamento (violação → modo)
| Violação (SCORER)                | Sinal                          | Modo principal          | Modo auxiliar       |
| -------------------------------- | ------------------------------ | ----------------------- | ------------------- |
| `CadenceLow`                     | ritmo uniforme                 | **REWRITE_CADENCE**     | REWRITE_TRANSITIONS |
| `HeatFlat` / `HeatSpikes`        | emoção baixa / picos 5/5       | **REWRITE_HEAT**        | REWRITE_PUNCH       |
| `PunchUnderuse` / `PunchOveruse` | `:`/`—` pouco / excessivo      | **REWRITE_PUNCH**       | REWRITE_STRUCTURE   |
| `LexiconLow` / `RedlistHit`      | pouco whitelist / termo banido | **REWRITE_LEXICON**     | —                   |
| `TransitionSpam`                 | conector repetido              | **REWRITE_TRANSITIONS** | REWRITE_CADENCE     |
| `NearCopy`                       | similaridade alta              | **REWRITE_ORIGINALITY** | REWRITE_STRUCTURE   |

### 3.3) REWRITE_CADENCE (ritmo e respiração)

Quando usar: CadenceScore < alvo ou frases com comprimentos semelhantes.

Ação
Inserir 1 frase longa (30–40) e 1 curta (≤10) por seção-alvo.
Variar início de período (verbo, advérbio, pergunta curta).
Dividir frases encadeadas por vírgulas em duas frases naturais.

Pseudoprompt interno
[REWRITE_CADENCE]
- Mantenha o sentido original.
- Introduza 1 período longo (30–40 palavras) e 1 curto (≤10) nesta seção.
- Reordene termos para variar o ritmo; evite ponto-e-vírgula.

Mini-exemplo
Antes: “Precisamos de consistência no plano e disciplina na execução para manter o foco.”
Depois: “Precisamos de consistência no plano. E de disciplina na execução — para manter o foco quando a euforia passa.”

### 3.4) REWRITE_HEAT (curva emocional)
Quando usar: HeatCurveMatch < alvo, tom frio ou picos 5/5 seguidos.

Ação
Inserir marca de calor por parágrafo (2ª pessoa, detalhe sensorial, pergunta direta).
Conduzir picos 4/5 na virada de tese e no fecho; abrir em 3/5.

Pseudoprompt
[REWRITE_HEAT]
- Adicione 1-2 detalhes sensoriais por bloco (priorizar substantivos concretos + verbos de percepção).
- Movimente o pico emocional para a virada de tese (heat 4/5) e mantenha 3/5 no restante.
- Evite adjetivação gratuita; use verbos concretos.

Mini-exemplo
Antes: “Mudanças exigem planejamento.”
Depois: “Mudanças exigem planejamento. E você sabe onde costuma travar? No primeiro passo — quando a planilha é perfeita e o corpo hesita.”

### 3.5) REWRITE_PUNCH (pontuação assinatura)
Quando usar: PunctuationFit fora de [2.0,4.0]/100w.

Ação
Usar “:” em sínteses e “—” em contrastes; limitar excesso.
Converter dois-pontos redundantes em verbos de síntese (“em suma”, “resultado”).

Pseudoprompt
[REWRITE_PUNCH]
- Coloque ":" ao apresentar uma síntese clara.
- Use "—" para contraste ou virada.
- Mantenha punch density em 2.0–4.0 por 100 palavras.

Mini-exemplo
Antes: "O problema é simples: você adia."
Depois: "O problema é simples — você adia. A síntese é esta: rotina antes de intensidade."

### 3.6) REWRITE_PUNCT_MINIMAL (gate de pontuação)
Quando usar: PunctuationGate falha (':' >1, '—' >1, punch fora de [2.0,4.0]/100w).

**Ação:**
- Reduzir dois-pontos para máximo 1 (manter apenas na síntese principal).
- Reduzir travessões para máximo 1 (manter apenas no contraste principal).
- Ajustar punch para [2.0,4.0]/100w se necessário.
- Alteração mínima: preservar conteúdo, ajustar pontuação.

**Pseudoprompt:**
```
[REWRITE_PUNCT_MINIMAL]
- Máximo 1 ":" por fewshot (síntese principal).
- Máximo 1 "—" por fewshot (contraste principal).
- Punch density: [2.0,4.0]/100w.
- Alteração mínima: preserve conteúdo, ajuste pontuação.
```

**Mini-exemplo:**
```
Antes: "O ponto é: clareza primeiro — intensidade depois — e consistência sempre."
Depois: "O ponto é: clareza primeiro, intensidade depois e consistência sempre."
```

### 3.7) REWRITE_LEXICON (whitelist/redlist)
Quando usar: LexicalCompliance < alvo ou redlist > 0.

Ação
Substituir promo-speak por verbos de ação e substantivos concretos.
Reforçar whitelist com naturalidade (sem spam de conectores).

Pseudoprompt
[REWRITE_LEXICON]
- Remova termos promocionais (ex.: imperdível, exclusivo).
- Prefira verbos concretos (executar, medir, comparar) e nomes específicos.
- Use conectores-whitelist de forma moderada (≤ 40% dos parágrafos).

Mini-exemplo
Antes: “Oferta imperdível para revolucionar sua rotina.”
Depois: “Proposta direta: troque uma hora de rolagem por trinta minutos de leitura útil.”

### 3.8) REWRITE_TRANSITIONS (conectores e fluidez)
Quando usar: TransitionSpam ou ausência de pontes entre ideias.

Ação
Rotacionar conectores (“rapaziada”, “olha só”, “o ponto é:”, “sem rodeio:”).
Reduzir frequência para ≤ 40% dos parágrafos.

Pseudoprompt
[REWRITE_TRANSITIONS]
- Substitua conectores repetidos.
- Use no máximo 1 conector a cada 2 parágrafos.
- Prefira transições implícitas via verbo ou pergunta curta quando possível.

Mini-exemplo
Antes: “Olha só… Olha só… Olha só…”
Depois: “Olha só… O ponto é: … Sem rodeio: …”

### 3.9) REWRITE_ORIGINALITY (anti-colagem)
Quando usar: ngram_overlap ≥ 12 ou cos_sim > 0.92 com janelas do corpus.

Ação
Mudar a ótica da frase (ordem dos elementos, voz ativa/passiva, foco).
Introduzir variação sintática e metáfora nova sem alterar o sentido.

Pseudoprompt
[REWRITE_ORIGINALITY]
- Reescreva mantendo o significado, trocando estrutura e ordem dos termos.
- Evite qualquer sequência de 12 palavras idênticas ao corpus.
- Após reescrever, verifique overlap n-gram e cos_sim novamente.

Mini-exemplo
Antes: “Sem rodeio: clareza antes de intensidade.”
Depois: “Vamos ser claros: intensidade sem clareza só atrasa o jogo.”

### 3.10) REWRITE_IA_PATTERNS (anti-padrões de IA genérica)
Quando usar: detecção de padrões típicos de IA genérica (≥ 12% das sentenças).

**Ação:**
- Substituir moldes sintáticos banidos por conectores whitelist
- Converter voz passiva inflada em voz ativa
- Trocar clichês por expressões concretas e diretas

**Pseudoprompt:**
```
[REWRITE_IA_PATTERNS]
- Substitua padrões de IA genérica por conectores whitelist ("Na prática:", "Sem rodeio:", "O ponto é:")
- Converta voz passiva em voz ativa quando possível
- Troque clichês por exemplos concretos
- Mantenha significado, mude apenas a forma
```

**Mini-exemplos:**
```
Antes: "É importante ressaltar que, no cenário atual, a tecnologia é fundamental."
Depois: "Na prática: tecnologia resolve problemas reais — não é só ferramenta."

Antes: "À medida que o mundo evolui, observa-se que cada vez mais pessoas..."
Depois: "O ponto é: pessoas mudam comportamento quando veem resultado concreto."
```

### 3.11) REWRITE_HUMANIZE (tom conversa + clareza factual)
Quando usar: HumanScore < 0.75 (texto muito formal ou robótico).

**Ação:**
- Aumentar uso de pronomes de 2ª pessoa ("você", "ele", "ela")
- Simplificar estrutura SVOC (sujeito-verbo-objeto-complemento)
- Reduzir orações subordinadas excessivas
- Adicionar verbos e substantivos concretos
- Eliminar linguagem formal excessiva

**Pseudoprompt:**
```
[REWRITE_HUMANIZE]
- Use mais "você", "ele", "ela" para criar tom de conversa
- Simplifique frases: sujeito-verbo-objeto direto
- Reduza orações subordinadas (máx. 1 por frase)
- Adicione verbos concretos: executa, mostra, corta, publica
- Elimine linguagem formal desnecessária
- Mantenha clareza factual com leveza
```

**Mini-exemplos:**
```
Antes: "A implementação da solução foi realizada com base nos parâmetros estabelecidos."
Depois: "Você implementa a solução usando os parâmetros que definiu."

Antes: "É importante ressaltar que, considerando os aspectos mencionados anteriormente..."
Depois: "O ponto é: você precisa considerar o que já discutimos."
```

### 3.12) REWRITE_DECISIVE (anti-hedging excessivo)
Quando usar: HedgingGate > 10% (muitas frases com "talvez", "possivelmente", "pode ser").

**Ação:**
- Reduzir hedging desnecessário ("talvez" → "é", "pode ser" → "é")
- Manter apenas hedging justificado por incerteza real
- Aumentar tom decisivo e direto
- Preservar nuance quando necessário

**Pseudoprompt:**
```
[REWRITE_DECISIVE]
- Substitua "talvez", "possivelmente", "pode ser" por afirmações diretas quando apropriado
- Mantenha hedging apenas quando há incerteza real
- Use "é" em vez de "pode ser" para fatos estabelecidos
- Aumente tom decisivo sem perder precisão
```

**Mini-exemplos:**
```
Antes: "Talvez a IA possa ajudar na produtividade."
Depois: "A IA ajuda na produtividade quando você usa direito."

Antes: "Possivelmente, essa estratégia pode funcionar."
Depois: "Essa estratégia funciona quando você executa por 7 dias."
```

### 3.13) REWRITE_ACTIVE_VOICE (anti-voz passiva excessiva)
Quando usar: PassiveVoiceGate > 15% (muitas frases em voz passiva).

**Ação:**
- Converter voz passiva em voz ativa quando possível
- Manter voz passiva apenas quando o agente é irrelevante
- Aumentar clareza e direcionamento
- Preservar significado original

**Pseudoprompt:**
```
[REWRITE_ACTIVE_VOICE]
- Converta "foi feito por" em "você fez" ou "eles fizeram"
- Use "você" como sujeito quando apropriado
- Mantenha voz passiva apenas quando o agente é desconhecido/irrelevante
- Aumente clareza sem mudar significado
```

**Mini-exemplos:**
```
Antes: "A estratégia foi implementada com sucesso."
Depois: "Você implementou a estratégia com sucesso."

Antes: "Os resultados foram analisados pela equipe."
Depois: "A equipe analisou os resultados."
```

### 3.14) REWRITE_RHYTHM_VARIETY (anti-ritmo previsível)
Quando usar: PredictableRhythm > 18% (muitas sentenças no mesmo bucket de tamanho).

**Ação:**
- Variar comprimentos de frase (5-8, 15-20, 25-30 palavras)
- Quebrar padrões rítmicos previsíveis
- Criar burstiness natural (frases curtas + longas)
- Manter coesão sem monotonia

**Pseudoprompt:**
```
[REWRITE_RHYTHM_VARIETY]
- Varie comprimentos: 1 frase curta (5-8w) + 1 média (15-20w) + 1 longa (25-30w)
- Quebre padrões: evite 3 frases seguidas do mesmo tamanho
- Crie respiração: use frases curtas para impacto, longas para explicação
- Mantenha coesão sem ritmo robótico
```

**Mini-exemplos:**
```
Antes: "Você executa. Você mede. Você compara. Você ajusta."
Depois: "Você executa. Depois de uma semana testando, você mede o resultado e compara com o baseline anterior. Você ajusta."

Antes: "A estratégia funciona. A estratégia é simples. A estratégia é eficaz."
Depois: "A estratégia funciona. É simples: você escolhe uma métrica, executa por 7 dias e mede a diferença. Eficaz."
```

### 3.15) INJECT_DIRECT_ADDRESS (anti-calor desapegado)
Quando usar: LowWarmth < 1 ocorrência de 2ª pessoa por bloco OU > 3 ocorrências (anti-ressonância).

**Ação:**
- Ajustar para 1-3 ocorrências de "você", "ele", "ela", "nós" por bloco
- Adicionar endereçamento direto ("Cara", "Olha só")
- Injetar tom conversacional balanceado
- Manter naturalidade

**Pseudoprompt:**
```
[INJECT_DIRECT_ADDRESS]
- Substitua "é importante" por "você precisa"
- Adicione "Cara", "Olha só", "Entendeu?" quando apropriado
- Use "você" como sujeito em 60%+ das frases
- Mantenha tom conversacional sem forçar
```

**Mini-exemplos:**
```
Antes: "É importante definir métricas claras."
Depois: "Você precisa definir métricas que você entende."

Antes: "A execução deve ser consistente."
Depois: "Cara, você executa de forma consistente ou não executa."
```

### 3.16) REWRITE_SPONTANEOUS (anti-formalidade robótica)
Quando usar: RoboticFormality > 20% (muitos padrões explicativos previsíveis).

**Ação:**
- Quebrar padrões "É importante:", "Deve-se", "É necessário"
- Adicionar interjeições e aberturas espontâneas
- Variar estruturas de frase
- Injetar tom conversacional natural

**Pseudoprompt:**
```
[REWRITE_SPONTANEOUS]
- Substitua "É importante" por "Cara, você precisa"
- Adicione "Olha só:", "Beleza?", "Tá ligado?" quando apropriado
- Quebre padrões explicativos previsíveis
- Use variação sintática natural
```

**Mini-exemplos:**
```
Antes: "É importante ressaltar que a produtividade é fundamental."
Depois: "Cara, produtividade não é teoria — é o que você entrega."

Antes: "Deve-se considerar os aspectos técnicos."
Depois: "Olha só: os aspectos técnicos importam, mas você precisa ver o resultado."
```

### 3.17) INJECT_CREATIVE_SPARK (anti-falta de criatividade)
Quando usar: LowCreativity < 0.15 (pouca densidade criativa).

**Ação:**
- Adicionar analogias simples e funcionais
- Injetar contrastes sutis
- Usar metáforas leves
- Criar exemplos concretos e vívidos

**Pseudoprompt:**
```
[INJECT_CREATIVE_SPARK]
- Adicione analogia simples: "Como um mecânico que..."
- Use contraste funcional: "Não é X, é Y"
- Crie exemplo concreto: "Às 6h17, café amargo..."
- Mantenha criatividade sutil e útil
```

**Mini-exemplos:**
```
Antes: "A execução requer disciplina."
Depois: "Como um mecânico que testa uma peça por vez, você executa com disciplina."

Antes: "O planejamento é essencial."
Depois: "Não é planejamento complexo — é clareza do que você quer."
```

### 3.18) REWRITE_CONSEQUENCE_FOCUS (anti-orientação rígida)
Quando usar: RigidOrientation > 60% (muitos conselhos imperativos sem nuance).

**Ação:**
- Focar em consequências, não só conselhos
- Mostrar o efeito da ação
- Adicionar nuance e contexto
- Reduzir imperativos diretos

**Pseudoprompt:**
```
[REWRITE_CONSEQUENCE_FOCUS]
- Mostre o efeito: "Se você faz X, acontece Y"
- Foque em consequência: "O resultado mostra..."
- Adicione nuance: "Quando funciona, você vê..."
- Reduza imperativos diretos
```

**Mini-exemplos:**
```
Antes: "Execute a tarefa diariamente."
Depois: "Quando você executa diariamente, o resultado aparece em 7 dias."

Antes: "Meça seus resultados."
Depois: "Se você mede, você vê o que funciona — se não mede, você reza."
```

### 3.19) INJECT_QUESTIONS (anti-frase declarativa isolada)
Quando usar: FraseDeclarativaIsolada > 30% (muitas frases declarativas sem pergunta).

**Ação:**
- Adicionar perguntas diretas e retóricas
- Injetar questionamentos sobre consequências
- Criar engajamento conversacional
- Manter naturalidade

**Pseudoprompt:**
```
[INJECT_QUESTIONS]
- Adicione perguntas diretas: "O que acontece?", "Por que funciona?", "Entendeu?"
- Use perguntas retóricas: "O resultado?", "E aí?", "Tá ligado?"
- Foque em consequências: "Se você faz X, o que acontece?"
- Mantenha tom conversacional natural
```

**Mini-exemplos:**
```
Antes: "A produtividade aumenta com disciplina."
Depois: "A produtividade aumenta com disciplina. O que acontece? Você vê resultado em 7 dias."

Antes: "O planejamento é essencial."
Depois: "O planejamento é essencial. Por que? Porque clareza corta confusão."
```

### 3.20) REWRITE_STRUCTURE (macro-ordem, opcional)
Quando usar: parágrafos fora do esqueleto do formato (thread/artigo/roteiro).

Ação
Reordenar para Abertura → Caso → Tese → Lista → Fecho/CTA (ou esqueleto do formato).
Inserir subtítulos curtos e listas quando o bloco denso persistir.

Pseudoprompt
[REWRITE_STRUCTURE]
- Reorganize a seção seguindo o esqueleto do formato atual.
- Converta enumerações extensas em lista (3–7 itens).
- Mantenha coesão com conectores discretos.

### 3.12) Orquestração (ordem recomendada)
Macro: REWRITE_STRUCTURE (se necessário).
Anti-IA: REWRITE_IA_PATTERNS (se padrões detectados).
Humanização: REWRITE_HUMANIZE (se HumanScore < 0.75).
Decisão: REWRITE_DECISIVE (se HedgingGate > 10%).
Voz: REWRITE_ACTIVE_VOICE (se PassiveVoiceGate > 15%).
Ritmo: REWRITE_RHYTHM_VARIETY (se PredictableRhythm > 18%).
Calor: INJECT_DIRECT_ADDRESS (se LowWarmth < 35%).
Espontaneidade: REWRITE_SPONTANEOUS (se FormalidadeRobotica > 20%).
Mecânica: REWRITE_RHYTHM_VARIETY (se EscritaMecanica > 25%).
Criatividade: INJECT_CREATIVE_SPARK (se FaltaCriatividade > 0.30).
Consequência: REWRITE_CONSEQUENCE_FOCUS (se OrientacaoRigida > 25%).
Perguntas: INJECT_QUESTIONS (se FraseDeclarativaIsolada > 30%).
Cadência: REWRITE_CADENCE → REWRITE_HEAT.
Micro: REWRITE_PUNCH → REWRITE_TRANSITIONS → REWRITE_LEXICON.
Sanidade: REWRITE_ORIGINALITY + rechecagem dos gates.
Limite: máx. 3 passes por texto antes de reamostrar o RAG (aumentar k ou reduzir style_bias).

### 3.13) Pós-condições e verificações
Após aplicar qualquer modo:
Reexecutar SCORER nas seções alteradas.
Confirmar gates: Style ≥ 0.80, Lexicon ≥ 0.95, Heat ≥ 0.80, Punch ≥ 0.75, Originalidade OK.
Registrar actions_applied e novas métricas em resumo de calibração.

### 3.14) Checklist rápido (por seção)
 Sentidos preservados; sem fatos novos.
 1 frase longa (30–40) e 1 curta (≤10) após REWRITE_CADENCE.
 1 marca de calor por parágrafo após REWRITE_HEAT.
 : na síntese e — no contraste; 2.0–4.0/100w.
 Conectores ≤ 40% dos parágrafos; sem repetição tripla.
 redlist = 0; whitelist natural, sem spam.
 padrões de IA genérica ≤ 12% das sentenças.
 HumanScore ≥ 0.75 (tom conversa + clareza factual).
 HedgingGate ≤ 10% (frases com hedging excessivo).
 PassiveVoiceGate ≤ 15% (frases em voz passiva).
 PredictableRhythm ≤ 18% (sentenças no mesmo bucket).
 LowWarmth ≥ 35% (uso de 2ª pessoa).
 ngram_overlap < 12 e cos_sim ≤ 0.92.

Resumo do Tópico 3: o REWRITER é o braço operacional do SCORER. Ele corrige o desvio com cirurgia mínima, mantendo o texto autoral, coeso e no seu som de voz.

::contentReference[oaicite:0]{index=0}

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

## Tópico 4 — Presets por Formato & Perfis (alvos, pesos e exceções)

> Objetivo: definir **alvos de métrica** e **pesos do StyleScore** por **formato** (thread, artigo, roteiro) e por **perfil de uso** (informar, orientar, convencer, CTA) — incluindo exceções e regras de ajuste automático.

---

### 4.1) Matriz de formatos × perfis

| Formato \ Perfil | **Informar** | **Orientar** | **Convencer** | **CTA** |
|---|---:|---:|---:|---:|
| **Thread** | \- | **Padrão** | ▲ Heat | ▲ Punch |
| **Artigo** | **Padrão** | \- | ▲ Heat + Cadence | ▲ Punch |
| **Roteiro** | \- | **Padrão** | ▲ Heat | ▲ Heat + Punch |

**Lendas:**  
- **Padrão** = preset base do formato (tabela 4.2).  
- **▲** = elevar alvo/intervalo levemente (detalhado nas seções abaixo).  

---

### 4.2) Presets base por formato (alvos + pesos do StyleScore)

| Métrica / Formato | **Thread** | **Artigo** | **Roteiro** |
|---|---:|---:|---:|
| **avg_sentence_len** | 16–20 | 18–22 | 16–20 |
| **burstiness (coef.)** | 0.65–0.85 | 0.60–0.80 | 0.70–0.90 |
| **heat_target** | 3 | 3 | 3–4 |
| **transitions_ceiling** | ≤ 40% | ≤ 35% | ≤ 45% |
| **punch_range_per_100w** | 2.0–4.0 | 2.0–4.0 | 2.0–4.0 |

→ Presets calibrados com base nas métricas do CORPUS (cadência≈18, punch≈2.8, heat≈3.1).
| **Heat alvo (médio)** | 3 | 3 | 3–4 |
| **Punch (/100w)** | 2.0–4.0 | 2.0–4.0 | 2.0–4.0 |
| **Transitions densidade** | ≤ 40% parágrafos; aplicar ConnectorRotation | ≤ 35%; aplicar ConnectorRotation | ≤ 45%; aplicar ConnectorRotation |
| **Pesos StyleScore** | 0.35 Cdc · 0.20 Heat · 0.20 Lex · 0.15 Punct · 0.10 Outros | 0.30 Cdc · 0.25 Heat · 0.20 Lex · 0.20 Punct · 0.05 Outros | 0.40 Cdc · 0.15 Heat · 0.20 Lex · 0.20 Punct · 0.05 Outros |

> **Cdc** = CadenceScore; **Lex** = LexicalCompliance; **Punct** = PunctuationFit.

---

### 4.3) Ajustes por perfil de uso

#### a) **Informar** (didático neutro)
- **Heat**: manter 3 (picos 4 apenas na *virada de tese*).  
- **Punch**: meio da faixa; priorizar “:`” em síntese e reduzir “—” se soar teatral.  
- **Ação SCORER**: elevar peso de **Lexicon** em +0.05 se houver jargão (exigir glossário inline).

#### b) **Orientar** (guia prático)
- **Heat**: 3 (1 marca de calor por parágrafo).  
- **Cadence**: garantir 1 frase curta (≤10) com imperativo por seção.  
- **Ação SCORER**: se `Punch < 2.0`, sugerir `REWRITE_PUNCH` em sínteses.

#### c) **Convencer** (opinião/ensaio)
- **Heat**: alvo **3.2–3.8** com pico 4 controlado.  
- **Cadence**: permitir 1–2 frases longas (30–40) para argumento; manter burstiness ≥ 0.65.  
- **Ação SCORER**: aumentar peso de **Heat** em +0.05 e de **Cadence** em +0.05 (tirar de “Outros”).

#### d) **CTA** (chamada à ação)
- **Punch**: topo da faixa (até limite superior).  
- **Heat**: pico 4 no parágrafo final.  
- **Ação SCORER**: checar **PunctuationFit ≥ 0.80** e presença de verbo de ação claro no fecho.

---

### 4.4) Subpresets por **seção** (layout interno)

| Seção | Thread | Artigo | Roteiro |
|---|---|---|---|
| **Abertura** | Heat 3; 1 conector opcional | Heat 3; frase média 18–20 | Heat 3–4; fala curta e direta |
| **Caso/Exemplo** | 1 detalhe sensorial | 1 anedota breve | 1 cena concreta |
| **Tese** | 1 frase longa (30–36) | 1–2 frases longas | 1 frase longa, 1 curta |
| **Lista/Coluna** | 3–5 itens; frases curtas | 3–7 itens; mix curto/longa | 3–5 falas; cadência alta |
| **Fecho/CTA** | Heat 4; verbo de ação | Heat 3–4; síntese com “:” | Heat 4; instrução clara |

> O SCORER avalia **por seção**; o REWRITER atua **onde** a seção escapa do preset.

---

### 4.5) Exceções e tolerâncias

- **Texto muito curto (< 150 palavras)**  
  - Relaxar `HeatCurveMatch` em **−0.05** (curvas ficam discretas).  
  - Manter `Punch` dentro da faixa, mas **peso Punct +0.05**.

- **Texto muito longo (> 1200 palavras)**  
  - Tolerância de `avg_sentence_len` **±1**.  
  - Exigir **2 picos** (virada e fecho) em Heat; se ausente, `REWRITE_HEAT`.

- **Tema técnico com glossário**  
  - Se jargão ≥ 3/100w, `LexicalCompliance` sobe peso +0.05 e exige **glossário inline**.

- **Tom confessional**  
  - Permitir Heat médio **2.5–3.5** com picos **curtos**; reforçar `REWRITE_ORIGINALITY` (evitar eco de memórias do corpus).

---

### 4.6) Regras de recalibração automática (auto-tuning leve)

```python
if profile == "convencer":
    weights["Heat"] += 0.05; weights["Cadence"] += 0.05; weights["Outros"] -= 0.10

if format == "roteiro" and cadence_score < 0.78:
    suggest("REWRITE_CADENCE", section="tese|fecho")

if format == "thread" and punct_density < 2.0:
    suggest("REWRITE_PUNCH", section="fecho")

if profile == "CTA" and heat_peak < 4:
    suggest("REWRITE_HEAT", section="fecho")

### 4.7) Checklists rápidos por formato

Thread
 avg_sentence_len ∈ 16–20
 Burstiness ≥ 0.65
 Heat 3; pico 4 no fecho/CTA
 Punch 2.0–4.0/100w
 Conectores ≤ 40%

Artigo
 avg_sentence_len ∈ 18–22
 Burstiness 0.60–0.80
 Heat 3; pico 4 na virada de tese
 Punch 2.0–4.0/100w
 Conectores ≤ 35%

Roteiro
 avg_sentence_len ∈ 16–20
 Burstiness 0.70–0.90
 Heat 3–4 (picos curtos)
 Punch 2.0–4.0/100w
 Conectores ≤ 45%

 4.8) Por que esse tópico importa
Evita que um mesmo texto seja julgado com régua errada.
Mantém a identidade de voz respeitando a intenção do formato e do perfil.
Reduz reescritas desnecessárias e melhora a previsibilidade do pipeline.

Resumo do Tópico 4: presets por formato × perfil alinham o SCORER com o objetivo comunicacional. A voz continua sua, mas a régua muda conforme a peça — sem perder consistência.

::contentReference[oaicite:0]{index=0}

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

## Tópico 5 — Originalidade & Anti-colagem (detecção, thresholds e ações)

> Objetivo: garantir que a saída seja **100% original**, mesmo quando condicionada por `RAG_FEWSHOTS`.  
> Este tópico define **como medir**, **quando reprovar** e **como reescrever** para eliminar sobreposição indevida com o `/CORPUS/`.

---

### 5.1) Escopo e princípios

1) **Estilo ≠ conteúdo** — o SCORER mede semelhança **lexical e semântica** com o banco, não “inspiração estilística”.  
2) **Mínimo necessário** — usar apenas sinais de cadência; qualquer eco literal significativo reprova.  
3) **Camadas** — checagem por **n-grams**, **semântica** (embeddings), **estrutura** (ordem sintática) e **variantes** (BLEU/ROUGE).

---

### 5.2) Métricas de originalidade (por parágrafo e global)

| Métrica | Como calcula | Limite (reprova) | Observação |
|---|---|---|---|
| **n-gram overlap (3–12)** | Maior sequência idêntica com qualquer janela do `/CORPUS/` | **≥ 12** palavras consecutivas | 8–11 = alerta → reescrever |
| **cos_sim_max** | Máx. similaridade de embeddings com janelas mais próximas | **> 0.92** | 0.88–0.92 = zona cinza (ver ROUGE) |
| **ROUGE-L_max** | Maior similaridade de subsequência longa | **> 0.65** | Usa após cos_sim alto |
| **BLEU_max** | BLEU contra top-k vizinhos | **> 0.55** | Sinal de paráfrase próxima |
| **NoveltyScore** | `1 − max_sim` (LSH/ANN) | **< 0.20** | Texto muito colado no banco |
| **Diversity intra-doc** | Jaccard entre parágrafos | **> 0.75** (muitos iguais entre si) | Sinal de autocolagem |

> **Regra geral de reprovação:** (n-gram ≥ 12) **ou** (cos_sim > 0.92 **e** ROUGE-L > 0.65) **ou** (BLEU > 0.55).  

---

### 5.3) Pipeline de verificação (ordem recomendada)

1) **Filtro rápido n-gram (3–12)**  
2) **Top-k vizinhos semânticos** (k=10) por embeddings  
3) **Confirmação por ROUGE-L** nas correspondências > 0.88  
4) **BLEU** para suspeitas restantes  
5) **NoveltyScore** global do documento  
6) **Diversity intra-doc** (evita repetição da própria saída)

**Pseudocódigo**
```python
ng = ngram_overlap_max(text, corpus)
if ng >= 12: fail("NearCopy")

candidates = topk_semantic(text, corpus, k=10)
sim = max_cos(candidates)

if sim > 0.92 and rougeL(text, argmax(candidates)) > 0.65:
    fail("NearCopy")
elif bleu(text, argmax(candidates)) > 0.55:
    fail("ParaphraseClose")

if novelty(text, corpus) < 0.20:
    warn("LowNovelty")

### 5.4) Exceções seguras (quando não é colagem)
Frases utilitárias curtas (≤ 7 palavras) de uso comum: “vamos lá”, “o ponto é”, “sem rodeio”, etc.
Vocabulário técnico inevitável (termos únicos) se houver glossário inline.
Citações claramente marcadas como citação (com fonte autorizada) — não confundir com RAG de estilo.

### 5.5) Ações automáticas (REWRITER) por violação
| Violação                                     | Ação principal                                                      | Ações auxiliares                                                             |
| -------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `NearCopy` (n-gram ≥12)                      | `REWRITE_ORIGINALITY` (trocar estrutura, foco, ordem)               | `REWRITE_CADENCE` (variar ritmos); `REWRITE_PUNCH` (mudar pontos de síntese) |
| `ParaphraseClose` (cos_sim/ROUGE/BLEU altos) | `REWRITE_ORIGINALITY` (metáfora nova + voz ativa/passiva alternada) | `REWRITE_LEXICON` (substituições por verbos concretos)                       |
| `LowNovelty` (novelty<0.20)                  | Aumentar `k` no RAG e reduzir `style_bias` (−0.1)                   | Inserir 1 few-shot **sintético** (peso 0.3)                                  |
| `SelfSimilarityHigh` (Jaccard intra-doc)     | `REWRITE_STRUCTURE` (quebrar/mesclar parágrafos)                    | `REWRITE_CADENCE`                                                            |

Pseudoprompt resumido — REWRITE_ORIGINALITY
- Preserve o sentido e as evidências.
- Refaça a frase mudando a ordem dos elementos, o foco e a voz (ativa↔passiva).
- Introduza 1 metáfora ou imagem **nova**, sem repetir padrões do corpus.
- Evite qualquer sequência de 12 palavras idênticas ao banco.

### 5.6) Interação com o RAG (prevenção na origem)
CONSTRAINT interna (no RAG_FEWSHOTS):
“Imitar cadência/lexicon; não copiar frases na saída final.”
Peso do estilo (style_bias): começar em 0.7; reduzir para 0.6 se houver reprovação recorrente.
Diversidade de janelas: garantir MMR com λ=0.7 para evitar um único “molde”.

### 5.7) Estratégias de reescrita guiada (templates rápidos)

Mudança de ótica
Antes: “Sem rodeio: clareza antes de intensidade.”
Depois: “Vamos ser claros: intensidade sem clareza vira barulho.”

Deslocamento de foco
Antes: “Você confunde movimento com avanço.”
Depois: “Movimento não é avanço — é só barulho bem organizado.”

Variação sintática
Antes: “Escolhe uma métrica, executa 7 dias e compara.”
Depois: “Escolha uma métrica. Execute por 7 dias. Compare o resultado.”

Metáfora original
Antes: “A audiên
Depois: “Audiência é termômetro de bolso: sobe quando o bolso esquenta.”

(5.8) Checkpoints e gates finais
Gate 1 — n-gram: < 12 em todo o doc e por parágrafo.
Gate 2 — semântica: cos_sim_max ≤ 0.92.
Gate 3 — ROUGE-L: ≤ 0.65.
Gate 4 — BLEU: ≤ 0.55.
Gate 5 — Novelty: ≥ 0.20.
Gate 6 — Diversity intra-doc: Jaccard ≤ 0.75.
Se qualquer gate falhar → reprovar, aplicar REWRITER apenas nas seções afetadas e reavaliar.

(5.9) Relatórios e auditoria (EVAL)
Registrar por execução:
{
  "run_id": "2025-10-13T10:20:00Z",
  "originality": {
    "ngram_overlap_max": 8,
    "cos_sim_max": 0.87,
    "rougeL_max": 0.48,
    "bleu_max": 0.39,
    "novelty_doc": 0.44,
    "self_similarity_jaccard": 0.41
  },
  "actions": ["REWRITE_ORIGINALITY@sec2", "REWRITE_CADENCE@sec2"],
  "status": "approved"
}

Agregados semanais devem listar taxa de reprovação por near-copy e impacto das correções (queda média de cos_sim e ROUGE-L).
### 5.10) Checklist rápido (antes de aprovar)
 Nenhum trecho com ≥ 12 palavras idênticas ao corpus.
 cos_sim_max ≤ 0.92 e ROUGE-L ≤ 0.65.
 BLEU ≤ 0.55.
 Novelty ≥ 0.20; diversidade entre parágrafos ok.
 Reescritas preservam sentido e estrutura lógica.
 Relatório de execução gerado para colar no .md.

 Resumo do Tópico 5: originalidade não é um acaso — é um processo medido.
Com gates claros e reescrita dirigida, o texto mantém seu som de voz, sem ecoar o banco.

::contentReference[oaicite:0]{index=0}

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

## Tópico 6 — Telemetria, Relatórios & Integração com EVAL

> Objetivo: padronizar **como o SCORER registra métricas, violações e reescritas**, consolidando tudo em relatórios para análise de qualidade, tuning e detecção de drift.

---

### (6.1) Estrutura de blocos markdown (GPT Plus)
📁 estilometria-agent/
├── eval_plan.md # metas/rotinas de teste e critérios de aprovação
├── probes.txt # prompts fixos para regressão (semente estável)
├── aggregates(dados internos em memória GPT Plus) # métricas agregadas (dia/semana/mês)
├── optout_resumo de calibração(dados internos em memória GPT Plus) # remoções do CORPUS (PII/licenças)
└── 📁 relatórios/ (gerados sob demanda)
├── 2025-10-13_10-30-21(dados internos em memória GPT Plus)
└── ...

---

### (6.2) Esquema de relatório por execução (gerado sob demanda)

```json
{
  "run_id": "2025-10-13_10-30-21",
  "source": {
    "file": "artigo_midia_2025-10-13.md",
    "format": "artigo",
    "profile": "informar",
    "probe_id": "P001"
  },
  "rag": {
    "k": 24,
    "style_bias": 0.70,
    "selected_windows": ["a1b2_005", "a1b2_011"],
    "synthetic_ratio": 0.00
  },
  "style_plan": {
    "avg_sentence_len_target": [18,22],
    "burstiness_target": "alto",
    "heat_target": 3,
    "punch_target_per_100w": [2.0,4.0],
    "transitions_whitelist": ["rapaziada","olha só","o ponto é:","sem rodeio:"]
  },
  "scores": {
    "Style": 0.84,
    "Cadence": 0.83,
    "Heat": 0.81,
    "Lexicon": 0.98,
    "Punch": 0.78
  },
  "originality": {
    "ngram_overlap_max": 8,
    "cos_sim_max": 0.86,
    "rougeL_max": 0.48,
    "novelty_doc": 0.44,
    "self_similarity_jaccard": 0.41
  },
  "violations": ["PunchUnderuse"],
  "rewriter": {
    "actions": ["REWRITE_PUNCH@secao_sintese"],
    "delta": {"Punch": "+0.09", "Style": "+0.02"}
  },
  "gates": {"approved": true, "failed": []}
}
```

### (6.3) Métricas-chave (KPIs de qualidade)

#### **Primários**
- StyleScore_médio (≥ 8.0)
- HumanizationIndex_médio (≥ 8.5)
- HeatCurveMatch_médio (≥ 7.0) (↑ leve peso para presença de detalhe sensorial contextual)
- LexicalCompliance_médio (≥ 0.96; redlist=0)
- PunctuationFit_médio (≥ 0.75; 2.0–4.0 por 100w; pelo menos 1 "punch sentence" por parágrafo)

#### **Originalidade**
- ngram_overlap_max (< 12)
- cos_sim_max (≤ 0.92)
- ROUGE-L_max (≤ 0.65)
- reprovações_por_nearcopy_rate (→ ideal < 5%)

#### **Operacionais**
- avg_rewrites_per_doc (≤ 2.0)
- pass_at_1 (≥ 60%) / pass_at_2 (≥ 85%)
- tempo_médio_por_pass (benchmark interno)

(6.4) Agregados semanais (aggregates(dados internos em memória GPT Plus))
{
  "period": "W42-2025",
  "counts": {"runs": 46, "approved": 41, "failed": 5},
  "means": {"Style":0.833,"Cadence":0.812,"Heat":0.804,"Lexicon":0.979,"Punch":0.766},
  "stdevs": {"Style":0.018,"Cadence":0.024,"Heat":0.021,"Lexicon":0.007,"Punch":0.026},
  "originality": {"nearcopy_rate": 0.043, "cos_sim_p95": 0.90, "ngram_max_p95": 10},
  "rewrites": {"avg_per_doc": 1.7, "top_modes": ["REWRITE_PUNCH","REWRITE_CADENCE"]},
  "notes": "Melhorar ':' em sínteses de artigo; revisar whitelist para novos conectores."
}

(6.5) Detecção de drift (alertas)
Condições de alerta (disparar issue de tuning):
StyleScore_médio ↓ ≥ 0.03 vs. média das últimas 4 semanas.
nearcopy_rate ↑ ≥ 0.05 absoluto na semana.
Punch fora da faixa em ≥ 25% dos documentos do formato artigo.
CadenceScore < 0.78 por 3 semanas em roteiro.

Ações automáticas sugeridas:
Reduzir style_bias em −0.05 e aumentar k em +6.
Ajustar peso de PunctuationFit +0.05 (formato impactado).
Reexecutar probes.txt completo e comparar deltas.

(6.6) Painéis de leitura rápida (templates)
Dashboard Semanal (resumo)
Cards: Style (média), Cadence, Heat, Lexicon, Punch.
Sparklines de 4 semanas para cada métrica.
Top 3 violações e sua frequência.
Tabela de nearcopy cases (run_id, seção, ação aplicada).

Dashboard de Originalidade
Histogramas de cos_sim_max e ngram_overlap_max.
Scatter: cos_sim_max × ROUGE-L_max.
Linha do tempo de nearcopy_rate.

(6.7) Integração com probes.txt (regressão)
Formato do bloco markdown:
# id; tema; objetivo; formato; heat; notas
P001; "mídia esportiva e audiência"; informar; artigo; 3; "bastidor, sem conspiratório"
P002; "rotina em dias difíceis"; orientar; thread; 3; "detalhe sensorial"
P003; "consumo de status"; convencer; artigo; 4; "humor ácido controlado"
P004; "masculinidade prática"; orientar; thread; 3; "evitar moralismo"
P005; "IA e trabalho"; informar; artigo; 3; "glossário inline"

Procedimento
1. Rodar probes com semente fixa ao fechar sprint/tuning.
2. Gerar relatório markdown; consolidar em resumo de calibração.
3. Comparar com baseline (primeira execução aprovada).
4. Se métrica cair além da tolerância → rollback e issue.

### 6.8) Opt-out, PII e ética (interação com resumo de calibraçãos)
Qualquer run reprovado por PII/Redlist deve marcar gates.approved=false e incluir motivo explícito.
optout_resumo de calibração(dados internos em memória GPT Plus) deve conter {window_id, motivo, timestamp, actor} sempre que uma janela do CORPUS for removida.
Nunca registrar PII no resumo de calibração; use máscaras (***@***.***, ***.***.***-**).

### 6.9) Rotina semanal recomendada
Coleta: consolidar runs → aggregates(dados internos em memória GPT Plus).
Análise: checar KPIs e violações mais comuns.
Tuning leve: ajustar 1–2 parâmetros (ex.: punch_range, style_bias).
Regressão: rodar probes.txt; comparar com baseline.
Notas: atualizar eval_plan.md com decisões e próximos passos.

### 6.10) Checklist de Telemetria
 Todas as execuções com run_id ISO e metadados (format, profile).
 Scores completos + flags de originalidade.
 Ações do REWRITER registradas com deltas de métrica.
 Agregados semanais atualizados.
 Alertas de drift avaliados e documentados em eval_plan.md.
 Nenhum dado sensível nos resumo de calibraçãos.

 Resumo do Tópico 6: Telemetria bem feita transforma “achismo de estilo” em gestão de qualidade.
Você enxerga tendências, previne drift e ajusta o sistema sem perder o som da fala.

::contentReference[oaicite:0]{index=0}

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

## Tópico 7 — Humanization Index v6.0

> Objetivo: quantificar o "humano plausível" do texto e acionar correções automáticas quando o estilo cair em padrões típicos de IA.

### Categorias & Pesos (0–100)
| Código | Categoria | Peso |
|--------|------------|-----:|
| falta_criatividade | Falta de criatividade | 14 |
| escrita_mecanica | Escrita mecânica | 12 |
| ritmo_previsivel | Ritmo previsível | 10 |
| sintaxe_monotona | Sintaxe monótona/previsível | 10 |
| formalidade_robotica | Formalidade robótica | 10 |
| calor_desapegado | Calor desapegado | 12 |
| orientacao_rigida | Orientação rígida | 8 |
| falta_complexidade | Falta de complexidade | 10 |
| vocabulario_utilitario | Vocabulário utilitário | 8 |
| falta_variacao_emocional | Falta de variação emocional | 6 |
| **Total** |  | **100** |

### Cálculo
```
contrib_i = (1 - risk_i) * peso_i
HumanizationIndex = Σ contrib_i # 0–100
```

### Faixas de decisão
- ≥85 → Ótimo
- 75–84 → Bom
- 65–74 → Atenção
- <65 → Reprova (reescrita automática)

### Comandos principais
- `/HUMANIZE_SCORE_TEXT`
- `/HUMANIZE_ENFORCE`
- `/HUMANIZE_SCORE_CALIBRATE`
- `/HUMANIZE_AUDIT_BATCH`

---

## Tópico 8 — Humanization Hook (Auto-Trigger v1.0)

> Objetivo: acionar automaticamente o processo de humanização após qualquer geração de texto que retorne StyleScore ou HumanizationIndex abaixo de 75.

### Lógica
1. Após cada geração, capturar os valores:  
   - **StyleScore** (0–100)  
   - **HumanizationIndex** (0–100)
2. Se qualquer um for **< 75**, executar:  
   ```
   /HUMANIZE_ENFORCE
   args: { texto: "<texto>", modo: "auto" }
   ```
3. Se o resultado final ainda for **< 85**, executar reforço:  
   ```
   /HUMANIZE_ENFORCE
   args: { texto: "<texto>", modo: "assistido" }
   ```

### Flags automáticas
- Ativa apenas em modos `longform`, `materia`, `ensaio` ou `resposta_expandida`
- Ignora textos com menos de **80 palavras**
- Integração direta com `/HUMANIZE_SCORE_TEXT` para logging

### Logs gerados
Cada iteração grava um registro em:
```
logs/humanization_autofix.log
```

Estrutura:
```
[timestamp] [file_id] [StyleScore_before→after] [HumanizationIndex_before→after] [modo]
```

### Notificação
Se após 2 iterações consecutivas o score continuar < 75, acionar:
```
/HUMANIZE_REPORT
args: { folder: "EVAL/", reason: "persistent_low_score" }
```

### Benefício
- Elimina saídas "robóticas" antes da entrega.  
- Garante tom humano, variação sintática e calor.  
- Mantém conformidade com métricas do Humanization Index v6.0.

---

## Tópico 9 — Humanization Analytics v1.2

> Objetivo: registrar e correlacionar a evolução de estilo, tom e índice de humanização em cada iteração do sistema.

---

### 1. Estrutura do Registro

Cada execução de `/HUMANIZE_SCORE_TEXT` ou `/HUMANIZE_ENFORCE` grava uma linha em:
```
logs/humanization_analytics.csv
```

Formato:
```
timestamp,file_id,StyleScore_before,StyleScore_after,HumanizationIndex_before,HumanizationIndex_after,mode,delta_score,delta_index
```

---

### 2. Cálculo de Delta

```
delta_score = StyleScore_after - StyleScore_before
delta_index = HumanizationIndex_after - HumanizationIndex_before
```

- Se `delta_score ≥ +10` → loga status: `IMPROVED`
- Se `delta_score < +10` e `>= 0` → loga status: `MINOR_CHANGE`
- Se `delta_score < 0` → loga status: `REGRESSION`

---

### 3. Módulo de Correlação

O sistema gera estatísticas automáticas a cada 100 logs:

```
/HUMANIZE_REPORT
args: { folder: "EVAL/", mode: "auto", summarize: "delta_trends" }
```

Indicadores:
- Média de aumento de StyleScore por categoria penalizada.
- Categoria mais recorrente de falha.
- Correlação entre "modo" (`auto` vs `assistido`) e melhoria percentual.

---

### 4. Flags de Auto-Ajuste

| Condição | Ação |
|-----------|------|
| Média de delta_score < +5 em 3 ciclos consecutivos | recalibrar pesos via `/HUMANIZE_SCORE_CALIBRATE` |
| >40% de textos reescritos em modo assistido | sugerir revisão manual da política |
| Score médio geral < 75 | ativar modo de reforço "warm_start" |

---

### 5. Modo Warm Start

> Quando ativado, injeta automaticamente um pre-fewshot de cadência humana antes da geração.

```
HUMANIZE_WARM_START = true
HUMANIZE_WARMSHOT_PATH = "fewshots/human_warm_cadence.txt"
```

Esse recurso garante que o modelo "ouça" cadências humanas antes de escrever — reduzindo formalismo e rigidez no primeiro rascunho.

---

### 6. Objetivo Global

- Consolidar métricas de melhoria real de estilo.
- Criar rastreabilidade entre versões IA → humanizada.
- Permitir auditoria quantitativa do progresso do agente.

---
**Status:** ativo por padrão.  
**Sincronização:** executado a cada iteração de humanização automática.

---

## Tópico 10 — Guia de Uso End-to-End & Checklists Finais

> Objetivo: padronizar **como usar o SCORER no fluxo completo**, do `RAG_FEWSHOTS` ao **OK final**, com exemplos, playbooks e listas de verificação para reduzir retrabalho.

---

### 7.1) Pipeline resumido (orquestração)

[03_RAG_STYLE] → STYLE_PLAN + RAG_FEWSHOTS
↓
[GERADOR] → rascunho_v1
↓
[04_SCORER] → scores + gates + fix_suggestions
↓
[REWRITER] → rascunho_v2 (até passar)
↓
[EVAL] → resumo de calibraçãos/aggregates + probes (regressão)


**Regra de iteração:** máximo **3 passes** de reescrita antes de reamostrar RAG (↑k, ↓style_bias).

---

### 7.2) Playbook padrão (passo a passo)

1) **Receber o STYLE_PLAN** (alvos por formato/perfil) do `03_RAG_STYLE`.  
2) **Rodar SCORER** no rascunho_v1.  
3) **Se gates falharem**, aplicar **1–3 modos do REWRITER** (Tópico 3) **somente** nas seções apontadas.  
4) **Reexecutar SCORER** → aceitar se todos os gates ok.  
5) **Registrar** em relatórios e atualizar agregados semanais.

---

### 7.3) Exemplo end-to-end (artigo • “informar”)

**STYLE_PLAN (resumo)**
```json
{
  "format": "artigo",
  "avg_sentence_len_target": [18,22],
  "burstiness_target": "alto",
  "heat_target": 3,
  "punch_target_per_100w": [2.0,4.0],
  "transitions_whitelist": ["olha só", "o ponto é:", "sem rodeio:"],
  "redlist_hard": true
}

Scores v1 (SCORER)
{"Style":0.77,"Cadence":0.74,"Heat":0.82,"Lexicon":0.98,"Punch":0.62,
 "originality":{"ngram_max":8,"cos_sim_max":0.87,"rougeL_max":0.46}}

Violações: CadenceLow, PunchUnderuse
Ações: REWRITE_CADENCE@secao_2, REWRITE_PUNCH@sintese

Scores v2
{"Style":0.84,"Cadence":0.83,"Heat":0.81,"Lexicon":0.98,"Punch":0.78}

Status: ✅ aprovado (relatório gerado)

### 7.4) Critérios de aceite (OK-to-ship)
StyleScore ≥ 0.80 (ou preset do formato).
LexicalCompliance ≥ 0.95 e redlist = 0.
HeatCurveMatch ≥ 0.80 (curva respeita seção de virada e fecho).
PunctuationFit ≥ 0.75 e punch dentro da faixa do formato.
Originalidade: ngram<12, cos_sim≤0.92, ROUGE-L≤0.65.
Transições: ≤ 40% dos parágrafos; sem repetição tripla.
Checklist de seção (Tópico 4.4) atendida.

### 7.5) Troubleshooting (erros comuns → solução)
| Sintoma                       | Provável causa          | Solução objetiva                                          |
| ----------------------------- | ----------------------- | --------------------------------------------------------- |
| Texto “plano”, sem respiração | Burstiness baixo        | `REWRITE_CADENCE` (1 longa 30–40 + 1 curta ≤10 por seção) |
| Fecho fraco                   | Heat final baixo        | `REWRITE_HEAT@fecho` + verbo de ação; checar Punch        |
| Excesso de “:”/“—”            | Overuse de punch        | `REWRITE_PUNCH` (mover contraste p/ verbo/pergunta)       |
| Tom caricatural               | Transitions spam        | `REWRITE_TRANSITIONS` e reduzir `transitions_bias`        |
| Reprova por near-copy         | Similaridade com janela | `REWRITE_ORIGINALITY` + reamostrar RAG (↑k, ↓style_bias)  |
| Jargão confunde               | Glossário ausente       | `REWRITE_LEXICON` (glossário inline curto)                |

### 7.6) Integração com 02_PROMPT_SKELETONS.md (pós-geração)
Se o esqueleto não foi seguido (ex.: faltou “Lista/Coluna”), aplicar REWRITE_STRUCTURE.
Em thread/roteiro, reforçar frases curtas nas falas/itens; manter 1 pico de heat.

### 7.7) Integração com 03_RAG_STYLE.md (prevenção)
style_bias alto e reprovação recorrente por originalidade → reduzir −0.05 ~ −0.1.
Pouca aderência de cadência → aumentar k e priorizar janelas com stdev_sentence_len alto.
Falta de conectores naturais → revisar whitelist.txt e few-shots sintéticos (Tópico 4 do RAG).

### 7.8) Templates prontos de ação (copiar/colar)
A) Reforçar cadência (artigo)
[REWRITE_CADENCE]
- Mantenha sentido.
- Nesta seção, insira 1 frase longa (30–40) e 1 curta (≤10).
- Varie inícios: verbo, pergunta, advérbio.

B) Ajustar heat (convencer)
[REWRITE_HEAT]
- Traga 1 pergunta direta por parágrafo.
- Concentre o pico (4/5) na virada de tese.
- Evite picos seguidos; média 3/5.

C) Corrigir punch (CTA/fecho)
[REWRITE_PUNCH]
- Use ":" na síntese do fecho e "—" no contraste principal.
- Mantenha 2.0–4.0 punches/100w.

D) Anti-colagem (qualquer formato)
[REWRITE_ORIGINALITY]
- Troque a ordem dos elementos; alterne voz ativa/passiva.
- Introduza 1 metáfora original.
- Evite sequência ≥ 12 palavras idênticas ao corpus.

### 7.9) Parâmetros default (referência rápida)
Cadence target (artigo): [18,22] • bônus stdev ≥ 5.5
Heat target: 3 (pico 4 na virada/fecho)
Punch/100w: artigo 2.0–4.0 • thread 2.0–4.0 • roteiro 2.0–4.0
Transitions: ≤ 35% (artigo), ≤ 40% (thread), ≤ 45% (roteiro); aplicar ConnectorRotation para evitar duplicação
Originalidade gates: ngram<12 • cos≤0.92 • ROUGE-L≤0.65
Passes máximos: 3 (antes de reamostrar RAG)

### 7.10) Checklist final (antes de entregar)
 StyleScore ≥ 0.80 e presets do formato atendidos.
 Originalidade OK (todos os gates).
 Heat com pico no lugar certo (virada/fecho).
 Punch usado com intenção (síntese/contraste).
 Léxico sem redlist; whitelist natural (sem spam).
 Relatórios salvos em relatórios e agregados atualizados.

 Resumo do Tópico 7: o SCORER vira procedimento operacional — do diagnóstico à aprovação final, com rotas claras de correção e métricas que garantem o som da fala de ponta a ponta.

 
::contentReference[oaicite:0]{index=0}

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

# 04_SCORER.md  
> Módulo de medição estilométrica e correção da voz.

---

## Tópico 11 — Calibração & Tuning (versão ChatGPT Plus)

> Objetivo: calibrar o SCORER **interativamente** dentro do seu agente do GPT Plus — sem ação do agentes, sem processo manual e sem dependências externas. Toda a calibração acontece via comandos no chat e atualização manual dos `.md` no “Meus GPTs”.

---

### 8.1) Como calibrar **dentro do GPT Plus**

Use estes comandos no agente:

- **“Rodar avaliação rápida (5 peças recentes)”**  
  O agente mede `StyleScore`, `Cadence`, `Heat`, `Punch`, `Lexicon`, `Originalidade`.  
  Saída: tabela-resumo + diagnóstico curto.

- **“Comparar com baseline”**  
  O agente compara com os **presets atuais** (por formato/perfil) definidos em `04_SCORER.md` e `02_PROMPT_SKELETONS.md`.  
  Saída: deltas por métrica e alerta de drift.

- **“Sugerir tuning leve”**  
  O agente aponta **apenas 1–2 ajustes** de cada vez (ex.: reduzir `style_bias`, ampliar `k` conceitual, ajustar alvo de `avg_sentence_len`, estreitar faixa de `Punch`).  
  Saída: bloco de “Proposta de Tuning”.

- **“Gerar patch de presets”**  
  O agente devolve um **bloco editável** (markdown) com novos valores para você **colar** no `02_PROMPT_SKELETONS.md` e no `04_SCORER.md`.

> **Importante:** o GPT Plus **não executa em background**. Sempre que quiser reavaliar, chame um desses comandos.

---

### 8.2) O que **não** existe nesta versão

- Nenhum “processo manual”, “execução manual”, “CI”, ou ação do agentes externos.  
- Nenhum relatório persistido automaticamente.  
- Nada roda sozinho quando você fecha a aba.  
- Se quiser histórico, **peça ao agente** um resumo de calibração e **cole** no seu doc.

---

### 8.3) Rotina recomendada (manual, dentro do chat)

1) **Rodar avaliação rápida** das últimas 3–5 peças (por formato).  
2) **Pedir comparação com baseline** (os presets vigentes).  
3) **Pedir sugestão de tuning leve** (máx. 2 alavancas por ciclo).  
4) **Gerar patch de presets** e **colar** nos `.md` (no construtor do GPT).  
5) **Reexecutar avaliação** em 1–2 peças novas para validar.

> Regra de parcimônia: **1 rodada de tuning por semana** é suficiente para manter estabilidade.

---

### 8.4) Tuning de cadência (sem interação externa)

- **Comando sugerido:** "/avaliar_cadencia - 5 peças boas para ajustar alvos"

- **O que o agente faz:**  
  Lê os textos **no contexto** do chat, calcula as métricas **no ato** e devolve os **novos alvos** (ex.: artigo 18–22 → manter; thread 16–20 → manter; roteiro 16–20 → manter, stdev mínimo 5.8).

- **Sua ação:**  
  **Copiar** o patch de presets para `02_PROMPT_SKELETONS.md` e `04_SCORER.md`.

---

### 8.5) Tuning de heat (curva emocional)

- **Comando:**  
  “Mostre a **curva de calor por seção** destas 3 peças e diga se o pico está na virada de tese/fecho. Proponha ajustes.”

- **Ajustes típicos (o agente sugere):**  
  - Mover pico 4/5 para **virada** e **fecho**.  
  - Elevar peso de `HeatCurveMatch` **apenas** no formato/perfil afetado.  
  - Instruções de `REWRITE_HEAT` (pergunta direta, detalhe sensorial).

---

### 8.6) Tuning de léxico (whitelist/redlist)

- **Comando:** "/avaliar_lexico - listar expressões saturadas e jargões"

- **Sua ação:**  
  Atualizar **manualmente** `whitelist.txt` e `redlist.txt` anexados ao GPT.

---

### 8.7) “Registro” sem execução interativa no chat

Como você quer **persistir** o histórico no GPT Plus?

- **Opção A (pragmática):** peça ao agente  
  “Resuma a calibração de hoje em um bloco markdown ‘Changeresumo de calibração’”  
  → **Cole** esse bloco no seu repositório local.

- **Opção B (em um único bloco markdown):** mantenha um `eval_plan.md` no seu repo.  
  Sempre que o agente sugerir tuning, copie o bloco:

```markdown
## Changeresumo de calibração - [DATA]
**Motivo:** [descrição do drift detectado]
**Ajustes:** [lista de parâmetros alterados]
**Resultado:** [métricas antes/depois]
**Status:** [estável/em teste]
```

---

### 8.8) Checklist de calibração (GPT Plus)

- [ ] Rodar avaliação em 3-5 peças recentes
- [ ] Comparar com presets atuais  
- [ ] Identificar 1-2 ajustes prioritários
- [ ] Gerar patch de presets
- [ ] Aplicar mudanças nos `.md`
- [ ] Testar em 1-2 peças novas
- [ ] Documentar no changeresumo de calibração

> **Lembrete:** Calibração é **iterativa e conservadora**. Melhor fazer ajustes pequenos e frequentes do que mudanças grandes e arriscadas.

---

### 8.9) Comandos rapidos (no chat)

/SCORE_TEXT source:'<cole o texto>' formato: artigo
/SCORE_COMPARE A:'<texto A>' B:'<texto B>' metrica:'StyleScore'
/REWRITE_ON_FAIL gates:['cadence','punch','originalidade'] modo:'minimal_change'

Execucao no chat
Peca ao agente
saida 100% original
nao copie frases
Comandos rapidos

## Política de Pontuação (Sincronizada)

### Limites por arquivo (inclui docs/YAML)
- **Dois-pontos:** máximo 20 (tolerância para documentação)
- **Travessões:** máximo 15 (tolerância para documentação)

### Limites por fewshot individual (o que realmente importa)
- **Dois-pontos:** máximo 1 (":" só em síntese)
- **Travessões:** máximo 1 ("—" só em contraste)
- **Punch_per_100w:** [2.0, 4.0] (coerente com presets)

> **Nota:** Limites por peça substituem qualquer regra global antiga.

> ✅ Compatível com GPT Plus — execução interativa e sem caminhos externos.