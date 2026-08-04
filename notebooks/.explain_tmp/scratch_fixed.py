# -*- coding: utf-8 -*-
"""Run CORRECTED variants (r'\\b' instead of r'\\\\b') of the gotcha cells,
to give honest 'expected when fixed' values for the teaching markdown."""
import re
from rapidfuzz import fuzz, process

print("===== NB33 regex cell, boundary fixed =====")
SKILLS_DB = {
    "programming": ["Python", "Java", "JavaScript", "TypeScript", "C++", "Go", "Rust", "Scala", "Kotlin", "Ruby", "PHP", "C#", "Swift"],
    "ml_dl": ["TensorFlow", "PyTorch", "scikit-learn", "Keras", "XGBoost", "LightGBM", "JAX"],
    "nlp": ["NLP", "spaCy", "NLTK", "Hugging Face", "Transformers", "BERT", "GPT", "LLM"],
    "data": ["SQL", "Pandas", "NumPy", "Spark", "Hadoop", "Tableau", "Power BI", "Looker"],
    "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins"],
    "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra"],
}
def extract_skills_regex(text, skills_db):
    found = []
    for category, skills in skills_db.items():
        for skill in skills:
            if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
                found.append({"raw": skill, "category": category, "confidence": 1.0, "method": "exact_match"})
    return found
resume = "Experienced with Python, TensorFlow, and AWS.\nAlso skilled in NLP, PyTorch, and Kubernetes."
for s in extract_skills_regex(resume, SKILLS_DB):
    print(f"  {s['raw']:15s} -> {s['category']:15s} (conf: {s['confidence']})")

print("===== NB33 fuzzy cell, boundary fixed =====")
def extract_skills_fuzzy(text, skills_db, threshold=85):
    all_skills = [(cat, s) for cat, skills in skills_db.items() for s in skills]
    words = re.findall(r"\b[A-Za-z#+]+", text)
    found = set()
    for word in words:
        best_match = process.extractOne(word, [s for _, s in all_skills], scorer=fuzz.ratio)
        if best_match and best_match[1] >= threshold:
            cat = next(c for c, s in all_skills if s == best_match[0])
            found.add((best_match[0], cat, best_match[1]))
    return found
for skill, cat, score in extract_skills_fuzzy("I know PyTorch, TensrFlow, and Dockr", SKILLS_DB):
    print(f"  '{skill:15s}' -> {cat:15s} (fuzzy: {score}%)")

print("===== NB35 education cell, boundary fixed =====")
DEGREES = ["B.Tech","B.E.","B.S.","B.Sc","B.A.","B.Com","B.B.A.","M.Tech","M.E.","M.S.","M.Sc","M.A.","M.Com","M.B.A.","MBA","PhD","Ph.D.","Doctorate","Bachelors","Masters","Bachelor","Master","10th","12th","Higher Secondary","SSC","HSC"]
def extract_education(text):
    entries = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        for degree in DEGREES:
            if re.search(r"\b" + re.escape(degree) + r"\b", line, re.IGNORECASE):
                inst_match = re.search(r"(?:at|from)\s+([A-Z][A-Za-z\s.]+)", line)
                institution = inst_match.group(1) if inst_match else ""
                year_match = re.search(r"\b(19\d{2}|20\d{2})\b", line)
                year = year_match.group(1) if year_match else None
                field_match = re.search(r"in\s+([A-Za-z\s]+)", line)
                field = field_match.group(1).strip() if field_match else ""
                entries.append({"degree": degree, "institution": institution, "field": field, "year": year,
                                "confidence": "high" if (institution and year) else "medium"})
                break
    return entries
for e in extract_education("B.Tech in Computer Science, IIT Bombay, 2019\nM.S. in Data Science from Stanford University, 2021\nPhD in NLP, MIT (ongoing)"):
    print(f"  {e['degree']:8s} in {e['field']:20s} @ {e['institution']:20s} ({e['year']}) [{e['confidence']}]")

print("===== NB39 skills loop, boundary fixed =====")
SKILLS_DB2 = {"programming": ["Python", "Java"], "ml_dl": ["TensorFlow", "PyTorch"]}
sample = "Srivatsa Gorti\nsrivatsa@email.com\n\nEXPERIENCE\nGoogle — Senior Data Scientist\n- Developed ML pipelines\n\nSKILLS\nPython, TensorFlow, NLP\n"
hits = []
for cat, skills in SKILLS_DB2.items():
    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", sample, re.IGNORECASE):
            hits.append((skill, cat))
print("  hits:", hits)

print("===== NB38 bullet counts (real run already done; just recount) =====")
project_text = """PROJECTS
Resume Intelligence Platform | Python, NLP, TensorFlow
- Built end-to-end resume parsing and ATS scoring system
- Achieved 92% accuracy on skill extraction

Sentiment Analysis Dashboard | Python, Flask, React
- Real-time sentiment analysis for 10K+ tweets/day
- Deployed on AWS with 99.9% uptime

E-commerce Recommendation Engine | Python, Spark, MongoDB
- Collaborative filtering for 1M+ users
- Increased conversion rate by 25%
"""
def extract_projects(text):
    projects = []
    lines = text.split("\n")
    current = None
    for line in lines:
        ls = line.strip()
        if not ls: continue
        proj_match = re.match(r"^([A-Za-z\s]+)\s*[|]\s*(.+)$", ls)
        if proj_match:
            if current: projects.append(current)
            current = {"name": proj_match.group(1).strip(), "tech": proj_match.group(2).strip(), "bullets": []}
            continue
        bullet = re.sub(r"^[\s•\-*–]+", "", ls)
        if bullet and current:
            current["bullets"].append(bullet)
    if current: projects.append(current)
    return projects
for p in extract_projects(project_text):
    print(f"  {p['name']} | {p['tech']} | bullets={len(p['bullets'])}")
    for b in p["bullets"]:
        print(f"      - {b}")
