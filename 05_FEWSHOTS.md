# 05_FEWSHOTS.md
> Biblioteca de exemplos curtos para **reforço de estilo** (voz, cadência, léxico e pontuação) — usada como *condicionamento interno* antes da geração.
> Versão GPT Plus: tudo é operado **no chat**, sem interação externa.

> **Punctuation ✅ — por fewshot: ':' ≤1, '—' ≤1, punch 2.0–4.0/100w**

---

## Tópico 1 — Objetivo & Estrutura da Biblioteca

### 1.1) O que são FEWSHOTS (neste projeto)
- **Micro-exemplos** (40–80 palavras) que **não** vão para o texto final.  
- Servem para “**afinar o ouvido**” do modelo com **cadência, tiques verbais e pontuação assinatura** antes de escrever.
- Diferem do `/CORPUS/`: aqui os exemplos são **curados e sintéticos** (ou editados) para **maximizar sinais de estilo** e **minimizar conteúdo factual**.

**Regra de ouro:** *"Use a música, não a letra."* — **jamais** copie frases dos FEWSHOTS na saída final.

> **Execução no chat**; **peça ao agente** para avaliar/reescrever; **não copie frases** dos fewshots; **saída 100% original**.

---

### 1.2) Tipos de FEWSHOTS (tags de estilo)
- `didatico` — claro, direto, “na prática:”, `:` em sínteses.
- `critico_construtivo` — confronta com elegância; pergunta única; `—` para contraste.
- `energetico` — ritmo mais curto; pico de **heat 4** breve; final com verbo de ação.
- `confessional_contido` — 1 detalhe sensorial; heat 3; sem melodrama.
- `humor_ironico_leve` — imagem concreta + ironia curta (sem sarcasmo longo).
- `analitico` — enumeração enxuta; `:` para tese; **burstiness alto** (1 longa + 1 curta).

> Use **até 3 tags** por FEWSHOT.

---

### 1.3) Esquema canônico de um FEWSHOT

```yaml
- id: fs_0001
  tags: [didatico, analitico]
  heat: 3                     # 1–5 (curto)
  cadence_hint: {avg_sentence_len: 16-22, burstiness: "alto"}
  punch_hint: "2.0–4.0/100w"  # uso de ":" e "—"
  lexicon: ["o ponto é:", "na prática:", "sem rodeio:"]
  text: >
    Cara, clareza primeiro — intensidade depois. 
    Você elege um número que dói quando cai e melhora quando você executa. 
    Como um mecânico que testa uma peça por vez, você compara por uma semana sem enfeite. 
    O resultado? Consistência deixa rastro — e rastro corta barulho como faca quente. 
    Por que funciona? Porque você vê a diferença que importa.
  constraint: "não copiar frases na saída final; usar apenas cadência e léxico"
```

---

### 1.4) Boas práticas

- Texto único, 40–80 palavras.
- 1 período longo (30–40) + 1 curto (≤ 10), quando fizer sentido.
- Inserir pelo menos 1 marcador de léxico da whitelist.
- Zero termos da redlist.

---

### 1.5) Como usar no GPT Plus (comandos)

**Adicionar FEWSHOT:**
```
/FEWSHOT_ADD
tags: [critico_construtivo]
heat: 3
text: "Olha só: você confunde movimento com avanço. Pare de reorganizar a mesa e faça o trabalho que conta — o que deixa rastro."
```

**Listar FEWSHOTS:**
```
/FEWSHOT_LIST tags:[didatico, analitico] limit:5
```

**Selecionar para esta peça (antes de gerar):**
```
/FEWSHOT_USE ids:[fs_0001, fs_0032]  # o agente usa internamente
```

**Remover/editar:**
```
/FEWSHOT_EDIT id:fs_0032 text:"..." | /FEWSHOT_REMOVE id:fs_0032
```

> **Dica:** se você não chamar `/FEWSHOT_USE`, o agente seleciona automaticamente 2–3 usando formato/perfil e 03_RAG_STYLE.md.

---

### 1.6) Curadoria (qualidade mínima)

- Sinal forte de estilo (pontuação, cadência, léxico).
- Conteúdo "neutro" (evitar fatos datados ou nomes próprios).
- Originalidade: escrita original, sem trechos do /CORPUS/.
- Anti-caricatura: evite repetir o mesmo conector mais de 1× no exemplo.

**Checklist rápido (cada FEWSHOT):**
- 40–80w, 1 longa + 1 curta
- ≥ 1 termo de whitelist; 0 redlist
- `:` em síntese ou `—` em contraste (quando fizer sentido)
- Heat condizente com a tag (2–4, pico curto)
- Constraint anti-colagem presente

---

### 1.7) Presets por formato (seleção automática)

- **Thread** → prioriza energetico, didatico, critico_construtivo; cadência 16–20.
- **Artigo** → analitico, didatico, critico_construtivo; cadência 18–22.
- **Roteiro** → energetico, confessional_contido; cadência 16–20; falas curtas.

---

### 1.8) Exemplo de pacote inicial (3 peças)

```yaml
fewshots:
- id: fs_0101
  tags: [didatico, analitico]
  heat: 3
  cadence_hint: {avg_sentence_len: 18-22, burstiness: "alto"}
  lexicon: ["na prática:", "o ponto é:"]
  text: >
    Olha só: você para de medir tudo. 
    Escolhe um número que dói quando cai e melhora quando você executa. 
    Tá ligado? Sem rastro você não avança — só se move como barco sem leme. 
    Você faz, compara, corrige. E repete até ficar chato de tão simples que funciona. 
    E aí? Você vê o resultado como água que corta pedra.

- id: fs_0102
  tags: [critico_construtivo]
  heat: 3
  cadence_hint: {avg_sentence_len: 16-20, burstiness: "alto"}
  lexicon: ["sem rodeio:"]
  text: >
    Cara, você quer atalho para trabalho que só se resolve no treino. 
    O que acontece? Você reduz promessa, aumenta repetição como café de manhã. 
    Se você não consegue mostrar o rastro, não vale a pena — é só movimento. 
    Entendeu? Sem rastro, sem resultado. 
    Por quê? Porque resultado é o que você vê.

- id: fs_0103
  tags: [energetico, humor_ironico_leve]
  heat: 4
  cadence_hint: {avg_sentence_len: 16-20, burstiness: "muito_alto"}
  lexicon: ["rapaziada", "o ponto é:"]
  text: >
    Rapaziada, coragem não é grito — é rotina que você faz quieta como café de manhã. 
    Se a ideia é boa, você aguenta segunda-feira sem reclamar. 
    E funciona como relógio suíço. 
    O resultado? Você vê progresso como planta que cresce.
```

