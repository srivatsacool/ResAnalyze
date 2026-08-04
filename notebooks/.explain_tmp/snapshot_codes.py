"""Snapshot all code-cell sources + md headings of the 5 block_d notebooks to JSON."""
import json
import sys
sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import load

NBS = [
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\21_glove\21.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\22_sentence_transformers\22.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\23_embedding_benchmarks\23.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\24_zero-shot_classification\24.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\25_error_handling_in_nlp\25.ipynb",
]
out = {}
for p in NBS:
    nb = load(p)
    codes = [{"".join(c["source"]), c.get("id")} for c in nb["cells"] if c["cell_type"] == "code"]
    # store as list of (source, id) pairs, sources as strings
    codes = [("".join(c["source"]), c.get("id")) for c in nb["cells"] if c["cell_type"] == "code"]
    headings = [("".join(c["source"]).split("\n")[0], c.get("id")) for c in nb["cells"] if c["cell_type"] == "markdown"]
    out[p] = {"codes": codes, "md_heads": headings}
with open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\before_snapshot.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("snapshot written:", len(out), "notebooks")
