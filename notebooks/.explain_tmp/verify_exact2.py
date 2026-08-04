# -*- coding: utf-8 -*-
"""Execute the EXACT code cells from block_g notebooks 40-45 in notebook order (ch40 first,
as a shared kernel would), capturing real outputs. Reports failures honestly."""
import json, io, sys, traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g"
def src(rel, idx):
    nb = json.load(open(BASE + "\\" + rel, encoding="utf-8-sig"))
    return "".join(c["source"]) if False else "".join([c["source"] for c in nb["cells"]][idx])

def run_cell(rel, idx, ns, label):
    code = src(rel, idx)
    print(f"--- {label} (cell {idx}) ---")
    try:
        exec(compile(code, f"<{rel}#{idx}>", "exec"), ns)
        print("[OK]")
    except Exception as e:
        print(f"[EXC] {type(e).__name__}: {e}")
    return ns

ns = {}
# CH40
run_cell("40_jd_parsing/40.ipynb", 2, ns, "40.2 define jd")
run_cell("40_jd_parsing/40.ipynb", 4, ns, "40.4 detect_jd_sections")
# CH41
run_cell("41_jd_skill_extraction/41.ipynb", 2, ns, "41.2 extract_jd_skills")
run_cell("41_jd_skill_extraction/41.ipynb", 4, ns, "41.4 skill_frequency")
# CH43
run_cell("43_qualification_detection/43.ipynb", 2, ns, "43.2 degrees")
run_cell("43_qualification_detection/43.ipynb", 4, ns, "43.4 years")
# CH42 (spacy)
run_cell("42_responsibility_detection/42.ipynb", 2, ns, "42.2 action verbs")
run_cell("42_responsibility_detection/42.ipynb", 4, ns, "42.4 seniority")
# CH44
run_cell("44_keyword_ranking/44.ipynb", 2, ns, "44.2 tfidf")
run_cell("44_keyword_ranking/44.ipynb", 4, ns, "44.4 embeddings")
# CH45
run_cell("45_requirement_classification/45.ipynb", 2, ns, "45.2 zero-shot")
run_cell("45_requirement_classification/45.ipynb", 4, ns, "45.4 rule-based")
print("\nEXACT-CHAIN DONE")
