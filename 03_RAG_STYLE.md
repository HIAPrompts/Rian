# 03_RAG_STYLE.md
> Recuperação de **cadências reais suas** (mini-trechos) para ancorar tom, ritmo, léxico e pontuação — **antes** de gerar o texto.
> 
> **Versão calibrada para ChatGPT Plus (execução 100% interativa, sem interação externa).**

---

## 1) Visão geral & propósito do RAG de estilo

**O que é:**  
Um RAG (Retrieval-Augmented Generation) **focado em estilo**: em vez de buscar fatos para citar, ele busca **trechos seus** (40–120 palavras) que representem **cadência, tique verbal, ritmo e pontuação**. Esses trechos viram **few-shots de estilo** dentro do prompt — **não** aparecem no texto final.

**Por que usar:**  
- Reduz **deriva de voz** (o LLM “ouve” seu ritmo antes de escrever).  
- Aumenta **consistência** de pontuação assinatura (`:`, `—`, vírgulas).  
- Reforça **léxico preferido** (whitelist) e evita redlist na origem.  
- Acelera a produção: menos reescrita posterior pelo SCORER.

**Diferença para RAG de conteúdo:**  
| Aspecto | RAG de Conteúdo | **RAG de Estilo (este bloco markdown)** |
|---|---|---|
| Fonte | Artigos, docs, dados | Seus **trechos** com cadência |
| Objetivo | Citar fatos e referências | **Imitar ritmo, tique e voz** |
| Saída | Parafraseia/consolida fatos | **Gera texto novo no seu tom** |
| Risco | Plágio factual se mal usado | **Anti-colagem** por design (ver filtros) |

**Entradas (do orquestrador):**  
- `tema` (assunto/ângulo), `objetivo` (informar/orientar/convencer/CTA)  
- `perfil` (público), `formato` (thread/artigo/roteiro)  
- `alvos_estilo` (avg_sentence_len, calor, pontuação) — dos **presets** do `02_PROMPT_SKELETONS.md`

**Saídas (para o gerador):**  
- `RAG_FEWSHOTS` (2–3 excerpts de 1–2 frases, ≤ 80 palavras cada)  
- `style_cues` (lista: conectivos, sinais de pontuação, léxico whitelist)  
- `rationale` (por que cada trecho foi escolhido)  
- **Proibição:** “não copie frases literais; use apenas cadência e léxico preferido”

**Critérios de sucesso (mínimos):**  
- `StyleScore ≥ 0.80` no primeiro rascunho (Tópico 11 do StyleSpec)  
- `LexicalCompliance ≥ 0.95` (whitelist presente, redlist = 0)  
- `HeatCurveMatch ≥ 0.8` (curva de calor do formato)  
- **Overlap lexical** da saída com qualquer excerpt **< 15%**

**Políticas (anti-plágio & privacidade):**  
- Os `excerpts` são **micro**, **não citáveis** (só guiam a voz).  
- **Jamais** colar o texto do `excerpt` na saída final.  
- Descartar trechos com `redlist_hits > 0`.  
- Respeitar opt-out/remoção de itens do `CORPUS/` (resumo de calibraçãos no Tópico 7).

**Interface rápida (pseudoprompt do orquestrador):**
[RAG_STYLE_SELECT]
Input: {tema, objetivo, perfil, formato, alvos_estilo}

Buscar no CORPUS por semântica (embedding) + filtro de estilo (avg_len, stdev, heat, punct).
Rerank híbrido: 0.60·cos_sim + 0.25·style_sim + 0.10·tag_overlap − 0.05·novelty_penalty.
Escolher 2–3 trechos diversos (didático / enérgico / crítico construtivo).

Emitir:
RAG_FEWSHOTS: [{id, excerpt≤80w, rationale, style_cues:[":","—","Sem rodeio:"]}×2-3]
CONSTRAINT: "Não copie frases literais; imite cadência e léxico preferido."


**Exemplo de saída do módulo de RAG de estilo (interno ao prompt):**
```yaml
[RAG_FEWSHOTS]
- id: corpus_042
  rationale: "tema clareza+execução; heat=3; ritmo ≈18/6; dois-pontos para síntese"
  style_cues: [":","—","Sem rodeio:","avg_sentence_len≈18","commas≈13/100w"]
  excerpt: "Sem rodeio: clareza antes de intensidade. Escolhe uma métrica, executa 7 dias — e compara."
- id: corpus_177
  rationale: "tom crítico construtivo; pico breve de calor 4; pergunta direta"
  style_cues: ["O ponto é:","imperativos","pergunta única"]
  excerpt: "O ponto é: você confunde movimento com avanço. O que trava você aqui?"
CONSTRAINT: "Imite cadência e léxico; não copie frases. Saída final 100% original."
```

Resumo: o RAG de estilo não fornece conteúdo; ele empresta a música da sua voz.
O gerador dança nessa música para compor um texto novo, seu, e mensurável pelo SCORER.

Quer que eu envie o **Tópico 2 — Estrutura do banco de cadências (`/CORPUS`)** agora?
::contentReference[oaicite:0]{index=0}

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 2 — Estrutura do banco de cadências (`/CORPUS/`)

> Objetivo: organizar, etiquetar e medir seus textos/trechos para que o RAG de estilo recupere **cadência**, **léxico** e **pontuação assinatura** com segurança (sem colagem literal).

---

### 2.1) Estrutura de pastas e convenções (GPT Plus)

📁 estilometria-agent/
└── 📁 CORPUS/
├── raw/ # insumos brutos (transcrições, textos integrais)
├── cleaned/ # limpeza leve (normalização + correções evidentes)
├── windows/ # janelas 300–600 chars com metadados de estilo
├── blocos auxiliares de estilo # metadados por bloco markdown (.yml/(dados internos em memória GPT Plus))
└── index/
├── corpus_index(dados internos em memória GPT Plus) # índice global (busca rápida)
└── novelty_lsh.index # estrutura p/ deduplicação e similaridade

> **Nota GPT Plus:** Esta estrutura é conceitual. No GPT Plus, você gerencia o corpus através de comandos no chat e anexos de bloco markdowns.

**Padrão de nome do bloco markdown (base):**
{autor}{fonte}{tema}{AAAAMMDD}{hash8}.txt
ex.: angelo_youtube_globo_vs_cazetv_20250207_a1b2c3d4.txt

---

### 2.2) Metadados mínimos por item (sidecar)

> Um **sidecar** (`.yml` ou `(dados internos em memória GPT Plus)`) acompanha cada item do `raw/` e/ou `cleaned/`.  
> Ele descreve **de onde veio**, **como soa** e **o que contém**.

**Campos recomendados (`blocos auxiliares de estilo{basename}.yml`):**
```yaml
id: "a1b2c3d4"
title: "Globo vai 'competir' com CazéTV"
source:
  type: "video"                # video|artigo|nota|podcast
  platform: "youtube"
  url: "https://…"
  author: "Angelo"
  date: "2025-02-07"
license: "autorais"            # autorais|perm_link|privado
privacy:
  contains_sensitive: false
  pii_present: false
  notes: ""
tags:
  topics: ["mídia", "negócios", "poder"]
  tone: ["mentor", "analítico", "provocador"]
style_metrics:
  avg_sentence_len: 20.1       # palavras/frase
  stdev_sentence_len: 7.2
  paragraph_words_avg: 84
  heat_estimate: 3           # 1–5
  punch_per_100w: 2.8          # ":" + "—"
  imperatives_per_100w: 3.1
  transitions_present: ["rapaziada", "olha só", "entendeu?"]
  whitelist_hits: 9
  redlist_hits: 0
  filler_rate: 0.6             # “né?”, “tá?”, “saca?” por 100w
quality:
  asr_noise: "baixo"           # para transcrição
  uppercase_ratio: 0.01
  lang: "pt-BR"
notes: "Análise fria de bastidores; picos curtos de calor."
```

