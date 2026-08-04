import json, sys, hashlib

NBS = [
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\26_pdf_parsing\26.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\27_docx_parsing\27.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\28_ocr_basics\28.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\29_text_normalization_for_resumes\29.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\30_language_detection\30.ipynb",
    r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\31_parsing_error_handling\31.ipynb",
]

ok = True
for p in NBS:
    name = p.split("\\")[-2]
    try:
        nb = json.load(open(p, encoding="utf-8-sig"))
        valid = "JSON-OK"
    except Exception as e:
        valid = f"JSON-FAIL: {e}"
        ok = False
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    md_tot = 0
    short = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "markdown":
            continue
        s = "".join(c.get("source", []))
        md_tot += len(s)
        if len(s) < 300:
            short.append((i, len(s)))
    print(f"== {name} | {valid} | md cells: {len(md_cells)} | code cells: {len(code_cells)} | total md chars: {md_tot}")
    if short:
        ok = False
        print(f"   !! SHORT MD CELLS (<300): {short}")
    # heading integrity: first line of each md cell should start with # or ## or be image/caption cells (0/1)
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "markdown":
            continue
        first = "".join(c.get("source", [])).split("\n")[0]
        if i == 1:
            continue  # image/caption cell
        if not (first.startswith("# ") or first.startswith("## ")):
            ok = False
            print(f"   !! cell {i} does not start with a heading: {first[:60]!r}")
    # code cell sha + source (for byte-identity check)
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code":
            src = "".join(c.get("source", []))
            print(f"   CODE[{i}] sha={hashlib.sha256(src.encode('utf-8')).hexdigest()[:12]} len={len(src)}")

print("\nALL CHECKS PASSED" if ok else "\nPROBLEMS FOUND")
