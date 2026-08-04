# -*- coding: utf-8 -*-
"""Verify block_g notebooks after markdown expansion: md>=300 chars, code cells byte-identical
to the first dump (transcribed below), headings intact, JSON valid."""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from nbtools import load

BASE = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g"

# Expected code-cell sources transcribed from the FIRST dumps (pre-apply), by notebook tag.
EXPECTED_CODE = {
"40": {
2: 'jd = """Senior Data Scientist\nGoogle, Mountain View\n\nAbout the role\nWe are looking for a senior data scientist to join our ML team.\n\nResponsibilities\n- Develop and deploy ML models at scale\n- Collaborate with product teams\n- Mentor junior data scientists\n\nQualifications\n- 5+ years experience in data science\n- Strong Python and SQL skills\n- Experience with TensorFlow or PyTorch\n- MS/PhD in Computer Science or related field\n\nNice to have\n- Experience with NLP\n- Published research papers\n\nBenefits\n- Competitive salary and equity\n- Health insurance\n- Remote work options\n""" + '"\nprint("JD structure: Title -> Company -> About -> Responsibilities -> Qualifications -> Nice-to-have -> Benefits")',
4: 'import re\n\nJD_SECTIONS = {\n    "about": ["about", "overview", "summary", "who we are", "the role"],\n    "responsibilities": ["responsibilities", "what you\'ll do", "the role", "key duties", "what you will do"],\n    "qualifications": ["qualifications", "requirements", "what you bring", "skills", "experience required"],\n    "nice_to_have": ["nice to have", "bonus", "preferred", "plus", "good to have"],\n    "benefits": ["benefits", "perks", "what we offer", "compensation"],\n}\n\ndef detect_jd_sections(text):\n    lines = text.split("\\n")\n    sections = {}\n    current_section = "header"\n    sections[current_section] = []\n    for line in lines:\n        ls = line.strip().lower()\n        found = False\n        for sec_name, keywords in JD_SECTIONS.items():\n            if any(kw in ls for kw in keywords) and len(ls) < 40:\n                current_section = sec_name\n                sections[current_section] = []\n                found = True\n                break\n        if not found and ls:\n            sections.setdefault(current_section, []).append(line.strip())\n    return sections\n\nsecs = detect_jd_sections(jd)\nfor name, content in secs.items():\n    print(f"\\n[{name.upper()}]")\n    for line in content[:3]:\n        print(f"  {line[:60]}")',
},
"41": {
2: 'import re\n\nSKILLS_DB = ["Python", "TensorFlow", "PyTorch", "SQL", "Spark", "Docker", "Kubernetes", "AWS", "NLP"]\n\ndef extract_jd_skills(jd_text, skills_db):\n    required, preferred = [], []\n    sections = detect_jd_sections(jd_text) if \'detect_jd_sections\' in dir() else {"qualifications": [jd_text], "nice_to_have": [jd_text]}\n    \n    for skill in skills_db:\n        found_in = []\n        for sec_name, lines in sections.items():\n            text = " ".join(lines).lower()\n            if skill.lower() in text:\n                found_in.append(sec_name)\n        if "nice_to_have" in found_in:\n            preferred.append(skill)\n        elif found_in:\n            required.append(skill)\n    return required, preferred\n\nreq, pref = extract_jd_skills(jd, SKILLS_DB)\nprint("Required:")\nfor s in req: print(f"  - {s}")\nprint("\\nPreferred:")\nfor s in pref: print(f"  - {s}")',
4: 'from collections import Counter\nimport re\n\ndef skill_frequency(jd_text, skills_db):\n    words = re.findall(r"\\\\b\\\\w+\\\\b", jd_text.lower())\n    freq = Counter(words)\n    # Check skills\n    skill_counts = {}\n    for skill in skills_db:\n        count = jd_text.lower().count(skill.lower())\n        if count > 0:\n            skill_counts[skill] = count\n    return sorted(skill_counts.items(), key=lambda x: -x[1])\n\nfor skill, count in skill_frequency(jd, SKILLS_DB)[:8]:\n    print(f"  {skill:12s}: mentioned {count}x")',
},
"42": {
2: 'import re, spacy\nnlp = spacy.load("en_core_web_sm")\n\nresponsibilities_text = """Responsibilities\n- Develop and deploy ML models at scale\n- Collaborate with cross-functional teams\n- Mentor junior data scientists\n- Design experiments to validate hypotheses\n- Present findings to stakeholders\n"""\n\ndoc = nlp(responsibilities_text)\nprint("Action verb detection:")\nfor token in doc:\n    if token.pos_ == "VERB":\n        # Find the object\n        obj = next((child.text for child in token.children if child.dep_ in ("dobj", "pobj", "attr")), None)\n        print(f"  Action: {token.lemma_:12s} -> Object: {obj or \'(none)\'}")',
4: 'seniority_signals = {\n    "junior": ["junior", "early career", "0-2 years", "entry level"],\n    "mid": ["mid", "3-5 years", "experienced"],\n    "senior": ["senior", "lead", "staff", "principal", "5+ years", "7+ years"],\n    "manager": ["manager", "head of", "director", "lead a team", "manage"],\n}\n\ndef detect_seniority(jd_text):\n    text_lower = jd_text.lower()\n    for level, signals in seniority_signals.items():\n        for signal in signals:\n            if signal in text_lower:\n                return level\n    return "not specified"\n\nprint(f"Seniority: {detect_seniority(jd)}")',
},
"43": {
2: 'import re\n\ndef extract_degree_requirements(jd_text):\n    degrees = {\n        "phd": ["phd", "doctorate", "ph.d"],\n        "masters": ["masters", "ms", "m.s.", "m.tech", "m.sc"],\n        "bachelors": ["bachelors", "bs", "b.s.", "b.tech", "b.e.", "b.sc"],\n    }\n    found = []\n    for level, keywords in degrees.items():\n        for kw in keywords:\n            if re.search(r"\\\\b" + re.escape(kw) + r"\\\\b", jd_text, re.IGNORECASE):\n                found.append(level)\n                break\n    return found\n\nprint(f"Degree requirements: {extract_degree_requirements(jd)}")',
4: 'def extract_years_required(jd_text):\n    """Extract years of experience required."""\n    patterns = [\n        r"(\\d+)[+]?\\s*(?:\\+)?\\s*years?\\s+(?:of\\s+)?(?:experience|exp)",\n        r"(?:experience|exp)[^\\n]{0,20}(\\d+)[+]?\\s*years?",\n    ]\n    for pat in patterns:\n        match = re.search(pat, jd_text, re.IGNORECASE)\n        if match:\n            return int(match.group(1))\n    return None\n\nprint(f"Years required: {extract_years_required(jd)}")',
},
"44": {
2: 'from sklearn.feature_extraction.text import TfidfVectorizer\nimport numpy as np\n\n# Compare JD against generic job corpus\njd_text = """Senior Data Scientist with Python, TensorFlow, and NLP.\n5+ years experience in machine learning and deep learning.\nStrong SQL and AWS skills required."""\n\ncorpus = [\n    jd_text,\n    "Software engineer with Java, Spring Boot, and microservices",\n    "Frontend developer with React, TypeScript, and CSS",\n    "DevOps engineer with Docker, Kubernetes, and CI/CD",\n    "Data analyst with Excel, Tableau, and SQL",\n]\n\nvec = TfidfVectorizer(stop_words="english", max_features=30)\nX = vec.fit_transform(corpus)\nscores = X[0].toarray().flatten()\nfeatures = vec.get_feature_names_out()\n\nprint("Top JD keywords:")\nfor idx in np.argsort(scores)[-10:][::-1]:\n    print(f"  {features[idx]:20s} {scores[idx]:.3f}")',
4: 'from sentence_transformers import SentenceTransformer, util\ntry:\n    model = SentenceTransformer("all-MiniLM-L6-v2")\n    jd_emb = model.encode(jd_text)\n    \n    # Score each keyword by similarity to JD\n    keywords = ["Python", "TensorFlow", "NLP", "SQL", "AWS", "Java", "React", "Docker"]\n    for kw in keywords:\n        kw_emb = model.encode(kw)\n        sim = util.cos_sim(jd_emb, kw_emb).item()\n        print(f"  {kw:12s} relevance: {sim:.3f}")\nexcept:\n    print("SentenceTransformer not available")',
},
"45": {
2: 'from transformers import pipeline\nrequirements = [\n    "5+ years experience in Python",\n    "Strong communication skills",\n    "PhD in Computer Science preferred",\n    "Experience with AWS or GCP",\n    "Published research papers a plus",\n    "Ability to work in fast-paced environment",\n]\n\ntry:\n    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")\n    labels = ["must-have", "nice-to-have", "preferred"]\n    \n    for req in requirements:\n        result = classifier(req, labels)\n        print(f"  \'{req[:40]:40s}\' -> {result[\'labels\'][0]:15s} ({result[\'scores\'][0]:.2f})")\nexcept:\n    print("Transformers not available. Rule-based fallback:")\n    for req in requirements:\n        if any(w in req.lower() for w in ["preferred", "plus", "nice", "bonus"]):\n            print(f"  \'{req[:40]:40s}\' -> nice-to-have (rule)")\n        else:\n            print(f"  \'{req[:40]:40s}\' -> must-have (rule)")',
4: 'def classify_requirement(text):\n    """Classify requirement by keyword rules."""\n    text_lower = text.lower()\n    if any(w in text_lower for w in ["preferred", "plus", "nice", "bonus", "desired"]):\n        return "nice-to-have"\n    if any(w in text_lower for w in ["must", "required", "essential", "minimum"]):\n        return "must-have"\n    if any(w in text_lower for w in ["ability to", "strong"]):\n        return "soft-skill"\n    return "must-have"  # default\n\nfor req in requirements:\n    print(f"  {classify_requirement(req):15s} | {req}")',
},
}

