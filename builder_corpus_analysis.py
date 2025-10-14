# -*- coding: utf-8 -*-
# BUILDER — corpus_analysis.json + rebuild_report.json (a partir de assets existentes)
# Lê: assets/{second_person.json, sensory_pool.json, sensory_patterns.json, connectors.json, style_gates.json?}
# Gera: assets/corpus_analysis.json, assets/rebuild_report.json

import os, json, re
from collections import Counter, defaultdict

ASSETS = os.path.join(os.getcwd(), "assets")
paths = {
    "second_person": os.path.join(ASSETS, "second_person.json"),
    "sensory_pool": os.path.join(ASSETS, "sensory_pool.json"),
    "sensory_patterns": os.path.join(ASSETS, "sensory_patterns.json"),
    "connectors": os.path.join(ASSETS, "connectors.json"),
    "style_gates": os.path.join(ASSETS, "style_gates.json"),
}
def load(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f: 
            return json.load(f)
    except Exception:
        return default

sp = load(paths["second_person"], [])
sens_pool = load(paths["sensory_pool"], [])
sens_patterns = load(paths["sensory_patterns"], [])
connectors = load(paths["connectors"], [])
gates = load(paths["style_gates"], {
    "min_words": 120, "min_sentences": 5, "min_paragraphs": 2,
    "cadence_target": [18,22], "cadence_tolerated": [16,24],
    "penalties": ["CadenceOutOfBand","CadenceMassTooLow"],
    "metrics": ["StyleScore","HumanizationIndex","Heat","Punch","Transitions"]
})

def get_sources(items):
    src = []
    for it in items:
        if isinstance(it, dict):
            s = it.get("source")
            if s: src.append(s.split("#")[0])
    return src

# Estatísticas básicas
sp_sources = get_sources(sp)
sens_sources = get_sources(sens_pool)
unique_sources = sorted(set(sp_sources + sens_sources))

def wc(s): 
    return len(s.split())

# Distribuições simples
wc_sp = [wc(it["text"]) for it in sp if isinstance(it, dict) and it.get("text")]
wc_sens = [wc(it["text"]) for it in sens_pool if isinstance(it, dict) and it.get("text")]

def pct(n, d): 
    return round(100.0 * n / d, 2) if d else 0.0

# Amostras determinísticas (primeiros 5)
examples = {
    "second_person": [it["text"] for it in sp[:5] if isinstance(it, dict) and it.get("text")],
    "sensory": [it["text"] for it in sens_pool[:5] if isinstance(it, dict) and it.get("text")],
    "connectors": [c["text"] for c in connectors[:5] if isinstance(c, dict) and c.get("text")]
}

# Monta corpus_analysis.json
corpus_analysis = {
    "assets_dir": ASSETS,
    "files_scanned_estimate": len(unique_sources),
    "samples": {
        "second_person": len(sp),
        "sensory_pool": len(sens_pool),
        "sensory_patterns": len(sens_patterns),
        "connector_types": len(connectors)
    },
    "word_count_distribution": {
        "second_person": {"min": min(wc_sp) if wc_sp else 0, "max": max(wc_sp) if wc_sp else 0, "avg": round(sum(wc_sp)/len(wc_sp),2) if wc_sp else 0},
        "sensory_pool": {"min": min(wc_sens) if wc_sens else 0, "max": max(wc_sens) if wc_sens else 0, "avg": round(sum(wc_sens)/len(wc_sens),2) if wc_sens else 0}
    },
    "examples": examples
}

with open(os.path.join(ASSETS, "corpus_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(corpus_analysis, f, ensure_ascii=False, indent=2)

# Monta rebuild_report.json
notes = [
    "Fonte: assets existentes (não reprocessou transcrições).",
    "second_person: exige 'você|vc' + verbo próximo (≤18 chars).",
    "sensory_pool: léxico sensorial explícito (cheiro/luz/som/textura/temperatura/cor).",
    "Faixa de palavras recomendada: 10–34; pontuação final obrigatória.",
    "connectors: início de frase + vírgula; filtrados previamente por whitelist/frequência."
]
rebuild_report = {
    "style_gates": gates,
    "stats": {
        "unique_sources_estimate": len(unique_sources),
        "second_person": len(sp),
        "sensory_pool": len(sens_pool),
        "sensory_patterns": len(sens_patterns),
        "connectors_kept": len(connectors)
    },
    "notes": notes,
    "paths": {
        "second_person": paths["second_person"],
        "sensory_pool": paths["sensory_pool"],
        "sensory_patterns": paths["sensory_patterns"],
        "connectors": paths["connectors"],
        "corpus_analysis": os.path.join(ASSETS, "corpus_analysis.json")
    }
}
with open(os.path.join(ASSETS, "rebuild_report.json"), "w", encoding="utf-8") as f:
    json.dump(rebuild_report, f, ensure_ascii=False, indent=2)

print({
    "ok": True,
    "corpus_analysis": os.path.join(ASSETS, "corpus_analysis.json"),
    "rebuild_report": os.path.join(ASSETS, "rebuild_report.json"),
    "samples": corpus_analysis["samples"]
})