---

### 1.9) Resumo do Tópico 1

- FEWSHOTS são exemplos estilísticos (não conteúdo) de 40–80w.
- Entram internamente no prompt e não podem aparecer no texto final.
- Use tags, cadence_hint, heat e lexicon para sinal forte de voz.
- Operação 100% no chat: `/FEWSHOT_ADD`, `/FEWSHOT_LIST`, `/FEWSHOT_USE`.
- Curadoria garante originalidade e evita caricatura.

---

## Tópico 2 — Guidelines de Escrita Sintética (como criar FEWSHOTS bons)

### 2.1) Princípios (o que um FEWSHOT precisa entregar)
- **Som da fala > conteúdo**: sinal de cadência, léxico e pontuação assinatura.  
- **Originalidade**: nada retirado do `/CORPUS/`; gere de cabeça.  
- **Economia**: 40–80 palavras; 1 período **longo** (30–40) + 1 **curto** (≤10).  
- **Heat controlado**: 3 como base; picos 4 **curtos** (sem gritar).  
- **Intenção de pontuação**: `:` para síntese; `—` para contraste.  
- **Léxico curado**: ≥1 termo da **whitelist**; 0 **redlist**.

---

### 2.2) Anti-caricatura (evite “tique de barro”)
- **Limite conectores**: máx. **1** conector-whitelist por FEWSHOT (ou 2 se distantes).  
- **Varie aberturas**: comece com verbo, pergunta curta, advérbio ou substantivo concreto.  
- **Sem bordões empilhados**: “rapaziada… olha só… o ponto é…” (não).  
- **Sarcasmo curto**: ironia seca, sem vira-lata nem vitimismo.  
- **Substitua adjetivo vazio por verbo**: “incrível” → “entrega x em y dias”.

---

### 2.3) DOs & DON’Ts

**DO**
- Amarre o parágrafo com **síntese clara** (`:`) ou **virada** (`—`).  
- Use **metáfora concreta** e **verbo de ação**.  
- Faça **pergunta única** quando o tom for crítico construtivo.

**DON’T**
- Não cite dados, nomes próprios, sresumo de calibraçãoans.  
- Não copie **nem parafraseie** seus textos do CORPUS.  
- Não empilhe conectores nem “punch” gratuito.

---

### 2.4) Esqueleto canônico (preencha no chat)

/FEWSHOT_ADD
tags: [<1–3 tags: didatico|critico_construtivo|energetico|confessional_contido|humor_ironico_leve|analitico>]
heat: <2–4>
text: "<40–80 palavras; 1 longa + 1 curta; ':' em síntese OU '—' em contraste; ≥1 termo whitelist; 0 redlist>"


> Dica: se tiver dúvida, peça: **/FEWSHOT_COACH** e cole o rascunho — o agente devolve correções pontuais.

---

### 2.5) Templates prontos (copie e edite)

**A) Didático + Analítico (heat 3)**
Você elege um número guia que dói quando cai e melhora quando você executa.
Na prática: você compara uma semana seguida, corta o que não move a agulha — e mantém o que deixa rastro.


**B) Crítico construtivo (heat 3–4 curto)**
Você confunde movimento com avanço.
Você para de reorganizar o cenário e faz a única coisa que conta — a próxima entrega que você mede.


**C) Energético (cadência alta, final com ação)**
Respira: rotina não é castigo, é alavanca.
Se a ideia é boa, você aguenta segunda-feira — você publica hoje, melhora amanhã.

**D) Confessional contido (sensorial breve, sem melodrama)**
Ontem, às 6h12, a tela ainda fria e o café amargo.
Foi quando você entende: disciplina é silêncio — e o silêncio trabalha por você.

**E) Humor irônico leve (imagem concreta, sem sarcasmo longo)**
Você promete revolução sem rotina e convida ao atraso — primeiro dia você lota, o terceiro você decide. Você foca no gesto que deixa rastro.


---

### 2.6) Qualidade mínima (bar for entry)
- [ ] 40–80 palavras, **1 longa + 1 curta**.  
- [ ] `:` **ou** `—` com função clara (não decorativa).  
- [ ] **Heat 3** (pico 4 curto se a tag pedir).  
- [ ] ≥1 termo **whitelist**; **0 redlist**.  
- [ ] Sem dados próprios do CORPUS; metáfora **original**.  
- [ ] Sem repetição de conector no mesmo FEWSHOT.

---

### 2.7) Avaliação rápida (use com o agente)
/FEWSHOT_REVIEW
id|text: "<cole o texto>"
checks: ["len_40_80","has_long+short","has_punch","whitelist>=1","redlist=0","heat_ok","no_corpus_echo"]

→ O agente devolve **OK/FAIL** por critério + sugestão de ajuste.

---

### 2.8) Exemplos aprovados (modelo de referência)

- **fs_ref_didatico**
  > Na prática: eleja um número guia único, execute por uma semana e compare sem enfeite.  
  > Olha só: consistência deixa rastro — e rastro dispensa discurso.

- **fs_ref_critico**
  > Sem rodeio: se não dá para mostrar, não vale.  
  > Você quer ritual; o trabalho pede rastro.

