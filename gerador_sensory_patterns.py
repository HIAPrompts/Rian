# -*- coding: utf-8 -*-
# GERADOR — sensory_patterns.json
# deduplica sensory_pool.json e mantém apenas o campo "text"

import os, json

ASSETS_DIR = os.path.join(os.getcwd(), "assets")
pool_path = os.path.join(ASSETS_DIR, "sensory_pool.json")
out_path  = os.path.join(ASSETS_DIR, "sensory_patterns.json")

if not os.path.exists(pool_path):
    raise SystemExit(f"❌ Arquivo não encontrado: {pool_path}")

with open(pool_path, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
seen = set()
for item in data:
    txt = item.get("text", "").strip()
    if not txt or txt in seen:
        continue
    seen.add(txt)
    texts.append(txt)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False, indent=2)

print({
    "ok": True,
    "input": pool_path,
    "output": out_path,
    "original": len(data),
    "deduplicated": len(texts)
})
