# 02_PROMPT_SKELETONS.md
> Blocos de prompt prontos para planejar, gerar, reescrever e validar no estilo Angelo.  
> Use em conjunto com `01_STYLE_SPEC.md` e `03_RAG_STYLE.md`.
> 
> **Versão calibrada para ChatGPT Plus (execução 100% interativa, sem interação externa).**

---

## 0) Como usar
1. **Preencha o BRIEF (Tópico 1)** com: tarefa, público, objetivo, restrições e links.  
2. Escolha o **Skeleton** conforme formato (Tópicos 2–4) **e objetivo** (Tópico 5).  
3. Aplique os **presets de ritmo e calor** (Tópico 6).  
4. (Opcional) Injete **few-shots do RAG** no bloco (Tópico 7).  
5. Gere o rascunho → **avalie/rewrite** com o bloco de reescrita (Tópico 8).  
6. Rode a **checagem final** e produza o **relatório compacto** (Tópico 9).

> **Execução no chat**; **peça ao agente** para usar os skeletons; **não copie frases** dos templates; **saída 100% original**.

> Regra: todos os skeletons presumem os gates e métricas do `01_STYLE_SPEC.md`.

---

## 1) BRIEF padrão (preencher antes de gerar)

### 1.1) Template de BRIEF
Tarefa/tema: {o que escrever; ângulo principal}
Público: {perfil do leitor}
Objetivo da peça: {informar | orientar | convencer | chamar pra ação}
Formato: {thread | artigo | roteiro}
Calor alvo: {2–5}
Ritmo alvo: {AvgSentenceLen=18–22, Stdev=6–8, Paragraph=50–120}
Restrições: {tamanho, data, fontes obrigatórias, jurisdição}
Links/dados de apoio (opcional): {lista com datas exatas}
CTA desejado: {ação + métrica (ex.: “7 dias de execução; medir X”)}
Observações: {tom específico, palavras a evitar, nuances}


### 1.2) Exemplo preenchido (thread)
Tarefa/tema: Clareza antes de intensidade na rotina de criadores
Público: iniciantes (18–28)
Objetivo da peça: orientar
Formato: thread
Calor alvo: 3–4
Ritmo alvo: AvgSentenceLen=19, Stdev=6, Paragraph=70–90
Restrições: 7 blocos; sem jargão; sem redlist
Links/dados de apoio: {"2024-11-10": estudo interno com 120 criadores}
CTA desejado: "Executa 7 dias; mede % de posts que movem a métrica"
Observações: usar “Sem rodeio:” e “Resumo:”


### 1.3) Exemplo preenchido (artigo)
Tarefa/tema: Por que “motivar” é pior que medir (para times pequenos)
Público: founders e líderes júnior
Objetivo da peça: convencer
Formato: artigo
Calor alvo: 3 (pico 4 no meio)
Ritmo alvo: AvgSentenceLen=20, Stdev=7, Paragraph=70–110, H2/150–250w
Restrições: 900–1200 palavras; incluir 1 caso real; sem promo-speak
Links/dados de apoio: {"2023-08-02": pesquisa X; "2025-05-14": relatório Y}
CTA desejado: “Definir 1 métrica e rodar 14 dias; comparar baseline”
Observações: fecho curto, imperativo; travessão só 1–2


### 1.4) Bloco “sanity check” do BRIEF (colado no prompt)

[BRIEF_CHECK]

A tarefa é específica?
Público definido (1 perfil)?
Objetivo único (1 verbo)?
Ritmo e calor têm valores?
Restrições e links estão claros?
CTA contém ação + métrica?
Se qualquer “não” → solicitar ajuste de BRIEF antes de gerar.

## 2) Skeleton — Thread / Post curto (modo social ou X)

> Estrutura de 5 a 8 blocos curtos com cadência oral, viradas claras e **punch de fechamento**.  
> Usado para posts de LinkedIn, X (Twitter), Threads e notas rápidas.

---

### 2.1) Estrutura macro (modelo base)
[Gancho] → [Tese curta] → [Prova 1] → [Prova 2] → [Síntese] → [CTA leve]

**Blocos-padrão:**
1️⃣ **Gancho (abridor de tensão):**
> "Cara, você não precisa de mais energia — você precisa de menos confusão."  
> "O que trava você não é a falta de ideia. É excesso de opção que você vê como barulho."

2️⃣ **Tese curta:**
> "A clareza sempre ganha do impulso — como água ganha de fogo."

3️⃣ **Provas (2 blocos):**
- exemplo real (você, alguém, cultura pop, negócio)  
- dado prático ou síntese de observação  

4️⃣ **Síntese (fecho mental):**
> "Você não decide o futuro — você decide o ritmo que funciona para você."

5️⃣ **CTA leve (movimento):**
> "Você executa 7 dias e mede o que mudou."  
> "Sem romantizar. Você só compara antes e depois — e vê o rastro."

---

### 2.2) Regras estilométricas específicas
| Elemento | Faixa / Regra |
|-----------|----------------|
| **Frase média** | 16–22 palavras (σ 6) |
| **Parágrafo** | 40–80 palavras |
| **Calor alvo** | 3–4 |
| **Marcas de calor** | 1 a cada 2 blocos |
| **Pausa simulada** | travessão `—` ou “tá?” a cada 3–4 frases |
| **Vocabulário** | direto, oralizado, sem jargão |
| **Punchlines** | terminam com ponto final seco |