Por que isso importa: o RAG filtra/ranqueia por métrica de estilo (não por "relevância factual"). Esses campos aceleram o rerank de cadência.

### 2.3) Pipeline de ingestão (modo GPT Plus)
**Comando sugerido:** "/processar_texto - extrair janelas de estilo"

O agente GPT Plus:
1. **Ingestão:** recebe texto via anexo ou cola no chat
2. **Limpeza leve:** normaliza aspas, travessão (—), dois-pontos (:)
3. **Windowing:** quebra em janelas de 300–600 caracteres com sobreposição
4. **Cálculo de métricas:** avg_sentence_len, heat, punch, imperatives, transitions
5. **Retorna:** janelas processadas + métricas para uso no RAG

> **Nota:** No GPT Plus, não há persistência automática. O agente processa sob demanda.

### 2.4) Regras de qualidade & filtros (gates)
Comprimento: janelas < 220 chars → descartar (pouca cadência).
Redlist: se redlist_hits > 0 → não elegível para RAG.
ASR noise alto: marcar e rebaixar no rerank (não excluir).
Overlap textual: n-gram Jaccard com outras janelas do mesmo item < 0.9 (evita repetição).
Picos falsos: excesso de exclamação (>0.5/100w) ou caixa alta → rebaixar score de estilo.
PII/sensível: contains_sensitive: true → banir do RAG por padrão.

### 2.5) Como calcular as métricas de estilo (resumo operacional)
avg_sentence_len: tokens de palavra por sentença (pontuação .!? + heurísticas de “:”/“—”).
stdev_sentence_len: desvio padrão para mapear burstiness.
punch_per_100w: contagem de : + — por 100 palavras.
imperatives_per_100w: heurística por verbo no imperativo + padrão “verbo no início”.
heat_estimate (1–5): função de punch, imperatives, densidade de perguntas retóricas e variação de frase.
transitions_present: matching contra whitelist (ex.: “rapaziada”, “olha só”, “entendeu?”, “sem rodeio”).
whitelist_hits & redlist_hits: contagem lexicon/100w (ajustar para evitar spam).
Obs.: o SCORER (bloco markdown 04_SCORER.md) consome essas métricas; o RAG só usa para selecionar e misturar janelas.

### 2.6) Exemplo de janela em windows/ (JSON)
{
  "window_id": "a1b2c3d4_005",
  "parent_id": "a1b2c3d4",
  "offset": [2400, 3020],
  "text_preview": "Rapaziada, olha só: quando três anúncios chegam no mesmo dia...",
  "style_metrics": {
    "avg_sentence_len": 19.6,
    "stdev_sentence_len": 6.8,
    "heat_estimate": 3,
    "punch_per_100w": 3.1,
    "imperatives_per_100w": 4.2,
    "transitions_present": ["rapaziada", "olha só"],
    "whitelist_hits": 5,
    "redlist_hits": 0
  },
  "quality": { "asr_noise": "baixo" },
  "eligible_for_rag": true,
  "tags": ["mídia", "bastidor", "mentor"]
}
```

### 2.7) Índice global (index/corpus_index(dados internos em memória GPT Plus))

Bloco markdown único para busca rápida (embedding + estilo).
Chaves mínimas por janela:
{
  "window_id": "a1b2c3d4_005",
  "embedding": [0.012, -0.044, ...],
  "avg_sentence_len": 19.6,
  "stdev_sentence_len": 6.8,
  "heat_estimate": 3,
  "punch_per_100w": 3.1,
  "imperatives_per_100w": 4.2,
  "whitelist_hits": 5,
  "redlist_hits": 0,
  "transitions_present": ["rapaziada","olha só"],
  "lang": "pt-BR",
  "topic_tags": ["mídia","negócios"]
}

### 2.8) Deduplicação & novidade (anti-colagem estrutural)
LSH/ANN em novelty_lsh.index para detectar janelas quase idênticas.
Novidade: score novelty = 1 - max_similaridade (0–1).
No rerank, penalizar novelty < 0.2 (muito repetidas); premiar 0.3–0.7 (patrimônio estilístico útil sem eco).

### 2.9) Política de dados sensíveis & opt-out
privacy.contains_sensitive: true → janela fora do RAG por padrão.
Remoções: manter optout_resumo de calibração(dados internos em memória GPT Plus) com {window_id, motivo, timestamp}.
Privacidade: não expor texto integral do raw/ no prompt — apenas excerpts ≤ 80 palavras (e ainda assim só internos ao prompt).

### 2.10) Atualização do banco (modo GPT Plus)
**Comando sugerido:** "/atualizar_banco - adicionar novo texto ao corpus"

O agente GPT Plus:
1. **Recebe:** novo texto via anexo ou cola no chat
2. **Processa:** aplica pipeline de ingestão (limpeza + windowing + métricas)
3. **Valida:** checa qualidade das janelas (heat/punch/imperatives/transitions)
4. **Integra:** adiciona ao corpus virtual para uso em futuras consultas RAG
5. **Testa:** executa validação rápida com StyleScore

> **Nota:** No GPT Plus, o "banco" é mantido na memória da conversa. Para persistir, peça ao agente para gerar um resumo de calibração.

### 2.11) Boas práticas (checklist)
- Sidecar preenchido (licença/privacidade/tags).
- redlist_hits = 0 nas janelas elegíveis.
- Média de frase dentro de 18–22 (ajustável por formato).
- Burstiness presente (stdev > 5.5 em PT).
- punch_per_100w e imperatives/100w no intervalo do seu preset.
- Transições-whitelist aparecem naturalmente (sem spam).
- novelty ≥ 0.2 e ASR noise controlado.

Resultado: o /CORPUS/ deixa de ser “um monte de txt” e vira um banco de cadências medido, pronto para o RAG selecionar o som certo para cada peça.

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 3 — Seleção & Mistura (query, filtros, rerank e shallow fusion)

> Objetivo: escolher **2–3 janelas** do `/CORPUS/windows/` que melhor expressem **cadência, léxico e pontuação assinatura** para o tema/objetivo atual — e **misturar** esses sinais de estilo no prompt sem copiar texto literal.

---

### 3.1) Entradas do seletor (do orquestrador)

```yaml
input:
  tema: "<assunto/ângulo>"
  objetivo: ["informar" | "orientar" | "convencer" | "CTA"]
  perfil: "<público-alvo>"
  formato: ["thread" | "artigo" | "roteiro"]
  alvos_estilo:
    avg_sentence_len: [16, 22]   # palavras/frase (faixa alvo: thread=16-20, artigo=18-22, roteiro=16-20)
    heat: 3                      # 1–5 (curva de calor média: thread=3, artigo=3, roteiro=3-4)
    cadence: "alto"              # alto|médio|baixo (burstiness)
    punch_per_100w: [2.0, 4.0]   # ":" + "—"
    transitions_ceiling: "≤ 40%" # densidade máxima de conectores (thread=≤40%, artigo=≤35%, roteiro=≤45%)

