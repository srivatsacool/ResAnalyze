# AI Resume Intelligence Platform

> **Version:** 0.2 (Architecture & Learning Design)
> **Status:** Active Planning
> **Author:** Srivatsa Gorti
> **Stack:** Python · NLP · FastAPI · React · MCP · OpenRouter

---

# Executive Summary

The **AI Resume Intelligence Platform** is a production-oriented AI application that demonstrates the complete lifecycle of modern AI engineering — from NLP research and experimentation to cloud deployment and MCP-based AI assistant integration.

This project is **not** a GPT wrapper. It is an engineered system where every stage of the analysis pipeline is transparent, independently testable, and built from first principles.

The project serves three purposes simultaneously:

- **Learning Platform** — Master NLP, embeddings, semantic search, prompt engineering, and AI system design from the ground up.
- **Engineering Portfolio** — Demonstrate production-quality architecture across backend, frontend, cloud, and AI integration.
- **AI Research Playground** — Experiment with multiple NLP techniques, compare algorithms, and understand why production AI systems are built the way they are.

---

# Why This Project Exists

Most resume analyzers today:

```
Resume → Send to GPT → Generic Suggestions
```

This approach has no explainability, no reusable architecture, and no educational value.

This platform instead builds a complete engineering pipeline:

```
Resume
  ↓  Document Parsing (PDF, DOCX, OCR)
  ↓  Text Cleaning & Normalization
  ↓  Section Detection
  ↓  Information Extraction (NER + Rules + Embeddings)
  ↓  Skill Normalization (ESCO / O*NET)
  ↓  Embedding Generation
  ↓  Semantic Matching against Job Description
  ↓  Explainable ATS Scoring
  ↓  Weak Bullet Detection & STAR Classification
  ↓  Confidence-Scored Extraction Report
  ↓  LLM Reasoning (selective — only where needed)
  ↓  Actionable Recommendations
  ↓  Interactive Dashboard with Visualizations
```

Each component is independently testable, replaceable, and explainable.

---

# Project Philosophy

## 1. Learning First
Every feature must teach an AI engineering concept. No feature exists purely for aesthetic value.

## 2. Explainability Over Magic
The system always explains:
- Why a score was assigned
- Why a skill is missing
- Why a bullet is weak
- How confident each extraction is and where it came from

Users never receive a mysterious "ATS Score: 82." They see the breakdown.

## 3. Engineering Before Prompting
LLMs are one component. The platform combines:
- Regex and rule-based parsing
- NLP (tokenization, POS, NER, dependency parsing)
- Classical ML (TF-IDF, cosine similarity)
- Neural embeddings (Sentence Transformers)
- Vector search (FAISS, ChromaDB)
- Explainable scoring engines
- Selective, versioned prompt engineering

## 4. Modular Engine Design
Every capability is an independent engine:

```
ResumeParserEngine → JobDescriptionEngine → SkillNormalizerEngine
       ↓                     ↓                       ↓
EmbeddingEngine ──────────────────────────────────────→ ATSEngine
       ↓                                               ↓
BulletScorerEngine                          RecommendationEngine
       ↓                                               ↓
LLMRewriteEngine                            EvaluationEngine
```

Each engine reads and writes a canonical `ResumeSchema`. No engine knows how another is implemented.

## 5. Production Engineering
This personal project follows production-grade practices:
- Clean architecture & dependency injection
- Typed schemas (Pydantic)
- Structured logging
- Configuration management
- Comprehensive testing
- CI/CD, Docker, cloud deployment

## 6. Continuous Learning
Each release represents an increase in understanding, not just more features.

---

# The Canonical Resume Schema

This is the foundational data contract of the entire system. Every engine reads from and writes to this schema. It lives in `shared/models/resume.py` as a Pydantic model.