- **fs_ref_energetico**
  > Rapaziada, foco no básico que paga as contas.  
  > Corre hoje — melhora o texto amanhã.

---

### 2.9) Resumo do Tópico 2
- **Escreva para soar**, não para informar.  
- **Compacte**: 40–80w, 1 longa + 1 curta, **punch** com função.  
- **Controle o heat** e **evite caricatura**.  
- Checklist + `/FEWSHOT_REVIEW` garantem padrão constante.  
- Tudo **interativo no chat**; nada do CORPUS entra literal.

---

## Tópico 3 — Biblioteca inicial por formato (12 itens)

> Regras: 40–80 palavras; **1 frase longa + 1 curta**; `:` em síntese **ou** `—` em contraste; ≥1 termo de **whitelist**; **0 redlist**.  
> Presets: **Thread 16–20**, **Artigo 18–22**, **Roteiro 16–20** (média de frase).

---

### 3.1) Thread (4 FEWSHOTS)

#### T3-TH-01 — didático + energético
/FEWSHOT_ADD
tags: [didatico, energetico]
heat: 3
text: "Eleja um número simples que dói quando cai e melhora quando você executa sete dias seguidos, sem romantizar o processo. Olha só: sem enfeite, sem atalhos — rastro visível do que foi feito hoje. Ajuste amanhã e repete até estabilizar."
<!-- src: [corpus_thread_003, corpus_thread_007] -->


#### T3-TH-02 — crítico construtivo
/FEWSHOT_ADD
tags: [critico_construtivo]
heat: 3
text: "Sem rodeio: você chama de estratégia o medo de começar, e planilha bonita gera avanço zero. Começa pequeno hoje e revisa em sete dias, comparando antes e depois para fechar a conta."


#### T3-TH-03 — analítico (lista implícita)
/FEWSHOT_ADD
tags: [analitico, didatico]
heat: 3
text: "Três checkpoints para a semana render: medir uma coisa, mostrar uma entrega e pedir um retorno específico. O resto é enfeite que faz barulho e gasta energia que você devia ter colocado no básico. Fechou, executa."


#### T3-TH-04 — humor irônico leve
/FEWSHOT_ADD
tags: [humor_ironico_leve, energetico]
heat: 3
text: "Rapaziada, planejamento sem execução não paga a conta — primeiro passo claro, terceiro dia mantendo. Publica hoje, melhora amanhã."


---

### 3.2) Artigo (4 FEWSHOTS)

#### T3-AR-01 — didático + analítico
/FEWSHOT_ADD
tags: [didatico, analitico]
heat: 3
text: "O ponto é: métrica guia a escrita e decide o que vive no texto e o que fica para rascunho. Critério economiza energia; a cada sessão, compare antes e depois. Aceite cortar para que a clareza pague a conta."
<!-- src: [corpus_artigo_001, corpus_artigo_015] -->


#### T3-AR-02 — crítico construtivo (pergunta única)
/FEWSHOT_ADD
tags: [critico_construtivo]
heat: 3
text: "Você confunde movimento com avanço, acumula referências sem digerir, copia ritmo alheio e chama isso de pesquisa. Sem rodeio: o que muda para o leitor depois deste parágrafo? Responda."
<!-- src: [corpus_artigo_008, corpus_artigo_022] -->


#### T3-AR-03 — confessional contido
/FEWSHOT_ADD
tags: [confessional_contido]
heat: 3
text: "Às 6h17, café amargo e tela fria; anotei a tese antes de abrir qualquer aba, porque distração parece trabalho e te rouba o texto — disciplina é silêncio que organiza a página. Na prática: uma página por dia. Com começo, meio e fecho visíveis."


#### T3-AR-04 — analítico + punch
/FEWSHOT_ADD
tags: [analitico]
heat: 3
text: "Tese, evidência, síntese: a tríade que segura um artigo. Estrutura separa opinião de barulho e transforma ideia em serviço para quem lê; entregue utilidade."
<!-- src: [corpus_artigo_011, corpus_artigo_019] -->


---

### 3.3) Roteiro (4 FEWSHOTS)

#### T3-RO-01 — energético (fala curta + contraste)
/FEWSHOT_ADD
tags: [energetico]
heat: 4
text: "Rapaziada, câmera ligada e verdade sem espuma: abre simples e dá um exemplo que dói no bolso. Depois fecha com um passo claro que qualquer um consegue cumprir. Roteiro bom não grita — conduz, mostra e chama pra ação com clareza."
<!-- src: [corpus_roteiro_001, corpus_roteiro_008] -->


#### T3-RO-02 — didático com cadência de fala
/FEWSHOT_ADD
tags: [didatico]
heat: 3
text: "Uma ideia por cena, uma razão para ficar, uma ação para o final. Cortes no silêncio, ênfase no verbo que anda. Na prática: oralidade pede ritmo que o ouvido entende — fala reto."
<!-- src: [corpus_roteiro_005, corpus_roteiro_012] -->


#### T3-RO-03 — crítico construtivo (pico breve)
/FEWSHOT_ADD
tags: [critico_construtivo, energetico]
heat: 4
text: "Muita fala tentando ficar inteligente mata a cena, e você perde tempo explicando o óbvio — roteiro vive de gesto claro, conflito simples e resolução visível. Um gancho, uma prova, fecho com ação."


#### T3-RO-04 — humor irônico leve (imagem concreta)
/FEWSHOT_ADD
tags: [humor_ironico_leve]
heat: 3
text: "Prometer vídeo épico sem pauta é gravar corrida sem pista. Energia tem, direção não. O ponto é: escreve três bullets, mostra um exemplo que respira na câmera e termina com pedido específico. Curto, limpo, publicável."
<!-- src: [corpus_roteiro_003, corpus_roteiro_014] -->


---