→ Presets calibrados com base nas métricas do CORPUS (cadência≈18, punch≈2.8, heat≈3.1).
    transitions_bias: 0.7        # peso para conectores-whitelist
  hard_constraints:
    redlist_hard: true
    max_ngram_overlap: 12        # com qualquer janela selecionada
```

### 3.2) Construção da query (semântica + estilo)

**3.2.1 Semântica (embedding)**
query_sem: vetor do tema e objetivo (ex.: “mídia esportiva, bastidor, análise de incentivos”).

**3.2.2 Estilo (features-alvo)**
query_style: vetor com avg_sentence_len, stdev (burstiness), heat, punch_per_100w, imperatives/100w, transitions_present.

**3.2.3 Expansões (sinônimos e conectores)**
acrescentar ao query_style os conectores-whitelist do whitelist.txt (ex.: "rapaziada", "olha só", "entendeu?", "sem rodeio", "o ponto é:").

→ Fonte única de léxico: whitelist.txt e redlist.txt (diretório raiz).

**3.2.4 Padrões Humanos (HumanScore)**
query_human: vetor com features de humanização extraídas de transcrições de alta pontuação:
- conversational_tone: "Salve rapaziada", "Cara, se você", "Tá ligado?", "Beleza?"
- factual_clarity: "Basicamente", "É muito simples", "O que você precisa fazer"
- informative_analysis: "Eu vou falar um pouco sobre", "O que eu quero trazer para você"
- simple_grammar: estrutura SVOC, pronomes 2ª pessoa, verbos concretos

→ Fonte: human_tone_samples.json (45 amostras com HumanScore ≥ 0.85).

Resultado: a query final é híbrida: Q = [query_sem ⊕ query_style ⊕ query_human].

### 3.3) Pré-filtro (gates rápidos)
Aplicar sobre o índice index/corpus_index(dados internos em memória GPT Plus) antes do ranqueamento:
Idioma: lang == "pt-BR".
Elegibilidade: eligible_for_rag == true.
Redlist: redlist_hits == 0.
Comprimento: avg_sentence_len ∈ [16, 26] (range mais amplo que o alvo).
Qualidade: quality.asr_noise != "alto" (se “alto”, apenas rebaixar depois).
Sensível/PII: privacy.contains_sensitive == false.

### 3.4) Ranqueamento híbrido (semântica + estilo + humanização + UX)
Score composto por cinco fatores (normalizados em 0–1):
score = 0.50*cos_sim(query_sem, emb_window)
      + 0.22*style_sim(query_style, style_metrics_window)
      + 0.15*human_score(query_human, human_patterns_window)
      + 0.08*transitions_bonus(window.transitions_present, whitelist)
      + 0.05*ux_penalty(window)           # penaliza CAPS, ! excessiva, ruído ASR

cos_sim: similaridade semântica (tema/objetivo).
style_sim: proximidade da janela às metas estilísticas (avg_sentence_len, stdev, heat, punch, imperatives).
human_score: proximidade aos padrões humanos (conversational_tone, factual_clarity, simple_grammar, 2nd_person_usage).
transitions_bonus: +0.02 por conector-whitelist presente (máx. 0.08), sem spam.
ux_penalty: −0.02 a −0.12 por sinais de ruído (CAIXA ALTA, "!!!", erros recorrentes de ASR).

**3.4.1 Cálculo do HumanScore:**
human_score = 0.30*conversational_tone_score + 0.25*factual_clarity_score + 0.25*simple_grammar_score + 0.20*2nd_person_score

Onde:
- conversational_tone_score: presença de aberturas diretas, confirmações, tom coloquial
- factual_clarity_score: uso de "Basicamente", "É simples", explicações diretas
- simple_grammar_score: estrutura SVOC, frases curtas, verbos concretos
- 2nd_person_score: uso de "você", "ele", "ela", "nós" como sujeitos
Selecionar top-12 janelas para a etapa de diversidade.

### 3.5) Diversidade e novidade (evitar eco)
Aplicar MMR (Maximal Marginal Relevance) ou heurística simples:
MMR(window_i) = λ*score(window_i) - (1-λ)*max_j sim(window_i, window_j_selecionadas)
λ = 0.7
similaridade = cos_sim(embeddings) ⊕ jaccard_ngrams(3-5)
Garantir variação de tom entre as candidatas: {didático, enérgico, crítico construtivo}.
Filtrar janelas com novelty < 0.2 (muito repetidas no banco).
Manter 4–6 finalistas para mistura.

### 3.6) Seleção final (2–3 janelas)
Critérios:
Cobertura de sinais: entre as escolhidas, somar conectores-whitelist distintos (ex.: “rapaziada”, “olha só”, “o ponto é”).
Curva de calor: 1 janela heat≈3 (base), 1 janela com pico heat≈4 (ênfase), opcional 1 com heat≈2 (controle).
Ritmo: uma janela com frase média perto de 18–20; outra com pico de 30–40 (para ensinar burstiness).
Pontuação assinatura: presença de : e — dentro do alvo.

### 3.7) Geração do bloco RAG_FEWSHOTS (interno ao prompt)
Formato canônico:

[RAG_FEWSHOTS]
- id: "<window_id>"
  rationale: "<por que esta janela ensina algo útil para ESTE texto>"
  style_cues:
    transitions: ["rapaziada", "olha só", "entendeu?"]    # escolher 1–3 naturais
    punctuation: [":", "—"]                               # sinais de punch
    rhythm: { avg_sentence_len: 19, burstiness: "alto" }  # alvo de cadência
    heat: 3                                               # 1–5
  excerpt: "<≤ 80 palavras — texto exato da janela>"
- id: "<window_id_2>"
  rationale: "<ênfase/virada de tese; pico breve de calor>"
  style_cues:
    transitions: ["o ponto é:", "sem rodeio:"]
    punctuation: [":"] 
    rhythm: { avg_sentence_len: 28, burstiness: "alto" }
    heat: 4
  excerpt: "<≤ 80 palavras>"
CONSTRAINT: "Imite cadência e léxico; **não copie frases**; **saída 100% original**; execução **no chat** (peça ao agente)."

Observação: o excerpt é colado apenas aqui, interno ao prompt. Nunca aparece no texto final.

### 3.8) Shallow Fusion (mistura leve de estilo no planejador)
A mistura acontece no plano (não no texto diretamente):
Transições-whitelist: injetar como tendência a cada abertura de parágrafo (probabilidade moderada; sem spam).
Ritmo: definir alvo avg_sentence_len por seção; variar ±30% para burstiness.
Pontuação de punch: recomendar : e — nos pontos de síntese/virada.
Curva de calor: distribuir picos no meio e no fecho; abertura quente, mas sem gritar.
Léxico: viés leve para whitelist; proibição dura para redlist.

Pseudoprompt (interno):
[STYLE_PLAN]
- Use transitions naturais do conjunto {rapaziada, olha só, entendeu?, na prática, resumo} no início de alguns parágrafos (≤ 40% thread, ≤ 35% artigo, ≤ 45% roteiro).

→ Rotacione conectores; limite a 1 por fewshot; evite repetições próximas.
- Mantenha avg_sentence_len ≈ 19 (±30%), com 1–2 frases longas (30–40) por seção para burstiness.
- Utilize ":" para sínteses e "—" para contraste; evite excesso.
- Heat alvo 3/5; 1 pico 4/5 em viradas de tese; fecho com energia clara.
- Respeite redlist (banido); se usar jargão, explique inline (glossário breve).

### 3.9) Guardrails de originalidade (anti-colagem)
Após a geração do rascunho:
N-gram overlap (3–12): se > 12 palavras consecutivas iguais a qualquer excerpt, regerar o parágrafo.
Lexical spam: limitar conectores-whitelist a ≤ 1 a cada 2 parágrafos.
Redlist: ocorrência > 0 reprova.
Pontuação: punch_per_100w ∈ [2.0, 4.0] (ajustar por formato).

### 3.10) Erros comuns & correções

Erro: "Transição" repetida ("rapaziada" abrindo 3 parágrafos seguidos).
Correção: substituir 2 por variações ("olha só", "entendeu?", "na prática") ou remover.

Erro: frase média muito longa (≥ 26) ou muito curta (≤ 12) em toda a peça.
Correção: reescalonar com REWRITE_CADENCE (ver 04_SCORER.md), introduzindo 1–2 períodos longos e curtos por seção.

Erro: excesso de : e —.
Correção: manter punch_per_100w dentro da faixa e mover parte dos contrastes para verbos ou perguntas diretas.

Erro: heat descontrolado (picos 5/5 em sequência).
Correção: rebaixar para 3/5 e reservar 4/5 apenas para virada de tese e fecho.

### 3.11) Exemplo completo (tema fictício)
Input:
tema: "disputa de audiência entre TV aberta e streamings esportivos"
objetivo: "informar"
formato: "artigo"
alvos_estilo: { avg_sentence_len: [16,22], heat: 3, cadence: "alto", punch_per_100w: [2.0,4.0], transitions_bias: 0.7 }

RAG_FEWSHOTS (gerado):
- id: "globo_cazetv_20250207_05"
  rationale: "explicar 'tabuleiro' com tom de bastidor; heat-base 3; dois-pontos para síntese"
  style_cues:
    transitions: ["olha só"]
    punctuation: [":", "—"]
    rhythm: { avg_sentence_len: 19, burstiness: "alto" }
    heat: 3
  excerpt: "Olha só: quando a mesma marca aparece em três telões diferentes, isso não é acaso — é roteiro. Quem paga decide onde o jogo passa."
- id: "midiapoder_20250301_12"
  rationale: "pico breve de ênfase; pergunta direta para reengajar"
  style_cues:
    transitions: ["entendeu?"]
    punctuation: [":"]
    rhythm: { avg_sentence_len: 28, burstiness: "alto" }
    heat: 4
  excerpt: "Entendeu? Audiência não é amor, é preço. Se o preço muda, muda a fila. Qual incentivo prende o público agora?"
CONSTRAINT: "Imitar cadência/lexicon; proibir cópia literal no texto final."

STYLE_PLAN (derivado):
- Abrir 1º parágrafo com "olha só" (uma vez).
- Manter avg_sentence_len ≈ 19; incluir 2 frases longas (30–36) na seção de análise.
- ":" para síntese; "—" para contraste; heat 3 com 1 pico 4 ao explicar o incentivo.
- Rotacionar conectores; máximo 1 por fewshot; evitar repetições próximas.
- Fecho com ação concreta (o que observar na próxima janela de mídia).
Saída esperada: texto original que soa como você, com conectores naturais, ritmo variado, pontuação assinatura e curva de calor controlada — sem colar nenhuma frase dos excerpts.

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 4 — Few-shots sintéticos (exemplos de reforço de estilo)

> Objetivo: gerar **micro-excertos sintéticos** (≤ 80 palavras) que imitam suas marcas estilísticas — cadência, calor, ritmo e pontuação — para **reforçar o treinamento** do RAG de estilo quando o `/CORPUS/` real ainda não cobre certos temas ou tons.

---

### 4.1) Por que usar few-shots sintéticos
- Cobrir **lacunas temáticas** (ex.: “economia comportamental” ainda sem trecho real).  
- Treinar **variações de tom** (“crítico”, “didático”, “provocador”) mantendo a mesma voz.  
- Reduzir **dependência de corpus real** e evitar overfitting em janelas repetidas.  
- Garantir que o sistema possa gerar **prototipagem de estilo** mesmo em novos domínios.

> **Meta:** 30 – 50 few-shots sintéticos de alta qualidade, medidos e avaliados pelo `04_SCORER.md`.

---

### 4.2) Estrutura dos blocos markdown de few-shots

📁 estilometria-agent/
└── 📁 FEWSHOTS/
├── 0001_didatico_heat3.yaml
├── 0002_critico_heat4.yaml
├── 0003_reflexivo_heat2.yaml
└── …

Cada item contém **1 exemplo** de estilo, com metadados e métricas:

```yaml
id: "0001_didatico_heat3"
tone: "didático"
heat: 3
avg_sentence_len: 19
burstiness: "alto"
punch_per_100w: 3.1
transitions: ["olha só", "na prática"]
whitelist_hits: 6
redlist_hits: 0
excerpt: >
  Olha só: quando você quer clareza, não comece pelo plano — comece pela pergunta. 
  Se a pergunta for boa, o plano se escreve sozinho.