```python
# shared/models/resume.py

class ExtractedField(BaseModel):
    value: Any
    confidence: float          # 0.0 – 1.0
    source: Literal["regex", "NER", "LLM", "rule", "embedding"]

class PersonalInfo(BaseModel):
    name: ExtractedField
    email: ExtractedField
    phone: ExtractedField
    location: ExtractedField
    linkedin: Optional[ExtractedField]
    github: Optional[ExtractedField]

class Skill(BaseModel):
    raw: str                   # Exactly as found in the resume
    normalized: str            # Canonical name (from ESCO/O*NET)
    taxonomy_id: Optional[str] # e.g., "ESCO:S4.3.2"
    category: Literal["technical", "soft", "tool", "domain"]
    confidence: float

class ExperienceBullet(BaseModel):
    text: str
    has_metric: bool           # "increased revenue by 20%"
    has_action_verb: bool      # Starts with strong action verb
    has_specificity: bool      # Contains tech, team size, timeline
    star_score: float          # 0.0 – 1.0 STAR format compliance
    weakness_flags: List[str]  # e.g., ["vague_impact", "weak_verb"]

class Experience(BaseModel):
    company: ExtractedField
    role: ExtractedField
    duration: ExtractedField
    bullets: List[ExperienceBullet]

class Education(BaseModel):
    institution: ExtractedField
    degree: ExtractedField
    field: ExtractedField
    year: Optional[ExtractedField]

class ResumeSchema(BaseModel):
    raw_text: str
    parse_method: Literal["pdf", "docx", "ocr"]
    personal_info: PersonalInfo
    summary: Optional[ExtractedField]
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    certifications: List[ExtractedField]
    projects: List[dict]
    languages: List[ExtractedField]
    parsing_warnings: List[str]
    schema_version: str = "1.0"
```

**Every engine is required to preserve this schema** and only add fields — never mutate existing ones.

---

# MCP Tool Surface

The Model Context Protocol server exposes these tools to AI assistants. Defining them early shapes the shared service layer.

| Tool Name | Input | Output | Engine Used |
|---|---|---|---|
| `parse_resume` | PDF/DOCX bytes or text | `ResumeSchema` JSON | `ResumeParserEngine` |
| `score_resume` | `ResumeSchema` + JD text | `ATSReport` JSON | `ATSEngine` |
| `extract_skills` | Raw text | `List[Skill]` JSON | `SkillNormalizerEngine` |
| `rewrite_bullet` | Bullet text + context | Rewritten bullet | `LLMRewriteEngine` |
| `detect_weak_bullets` | `ResumeSchema` | `BulletReport` JSON | `BulletScorerEngine` |
| `compare_resumes` | Resume A + Resume B + JD | `ComparisonReport` JSON | `ATSEngine` |
| `get_skill_trends` | `List[Skill]` | Market demand report | `SkillTrendEngine` |
| `generate_interview_prep` | `ResumeSchema` + JD text | Questions + STAR hints | `LLMRewriteEngine` |

---

# Shared Service Architecture

The `shared/` package is the canonical Python library imported by **both** the FastAPI backend and the MCP server. Neither the backend nor the MCP server contain business logic — they are thin transport layers.

```
shared/
├── __init__.py
├── config.py                  # Settings via pydantic-settings
├── models/
│   ├── resume.py              # ResumeSchema (canonical)
│   ├── job.py                 # JobDescriptionSchema
│   └── reports.py             # ATSReport, BulletReport, ComparisonReport
├── engines/
│   ├── parser.py              # ResumeParserEngine
│   ├── job_parser.py          # JobDescriptionEngine
│   ├── skill_extractor.py     # SkillNormalizerEngine
│   ├── embedder.py            # EmbeddingEngine
│   ├── ats.py                 # ATSEngine
│   ├── bullet_scorer.py       # BulletScorerEngine
│   ├── recommender.py         # RecommendationEngine
│   └── llm.py                 # LLMRewriteEngine
├── prompts/
│   └── registry.py            # Prompt version manager
└── utils/
    ├── cache.py               # Document hash → embedding cache
    ├── text.py                # Normalization utilities
    └── logging.py             # Structured logger
```

---

# Pipeline Configuration Pattern

The analysis pipeline is configured via a YAML file, not hardcoded. This allows reconfiguration without code changes — a real production AI engineering pattern.

```yaml
# shared/pipeline_config.yaml
pipeline:
  - step: parse
    engine: ResumeParserEngine
    config:
      ocr_fallback: true
      encoding_repair: true

  - step: normalize_skills
    engine: SkillNormalizerEngine
    config:
      use_esco: true
      use_onet: true
      confidence_threshold: 0.75
      fallback: embedding_match

  - step: embed
    engine: EmbeddingEngine
    config:
      model: "all-MiniLM-L6-v2"
      cache_enabled: true
      cache_backend: "local_json"

  - step: score_bullets
    engine: BulletScorerEngine
    config:
      score_metrics: true
      score_star: true
      score_action_verbs: true

  - step: ats_score
    engine: ATSEngine
    config:
      weights:
        skills: 0.40
        experience: 0.30
        education: 0.20
        format: 0.10
      ats_simulation_modes: ["keyword_only", "nlp_hybrid", "semantic"]
```

