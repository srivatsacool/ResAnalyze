# **AI Resume Intelligence Platform**

### Executive Overview & Project Foundation

> **Version:** 0.1 (Planning Phase)
> **Status:** Research & Design
> **Author:** Srivatsa Gorti
> **Project Type:** Personal Public Portfolio Project
> **Primary Stack:** Python • NLP • AI Engineering • FastAPI • React • MCP • OpenRouter

---

# Executive Summary

The **AI Resume Intelligence Platform** is a production-oriented AI application designed to demonstrate the complete lifecycle of modern AI engineering, from research and experimentation to deployment and integration with AI assistants through the Model Context Protocol (MCP).

Unlike conventional resume analyzers that simply send a resume to an LLM and return generic feedback, this project aims to build an explainable, modular, and extensible AI system where every stage of the analysis pipeline is transparent and independently engineered.

The project serves three purposes simultaneously:

* **Learning Platform** — Master NLP, embeddings, semantic search, prompt engineering, and AI system design from first principles.
* **Engineering Portfolio** — Demonstrate production-quality software architecture, backend engineering, frontend development, cloud deployment, and AI integration.
* **AI Research Playground** — Experiment with multiple NLP techniques, compare algorithms, evaluate approaches, and understand why modern AI systems are built the way they are.

Rather than treating the LLM as the entire application, this platform uses traditional NLP techniques, semantic embeddings, vector search, structured prompts, and explainable scoring to create a complete AI engineering system.

---

# Vision

Build a modern AI platform capable of understanding resumes and job descriptions with explainable reasoning, semantic understanding, and production-quality architecture while documenting the complete learning journey from beginner concepts to advanced AI engineering.

---

# Mission

To build a personal flagship AI project that demonstrates the ability to design, engineer, deploy, and maintain a real-world AI application using modern software engineering practices.

---

# Why This Project Exists

Most resume analyzers today follow this workflow:

```text
Upload Resume
        ↓
Send Entire Resume to GPT
        ↓
Receive Generic Suggestions
```

This approach has several limitations:

* No understanding of the underlying NLP concepts.
* No explainability.
* No reusable architecture.
* Heavy dependence on one LLM.
* Difficult to improve individual components.
* Poor educational value.

This project instead follows an engineering-first pipeline:

```text
Resume
    ↓
Document Parsing
    ↓
Text Cleaning
    ↓
Information Extraction
    ↓
Section Detection
    ↓
Skill Extraction
    ↓
Embedding Generation
    ↓
Semantic Matching
    ↓
ATS Scoring
    ↓
LLM Reasoning
    ↓
Resume Improvements
    ↓
Interactive Dashboard
```

Each component exists independently and can be evaluated, improved, or replaced.

---

# Project Philosophy

This repository follows a set of guiding principles.

---

## 1. Learning First

Every feature should teach an AI engineering concept.

If a feature does not improve understanding of NLP, AI systems, software architecture, or engineering practices, it should not be included.

---

## 2. Explainability Over Magic

The platform should always explain:

* why a score was assigned
* why a skill is missing
* why a recommendation was generated
* why two resumes differ

The user should never receive a mysterious "ATS Score: 82" without understanding how it was calculated.

---

## 3. Engineering Before Prompting

Large Language Models are powerful, but they are only one component of the system.

The platform combines:

* Regex
* Rule-based parsing
* NLP
* Named Entity Recognition
* Embeddings
* Semantic Search
* Explainable Scoring
* Prompt Engineering
* LLM Reasoning

This reflects how many production AI applications are actually built.

---

## 4. Modular Architecture

Every capability should be an independent engine.

```text
Resume Parser Engine

↓

Job Description Engine

↓

Skill Extraction Engine

↓

Embedding Engine

↓

ATS Engine

↓

Resume Rewrite Engine

↓

Recommendation Engine

↓

Evaluation Engine
```

Each engine should be independently testable.

---

## 5. Production Engineering

Although this is a personal project, it should follow production-grade engineering practices.

Examples include:

* Clean architecture
* Dependency injection
* Logging
* Configuration management
* Testing
* CI/CD
* Docker
* Cloud deployment
* Versioning

---

## 6. Continuous Learning

The project is designed to evolve over time.

Each release represents an increase in knowledge rather than simply more features.

---

# Project Objectives