---

### 2.3) Template de prompt (modo geração)
[PROMPT_THREAD]
Tarefa: {tema resumido}
Público: {perfil resumido}
Objetivo: {informar / orientar / provocar}
Calor alvo: {3–4}
Ritmo alvo: Frase média 18±6
Referências (RAG): {opcional}

Escreva uma thread de 5–8 blocos no estilo Angelo:
Abrir com tensão e frase seca.
Conduzir com raciocínio oralizado.
Alternar prova e provocação.
Fechar com frase de síntese + CTA leve.
Sem hashtags. Sem emojis. Sem “motivação”.

---

### 2.4) Exemplo (tema: clareza antes de intensidade)
Clareza vence intensidade.
Você não precisa de mais energia — você precisa de menos confusão.

Todo criador que você conhece erra do mesmo jeito: você tenta fazer dez coisas por semana, mas mede zero.

Cara, se você não mede, você reza. E a sorte nunca escala para você.

O jogo não é você fazer mais. É você fazer o que deixa rastro — e repetir até virar hábito natural.

Você executa 7 dias. Você compara antes e depois. O resto é barulho que você ignora como chuva.

---

### 2.5) Bloco de pós-edição (revisão interativa no GPT Plus)
[REWRITE_THREAD]

Garantir 1 punchline por bloco.
Substituir abstrações por ação concreta.
Revisar se cada bloco tem 1 verbo de movimento que você faz (decide, executa, mede).
StyleScore alvo ≥ 0.82.
Calor médio 3.5 (pico 4 no meio).
Ritmo dentro de 18±6.


---

### 2.6) Microchecagem final
| Verificação | OK |
|--------------|----|
| Gancho com tensão inicial | [ ] |
| Tese clara (frase 2–3) | [ ] |
| 2 provas reais | [ ] |
| 1 síntese final | [ ] |
| CTA claro e mensurável | [ ] |
| Redlist = 0 | [ ] |
| StyleScore ≥ 0.80 | [ ] |

---

> **Resumo:** A thread é um soco com didática.  
> 7 blocos, ritmo oral, moral prática.  
> Sem enfeite — só clareza, lógica e provocação.

## 3) Skeleton — Artigo Web (modo longo e estruturado)

> Estrutura para textos de **800–1.600 palavras**, escaneáveis, com navegação clara (H2/H3),  
> provas concretas e **CTA mensurável**. Usa o “Modo Artigo” do StyleSpec.

---

### 3.1) Arquitetura do artigo (mapa)
H1 — Título (promessa clara)
Lide (50–80w) — dor/benefício + tese em 1 linha
H2 — Diagnóstico (o erro comum e o porquê)
H2 — Princípio (o que muda o jogo)
H2 — Aplicação (H3×3 passos com critérios)
H2 — Contrapeso (limites/risco/condição de borda)
H2 — Casos rápidos (2–3 exemplos objetivos)
H2 — Fecho/CTA (o que fazer em 7–14 dias + como medir)

**Regras de escaneabilidade:**
- `H2/H3` a cada **150–250 palavras**  
- Parágrafos **50–120 palavras**  
- **Listas** (3–5 itens) a cada 200–300 palavras  
- **Pull-quote** opcional (máx. 2) para punchline

---

### 3.2) Sinais de tom e ritmo (alvos)
| Métrica | Alvo | Faixa |
|---|---:|:---:|
| AvgSentenceLen | **20** | 18–28 |
| StdevSentenceLen | **7** | 6–8 |
| ParagraphWords | **70–110** | 50–120 |
| Calor | **3** | pico **4** no meio |
| Dois-pontos/100w | **1–3** | — |
| Travessões/100w | **0–2** | — |
| Conectivos/100w | **≥ 3** | — |

---

### 3.3) Template de prompt (geração do rascunho)
[PROMPT_ARTIGO]
Tarefa/tema: {defina o ângulo principal}
Público: {perfil}
Objetivo: {informar|orientar|convencer}
Calor: alvo 3 (pico 4 na virada)
Ritmo: AvgSentenceLen=20 (σ=7), Paragraph=70–110, H2/150–250w
Links/dados: {opcional, com datas}
Restrições: {tamanho, fontes, jurisdição, redlist=0}

Escreva um artigo no estilo Angelo com a arquitetura:
H1 → Lide (50–80w, tese 1 linha) →
H2 Diagnóstico → H2 Princípio →
H2 Aplicação (H3×3 com critérios) →
H2 Contrapeso → H2 Casos (2–3) → H2 Fecho/CTA.

Instruções de estilo:

Voz: mentor pragmático, direto, sem jargão.
Conectivos preferidos: “então”, “agora”, “ou seja”, “por isso”.
Inserir 1 frase curta a cada 2–3 parágrafos.
Usar 1 expressão whitelist (“Resumo:”, “Na prática:”, “O ponto é:”).
CTA final com ação + métrica (7–14 dias).

---

### 3.4) Modelos de seções (copiar/colar)