### 3.4) Resumo do Tópico 3
- 12 FEWSHOTS prontos (4 por formato), já no padrão `/FEWSHOT_ADD`.  
- Cada um traz **cadência**, **punch** e **heat** calibrados para o uso interno.  
- Use **2–3** por peça ou deixe o agente escolher automaticamente.  
- Se quiser mais variações, peça: **“/FEWSHOT_ADD no estilo X sobre Y”** — eu gero na hora.

## Tópico 4 — Avaliação & Refinamento de Fewshots

### 4.1) Objetivo
Garantir que cada fewshot mantenha:
- **Cadência** compatível com o preset (±10 % da média).  
- **Heat** coerente com o tom e tags.  
- **Lexicon** estritamente whitelist.  
- **Ausência total de eco** com o `/CORPUS/`.

O módulo de verificação atua como mini-SCORER autônomo, acessível no chat via comando.

---

### 4.2) Comando de Avaliação
/FEWSHOT_SCORE
id|text: "<cole o fewshot>"
checks: ["cadence", "heat", "lexicon", "burstiness", "originality"]
return: ["score_global","flags","suggestion"]


> Retorna StyleScore (0–1) e flags:
> - 🔵 cadence_off → frase longa ou curta demais  
> - 🔴 redlist_hit → termo banido  
> - 🟡 low_heat → tom frio; precisa de verbo ativo  
> - 🟣 echo_detected → similaridade alta com `/CORPUS/`

---

### 4.3) Critérios de aprovação
| Métrica | Limite mínimo | Ação se falhar |
|----------|----------------|----------------|
| **StyleScore** | ≥ 0.82 | reescrever |
| **LexicalCompliance** | ≥ 0.95 | substituir termo |
| **Heat** | 2 ≤ heat ≤ 4 | ajustar intensidade |
| **Overlap** | < 15 % com CORPUS | re-sintetizar |

---

### 4.4) Loop de Refinamento (manual)
/FEWSHOT_REWRITE
id|text: "<cole o texto>"
targets: ["cadence","heat","lexicon"]
mode: "guided"

→ o agente devolve versão ajustada e novo StyleScore.

---

### 4.5) Check de Curadoria em Lote
/FEWSHOT_AUDIT
tags:[didatico,critico_construtivo,energetico]
filters: {score<0.82, redlist>0}
output: "relatorio_markdown"

> Gera relatório com lista de fewshots reprovados + motivos.

---

### 4.6) Tabela de Diagnóstico (interno)
| Código | Tipo | Causa provável | Correção |
|:--:|:--|:--|:--|
| **C1** | Cadência fora de faixa | frase longa demais | dividir em 2 |
| **C2** | Burstiness baixo | ritmo mecânico | alternar longa+curta |
| **L1** | Redlist | jargão/promo-speak | substituir |
| **H1** | Heat frio | verbo neutro | usar verbo de ação |
| **O1** | Overlap | eco com CORPUS | reescrever |
| **M1** | Miss Lexicon | nenhum termo whitelist | inserir 1 marcador |

---

### 4.7) Pipeline resumido
1. Adicionar fewshot → `/FEWSHOT_ADD`  
2. Avaliar → `/FEWSHOT_SCORE`  
3. Se falhar → `/FEWSHOT_REWRITE`  
4. Confirmar → `/FEWSHOT_AUDIT`  

---

### 4.8) Resumo do Tópico 4
- Avaliação = StyleScore + LexicalCompliance + Heat + Overlap.  
- Reescrita guiada no chat; zero interação externa.  
- Ferramentas: `/FEWSHOT_SCORE`, `/FEWSHOT_REWRITE`, `/FEWSHOT_AUDIT`.  
- A curadoria é contínua: refine até soar humano e fiel à voz original.

---

## Tópico 5 — Mixagem & Diversidade de Cadência

### 5.1) Objetivo
Evitar que a peça final “trave” num único ritmo. A mistura correta:
- mantém **burstiness alto** (alternância de frases),
- distribui **heat** sem picos longos,
- usa **punch** (`:`/`—`) com intenção, não como muleta.

---

### 5.2) Regra dos 3 Slots (mix básico)
Use **até 3 fewshots** por peça, cada um ocupando um *slot* de função:

| Slot | Função | Tags preferidas | Papel na cadência |
|---|---|---|---|
| **S1** | Base didática | `didatico` / `analitico` | define frase **média** (16–22) e `:` em síntese |
| **S2** | Virada construtiva | `critico_construtivo` | injeta **pergunta única** e `—` em contraste |
| **S3** | Energia/fecho | `energetico` / `humor_ironico_leve` / `confessional_contido` | acelera o ritmo e posiciona **heat 4** breve |

> **Thread**: S1 + S2; S3 opcional.  
> **Artigo**: S1 + S2 + S3 (com S1 predominante).  
> **Roteiro**: S2 + S3; S1 leve.

---

### 5.3) Comando de mixagem
/FEWSHOT_MIX
select: {max: 3, require_tags: ["didatico|analitico", "critico_construtivo"], optional_tags: ["energetico|humor_ironico_leve|confessional_contido"]}
constraints:
avg_sentence_len:
thread: "16–20"
artigo: "18–22"
roteiro: "16–20"
heat_target:
thread: 3
artigo: 3
roteiro: "3–4"
punch_per_100w: "2.0–4.0"
diversity:
- no_same_tag_twice: true
- min_lexicon_overlap: 0 # evita repetir o mesmo conector
- cadence_spread: "longa+curta" # garante alternância
return: ["ids_selecionados","rationale_mix","uso_recomendado_por_seção"]


---

### 5.4) Balanceamento por formato (pesos de influência)
> Quanto cada slot “contamina” o ritmo do texto final.