The project aims to accomplish the following objectives.

---

## Learning Objectives

Gain practical understanding of:

* Python
* Data Processing
* Machine Learning Fundamentals
* Text Mining
* Natural Language Processing
* Information Extraction
* Semantic Search
* Sentence Embeddings
* Prompt Engineering
* LLM Integration
* Retrieval-Augmented Generation concepts
* AI Engineering
* FastAPI
* React
* Docker
* Cloud Deployment
* MCP

---

## Technical Objectives

Build a production-ready AI platform capable of:

* Resume Parsing
* Job Description Parsing
* Skill Extraction
* Education Detection
* Experience Detection
* Project Detection
* Semantic Resume Matching
* ATS Score Generation
* Explainable Recommendations
* Resume Rewriting
* Career Guidance
* AI Chat Interface
* MCP Integration

---

## Engineering Objectives

Demonstrate knowledge of:

* Software Architecture
* API Design
* Backend Development
* Frontend Development
* Authentication
* Cloud Deployment
* Testing
* Monitoring
* Documentation

---

# Non-Goals

The project intentionally avoids several areas.

---

## No Custom LLM Training

The project will not train foundation models.

Instead it will leverage existing LLMs through OpenRouter.

---

## No Resume Database

The application is not intended to build a database of user resumes.

---

## No Recruitment Platform

The application does not replace recruiters or applicant tracking systems.

---

## No Automated Hiring Decisions

The platform assists users.

It does not determine whether someone should be hired.

---

## No Proprietary AI Models

The project focuses on engineering AI systems rather than developing new foundation models.

---

# Target Audience

The primary audience is yourself as an AI engineer.

Secondary audiences include:

* Recruiters
* Hiring Managers
* Technical Interviewers
* AI Engineers
* Software Engineers
* Data Scientists
* NLP Enthusiasts
* Students learning AI Engineering

---

# Expected Learning Outcomes

By the completion of Version 1.0, you should understand:

### Programming

* Python
* Async Programming
* APIs
* Type Hinting
* Packaging

---

### Data Processing

* Pandas
* NumPy
* Regex
* Data Cleaning
* Feature Engineering

---

### NLP

* Tokenization
* Lemmatization
* Stemming
* POS Tagging
* Dependency Parsing
* Named Entity Recognition
* Keyword Extraction
* Topic Modeling

---

### Semantic AI

* TF-IDF
* Word2Vec
* Sentence Transformers
* Embeddings
* Cosine Similarity
* Vector Databases
* Semantic Search

---

### AI Engineering

* Prompt Engineering
* JSON Structured Output
* Tool Calling
* Provider Abstraction
* OpenRouter
* Model Selection
* Evaluation

---

### Backend

* FastAPI
* Authentication
* API Design
* Logging
* Middleware
* Dependency Injection

---

### Frontend

* React
* TypeScript
* TailwindCSS
* Animations
* Dashboard Design

---

### Deployment

* Docker
* Cloud Run
* Cloudflare Pages
* GitHub Actions
* Environment Management

---

### MCP

* MCP Server
* Tool Design
* AI Agent Integration
* Shared Service Layer

---

# Success Criteria

The project will be considered successful when it satisfies the following conditions.

## Learning

* Complete every planned notebook.
* Understand every major NLP concept.
* Be able to explain every architectural decision.

---

## Engineering

* Clean modular architecture.
* Comprehensive documentation.
* Production deployment.
* Well-tested APIs.

---

## Product

The application should allow users to:

* Upload resumes.
* Upload job descriptions.
* Receive explainable ATS scores.
* Compare resumes with job descriptions.
* Identify missing skills.
* Improve resume bullets using AI.
* Visualize strengths and weaknesses.
* Interact through an MCP-compatible AI assistant.

---

# Guiding Principles

Every future decision should align with these principles:

1. Understand before implementing.
2. Build reusable components.
3. Prefer modularity over shortcuts.
4. Keep the architecture explainable.
5. Measure and evaluate every major feature.
6. Treat documentation as part of the product.
7. Build features that demonstrate engineering skill, not just AI capability.
8. Optimize for long-term learning rather than short-term completion.

---

# Complete Project Structure & Learning Roadmap

