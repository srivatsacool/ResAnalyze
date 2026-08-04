# -*- coding: utf-8 -*-
"""Verify expected behavior of block_g notebooks 40-45 by executing their actual logic."""
import re, sys
from collections import Counter

print("=" * 60)
print("CH40: detect_jd_sections")
print("=" * 60)
jd = """Senior Data Scientist
Google, Mountain View

About the role
We are looking for a senior data scientist to join our ML team.

Responsibilities
- Develop and deploy ML models at scale
- Collaborate with product teams
- Mentor junior data scientists

Qualifications
- 5+ years experience in data science
- Strong Python and SQL skills
- Experience with TensorFlow or PyTorch
- MS/PhD in Computer Science or related field

Nice to have
- Experience with NLP
- Published research papers

Benefits
- Competitive salary and equity
- Health insurance
- Remote work options
"""

JD_SECTIONS = {
    "about": ["about", "overview", "summary", "who we are", "the role"],
    "responsibilities": ["responsibilities", "what you'll do", "the role", "key duties", "what you will do"],
    "qualifications": ["qualifications", "requirements", "what you bring", "skills", "experience required"],
    "nice_to_have": ["nice to have", "bonus", "preferred", "plus", "good to have"],
    "benefits": ["benefits", "perks", "what we offer", "compensation"],
}

def detect_jd_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = "header"
    sections[current_section] = []
    for line in lines:
        ls = line.strip().lower()
        found = False
        for sec_name, keywords in JD_SECTIONS.items():
            if any(kw in ls for kw in keywords) and len(ls) < 40:
                current_section = sec_name
                sections[current_section] = []
                found = True
                break
        if not found and ls:
            sections.setdefault(current_section, []).append(line.strip())
    return sections

secs = detect_jd_sections(jd)
for name, content in secs.items():
    print(f"\n[{name.upper()}] ({len(content)} lines)")
    for line in content[:3]:
        print(f"  {line[:60]}")

print()
print("=" * 60)
print("CH41: extract_jd_skills (with ch40 state: detect_jd_sections in scope)")
print("=" * 60)
SKILLS_DB = ["Python", "TensorFlow", "PyTorch", "SQL", "Spark", "Docker", "Kubernetes", "AWS", "NLP"]

def extract_jd_skills(jd_text, skills_db):
    required, preferred = [], []
    sections = detect_jd_sections(jd_text) if 'detect_jd_sections' in dir() else {"qualifications": [jd_text], "nice_to_have": [jd_text]}
    for skill in skills_db:
        found_in = []
        for sec_name, lines in sections.items():
            text = " ".join(lines).lower()
            if skill.lower() in text:
                found_in.append(sec_name)
        if "nice_to_have" in found_in:
            preferred.append(skill)
        elif found_in:
            required.append(skill)
    return required, preferred

req, pref = extract_jd_skills(jd, SKILLS_DB)
print("Required:", req)
print("Preferred:", pref)

print()
print("--- CH41 fallback path (fresh kernel: detect_jd_sections NOT defined) ---")
def extract_jd_skills_fallback(jd_text, skills_db):
    required, preferred = [], []
    sections = {"qualifications": [jd_text], "nice_to_have": [jd_text]}
    for skill in skills_db:
        found_in = []
        for sec_name, lines in sections.items():
            text = " ".join(lines).lower()
            if skill.lower() in text:
                found_in.append(sec_name)
        if "nice_to_have" in found_in:
            preferred.append(skill)
        elif found_in:
            required.append(skill)
    return required, preferred
r2, p2 = extract_jd_skills_fallback(jd, SKILLS_DB)
print("Fallback Required:", r2)
print("Fallback Preferred:", p2)

print()
print("--- CH41 skill_frequency ---")
def skill_frequency(jd_text, skills_db):
    words = re.findall(r"\b\w+\b", jd_text.lower())
    freq = Counter(words)
    skill_counts = {}
    for skill in skills_db:
        count = jd_text.lower().count(skill.lower())
        if count > 0:
            skill_counts[skill] = count
    return sorted(skill_counts.items(), key=lambda x: -x[1])

print("skill_frequency(jd, SKILLS_DB):", skill_frequency(jd, SKILLS_DB))
print("word 'python' count incl substring:", jd.lower().count("python"))

print()
print("=" * 60)
print("CH43: degree + years extraction")
print("=" * 60)
def extract_degree_requirements(jd_text):
    degrees = {
        "phd": ["phd", "doctorate", "ph.d"],
        "masters": ["masters", "ms", "m.s.", "m.tech", "m.sc"],
        "bachelors": ["bachelors", "bs", "b.s.", "b.tech", "b.e.", "b.sc"],
    }
    found = []
    for level, keywords in degrees.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", jd_text, re.IGNORECASE):
                found.append(level)
                break
    return found

