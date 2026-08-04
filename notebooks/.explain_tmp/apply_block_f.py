# -*- coding: utf-8 -*-
from nbtools import apply

# ============ NB32 — Resume Section Detection ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\32_section_detection\32.ipynb", replace={
0: r"""# 32 — Resume Section Detection
**Goal:** Identify section boundaries in unstructured resume text.

A raw resume is a flat wall of lines; its meaning lives in its *structure* — where the summary ends and the experience section begins. This chapter builds that structure: a curated list of known section names, a regex scanner that flags section headers line by line, and a zero-shot ML fallback for layouts that regex cannot read.

**Why it matters for resumes / ATS:** every later extraction step needs to know *which lines belong to which section*. Detecting "EDUCATION", "education", or "Academic Qualifications" as the same section is what lets Ch. 33–38 scope their parsers to the right content block instead of scanning the whole document — and it stops a stray "Skills" mention inside a bullet from being misread as a section header.""",
1: r"""## 1. Common Resume Sections

Resumes converge on a small set of standard sections — summary, experience, education, skills, projects — but the *labels* vary wildly: "Work History", "Employment", and "Professional Experience" all mean the same thing. The first job is to enumerate the aliases so a detector can map any of them onto one canonical section.

**What the code does:** builds `SECTIONS`, a flat list of 17 known section names, grouped by meaning — three names for experience, two for education, three for skills. Running it prints `Known sections: 17` and then every entry in the list.

**Why it matters:** the list *is* the detector's vocabulary. A candidate who writes "Core Competencies" instead of "Skills" is only caught because `core competencies` is in the list — so growing this list (a job-title-aware alias table) directly improves recall.""",
3: r"""## 2. Regex-Based Section Detection

Section headers are short, standalone lines that *start with* a known section name — an ideal regex target. The recipe: compile one anchored, case-insensitive pattern per section name, then scan the resume line by line.

**What the code does:** `SECTION_PATTERNS` pre-compiles `^<name>` patterns with `re.escape`; `detect_sections()` walks the lines, skips blanks, and when a line matches a pattern **and is shorter than 40 characters** it records `(section, line_index, header_text)`.
- The `< 40` check is the header heuristic: a long line that merely *contains* "experience" ("I gained experience in…") is not a header.
- On the sample resume the run detects 4 sections: `SUMMARY` at line 0, `EXPERIENCE` at line 3, `EDUCATION` at line 7, `SKILLS` at line 10 — exactly the boundaries a human reader would draw.

**Try it:** `re.escape(s)` is what keeps punctuation-heavy names like "C#" or "R&D" safe inside the pattern.""",
5: r"""## 3. ML-Based Section Classification

Real resumes break the regex contract — "Professional Experience", "Technical Skills & Expertise" — or bury headers in unusual layouts. For those, a zero-shot classifier labels a line *semantically*: it asks a pretrained model (`facebook/bart-large-mnli`) how well each candidate section name matches the line, with no fine-tuning.

**What the code does:** builds a zero-shot `pipeline`, scores each test line against all 17 `SECTIONS`, and prints the best label with its probability. The construction and scoring loop sit inside a `try/except`, so a model that fails to load degrades to a printed fallback message instead of crashing.

**Expected behavior:** each line is labeled with the section it scores highest against, along with that score. Note two caveats: the first run downloads the model (needs network, ~1.6 GB), and the fallback only guards the pipeline call — a hard failure at the `from transformers import pipeline` import itself would still raise. Regex stays the fast, offline default; ML is the escape hatch for hard layouts.""",
7: r"""## 4. Section Content Extraction

Detecting headers is only half the job — the pipeline also needs the *content* that belongs under each header, so the education parser does not accidentally read experience bullets.

**What the code does:** `extract_section_content()` runs the same header check inside a small state machine: any header line flips `in_section` off (a new section just ended the old one), and if that header is the target section it flips `in_section` on. Every following non-blank, non-header line is appended until the next header.

**Verified on the sample resume:** requesting `"experience"` returns exactly the two lines under `EXPERIENCE` — `['Google — Senior Data Scientist, 2020-Present', 'Built ML pipelines.']` — and stops at `EDUCATION`.

**Try it:** call it with `"skills"` and the same state machine walks to the `SKILLS` header and collects its single line — the mechanism every section-scoped parser in Ch. 35–38 relies on.""",
9: r"""## Summary: Regex + heuristics for basic detection. Zero-shot ML for complex layouts.

**Section headers are the skeleton of a resume — detect them first, and everything else gets easier.**

Header detection is deliberately cheap: anchored regexes plus a line-length heuristic catch the vast majority of real resumes in microseconds with zero dependencies, and the zero-shot classifier is the safety net for unconventional layouts at the cost of a model download. What matters is that both paths produce the same contract — `(section, line_index, header_text)` — so downstream parsers never care *how* the section was found.

This is the entry point of the extraction pipeline: Ch. 33 starts consuming these sections to pull out skills, and Ch. 35–38 scope their parsers to the content blocks this chapter isolates.""",
})

