# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0-alpha] - 2026-07-30

### Added
- Block J (55–63): LLM Engineering — OpenRouter setup, prompt engineering, versioning, structured output, tool calling, weak bullet rewriter, STAR generator, career advisor, model comparison.
- Block K (64–69): Evaluation — Precision/Recall/F1, confusion matrices, hallucination testing, A/B prompt testing, human evaluation protocol, latency profiling.

### Changed
- PLAN.md: Part III status updated from "Deferred" to "Complete (J-K)".
- ROADMAP.md: Added Stage 3 (Part III) with all 15 notebooks marked ✅.

## [0.3.0-alpha] - 2026-07-30

### Added
- **All 55 notebooks for Part I & Part II complete** (00–54).
  - Part I: Blocks A–D (00–25) — NLP Foundations with full explanations and working code.
  - Part II: Blocks E–I (26–54) — Resume & Job Intelligence matcher and ATS scoring engine.

### Changed
- All checklist items in ROADMAP.md marked ✅ across Stages 1–2.
- PLAN.md notebook counts, development stages, and Part III status updated.

### Removed
- Old flat notebook directories and `part3_production/`.
- One-shot generator scripts cleaned up.

## [0.2.0-alpha] - 2026-07-30

### Added
- Defined canonical `ResumeSchema` Pydantic model with `ExtractedField` confidence scoring on every field.
- Defined complete MCP tool surface (8 tools with typed contracts).
- Defined shared service architecture (`shared/` package structure).
- Defined pipeline configuration pattern (YAML-driven, engine-swappable).
- Defined prompt versioning strategy (`registry.json` + regression tests).
- Defined caching strategy (document hash → embedding cache).
- Defined feedback loop architecture (SQLite correction dataset).
- Defined structured `evaluation/` benchmark framework.
- Reorganized 76 notebooks into 3 tight parts (Foundations, Intelligence, Production) across 12 blocks.
- Added 10 core features: Explainable ATS, ATS Simulation Mode, Weak Bullet Detector, Confidence Dashboard, Skill Normalization Engine, Embedding Space Visualizer, Resume Diff Mode, Skill Trend Radar, Prompt Observatory, Interview Prep Connector.
- Expanded development stages from 4 to 5 (split notebook stages from app build).
- Reorganized `notebooks/` into `part1_foundations/`, `part2_intelligence/`, `part3_production/`.

### Changed
- Rewrote `PLAN.md` to v0.2 — tighter structure, all brainstormed ideas integrated.
- Rewrote `ROADMAP.md` to reflect new 5-stage structure with full notebook checklist.

## [0.1.0-alpha] - 2026-07-30



### Added
- Created foundational plan in [PLAN.md](file:///d:/Projects/ResAnalyze/PLAN.md) detailing Phase 0-9 learning notebooks, folder structure, and objectives.
- Initialized comprehensive project directory structure for documentation, notebooks, datasets, frontend, backend, mcp server, and deployment targets.
- Added root configurations including `.gitignore`, `.env.example`, `LICENSE`, and `README.md`.
- Added directory setup utility script `scripts/setup_dirs.ps1`.