## Project Directory Structure

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
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   ├── research/
│   ├── diagrams/
│   ├── references/
│   └── images/
│
├── notebooks/
│   ├── 00_environment_setup/
│   ├── 01_python_refresh/
│   ├── 02_data_preprocessing/
│   ├── 03_regex/
│   ├── 04_nlp_basics/
│   ├── 05_vectorization/
│   ├── 06_embeddings/
│   ├── 07_resume_parsing/
│   ├── 08_job_description/
│   ├── 09_similarity/
│   ├── 10_skill_extraction/
│   ├── 11_ats_scoring/
│   ├── 12_resume_rewriting/
│   ├── 13_llm_experiments/
│   ├── 14_evaluation/
│   ├── 15_complete_pipeline/
│   └── assets/
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   ├── external/
│   ├── resume/
│   ├── jobs/
│   ├── skills/
│   ├── universities/
│   ├── companies/
│   ├── certifications/
│   └── locations/
│
├── experiments/
│
├── prompts/
│
├── backend/
│
├── frontend/
│
├── mcp/
│
├── deployment/
│
├── docker/
│
├── evaluation/
│
├── tests/
│
├── scripts/
│
└── shared/
```

---

## Notebook Roadmap (Complete Learning Path)

### Phase 0 — Foundations

| Notebook | Topic             | Concepts Covered                            | Dataset        |
| -------- | ----------------- | ------------------------------------------- | -------------- |
| 00       | Environment Setup | Conda, venv, Jupyter, VSCode, Git           | —              |
| 01       | Python Refresher  | Lists, Dicts, Functions, OOP, File Handling | —              |
| 02       | Pandas & NumPy    | DataFrames, Cleaning, Analysis              | Sample CSV     |
| 03       | Regex Mastery     | Email, Phone, Dates, URLs, Skills           | Resume Dataset |

---

### Phase 1 — NLP Fundamentals

| Notebook | Topic                    | Concepts                           |
| -------- | ------------------------ | ---------------------------------- |
| 04       | NLP Introduction         | NLP Pipeline, Corpus, Tokens       |
| 05       | Tokenization             | Word Tokenizer, Sentence Tokenizer |
| 06       | Text Cleaning            | Lowercase, Symbols, Unicode        |
| 07       | Stop Words               | Stopword Removal                   |
| 08       | Lemmatization            | spaCy, NLTK                        |
| 09       | Stemming                 | Porter, Snowball                   |
| 10       | POS Tagging              | Parts of Speech                    |
| 11       | Dependency Parsing       | Dependency Trees                   |
| 12       | Named Entity Recognition | PERSON, ORG, DATE, SKILL           |
| 13       | Chunking                 | Phrase Extraction                  |
| 14       | Keyword Extraction       | TF-IDF, KeyBERT                    |

---

### Phase 2 — Text Representation

| Notebook | Topic                 | Concepts               |
| -------- | --------------------- | ---------------------- |
| 15       | Bag of Words          | CountVectorizer        |
| 16       | TF-IDF                | Weighting              |
| 17       | N-Grams               | Uni/Bi/Tri-Grams       |
| 18       | Cosine Similarity     | Similarity Metrics     |
| 19       | Word2Vec              | Word Embeddings        |
| 20       | FastText              | Sub-word Embeddings    |
| 21       | GloVe                 | Pre-trained Embeddings |
| 22       | Sentence Transformers | BERT Embeddings        |
| 23       | Embedding Comparison  | Benchmark All Methods  |

---

### Phase 3 — Resume Intelligence

| Notebook | Topic                    |
| -------- | ------------------------ |
| 24       | PDF Parsing              |
| 25       | DOCX Parsing             |
| 26       | OCR Basics               |
| 27       | Resume Section Detection |
| 28       | Skill Extraction         |
| 29       | Education Parsing        |
| 30       | Experience Parsing       |
| 31       | Project Extraction       |
| 32       | Certification Extraction |
| 33       | Resume JSON Schema       |

---

### Phase 4 — Job Description Intelligence

| Notebook | Topic                      |
| -------- | -------------------------- |
| 34       | JD Parsing                 |
| 35       | Skill Extraction           |
| 36       | Responsibility Detection   |
| 37       | Qualification Detection    |
| 38       | Keyword Ranking            |
| 39       | Requirement Classification |

---

### Phase 5 — Semantic Intelligence

| Notebook | Topic                 |
| -------- | --------------------- |
| 40       | Resume vs JD Matching |
| 41       | Semantic Search       |
| 42       | FAISS                 |
| 43       | ChromaDB              |
| 44       | Embedding Evaluation  |
| 45       | Similarity Benchmark  |

---

### Phase 6 — Explainable ATS

| Notebook | Topic                 |
| -------- | --------------------- |
| 46       | ATS Rule Design       |
| 47       | Explainable Scoring   |
| 48       | Skill Gap Analysis    |
| 49       | Recommendation Engine |
| 50       | Resume Ranking        |

---

### Phase 7 — LLM Engineering

| Notebook | Topic                 |
| -------- | --------------------- |
| 51       | OpenRouter Setup      |
| 52       | Prompt Engineering    |
| 53       | JSON Outputs          |
| 54       | Function Calling      |
| 55       | Resume Rewrite        |
| 56       | STAR Bullet Generator |
| 57       | Career Advisor        |
| 58       | Model Comparison      |

---

### Phase 8 — Evaluation

| Notebook | Topic                 |
| -------- | --------------------- |
| 59       | Precision & Recall    |
| 60       | F1 Score              |
| 61       | Hallucination Testing |
| 62       | Prompt Evaluation     |
| 63       | Human Evaluation      |
| 64       | Performance Benchmark |

---

### Phase 9 — Production Pipeline

| Notebook | Topic                 |
| -------- | --------------------- |
| 65       | End-to-End Pipeline   |
| 66       | API Prototype         |
| 67       | Modularization        |
| 68       | Backend Preparation   |
| 69       | Production Validation |

---

## Topics Covered

By the end of Stage 1, you'll have practical exposure to:

| Category        | Topics                                                              |
| --------------- | ------------------------------------------------------------------- |
| Python          | OOP, Packaging, Async, File Handling                                |
| Data Science    | NumPy, Pandas                                                       |
| NLP             | Tokenization, Lemmatization, Stemming, POS, NER, Dependency Parsing |
| Text Mining     | TF-IDF, CountVectorizer, N-Grams                                    |
| Embeddings      | Word2Vec, FastText, GloVe, Sentence Transformers                    |
| Search          | FAISS, ChromaDB, Semantic Search                                    |
| Resume Parsing  | Section Detection, Skill Extraction, Experience Parsing             |
| LLM Engineering | Prompt Engineering, Structured Outputs, Function Calling            |
| Evaluation      | Precision, Recall, F1, Latency                                      |
| Backend         | FastAPI Architecture                                                |
| AI Engineering  | Modular Design, Providers, Pipelines                                |

---

## Dataset Strategy

| Dataset                         | Purpose                    | Used In              | Source                                                                                                                        |
| ------------------------------- | -------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Resume Dataset (Kaggle)         | Resume parsing             | Resume notebooks     | [Kaggle Datasets](https://www.kaggle.com/datasets?utm_source=chatgpt.com)                                                     |
| Resume NER                      | Entity extraction          | NER notebooks        | [Resume NER (Hugging Face)](https://huggingface.co/oksomu/resume-ner?utm_source=chatgpt.com) ([Hugging Face][1])              |
| Job Description Dataset         | JD parsing                 | JD notebooks         | [Hugging Face Resume/Job Datasets](https://huggingface.co/datasets?other=resume&utm_source=chatgpt.com) ([Hugging Face][2])   |
| ESCO Skills                     | Skills, occupations        | Skill extraction     | [ESCO Dataset](https://esco.ec.europa.eu/en/use-esco/download?utm_source=chatgpt.com)                                         |
| O*NET                           | Occupations & competencies | Recommendations      | [O*NET Database Downloads](https://www.onetcenter.org/database.html?utm_source=chatgpt.com)                                   |
| Stack Overflow Developer Survey | Technology trends          | Skill recommendation | [Stack Overflow Survey](https://survey.stackoverflow.co/?utm_source=chatgpt.com)                                              |
| Open Skills Project             | Skill taxonomy             | Skill normalization  | [Open Skills Project GitHub](https://github.com/workforce-data-initiative/skills-ml?utm_source=chatgpt.com)                   |
| Universities Dataset            | Education normalization    | Education parser     | [World Universities CSV](https://github.com/endSly/world-universities-csv?utm_source=chatgpt.com)                             |
| Countries & Cities              | Location parsing           | Resume parser        | [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database?utm_source=chatgpt.com)          |
| Company Dataset                 | Organization normalization | Experience parser    | [Fortune 1000 Dataset (GitHub search)](https://github.com/search?q=fortune+1000+csv&type=repositories&utm_source=chatgpt.com) |
| Action Verbs                    | Resume rewriting           | Resume rewrite       | [Harvard Action Verbs PDF](https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/?utm_source=chatgpt.com)   |
| Certification Lists             | Certification recognition  | Certification parser | [AWS Certifications](https://aws.amazon.com/certification/?utm_source=chatgpt.com)                                            |

### Recommended download priority

| Priority | Dataset                 | Why                                                       |
| -------- | ----------------------- | --------------------------------------------------------- |
| ⭐⭐⭐⭐⭐    | Resume Dataset          | Core data for parsing and structure learning              |
| ⭐⭐⭐⭐⭐    | Job Description Dataset | Essential for matching resumes to jobs                    |
| ⭐⭐⭐⭐⭐    | ESCO                    | Canonical skills and occupations                          |
| ⭐⭐⭐⭐⭐    | O*NET                   | Professional occupation and competency mapping            |
| ⭐⭐⭐⭐     | Resume NER              | Learn entity extraction and resume information extraction |
| ⭐⭐⭐⭐     | Stack Overflow Survey   | Technology relationships and trends                       |
| ⭐⭐⭐      | Universities            | Normalize education entities                              |
| ⭐⭐⭐      | Countries/Cities        | Normalize locations                                       |
| ⭐⭐⭐      | Company Lists           | Normalize employers                                       |
| ⭐⭐       | Certifications          | Recognize credentials                                     |
| ⭐⭐       | Action Verbs            | Improve resume bullet rewriting                           |

[1]: https://huggingface.co/oksomu/resume-ner?utm_source=chatgpt.com "oksomu/resume-ner · Hugging Face"
[2]: https://huggingface.co/datasets?other=resume&utm_source=chatgpt.com "Datasets – Hugging Face"

---

# High-Level Development Stages

```text
Stage 0
Research & Planning
        │
        ▼