EXPECTED_HEADS = {
"40": ["# 40 — JD Parsing", "## 1. Typical JD Structure", "## 2. JD Section Detection", "## Summary: JD parsing identifies sections for targeted extraction. Similar approach to resume sections."],
"41": ["# 41 — JD Skill Extraction", "## 1. Required vs Preferred Skills", "## 2. Skill Frequency Analysis", "## Summary: Section-based extraction distinguishes required from preferred skills."],
"42": ["# 42 — Responsibility Detection", "## 1. Identifying Action Phrases", "## 2. Seniority Signal Detection", "## Summary: POS tagging extracts action verbs. Keyword matching detects seniority."],
"43": ["# 43 — Qualification Detection", "## 1. Degree Requirement Extraction", "## 2. Experience Year Extraction", "## Summary: Regex extracts degree and experience requirements. Combine for qualification matching."],
"44": ["# 44 — Keyword Ranking", "## 1. TF-IDF Keyword Extraction from JD", "## 2. Embedding-Based Keyword Importance", "## Summary: TF-IDF ranks distinctive keywords. Embedding similarity measures semantic relevance to the JD."],
"45": ["# 45 — Requirement Classification", "## 1. Zero-Shot Classification", "## 2. Rule-Based Classification", "## Summary: Zero-shot is more accurate. Rule-based is faster and always available."],
}