**H1 — Título (3 alternativas)**
- “{Benefício} sem {custo ilusório}: um método simples”  
- “Pare de {erro comum}: clareza antes de intensidade”  
- “Como {resultado} em {tempo} fazendo o básico bem-feito”

**Lide (50–80w)**
> Enuncie a dor **sem suspense**. Mostre por que importa agora.  
> **Tese em 1 linha** no final (ex.: “Em uma frase: X > Y.”).

**H2 — Diagnóstico**
- O que a maioria faz de errado (e por que).  
- 1 dado/sinal, 1 exemplo prático.  
- Feche com mini-síntese: "X gera Y."

**H2 — Princípio**
- Defina o **princípio simples** que muda o jogo.  
- Explique com 1 metáfora concreta (vida real ou bastidor).  
- Prepare a aplicação: "Aplicação: …"

**H2 — Aplicação**
- **H3 Passo 1:** imperativo + **critério de sucesso** (como medir).  
- **H3 Passo 2:** idem.  
- **H3 Passo 3:** idem.  
- Lista curta de ferramentas mínimas (planilha, rotina, tempo).

**H2 — Contrapeso**
- Quando **não** usar; riscos de exagero; condição de borda.  
- Garante confiança: honestidade > propaganda.

**H2 — Casos rápidos**
- 2–3 mini-casos (4–6 linhas cada).  
- “Contexto → Ação → Resultado (métrica + data)”.

**H2 — Fecho/CTA**
- Frase curta de síntese.  
- CTA: “Decide hoje. Executa 7–14 dias. Mede {métrica}. Ajusta.”

---

### 3.5) Exemplo de outline preenchido (tema fictício)
H1: Clareza antes de intensidade: como parar de correr no lugar
Lide: A pressa não é o problema. A falta de clareza é. Se você confunde o que você vê
movimento com avanço, você gasta energia onde a métrica não mexe. Em uma frase:
clareza antes de intensidade que você vê.

H2 Diagnóstico

Todo time que você vê fica ocupado demais e produtivo de menos.
Sinal: 70% das tarefas semanais não mexem a métrica que você quer.
Esforço sem direção vira ansiedade.

H2 Princípio
Você usa uma alavanca por vez. A métrica define o que você vê viver e morrer.
Sua prioridade é você dizer "não" com método que você entende.

H2 Aplicação
H3 Passo 1 — Você define 1 métrica: {exemplo}. 
Sucesso: você vê variar ≥10% em 14 dias.

H3 Passo 2 — Você corta 3 tarefas que não mexem nessa métrica (lista que você faz).

H3 Passo 3 — Você executa rotina mínima diária (15–25min) + planilha que você vê.

H2 Contrapeso
Se a métrica já está estável, gargalo é priorização (não clareza).
Risco: trocar métrica todo dia (quebra consistência).
H2 Casos rápidos
Caso A: criador solo — cortou lives diárias → +18% em retenção.
Caso B: equipe pequena — 3 sprints focados → -22% retrabalho.
H2 Fecho/CTA
Menos tese, mais prática.
CTA: decide hoje, roda 14 dias, mede {métrica}, ajusta.


---

### 3.6) Bloco de reescrita (pós-avaliação)
[REWRITE_ARTIGO]
Objetivo: elevar StyleScore ≥ 0.83 sem mudar conteúdo.
Ações:

Ritmo: ajustar frases para 18–28 (σ 6–8); quebrar parágrafos >120w.
Estrutura: garantir H2/H3 a cada 150–250w; passos com critério de sucesso.
Léxico: remover redlist; inserir 1 expressão whitelist.
Calor: pico 4 na seção de virada/provas; fecho firme.
Pontuação: ":" para síntese/listas; "—" 0–2/100w para punch.

---

### 3.7) Checagem final & métricas (hooks para o SCORER)
- `H2/H3SpacingOK` ✅  
- `AvgSentenceLen ∈ [18,28]` ; `Stdev ∈ [6,8]`  
- `ParagraphWords ∈ [50,120]` (≥90% dos parágrafos)  
- `Connectives/100w ≥ 3`  
- `ListPresence ≥ 2`  
- `WhitelistPresence ≥ 1/250w` ; `Redlist = 0`  
- `HeatCurveMatch` (pico no meio; fecho 4 breve)  
- `CTACompleteness` (verbo + métrica + horizonte 7–14 dias)  
- `StyleScore ≥ 0.83`

---

### 3.8) Snippets prontos (colar quando precisar)

**Pull-quote (punch):**  
> “Não é drama — é método.”

**Síntese:**  
> "Clareza antes de intensidade."

**Aplicação (box):**  
> 1) Define uma métrica.  
> 2) Corta o que não mexe nela.  
> 3) Executa 7–14 dias. Mede. Ajusta.

**Fecho curto:**  
> “Decide hoje. Executa. Mede.”

## 4) Skeleton — Roteiro de Vídeo/Voz (curto e médio)

> Estrutura para **60–90s (short)** e **5–7 min (médio)** com cadência oral, pausas, e sinais de edição.  
> Frases levemente **mais curtas**, picos de calor mais claros e **CTA falado**.

---