Stage 1
NLP Learning & Notebook Experiments
        │
        ▼
Stage 2
Production AI Resume Intelligence Platform
        │
        ▼
Stage 3
MCP Integration & Production Deployment
        │
        ▼
Version 1.0
AI Resume Intelligence Platform
```

---

# Stage Overview

## Stage 0 — Research & Planning

Focus on:

* Project planning
* Architecture design
* Dataset collection
* Repository organization
* Documentation

Deliverable:
A complete project blueprint.

---

## Stage 1 — Learning & Research

Focus on:

* Jupyter notebooks
* NLP concepts
* Resume parsing experiments
* Embedding experiments
* Semantic search
* Prompt engineering
* Evaluation

Deliverable:
A library of reusable AI components and documented learning.

---

## Stage 2 — Application Development

Focus on:

* FastAPI backend
* React frontend
* OpenRouter integration
* Explainable ATS engine
* Visualization dashboard
* Production-quality architecture

Deliverable:
A fully functional AI Resume Intelligence Platform.

---

## Stage 3 — MCP & Deployment

Focus on:

* Shared service architecture
* MCP server
* Cloud deployment
* Docker
* CI/CD
* Monitoring

Deliverable:
A production-ready platform accessible via both the web application and MCP-compatible AI assistants.

---

# Long-Term Vision

The Version 1.0 platform is only the foundation.

Future versions may expand into:

* Cover Letter Intelligence
* LinkedIn Profile Analysis
* Portfolio Review
* Mock Interview Preparation
* Career Roadmap Generation
* Learning Recommendations
* Recruiter Analytics
* Multi-language Resume Support
* Browser Extensions
* Mobile Companion Application

---

## Closing Statement

This project is more than a resume analyzer. It is a comprehensive exploration of modern AI engineering, combining research, software architecture, natural language processing, semantic understanding, cloud deployment, and AI integration into a single cohesive platform. Every notebook, module, API, and interface is designed to deepen technical understanding while producing a polished, production-quality application that showcases end-to-end engineering capabilities. This `PLAN.md` serves as the project's blueprint and will guide every design and implementation decision from the initial research phase through the final production release.