| Formato | S1 (base) | S2 (virada) | S3 (fecho) | Observações |
|---|---:|---:|---:|---|
| **Thread** | 0.45 | 0.35 | 0.20 | ritmo rápido, CTA curto |
| **Artigo** | 0.55 | 0.30 | 0.15 | prioriza clareza/estrutura |
| **Roteiro** | 0.35 | 0.30 | 0.35 | oralidade, picos breves |

> O agente usa esses pesos para “puxar” o gerador sem esmagar um único tique.

---

### 5.5) Diversidade mínima (gates do mix)
- **CadenceSpread**: presença explícita de **1 frase longa** (30–40) **e** **1 curta** (≤10) entre os slots.  
- **HeatSpread**: no máximo **1** slot com heat=4; os demais em 3.  
- **PunchIntent**: `:` aparece **no slot base**; `—` **no slot de virada**.  
- **LexiconRotation**: conectores-whitelist **não** podem repetir no mix.

/FEWSHOT_BALANCE
fix: ["CadenceSpread","HeatSpread","LexiconRotation","PunchIntent"]

---

### 5.6) Rotação de conectores (anticaricatura)
/FEWSHOT_ROTATE_CONNECTORS
avoid: ["Sem rodeio:","O ponto é:"]
prefer: ["na prática:","resumo:","rapaziada","olha só"]
policy: "≤ 1 conector por slot"


---

### 5.7) Estratégias de mix prático (receitas rápidas)

**A) Thread → “guia prático”**
- S1: `didatico` (na prática:, `:`)
- S2: `critico_construtivo` (pergunta única, `—`)
- S3: *(opcional)* `energetico` (fecho com verbo de ação)

**B) Artigo → “opinião com prova”**
- S1: `analitico` (estrutura, `:`)
- S2: `critico_construtivo` (contraste, pergunta)
- S3: `confessional_contido` (detalhe sensorial curto)

**C) Roteiro → “fala que anda”**
- S2: `critico_construtivo` (virada)
- S3: `energetico` (chamada clara)
- S1: *leve* `didatico` só para abrir via `na prática:`

---

### 5.8) MMR de estilo (seleção com diversidade)
> Para não puxar dois fewshots “quase iguais”.

/FEWSHOT_SELECT_MMR
k: 3
lambda: 0.7 # 0=diversidade pura · 1=similaridade pura ao pedido
signals: ["cadence","heat","punch","lexicon"]


---

### 5.9) Exemplo completo (artigo)
/FEWSHOT_MIX
select: {max: 3}
constraints: {formato:"artigo"}
→ ids: [fs_0101 (analitico), fs_0102 (critico), fs_0103 (confessional)]
→ rationale:
fs_0101 define tese+sintese com ":" e cadência 18–22
fs_0102 injeta pergunta única e "—" em contraste (virada)
fs_0103 adiciona detalhe sensorial curto para calor orgânico
→ uso:
Abertura: fs_0101
Virada de tese: fs_0102
Fecho: fs_0103


---

### 5.10) Checklist do mix (passa/volta)
- [ ] Tags variadas (sem repetição de tipo).  
- [ ] Longa + curta presentes entre os slots.  
- [ ] `:` na síntese, `—` no contraste.  
- [ ] 0 repetição de conector; whitelist **rotacionada**.  
- [ ] Heat 4 só em um slot e **breve**.  
- [ ] `punch 2.0–4.0/100w` (estimado nos fewshots).

---

### 5.11) Resumo do Tópico 5
- Misture **funções de cadência** (base, virada, fecho) — não só “estilos”.  
- Garanta **spread** de ritmo, heat e punch; **rote** conectores.  
- Use `/FEWSHOT_MIX`, `/FEWSHOT_BALANCE`, `/FEWSHOT_ROTATE_CONNECTORS` e, se precisar, **MMR de estilo** para escolher 3 bons exemplos.

---

## Tópico 6 — Integração com o Gerador & Orquestração

### 6.1) Objetivo
Fazer com que os FEWSHOTS realmente **influenciem** o estilo do texto gerado, sem aparecer nele.  
O sistema os injeta antes da escrita, garantindo que o LLM “ouça” a cadência da sua voz antes de começar.

---

### 6.2) Modo de Inserção
Quando o gerador (por ex. `/CREATE_MATERIA` ou `/ESCREVER_ARTIGO`) é chamado, o orquestrador faz:
1. Lê metadados do formato (`thread`, `artigo`, `roteiro`).
2. Executa `/FEWSHOT_MIX` usando presets daquele formato.
3. Injeta 2–3 FEWSHOTS no **bloco inicial oculto** do prompt (não exibido ao leitor).
4. Adiciona instrução:  
   > “Imite cadência e léxico; não copie frases literais; saída 100% original.”

---

### 6.3) Estrutura interna do bloco injetado

```yaml
[RAG_STYLE_FEWSHOTS]
- id: fs_0101
  tags: [didatico, analitico]
  rationale: "clareza e síntese"
  text: "Pare de medir tudo. Eleja um número que dói quando baixa e melhora quando executa. Consistência deixa rastro."
- id: fs_0102
  tags: [critico_construtivo]
  rationale: "pergunta única + contraste"
  text: "O que trava você? Sem rastro não há avanço."
CONSTRAINT: "Imite cadência e ritmo; não copie frases; preserve calor e léxico."
```

---

### 6.4) Parâmetros de influência

| Parâmetro           | Descrição                                 | Peso padrão |
| ------------------- | ----------------------------------------- | ----------- |
| `cadence_influence` | força do ritmo (sentence_len, burstiness) | 0.35        |
| `lexicon_influence` | presença dos conectores whitelist         | 0.25        |
| `punct_influence`   | uso proporcional de ":" e "—"             | 0.20        |
| `heat_influence`    | ajuste de temperatura emocional           | 0.20        |

Valores podem ser ajustados no orquestrador com /TUNE_STYLE_WEIGHTS.

### 6.5) Comando de integração manual
/FEWSHOT_INJECT
formato: "artigo"
target_prompt: "<texto-base>"
options:
  max_fewshots: 3
  cadence_influence: 0.35
  lexicon_influence: 0.25
  heat_target: 3
