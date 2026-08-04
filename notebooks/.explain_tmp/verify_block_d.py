"""Verify block_d notebooks after markdown expansion."""
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
with open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\before_snapshot.json", encoding="utf-8") as f:
    before = json.load(f)

MIN_CHARS = 300
all_ok = True
for p in NBS:
    # 1. JSON validity
    with open(p, encoding="utf-8") as f:
        json.load(f)
    nb = load(p)
    name = p.split("block_d\\")[-1]
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    total_md = sum(len("".join(c["source"])) for c in md_cells)

    # 2. code sources byte-identical (compare joined source strings)
    code_now = [["".join(c["source"]), c.get("id")] for c in code_cells]
    code_before = before[p]["codes"]
    code_ok = code_now == code_before
    if not code_ok:
        for i, (a, b) in enumerate(zip(code_now, code_before)):
            if a != b:
                print(f"    code cell {i} differs: before len={len(b[0])} now len={len(a[0])}")

    # 3. headings intact: compare first source line per md cell vs before
    heads_now = [["".join(c["source"]).split("\n")[0], c.get("id")] for c in md_cells]
    heads_before = before[p]["md_heads"]
    # allow the final cell heading conversion Summary->Key Insight (same wording after colon)
    def norm(h):
        h0 = h[0]
        if h0.startswith("## Key Insight:"):
            return ["## Summary:" + h0[len("## Key Insight:"):], h[1]]
        return h
    heads_ok = [norm(h) for h in heads_now] == heads_before
    if not heads_ok:
        print("    heading mismatch:")
        for i, (a, b) in enumerate(zip(heads_now, heads_before)):
            if a != b:
                print(f"      md cell {i}: before={b[0]!r} now={a[0]!r}")

    # 4. every md cell >= MIN_CHARS
    short = [(i, len("".join(c["source"]))) for i, c in enumerate(md_cells) if len("".join(c["source"])) < MIN_CHARS]

    ok = code_ok and heads_ok and not short
    all_ok = all_ok and ok
    print(f"{name}: md_cells={len(md_cells)} total_md_chars={total_md} code_ok={code_ok} headings_ok={heads_ok} short_cells={short} -> {'PASS' if ok else 'FAIL'}")

print("\nALL PASS" if all_ok else "\nSOME FAILURES")
