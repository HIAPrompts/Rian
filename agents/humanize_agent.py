# -*- coding: utf-8 -*-
"""
Humanize Agent — modo estrito (sem criação textual)
Usa apenas assets/: second_person.json, sensory_pool.json, sensory_patterns.json, connectors.json,
style_gates.json (opcional), tone_profiles.json (opcional), corpus_analysis.json (opcional).

CLI:
  python agents/humanize_agent.py --input draft.txt --mode compose --seed 7 --max-connectors 1 --output outputs/result.json
"""
import os, re, json, argparse, random
from typing import List, Dict

def load_asset(assets_dir: str, name: str, default):
    path = os.path.join(assets_dir, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def norm_connectors(raw) -> List[str]:
    pool = []
    for it in raw or []:
        if isinstance(it, dict):
            t = (it.get("text") or "").strip()
        else:
            t = str(it).strip()
        if not t or t.startswith("#") or t.startswith("["):
            continue
        if t not in pool:
            pool.append(t)
    return pool

def as_text_pool(raw, key="text") -> List[str]:
    out = []
    if not raw:
        return out
    if isinstance(raw[0], dict):
        for it in raw:
            t = (it.get(key) or "").strip()
            if t and t not in out:
                out.append(t)
    else:
        for it in raw:
            t = str(it).strip()
            if t and t not in out:
                out.append(t)
    return out

def as_items_with_source(raw, key="text") -> List[Dict[str,str]]:
    out = []
    for it in raw or []:
        if isinstance(it, dict):
            t = (it.get(key) or "").strip()
            s = (it.get("source") or "").strip()
            if t and {"text": t, "source": s} not in out:
                out.append({"text": t, "source": s})
    return out

def score_text(text: str, gates: Dict) -> Dict:
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = text.split()
    paragraphs = [p for p in text.split("\n") if p.strip()]
    avg = round((len(words) / max(1, len(sentences))) if sentences else 0.0, 2)
    lo, hi = gates.get("cadence_target", [18,22])
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "avg_sentence_len": avg,
        "passes_hard_gate": (
            len(words)   >= gates.get("min_words",120) and
            len(sentences)   >= gates.get("min_sentences",5) and
            len(paragraphs)  >= gates.get("min_paragraphs",2)
        ),
        "passes_cadence_gate": (lo <= avg <= hi) if sentences else False
    }

def deterministic_choice(pool: List, key, seed=0):
    if not pool:
        return None
    rnd = random.Random((hash(key) ^ seed) & 0xFFFFFFFF)
    return pool[rnd.randrange(0, len(pool))]

def build_plan(paragraphs: List[str], connectors: List[str], sensory_items: List[Dict], second_items: List[Dict], max_conn=1, seed=0):
    plan = []
    for i, p in enumerate(paragraphs):
        step = {"paragraph_index": i+1, "original": p, "inject": []}
        # conector (máx 1)
        if max_conn > 0 and connectors:
            conn = deterministic_choice(connectors, ("conn", i), seed)
            if conn:
                step["inject"].append({"type":"connector", "text": f"{conn},"})
        # sensorial (com fonte)
        if sensory_items:
            sens = deterministic_choice(sensory_items, ("sens", i), seed)
            if sens:
                step["inject"].append({"type":"sensory", "text": sens["text"], "source": sens.get("source","")})
        # 2ª pessoa (com fonte)
        if second_items:
            sp = deterministic_choice(second_items, ("second", i), seed)
            if sp:
                step["inject"].append({"type":"second_person", "text": sp["text"], "source": sp.get("source","")})
        plan.append(step)
    return plan

def apply_plan(plan: List[Dict]) -> (str, List[Dict]):
    rewritten = []
    citations = []
    for step in plan:
        parts = []
        for inj in step["inject"]:
            parts.append(inj["text"])
            if inj["type"] in ("sensory","second_person"):
                citations.append({"type": inj["type"], "quote": inj["text"], "source": inj.get("source","")})
        parts.append(step["original"])
        rewritten.append(" ".join(parts))
    return "\n\n".join(rewritten), citations

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets-dir", default=os.path.join(os.getcwd(), "assets"))
    ap.add_argument("--input", required=True, help="caminho de rascunho .txt")
    ap.add_argument("--output", default=None, help="JSON de saída (report + final_text se compose)")
    ap.add_argument("--mode", choices=["dry-run","compose"], default="compose")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-connectors", type=int, default=1)
    args = ap.parse_args()

    # Carrega assets
    gates = load_asset(args.assets_dir, "style_gates.json", {
        "min_words":120, "min_sentences":5, "min_paragraphs":2,
        "cadence_target":[18,22]
    })
    connectors_raw = load_asset(args.assets_dir, "connectors.json", [])
    sensory_raw    = load_asset(args.assets_dir, "sensory_pool.json", [])
    second_raw     = load_asset(args.assets_dir, "second_person.json", [])
    tone_profiles  = load_asset(args.assets_dir, "tone_profiles.json", {}) if os.path.exists(os.path.join(args.assets_dir,"tone_profiles.json")) else {}

    connectors = norm_connectors(connectors_raw)
    sensory_items = as_items_with_source(sensory_raw)
    second_items  = as_items_with_source(second_raw)

    # Lê rascunho
    with open(args.input, "r", encoding="utf-8") as f:
        draft = f.read().strip()
    paragraphs = [p.strip() for p in draft.split("\n") if p.strip()]

    # Plano determinístico
    plan = build_plan(paragraphs, connectors, sensory_items, second_items, max_conn=args.max_connectors, seed=args.seed)

    # Scoring pré
    pre = score_text(draft, gates)

    result = {
        "meta": {"mode": args.mode, "seed": args.seed, "assets_dir": args.assets_dir},
        "assets_stats": {
            "connectors": len(connectors),
            "sensory_pool": len(sensory_items),
            "second_person": len(second_items)
        },
        "style_gates": gates,
        "tone_metadata": tone_profiles.get("metadata", {}) if isinstance(tone_profiles, dict) else {},
        "pre_score": pre,
        "plan": plan
    }

    if args.mode == "compose":
        final_text, citations = apply_plan(plan)
        post = score_text(final_text, gates)
        result.update({"final_text": final_text, "post_score": post, "citations": citations})

    out_path = args.output or os.path.join(os.getcwd(), "outputs", f"humanize_{args.mode}_{args.seed}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({"ok": True, "output": out_path, "pre": result["pre_score"], "post": result.get("post_score")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