---

# Feature Definitions

## Core Features

### 1. Explainable ATS Scoring
No mystery scores. Every point in the ATS score is traceable to a specific criterion with a weight and a reason.

```
ATS Score: 74/100
  ├── Skills Match:        28/40  (Python ✅, FastAPI ✅, Kubernetes ❌, Terraform ❌)
  ├── Experience Match:    22/30  (4.5 yrs matched, Senior-level detected)
  ├── Education Match:     16/20  (B.Tech CS — matched requirement)
  └── Format & Keywords:   8/10   (Missing: quantified impact in 3 bullets)
```

### 2. ATS Simulation Mode
The same resume scored against three different ATS parsing models to show how optimization differs:

| ATS Mode | Description | Teaches |
|---|---|---|
| **Keyword-Only** | Exact keyword matching (legacy ATS) | Importance of exact terms |
| **NLP Hybrid** | Synonyms + semantic expansion | Vocabulary normalization |
| **Semantic** | Embedding similarity (modern ATS) | Why embeddings matter |

### 3. Weak Bullet Detector
Each resume bullet is scored before LLM rewrite is considered:

| Signal | Check | Example |
|---|---|---|
| **Quantified Impact** | Has metric/number | "increased throughput by 40%" ✅ |
| **Action Verb** | Starts with strong verb | "Developed" vs "Helped with" |
| **Specificity** | Contains tech/scale/scope | Stack, team size, timeline |
| **STAR Compliance** | Situation-Task-Action-Result | 0.0 – 1.0 score |

LLM rewrite is only triggered for bullets that fail ≥ 2 checks. Not everything goes to the LLM.

### 4. Confidence Dashboard
Every extracted field is shown with its confidence and extraction source. Low-confidence items are flagged for user review.

| Field | Value | Confidence | Source |
|---|---|---|---|
| Email | john@example.com | 99% | Regex |
| Company | Google | 91% | NER |
| Skill: React | React (ESCO: S4.1) | 87% | Embedding Match |
| Degree | B.Tech | 74% | Rule + NER |
| Duration | 2021–2023 | 68% | Regex + Context |

### 5. Skill Normalization Engine
Three-tier normalization with fallback chain:

```
Raw skill text
  ↓ Tier 1: Exact match → ESCO / O*NET taxonomy
  ↓ Tier 2: Fuzzy match (rapidfuzz, threshold 0.85)
  ↓ Tier 3: Embedding similarity (cosine > 0.80)
  ↓ Output: { raw, normalized, taxonomy_id, confidence }
```

### 6. Embedding Space Visualizer
UMAP/t-SNE projection of resume and JD embeddings into 2D space:
- Where your resume sits relative to the target JD cluster
- Which skills, when added, would move your resume closer
- Competitor resume positions (from dataset)

### 7. Resume Diff Mode
Upload two versions of your resume:
- Bullet-level diff view (what changed)
- Which version scores higher for a given JD and by how much
- Which specific changes drove the score delta

### 8. Skill Trend Radar
For every skill on the resume:
- Current market demand (Stack Overflow Survey + ESCO)
- Year-over-year growth or decline trend
- Top 3 related skills worth adding

### 9. Prompt Observatory (Dev Mode)
A dedicated UI panel showing every LLM call made during a session:
- Exact prompt template used (with version)
- Token count, latency, model used
- Raw vs. parsed response
- Cost estimate per call

Like browser DevTools, but for AI engineering.

### 10. Interview Prep Connector
Generated from the JD and parsed resume:
- Top 5 technical interview questions based on JD requirements
- Top 3 behavioral questions based on company culture signals
- Suggested STAR story framework for each experience bullet

---

# Prompt Versioning Strategy

All prompts are versioned. Prompt drift is a real production risk.

```
prompts/
├── registry.json              # name → version → file mapping
├── v1/
│   ├── bullet_rewrite.txt
│   ├── career_advisor.txt
│   └── skill_gap.txt
└── v2/
    ├── bullet_rewrite.txt     # Improved version
    └── skill_gap.txt
```

