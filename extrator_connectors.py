# -*- coding: utf-8 -*-
# EXTRATOR — connectors.json (modo estrito, 100% do corpus)
# Saídas:
#   assets/connectors.json        -> [{text, count, sources[]}]
#   assets/connectors_report.json -> estatísticas e exemplos

import os, re, json, glob, unicodedata
from collections import defaultdict, Counter

# >>> ajuste o diretório das transcrições se necessário:
TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR") or os.getcwd()
ASSETS_DIR = os.path.join(os.getcwd(), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# --------- limpeza mínima ----------
EMOJI   = re.compile(r'[\U00010000-\U0010ffff]')
BRACK   = re.compile(r'\[.*?\]')
URL     = re.compile(r'https?://\S+|www\.\S+')
TIMECOD = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b')
MULTI   = re.compile(r'\s+')
SENT_SPLIT = re.compile(r'(?<=[\.!?…])\s+')

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

def wc_ok(s, lo=6, hi=40):
    n = len(s.split()); return lo <= n <= hi

# --------- whitelist de conectores (somente início + vírgula) ----------
WHITELIST = [
    "Na prática", "Por fim", "Além disso", "Por outro lado", "Em resumo",
    "Enquanto isso", "Logo depois", "Antes de mais nada", "Em vez disso",
    "Por isso", "Então", "De quebra"
]
LEAD_RX = re.compile(r'^(' + '|'.join([re.escape(c) for c in WHITELIST]) + r'),\s', re.IGNORECASE)

# --------- varredura ----------
cnt = Counter()
sources = defaultdict(set)
files = sorted(glob.glob(os.path.join(TRANSCRIPTS_DIR, "**", "*.txt"), recursive=True))
files_scanned = 0

for fp in files:
    try:
        raw = open(fp, "r", encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    files_scanned += 1
    rel = os.path.relpath(fp, TRANSCRIPTS_DIR)
    txt = clean_text(raw)
    for s in sentences(txt):
        if not wc_ok(s): 
            continue
        m = LEAD_RX.match(s)
        if not m: 
            continue
        # pega o conector na forma canônica (como definido na whitelist, respeitando caixa da whitelist)
        # normaliza para o primeiro item da whitelist que case em casefold()
        found = m.group(1)
        canon = next((w for w in WHITELIST if w.casefold()==found.casefold()), found)
        cnt[canon] += 1
        sources[canon].add(rel)

# --------- filtragem: freq>=2 e >=2 fontes ----------
connectors = [
    {"text": c, "count": int(n), "sources": sorted(list(sources[c]))}
    for c, n in cnt.most_common()
    if n >= 2 and len(sources[c]) >= 2
]

# salvar
out_path = os.path.join(ASSETS_DIR, "connectors.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(connectors, f, ensure_ascii=False, indent=2)

report = {
    "transcripts_dir": TRANSCRIPTS_DIR,
    "files_scanned": files_scanned,
    "whitelist_size": len(WHITELIST),
    "candidates_found": sum(cnt.values()),
    "connectors_kept": len(connectors),
    "top_examples": connectors[:5]
}
rep_path = os.path.join(ASSETS_DIR, "connectors_report.json")
with open(rep_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print({"ok": True, "files": files_scanned, "kept": len(connectors), "output": out_path, "report": rep_path})