def extract_years_required(jd_text):
    patterns = [
        r"(\d+)[+]?\s*(?:\+)?\s*years?\s+(?:of\s+)?(?:experience|exp)",
        r"(?:experience|exp)[^\n]{0,20}(\d+)[+]?\s*years?",
    ]
    for pat in patterns:
        match = re.search(pat, jd_text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

print("Degree requirements:", extract_degree_requirements(jd))
print("Years required:", extract_years_required(jd))

print()
print("=" * 60)
print("CH42: spacy action verbs + seniority")
print("=" * 60)
import spacy
nlp = spacy.load("en_core_web_sm")
responsibilities_text = """Responsibilities
- Develop and deploy ML models at scale
- Collaborate with cross-functional teams
- Mentor junior data scientists
- Design experiments to validate hypotheses
- Present findings to stakeholders
"""
doc = nlp(responsibilities_text)
for token in doc:
    if token.pos_ == "VERB":
        obj = next((child.text for child in token.children if child.dep_ in ("dobj", "pobj", "attr")), None)
        print(f"  Action: {token.lemma_:12s} -> Object: {obj or '(none)'}")

seniority_signals = {
    "junior": ["junior", "early career", "0-2 years", "entry level"],
    "mid": ["mid", "3-5 years", "experienced"],
    "senior": ["senior", "lead", "staff", "principal", "5+ years", "7+ years"],
    "manager": ["manager", "head of", "director", "lead a team", "manage"],
}
def detect_seniority(jd_text):
    text_lower = jd_text.lower()
    for level, signals in seniority_signals.items():
        for signal in signals:
            if signal in text_lower:
                return level
    return "not specified"
print("Seniority(jd):", detect_seniority(jd))
print("Seniority(no signals):", detect_seniority("Hiring a data scientist. No level words here at all."))

print()
print("=" * 60)
print("CH44: TF-IDF (sklearn)")
print("=" * 60)
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
jd_text44 = """Senior Data Scientist with Python, TensorFlow, and NLP.
5+ years experience in machine learning and deep learning.
Strong SQL and AWS skills required."""
corpus = [
    jd_text44,
    "Software engineer with Java, Spring Boot, and microservices",
    "Frontend developer with React, TypeScript, and CSS",
    "DevOps engineer with Docker, Kubernetes, and CI/CD",
    "Data analyst with Excel, Tableau, and SQL",
]
vec = TfidfVectorizer(stop_words="english", max_features=30)
X = vec.fit_transform(corpus)
scores = X[0].toarray().flatten()
features = vec.get_feature_names_out()
print("vocab size:", len(features))
print("vocab:", list(features))
print("Top JD keywords:")
for idx in np.argsort(scores)[-10:][::-1]:
    print(f"  {features[idx]:20s} {scores[idx]:.3f}")

print()
print("--- CH44 embedding path: what happens with broken sentence_transformers ---")
try:
    from sentence_transformers import SentenceTransformer, util
    print("import ok")
except Exception as e:
    print("import FAILED -> notebook prints 'SentenceTransformer not available':", type(e).__name__, str(e)[:80])

print()
print("=" * 60)
print("CH45: rule-based classification (zero-shot unavailable -> fallback)")
print("=" * 60)
requirements = [
    "5+ years experience in Python",
    "Strong communication skills",
    "PhD in Computer Science preferred",
    "Experience with AWS or GCP",
    "Published research papers a plus",
    "Ability to work in fast-paced environment",
]
def classify_requirement(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["preferred", "plus", "nice", "bonus", "desired"]):
        return "nice-to-have"
    if any(w in text_lower for w in ["must", "required", "essential", "minimum"]):
        return "must-have"
    if any(w in text_lower for w in ["ability to", "strong"]):
        return "soft-skill"
    return "must-have"

for req in requirements:
    print(f"  {classify_requirement(req):15s} | {req}")

print()
print("--- CH45 notebook fallback branch (as written in cell 2) ---")
try:
    from transformers import pipeline
    print("transformers import ok")
except Exception as e:
    print("transformers import FAILED -> except branch runs:", type(e).__name__, str(e)[:60])
    for req in requirements:
        if any(w in req.lower() for w in ["preferred", "plus", "nice", "bonus"]):
            print(f"  '{req[:40]:40s}' -> nice-to-have (rule)")
        else:
            print(f"  '{req[:40]:40s}' -> must-have (rule)")
print()
print("ALL VERIFICATION DONE")
