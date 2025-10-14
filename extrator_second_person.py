# -*- coding: utf-8 -*-
# EXTRATOR — second_person.json (modo estrito, 100% do corpus)
# Saídas:
#   assets/second_person.json          -> lista de {text, source}
#   assets/second_person_report.json   -> contagens e amostras

import os, re, json, glob, unicodedata

# >>> Ajuste aqui o diretório das transcrições, se necessário
TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR") or os.getcwd()

ASSETS_DIR = os.path.join(os.getcwd(), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# --------- Normalização e utilidades ----------
EMOJI = re.compile(r'[\U00010000-\U0010ffff]')
BRACK = re.compile(r'\[.*?\]')              # [DownSub.com], timestamps entre colchetes etc.
URL   = re.compile(r'https?://\S+|www\.\S+')
TIMECODE = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b')  # 00:12 ou 01:02:03

FILLERS = set('eh ah hã ã tipo mano cara rapaziada'.split())
VERB_NEAR = re.compile(
    r'\b(você|vc)\b.{0,18}\b('
    r'é|está|tá|foi|era|será|pode|precisa|tem|vai|quer|deve|consegue|vê|sente|pensa|olha|lembra|faz|fez|fará|ganha|ganhar|muda|mudar'
    r')\b',
    re.IGNORECASE
)

def clean_text(raw: str) -> str:
    raw = unicodedata.normalize('NFC', raw)
    raw = raw.replace('\r\n','\n').replace('\r','\n')
    lines = []
    for ln in raw.split('\n'):
        ln = EMOJI.sub('', ln)
        ln = BRACK.sub('', ln)
        ln = URL.sub('', ln)
        ln = TIMECODE.sub('', ln)
        ln = ln.strip(' -"''|•#\t')
        if not ln:
            continue
        lines.append(ln)
    text = ' '.join(lines)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

SENT_SPLIT = re.compile(r'(?<=[\.!?…])\s+')

def sentences(text: str):
    # Split e pequena correção para ASR que perde ponto final
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
    parts = s.split()
    return bool(parts and parts[0].lower() in FILLERS)

def dedup_keep_order(items, key=lambda x: x):
    seen=set(); out=[]
    for it in items:
        k = key(it)
        if k in seen: 
            continue
        seen.add(k); out.append(it)
    return out

# --------- Varredura ----------
paths = sorted(glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.txt"), recursive=True))
results = []
files_scanned = 0

for fp in paths:
    try:
        raw = open(fp, "r", encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    files_scanned += 1
    rel = os.path.relpath(fp, TRANSCRIPTS_DIR)
    txt = clean_text(raw)
    idx = 0
    for s in sentences(txt):
        idx += 1
        if not wc_ok(s): 
            continue
        if s[-1] not in '.!?…':
            continue
        if starts_with_filler(s):
            continue
        if not VERB_NEAR.search(s):
            continue
        results.append({"text": s, "source": f"{rel}#s{idx}"})

# --------- Dedup e salvar ----------
results = dedup_keep_order(results, key=lambda d: d["text"])

out_json = os.path.join(ASSETS_DIR, "second_person.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

report = {
    "transcripts_dir": TRANSCRIPTS_DIR,
    "files_scanned": files_scanned,
    "samples_kept": len(results),
    "rules": {
        "length_words": "10–34",
        "punctuation_final": True,
        "pattern": "você|vc + verbo em <=18 caracteres",
        "removed": ["emojis", "URLs", "timecodes", "conteúdo entre colchetes", "linhas vazias", "fillers no início"]
    },
    "examples": results[:5]
}
out_report = os.path.join(ASSETS_DIR, "second_person_report.json")
with open(out_report, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(json.dumps({
    "ok": True,
    "files_scanned": files_scanned,
    "second_person_saved": out_json,
    "report": out_report,
    "count": len(results)
}, ensure_ascii=False, indent=2))