`registry.json` example:
```json
{
  "bullet_rewrite": { "active": "v2", "tested_models": ["gemini-2.5-flash", "llama-3.1-70b"] },
  "career_advisor": { "active": "v1", "tested_models": ["gemini-2.5-pro"] }
}
```

Regression tests run against each prompt version on a labeled golden dataset before promotion.

---

# Caching Strategy

Embedding generation is expensive. All computed embeddings are cached by document hash.

```
Cache Key: SHA-256(raw_text + model_name)
Cache Value: numpy embedding vector
Cache Backend: local JSON (dev) → Redis (prod)
Cache TTL: 7 days
```

This also applies to parsed resume JSON — if the document hash hasn't changed, skip re-parsing.

---

# Feedback Loop

A simple human-in-the-loop feedback system:

- Thumbs up/down on each recommendation
- Optional text correction of extracted fields
- Stored in local SQLite as a correction dataset
- Used for prompt improvement and extractor calibration in later phases

---

# Evaluation Framework

The `evaluation/` directory is a structured benchmark suite, not just ad-hoc notebooks.

```
evaluation/
├── datasets/
│   ├── resume_ner_gold.json       # Labeled NER ground truth
│   ├── ats_score_gold.json        # Human-scored resume/JD pairs
│   └── bullet_quality_gold.json   # Human-labeled bullet quality
├── benchmarks/
│   ├── parser_bench.py            # Precision/Recall on extraction
│   ├── ner_bench.py               # NER entity matching
│   ├── ats_bench.py               # Score correlation with human judges
│   └── bullet_bench.py            # Weak bullet detection accuracy
├── reports/                       # Auto-generated HTML reports per run
└── run_all.py                     # Single command to run full suite
```

---

# Notebook Structure — 3 Parts

The 70-notebook learning path is divided into three tightly scoped parts. Each part has a clear input, output, and purpose.

---

## PART I — Foundations & NLP Mastery
**Goal:** Master the tools and algorithms needed to process text at an engineering level.
**Output:** A reusable NLP utility library and deep understanding of text representation.
**Notebooks:** 00 – 25

---

### Block A: Environment & Python Tooling (Notebooks 00–03)

| # | Notebook | Key Concepts | Dataset |
|---|---|---|---|
| 00 | Environment Setup | Conda, venv, Jupyter, VSCode, Git, pyproject.toml | — |
| 01 | Python Engineering Refresher | OOP, dataclasses, type hints, generators, file I/O | — |
| 02 | Data Tooling: Pandas & NumPy | DataFrames, vectorized ops, cleaning, analysis | Sample CSV |
| 03 | Regex Mastery for Resumes | Email, phone, dates, URLs, GPA, skills, durations | Resume Dataset |

---

### Block B: NLP Pipeline (Notebooks 04–12)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 04 | NLP Introduction | Corpus, vocabulary, tokens, pipeline anatomy | — |
| 05 | Tokenization | Word, sentence, subword tokenizers; Unicode edge cases | NLTK, spaCy |
| 06 | Text Normalization | Lowercase, Unicode fix, OCR artifact repair, ligatures | unicodedata |
| 07 | Stop Words & Filtering | Stopword removal; when NOT to remove stops in resumes | NLTK |
| 08 | Lemmatization | spaCy vs NLTK; morphological analysis; resume impact | spaCy |
| 09 | Stemming | Porter, Snowball; compare with lemmatization | NLTK |
| 10 | POS Tagging | Parts of speech; identifying action verbs in bullets | spaCy |
| 11 | Dependency Parsing | Dependency trees; extracting subject-verb-object triples | spaCy |
| 12 | Named Entity Recognition | PERSON, ORG, DATE, GPE; training custom NER for skills | spaCy |

---