return: "prompt_expandido"
→ O agente retorna o prompt expandido, já contendo o bloco [RAG_STYLE_FEWSHOTS].

### 6.6) Avaliação pós-injeção
Após gerar um texto completo, execute:
/EVAL_FEWSHOT_INFLUENCE
source: "<texto final>"
compare_with: [ids dos fewshots usados]
metrics: ["cadence_shift","lexicon_overlap","heat_curve_match"]

Alvo mínimo:
cadence_shift ≤ ±10%
lexicon_overlap < 15%
heat_curve_match ≥ 0.8

### 6.7) Diagnóstico de falha
| Sintoma                | Causa                        | Ação                            |
| :--------------------- | :--------------------------- | :------------------------------ |
| Texto frio / sem ritmo | fewshots pouco energéticos   | reequilibrar heat 4             |
| Cadência travada       | mix com frases curtas demais | incluir 1 analítico             |
| Repetição literal      | overlap > 15%                | excluir fewshot e re-sintetizar |
| Falta de punch         | ausência de ":" ou "—"       | revisar slot S1/S2              |
| Léxico estranho        | fewshot sem whitelist        | corrigir via `/LEXICON_SYNC`    |

### 6.8) Relatório de performance
/FEWSHOT_LOG
fields: ["id","tags","score_final","heat_avg","cadence_avg","lexicon_hits"]
output: "relatorio_markdown"

Mantém rastreio de desempenho sem precisar de blocos markdown externos.

### 6.9) Resumo do Tópico 6
FEWSHOTS são injetados antes da escrita, nunca exibidos.
Eles guiam cadência, léxico e calor — mas não conteúdo.
Avaliação via /EVAL_FEWSHOT_INFLUENCE garante ritmo humano.
Ajustes finos com /TUNE_STYLE_WEIGHTS e /FEWSHOT_LOG completam o ciclo.

# 05_FEWSHOTS.md
> Biblioteca de exemplos curtos — **expansão e síntese automática**.

---

## Tópico 7 — Expansão, Variações & Síntese de Novos Fewshots

### 7.1) Objetivo
Aumentar a biblioteca sem perder **voz**, **originalidade** e **diversidade de cadência**.  
Tudo acontece **no chat**: você pede, o agente sintetiza, avalia e só entra o que passar nos gates.

---

### 7.2) Fontes de expansão
1) **Síntese pura** (do zero) — melhor para evitar eco.  
2) **Derivação de um fewshot existente** — cria 3–5 variações controladas.  
3) **Destilação de um texto seu “bom”** — extrai um exemplo **estilístico** (não factual).

> Regras fixas: **40–80w**, 1 frase **longa** (30–40) + 1 **curta** (≤10), ≥1 termo **whitelist**, **0 redlist**, `:` ou `—` com função.

---

### 7.3) Comandos principais

**A) Síntese do zero (guiada por tags)**
/FEWSHOT_SYNTH
tags: [didatico, analitico] # 1–3 tags
formato: artigo # thread|artigo|roteiro
heat: 3
constraints: {avg_sentence_len: "18–22", punch: "2.0–4.0/100w"}
lexicon_hint: ["na prática:", "olha só"]
return: ["id","text","score","rationale"]


**B) Variações controladas (parafrasear cadência, não conteúdo)**
/FEWSHOT_VARIATIONS
id|text: "<cole o fewshot base>"
n: 3
policies:
keep_function_words: [":","—"]
change_opening: true
rotate_lexicon: true # alterna conectores whitelist
keep_heat: "±0.5"
gates: ["len_40_80","long+short","no_redlist","originality<15% overlap"]


**C) Destilar de um texto seu (anti-colagem habilitada)**
/FEWSHOT_FROM_TEXT
source: "<cole 1–2 parágrafos do SEU texto>"
mode: "style_only" # copia ritmo/tiques, não ideias
extract:
cadence_hint
punch_hint
lexicon_markers
rewrite_to_fewshot: true


**D) Minerar do CORPUS com proteção**  
> Usa o CORPUS apenas como **bússola de cadência**, reescrevendo tudo.
/FEWSHOT_FROM_CORPUS
topic_hint: "rotina e prova"
k: 6
policy:
anti_copy: true # proíbe n-gram >= 12 e match semântico alto
synthesize: true # sempre reescreve do zero
whitelist>=1; redlist=0
return: ["id","text","score","why"]


---

### 7.4) Gates de aprovação (automáticos)
| Gate | Regra | Reprova se… |
|---|---|---|
| **Tamanho** | 40–80 palavras | <40 ou >80 |
| **Cadência** | 1 longa (30–40) + 1 curta (≤10) | ausente |
| **Punch** | presença funcional de `:` **ou** `—` | decorativo/ausente |
| **Lexicon** | ≥1 whitelist; 0 redlist | falha em qualquer |
| **Originalidade** | overlap com CORPUS < **15%** | ≥15% |
| **Heat** | 2–4 (pico 4 curto) | fora da faixa |

/FEWSHOT_SCORE id|text:"..."
→ retorna {StyleScore, Lexical, Heat, Overlap, Flags}


**Limiares de aceite:**  
`StyleScore ≥ 0.82` **e** `Lexical ≥ 0.95` **e** `Overlap < 15%`.

---

### 7.5) Curadoria em lote (entrada/saída)
/FEWSHOT_BULK
op: "synth" | "variations" | "from_text" | "from_corpus"
n: 12
tags: [didatico, critico_construtivo, energetico]
formato: thread
post_checks: ["score>=0.82","no_redlist","overlap<15%","mix_diversity"]
export: "markdown_block" # te entrega blocos prontos para /FEWSHOT_ADD


---