# ============ NB33 — Skill Extraction (Rules) ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\33_skill_extraction_(rules)\33.ipynb", replace={
0: r"""# 33 — Skill Extraction (Rules)
**Goal:** Extract skills from resume text using rule-based matching.

Skills are the highest-signal tokens in a resume — the terms recruiters filter on. This chapter starts with a curated taxonomy, then matches it against resume text two ways: exact word-boundary regexes for precision, and fuzzy string similarity for typo tolerance.

**Why it matters for resumes / ATS:** ATS keyword screens are literal — "TensorFlow" in the job description must appear somewhere in the resume. Rule-based extraction is the fastest, most explainable way to prove a skill is present, and its `(raw, category, confidence)` records give the normalization engine in Ch. 34 something to canonicalize.""",
1: r"""## 1. Building a Skills Database

Extraction is only as good as the vocabulary it searches with. The `SKILLS_DB` dict organizes known skills into six categories — `programming`, `ml_dl`, `nlp`, `data`, `cloud`, `databases` — modeled on public taxonomies like ESCO and O*NET.

**What the code does:** defines the dict, then prints the total and a preview of each category. Running it reports **49 known skills** across the six groups: 13 programming languages, 7 ML/DL frameworks, 8 NLP terms, 8 data tools, 7 cloud tools, and 6 databases.

**Why it matters:** the category labels are the bridge to the final schema — a raw match like "PyTorch" arrives pre-tagged as `ml_dl`, so Ch. 34 and Ch. 39 do not have to re-infer what it is. A bigger database means better recall, but every entry is also a chance for false positives — which is why the matching strategy matters as much as the vocabulary.""",
3: r"""## 2. Regex Skill Matching

The baseline matcher: for every skill in the database, ask "does this exact string appear in the resume?" — with word boundaries and case-insensitivity so "Python" is not found inside "Pythonista" and lowercase "python" still matches.

**What the code does:** `extract_skills_regex()` iterates every `(category, skill)` pair and runs `re.search` with `re.escape` plus the `IGNORECASE` flag, emitting a dict with `raw`, `category`, `confidence: 1.0`, and `method: "exact_match"` on every hit.

**Honest failure mode:** the cell writes `r"\\b"` (escaped backslash + `b`) instead of `r"\b"`, so as written the boundary pattern never matches and the loop prints nothing. With the boundary fixed, the sample resume yields six exact matches at confidence 1.0: `Python` (programming), `TensorFlow` and `PyTorch` (ml_dl), `NLP` (nlp), `AWS` and `Kubernetes` (cloud) — a classic raw-string escaping gotcha worth remembering.

**Try it:** `re.escape()` is what makes "C++" and "C#" safe — without it the `+` and `#` would act as regex operators.""",
5: r"""## 3. Fuzzy Matching for Typos

Resumes are riddled with typos — "TensrFlow", "Pytorch", "Dockr". Exact matching misses all of them. Fuzzy matching compares each candidate word against every known skill and keeps the best match that clears a similarity threshold.

**What the code does:** `extract_skills_fuzzy()` tokenizes the text with `re.findall`, runs `rapidfuzz`'s `process.extractOne()` per word against the flattened skill list using `fuzz.ratio`, keeps matches scoring ≥ 85, and returns a set of `(skill, category, score)` tuples so each skill appears once.

**Verified with the boundary fixed:** on "I know PyTorch, TensrFlow, and Dockr" the fuzzy layer recovers all three typos — `PyTorch` at 100%, `TensorFlow` at ~95%, `Docker` at ~91% — while "I", "know", and "and" fall far below the threshold and are dropped. As written (double-escaped `\\b`), the tokenizer finds no words and the cell prints nothing.

**Trade-off:** fuzzy matching rescues typos but invites false positives ("Go" vs "Godot"). The threshold is the dial — 85 balances typo recall against spurious hits, and the set-dedupe keeps one entry per skill even when several words match it.""",
7: r"""## Summary: Start with exact regex matching, layer fuzzy matching for typos.

**Rule-based skill extraction is the precision play: fast, explainable, and dependency-free.**

Exact matching is the right first layer — zero false positives when a skill string genuinely appears. Fuzzy matching is the second layer, trading a little precision for typo tolerance, and both layers carry the category labels and confidence that keep output schema-ready: exact matches are 1.0 by construction, fuzzy matches carry their similarity score. The threshold is a tunable business decision, not a fixed constant.

The raw `(skill, category)` pairs produced here are exactly what Ch. 34's normalization engine consumes next — collapsing "ML" and "Machine Learning" into one canonical entry.""",
})

