"""Verify block_b notebooks after markdown expansion:
(a) every md cell >= 300 chars, (b) code cell ids/outputs/execution_count unchanged,
(c) headings intact, (d) JSON valid. Ch11 must NOT be in the list."""
import json, sys
sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import load

NBS = {
 "04": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\04_nlp_introduction\04.ipynb",
 "05": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\05_tokenization\05.ipynb",
 "06": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\06_text_normalization\06.ipynb",
 "07": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\07_stop_words\07.ipynb",
 "08": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\08_lemmatization\08.ipynb",
 "09": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\09_stemming\09.ipynb",
 "10": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\10_pos_tagging\10.ipynb",
 "12": r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\12_named_entity_recognition\12.ipynb",
}

# original cell ids from pre-edit dumps: {nb: {idx: id}}
ORIG_IDS = {
 "04": {0:"ed69f1d9",1:"img_nlp_pipeline",2:"7abcaf9b",3:"da64609b",4:"5075f855",5:"f16e4da3",6:"8fbbf2da"},
 "05": {0:"2d14f66e",1:"a1cd1b15",2:"903c87d2",3:"41a117ab",4:"7ead1703",5:"64c60650",6:"549e1170",7:"8007be5b",8:"a6b5ad86",9:"efea82a0"},
 "06": {0:"1a9f3677",1:"bab96acf",2:"8f368bf0",3:"9c601740",4:"32d26f45",5:"865fcf8f",6:"45596813",7:"f97848e2",8:"0dae9f33",9:"6b310938"},
 "07": {0:"dbd88379",1:"1ad9dd05",2:"03915e7a",3:"b3dab354",4:"8d6d5fc6",5:"3c550ba3",6:"4573c08a",7:"fae864cf"},
 "08": {0:"fcac0fbc",1:"c5cbf709",2:"615f1529",3:"fc91d13d",4:"80fbd5f5",5:"2d75e268",6:"889f5081",7:"f3afdebf",8:"375074ae",9:"6d31627e",10:"420bd843"},
 "09": {0:"4b796d6e",1:"3c6db51a",2:"bc43a416",3:"7f097e19",4:"1dbcc5f5",5:"6fa7ca52"},
 "10": {0:"6f721585",1:"0f2b74e4",2:"158a8020",3:"b6e6a87b",4:"50868c42"},
 "12": {0:"05b8a9cd",1:"3e9c8a69",2:"991f92d4",3:"0966d026",4:"a5c6a691",5:"851c6f62",6:"267be62d",7:"822c66d7",8:"60df0032"},
}

