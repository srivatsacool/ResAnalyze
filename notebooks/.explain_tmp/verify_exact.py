# -*- coding: utf-8 -*-
"""Execute the EXACT code cells from block_g notebooks (in order, with ch40 preamble)
and report real outputs, so markdown claims match actual notebook behavior byte-for-byte."""
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g"

def load_nb(rel):
    with open(BASE + "\\" + rel, encoding="utf-8-sig") as f:
        return json.load(f)

# --- ch40 state ---
nb40 = load_nb("40_jd_parsing/40.ipynb")
src40 = {i: "".join(c["source"]) for i, c in enumerate(nb40["cells"]) if c["cell_type"] == "code"}
print("### CH40 cell2 repr (first 80 chars):", repr(src40[2][:80]))
print("### CH40 cell4 has split('\\\\n'):", repr(src40[4][src40[4].find('split'):src40[4].find('split')+20]))

ns = {}
exec(compile(src40[2], "<ch40c2>", "exec"), ns)
exec(compile(src40[4], "<ch40c4>", "exec"), ns)
print("\n--- CH40 OUTPUT (cell4) ---")
print(ns["detect_jd_sections"](ns["jd"]))

# --- ch41 ---
nb41 = load_nb("41_jd_skill_extraction/41.ipynb")
src41 = {i: "".join(c["source"]) for i, c in enumerate(nb41["cells"]) if c["cell_type"] == "code"}
print("\n### CH41 cell2 snippet:", repr(src41[2][:220]))
print("### CH41 cell4 regex line:", repr([l for l in src41[4].split("\n") if "findall" in l][0]))
ns41 = dict(ns)
exec(compile(src41[2], "<ch41c2>", "exec"), ns41)
print("\n--- CH41 OUTPUT (cell2) ---")
print("required:", ns41["req"])
print("preferred:", ns41["pref"])
ns41b = dict(ns)
exec(compile(src41[4], "<ch41c4>", "exec"), ns41b)
print("\n--- CH41 OUTPUT (cell4) ---")
print(ns41b["skill_frequency"](ns["jd"], ns41b["SKILLS_DB"]))

# --- ch43 ---
nb43 = load_nb("43_qualification_detection/43.ipynb")
src43 = {i: "".join(c["source"]) for i, c in enumerate(nb43["cells"]) if c["cell_type"] == "code"}
print("\n### CH43 cell2 regex line:", repr([l for l in src43[2].split("\n") if "re.search" in l][0]))
print("### CH43 cell4 patterns:", repr([l for l in src43[4].split("\n") if "r(" in l or "r\"" in l]))
ns43 = dict(ns)
exec(compile(src43[2], "<ch43c2>", "exec"), ns43)
print("\n--- CH43 OUTPUT (cell2) ---")
print("degrees:", ns43["extract_degree_requirements"](ns["jd"]))
ns43b = dict(ns)
exec(compile(src43[4], "<ch43c4>", "exec"), ns43b)
print("\n--- CH43 OUTPUT (cell4) ---")
print("years:", ns43b["extract_years_required"](ns["jd"]))

print("\nDONE")