# ============ NB34 — Skill Normalization Engine ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\34_skill_normalization_engine\34.ipynb", replace={
0: r"""# 34 — Skill Normalization Engine
**Goal:** Normalize skill names to canonical taxonomy (ESCO/O*NET).

Extraction (Ch. 33) finds *mentions*; normalization decides what each mention *means*. "ML", "machine learning", and "Machine Learning" are one skill; "AWS" and "Amazon Web Services" are one service. This chapter builds a fallback chain that maps raw strings onto a canonical taxonomy, escalating from exact lookup to fuzzy match to semantic embeddings.

**Why it matters for resumes / ATS:** a normalized skill vocabulary is what makes matching *countable*. An ATS that treats "ML" and "Machine Learning" as different strings under-counts matches against a job description; normalizing both to one canonical name makes scores fair and analytics clean — and it is the only way to compare candidates across thousands of differently-worded resumes.""",
1: r"""## 1. Three-Tier Normalization

One normalizer, three escalating strategies — each tier is cheaper and more literal than the last, so the chain only spends effort when it has to:

| Tier | Strategy | Example |
|---|---|---|
| 1 | Exact match against taxonomy | `"Python"` → `"Python (programming language)"` |
| 2 | Fuzzy match (`rapidfuzz`) | `"Tensorflo"` → `"TensorFlow"` (typo tolerance) |
| 3 | Embedding similarity (`sentence-transformers`) | `"ML"` → `"Machine Learning"` (semantic) |

**What the code does:** the cell documents the chain in a printed docstring. Note the docstring quotes a 0.85 fuzzy threshold and a 0.80 embedding threshold, while the actual code in the next cells uses `80` for `fuzz.ratio` and `0.65` for cosine similarity — treat printed thresholds as aspirational and code defaults as truth.

**Why it matters:** the tier also carries confidence meaning — an exact hit is more trustworthy than a fuzzy one, which is more trustworthy than a semantic one — and that ordering flows straight into the schema's `confidence` field in Ch. 39.""",
3: r"""## 2. Building the Normalizer

`SkillNormalizer` wraps a 10-entry canonical taxonomy (including `"ml"` → `"Machine Learning"` and `"aws"` → `"Amazon Web Services"`) and implements tiers 1 and 2: look up the lowercased, stripped raw skill; if absent, fuzzy-match it against the taxonomy keys with `fuzz.ratio`.

**What the code does:** `normalize()` returns `{"normalized", "tier", "confidence"}` — tier 1 hits get `1.0`, tier 2 hits get `score/100`, and unknown skills fall through to tier 0 with `0.5` confidence while keeping the raw string.

**Verified on the sample list:** `"Python"` → `Python (programming language)` (tier 1, conf 1.00); `"pytorch"` → `PyTorch` (tier 1 — case handled by `.lower()`); `"Tensorflo"` → `TensorFlow` (tier 2, conf 0.95); `"ML"` and `"NLP"` → their full forms (tier 1); and `"CloudWhiz"` → unchanged (tier 0, conf 0.50). That last row is the honest case: unknown skills pass through rather than being forced into a wrong bucket.

**Try it:** feed "Pytorch" with wrong casing — only spelling, not casing, costs you a tier.""",
5: r"""## 3. Embedding-Based Normalization (Tier 3)

The fuzzy tier only rescues *spelling* variants. "ML" vs "Machine Learning" shares almost no characters — only meaning — so it needs semantic similarity: encode both strings with a sentence-transformer and compare the vectors with cosine similarity.

**What the code does:** `EmbeddingNormalizer` subclasses `SkillNormalizer`, encodes the canonical taxonomy once with `all-MiniLM-L6-v2`, then `normalize_embedding()` encodes the raw skill, takes the argmax cosine score, and returns the best canonical text if it clears `threshold=0.65`. Model loading is wrapped so a missing `sentence-transformers` install sets `has_embeddings = False` and degrades to the tier 1/2 fallback instead of failing.

**Expected behavior:** abbreviations and paraphrases ("ML", "NLP", "Cloud computing") map to their canonical forms via embedding proximity, even with near-zero string overlap — at the cost of a ~90 MB model download on first use and slower per-skill latency than the regex/fuzzy tiers.""",
7: r"""## Summary: Three-tier normalization catches exact matches, typos, and semantic variants.

**Normalization turns noisy extraction into a clean, countable skill vocabulary.**

The tiered fallback is a classic robustness pattern: cheapest and most precise first, most expensive and most flexible last, with each tier reporting its own confidence so downstream consumers can weight the result. Exact and fuzzy tiers run offline in milliseconds; the embedding tier adds semantic coverage for abbreviations and paraphrases when the model is installed.

The output contract — canonical name + tier + confidence — is exactly the `Skill` shape Ch. 39's schema formalizes, so normalized skills flow straight into the final JSON. Next, Ch. 35 applies the same section-scoped thinking to education.""",
})