### 4.1) Parâmetros de voz (vídeo/voz)
| Métrica | Alvo curto (60–90s) | Alvo médio (5–7 min) | Observações |
|---|---:|---:|---|
| **AvgSentenceLen** | 12–18 | 14–20 | oralidade: frases menores |
| **Stdev** | 5–8 | 6–9 | variação viva |
| **Parágrafo/bloco** | 1–3 linhas | 2–4 linhas | respiração + cortes |
| **Calor** | 3–5 (picos breves) | 3–4 (picos controlados) | calor em ondas |
| **Punch/100w (“—”, “:”)** | 2–5 | 1–3 | ênfase falada |
| **Imperatives/100w** | 4–10 | 3–7 | move à ação |

> **Marcações de palco:**  
> `[PAUSA]` (respirar / timing) · `[B-ROLL: …]` (recurso visual) · `[ON SCREEN: …]` (texto/tela).

---

### 4.2) Esqueleto — **Short 60–90s**
[FRIO RÁPIDO 1–2s] — provoca / recorte do clímax
[GANCHO 5–8s] — tensão + promessa
[TESE 1 linha] — ponto central
[PROVAS RÁPIDAS ×2] — exemplo e contraexemplo (concreto)
[PASSO ÚNICO] — o que fazer hoje (imperativo)
[CTA FALADO] — ação + métrica + tempo
[FECHO 1 linha] — punch final (curto)

**Template de prompt (short):**
[PROMPT_VIDEO_SHORT]
Tema: {…}
Público: {…}
Objetivo: {orientar|convencer|CTA}
Duração: 60–90s
Calor alvo: 4 (picos breves 5)
Ritmo: frases 12–18; stdev 5–8

Escreva roteiro no estilo Angelo com:
FRIO RÁPIDO (2s) que corta a atenção.
GANCHO com dor/benefício (1–2 frases).
TESE em 1 linha.
PROVAS RÁPIDAS (2 blocos, concretos).
PASSO ÚNICO executável hoje.
CTA FALADO com métrica (7 dias).
FECHO (frase curta).
Inclua marcações [PAUSA], [B-ROLL], [ON SCREEN].
Sem jargão, sem promo-speak.

**Exemplo (curto):**
[FRIO RÁPIDO] Você não precisa de motivação. Você precisa de clareza que você vê. [PAUSA]

[GANCHO] A maioria corre. Quase ninguém mede. [ON SCREEN: "Clareza > Intensidade"]

[TESE] Sem alvo, esforço vira ansiedade.

[PROVA] Criador A cortou 3 tarefas e mediu 7 dias — retenção subiu 14%.
[PROVA] Outro aumentou volume sem medir — cresceu zero. [B-ROLL: gráfico flat]

[PASSO] Você escolhe uma métrica. Você executa 15 min por dia. Você anota antes/depois.

[CTA] Sete dias. Você compara. Se não mexeu, você troca a alavanca — não a meta.

[FECHO] Sem rodeio: decide hoje. [PAUSA]

---

### 4.3) Esqueleto — **Médio 5–7 min**
[ABERTURA 5–10s] — FRIO + GANCHO
[TESE 1 linha]
[NUT-GRAF 20–30s] — por que importa (promessa de valor)
[BLOCO 1 — Diagnóstico] — erro comum + sinal real
[BLOCO 2 — Princípio] — o que muda o jogo (metáfora concreta)
[BLOCO 3 — Aplicação] — 3 passos com critério de sucesso
[BLOCO 4 — Contrapeso] — limite/risco (honestidade)
[CASOS RÁPIDOS ×2] — mini-histórias, dado e desfecho
[CTA FALADO] — plano 7–14 dias + métrica
[FECHO] — punch final + linha de moral

**Template de prompt (médio):**
[PROMPT_VIDEO_MEDIO]
Tema: {…}
Público: {…}
Objetivo: {informar|orientar|convencer}
Duração: 5–7 min
Calor alvo: 3–4 (picos 4)
Ritmo: frases 14–20; stdev 6–9

Roteiro no estilo Angelo com:
ABERTURA (FRIO + GANCHO + TESE).
NUT-GRAF (por que agora).
4 BLOCOS (Diagnóstico, Princípio, Aplicação 3 passos, Contrapeso).
CASOS RÁPIDOS ×2 (contexto → ação → métrica).
CTA FALADO (ação + métrica + horizonte).
FECHO (frase seca + moral).
Inserir [PAUSA], [B-ROLL], [ON SCREEN], [SFX opcional].

**Exemplo (médio) — esqueleto preenchido:**
[ABERTURA/FRIO] Você não está cansado; está confuso. [PAUSA]
[GANCHO] Corre todo dia e a métrica não mexe. [ON SCREEN: “Movimento ≠ Avanço”]
[TESE] Clareza vence intensidade.

[NUT-GRAF] Hoje você sai com um método simples pra separar esforço de resultado. [B-ROLL: relógio+planilha]

[B1 — DIAGNÓSTICO] Todo time lota a agenda. Quase ninguém mede. [ON SCREEN: “70% tarefas não mexem a métrica”]

[B2 — PRINCÍPIO] Uma alavanca por vez. Prioridade é dizer “não” com método. [PAUSA]
Metáfora: obra — um tijolo por vez, prumo e nível. [B-ROLL: obra]

