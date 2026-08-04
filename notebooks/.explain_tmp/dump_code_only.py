import json

NBS = [
    ("26", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\26_pdf_parsing\26.ipynb"),
    ("27", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\27_docx_parsing\27.ipynb"),
    ("28", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\28_ocr_basics\28.ipynb"),
    ("29", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\29_text_normalization_for_resumes\29.ipynb"),
    ("30", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\30_language_detection\30.ipynb"),
    ("31", r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\31_parsing_error_handling\31.ipynb"),
]
for tag, p in NBS:
    nb = json.load(open(p, encoding="utf-8-sig"))
    print(f"\n########## {tag} code cells ##########")
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code":
            print(f"--- ch{tag} CODE cell [{i}] id={c.get('id')}")
            print("".join(c["source"]), end="")
            print("--- end ---")