# ============ NB35 — Education Parsing ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\35_education_parsing\35.ipynb", replace={
0: r"""# 35 — Education Parsing
**Goal:** Extract degree, institution, field, and graduation year.

Education is one of the most regular blocks on a resume: a degree name, an institution, a field, and a year, usually on one or two lines. Its regularity makes it a perfect regex target — no ML required. This chapter builds a degree vocabulary, an extractor that pulls the four fields, and an alias table that normalizes institution names.

**Why it matters for resumes / ATS:** education is a hard filter in many postings ("MS in CS required"). Structured extraction lets an ATS answer "does this candidate hold a Master's in a relevant field?" reliably — and normalizing "IIT Bombay" to "Indian Institute of Technology Bombay" keeps those checks consistent across thousands of differently-phrased resumes.""",
1: r"""## 1. Education Patterns

The extractor's vocabulary is a list of degree strings covering the common variants: bachelor's (`B.Tech`, `B.E.`, `B.S.`, `B.Sc`, `B.A.`), master's (`M.S.`, `M.Tech`, `M.B.A.`, `MBA`), doctorates (`PhD`, `Ph.D.`, `Doctorate`), generic words (`Bachelors`, `Masters`), and even pre-university markers (`10th`, `12th`, `SSC`, `HSC`) common in some regions.

**What the code does:** defines `DEGREES` and prints `Known degree patterns: 27` — the full count of patterns the matcher will try against each line.

**Why it matters:** coverage here defines recall. Generic forms like "Masters" catch informal resumes that "M.S." misses, while regional markers (`10th`/`12th`) matter for markets where school-leaving certificates are listed — a reminder that a production vocabulary should be tuned to the candidate population.""",
3: r"""## 2. Education Extractor

`extract_education()` applies the standard recipe: split into lines, scan each line for any degree pattern, then pull the surrounding fields with three small regexes — institution after "at"/"from", a 19xx/20xx year, and a field after "in".

**What the code does:** for each matched line it assembles a dict with `degree`, `institution`, `field`, `year`, and a `confidence` of `"high"` when both institution and year were found, else `"medium"`. It stops at the first degree per line.

**Honest failure modes:** as written, the degree check uses `r"\\b"` (escaped backslash) instead of `r"\b"`, so no line matches and the cell prints nothing. With the boundary fixed, two of the three test entries come out — `B.Tech` / Computer Science / 2019 (medium: no "at"/"from" preposition) and `PhD` / NLP / no year (medium) — while "M.S. in Data Science from Stanford University, 2021" is *skipped entirely*, because the trailing `\b` after the period in `M.S.` requires a word character next, and a space is not one. That is the classic `\b`-ends-on-punctuation trap.

**Try it:** the `(?:at|from)` alternation explains why "from Stanford University" yields an institution but "IIT Bombay" after a comma does not.""",
5: r"""## 3. Institution Normalization

Institutions are spelled a dozen ways ("IIT Bombay" vs "Indian Institute of Technology Bombay", "MIT" vs "Massachusetts Institute of Technology"). An alias map collapses them onto full canonical names — the same idea as Ch. 34's skill taxonomy, applied to universities.

**What the code does:** `UNIVERSITY_ALIASES` maps 11 shorthand keys (lowercased) to full names; `normalize_institution()` lowercases the input and looks it up, returning the input unchanged when there is no alias.

**Verified on the sample:** `"IIT Bombay"` → `Indian Institute of Technology Bombay`, `"Stanford"` → `Stanford University`, `"MIT"` → `Massachusetts Institute of Technology` — and `"NIT Trichy"` → `NIT Trichy` unchanged, because the map only contains the generic key `"nit"`, not specific campuses.

**Try it:** that `"nit"` key is effectively a wildcard — it will rewrite *any* "NIT ..." entry to the generic name. Decide whether you want that behavior before deploying.""",
7: r"""## Summary: Regex extracts structured education data. Institution aliases normalize names.

**Education is the most regular resume block — and the most reliably regex-parseable one.**

A 27-pattern degree vocabulary, three field regexes, and an 11-entry alias table are enough to extract degree, institution, field, and year with a confidence signal. The extraction dicts are already schema-shaped: they map 1:1 onto the `Education` model in Ch. 39, with `confidence` ready to flow into `ExtractedField`. And the `\b`-escaping lesson carries forward — verify a regex result before trusting it.

Next, Ch. 36 applies the same line-state-machine approach to the messier, bullet-heavy experience section.""",
})

