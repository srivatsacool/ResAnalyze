# -*- coding: utf-8 -*-
"""Snapshot code cells (index, id, source) of the 8 block_f notebooks for later byte-identical verification."""
import json, os

base = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f"
snap_dir = r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\code_snap"
os.makedirs(snap_dir, exist_ok=True)

notebooks = {
    "32_section_detection": "32.ipynb",
    "33_skill_extraction_(rules)": "33.ipynb",
    "34_skill_normalization_engine": "34.ipynb",
    "35_education_parsing": "35.ipynb",
    "36_experience_parsing": "36.ipynb",
    "37_bullet_parsing_and_star_scoring": "37.ipynb",
    "38_project_extraction": "38.ipynb",
    "39_resume_json_schema": "39.ipynb",
}

for tag, fname in notebooks.items():
    path = os.path.join(base, tag, fname)
    nb = json.load(open(path, encoding="utf-8-sig"))
    snap = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code":
            snap.append({"index": i, "id": c.get("id"), "source": "".join(c.get("source", []))})
    with open(os.path.join(snap_dir, tag + ".json"), "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1)
    print(tag, "->", len(snap), "code cells snapshotted")