rationale: "Demonstra cadência natural + clareza direta, ritmo 19 palavras/frase, dois-pontos e tom de mentor."
```

---

### 4.3) Critérios de criação
| Critério               | Meta     | Descrição                               |
| ---------------------- | -------- | --------------------------------------- |
| `avg_sentence_len`     | 18 – 22  | Frase média controlada                  |
| `burstiness`           | alto     | variação 12–36 palavras                 |
| `heat`                 | 2–4      | intensidade emocional                   |
| `punch_per_100w`       | 2 – 4    | uso de “:” e “—”                        |
| `imperatives_per_100w` | 2 – 5    | presença de verbos de ação              |
| `whitelist_hits`       | ≥ 5      | presença natural de conectores pessoais |
| `redlist_hits`         | 0        | nenhuma ocorrência banida               |
| `tone`                 | coerente | didático, crítico, provocador, etc.     |

### 4.4) Tipos de few-shots sintéticos
| Tipo                    | Função                | Padrão de calor | Uso no sistema             |
| ----------------------- | --------------------- | --------------- | -------------------------- |
| **Didático**            | Explica, guia         | Heat = 3        | Artigos, threads de ensino |
| **Crítico construtivo** | Corrige ou alerta     | Heat = 4        | Opinião, análise           |
| **Reflexivo**           | Pausa e introspecção  | Heat = 2        | Fecho, ensaio              |
| **Provocador**          | Rompe inércia, cutuca | Heat = 4        | Aberturas fortes           |
| **Neutro-transicional** | Liga seções           | Heat = 2 – 3    | Padrão de transição        |

### 4.5) Geração automática (pseudoprompt)
Processo interno do agente FEWSHOT_GENERATOR, que lê o 01_STYLE_SPEC.md e o whitelist.txt para criar exemplos calibrados.
[GENERATE_FEWSHOT]
input:
  tone: "crítico construtivo"
  heat_target: 4
  length_target: 70-80
  include_whitelist: true
  forbid_redlist: true
  preserve_punctuation: [":", "—"]
  burstiness_target: "alto"
instruction:
  "Crie um mini-trecho de 60–80 palavras com a voz do mentor direto, 
   cadência oralizada, um toque de ironia leve e um fechamento que soe humano.
   Use conectores-whitelist, evite jargões e mantenha originalidade 100%."
output:
  fewshot.yaml

### 4.6) Pós-processamento (validação automática)
Verificação estilométrica → via 04_SCORER.md.
Métricas mínimas de aprovação:
StyleScore ≥ 0.82
LexicalCompliance ≥ 0.95
HeatCurveMatch ≥ 0.8
Burstiness ≥ 5.5
Overlap (entre few-shots) < 20%
Armazenamento: mover aprovados para biblioteca de FEWSHOTS e registrar em probes.txt.

### 4.7) Boas práticas na curadoria manual
Evite “textos de vitrine” (floreados ou genéricos).
Prefira micro-ideias completas: começo-meio-fecho em ≤ 3 frases.
Inclua sempre 1 marca de calor (2ª pessoa, detalhe sensorial ou metáfora concreta).
Varie voz interna (“entendeu?”, “olha só”, “repara nisso”).
Cada few-shot deve parecer um frame de conversa real, não uma redação.

### 4.8) Exemplo real (sintético gerado + anotado)

```yaml
id: "0005_provocador_heat4"
tone: "provocador"
heat: 4
avg_sentence_len: 21
burstiness: "alto"
punch_per_100w: 3.4
transitions: ["entendeu?"]
excerpt: >
  Entendeu? Você chama de falta de tempo o que, na verdade, é medo de começar.
  E medo não se some — se gasta, frase por frase, até virar impulso.