# ============ NB36 — Experience Parsing ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\36_experience_parsing\36.ipynb", replace={
0: r"""# 36 — Experience Parsing
**Goal:** Extract company, role, duration, and responsibilities.

Experience is the most information-dense section of a resume and the least regular: header lines vary ("Google, Mountain View — Senior Data Scientist"), dates come in every format, and the real payload is an arbitrary list of bullets. This chapter builds a line-driven state machine that groups those lines into experience entries.

**Why it matters for resumes / ATS:** experience is what recruiters actually evaluate — role progression, tenure, and quantified achievements. Parsing it into `(company, role, duration, bullets)` is what makes role-level matching ("has this candidate been a Senior Data Scientist?") and tenure scoring possible, and it feeds the bullet scoring in Ch. 37.""",
1: r"""## 1. Experience Pattern Recognition

Before writing a parser, study the shape of the data. Experience entries follow a near-universal template: a **header line** (`Company, Location — Role`), a **date range** line, then **bullet points** of achievements — and the whole pattern repeats per employer.

**What the code does:** sets up `exp_text`, a two-company sample (Google and Amazon), and prints the expected shape: header, date range, bullets.

**Why it matters:** every design decision in the parser comes from this template. The header line carries the em-dash delimiter (`—`) between location and role; dates are anchored on month names or 4-digit years; bullets start with `-`, `•`, or whitespace. If you can name these regularities, you can encode them — and you know which resumes (non-standard layouts) will defeat the parser.""",
3: r"""## 2. Experience Parser

`parse_experience()` is a small **state machine**: it walks lines, and each line either starts a new entry, sets the duration, or appends a bullet — depending on which pattern it matches.

**What the code does:** three checks per line, in order:
- **Header regex** `^([A-Za-z\s.]+),?\s*([A-Za-z\s]+)?\s*[—\-–]\s*(.+)$` — on a match, the current entry is finalized and a new `{"company", "role", "duration", "bullets"}` starts.
- **Date regex** (month names or `\d{4}` followed by `-`) — records the first 40 characters of the line as `duration`.
- **Bullet strip** `^[\s•\-*–]+` — any other non-trivial line (length > 10) is added to the current entry's bullets.

**Verified on the sample:** two entries come out — `Google | Senior Data Scientist | Jan 2020 - Present` with 3 bullets, and `Amazon | Data Scientist II | 2018 - 2020` with 2 bullets — each bullet's leading dash stripped.

**Try it:** the header regex requires the dash delimiter; a resume that writes "Google, Senior Data Scientist" on one line without a dash will fail to start a new entry — a known coverage gap.""",
5: r"""## 3. Duration Calculation

Tenure is a recruiter filter ("5+ years of experience"), but durations arrive as free text: "5+ years", "2020 - Present", "2018 - 2020". `parse_duration()` converts them to a single comparable number — years.

**What the code does:** three fallbacks, in order:
- an explicit `N years` pattern (optional `+`) → `N`;
- a date-range pattern that finds all 4-digit years and subtracts the first from the last;
- otherwise `0`.

**Verified on the sample:** `"5+ years"` → `5`, `"2018 - 2020"` → `2`, `"3 years"` → `3` — but `"2020 - Present"` → `0`, because "Present" is not a year. That is the honest limitation: active roles undercount tenure until you special-case "Present" against a reference date such as today.""",
7: r"""## Summary: Pattern matching extracts structured experience. Duration calc estimates tenure.

**Experience parsing is a state machine over lines: header, date, bullet — repeat.**

The three-pattern loop is deliberately simple and fully explainable: it recovers company, role, duration, and bullets without any model, and it degrades predictably (a missing dash, an unparsable date) rather than failing silently. Duration math is an estimate, not truth — "Present" needs a reference date to be counted.

The output shape — `{company, role, duration, bullets}` — is the `Experience` model from Ch. 39, and the bullets it collects are the raw material Ch. 37 scores for STAR compliance next.""",
})

