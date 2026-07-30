# AI Resume Intelligence Platform — Roadmap

> Live document. Last updated: 2026-07-30 13:04:37+05:30 (1:04 PM IST).

---

## Stage Status

| Stage | Focus | Status | Last Updated |
|-------|-------|--------|--------------|
| Stage 0 | Research & Planning | ✅ Complete | 2026-07-30 |
| Stage 1 | Part I Notebooks — Foundations & NLP (00–25) | 🔲 In Progress (Blocks A-C complete) | 2026-07-30 |
| Stage 2 | Part II Notebooks — Resume & Job Intelligence (26–54) | 🔲 Planned | - |

---

## Stage 0 — Research & Planning ✅

- [x] Define executive objectives, success criteria, and non-goals.
- [x] Define canonical `ResumeSchema` (Pydantic model contract).
- [x] Define MCP tool surface (8 tools with typed contracts).
- [x] Define shared service architecture (`shared/` package).
- [x] Define pipeline configuration pattern (YAML-driven).
- [x] Define all notebooks across 2 parts (55 total).
- [x] Establish feature definitions (10 core features).
- [x] Establish project directory structure with `.gitkeep` files.
- [x] Create `README.md`, `PLAN.md`, `CHANGELOG.md`, `.gitignore`, `.env.example`, `LICENSE`.
- [x] Initialize Git repository, first commit.

---

## Stage 1 — Part I: Foundations & NLP Mastery 🔲

**Notebooks 00–25 · 4 Blocks**

### Block A: Environment & Tooling (00–03) ✅
- [x] 00 — Environment Setup
- [x] 01 — Python Engineering Refresher
- [x] 02 — Pandas & NumPy
- [x] 03 — Regex Mastery

### Block B: NLP Pipeline (04–12) ✅
- [x] 04 — NLP Introduction
- [x] 05 — Tokenization
- [x] 06 — Text Normalization
- [x] 07 — Stop Words
- [x] 08 — Lemmatization
- [x] 09 — Stemming
- [x] 10 — POS Tagging
- [x] 11 — Dependency Parsing
- [x] 12 — Named Entity Recognition

### Block C: Text Representation (13–20) ✅
- [x] 13 — Chunking & Phrase Extraction
- [x] 14 — Keyword Extraction
- [x] 15 — Bag of Words
- [x] 16 — TF-IDF Deep Dive
- [x] 17 — N-Grams
- [x] 18 — Cosine Similarity
- [x] 19 — Word2Vec
- [x] 20 — FastText

### Block D: Semantic Embeddings (21–25)
- [ ] 21 — GloVe
- [ ] 22 — Sentence Transformers
- [ ] 23 — Embedding Benchmarks
- [ ] 24 — Zero-Shot Classification
- [ ] 25 — Error Handling in NLP

**Deliverable:** Reusable NLP utility library + deep conceptual understanding.

---

## Stage 2 — Part II: Resume & Job Intelligence 🔲

**Notebooks 26–54 · 5 Blocks**

### Block E: Document Parsing (26–31)
- [ ] 26 — PDF Parsing
- [ ] 27 — DOCX Parsing
- [ ] 28 — OCR Basics
- [ ] 29 — Text Normalization for Resumes
- [ ] 30 — Language Detection
- [ ] 31 — Parsing Error Handling

### Block F: Resume Information Extraction (32–39)
- [ ] 32 — Resume Section Detection
- [ ] 33 — Skill Extraction (Rules)
- [ ] 34 — Skill Normalization Engine (ESCO + fuzzy + embedding)
- [ ] 35 — Education Parsing
- [ ] 36 — Experience Parsing
- [ ] 37 — Bullet Parsing & STAR Scoring
- [ ] 38 — Project Extraction
- [ ] 39 — Resume JSON Schema — Live Build

### Block G: Job Description Intelligence (40–45)
- [ ] 40 — JD Parsing
- [ ] 41 — JD Skill Extraction
- [ ] 42 — Responsibility Detection
- [ ] 43 — Qualification Detection
- [ ] 44 — Keyword Ranking
- [ ] 45 — Requirement Classification

### Block H: Semantic Matching (46–49)
- [ ] 46 — Resume vs JD Matching
- [ ] 47 — FAISS Vector Search
- [ ] 48 — ChromaDB
- [ ] 49 — Embedding Evaluation & Benchmark

### Block I: ATS Scoring Engine (50–54)
- [ ] 50 — ATS Rule Design
- [ ] 51 — Explainable Scoring
- [ ] 52 — ATS Simulation Mode (3 modes)
- [ ] 53 — Skill Gap Analysis
- [ ] 54 — Resume Ranking

**Deliverable:** Tested extraction and scoring pipeline producing a valid `ATSReport`.

---

## Version 1.0 Milestone

Version 1.0 is reached when:
- All 55 notebooks are complete and documented.
- Full pipeline runs end-to-end producing a valid `ATSReport`.
- All 10 features are working in the web UI.
- All 8 MCP tools are working and tested.
- Backend is deployed to Cloud Run.
- Frontend is deployed to Cloudflare Pages.
- CI/CD is active.
