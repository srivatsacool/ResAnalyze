"""Verify block_h notebooks after markdown expansion:
(a) every md cell >= 300 chars, (b) code cells byte-identical to pre-apply snapshot,
(c) headings intact (first line of each md cell unchanged), (d) JSON valid.
"""
import json, sys
sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import load

paths = [
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\46_resume_vs_jd_matching\46.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\47_faiss_vector_search\47.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\48_chromadb\48.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\49_embedding_evaluation_and_benchmark\49.ipynb",
]

# pre-apply code snapshot (built from "".join(source))
before = json.load(open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\code_before.json", encoding="utf-8"))

# expected original heading-first-lines (from the first dumps)
expected_heads = {
    "/46_resume_vs_jd_matching/46.ipynb": [
        "# 46 — Resume vs JD Matching", "![Resume vs JD Matching Pipeline]", "## 1. Multi-Signal Matching Strategy",
        "## 2. Building the Matcher", "## 3. Testing on Multiple JDs", "## Summary: Multi-signal matching with weighted scoring. Transparent, debuggable, no black box.",
        "## Key Insight",
    ],
    "/47_faiss_vector_search/47.ipynb": [
        "# 47 — FAISS Vector Search", "## 1. FAISS Basics", "## 2. Building a FAISS Index",
        "## 3. Querying with a JD", "## 4. Index Persistence",
        "## Summary: FAISS enables fast resume retrieval from large candidate pools. IVF scales to millions.",
        "## Key Insight",
    ],
    "/48_chromadb/48.ipynb": [
        "# 48 — ChromaDB", "## 1. Setting Up ChromaDB", "## 2. Adding Resumes with Metadata",
        "## 3. Querying with Metadata Filtering", "## 4. Updating and Deleting",
        "## Summary: ChromaDB adds metadata filtering on top of vector search. Good for production MVPs.",
        "## Key Insight",
    ],
    "/49_embedding_evaluation_and_benchmark/49.ipynb": [
        "# 49 — Embedding Evaluation & Benchmark", "## 1. Defining the Benchmark", "## 2. Evaluating Models",
        "## 3. Results Visualization",
        "## Summary: Systematic benchmarks prevent regression. Track RMSE across model versions.",
        "## Key Insight",
    ],
}

ok = True
for p in paths:
    key = p.split("block_h")[1].replace("\\", "/")
    nb = load(p)  # raises on invalid JSON
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    total_md = sum(len("".join(c["source"])) for c in md_cells)

    # (b) code cells byte-identical
    for c in code_cells:
        src = "".join(c["source"])
        match = next((b for b in before[key] if b["idx"] == nb["cells"].index(c) or b["id"] == c.get("id")), None)
    # simpler: index-based comparison
    b_list = sorted(before[key], key=lambda b: b["idx"])
    code_idx = [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]
    code_ok = True
    for bi, ci in zip(b_list, code_idx):
        c = nb["cells"][ci]
        if "".join(c["source"]) != bi["source"] or c.get("execution_count") != bi["execution_count"] or c.get("outputs") != bi["outputs"]:
            code_ok = False
            print(f"  !! CODE DIFF at idx {ci} in {key}")

    # (a) md min length + (c) headings
    md_min = min(len("".join(c["source"])) for c in md_cells)
    heads = [("".join(c["source"]).splitlines()[0]) for c in md_cells]
    # compare first-line prefix up to heading marker where applicable
    heads_ok = all(h.startswith(e) for h, e in zip(heads, expected_heads[key]))
    if not heads_ok:
        print(f"  !! HEADING MISMATCH in {key}")
        for h, e in zip(heads, expected_heads[key]):
            if not h.startswith(e):
                print(f"     got: {h!r}\n     exp: {e!r}")

    print(f"{key}: md={len(md_cells)} cells, total_md_chars={total_md}, md_min={md_min}, code_cells={len(code_cells)}, code_identical={code_ok}, headings_ok={heads_ok}")
    ok = ok and md_min >= 300 and code_ok and heads_ok

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