### Block C: Text Representation (Notebooks 13–20)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 13 | Chunking & Phrase Extraction | Noun chunks, verb phrases, skill phrase detection | spaCy |
| 14 | Keyword Extraction | TF-IDF keywords, KeyBERT, YAKE; compare all three | KeyBERT |
| 15 | Bag of Words | CountVectorizer; vocabulary size vs. sparsity tradeoff | sklearn |
| 16 | TF-IDF Deep Dive | IDF weighting; query-document relevance; cosine similarity | sklearn |
| 17 | N-Grams | Unigrams, bigrams, trigrams; n-gram TF-IDF for skills | sklearn |
| 18 | Cosine Similarity | Dot product, magnitude, similarity metrics; benchmarks | numpy |
| 19 | Word2Vec | Skip-gram, CBOW, negative sampling; analogy tasks | gensim |
| 20 | FastText | Subword embeddings; handles typos and rare words | gensim |

---

### Block D: Semantic Embeddings (Notebooks 21–25)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 21 | GloVe | Co-occurrence matrix; pre-trained embeddings; limitations | gensim |
| 22 | Sentence Transformers | BERT sentence embeddings; bi-encoder architecture | sentence-transformers |
| 23 | Embedding Benchmarks | Compare Word2Vec vs GloVe vs SentTrans on resume text | all above |
| 24 | Zero-Shot Classification | Classify text without labels; NLI-based classification | transformers |
| 25 | Error Handling in NLP | Malformed resumes, encoding errors, empty sections, fallbacks | — |

---

## PART II — Resume & Job Intelligence
**Goal:** Build every extraction, matching, and scoring engine that powers the platform.
**Output:** A complete, confidence-scored pipeline from raw document to `ATSReport`.
**Notebooks:** 26 – 49

---

### Block E: Document Parsing (Notebooks 26–31)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 26 | PDF Parsing | pdfplumber, PyMuPDF; layout preservation; multi-column | pdfplumber |
| 27 | DOCX Parsing | python-docx; paragraph styles; table extraction | python-docx |
| 28 | OCR Basics | Tesseract, EasyOCR; image-to-text; quality scoring | pytesseract |
| 29 | Text Normalization for Resumes | Ligatures, bullet symbols, smart quotes, hyphen variants | unicodedata |
| 30 | Language Detection | langdetect; basic multi-lingual resume support | langdetect |
| 31 | Parsing Error Handling | Corrupt files, empty sections, encoding fallback strategies | — |

---

### Block F: Resume Information Extraction (Notebooks 32–39)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 32 | Resume Section Detection | Rule-based + ML section classifier; heading patterns | spaCy, regex |
| 33 | Skill Extraction (Rules) | Regex + rule-based skill list matching | ESCO, O*NET |
| 34 | Skill Normalization Engine | Exact → Fuzzy → Embedding fallback chain; confidence scoring | rapidfuzz |
| 35 | Education Parsing | Degree, institution, year extraction; university normalization | spaCy, regex |
| 36 | Experience Parsing | Company, role, duration; NER + regex hybrid | spaCy |
| 37 | Bullet Parsing & STAR Scoring | Action verb detection, metric detection, STAR compliance | POS + rules |
| 38 | Project Extraction | Project names, tech stacks, outcomes | NER + regex |
| 39 | Resume JSON Schema — Live Build | Assemble `ResumeSchema` Pydantic model from all engines | Pydantic |

---

### Block G: Job Description Intelligence (Notebooks 40–45)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 40 | JD Parsing | Structure detection; responsibilities vs. requirements | spaCy |
| 41 | JD Skill Extraction | Required vs. preferred skills; experience level signals | NER + rules |
| 42 | Responsibility Detection | Action phrase extraction; seniority signals | POS + rules |
| 43 | Qualification Detection | Degree requirements, year requirements, cert requirements | regex + NER |
| 44 | Keyword Ranking | TF-IDF + KeyBERT on JD; top-k keywords for matching | KeyBERT |
| 45 | Requirement Classification | Must-have vs. nice-to-have classification; zero-shot | transformers |

---

### Block H: Semantic Matching & Search (Notebooks 46–49)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 46 | Resume vs JD Matching | Cosine similarity; section-level vs. document-level matching | sentence-transformers |
| 47 | FAISS Vector Search | Index types (Flat, IVF, HNSW); approximate nearest neighbor | faiss |
| 48 | ChromaDB | Persistent vector store; metadata filtering; hybrid search | chromadb |
| 49 | Embedding Evaluation & Benchmark | Which embedding model works best for resume domain? | all models |

---

### Block I: ATS Scoring Engine (Notebooks 50–54)