[B3 — APLICAÇÃO]
Passo 1 — Define 1 métrica. Sucesso: variar ≥10% em 14 dias.
Passo 2 — Corta 3 tarefas que não mexem nela.
Passo 3 — Rotina diária 15–25min + planilha. [ON SCREEN: checklist]

[B4 — CONTRAPESO] Se sua métrica já está estável, o gargalo é priorização — não clareza.

[CASO 1] Criador solo: cortou lives diárias → +18% retenção.
[CASO 2] Time pequeno: 3 sprints focados → -22% retrabalho. [B-ROLL: barra caindo]

[CTA] Decide hoje. Roda 14 dias. Mede {métrica}. Se não mexer, troca a alavanca.
[FECHO] Menos tese, mais prática. [PAUSA] Decide. Executa. Mede.


---

### 4.4) Direção de gravação (ritmo e calor)
- **Ritmo:** 0.85–1.00× do normal (limpo, sem pressa).  
- **Pausas:** 0.3–0.6s após punchlines; 0.8–1.2s antes do CTA.  
- **Dicção:** verbos fortes (decide, executa, mede); substantivos concretos.  
- **Expressão:** firme, sem bronca; sorriso curto em viradas.  
- **Gestos:** mão marca “:”; travessão “—” vira breve inclinação de cabeça.

---

### 4.5) Bloco de pós-edição (captação/edição)
[REWRITE_VOICEOVER]

Cortar repetições e enroscos.
Substituir jargão por verbo simples.
Inserir [PAUSA] após punchlines.
Garantir 1 frase curta por bloco.
StyleScore ≥ 0.82 (curto) / ≥ 0.83 (médio).
Calor curva 3→4→3; pico breve.


**On-screen package (opcional):**
- `[ON SCREEN: “Sem rodeio:”]` no gancho.  
- Lower-third com **tese** (1 linha).  
- Box **“Na prática”** nos passos.  
- **Pull-quote**: “Não é drama — é método.”

---

### 4.6) Checklists finais

**Técnico (captação):**
- [ ] Áudio limpo (sem room echo).
- [ ] Pausas marcadas após punch.
- [ ] Ritmo falado dentro da faixa.

**Conteúdo (estilo):**
- [ ] Tese em 1 linha.
- [ ] 2 provas concretas.
- [ ] Passo(s) com critério de sucesso.
- [ ] CTA falado (ação + métrica + tempo).
- [ ] Redlist = 0; 1 expressão whitelist.

**SCORER (métricas):**
- `AvgSentenceLen` ok; `Stdev` ok.
- `Punch/100w` na faixa.
- `HeatCurveMatch` ≥ 0.8.
- `StyleScore` ≥ alvo.

---

### 4.7) Snippets prontos (colar)
- **Abertura:** "Você corre sem sair do lugar."  
- **Tese:** "Clareza vence intensidade."  
- **Aplicação:** "Define 1 métrica. Executa 7 dias. Mede."  
- **Fecho:** "Decide hoje. O resto é barulho."

## 5) Skeleton por Objetivo (Informar / Orientar / Convencer / CTA)

> Objetivo: escolher **uma intenção dominante** por peça e aplicar blocos de prompt com métricas e exemplos.  
> Regra: **1 objetivo por texto** (os outros podem aparecer como suporte, não como motor).

---

### 5.1) **Informar** (clareza > opinião)

**Quando usar:** notas técnicas, atualizações, sínteses de estudo, comparativos.  
**Tom/Calor:** 2–3 (autoridade calma).  
**Ritmo:** frase 18–22 (σ 6–8); parágrafo 60–110w.

**Estrutura macro:**
[Contexto curto] → [Fato 1 + fonte/data] → [Fato 2 + fonte/data]
→ [Comparação/variação] → [Síntese em 1 linha]


**Template de prompt:**
[PROMPT_INFORMAR]
Tarefa: sintetizar {assunto}
Público: {perfil}
Objetivo: informar (sem prescrição)
Calor: 2–3
Ritmo: 18–22 / σ 6–8 / 60–110w por parágrafo
Instruções:

Liste 2–4 fatos com datas e números (se houver).
Use conectivos: “agora”, “ou seja”, “por isso”.
Finalize com síntese “Em uma frase: …”.
Sem jargão; sem redlist; 1 expressão whitelist.


**Exemplo curtíssimo:**
> Em 2024, X cresceu 11%. Em 2025, a projeção caiu para 6%.  
> Ou seja: o ritmo desacelerou, mas ainda é positivo.

**Checklist (Informar):**
- [ ] 2–4 fatos datados  
- [ ] Síntese em 1 linha  
- [ ] Calor 2–3  
- [ ] Redlist = 0

---

### 5.2) **Orientar** (passos práticos + critério de sucesso)

**Quando usar:** tutoriais curtos, checklists, rotina mínima.  
**Tom/Calor:** 3–4 (didático e firme).  
**Ritmo:** frase 18–22; 1 frase curta a cada 2 parágrafos.

**Estrutura macro:**
[Gancho didático] → [Tese curta] → [Passos 3–5 com critério]
→ [Ferramenta mínima] → [Fecho com medição]

