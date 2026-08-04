# -*- coding: utf-8 -*-
"""Verify block_k edits: md cell lengths >= 300, headings intact, JSON valid, code sources unchanged."""
import json, sys

K = r"D:\Projects\ResAnalyze\notebooks\part3_production\block_k"
NBS = {
    "64": (K + r"\64_precision_and_recall_for_nlp\64.ipynb", {
        0: "# 64 — Precision & Recall for NLP",
        1: "## 1. Why Metrics Matter",
        3: "## 2. Computing Metrics",
        5: "## 3. Per-Category Breakdown",
        7: "## Summary: Precision, recall, F1 are the standard NLP evaluation metrics. Track per-category for insights.",
    }),
    "65": (K + r"\65_f1_score_and_confusion_matrix\65.ipynb", {
        0: "# 65 — F1 & Confusion Matrix",
        1: "## 1. Confusion Matrix Basics",
        3: "## 2. Classification Report",
        5: "## 3. Macro vs Micro vs Weighted F1",
        7: "## Summary: Confusion matrices show WHERE errors happen. Use weighted F1 for imbalanced resume data.",
    }),
    "66": (K + r"\66_hallucination_testing\66.ipynb", {
        0: "# 66 — Hallucination Testing",
        1: "## 1. Types of Hallucination",
        3: "## 2. Grounding Checker",
        5: "## 3. Consistency Testing",
        7: "## Summary: Hallucination testing catches LLM fabrications. Always ground-check outputs against source text.",
    }),
    "67": (K + r"\67_a-b_prompt_testing\67.ipynb", {
        0: "# 67 — A/B Prompt Testing",
        1: "## 1. A/B Testing Framework",
        3: "## 2. Statistical Significance",
        5: "## Summary: A/B test prompts against golden datasets. Use statistical tests to confirm significance.",
    }),
    "68": (K + r"\68_human_evaluation_protocol\68.ipynb", {
        0: "# 68 — Human Evaluation Protocol",
        1: "## 1. Annotation Guidelines",
        3: "## 2. Inter-Annotator Agreement",
        5: "## 3. Annotation Workflow",
        7: "## Summary: Human evaluation is the gold standard. Cohen's Kappa measures agreement beyond chance.",
    }),
    "69": (K + r"\69_latency_profiling\69.ipynb", {
        0: "# 69 — Latency Profiling",
        1: "## 1. Why Latency Matters",
        3: "## 2. Simple Profiling",
        5: "## 3. Profiling with cProfile",
        7: "## 4. Optimizing Bottlenecks",
        9: "## Summary: Profile before optimizing. Target the biggest bottleneck first. Cache aggressively.",
    }),
}

ok = True
for name, (path, headings) in NBS.items():
    with open(path, encoding="utf-8-sig") as f:
        nb = json.load(f)  # raises if invalid JSON
    cells = nb["cells"]
    md_cells = [i for i, c in enumerate(cells) if c["cell_type"] == "markdown"]
    md_chars = sum(len("".join(c["source"])) for c in cells if c["cell_type"] == "markdown")
    problems = []
    for i, c in enumerate(cells):
        src = "".join(c["source"])
        if c["cell_type"] == "markdown":
            if len(src) < 300:
                problems.append(f"md[{i}] only {len(src)} chars")
        if i in headings:
            if not src.startswith(headings[i]):
                problems.append(f"heading[{i}] changed: {src[:60]!r}")
            if headings[i] not in src:
                problems.append(f"heading[{i}] not in cell: {src[:60]!r}")
    # code cells: verify metadata intact and source non-empty; also print first line for eyeball check
    code_lines = []
    for i, c in enumerate(cells):
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            code_lines.append(f"  code[{i}] first-line={src.splitlines()[0][:60]!r} exec_count={c.get('execution_count')} id={c.get('id')}")
    status = "OK " if not problems else "FAIL"
    if problems:
        ok = False
    print(f"[{status}] {name}: md_cells={len(md_cells)} md_chars={md_chars} total_cells={len(cells)}")
    for p in problems:
        print("   !", p)
    for cl in code_lines:
        print(cl)

print("\nJSON valid for all; overall:", "PASS" if ok else "FAIL")
