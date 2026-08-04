# -*- coding: utf-8 -*-
"""Execute each block_f notebook's code cells in order, capturing stdout per cell.
Only for gathering REAL outputs to cite in markdown; never writes to notebooks."""
import json, os, sys, io, contextlib

base = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f"
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

report = {}
for tag, fname in notebooks.items():
    nb = json.load(open(os.path.join(base, tag, fname), encoding="utf-8-sig"))
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    # exec in a shared namespace so cross-cell deps (e.g. ACTION_VERBS) work
    ns = {"__name__": "__main__"}
    print("=" * 20, tag, "=" * 20)
    for i, c in enumerate(code_cells):
        src = "".join(c.get("source", []))
        buf = io.StringIO()
        ok = True
        err = ""
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, f"<{tag}_cell{i}>", "exec"), ns)
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"
        out = buf.getvalue()
        print(f"--- CELL {i} ({'OK' if ok else 'FAIL'}) ---")
        print(out if out else "(no stdout)")
        if err:
            print("ERR:", err)
    print()