**Template de prompt:**
[PROMPT_ORIENTAR]
Tarefa: orientar {público} sobre {tema}
Objetivo: ação guiada
Calor: 3–4
Ritmo: 18–22; 1 frase curta a cada 2–3 parágrafos
Instruções:

Traga 3–5 passos no imperativo (1 alavanca por item).
Cada passo com critério de sucesso (como medir).
Inserir box “Na prática” (3 linhas).
Fechar com plano de 7–14 dias.

**Exemplo de passos:**
1) Define 1 métrica. Sucesso: variar ≥10% em 14 dias.  
2) Corta 3 tarefas que não mexem nela.  
3) Rotina diária de 15–25min + planilha simples.

**Checklist (Orientar):**
- [ ] 3–5 passos com critério  
- [ ] Box "Aplicação"  
- [ ] CTA 7–14 dias  
- [ ] Calor 3–4

---

### 5.3) **Convencer** (tese + provas + contrapeso)

**Quando usar:** ensaio opinativo com proposta prática.  
**Tom/Calor:** 3–4 (pico breve em 4).  
**Ritmo:** intercalar média com 1 frase curta por seção.

**Estrutura macro:**
[Gancho] → [Tese 1 linha] → [Prova 1: dado/precedente]
→ [Prova 2: caso prático] → [Prova 3: contraexemplo]
→ [Contrapeso] → [CTA medível]

**Template de prompt:**
[PROMPT_CONVENCER]
Tarefa: defender a tese {…}
Público: {…}
Calor: 3–4 (pico no miolo)
Instruções:

Tese em 1 linha (sem enrolar).
3 provas: dado, caso, contraexemplo.
Contrapeso honesto (quando não aplicar).
CTA com ação + métrica + horizonte.
Whitelist ≥ 1 (“O ponto é:”, “Resumo:”).

**Exemplo curtíssimo:**
> Tese: clareza vence intensidade.  
> Caso: cortamos 3 rotinas e a métrica subiu 18% em 21 dias.  
> Contrapeso: se a métrica já está estável, o gargalo é priorização.  
> CTA: decide hoje; roda 14 dias; mede.

**Checklist (Convencer):**
- [ ] Tese 1 linha  
- [ ] 3 provas distintas  
- [ ] Contrapeso  
- [ ] CTA mensurável

---

### 5.4) **CTA** (chamar pra ação direta)

**Quando usar:** fechamento de peça, anúncio de decisão, “cutucar” execução.  
**Tom/Calor:** 4–5 (pico breve, seguido de resfriamento).  
**Ritmo:** frases curtas, 1–2 linhas; punch seco.

**Estrutura macro:**
[Pain] → [Comando simples] → [Janela de tempo] → [Métrica] → [Fecho curto]
[PROMPT_CTA]
Tarefa: convocar {público} para {ação}
Calor: 4–5 (pico curto; depois 3)
Instruções:

2–3 frases curtas seguidas.
1 comando central (imperativo).
Janela: 7–14 dias. Métrica clara.
Sem justificativa longa; sem promo-speak.

**Exemplo curtíssimo:**
> Você decide hoje. Você executa 7 dias. Você mede {métrica}.  
> Se não mexeu, você troca a alavanca — não a meta.

**Exemplo com analogia:**
> Como um mecânico que testa uma peça por vez, você isola uma variável e mede o resultado.

**Checklist (CTA):**
- [ ] Imperativo explícito  
- [ ] Janela de tempo  
- [ ] Métrica do sucesso  
- [ ] Pico breve e resfriamento

---

### 5.5) Tabela rápida de diferenças

| Objetivo | Papel da tese | Provas | Passos | Contrapeso | CTA |
|---|---|---|---|---|---|
| **Informar** | síntese | 2–4 fatos | opcional | opcional | opcional |
| **Orientar** | curta | 1 prova leve | **3–5 com critério** | opcional | **sim** (7–14d) |
| **Convencer** | **1 linha** | **3 (dado/caso/contraex.)** | opcional | **sim** | **sim** |
| **CTA** | implícita | nenhuma | 1–2 verbos | não | **central** |

---

### 5.6) Pós-edição por objetivo (blocos prontos)

**[REWRITE_INFORMAR]**  
- Cortar adjetivos; manter datas/números.  
- Conectivos “ou seja”, “agora”, “por isso”.  
- StyleScore ≥ 0.80; calor 2–3.

**[REWRITE_ORIENTAR]**  
- Verbo no início do passo.  
- Critério de sucesso explícito por passo.  
- Inserir "Aplicação" (3 linhas).  
- StyleScore ≥ 0.82; calor 3–4.

**[REWRITE_CONVENCER]**  
- Tese em 1 linha; completar 3 provas.  
- Adicionar contrapeso se faltar.  
- CTA mensurável.  
- StyleScore ≥ 0.83; pico de calor breve.

**[REWRITE_CTA]**  
- Frases ≤ 9 palavras.  
- 1 comando + 1 métrica + 1 janela.  
- Remover qualquer jargão/eresumo de calibraçãoio vazio.  
- StyleScore ≥ 0.82; calor 4–5 (pico curto).

---

### 5.7) Snippets (colar conforme objetivo)

**Informar — síntese:**  
> “Em uma frase: {conclusão objetiva}.”