| # | Notebook | Key Concepts | Library |
|---|---|---|---|
| 50 | ATS Rule Design | Weighted criteria; skills, experience, education, format | — |
| 51 | Explainable Scoring | Score decomposition; per-criterion breakdown with reasons | — |
| 52 | ATS Simulation Mode | Keyword-only vs NLP hybrid vs semantic; compare results | all above |
| 53 | Skill Gap Analysis | Missing vs. present skills; gap severity scoring | — |
| 54 | Resume Ranking | Score N resumes against one JD; ranking algorithm | — |

---

## PART III — LLM Engineering & Production (Deferred)

> **Status:** Deferred. LLM/prompt engineering notebooks (Blocks J, K, L) are not part of the current scope. The architecture remains designed to accommodate them in the future — the `shared/` package, MCP tool surface, and modular engine pattern are all LLM-ready.

---

# Part Summary

| Part | Notebooks | Purpose | Output |
|---|---|---|---|
| **Part I — Foundations & NLP Mastery** | 00–25 (26 notebooks) | Master NLP algorithms from scratch | NLP utility library |
| **Part II — Resume & Job Intelligence** | 26–54 (29 notebooks) | Build every extraction and scoring engine | Tested engine pipeline |

---

# Project Structure

```text
AI-Resume-Intelligence/
│
├── README.md
├── PLAN.md
├── ROADMAP.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── docs/
│   ├── architecture/          # System design docs, engine contracts
│   ├── api/                   # OpenAPI specs, endpoint docs
│   ├── deployment/            # Cloud Run, Docker, CI/CD guides
│   ├── research/              # NLP research notes and comparisons
│   ├── diagrams/              # Architecture and pipeline diagrams
│   ├── references/            # External references and papers
│   └── images/
│
├── notebooks/
│   ├── part1_foundations/     # Notebooks 00–25
│   ├── part2_intelligence/    # Notebooks 26–54
│   ├── part3_production/      # Notebooks 55–75
│   └── assets/                # Shared notebook assets, sample data
│
├── shared/                    # Canonical Python package (backend + MCP both import this)
│   ├── __init__.py
│   ├── config.py
│   ├── pipeline_config.yaml
│   ├── models/
│   │   ├── resume.py          # ResumeSchema (Pydantic)
│   │   ├── job.py             # JobDescriptionSchema
│   │   └── reports.py         # ATSReport, BulletReport, ComparisonReport
│   ├── engines/
│   │   ├── parser.py
│   │   ├── job_parser.py
│   │   ├── skill_extractor.py
│   │   ├── embedder.py
│   │   ├── ats.py
│   │   ├── bullet_scorer.py
│   │   ├── recommender.py
│   │   └── llm.py
│   ├── prompts/
│   │   ├── registry.json
│   │   ├── v1/
│   │   └── v2/
│   └── utils/
│       ├── cache.py
│       ├── text.py
│       └── logging.py
│
├── backend/                   # FastAPI — thin transport layer over shared/
│   ├── main.py
│   ├── routers/
│   ├── middleware/
│   ├── dependencies.py
│   └── requirements.txt
│
├── frontend/                  # React + TypeScript + TailwindCSS
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   ├── resume-upload/
│   │   │   ├── ats-report/
│   │   │   ├── bullet-scorer/
│   │   │   ├── embedding-viz/     # UMAP visualizer
│   │   │   ├── skill-radar/       # Skill trend radar
│   │   │   ├── prompt-observatory/ # Dev mode LLM inspector
│   │   │   └── resume-diff/       # Resume version comparator
│   │   ├── hooks/
│   │   └── lib/
│   ├── package.json
│   └── tailwind.config.ts
│
├── mcp/                       # MCP Server — thin transport layer over shared/
│   ├── server.py
│   ├── tools/
│   │   ├── parse_resume.py
│   │   ├── score_resume.py
│   │   ├── extract_skills.py
│   │   ├── rewrite_bullet.py
│   │   ├── detect_weak_bullets.py
│   │   ├── compare_resumes.py
│   │   ├── get_skill_trends.py
│   │   └── generate_interview_prep.py
│   └── requirements.txt
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   ├── external/
│   ├── resume/
│   ├── jobs/
│   ├── skills/                # ESCO, O*NET, action verbs
│   ├── universities/
│   ├── companies/
│   ├── certifications/
│   └── locations/
│
├── evaluation/
│   ├── datasets/              # Labeled ground truth
│   ├── benchmarks/
│   │   ├── parser_bench.py
│   │   ├── ner_bench.py
│   │   ├── ats_bench.py
│   │   └── bullet_bench.py
│   ├── reports/
│   └── run_all.py
│
├── experiments/               # Ad-hoc research notebooks
├── prompts/                   # Standalone prompt library (mirror of shared/prompts)
├── deployment/
│   ├── cloud_run/
│   └── cloudflare/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.mcp
│   └── docker-compose.yml
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── scripts/
    ├── setup_dirs.ps1
    ├── download_datasets.py
    └── run_evaluation.py
```

