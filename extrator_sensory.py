# -*- coding: utf-8 -*-
# EXTRATOR — sensory_pool.json (modo estrito, 100% do corpus)
# Saída: assets/sensory_pool.json  -> lista de {text, source}

import os, re, json, glob, unicodedata

# >>> ajuste o diretório das transcrições se necessário:
TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR") or os.getcwd()
ASSETS_DIR = os.path.join(os.getcwd(), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# --- limpeza ---
EMOJI   = re.compile(r'[\U00010000-\U0010ffff]')
BRACK   = re.compile(r'\[.*?\]')
URL     = re.compile(r'https?://\S+|www\.\S+')
TIMECOD = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b')
MULTI   = re.compile(r'\s+')
SENT_SPLIT = re.compile(r'(?<=[\.!?…])\s+')

FILLERS = set('eh ah hã ã tipo mano cara rapaziada'.split())

# léxico sensorial (cheiro/luz/som/textura/temperatura/cor/sabor)
SENS_RX = re.compile(
    r'\b('
    r'cheiro|aroma|odor|perfume|'
    r'luz|sombra|claridade|escuro|brilho|ofuscante|fosco|opaco|'
    r'som|ruído|silêncio|barulho|eco|voz|sussurro|'
    r'frio|quente|morno|gelado|úmido|seco|'
    r'áspero|macio|textura|liso|pegajoso|'
    r'sabor|gosto|amargo|doce|azedo|salgado|picante|'
    r'vermelh[oa]|azul|verde|amarel[oa]|branc[oa]|pret[oa]'
    r')\b', re.IGNORECASE
)

# opcional: filtros de "lixo comum" de ASR/marcas
CLUTTER = re.compile(r'\b(DownSub\.com|http|www\.|Records|Taylor Swift|Drake|Chris Brown|Manual do Guerreiro)\b', re.IGNORECASE)

def clean_text(raw: str) -> str:
    raw = unicodedata.normalize('NFC', raw).replace('\r\n','\n').replace('\r','\n')
    lines=[]
    for ln in raw.split('\n'):
        ln = EMOJI.sub('', ln)
        ln = BRACK.sub('', ln)
        ln = URL.sub('', ln)
        ln = TIMECOD.sub('', ln)
        ln = ln.strip(' -"''|•#\t')
        if ln:
            lines.append(ln)
    return MULTI.sub(' ', ' '.join(lines)).strip()

def sentences(text: str):
    for s in SENT_SPLIT.split(text):
        s = s.strip()
        if not s:
            continue
        if s[-1] not in '.!?…' and ',' in s and len(s.split()) >= 12:
            s += '.'
        yield s

def wc_ok(s, lo=10, hi=34):
    n = len(s.split()); return lo <= n <= hi

def starts_with_filler(s):
    p = s.split()
    return bool(p and p[0].lower() in FILLERS)

def dedup_keep_order(items, key=lambda x: x):
    seen=set(); out=[]
    for it in items:
        k = key(it)
        if k in seen: continue
        seen.add(k); out.append(it)
    return out

paths = sorted(glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.txt"), recursive=True))
results=[]
for fp in paths:
    try:
        raw = open(fp, "r", encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    rel = os.path.relpath(fp, TRANSCRIPTS_DIR)
    txt = clean_text(raw)
    for i, s in enumerate(sentences(txt), 1):
        if not wc_ok(s): 
            continue
        if s[-1] not in '.!?…': 
            continue
        if starts_with_filler(s): 
            continue
        if CLUTTER.search(s): 
            continue
        if not SENS_RX.search(s):
            continue
        results.append({"text": s, "source": f"{rel}#s{i}"})

results = dedup_keep_order(results, key=lambda d: d["text"])
out_path = os.path.join(ASSETS_DIR, "sensory_pool.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print({"ok": True, "files": len(paths), "kept": len(results), "output": out_path})