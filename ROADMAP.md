# AI Resume Intelligence Platform — Roadmap

> Live document. Updated as stages complete.

---

## Stage Status

| Stage | Focus | Status |
|---|---|---|
| Stage 0 | Research & Planning | ✅ Complete |
| Stage 1 | Part I Notebooks — Foundations & NLP | 🔲 Next |
| Stage 2 | Part II Notebooks — Resume & Job Intelligence | 🔲 Planned |
| Stage 3 | Part III Notebooks — LLM Engineering & Production | 🔲 Planned |
| Stage 4 | Application Build (Backend + Frontend) | 🔲 Planned |
| Stage 5 | MCP Server + Docker + Cloud Deployment | 🔲 Planned |

---

## Stage 0 — Research & Planning ✅

- [x] Define executive objectives, success criteria, and non-goals.
- [x] Define canonical `ResumeSchema` (Pydantic model contract).
- [x] Define MCP tool surface (8 tools with typed contracts).
- [x] Define shared service architecture (`shared/` package).
- [x] Define pipeline configuration pattern (YAML-driven).
- [x] Define all 76 notebooks across 3 parts.
- [x] Establish feature definitions (10 core features).
- [x] Establish project directory structure with `.gitkeep` files.
- [x] Create `README.md`, `PLAN.md`, `CHANGELOG.md`, `.gitignore`, `.env.example`, `LICENSE`.
- [x] Initialize Git repository, first commit.

---

## Stage 1 — Part I: Foundations & NLP Mastery 🔲

**Notebooks 00–25 · 4 Blocks**

### Block A: Environment & Tooling (00–03)
- [ ] 00 — Environment Setup
- [ ] 01 — Python Engineering Refresher
- [ ] 02 — Pandas & NumPy
- [ ] 03 — Regex Mastery

### Block B: NLP Pipeline (04–12)
- [ ] 04 — NLP Introduction
- [ ] 05 — Tokenization
- [ ] 06 — Text Normalization
- [ ] 07 — Stop Words
- [ ] 08 — Lemmatization
- [ ] 09 — Stemming
- [ ] 10 — POS Tagging
- [ ] 11 — Dependency Parsing
- [ ] 12 — Named Entity Recognition

### Block C: Text Representation (13–20)
- [ ] 13 — Chunking & Phrase Extraction
- [ ] 14 — Keyword Extraction
- [ ] 15 — Bag of Words
- [ ] 16 — TF-IDF Deep Dive
- [ ] 17 — N-Grams
- [ ] 18 — Cosine Similarity
- [ ] 19 — Word2Vec
- [ ] 20 — FastText

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

## Stage 3 — Part III: LLM Engineering & Production 🔲

**Notebooks 55–75 · 3 Blocks**

### Block J: LLM Engineering (55–63)
- [ ] 55 — OpenRouter Setup
- [ ] 56 — Prompt Engineering
- [ ] 57 — Prompt Versioning
- [ ] 58 — JSON Structured Output
- [ ] 59 — Function / Tool Calling
- [ ] 60 — Weak Bullet Rewriter
- [ ] 61 — STAR Bullet Generator
- [ ] 62 — Career Advisor
- [ ] 63 — Model Comparison

### Block K: Evaluation (64–69)
- [ ] 64 — Precision & Recall for NLP
- [ ] 65 — F1 Score & Confusion Matrix
- [ ] 66 — Hallucination Testing
- [ ] 67 — A/B Prompt Testing
- [ ] 68 — Human Evaluation Protocol
- [ ] 69 — Latency Profiling

### Block L: Production Pipeline (70–75)
- [ ] 70 — End-to-End Pipeline
- [ ] 71 — Pipeline Config Pattern
- [ ] 72 — Caching Layer
- [ ] 73 — Feedback Loop
- [ ] 74 — Modularization into `shared/`
- [ ] 75 — API Prototype

**Deliverable:** Deployable `shared/` package with test coverage and API prototype.

---

## Stage 4 — Application Build 🔲

### Backend (FastAPI)
- [ ] Project scaffold (`main.py`, routers, middleware, DI)
- [ ] Resume upload endpoint (PDF, DOCX)
- [ ] Analysis pipeline endpoint (returns `ATSReport`)
- [ ] Resume comparison endpoint
- [ ] Bullet rewrite endpoint
- [ ] Auth (JWT session tokens)
- [ ] Rate limiting on analysis endpoints
- [ ] Structured logging middleware
- [ ] OpenAPI docs

### Frontend (React + TypeScript + Tailwind)
- [ ] Project scaffold (Vite + React + TypeScript + Tailwind)
- [ ] Resume & JD upload UI
- [ ] ATS Score Dashboard (explainable breakdown)
- [ ] Confidence Dashboard (extraction table with confidence scores)
- [ ] Bullet Scorer UI (per-bullet STAR scoring)
- [ ] Embedding Space Visualizer (UMAP 2D projection)
- [ ] Skill Trend Radar (market demand chart)
- [ ] Resume Diff Mode (version comparison view)
- [ ] Prompt Observatory (dev mode LLM call inspector)
- [ ] Interview Prep Panel

**Deliverable:** Fully functional AI Resume Intelligence Platform.

---

## Stage 5 — MCP Server + Deployment 🔲

### MCP Server
- [ ] Scaffold `mcp/server.py`
- [ ] Implement all 8 MCP tools
- [ ] Test with Claude Desktop / Cursor
- [ ] Document tool schemas

### Docker
- [ ] `Dockerfile.backend`
- [ ] `Dockerfile.mcp`
- [ ] `docker-compose.yml` (backend + mcp + optional vector DB)

### Cloud Deployment
- [ ] Backend → Google Cloud Run
- [ ] Frontend → Cloudflare Pages
- [ ] GitHub Actions CI/CD pipeline
- [ ] Environment secrets management
- [ ] Basic monitoring (Cloud Logging)

**Deliverable:** Production platform accessible via web app and MCP-compatible AI assistants.

---

## Version 1.0 Milestone

Version 1.0 is reached when:
- All 76 notebooks are complete and documented.
- Full pipeline runs end-to-end producing a valid `ATSReport`.
- All 10 features are working in the web UI.
- All 8 MCP tools are working and tested.
- Backend is deployed to Cloud Run.
- Frontend is deployed to Cloudflare Pages.
- CI/CD is active.