# ============ NB37 — Bullet Parsing & STAR Scoring ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\37_bullet_parsing_and_star_scoring\37.ipynb", replace={
0: r"""# 37 — Bullet Parsing & STAR Scoring
**Goal:** Score resume bullets on action verbs, metrics, and STAR compliance.

A resume bullet is a mini-argument: "Reduced model latency by 40% by optimizing inference pipeline". The STAR method (Situation, Task, Action, Result) is the rubric recruiters use to judge whether that argument is strong. This chapter scores bullets mechanically — action verbs, quantified metrics, context, outcome — with pure rules, no LLM.

**Why it matters for resumes / ATS:** screening systems rank candidates partly on bullet quality. Rule-based STAR scoring gives an instant, consistent, explainable 0–1 quality signal per bullet — the feature that lets an ATS (or a career coach) say "this bullet is weak, add a metric" — and it is the same signal Ch. 39 stores per bullet for downstream reporting.""",
1: r"""## 1. STAR Method Explained

STAR = **S**ituation, **T**ask, **A**ction, **R**esult. A strong bullet leads with a strong action verb, quantifies the result, names the technology or context, and states an outcome. A weak one is passive ("Was responsible for ML models"), metric-free, and result-free.

**What the code does:** the cell is a printed reference card. It contrasts a good bullet ("Reduced model latency by 40% by optimizing inference pipeline" — Action `Reduced`, Result `40%`, Task `optimizing inference`) against a weak one, then lists the four scoring criteria the rest of the chapter encodes: strong action verb, quantified metric, specific context, result/outcome.

**Why it matters:** these four criteria are *operationalizable* — each maps to a regex check in the next cells. That is the whole trick of rule-based scoring: turn a hiring heuristic into a checklist.""",
3: r"""## 2. Bullet Scorer

`score_bullet()` converts the STAR rubric into a 0–1 score by summing weighted regex checks, capped at 1.0:

| Check | Weight |
|---|---|
| First word is a strong action verb (21 verbs in `ACTION_VERBS`) | +0.30 |
| Quantified metric (`%`, `million`, `$`, `x`, `percent`) | +0.30 |
| "by N" improvement phrasing | +0.15 |
| Technology context (`using`/`with`/`via` + capital letter) | +0.15 |
| Context nouns (`team`, `pipeline`, `system`, `platform`) | +0.10 |

**Verified on the five test bullets:** the TensorFlow bullet scores `0.75` (STRONG); "Led team of 5 engineers to deliver ML platform" scores `0.40` (GOOD); "Improved customer engagement with data-driven recommendations" scores `0.30` (WEAK) — an action verb with no metric to back it; "Was responsible for ML model development" and "Worked on various projects" score `0.00` (WEAK).

**Try it:** the weights are a judgment call, not gospel — rebalance them and the STRONG/GOOD/WEAK boundaries move with your hiring priorities.""",
5: r"""## 3. STAR Compliance Check

Scoring is continuous; compliance is boolean. `star_compliance()` answers five yes/no questions about a bullet — starts with an action verb, contains a number, mentions a technology (any capitalized word), signals an outcome ("by", "resulting", "achieving", "increasing", "reducing"), and avoids passive openers ("was"/"were"/"had"/"has been").

**What the code does:** returns a dict of five booleans; the cell prints `passed/5` plus a tick per check.

**Verified on the test bullets:** the TensorFlow bullet passes all 5; "Led team of 5 engineers to deliver ML platform" passes 4 (no outcome signal); "Was responsible for ML model development" passes just 1 — `has_technology`, and only because "Was" is a capitalized word. That exposes the crude proxy: `has_technology` fires on *any* capital-letter sequence, so a passive opener alone satisfies it.

**Try it:** compare the 0.40-scoring "Led team..." bullet (4/5 STAR) with the 0.30 "Improved..." bullet (3/5) — the score and the compliance count agree on ranking but measure different things.""",
7: r"""## Summary: Bullet scoring identifies weak bullets for improvement. Rule-based, no LLM needed.

**Bullet quality is measurable — action verb + metric + context + outcome, summed and capped.**

The scorer and the compliance checker are two views of the same rubric: a continuous 0–1 score for ranking, and a five-flag report for coaching ("add a metric", "switch to active voice"). Both are pure regex over one line of text — fast enough to run over a whole resume in microseconds, and fully explainable to a candidate.

The `star_score` and boolean flags computed here are stored per bullet in Ch. 39's `ExperienceBullet` model, giving the final resume JSON a per-bullet quality signal. Next, Ch. 38 extracts the projects section, whose bullets get scored the same way.""",
})