### 7.6) Diversidade e rotação (evitar clones)
/FEWSHOT_DIVERSIFY
pool: [ids|texts]
rules:
max_same_tag: 1
min_lexicon_overlap: 0
cadence_spread: "longa+curta"
heat_distribution: "1x4 + resto 3"


---

### 7.7) Correções rápidas (assistidas)
/FEWSHOT_FIX
id|text: "<cole o texto>"
issues: ["cadence_off","no_punch","low_heat","redlist_hit"]
policy: "minimal_change" # altera o mínimo para passar nos gates


---

### 7.8) Workflow sugerido
1. **Gerar** 6–12 candidatos → `/FEWSHOT_SYNTH` ou `/FEWSHOT_FROM_TEXT`.  
2. **Pontuar** → `/FEWSHOT_SCORE`.  
3. **Corrigir** os reprovados → `/FEWSHOT_FIX`.  
4. **Diversificar** o conjunto → `/FEWSHOT_DIVERSIFY`.  
5. **Adicionar** os aprovados → `/FEWSHOT_ADD`.  
6. **Auditar** periodicamente → `/FEWSHOT_AUDIT`.

---

### 7.9) Resumo do Tópico 7
- Expansão pode ser **sintética**, **derivada** ou **destilada** do seu texto.  
- Gates garantem **cadência, punch, heat, léxico** e **originalidade**.  
- Comandos de lote e diversificação evitam biblioteca com exemplos “iguais”.  
- Tudo **interativo** e **sem colagem**: usamos a música, nunca a letra.

# 05_FEWSHOTS.md
> Biblioteca de exemplos curtos — **operação no GPT Plus & checklists finais**.

---

## Tópico 8 — Operação, Manutenção & Boas Práticas

### 8.1) O que manter sempre
- **Qualidade**: 40–80w; 1 longa (30–40) + 1 curta (≤10); `:` (síntese) **ou** `—` (contraste).
- **Léxico**: ≥1 termo **whitelist**; **0 redlist** (fonte: `whitelist.txt` e `redlist.txt`).

→ Fonte única de léxico: whitelist.txt e redlist.txt (diretório raiz).
- **Originalidade**: overlap com `/CORPUS/` **< 15%**.
- **Diversidade**: não repetir tag nem conector no mesmo mix.

---

### 8.2) Comandos de rotina (GPT Plus)

**Listar / filtrar**
/FEWSHOT_LIST tags:[didatico,critico_construtivo] limit:10


**Pontuar em lote**
/FEWSHOT_AUDIT tags:[*] filters:{score<0.82|overlap>=15%|redlist>0}


**Reescrever os reprovados (mínima mudança)**
/FEWSHOT_FIX id:<id> issues:["cadence_off","no_punch","low_heat","redlist_hit"]


**Selecionar para a peça atual (mix automático)**
/FEWSHOT_MIX select:{max:3} constraints:{formato:"artigo"}


**Injetar no prompt (pré-geração)**
/FEWSHOT_INJECT formato:"artigo" max_fewshots:3


---

### 8.3) Backup/Export (markdown único)
/FEWSHOT_EXPORT scope:"all" format:"markdown_block"

→ Entrega um bloco `.md` com todos os fewshots aprovados (texto + tags + scores) para você colar no seu repo.

**Importar de volta (cole o bloco)**
/FEWSHOT_IMPORT markdown:"<bloco colado>"


---

### 8.4) Higiene da biblioteca

**Deletar duplicatas/parecidos**
/FEWSHOT_DEDUP threshold_semantic:0.90 action:"review"


**Rotacionar conectores (anti-caricatura)**
/FEWSHOT_ROTATE_CONNECTORS avoid:["Sem rodeio:","O ponto é:"] prefer:["na prática:","resumo:","olha só","entendeu?"]


**Equalizar tags (evitar viés)**
/FEWSHOT_BALANCE_TAGS target_dist:{didatico:30,critico_construtivo:25,analitico:20,energetico:15,confessional_contido:5,humor_ironico_leve:5}


---

### 8.5) Política de entrada/saída

- **Entrada**: só aceita fewshot com `StyleScore ≥ 0.82`, `Lexicon ≥ 0.95`, `Overlap < 15%`.
- **Saída**: arquivar (export) qualquer item que caia **2 ciclos seguidos** abaixo do limiar.
- **Rotina**: 1 auditoria quinzenal (`/FEWSHOT_AUDIT`) + 1 rotação leve de conectores.

---

### 8.6) Troubleshooting rápido

| Sintoma | Causa provável | Ação |
|---|---|---|
| Estilo “morno” | Heat baixo ou falta de `—` | Repor `critico_construtivo`; usar `—` com função |
| Ritmo mecânico | Burstiness baixo | Garantir longa+curta no conjunto |
| Saída repetindo conector | Mix sem rotação | `/FEWSHOT_ROTATE_CONNECTORS` |
| Eco com CORPUS | Overlap alto | `/FEWSHOT_FIX issues:["overlap"]` ou re-sintetizar |
| Jargão/promo | Redlist | `/FEWSHOT_FIX issues:["redlist_hit"]` |

---

### 8.7) Checklist final (antes de publicar)

- [ ] Mix com **até 3 fewshots** e tags variadas.  
- [ ] **Longa + curta** presentes; `:` na síntese, `—` no contraste.  
- [ ] **Whitelist ≥1**, **redlist = 0**.  
- [ ] **Overlap < 15%**; cadência dentro do preset do formato.  
- [ ] Export atualizado, se entrou/saíram itens.

---

### 8.8) Comandos rapidos (no chat)

/FEWSHOT_LIST tags:[didatico,critico_construtivo] limit:5
/FEWSHOT_EDIT id:'T3-AR-03' acao:'refinar'
/FEWSHOT_SCORE id:'T3-AR-03'

### Comandos de Humanização

/HUMANIZE_SCORE_TEXT  
args: { texto: "<texto ou bloco>" }  
Avalia o índice de humanização com base nas métricas de 06_HUMANIZATION_POLICIES.md  
Retorna score detalhado + flags + recomendações  