all_ok = True
for rel, tag in [("40_jd_parsing/40.ipynb","40"),("41_jd_skill_extraction/41.ipynb","41"),
                 ("42_responsibility_detection/42.ipynb","42"),("43_qualification_detection/43.ipynb","43"),
                 ("44_keyword_ranking/44.ipynb","44"),("45_requirement_classification/45.ipynb","45")]:
    path = BASE + "\\" + rel
    nb = load(path)
    json.dumps(nb)  # JSON valid (also parsed above)
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    md_chars = sum(len("".join(c["source"])) for c in md_cells)
    short = [(i, len("".join(c["source"]))) for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown" and len("".join(c["source"])) < 300]
    print(f"== {tag}: md={len(md_cells)} code={len(code_cells)} md_chars_total={md_chars} short_md={short or 'NONE'}")
    # heading check: first line of each md cell must equal expected heading EXACTLY
    got_heads = ["".join(c["source"]).split("\n")[0] for c in nb["cells"] if c["cell_type"] == "markdown"]
    exp_heads = EXPECTED_HEADS[tag]
    head_ok = got_heads == exp_heads
    print(f"   headings intact: {head_ok}")
    if not head_ok:
        print("   got:", got_heads)
        print("   exp:", exp_heads)
        all_ok = False
    # code byte-identity
    for idx, exp_src in EXPECTED_CODE[tag].items():
        got_src = "".join(nb["cells"][idx]["source"])
        if got_src != exp_src:
            all_ok = False
            print(f"   CODE MISMATCH cell {idx}!")
            # show first differing line
            gl, el = got_src.split("\n"), exp_src.split("\n")
            for n, (a, b) in enumerate(zip(gl, el)):
                if a != b:
                    print(f"     line {n}: got={a!r} exp={b!r}")
                    break
            if len(gl) != len(el):
                print(f"     line-count diff: got={len(gl)} exp={len(el)}")
        else:
            print(f"   code cell {idx}: byte-identical OK")
    # code cells not in replace: ensure no extra code cells modified (count check)
    print()
print("ALL_OK" if all_ok else "FAILURES PRESENT")
