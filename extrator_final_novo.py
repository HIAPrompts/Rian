# -*- coding: utf-8 -*-
# EXTRATOR — second_person.json (modo estrito, 100% do corpus)
# Saída: assets/second_person.json  -> lista de {text, source}

import os, re, json, glob, unicodedata

# >>> Se precisar, troque aqui pelo nome da sua pasta de transcrições
TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR") or os.path.join(os.getcwd(), "EXTRAÇÃO DE TEXTO")
ASSETS_DIR = os.path.join(os.getcwd(), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# --- limpeza básica ---
EMOJI   = re.compile(r'[\U00010000-\U0010ffff]')
BRACK   = re.compile(r'\[.*?\]')                          # [DownSub.com], [00:12], etc.
URL     = re.compile(r'https?://\S+|www\.\S+')
TIMECOD = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b')     # 00:12 ou 01:02:03
MULTI   = re.compile(r'\s+')

FILLERS = set('eh ah hã ã tipo mano cara rapaziada'.split())
SENT_SPLIT = re.compile(r'(?<=[\.!?…])\s+')

# você|vc + verbo a até 18 caracteres de distância
VERB_NEAR = re.compile(
    r'\b(você|vc)\b.{0,18}\b('
    r'é|está|tá|foi|era|será|pode|precisa|tem|vai|quer|deve|consegue|vê|sente|pensa|olha|lembra|faz|fez|fará|ganha|ganhar|muda|mudar'
    r')\b',
    re.IGNORECASE
)

def clean_text(raw: str) -> str:
    raw = unicodedata.normalize('NFC', raw).replace('\r\n','\n').replace('\r','\n')
    lines = []
    for ln in raw.split('\n'):
        ln = EMOJI.sub('', ln)
        ln = BRACK.sub('', ln)
        ln = URL.sub('', ln)
        ln = TIMECOD.sub('', ln)
        ln = ln.strip(' -"''|•#\t')
        if ln:
            lines.append(ln)
    text = MULTI.sub(' ', ' '.join(lines)).strip()
    return text

def sentences(text: str):
    for s in SENT_SPLIT.split(text):
        s = s.strip()
        if not s:
            continue
        # corrige ASR sem ponto final quando há vírgulas e tamanho razoável
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
        if k in seen: 
            continue
        seen.add(k); out.append(it)
    return out

paths = sorted(glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.txt"), recursive=True))
results = []
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
        if not VERB_NEAR.search(s):
            continue
        results.append({"text": s, "source": f"{rel}#s{i}"})

# dedup e salvar
results = dedup_keep_order(results, key=lambda d: d["text"])
out_path = os.path.join(ASSETS_DIR, "second_person.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print({"ok": True, "files": len(paths), "kept": len(results), "output": out_path})