# ============ NB38 — Project Extraction ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\38_project_extraction\38.ipynb", replace={
0: r"""# 38 — Project Extraction
**Goal:** Extract project names, tech stacks, and outcomes from resumes.

Projects are where candidates show initiative — side builds, capstones, open-source work — often formatted like mini-experience entries but without dates. This chapter parses the typical "Name | Tech Stack" header plus bullets, reusing the state-machine pattern from Ch. 36 with a simpler schema.

**Why it matters for resumes / ATS:** for junior candidates, projects *are* the experience. Extracting the name and tech stack lets an ATS match project tech against JD requirements, and the outcome bullets ("Achieved 92% accuracy…", "99.9% uptime") carry the same quantified-impact signal Ch. 37 scores — giving candidates without formal work history a fair shot.""",
1: r"""## 1. Project Pattern Recognition

Project blocks follow their own template: a header line `Name | Tech Stack` (pipe-delimited), followed by bullets that describe what was built and what it achieved. Note what is missing versus experience: no company, no dates.

**What the code does:** sets up `project_text` with three sample projects — "Resume Intelligence Platform | Python, NLP, TensorFlow", "Sentiment Analysis Dashboard | Python, Flask, React", and "E-commerce Recommendation Engine | Python, Spark, MongoDB" — and prints the expected shape: name, tech stack, bullets with outcomes.

**Why it matters:** the pipe delimiter is the parser's anchor — it is rare in ordinary prose, so a line containing `|` is almost certainly a project header. That single observation keeps the parser nearly as simple as the education extractor.""",
3: r"""## 2. Project Parser

`extract_projects()` is the Ch. 36 state machine, simplified: a header regex captures the name and tech stack, and every following non-empty line becomes a bullet of the current project.

**What the code does:** the header pattern `^([A-Za-z\s]+)\s*[|]\s*(.+)$` splits on the first pipe; anything else is bullet-stripped (leading `-`/`•`/whitespace removed) and appended to `current["bullets"]`; a new header finalizes the previous project.

**Verified on the sample:** the first project parses cleanly — "Resume Intelligence Platform" with 2 bullets. The second, "Sentiment Analysis Dashboard", ends up with **5 bullets** because the third project's header line — "E-commerce Recommendation Engine | Python, Spark, MongoDB" — fails to match: the hyphen in "E-commerce" is not in `[A-Za-z\s]+`, so the line is treated as a bullet and drags its two outcome bullets along. A textbook case of a delimiter assumption failing on real data.

**Try it:** add `-` to the header character class (e.g. `[A-Za-z\s-]+`) and all three projects parse — a one-character fix with a visible payoff.""",
5: r"""## Summary: Project extraction follows similar pattern to experience but without dates.

**Projects reuse the experience state machine, minus dates, plus a pipe-delimited header.**

One regex over the header line and a bullet strip are enough to recover name, tech stack, and outcome bullets from a standard projects block — and the hyphen-in-name failure above is the real lesson: every parser encodes assumptions about delimiters, and those assumptions fail on real data in predictable ways. Validate against a corpus before trusting recall.

Project dicts (`name`, `tech`, `bullets`) slot into Ch. 39's `projects` list, and their outcome bullets are scored by the same Ch. 37 STAR logic. With all four content sections parsed, Ch. 39 finally assembles everything into one schema.""",
})

