"""Run block_i code cells in dependency order to capture real outputs."""
import sys, io, json
sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import load

BI = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_i"
import matplotlib
matplotlib.use("Agg")

def code_sources(path):
    nb = load(path)
    return ["".join(c.get("source", [])) for c in nb["cells"] if c["cell_type"] == "code"]

order = [
    (f"{BI}\\50_ats_rule_design\\50.ipynb", "CH50"),
    (f"{BI}\\51_explainable_scoring\\51.ipynb", "CH51"),
    (f"{BI}\\52_ats_simulation_mode\\52.ipynb", "CH52"),
    (f"{BI}\\53_skill_gap_analysis\\53.ipynb", "CH53"),
    (f"{BI}\\54_resume_ranking\\54.ipynb", "CH54"),
]

namespace = {}
for path, label in order:
    print("=" * 70)
    print(f"### {label} — {path.split(chr(92))[-2]}")
    print("=" * 70)
    for i, src in enumerate(code_sources(path)):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            exec(compile(src, f"<{label} cell {i}>", "exec"), namespace)
            ok = True
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"
        finally:
            sys.stdout = old
        out = buf.getvalue()
        print(f"--- cell {i} {'OK' if ok else 'FAIL ' + err}")
        if out:
            print(out.rstrip()[:3000])
