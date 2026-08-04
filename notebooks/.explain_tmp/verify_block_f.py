# -*- coding: utf-8 -*-
"""Verify block_f notebooks: JSON valid, code cells byte-identical to snapshot,
md cells >=300 chars, headings intact."""
import json, glob, os

snap_dir = r"D:/Projects/ResAnalyze/notebooks/.explain_tmp/code_snap"
base = r"D:/Projects/ResAnalyze/notebooks/part2_intelligence/block_f"
tags = ["32_section_detection", "33_skill_extraction_(rules)", "34_skill_normalization_engine",
        "35_education_parsing", "36_experience_parsing", "37_bullet_parsing_and_star_scoring",
        "38_project_extraction", "39_resume_json_schema"]

HEADINGS = {
    "32": ["# 32 — Resume Section Detection", "## 1. Common Resume Sections",
           "## 2. Regex-Based Section Detection", "## 3. ML-Based Section Classification",
           "## 4. Section Content Extraction",
           "## Summary: Regex + heuristics for basic detection. Zero-shot ML for complex layouts."],
    "33": ["# 33 — Skill Extraction (Rules)", "## 1. Building a Skills Database",
           "## 2. Regex Skill Matching", "## 3. Fuzzy Matching for Typos",
           "## Summary: Start with exact regex matching, layer fuzzy matching for typos."],
    "34": ["# 34 — Skill Normalization Engine", "## 1. Three-Tier Normalization",
           "## 2. Building the Normalizer", "## 3. Embedding-Based Normalization (Tier 3)",
           "## Summary: Three-tier normalization catches exact matches, typos, and semantic variants."],
    "35": ["# 35 — Education Parsing", "## 1. Education Patterns", "## 2. Education Extractor",
           "## 3. Institution Normalization",
           "## Summary: Regex extracts structured education data. Institution aliases normalize names."],
    "36": ["# 36 — Experience Parsing", "## 1. Experience Pattern Recognition", "## 2. Experience Parser",
           "## 3. Duration Calculation",
           "## Summary: Pattern matching extracts structured experience. Duration calc estimates tenure."],
    "37": ["# 37 — Bullet Parsing & STAR Scoring", "## 1. STAR Method Explained", "## 2. Bullet Scorer",
           "## 3. STAR Compliance Check",
           "## Summary: Bullet scoring identifies weak bullets for improvement. Rule-based, no LLM needed."],
    "38": ["# 38 — Project Extraction", "## 1. Project Pattern Recognition", "## 2. Project Parser",
           "## Summary: Project extraction follows similar pattern to experience but without dates."],
    "39": ["# 39 — Resume JSON Schema — Live Build", "## 1. The Canonical Schema",
           "## 2. Building the Pipeline End-to-End",
           "## Summary: ResumeSchema provides a unified contract. Every engine reads/writes this format."],
}

all_ok = True
for tag in tags:
    num = tag[:2]
    fname = num + ".ipynb"
    p = os.path.join(base, tag, fname)
    nb = json.load(open(p, encoding="utf-8-sig"))  # JSON validity
    snap = json.load(open(os.path.join(snap_dir, tag + ".json"), encoding="utf-8"))
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    total_md = sum(len("".join(c.get("source", []))) for c in md_cells)

    # 1) code cells byte-identical
    ok_code = True
    for s in snap:
        c = nb["cells"][s["index"]]
        cur = "".join(c.get("source", []))
        if c.get("id") != s["id"] or cur != s["source"] or c.get("execution_count") is not None:
            ok_code = False
            print(f"  MISMATCH {tag} cell {s['index']}: id {c.get('id')} vs {s['id']}")
    # 2) md cells >= 300 chars
    short = [(i, len("".join(c.get("source", [])))) for i, c in enumerate(md_cells)
             if len("".join(c.get("source", []))) < 300]
    # 3) headings intact
    md_all = "\n".join("".join(c.get("source", [])) for c in md_cells)
    missing_h = [h for h in HEADINGS[num] if h not in md_all]
    ok = ok_code and not short and not missing_h
    all_ok = all_ok and ok
    print(f"{num} | md cells: {len(md_cells):2d} | total md chars: {total_md:5d} | code cells: {len(code_cells)} "
          f"| code identical: {'YES' if ok_code else 'NO'} | md>=300: {'YES' if not short else short} "
          f"| headings ok: {'YES' if not missing_h else missing_h}")

print("ALL OK" if all_ok else "FAILURES PRESENT")