# ============ NB39 — Resume JSON Schema ============
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_f\39_resume_json_schema\39.ipynb", replace={
0: r"""# 39 — Resume JSON Schema — Live Build
**Goal:** Assemble all extracted fields into the canonical ResumeSchema Pydantic model.

Every parser in this block produces ad-hoc dicts with slightly different shapes. This chapter fixes that: a single Pydantic `ResumeSchema` that every extraction engine reads and writes, plus a live end-to-end build that fills it from one raw resume string.

**Why it matters for resumes / ATS:** a schema is the *contract* between extraction and consumption. Downstream systems — matching engines, dashboards, storage — only need to know one shape, and Pydantic enforces it at runtime: a bullet missing `star_score` still validates with its default, while a `Skill` with an invalid `category` is rejected. That is the difference between a pipeline that degrades gracefully and one that silently corrupts data.""",
1: r"""## 1. The Canonical Schema

The schema is a set of nested Pydantic models, each carrying the outputs of the previous chapters:

| Model | Fields | Source |
|---|---|---|
| `ExtractedField` | `value`, `confidence` (0–1), `source` (`regex`/`NER`/`LLM`/`rule`/`embedding`) | Ch. 33–34 provenance |
| `Skill` | `raw`, `normalized`, `category`, `confidence` | Ch. 33–34 |
| `ExperienceBullet` | `text`, `has_metric`, `has_action_verb`, `star_score` | Ch. 37 |
| `Experience` | `company`, `role`, `duration`, `bullets` | Ch. 36 |
| `Education` | `institution`, `degree`, `field`, `year` | Ch. 35 |
| `ResumeSchema` | `raw_text`, `personal_info`, `skills`, `experience`, `education`, `projects`, `schema_version` | all |

**What the code does:** defines the models with sensible defaults (`""`, `[]`, `0.0`) so partial extractions still validate, then prints the field list: `['raw_text', 'personal_info', 'skills', 'experience', 'education', 'projects', 'schema_version']`.

**Why it matters:** defaults are the resilience mechanism — a resume with no projects still produces a valid document, and `schema_version` makes future migrations explicit.""",
3: r"""## 2. Building the Pipeline End-to-End

The payoff: `build_full_resume()` runs the whole block's logic — section detection, personal-info extraction, skill matching, experience matching — against one raw text and returns a populated `ResumeSchema`.

**What the code does:** creates the schema from `raw_text`; sets `personal_info` from the first non-empty line (the name) plus a placeholder email; matches a small inline `SKILLS_DB` against the text; and finds every `Company — Role` pattern for experience. Where a chapter function is not available in this notebook's namespace (e.g. `detect_sections`), it is skipped via a `dir()` guard rather than crashing.

**Verified on the sample:** the build returns `Skills: 0`, `Experience: 1`, `Schema v1.0`, and the JSON dump shows `personal_info` with the name and the placeholder email, an empty `skills` list, and one experience entry. Two honest artifacts: the email is hardcoded, and the skills count is 0 because the inline matcher carries the same `\\b` escaping gotcha from Ch. 33 (with the boundary fixed it would find `Python` and `TensorFlow`). End-to-end output is only as good as each stage's own tests.

**Try it:** `model_dump_json(indent=2)` is the serialization API — it is what ships the whole structured profile to whatever consumes it next.""",
5: r"""## Summary: ResumeSchema provides a unified contract. Every engine reads/writes this format.

**A typed schema is the contract that turns eight ad-hoc parsers into one pipeline.**

With `ResumeSchema`, extraction, storage, and matching all speak one shape: Pydantic validates it, defaults keep partial results valid, `schema_version` future-proofs it, and the `confidence`/`source` fields preserve provenance from Ch. 33–37 so downstream scoring can weight by trust. The live build shows the contract working end-to-end — and the placeholder email and empty skills list show exactly where the individual stages still need hardening.

This closes Block F's extraction pipeline. Everything produced here is the input to Ch. 40 — JD Parsing — which parses the *job description* into the same schema shape so resume and JD can finally be matched field by field.""",
})
