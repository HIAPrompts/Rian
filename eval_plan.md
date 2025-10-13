# eval_plan.md
> Plano de avaliação e calibração do sistema de **estilometria** (GPT Plus).  
> Uso 100% **interativo no chat**. Sem interação externa.

---

## Tópico 1 — Estrutura & Rotina de Avaliação

### 1.1) Objetivo
Garantir que o "**som da fala**" se mantenha estável em todos os formatos (thread, artigo, roteiro), medindo e corrigindo:
- **Cadence** (média de frase + burstiness)
- **Heat** (curva emocional e picos breves)
- **Lexicon** (whitelist ≥1; redlist = 0)
- **Punch** (uso intencional de `:` e `—`)
- **Originalidade** (overlap < 15% com CORPUS/FEWSHOTS)

> **Execução no chat**; **peça ao agente** para avaliar; **não copie frases** dos exemplos; **saída 100% original**.

---

### 1.2) Materiais de referência
- `probes.txt` → 12 **probes fixos** (temas/formatos/alvos).  
- **Presets globais** (coerentes com 01–05):
  - **Thread**: `avg_sentence_len 16–20`, `heat 3`, `punch 2.0–4.0/100w`, `transitions ≤ 40%`
  - **Artigo**: `avg_sentence_len 18–22`, `heat 3`, `punch 2.0–4.0/100w`, `transitions ≤ 35%`
  - **Roteiro**: `avg_sentence_len 16–20`, `heat 3–4`, `punch 2.0–4.0/100w`, `transitions ≤ 45%`

---

### 1.3) KPIs (pass/fail)
| KPI | Alvo | Observações |
|---|---|---|
| **StyleScore** | ≥ **0.80** por peça (média semanal ≥ 0.82) | composto (Cadence/Heat/Lexicon/Punch/Originalidade) |
| **LexicalCompliance** | ≥ **0.95** | whitelist≥1; redlist = 0 |
| **HeatCurveMatch** | ≥ **0.80** | pico 4 breve em virada/fecho (quando aplicável) |
| **Cadence** | dentro do preset por formato | ver 1.2 |
| **Punch /100w** | 2.0–4.0 | `:` em síntese; `—` em contraste |
| **Overlap** | < **15%** | com qualquer janela do CORPUS/FEWSHOTS |

---

### 1.4) Rotina de execução (no chat)

**Semanal (sanidade)**
/RUN_PROBES
source: "probes.txt"
sample: 6 # 2 por formato
steps: ["GERAR", "SCORER", "REWRITE_IF_FAIL", "SCORER"]
output: "resumo_markdown"

→ Esperado: ≥ 4/6 peças **pass** em 1–2 passes de reescrita.

**Mensal (regressão completa)**
/RUN_PROBES
source: "probes.txt"
sample: "all" # P001–P012
steps: ["GERAR","SCORER","REWRITE_IF_FAIL x3","SCORER"]
report: ["means","stdev","fail_reasons","suggested_tuning"]

→ Gera relatório com médias e sugestões de calibração.

---

### 1.5) Critérios de aceite por formato

**Thread**
- `avg_sentence_len 16–20`, burstiness alto, **≤ 40%** parágrafos com transição.
- Heat **3**; **1** pico 4 curto (opcional).
- **Punch** 2.0–4.0/100w; CTA curto.

**Artigo**
- `avg_sentence_len 18–22`; estrutura **tese→exemplos→síntese**.
- Heat **3**; pico 4 na **virada** *ou* **fecho** (breve).
- Punch 2.0–4.0/100w; `:` obrigatório na síntese principal.

**Roteiro**
- `avg_sentence_len 16–20`; oralidade (frases curtas que “andam”).
- Heat **3–4**; picos breves; **≤ 45%** falas com transição.
- `—` no contraste/virada; CTA claro.

---

### 1.6) Fluxo de correção (passo a passo)
1) Rodar SCORER → **identificar gates** reprovados.  
2) Aplicar **reparos localizados**:
   - `REWRITE_CADENCE` (longa+curta por seção)
   - `REWRITE_HEAT` (pergunta direta; mover pico)
   - `REWRITE_PUNCH` (":" em síntese; "—" no contraste)
   - `REWRITE_LEXICON` (glossário/remoção de jargão)
   - `REWRITE_ORIGINALITY` (troca de ordem/voz/imagética)
3) Rerrodar SCORER → aceitar se todos os gates passarem.

Atalho:
/FIX_ON_FAIL
targets: ["cadence","heat","punch","lexicon","originality"]
mode: "minimal_change"


---

### 1.7) Sinal de drift & quando calibrar
- **Sinais**: queda de `StyleScore_médio ≥ 0.03`, aumento de reprova por `originality` ou `punch`.  
- **Ação** (no chat):
/SUGGEST_TUNING
symptoms: ["style_down_0.03","punch_underuse","originality_warn"]
presets_current: "<auto>"
return: "patch_markdown" # patch para colar em 02/03/04

→ Ajustes típicos: `style_bias −0.05`, ampliar **k** (diversidade de janelas), refinar heat/punch por formato.

---

### 1.8) Relatório padrão (para arquivar)
/EVAL_REPORT
include: ["means","stdev","fail_gates","top_rewrites","tuning_patch"]
output: "markdown_block"

→ Cole o bloco no seu repositório (ou no próprio agente) como histórico.

---

### 1.9) Checklist rápido (passar/voltar)
- [ ] Rodou **RUN_PROBES** (amostra semanal/mensal).  
- [ ] **SCORER** aprovou com StyleScore ≥ 0.80 (média ≥ 0.82).  
- [ ] **Whitelisted** presente; **redlist = 0**.  
- [ ] **HeatCurveMatch ≥ 0.80**; pico no lugar certo.  
- [ ] **Punch** 2.0–4.0/100w, com função clara.  
- [ ] **Overlap < 15%**.  
- [ ] Relatório gerado e (se houver) **patch** colado nos presets.

---

### 1.10) Comandos rapidos (no chat)

/RUN_PROBES source:'probes.txt' sample:6 steps:['GERAR','SCORER']
/EVAL_REPORT include:['means','stdev','fail_gates'] output:'markdown'
/SUGGEST_TUNING symptoms:['style_down_0.03'] return:'patch_markdown'

Execucao no chat
Peca ao agente
saida 100% original
nao copie frases
Comandos rapidos

→ HEAT usa níveis inteiros (3 base; 4 só em pico breve). Evite valores decimais.