/HUMANIZE_ENFORCE  
args: { texto: "<texto>", modo: "auto" | "assistido" }  
Reescreve o texto quando o índice < 65  
Usa técnicas de variação sintática, tom e calor  

/HUMANIZE_QUICKCHECK  
args: { texto: "<texto>", flags: ["flat_tone","cold_prescription","no_question","no_consequence"] }  
Faz checagem leve de estilo IA vs humano  

/HUMANIZE_COMPARE  
args: { A: "<texto_original>", B: "<texto_reescrito>" }  
Compara StyleScore e HumanizationIndex entre duas versões  

/HUMANIZE_REPORT  
args: { folder: "EVAL/" }  
Gera um sumário consolidado de humanização em lote (modo manual)  

Execucao no chat
Peca ao agente
saida 100% original
nao copie frases
Comandos rapidos

→ Pesos do StyleScore: ver 04_SCORER.md (fonte única).
→ HEAT usa níveis inteiros (3 base; 4 só em pico breve). Evite valores decimais.

---

## Tópico 9 — Exemplos Reais de Cadência Humana (CORPUS_RAW)

> **Fonte:** Transcrições reais extraídas do CORPUS_RAW para referência de cadência natural.
> **Uso:** Apenas para análise de padrões de fala humana — NÃO copiar frases na saída final.

### 9.1) Exemplos de Cadência Natural

**EXEMPLO_REAL_001** — Tom conversacional empresarial
```
"E então antissocial para isso e também para tipo outro exemplo de eu ficar antissocial cara eu tinha uma empresa chamada COB que ela vivia de eventos é eu encontrar meus clientes barra seguidores em lugar em lugares diferentes do mundo por causa disso eu falei não quero mais não ah mas eu vou deixar de ganhar 1 2 milhões de por ano não não preciso disso entendeu então e eu parei de frequentar eventos"
```
- **Características:** Variação sintática natural, 2ª pessoa ("entendeu"), detalhes sensoriais (empresa, eventos, lugares)
- **Cadência:** 58 palavras, 3 sentenças, variação 0.72

**EXEMPLO_REAL_002** — Tom analítico com personalidade
```
"Cara, esses dias eu vi uma pesquisa que mostrava que o skill número um que as mulheres apreciavam no homem não era o o dinheiro, era idiomas. Bum. Fui lá, aprendi um idioma, 2 3 4 5 idiomas. Se você contar montenegrino, sérvio, croata, eh, como mesmo como idiomas diferentes, coloca mais três aí."
```
- **Características:** Interjeições naturais ("Bum"), 2ª pessoa ("você"), detalhes específicos (idiomas)
- **Cadência:** 52 palavras, 3 sentenças, variação 0.68

**EXEMPLO_REAL_003** — Tom didático com experiência pessoal
```
"O que que são esses fundamentos, cara? Quando eu era atleta, a gente tinha, cara, eu tinha que treinar, eu tinha que subir o estádio, botar um pé no degrau da arquibancada de cima e fazer agachamento com joelho de base e simular o movimento do chute."
```
- **Características:** Pergunta direta, detalhes sensoriais (estádio, arquibancada, movimento), 2ª pessoa ("cara")
- **Cadência:** 45 palavras, 2 sentenças, variação 0.75

**EXEMPLO_REAL_004** — Tom crítico com exemplos concretos
```
"Quando o carro importado ficou acessível, Porsche, Porsche é coisa de Novo Rico, de gente que mora em Alfaville, de Raul, de facção criminosa, Rand Rover Velar também. É exatamente isso que quer dizer aqui o o texto, ó."
```
- **Características:** Repetição natural ("Porsche, Porsche"), detalhes específicos (marcas, lugares), 2ª pessoa implícita
- **Cadência:** 35 palavras, 2 sentenças, variação 0.71

**EXEMPLO_REAL_005** — Tom analítico com comparação geográfica
```
"Esse círculo aí do Brasil, América do Sul, é o único lugar do mundo onde o pobre come carne vermelha. Agora pensa aí. E aí eu parei e lembrei. África sub-saariana, o pobre come grãos. É muito difícil você ter acesso à carne de boi, porque não tem criação de boi no deserto."
```
- **Características:** 2ª pessoa ("você", "agora pensa aí"), detalhes sensoriais (carne, deserto, grãos), variação temporal
- **Cadência:** 48 palavras, 4 sentenças, variação 0.69

### 9.2) Padrões Identificados

**Conectores Naturais Reais:**
- "E então", "tipo", "cara", "agora pensa aí", "é exatamente isso"
- "Bum", "eh", "ó", "entendeu"

**Variação Sintática Natural:**
- Média: 0.71 (vs. 0.50 mínimo para aprovação)
- Alternância entre frases curtas e longas
- Uso natural de interjeições e pausas

**Detalhes Sensoriais:**
- Lugares específicos (estádio, deserto, Alfaville)
- Objetos concretos (carros, idiomas, carne)
- Ações físicas (agachamento, movimento do chute)

**2ª Pessoa Natural:**
- "você", "cara", "entendeu", "agora pensa aí"
- Uso implícito no contexto conversacional

---

## Política de Pontuação (Sincronizada)

### Arquivo completo (inclui docs/YAML)
- **Dois-pontos:** máximo 20 (tolerância para documentação)
- **Travessões:** máximo 15 (tolerância para documentação)

### Limites por fewshot individual (o que realmente importa)
- **Dois-pontos:** máximo 1 (":" só na síntese)
- **Travessões:** máximo 1 ("—" só no contraste)
- **Punch_per_100w:** [2.0, 4.0] (coerente com presets)

> **Nota:** Limites por peça substituem qualquer regra global antiga.

> ✅ Compatível com GPT Plus — execução interativa e sem caminhos externos.

