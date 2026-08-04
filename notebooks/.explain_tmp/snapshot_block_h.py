"""Snapshot code-cell sources of the 4 block_h notebooks to JSON for later diff verification."""
import json, sys
sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import load

paths = [
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\46_resume_vs_jd_matching\46.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\47_faiss_vector_search\47.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\48_chromadb\48.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\49_embedding_evaluation_and_benchmark\49.ipynb",
]
snap = {}
for p in paths:
    nb = load(p)
    key = p.split("block_h")[1].replace("\\", "/")
    snap[key] = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code":
            snap[key].append({
                "idx": i,
                "id": c.get("id"),
                "source": "".join(c.get("source", [])),
                "execution_count": c.get("execution_count"),
                "outputs": c.get("outputs"),
            })
with open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\code_before.json", "w", encoding="utf-8") as f:
    json.dump(snap, f, ensure_ascii=False, indent=1)
print("snapshot saved:", {k: len(v) for k, v in snap.items()})