---

# Dataset Strategy

| Priority | Dataset | Purpose | Used In |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | Resume Dataset (Kaggle) | Core resume parsing | Parts I & II |
| ⭐⭐⭐⭐⭐ | Job Description Dataset | JD parsing & matching | Part II |
| ⭐⭐⭐⭐⭐ | ESCO Skills Taxonomy | Skill normalization | Part II |
| ⭐⭐⭐⭐⭐ | O*NET Database | Occupation & competency mapping | Part II |
| ⭐⭐⭐⭐ | Resume NER Dataset (HuggingFace) | NER training & evaluation | Parts I & II |
| ⭐⭐⭐⭐ | Stack Overflow Survey | Skill trend radar | Part II |
| ⭐⭐⭐ | World Universities CSV | Education normalization | Part II |
| ⭐⭐⭐ | Countries & Cities DB | Location parsing | Part II |
| ⭐⭐⭐ | Fortune 1000 / Company Lists | Company normalization | Part II |
| ⭐⭐ | AWS/GCP/Azure Certification Lists | Certification recognition | Part II |
| ⭐⭐ | Harvard Action Verbs | Bullet verb scoring | Part II |

---

# Development Stages

```
Stage 0 — Research & Planning     ← CURRENT (complete)
         ↓
Stage 1 — Part I Notebooks        ← NLP foundations (Notebooks 00–25)
         ↓
Stage 2 — Part II Notebooks       ← Intelligence engines (Notebooks 26–54)
         ↓
Version 1.0
```

---

# Success Criteria

## Learning
- Complete all 76 planned notebooks.
- Be able to explain every algorithm, every design decision, every trade-off.
- Understand why each component was built the way it was.

## Engineering
- Every engine is independently tested.
- `ResumeSchema` flows correctly end-to-end through the full pipeline.
- FastAPI backend and MCP server are thin wrappers over shared engines.
- Prompt versions are tracked and regression-tested.

## Product
The application allows users to:
- Upload resumes (PDF, DOCX) and job descriptions.
- See a fully explainable ATS score with per-criterion breakdown.
- View each extraction with its confidence score and source.
- Compare their resume against three ATS simulation modes.
- Detect and selectively rewrite weak bullets.
- Visualize resume-to-JD semantic distance.
- Compare two resume versions and see which scores higher and why.
- See skill market trends for every skill on their resume.
- Interact with the platform via any MCP-compatible AI assistant.

---

# Guiding Principles

1. Understand before implementing.
2. Define contracts (schemas, tool surfaces) before writing engines.
3. Every extraction must carry a confidence score and source.
4. LLMs are selective — trigger them only when rule-based systems are insufficient.
5. The `shared/` package is the source of truth. Backend and MCP are transports.
6. Prompts are code — version them, test them, and never silently change them.
7. Measure and benchmark every major engine before moving on.
8. Documentation is part of the product.
9. Build features that demonstrate engineering judgment, not just AI capability.

---

# Long-Term Vision (Post v1.0)

- Cover Letter Intelligence
- LinkedIn Profile Analysis
- Portfolio Code Review
- Mock Interview with AI feedback
- Career Roadmap Generation
- Skill Learning Recommendations
- Multi-language Resume Support
- Browser Extension
- Mobile Companion Application

---

## Closing Statement

This project is a comprehensive exploration of modern AI engineering. Every notebook, engine, API, and interface is designed to deepen technical understanding while producing a polished, production-quality application that showcases end-to-end engineering capability. The architecture — canonical schemas, modular engines, thin transports, versioned prompts, confidence scoring, and a shared service layer — reflects how real production AI systems are built. This `PLAN.md` is the single source of truth for every design and implementation decision.