**Orientar — aplicação:**  
> "Aplicação: define 1 métrica, executa 7 dias, mede."

**Convencer — virada:**  
> "Você confunde movimento com avanço."

**CTA — fecho:**  
> “Decide hoje. Executa. Mede.”

## 6) Presets de Ritmo & Calor por Formato

> Objetivo: padronizar **alvos de ritmo, cadência e energia** por formato de peça.  
> Use estes presets para **configurar o prompt** (geração) e para **validar no SCORER** (avaliação).

---

### 6.1) Tabela-mãe de presets (resumo operacional)

→ No exemplo, use no máx. 1 conector whitelist e varie aberturas.

| Formato | AvgSentenceLen | Stdev | ParagraphWords | Calor alvo | Picos | Punch/100w (`:` + `—`) | Imperatives/100w | H2/H3 |
|---|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|
| **Thread/Post curto** | 16–20 | 6 | 40–80 | 3 | 1 pico breve | 2.0–4.0 | 3–7 | — |
| **Artigo Web** | 18–22 | 7 | 70–110 | 3 | pico 4 no meio | 2.0–4.0 | 2–6 | **H2/150–250w** |
| **Roteiro Vídeo (curto)** | 16–20 | 5–8 | 1–3 linhas/bloco | 3–4 (picos 5) | 1–2 picos curtíssimos | 2.0–4.0 | 4–10 | — |

→ Presets calibrados usando métricas do CORPUS (cadência≈18, punch≈2.8, heat≈3.1).
| **Roteiro Vídeo (médio)** | 16–20 | 6–9 | 2–4 linhas/bloco | 3–4 | 1 pico 4 | 2.0–4.0 | 3–7 | — |
| **Nota técnica / Informar** | 18–22 | 6–8 | 60–110 | 2–3 | sem pico | 2.0–4.0 | 1–3 | H2 opcional |
| **Ensaio/Convencer** | 18–22 | 6–8 | 70–110 | 3–4 | 1 pico breve | 2.0–4.0 | 2–5 | H2/200–300w |

> **Regra global:** inserir **1 frase curta (≤ 9 palavras)** a cada **2–3 parágrafos** (todos os formatos).

---

### 6.2) Preset — Thread/Post curto

**Parâmetros**  
- `AvgSentenceLen`: 16–20 · `Stdev`: ~6  
- `ParagraphWords`: 40–80 · `Calor`: 3 (1 pico)  
- `Punch/100w`: 2.0–4.0 · `Imperatives/100w`: 3–7  

**Curva de calor**: 2 → **3** → 3  
**Checklist**  
- [ ] Gancho com tensão (frase curta)  
- [ ] Tese em 1 linha  
- [ ] 2 provas rápidas (exemplo/dado)  
- [ ] Fecho com CTA leve  
- [ ] Redlist = 0; 1 expressão whitelist

**Hook SCORER**  
- `StyleScore ≥ 0.82` · `HeatCurveMatch ≥ 0.8` · `PunchDensity ∈ [2,4]`

---

### 6.3) Preset — Artigo Web

**Parâmetros**  
- `AvgSentenceLen`: 18–22 · `Stdev`: 7  
- `ParagraphWords`: 70–110 · `H2/H3`: a cada 150–250w  
- `Calor`: 3 (pico 4 na virada/provas)  
- `Punch/100w`: 2.0–4.0 · `Imperatives/100w`: 2–6

**Curva de calor**: 2 → 3 → **4** → 3 → 2–3  
**Checklist**  
- [ ] Lide (50–80w) + tese 1 linha  
- [ ] Diagnóstico → Princípio → Aplicação (H3×3) → Contrapeso → Casos → CTA  
- [ ] 2 listas distribuídas (3–5 itens)  
- [ ] Fecho com ação + métrica (7–14 dias)

**Hook SCORER**  
- `H2/H3SpacingOK` · `ParagraphWords ≥ 90% dentro da faixa` · `StyleScore ≥ 0.83`

---

### 6.4) Preset — Roteiro Vídeo (curto 60–90s)

**Parâmetros**  
- `AvgSentenceLen`: 16–20 · `Stdev`: 5–8  
- `Blocos`: 1–3 linhas cada  
- `Calor`: 3–4 (picos 5 curtos)  
- `Punch/100w`: 2.0–4.0 · `Imperatives/100w`: 4–10

**Curva de calor**: 3 → **3–4** → 3  
**Checklist**  
- [ ] FRIO rápido (2s) + Gancho  
- [ ] Tese 1 linha  
- [ ] Provas rápidas ×2  
- [ ] Passo único executável  
- [ ] CTA falado (métrica + tempo)

**Hook SCORER**  
- `HeatPeaks ≤ 2 e curtos` · `AvgSentenceLen ≤ 18` · `StyleScore ≥ 0.82`

---

### 6.5) Preset — Roteiro Vídeo (médio 5–7 min)

**Parâmetros**  
- `AvgSentenceLen`: 16–20 · `Stdev`: 6–9  
- `Blocos`: 2–4 linhas  
- `Calor`: 3–4 (pico 4)  
- `Punch/100w`: 2.0–4.0 · `Imperatives/100w`: 3–7

