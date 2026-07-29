# AI Resume Intelligence Platform

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-cyan.svg)](https://react.dev/)
[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-orange.svg)](https://modelcontextprotocol.io/)

A production-oriented AI application designed to demonstrate the complete lifecycle of modern AI engineering—from Natural Language Processing (NLP) research and experimentation to deployment and integration with AI assistants via the Model Context Protocol (MCP).

---

## 🌟 Features Overview

- **Explainable ATS Scoring Engine**: No black-box scores. Detailed breakdown of matching criteria, section completeness, education/experience mapping, and skill gap analysis.
- **Advanced Skill Extraction**: Rule-based, statistical, and Named Entity Recognition (NER) approaches for identifying skills in resumes and job descriptions.
- **Semantic Representation**: Multi-tiered text representation from CountVectorizer/TF-IDF to Sentence Transformers and vector databases (FAISS, ChromaDB).
- **LLM-Powered Insights**: AI-assisted career advisory, STAR-method resume bullet rewriting, and automated improvement recommendations via OpenRouter.
- **Model Context Protocol (MCP) Integration**: Access the core platform capabilities directly from any MCP-compatible AI assistant (like Claude, Gemini, or Cursor).
- **Interactive UI**: Sleek, modern dashboard built with React, TypeScript, and TailwindCSS for uploading resumes, job descriptions, and visualizing matching metrics.

---

## 📁 Repository Structure

```text
AI-Resume-Intelligence/
├── backend/            # FastAPI API Backend
├── frontend/           # React/TypeScript/Tailwind Frontend
├── mcp/                # Model Context Protocol Server
├── notebooks/          # Phase-by-phase Jupyter Notebooks (00 to 15)
├── datasets/           # Raw, processed, and external dataset taxonomy
├── docs/               # Architecture, API design, and deployment documentation
├── experiments/        # Research and ad-hoc prototyping
├── prompts/            # Versioned and structured LLM prompt templates
├── deployment/         # Cloud run configs, CD configurations
├── docker/             # Dockerfiles and docker-compose setups
├── evaluation/         # Benchmark suites, precision/recall calculators
├── tests/              # Pytest backend and Jest/Playwright frontend tests
└── scripts/            # Helper scripts and automation utilities
```

See [PLAN.md](file:///d:/Projects/ResAnalyze/PLAN.md) for the detailed file structure and Phase 0-9 Jupyter Notebook learning roadmap.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: v3.10 or higher
- **Node.js**: v18 or higher (for frontend development)
- **Git**
- **Conda** (Optional, recommended for virtual environments)

### 2. Environment Setup

Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```

To configure your Python virtual environment:
```bash
# Create environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install requirements (once requirements.txt is created)
pip install -r backend/requirements.txt
```

---

## 📚 Learning Path

The learning path progresses through 10 distinct phases in the `notebooks/` directory:
1. **Phase 0 — Foundations**: Environment, Python, Pandas, Regex
2. **Phase 1 — NLP Fundamentals**: Tokenization, POS, NER, spaCy
3. **Phase 2 — Text Representation**: Bag of Words, TF-IDF, GloVe, Embeddings
4. **Phase 3 — Resume Intelligence**: Parsing documents (PDF/DOCX), Section Detection, JSON Schema
5. **Phase 4 — Job Description Intelligence**: Responsibility & Qualification extraction
6. **Phase 5 — Semantic Intelligence**: Vector databases (FAISS, ChromaDB), semantic search
7. **Phase 6 — Explainable ATS**: Scoring rules, gap analysis, matching algorithms
8. **Phase 7 — LLM Engineering**: OpenRouter, prompt templates, structured output, rewriting
9. **Phase 8 — Evaluation**: Precision/Recall, Hallucination testing, latency benchmarks
10. **Phase 9 — Production Pipeline**: Packaging code, prototyping API, modularizing service layers

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
