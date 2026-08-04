# verify_block_a.py — post-edit verification against snapshot.
import json
from nbtools import load

PATHS = [
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\00_environment_setup\00.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\01_python_engineering_refresher\01.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\02_pandas_&_numpy\02.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\03_regex_mastery\03.ipynb",
]

snapshot = json.load(open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\snapshot.json", encoding="utf-8"))

ok_all = True
for p in PATHS:
    nb = load(p)  # json.load proves JSON validity (BOM-tolerant)
    code_srcs = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    md_srcs = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"]
    before = snapshot[p]

    # (b) code cells byte-identical
    code_ok = code_srcs == before["code"]
    # (c) every original markdown line still present (headings intact)
    headings_ok = True
    for old in before["md"]:
        first = old.split("\n")[0].strip()
        if first and first.startswith("#"):
            if not any(first in m for m in md_srcs):
                headings_ok = False
                print(f"  MISSING HEADING in {p}: {first!r}")
    # (a) every md cell >= 300 chars
    short = [(i, len(m)) for i, m in enumerate(md_srcs) if len(m) < 300]
    total_md = sum(len(m) for m in md_srcs)
    ok = code_ok and headings_ok and not short
    ok_all = ok_all and ok
    print(f"{'OK ' if ok else 'FAIL'} {p}")
    print(f"     md cells: {len(md_srcs)}  total md chars: {total_md}  min md cell: {min(len(m) for m in md_srcs)}")
    print(f"     code cells identical: {code_ok}  headings intact: {headings_ok}  short cells: {short}")
    print(f"     code cell count: {len(code_srcs)} (unchanged vs snapshot: {len(before['code'])})")

print("ALL OK" if ok_all else "FAILURES PRESENT")