**Curva de calor**: 3 → **4** → 3  
**Checklist**  
- [ ] ABERTURA (frio+gancho+tese)  
- [ ] 4 blocos (Diagnóstico, Princípio, Aplicação×3, Contrapeso)  
- [ ] Casos rápidos ×2  
- [ ] CTA falado claro

**Hook SCORER**  
- `PunchDensity ∈ [1,3]` · `HeatCurveMatch ≥ 0.8` · `StyleScore ≥ 0.83`

---

### 6.6) Preset — Nota Técnica / Informar

**Parâmetros**  
- `AvgSentenceLen`: 18–22 · `Stdev`: 6–8  
- `ParagraphWords`: 60–110  
- `Calor`: 2–3 (sem picos)  
- `Punch/100w`: 1–2 · `Imperatives/100w`: 1–3

**Curva de calor**: 2 → 2–3 → 2  
**Checklist**  
- [ ] 2–4 fatos com **datas/números**  
- [ ] Comparação direta / variação  
- [ ] Síntese “Em uma frase:”  
- [ ] Evitar adjetivação e jargão

**Hook SCORER**  
- `DataDensity alta` · `HeatPeaks=0` · `StyleScore ≥ 0.80`

---

### 6.7) Preset — Ensaio/Convencer

**Parâmetros**  
- `AvgSentenceLen`: 18–22 · `Stdev`: 6–8  
- `ParagraphWords`: 70–110  
- `Calor`: 3–4 (pico breve)  
- `Punch/100w`: 2–3 · `Imperatives/100w`: 2–5

**Curva de calor**: 2–3 → **4** → 3  
**Checklist**  
- [ ] Tese 1 linha  
- [ ] 3 provas (dado, caso, contraexemplo)  
- [ ] Contrapeso honesto  
- [ ] CTA mensurável

**Hook SCORER**  
- `MovementCoverage=7/7` · `HeatPeak breve` · `StyleScore ≥ 0.83`

---

### 6.8) Preset de **Pontuação Assinatura** (todos os formatos)
- `Commas/100w`: 10–18 (oralidade sem vício)  
- `Colons/100w`: 1–4 (síntese/ordem)  
- `Dashes/100w`: 0–3 (punch)  
- **Regra:** “:” para síntese/lista; “—” para **uma** ênfase por parágrafo; evite reticências (“…”) e múltiplas interrogações.

---

### 6.9) Preset de **Conectivos** (mínimos por 100 palavras)
- Meta: **≥ 3** entre “então”, “agora”, “ou seja”, “por isso”, “só que”, “resumo de calibraçãoo”.  
- Falhou meta → reforçar costura lógica na reescrita.

---

### 6.10) Mapeamento rápido (objetivo → preset)

| Objetivo | Use preset base | Ajuste |
|---|---|---|
| Informar | Nota Técnica | Calor 2–3; Punch baixo |
| Orientar | Thread ou Artigo | Imperatives/100w ↑; Box "Aplicação" |
| Convencer | Ensaio/Convencer | Pico 4 breve; 3 provas + contrapeso |
| CTA | Thread curto | Frases ≤ 9 palavras; pico 4–5 breve |

---

### 6.11) Snippets de configuração (colar no prompt)

**Thread**  
ritmo: {avg=19, stdev=6, paragraph=40-80}
calor: {target=3-4, peaks="1 pico breve"}
punch_per_100w: 2-4
imperatives_per_100w: 3-7


**Artigo**  
ritmo: {avg=20, stdev=7, paragraph=70-110, h2_every=150-250w}
calor: {target=3, peak=4}
punch_per_100w: 1-3
imperatives_per_100w: 2-6

**Vídeo curto**  
ritmo: {avg=15, stdev=6, lines_per_block=1-3}
calor: {target=4, peaks="1-2 curtíssimos"}
punch_per_100w: 2-5
imperatives_per_100w: 4-10

---

### 6.12) Hooks do SCORER (globais para presets)
- `AvgSentenceLen` dentro da faixa do preset  
- `Stdev` dentro da faixa (burstiness)  
- `ParagraphWords` ≥ 90% dos parágrafos no intervalo  
- `HeatCurveMatch` ≥ 0.8  
- `PunchDensity` na faixa do preset  
- `Imperatives/100w` coerente com o objetivo  
- `StyleScore` ≥ alvo do formato

---

### 6.13) Checklist final (rápido)
- [ ] Preset certo para o formato?  
- [ ] Curva de calor respeitada?  
- [ ] Pontuação assinatura nas faixas?  
- [ ] Conectivos ≥ 3/100w?  
- [ ] CTA coerente com o objetivo?  
- [ ] StyleScore dentro do alvo?

> Se algo falhar, use o bloco de **Reescrita do formato** (Tópicos 2–4) e reavalie.

### 8.1) Comandos rapidos (no chat)

/USE_SKELETON formato: artigo objetivo: informar
/SKELETON_PREVIEW formato: roteiro partes:[abertura,virada,fecho]
/SKELETON_TUNE formato: thread target_avg_len:18 transitions:'<=40%'

Execucao no chat
Peca ao agente
saida 100% original
nao copie frases
Comandos rapidos

→ Pesos do StyleScore: ver 04_SCORER.md (fonte única).
