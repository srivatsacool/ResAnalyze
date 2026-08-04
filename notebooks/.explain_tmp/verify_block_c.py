# -*- coding: utf-8 -*-
"""Verify: JSON valid, code cells byte-identical to snapshot, md cells >=300 chars, headings intact."""
import json, glob, os

snap_dir = r"D:/Projects/ResAnalyze/notebooks/.explain_tmp/code_snap"
paths = sorted(glob.glob(r"D:/Projects/ResAnalyze/notebooks/part1_foundations/block_c/*/*.ipynb"))

HEADINGS = {
    "13": ["# 13 — Chunking & Phrase Extraction", "## 1. Noun Chunks with spaCy", "## 2. Extracting Skill Phrases from Resumes",
           "## 3. Verb Phrase (Action + Object) Extraction", "## 4. Keyword Chunking for Resume Search",
           "## Key Insight: Chunking preserves multi-word concepts that single-token approaches miss."],
    "14": ["# 14 — Keyword Extraction", "## 1. TF-IDF Keyword Extraction", "## 2. RAKE (Rapid Automatic Keyword Extraction)",
           "## 3. KeyBERT (BERT-based Keyword Extraction)",
           "## Summary: TF-IDF = fast & interpretable. KeyBERT = semantic but slower. Use both."],
    "15": ["# 15 — Bag of Words (BoW)", "## 1. How BoW Works", "## 2. Vocabulary Size vs Sparsity",
           "## 3. BoW for Resume Comparison",
           "## Key Insight: BoW is simple but loses word order and semantics. Use as a baseline."],
    "16": ["# 16 — TF-IDF Deep Dive", "## 1. TF-IDF Manually", "## 2. TF-IDF with scikit-learn",
           "## 3. TF-IDF for Resume-JD Matching",
           "## Key Insight: TF-IDF downweights common words ('experience', 'data') and highlights distinctive ones (skills, tech)."],
    "17": ["# 17 — N-Grams", "## 1. Unigrams, Bigrams, Trigrams", "## 2. N-Grams for Skill Detection",
           "## 3. N-Gram Overlap for Resume Comparison",
           "## Summary: Use ngram_range=(1,2) for most resume tasks — captures bi-gram skills like 'machine learning'."],
    "18": ["# 18 — Cosine Similarity", "## 1. Cosine Similarity from Scratch", "## 2. Resume Similarity with TF-IDF + Cosine",
           "## 3. Resume vs JD Scoring",
           "## Key Insight: Cosine similarity = angle between vectors, not magnitude. Handles different document lengths gracefully."],
    "19": ["# 19 — Word2Vec", "## 1. Training a Small Word2Vec Model", "## 2. Word Similarity", "## 3. Most Similar Words",
           "## 4. Word Analogies", "## 5. Averaging Word Vectors for Document Similarity",
           "## Key Insight: Word2Vec captures semantics — 'python' is close to 'nlp' AND 'tensorflow'."],
    "20": ["# 20 — FastText", "## 1. Training FastText with Gensim", "## 2. FastText Handles Out-of-Vocabulary Words",
           "## 3. FastText vs Word2Vec on Typos", "## 4. Subword Details",
           "## Summary: Use FastText for resume parsing — resumes often have typos ('Tensorflo', 'Pytorch')."],
}

all_ok = True
for p in paths:
    tag = p.split("block_c")[-1].split("\\")[1]
    num = tag.split("_")[0]
    nb = json.load(open(p, encoding="utf-8-sig"))  # JSON validity
    snap = json.load(open(os.path.join(snap_dir, tag + ".json"), encoding="utf-8"))
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    total_md = sum(len("".join(c.get("source", []))) for c in md_cells)

    # 1) code cells byte-identical
    ok_code = True
    for s in snap:
        c = nb["cells"][s["index"]]
        cur = "".join(c.get("source", []))
        if c.get("id") != s["id"] or cur != s["source"]:
            ok_code = False
            print(f"  MISMATCH {tag} cell {s['index']}: id {c.get('id')} vs {s['id']}")
    # 2) md cells >= 300 chars
    short = [(i, len("".join(c.get("source", [])))) for i, c in enumerate(md_cells)
             if len("".join(c.get("source", []))) < 300]
    # 3) headings intact (as lines inside md cells)
    md_all = "\n".join("".join(c.get("source", [])) for c in md_cells)
    missing_h = [h for h in HEADINGS[num] if h not in md_all]
    ok = ok_code and not short and not missing_h
    all_ok = all_ok and ok
    print(f"{num} | md cells: {len(md_cells):2d} | total md chars: {total_md:5d} | code cells: {len(code_cells)} "
          f"| code identical: {'YES' if ok_code else 'NO'} | md>=300: {'YES' if not short else short} "
          f"| headings ok: {'YES' if not missing_h else missing_h}")

print("ALL OK" if all_ok else "FAILURES PRESENT")