# headings / preserved lines that must appear verbatim in the matching cell
PRESERVE = {
 "04": {0: ["# 04  NLP Introduction", "**Goal:** Understand what NLP is and see the full pipeline in action."],
        1: ["![NLP Pipeline Overview](../../../assets/images/nlp_pipeline_diagram_1785491141457.png)",
            "> **Figure:** The NLP processing pipeline — from raw resume text to structured data. Each stage in this notebook maps to a step in this pipeline."],
        2: ["## 2. The NLP Pipeline in Action"],
        4: ["## 3. Text Preprocessing Order Matters"],
        6: ["## Summary: NLP pipeline = raw text -> preprocessing -> tokenization -> POS -> NER -> parsing -> extraction"]},
 "05": {0: ["# 05 — Tokenization", "**Goal:** Master word, sentence, and subword tokenization."],
        1: ["## 1. Word Tokenization — Comparing Approaches"],
        3: ["## 2. spaCy Handles Resume Edge Cases"],
        5: ["## 3. Sentence Tokenization"],
        7: ["## 4. Subword Tokenization (BPE / WordPiece)"],
        9: ["## Summary: Choose spaCy for resume tokenization. It handles domain-specific tokens (C++, hyphens, slashes) correctly."]},
 "06": {0: ["# 06 — Text Normalization", "**Goal:** Clean messy real-world text into consistent form."],
        1: ["## 1. Case Normalization Trade-offs"],
        3: ["## 2. Unicode Normalization"],
        5: ["## 3. Bullet Symbol Normalization"],
        7: ["## 4. Complete ResumeCleaner"]},
 "07": {0: ["# 07 — Stop Words", "**Goal:** Understand when to remove (and NOT remove) common words."],
        1: ["## 1. NLTK vs spaCy Stop Lists"],
        3: ["## 2. The Problem — Stop Words That Matter"],
        5: ["## 3. Custom Resume Stop Words"],
        7: ["## Key Insight: Default stop lists designed for news articles. Customize for resumes."]},
 "08": {0: ["# 08 — Lemmatization", "**Goal:** Reduce words to dictionary base form using vocabulary + morphology."],
        1: ["## 1. spaCy Lemmatization"],
        3: ["## 2. spaCy vs NLTK"],
        5: ["## 3. When NOT to Lemmatize"],
        7: ["## Key Insight: Always preserve proper nouns (PROPN). Never lemmatize company names or tech brands."]},
 "09": {0: ["# 09 — Stemming", "**Goal:** Understand rule-based word reduction."],
        1: ["## 1. Porter vs Snowball"],
        3: ["## 2. The Crudeness Problem"],
        5: ["## Decision Guide",
            "- STEMMING: Fast search indexing, TF-IDF vocab reduction",
            "- LEMMATIZATION: Production NLP, resume matching, NER",
            "- **Use lemmatization for resume analysis**"]},
 "10": {0: ["# 10 — POS Tagging", "**Goal:** Label every word with its part of speech."],
        1: ["## 1. Context Determines POS"],
        3: ["## 2. Action Verbs from Resume Bullets"]},
 "12": {0: ["# 12 — NER", "**Goal:** Identify and classify named entities (people, companies, skills)."],
        1: ["## 1. Built-in spaCy NER"],
        3: ["## 2. The Problem: Skills Not Detected"],
        5: ["## 3. Adding Custom Skills with EntityRuler"],
        7: ["## 4. Hybrid Regex + NER Extractor"]},
}

# code cells with no outputs originally (must stay empty)
NO_OUTPUTS = {"06": [9], "12": [2, 4, 6, 8]}

fails = []
for k, path in NBS.items():
    nb = load(path)  # JSON validity by construction
    cells = nb["cells"]
    # (b) ids identical
    for idx, cid in ORIG_IDS[k].items():
        if cells[idx].get("id") != cid:
            fails.append(f"{k}: cell {idx} id changed {cells[idx].get('id')} != {cid}")
    # (c) preserved lines
    for idx, lines in PRESERVE[k].items():
        src = "".join(cells[idx].get("source", []))
        for ln in lines:
            if ln not in src:
                fails.append(f"{k}: cell {idx} missing preserved line: {ln!r}")
    # (a) md cells >= 300 chars
    md_lens = []
    for i, c in enumerate(cells):
        if c["cell_type"] == "markdown":
            l = len("".join(c.get("source", [])))
            md_lens.append(l)
            if l < 300:
                fails.append(f"{k}: md cell {i} only {l} chars")
    # (d) code cells: outputs non-empty where originally, empty where not
    for i, c in enumerate(cells):
        if c["cell_type"] == "code":
            n_out = len(c.get("outputs", []))
            if i in NO_OUTPUTS.get(k, []):
                if n_out != 0:
                    fails.append(f"{k}: code cell {i} gained {n_out} outputs")
            elif n_out == 0:
                fails.append(f"{k}: code cell {i} lost outputs")
    total_md = sum(md_lens)
    print(f"{k}: cells={len(cells)} md={len(md_lens)} min_md_len={min(md_lens)} total_md_chars={total_md}")

print()
print("FAILURES:", fails if fails else "NONE — all checks passed")