rationale: "Usa cadência oralizada, contraste forte com dois-pontos e travessão; heat 4 controlado."
```

---

### 4.9) Integração no RAG (fallback)
Quando o /CORPUS/ não tem janelas suficientes:
Consultar /FEWSHOTS/ por tone e heat_target.
Misturar 1 real (/CORPUS/) + 1 sintético (/FEWSHOTS/) no bloco RAG_FEWSHOTS.
Aplicar peso 0.7 → real, 0.3 → sintético no cálculo de style_sim.
Registrar synthetic_ratio em probes.txt.

### 4.10) Checklist de consistência

- redlist_hits = 0
- heat ∈ [2, 4]
- avg_sentence_len ∈ [18, 22]
- ≥ 1 marca de calor
- ≥ 1 pontuação-assinatura (: ou —)
- Curto (≤ 80 palavras)
- Autoral (Overlap < 15% com corpus real)
- Aprovado pelo SCORER

**Resumo:** os few-shots sintéticos são o "fôlego reserva" do seu estilo — mantêm o som da voz mesmo quando o banco real ainda está em silêncio.

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 5 — Guardrails de privacidade e anti-colagem

> Objetivo: garantir **originalidade**, **segurança de dados** e **uso ético** do `/CORPUS/` e dos `FEWSHOTS/`, impedindo cópia literal, vazamento de informações sensíveis e deriva de estilo por sobreajuste.

---

### 5.1) Princípios

1. **Estilo ≠ conteúdo.** O RAG de estilo só transfere **cadência/ritmo/pontuação/lexicon preferido**, não frases ou fatos.  
2. **Mínimo necessário.** O prompt interno usa **micro-excerpts** (≤ 80 palavras) **apenas** para calibrar o gerador.  
3. **Originalidade obrigatória.** Saída final deve ser **100% nova**, checada por **n-gram overlap** e **similaridade semântica**.  
4. **Privacidade acima de tudo.** Qualquer janela marcada como sensível fica **fora** da seleção, por padrão.  
5. **Auditável.** Toda decisão crítica (inclusão/exclusão) deve ter **resumo de calibração** no sistema de relatórios.

---

### 5.2) Tipos de risco e como mitigar

| Risco | Sinal | Mitigação |
|---|---|---|
| **Colagem literal** | frases idênticas | Gate de **n-grams (3–12)** e reamostragem por parágrafo |
| **Paráfrase excessivamente próxima** | semântica e ordem sintática iguais | Penalidade por **BLEU/ROUGE altos** + **cos_sim** > 0.92; reescrever |
| **Vazamento de PII** | e-mail, telefone, CPF, endereço | Regex/NER, mascaramento e veto a janelas com `privacy.contains_sensitive=true` |
| **Citação de dados privados** | diaries, confidenciais, contratos | **Banir** no pré-filtro; exigir licença “autorais/perm_link” com nota |
| **Sobreajuste de voz** | repetição de tics a cada parágrafo | Limitar **transitions** a ≤ 40% dos parágrafos; variar conectores |
| **Promo-speak/jargão vazio** | “imperdível, exclusivo, garanta já” | **redlist_hard=true**; reprova automática |
| **Calor emocional descontrolado** | picos 5/5 em sequência | **Heat governor** (rebaixa picos fora da curva do formato) |

---

### 5.3) Pré-filtros obrigatórios (antes de ranquear)

- `privacy.contains_sensitive == false`  
- `redlist_hits == 0`  
- `eligible_for_rag == true`  
- `lang == "pt-BR"`  
- `quality.asr_noise != "alto"` (se “alto”, **rebaixar** no rerank, não excluir)  
- `avg_sentence_len ∈ [16, 26]` (faixa ampla para preservar cadência, ajustar por formato)

---

### 5.4) Detecção e bloqueio de PII (pt-BR)

**Mascarar e vetar** sempre que correspondência positiva:

- **E-mail**: `[\w\.\-]+@[\w\.\-]+\.\w{2,}` → `***@***.***`  
- **Telefone BR**: `\(?\d{2}\)?\s?\d{4,5}\-?\d{4}` → `(**) *****-****`  
- **CPF**: `\d{3}\.?\d{3}\.?\d{3}\-?\d{2}` → `***.***.***-**`  
- **CNPJ**: `\d{2}\.?\d{3}\.?\d{3}\/?\d{4}\-?\d{2}` → `**.***.***/****-**`  
- **Endereço** (heurístico): `(?i)\b(rua|avenida|rodovia|estrada|alameda)\b.*\d+` → `ENDEREÇO_MASCARADO`  
- **Cartão** (Luhn): `(?:\d[ -]*?){13,19}` + verificação Luhn → `**** **** **** ****`

> Se PII aparece no **excerpt**: **descartar a janela**. Se surgir na **saída**: **bloquear** e reescrever.

---

### 5.5) Anti-colagem (n-gram + semântica)

**Durante a geração (por parágrafo):**

1. **N-gram overlap** (com `RAG_FEWSHOTS.excerpt` e `/CORPUS/windows/` do mesmo item):  
   - reprovar se houver sequência **≥ 12 palavras** idênticas;  
   - se **8–11 palavras**, reescrever com **técnicas de variação sintática** (mudar ordem, verbos, foco).
2. **Semântica**: `cos_sim(parágrafo, janela_top)`  
   - se `> 0.92` **e** ROUGE-L > 0.65 → **regerar** com `style_bias=0.6` e `paraphrase_strength=0.7`.  
3. **BLEU/ROUGE** (com trechos fonte)  
   - disparar alerta no resumo de calibração se **BLEU > 0.55** ou **ROUGE-L > 0.65**.

**Pseudocódigo:**
```python
if ngram_overlap >= 12 or (cos_sim > 0.92 and rougeL > 0.65):
    rewrite(style_bias=0.6, paraphrase_strength=0.7, vary_transitions=True)
```

### 5.6) Governança de "som de voz" (sem caricatura)

- **Limiter de conectores:** no máx. 1 transição-whitelist a cada 2 parágrafos.
- **Variedade:** rotacionar entre {"rapaziada", "olha só", "entendeu?", "na prática", "resumo"}.
- **Punch : e —:** 2.0–4.0/100w (ajustar por formato); excedeu → substituir por verbos ou perguntas diretas.
- **Burstiness:** coeficiente alvo 0.6–0.8; se < 0.45 ou > 0.9 → reequilibrar frases.

---

### 5.7) Privacidade, licença e remoções

- **Licenças em sidecar.license:** autorais | perm_link | privado.
- **privado** → não usar em RAG; apenas referência interna de análise.
- **Opt-out:** manter resumo de calibração de opt-out com {window_id, motivo, timestamp, actor}.
- **Direitos de terceiros:** se o texto tiver citação de terceiros não autorizada, marca license="restrita" e exclui do RAG.

---

### 5.8) Relatórios e auditoria (modo GPT Plus)
**Comando sugerido:** "/gerar_resumo - calibração desta execução"

O agente GPT Plus registra:
- Janelas selecionadas para RAG
- Filtros aplicados (PII, redlist)
- Métricas de estilo calculadas
- Ações de reescrita aplicadas
- Score final e violações

**Formato de resumo:**
```markdown
## Calibração - [DATA]
**Tema:** [assunto processado]
**Janelas usadas:** [lista de IDs]
**Métricas:** avg_sentence_len=19.4, punch=2.7/100w
**Ações:** [rewrite@p3, limit_transitions@p4]
**Score final:** StyleScore=0.84
```

> **Nota:** No GPT Plus, você pode colar este resumo como bloco markdown para histórico.

### 5.9) Fallbacks seguros

- **Corpus insuficiente** → usar 1 real + 1 sintético (peso 0.7/0.3) em RAG_FEWSHOTS.
- **Muitas reprovações por overlap** → reduzir style_bias e ampliar busca de janelas (k).
- **Heat fora da curva** → reescalar com HEAT_REWRITE(mode="flatten").
- **PII recorrente** → pausar fonte problemática e rodar higienização dedicada.

---

### 5.10) Checklist de aprovação (antes de entregar)

- **PII:** nenhum padrão detectado na saída final.
- **Redlist = 0** (promo-speak/clichês ausentes).
- **N-gram:** nenhuma sequência ≥ 12 palavras igual ao corpus.
- **Semântica:** cos_sim ≤ 0.92 e ROUGE-L ≤ 0.65 vs. janelas usadas.
- **Cadência:** avg_sentence_len dentro da faixa do formato; burstiness 0.6–0.8.
- **Punch:** 2.0–4.0/100w; sem excesso de ":"/"—".
- **Transições:** ≤ 40% dos parágrafos; sem repetição 3x seguida.
- **Relatórios gravados em relatórios de execução.**

**Resultado:** texto autoral, seguro e alinhado à sua voz — sem copiar, sem vazar, sem caricaturar.

::contentReference[oaicite:0]{index=0}

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 6 — Integração com o SCORER (métricas e feedback)

> Objetivo: conectar o módulo de RAG de estilo ao `04_SCORER.md` para **medir** a aderência de voz (cadência, léxico, calor, pontuação) e **retroalimentar** a geração com reescritas dirigidas (sem perder originalidade).

---

### 6.1) Visão geral do fluxo

[RAG_STYLE] → (RAG_FEWSHOTS + STYLE_PLAN)
↓
[GERADOR] → rascunho_v1
↓
[SCORER] → métricas + gates + sugestões
↓
[REWRITER] (modos específicos) → rascunho_v2 (até passar nos gates)
↓
[RELATÓRIOS] → registro de execução


---

### 6.2) Métricas consumidas e produzidas

**Entradas do SCORER (vindas do STYLE_PLAN e do corpus):**
- Alvos: `avg_sentence_len`, `burstiness`, `heat`, `punch_per_100w`, `transitions_bias`, `whitelist/ redlist`.

**Saídas do SCORER (sobre o rascunho):**
- `StyleScore (0–1)` — aderência global de voz.
- `CadenceScore (0–1)` — média de frase + variação (burstiness).
- `HeatCurveMatch (0–1)` — distribuição de calor por seção.
- `LexicalCompliance (0–1)` — whitelist/ redlist.
- `PunctuationFit (0–1)` — uso de “:” e “—” nas posições certas.
- `OriginalityFlags` — `ngram_overlap`, `cos_sim`, `rougeL`.

> *Gates mínimos sugeridos:* `StyleScore ≥ 0.80`, `LexicalCompliance ≥ 0.95`, `HeatCurveMatch ≥ 0.80`, `ngram_overlap_max < 12`.

---

### 6.3) Protocolo de troca (API interna simplificada)

**Envelope para o SCORER:**
```json
{
  "run_id": "2025-10-12T23:40:11Z",
  "style_plan": {
    "avg_sentence_len_target": [18,22],
    "burstiness_target": "alto",
    "heat_target": 3,
    "punch_target_per_100w": [2.0,4.0],
    "transitions_whitelist": ["rapaziada","olha só","entendeu?","na prática","resumo"],
    "redlist_hard": true
  },
  "draft_text": "<texto_gerado_v1>"
}

Resposta do SCORER:
{
  "scores": {
    "StyleScore": 0.77,
    "CadenceScore": 0.71,
    "HeatCurveMatch": 0.83,
    "LexicalCompliance": 0.98,
    "PunctuationFit": 0.62
  },
  "originality": {
    "ngram_overlap_max": 8,
    "cos_sim_max": 0.86,
    "rougeL_max": 0.48
  },
  "violations": ["CadenceLow","PunctuationUnderuse"],
  "fix_suggestions": [
    {"mode": "REWRITE_CADENCE", "targets": ["secao_2","secao_3"], "hint": "incluir 1–2 frases longas (30–40) e 1 curta (≤ 10)"},
    {"mode": "REWRITE_PUNCH", "targets": ["secao_1","fecho"], "hint": "inserir ':' na síntese e '—' no contraste principal"}
  ]
}
```

### 6.4) Modos de reescrita (REWRITER)

REWRITE_CADENCE
Quando: CadenceScore < 0.80.
Ação: redistribui tamanhos: ±30% em 2–3 frases/ seção; injeta 1 longa (30–40) e 1 curta (≤10).
Guardrail: manter conteúdo e coerência semântica local.

REWRITE_HEAT
Quando: HeatCurveMatch < 0.80 ou picos 5/5 em sequência.
Ação: baixa/eleva picos, concentrando 4/5 em virada de tese e fecho; abre em 3/5.
Guardrail: nunca encadear 5/5 por 2+ parágrafos.

REWRITE_PUNCH
Quando: PunctuationFit < 0.75 ou punch_per_100w fora de [2.0,4.0].
Ação: inserir : na síntese e — em contraste; remover excesso.
Guardrail: no máx. 1 punch por 3–4 frases.

REWRITE_LEXICON
Quando: LexicalCompliance < 0.95 ou redlist>0.
Ação: substituir promo-speak por verbos concretos; reforçar whitelist natural.
Guardrail: evitar spam de conectores.

REWRITE_TRANSITIONS
Quando: repetição 3x do mesmo conector.
Ação: rotacionar entre {"rapaziada", "olha só", "entendeu?", "na prática", "resumo"} e reduzir densidade.
Guardrail: ≤ 40% dos parágrafos com conector explícito.
O REWRITER aplica 1–3 modos por iteração e retorna ao SCORER até passar nos gates.

### 6.5) Estratégia de iterações (máx. 3 passes)
Passo A (macro): corrige cadência e heat.
Passo B (micro): acerta pontuação e transitions.
Passo C (sanity): valida originalidade e lexicon.
Se ainda reprovar após 3 passes → ampliar k do RAG (mais janelas) e reduzir style_bias em 10–20%.

### 6.6) Fórmulas de referência (simplificadas)
CadenceScore = f( |avg_sentence_len − target| , stdev_sentence_len )
penalização linear fora de [18,22]; bônus com stdev ≥ 5.5.
PunctuationFit = g(punch_per_100w in [2.0,4.0]) com peso extra se : ocorre em frases de síntese.
HeatCurveMatch = 1 − MSE(curva_prevista, curva_observada) por seção.
## StyleScore (fonte e cálculo)

O RAG **não calcula** StyleScore. A avaliação é feita pelo **SCORER** usando os pesos por formato definidos no **04_SCORER.md**.

→ Pesos do StyleScore: ver 04_SCORER.md (fonte única).

## Política de Heat (níveis discretos)

O projeto usa **níveis discretos** de HEAT:
- **3** como base (tom firme, sem exagero).
- **4** apenas em **picos breves** (virada/fecho), quando o formato pedir.
Exemplos/estimativas não devem usar decimais (3.4, 3.7…). Sempre arredondar para 3 ou 4.

### 6.7) De/Para de erros → ações
| Violação         | Sinal               | Ação prioritária                                |
| ---------------- | ------------------- | ----------------------------------------------- |
| `CadenceLow`     | frases uniformes    | `REWRITE_CADENCE` (+ 1 longa e 1 curta/ seção)  |
| `HeatFlat`       | curva 2–3 constante | `REWRITE_HEAT` (inserir pico 4/5 na virada)     |
| `PunchUnderuse`  | `punch < 2.0/100w`  | `REWRITE_PUNCH` (dois-pontos na síntese)        |
| `PunchOveruse`   | `punch > 4.0/100w`  | `REWRITE_PUNCH` (substituir por verbo/pergunta) |
| `TransitionSpam` | conector repetido   | `REWRITE_TRANSITIONS` (rotacionar/ reduzir)     |
| `RedlistHit`     | promo-speak         | `REWRITE_LEXICON` (verbo concreto/ glossário)   |

### 6.8) Exemplo de ciclo (realista)

Scores v1: Style=0.77 | Cadence=0.71 | Heat=0.83 | Lexicon=0.98 | Punch=0.62
Ações: REWRITE_CADENCE@sec2-3, REWRITE_PUNCH@sec1-fecho
Scores v2: Style=0.84 | Cadence=0.83 | Heat=0.82 | Lexicon=0.98 | Punch=0.78
Status: ✅ aprovado (relatório gerado)

### 6.9) Telemetria GPT Plus e telemetria (modo GPT Plus)
**Comando sugerido:** "/gerar_relatorio - execução completa"

O agente GPT Plus registra:
- Scores detalhados (Style, Cadence, Heat, Lexicon, Punch)
- Gates aprovados/falhados
- Ações de reescrita aplicadas
- Métricas de originalidade
- Parâmetros RAG utilizados

**Formato de relatório:**
```markdown
## Relatório de Execução - [DATA]
**Scores:** Style=0.84, Cadence=0.83, Heat=0.82, Lexicon=0.98, Punch=0.78
**Gates:** ✅ Aprovado
**Reescritas:** REWRITE_CADENCE@sec2-3, REWRITE_PUNCH@sec1-fecho
**Originalidade:** ngram_max=8, cos_sim_max=0.86, rougeL_max=0.48
**RAG:** k=24, style_bias=0.7
```

> **Nota:** No GPT Plus, você pode colar este relatório como bloco markdown para histórico.

### 6.10) Checklist de integração (modo GPT Plus)
✅ SCORER recebe STYLE_PLAN + draft_text.
✅ Scores calculados e gates aplicados.
✅ REWRITER acionado apenas nas seções apontadas.
✅ Reexecutar SCORER até aprovação ou 3 passes.
✅ Relatório gerado para histórico local.

**Resultado:** ciclo fechado de medição → correção → aprovação, mantendo o "som da fala" medível, auditável e reproduzível no GPT Plus.

::contentReference[oaicite:0]{index=0}

# 03_RAG_STYLE.md — Como manter o som da fala

## Tópico 7 — Rotina de atualização e testes (EVAL)

> Objetivo: manter o sistema **vivo e estável** com ingestões periódicas do `/CORPUS/`, testes de regressão estilométrica e tuning contínuo do RAG + SCORER — sem perder originalidade.

---

### 7.1) Calendário operacional

- **Diário (D1):** ingestão leve de novos textos/transcrições + `windowing` + indexação.
- **Semanal (W1):** bateria de **probes** (testes fixos) e análise de métricas agregadas.
- **Mensal (M1):** tuning fino de pesos (`style_bias`, `rerank λ`, faixas de `punch`, `avg_sentence_len`) e revisão do léxico.
- **Ad hoc:** quando surgir novo domínio/tema → criar **few-shots sintéticos** para cobrir lacuna.

---

### 7.2) Estrutura de EVAL (modo GPT Plus)

**Comando sugerido:** "/executar_testes - bateria de regressão"

O agente GPT Plus mantém:
- **Probes de teste:** prompts fixos para validar consistência
- **Relatórios de execução:** scores e métricas por teste
- **Agregados:** médias e tendências calculadas sob demanda
- **Relatório de opt-out:** remoções e PII detectadas

> **Nota:** No GPT Plus, não há persistência automática. O agente gera relatórios sob demanda.


---

### 7.3) Probes (exemplos para GPT Plus)

**Comando sugerido:** "/executar_probe - P001 mídia esportiva"

**Probes disponíveis:**
- **P001:** "mídia esportiva e audiência" (informar, artigo, heat=3)
- **P002:** "disciplina e rotina em dias difíceis" (orientar, thread, heat=3)
- **P003:** "economia comportamental do consumo de status" (convencer, artigo, heat=4)
- **P004:** "masculinidade e responsabilidade prática" (orientar, thread, heat=3)
- **P005:** "tecnoresumo de calibraçãoia/IA e trabalho" (informar, artigo, heat=3)

O agente GPT Plus executa cada probe e gera relatório com scores e métricas.

> **Nota:** No GPT Plus, os probes são executados sob demanda via comandos no chat.

---

### 7.4) Metas de aprovação (baseline)

- `StyleScore ≥ 0.82` (média por probe)  
- `CadenceScore ≥ 0.80` e `burstiness` 0.6–0.8  
- `HeatCurveMatch ≥ 0.80` (curva do formato)  
- `LexicalCompliance ≥ 0.96` (redlist=0)  
- `PunctuationFit ≥ 0.75` (punch 2.0–4.0/100w)  
- `Originality`: `ngram_overlap_max < 12`, `cos_sim_max ≤ 0.92`, `ROUGE-L ≤ 0.65`

> **Regra de parada:** 2 reprovações consecutivas no mesmo probe → abrir **issue** de tuning.

---

### 7.5) Plano de regressão (evitar drift)

1. **Seleção de 5–10 probes fixos** (cobrem seus principais registros de voz).  
2. **Após qualquer mudança** (pesos, lexicon, corpus grande): rodar todos os probes.  
3. Se **StyleScore médio cair ≥ 0.03** ou `LexicalCompliance` cair abaixo do alvo → **rollback** da mudança e registrar no `eval_plan.md`.

---

### 7.6) Coleta e agregação de métricas (modo GPT Plus)

**Comando sugerido:** "/gerar_agregado - últimas execuções"

**Por execução individual:**
```markdown
## Execução P003 - [DATA]
**Scores:** Style=0.84, Cadence=0.83, Heat=0.81, Lexicon=0.98, Punch=0.77
**Originalidade:** ngram_max=8, cos_sim_max=0.86, rougeL_max=0.48
**RAG:** k=24, style_bias=0.7
**Ações:** REWRITE_CADENCE@sec2, REWRITE_PUNCH@fecho
```

**Agregados (quando solicitado):**
```markdown
## Relatório Agregado - [PERÍODO]
**Médias:** Style=0.835, Cadence=0.812, Heat=0.804, Lexicon=0.979, Punch=0.761
**Taxa de falha:** 8%
**Principais falhas:** CadenceLow, PunchUnderuse
**Notas:** Ajustar avg_sentence_len alvo em artigos longos; reforçar ':' em sínteses
```

> **Nota:** No GPT Plus, você pode colar estes relatórios como blocos markdown para histórico.

### 7.7) Tuning — alavancas e impactos
| Parâmetro          | Onde           | Impacto                            | Risco                      |
| ------------------ | -------------- | ---------------------------------- | -------------------------- |
| `style_bias`       | RAG/STYLE_PLAN | aproxima ou afasta do corpus       | ↑ colagem se alto demais   |
| `k` (janelas)      | RAG            | diversidade de sinais              | ↑ latência                 |
| `λ` (MMR)          | Rerank         | controla novidade vs. aderência    | extremos causam drift      |
| `punch_range`      | SCORER         | mais/menos dois-pontos e travessão | caricatura se alto         |
| `transitions_bias` | STYLE_PLAN     | frequência de conectores           | spam se alto               |
| `heat_target`      | STYLE_PLAN     | intensidade emocional              | overdrive se 4–5 constante |

### 7.8) Fallbacks operacionais
- Poucas janelas boas → ampliar k, relaxar pré-filtro avg_sentence_len para [16,26] e puxar 1 few-shot sintético (peso 0.3).
- Excesso de reprovação por Punch → mover parte dos contrastes para verbos/perguntas.
- Transições repetidas → reduzir transitions_bias em 0.1 e ativar REWRITE_TRANSITIONS.
- Heat desbalanceado → REWRITE_HEAT(mode="flatten").

### 7.9) Checklist de release (modo GPT Plus)
**Comando sugerido:** "/executar_release - checklist mensal"

✅ Relatórios agregados acima das metas em ≥ 80% dos probes.
✅ Nenhum redlist em saídas de referência.
✅ Relatório de opt-out auditado (sem PII vazando).
✅ Atualização do léxico (entradas novas na whitelist e banimentos na redlist).
✅ Documentar mudanças em resumo de calibração (o que alterou e por quê).

> **Nota:** No GPT Plus, este checklist é executado via comandos no chat.

### 7.10) Guia de incidentes (modo GPT Plus)
**Comando sugerido:** "/resolver_incidente - [tipo]"

**Incidentes comuns:**
- **PII detectada:** bloquear entrega, mascarar, gerar relatório de incidente
- **Queda brusca de StyleScore:** rollback das últimas alavancas, rodar probes completos
- **Deriva de tom:** reduzir style_bias, limitar transições, recalibrar punch

**Resultado:** com essa rotina no GPT Plus, o sistema conserva o "som da fala" ao longo do tempo, mesmo com corpus em expansão e ajustes contínuos.

### 7.11) Comandos rapidos (no chat)

/RAG_STYLE_SELECT tema:'<assunto>' formato: artigo
/RAG_FEWSHOTS_PREVIEW max:3
/RAG_APPLY constraint:'nao copie frases; saida 100% original'

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

## Corpus Rayan (Importado)

### Estatísticas do Corpus
- **Janelas extraídas:** 127 mini_excerpts
- **Tamanho médio:** 68 palavras/janela
- **Marcadores preservados:** 89 ocorrências
- **Distribuição:** Thread (35%), Artigo (41%), Roteiro (24%)

### Marcadores Identificados
- "olha só": 23 ocorrências
- "o ponto é": 18 ocorrências  
- "sem rodeio": 15 ocorrências
- "na real": 12 ocorrências
- "tá ligado?": 11 ocorrências
- "ó": 10 ocorrências

### Uso no RAG
O corpus é usado como referência de estilo, não como fonte de conteúdo. Os marcadores ajudam a identificar padrões de fala característicos do autor.

### Excerpts Atualizados (6 exemplos)

#### Didáticos (2 exemplos)
```
"O ponto é: métrica guia a escrita. Decide o que vive no texto e o que fica para rascunho. Na prática, critério economiza energia. A cada sessão, compare antes e depois. Aceite cortar. Clareza paga conta."
<!-- src: [corpus_artigo_001, corpus_artigo_015] -->

"Uma ideia por cena. Uma razão para ficar. Uma ação para o final. Cortes no silêncio. Ênfase no verbo que anda. Tá ligado? Oralidade pede ritmo que o ouvido entende. Fala reto."
<!-- src: [corpus_roteiro_005, corpus_roteiro_012] -->
```

#### Energéticos (2 exemplos)
```
"Eleja um número simples. Dói quando cai e melhora quando você executa. Olha só: sem enfeite, sem atalhos. Só rastro visível do que foi feito. Publica hoje. Ajusta amanhã."
<!-- src: [corpus_thread_003, corpus_thread_007] -->

"Rapaziada, câmera ligada. Verdade sem espuma. Abre simples, dá um exemplo que dói no bolso. Fecha com um passo claro. Ó: roteiro bom não grita, conduz. Mostra. E chama pra ação."
<!-- src: [corpus_roteiro_001, corpus_roteiro_008] -->
```

#### Críticos Construtivos (2 exemplos)
```
"Você confunde movimento com avanço. Acumula referências sem digerir. Copia ritmo alheio e chama isso de pesquisa. Sem rodeio: o que muda para o leitor depois deste parágrafo? Responda."
<!-- src: [corpus_artigo_008, corpus_artigo_022] -->

"Prometer vídeo épico sem pauta é gravar corrida sem pista. Energia tem, direção não. Escreve três bullets. Mostra um exemplo que respira na câmera. Termina com pedido específico. Curto. Limpo. Publicável."
<!-- src: [corpus_roteiro_003, corpus_roteiro_014] -->
```

> ✅ Compatível com GPT Plus — execução interativa e sem caminhos externos.

