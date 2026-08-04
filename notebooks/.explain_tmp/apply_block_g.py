# -*- coding: utf-8 -*-
"""Expand markdown cells of block_g notebooks 40-45 (heading-only stubs -> teaching text)."""
from nbtools import apply

# ============================================================
# 40 - JD Parsing
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\40_jd_parsing\40.ipynb", replace={
0: r"""# 40 — JD Parsing
**Goal:** Parse job description structure into sections.

A job description is a single blob of prose, but it is *internally structured*: a header (title, company), an "about" pitch, a responsibilities list, a qualifications list, a nice-to-have list, and a benefits block. This chapter turns that blob into labeled buckets — the JD-side mirror of the resume-section parsing done in earlier blocks. Everything that follows in Block G assumes these buckets exist: skill extraction, responsibility detection, and qualification mining all read from *specific* sections rather than the raw text.

**Why it matters for resumes / ATS:** an ATS compares two documents — the resume and the JD — and every comparison is only as precise as the sections it compares. A skill in *Qualifications* is a hard requirement; the same skill in *Nice to have* is a soft bonus. If the parser cannot tell the two apart, every downstream score is wrong. Section parsing is the load-bearing wall for the whole matching pipeline.""",
1: r"""## 1. Typical JD Structure

Almost every JD follows the same skeleton: **header** (title, company, location), **about the role** (why the team exists), **responsibilities** (what the hire will do), **qualifications** (what they must already have), **nice to have** (soft extras), and **benefits** (compensation/perks). The wording varies — "What you'll do", "Requirements", "Perks" — but the *order* is remarkably stable, which is exactly what makes heading-based detection feasible.

**What the code does:** defines `jd`, a sample senior-data-scientist posting that will be reused by every later chapter in this block (Ch. 41–45 all operate on this same string). The `print` statement simply spells out the canonical section order the detector must recover. Working from one controlled example makes it easy to see where the parser succeeds and where it slips.""",
3: r"""## 2. JD Section Detection

Section detection is a **keyword-triggered state machine**: walk the text line by line; when a line contains a heading keyword ("responsibilities", "nice to have", …) *and* is short (`len(ls) < 40`), switch the active section; otherwise append the line to the current section. The length guard is the trick that stops body sentences like "We are looking for a senior data scientist…" from being mistaken for headings.

**What the code does:**
- `JD_SECTIONS` maps canonical section names to lists of heading synonyms ("what you'll do", "what we offer", "experience required").
- `detect_jd_sections()` lowercases each line, scans the synonym lists in order, and resets `current_section` when a heading matches.
- Non-heading lines accumulate via `setdefault` into the open section; lines before the first heading land in `header`.

**Expected:** running this on the sample `jd` recovers `header` (title + company), `about`, `responsibilities`, `qualifications`, `nice_to_have`, and `benefits` buckets. One sharp edge: the line "Strong Python and SQL skills" *contains* the keyword "skills", so a mid-list bullet can retrigger the qualifications heading and reset the bucket — real-world JD parsers need to require headings to be short, capitalized, and dash-free.""",
5: r"""## Summary: JD parsing identifies sections for targeted extraction. Similar approach to resume sections.

**Sections turn a prose JD into addressable buckets, and every later chapter depends on those buckets being correct.**

The same divide-and-conquer idea used for resumes applies here: parse structure first, extract content second. With sections labeled, Ch. 41 can pull skills out of *Qualifications* vs *Nice to have* separately, Ch. 42 knows where the duties live, and Ch. 43 knows where to hunt for degrees and years. The trade-off shown in this chapter is classic rules-vs-robustness: keyword+length heuristics are cheap and explainable, but a bullet containing a heading word can silently corrupt a bucket. This feeds directly into the skill extraction of Ch. 41.""",
})

# ============================================================
# 41 - JD Skill Extraction
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\41_jd_skill_extraction\41.ipynb", replace={
0: r"""# 41 — JD Skill Extraction
**Goal:** Extract required and preferred skills from job descriptions.

Ch. 40 split the JD into sections; this chapter harvests the *skills* from those sections. A posting mentions a handful of technologies — "Python", "TensorFlow", "SQL" — and the extractor's job is to find every mention and decide whether the skill is **required** (lives in Qualifications) or **preferred** (lives in Nice to have). The distinction is not cosmetic: it changes how a candidate is scored.

**Why it matters for resumes / ATS:** skill matching is the heart of resume–JD comparison, and the *required vs preferred* flag is what makes a match meaningful. Missing a required skill should disqualify; missing a preferred skill should only cost a few points. An ATS that flattens this distinction either rejects good candidates (preferred treated as required) or lets weak ones through (required treated as preferred). This chapter is the JD-side twin of the skill extraction performed on resumes in earlier blocks.""",
1: r"""## 1. Required vs Preferred Skills

The core idea: **a skill's section determines its weight**. A skill found in the *qualifications* bucket is required — a screening gate. The same skill in the *nice_to_have* bucket is preferred — a ranking signal. `extract_jd_skills()` checks each skill in a curated `SKILLS_DB` against each section's text and tags it accordingly.

**What the code does:**
- `SKILLS_DB` is the controlled vocabulary the extractor knows about (Python, TensorFlow, PyTorch, SQL, Spark, Docker, Kubernetes, AWS, NLP).
- It tries to reuse Ch. 40's `detect_jd_sections`; the guard is `'detect_jd_sections' in dir()` — but inside a function, `dir()` lists only *local* names, so this check is effectively always `False` and the fallback branch runs.
- The fallback places the whole JD text into both `qualifications` and `nice_to_have` buckets, so *every* found skill lands in both and is tagged **preferred**.

**Expected:** with the sample JD, `required` comes back empty and `preferred` contains `['Python', 'TensorFlow', 'PyTorch', 'SQL', 'NLP']` — all five skills the JD actually mentions (Spark/Docker/Kubernetes/AWS never appear). The intended design — skills from Qualifications → required, from Nice to have → preferred — would need `detect_jd_sections` passed in as an argument or the section logic inlined; as written, the section-aware path is dead code. The notebook also assumes Ch. 40's `jd` is still in the kernel, since the cell never redefines it.""",
3: r"""## 2. Skill Frequency Analysis

Beyond *presence*, frequency is a cheap importance signal: a skill named three times is usually more central than one named once. `skill_frequency()` counts how often each vocabulary skill appears anywhere in the JD text and ranks skills by that count.

**What the code does:**
- Builds a word-level `Counter` with `re.findall(r"\b\w+\b", ...)` for general term frequencies.
- Then, per skill, counts *substring* occurrences with `jd_text.lower().count(skill.lower())` — simpler than the regex pass and case-insensitive, but it also counts partial matches ("Python" would match inside "Pythonic").
- Returns skills sorted by count descending; the cell prints the top 8.

**Expected:** in the sample JD every listed skill is mentioned exactly once, so the ranking shows `Python`, `TensorFlow`, `PyTorch`, `SQL`, `NLP` each at `mentioned 1x`. The output is flat here because the sample is short; on a real posting a skill repeated in both About and Qualifications would float to the top — which is exactly the signal the ranking is meant to expose. Note the print slice `[:8]` just truncates the list for display.""",
5: r"""## Summary: Section-based extraction distinguishes required from preferred skills.

**Skill extraction is only as precise as the section boundaries feeding it — and the required/preferred split is a screening decision, not a display nicety.**

This chapter shows the two failure modes that plague real JD extractors: a vocabulary that silently drops unlisted skills (Spark, Docker, Kubernetes, AWS vanish because they are never mentioned — but also because the DB is finite), and a reuse guard that never fires, collapsing every skill into "preferred". The frequency pass adds a cheap importance signal on top. The extracted skills become the candidate set that Ch. 44 ranks and Ch. 46 matches against resume skills. Next, Ch. 42 extracts the *actions* a JD expects — responsibilities — using POS tagging.""",
})

# ============================================================
# 42 - Responsibility Detection
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\42_responsibility_detection\42.ipynb", replace={
0: r"""# 42 — Responsibility Detection
**Goal:** Extract key responsibilities and action items from JDs.

Responsibilities are the "what you'll do" half of a JD: bullet points like "Develop and deploy ML models at scale". Structurally they are **action phrases** — a verb plus an object — and that structure is exactly what this chapter extracts, using spaCy POS tagging (Ch. 10) and dependency relations (Ch. 11) to find verb → object pairs. The chapter also reads a second signal from the JD: the **seniority level** it implies, via keyword matching.

**Why it matters for resumes / ATS:** a resume bullet and a JD responsibility match when their action+object cores align — "reduced inference latency" (resume) vs "optimize model latency" (JD). Extracting the JD side of that pair is a prerequisite for Ch. 46's matching. Seniority is a coarser but crucial filter: a senior posting should not be matched against mid-level resumes, and keyword signals like "mentor" or "lead" often carry that information.""",
1: r"""## 1. Identifying Action Phrases

A responsibility bullet is an **action phrase**: a verb ("develop", "deploy", "mentor") and usually an object ("ML models", "junior data scientists"). spaCy tags each token's part of speech and records dependency relations, so the extractor can walk the verbs and read each verb's object off its dependency children — no regex, no manual rules.

**What the code does:**
- Loads `en_core_web_sm` and parses a five-bullet responsibilities sample.
- For every token with `pos_ == "VERB"`, looks for a child with a direct-object label (`dobj`, `pobj`, or `attr`).
- Prints the verb's **lemma** (so "deploying"/"deployed" normalize to `deploy`) and the object, or `(none)`.

**Expected:** running this on the sample yields `develop -> (none)`, `deploy -> models`, `collaborate -> (none)`, and `validate -> findings`. Two honest imperfections to learn from: (1) `develop` and `collaborate` show no object because their real objects sit behind conjunctions/prepositions ("collaborate *with* teams"); (2) bullet-initial capitalized verbs like "Mentor" and "Design" get tagged as nouns/adjectives by the tagger and are skipped entirely. The parser also mis-attaches "hypotheses" as a modifier of "findings" — dependency output is useful but not oracle-accurate on terse bullet text.""",
3: r"""## 2. Seniority Signal Detection

Job level is usually stated in the JD — "Senior", "Lead", "5+ years" — and `detect_seniority()` picks the level with a keyword sweep: a dict of level → signal phrases, checked in order, first hit wins.

**What the code does:**
- `seniority_signals` maps four levels (junior / mid / senior / manager) to phrase lists ("entry level", "3-5 years", "principal", "head of", …).
- `detect_seniority()` lowercases the whole JD once, then scans every level's signals in dict order with a plain substring `in` test.
- Returns the first level whose signal appears, or `"not specified"` if none do.

**Expected:** on the sample JD this returns **`junior`** — not because the role is junior, but because the responsibilities line "Mentor **junior** data scientists" contains "junior", and the `junior` level is checked *before* `senior` in dict order. The title says "Senior Data Scientist", yet the keyword scan never gets there. That is the classic ordering trap of first-match-wins keyword logic: signal priority is baked into dict order, and a stray mention anywhere in the document can override the header. Ordering signals by specificity (or scanning the header first) would fix it.""",
5: r"""## Summary: POS tagging extracts action verbs. Keyword matching detects seniority.

**Responsibilities are action+object pairs in disguise — and both extraction routes here are fast, transparent, and imperfect in instructive ways.**

POS+dependency extraction recovers `deploy -> models` cleanly but misses verbs the tagger mislabels and objects buried behind prepositions. Keyword seniority detection is a one-liner that works — until a single "junior" in a mentoring bullet beats "Senior" in the title, because dict order *is* priority order. Neither result is production-grade on its own; both are the right first pass. The extracted action pairs are exactly what Ch. 46 will align against resume achievement bullets, and the seniority flag can gate which resumes are even compared. Ch. 43 completes the JD picture by mining qualifications.""",
})

# ============================================================
# 43 - Qualification Detection
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\43_qualification_detection\43.ipynb", replace={
0: r"""# 43 — Qualification Detection
**Goal:** Extract degree requirements, year requirements, and certifications.

Qualifications are the *hard gates* of a JD: education level and years of experience. They are also among the most formulaic text in any posting — "MS/PhD in Computer Science", "5+ years experience" — which makes them ideal targets for **regex extraction**. This chapter pulls out (a) which degree levels are required and (b) how many years of experience, using two small, readable pattern sets.

**Why it matters for resumes / ATS:** degree and years are the closest thing a JD has to boolean filters. If the JD requires an MS and 5 years, a candidate with a BS and 2 years can be screened out *before* expensive semantic matching. Extracting these numbers as structured fields is also what lets an ATS answer recruiter queries like "show me senior ML roles that require a PhD" — and it is the natural complement to the skill and responsibility signals from Ch. 41–42.""",
1: r"""## 1. Degree Requirement Extraction

Degrees appear in many spellings — "PhD", "Ph.D.", "doctorate" — so the extractor maps every alias to one of three canonical levels: `phd`, `masters`, `bachelors`. Matching uses **word-boundary regexes** (`\b` around each alias) so that "MS" in "MS/PhD" matches while "MS" inside "MSc" or "MSc." does not.

**What the code does:**
- `degrees` is a dict of level → alias list ("masters": ["masters", "ms", "m.s.", "m.tech", "m.sc"], …).
- For each alias it builds `\b` + `re.escape(alias)` + `\b` and searches with `re.IGNORECASE`.
- A level is recorded once (the inner `break` stops after the first matching alias) and the result list preserves dict order.

**Expected:** on the sample JD — "MS/PhD in Computer Science or related field" — this returns `['phd', 'masters']`. Note the order follows the *dict* (`phd` first), not the order of appearance in the text. Both aliases match the same string because the `\b` boundaries anchor each alias independently; "MS" and "PhD" are separated by a slash, so both fire. If the JD said "Master's degree" the alias list would need "master's" added — a reminder that the vocabulary is the real product here.""",
3: r"""## 2. Experience Year Extraction

Years-of-experience requirements come in two word orders: "5+ years experience" and "experience: 5+ years". `extract_years_required()` tries **two regex patterns** in sequence and returns the first match's number, or `None` if neither fits.

**What the code does:**
- Pattern 1 anchors the number first: `(\d+)[+]?\s*years?\s+(?:of\s+)?(?:experience|exp)` — matches "5+ years experience", "3 years of experience", "2 yrs exp" variants.
- Pattern 2 anchors "experience" first and looks ahead for a number within ~20 chars: `(?:experience|exp)[^\n]{0,20}(\d+)[+]?\s*years?` — matches "experience: 5+ years".
- Returns `int(match.group(1))`; the `[+]?` handles the "+" in "5+" while `\s*` absorbs spacing.

**Expected:** on "5+ years experience in data science" the first pattern fires and the function returns `5`. A JD with no year phrasing returns `None` — a real distinction for the matcher (unknown ≠ zero years). The two-pattern design is the standard way to stay robust to word order without writing one giant regex; ranges like "5–7 years" would need a third pattern, and that is the ongoing maintenance cost of regex extraction.""",
5: r"""## Summary: Regex extracts degree and experience requirements. Combine for qualification matching.

**Degree and years are the JD's boolean filters — cheap to extract, decisive in screening — and regex is the right tool because the phrasing is formulaic.**

The two extractors show the whole regex mindset: alias dictionaries plus `\b`-anchored, case-insensitive patterns for degrees; ordered patterns plus `[+]?`-tolerant number capture for years. The verified outputs on the sample — `['phd', 'masters']` and `5` — are exactly the structured fields a matcher needs. Combining them with skills (Ch. 41) and responsibilities (Ch. 42) yields a complete JD profile: what you must know, what you must have done, and what you must hold. Ch. 44 shifts from *extraction* to *ranking* — deciding which of a JD's many keywords actually matter, via TF-IDF and embeddings.""",
})

# ============================================================
# 44 - Keyword Ranking
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\44_keyword_ranking\44.ipynb", replace={
0: r"""# 44 — Keyword Ranking
**Goal:** Rank JD keywords by importance using TF-IDF and KeyBERT.

Extraction answers "which skills appear?"; ranking answers "which ones *matter*?". A JD is dense with words, but only some are load-bearing: "Python" and "TensorFlow" define the role, while "skills" and "experience" are generic. This chapter ranks keywords two ways — **TF-IDF** (statistical distinctiveness against a corpus of other roles) and **embedding similarity** (the KeyBERT-style idea: how semantically close each keyword is to the JD's meaning).

**Why it matters for resumes / ATS:** when Ch. 46 matches a resume to a JD, every skill should count proportionally to its importance in the posting. Ranking turns "mention count" into "weight": a JD that stresses NLP should weight NLP matches more than a passing "Python" mention. TF-IDF gives a fast, interpretable ranking; embeddings catch semantic relatives (e.g. "deep learning" ↔ "neural networks") that pure term overlap would miss.""",
1: r"""## 1. TF-IDF Keyword Extraction from JD

**TF-IDF** scores a term by term frequency × inverse document frequency: a word is important if it appears often in *this* document but rarely in a comparison corpus. The cell builds a 5-document corpus — the JD plus four contrasting role descriptions (software engineer, frontend, DevOps, data analyst) — so terms unique to the JD stand out while shared filler collapses.

**What the code does:**
- `TfidfVectorizer(stop_words="english", max_features=30)` builds a 30-term vocabulary over the corpus (English stopwords removed, vocabulary capped).
- `X[0]` is the JD's row; `.toarray().flatten()` turns the sparse vector into a dense score array.
- `np.argsort(scores)[-10:][::-1]` takes the top 10 indices in descending order and prints each term with its score.

**Expected:** on the sample JD, `learning` leads (~0.51, because "machine learning" *and* "deep learning" both appear), followed by a cluster of JD-specific terms — `senior`, `scientist`, `nlp`, `python`, `deep`, `machine`, `skills`, `experience`, `required` — all near 0.26. The vocabulary cap (`max_features=30`) is the sharp edge: "TensorFlow" appears only once and gets pruned from the vocabulary entirely, so a rare-but-critical keyword can silently vanish. On a real corpus, tune `max_features` or drop it and filter by score instead.""",
3: r"""## 2. Embedding-Based Keyword Importance

TF-IDF sees characters, not meaning. **Embeddings** fix that: a sentence-transformer model (`all-MiniLM-L6-v2`) encodes the whole JD and each candidate keyword into vectors, and **cosine similarity** between the JD vector and a keyword vector measures semantic relevance — so "deep learning" and "neural networks" can reinforce each other even with zero shared tokens. This is the mechanism behind KeyBERT-style keyword extraction.

**What the code does:**
- `SentenceTransformer("all-MiniLM-L6-v2")` downloads/loads the model, then `model.encode(jd_text)` produces the JD embedding.
- Each keyword is encoded and compared with `util.cos_sim(jd_emb, kw_emb).item()`.
- The whole block sits in `try/except`: if the model is unavailable (no download, no GPU, no network), it prints "SentenceTransformer not available" and degrades gracefully.

**Expected:** with the model installed, verified similarity scores on the sample JD rank `AWS` (0.40) and `TensorFlow` (0.39) highest, then `SQL` (0.29) and `Python` (0.28), then `NLP` (0.16) — while skills absent from the JD score near zero (`Java` 0.13, `Docker` 0.07, `React` 0.07). The ranking is semantic, not lexical: "AWS" never appears in the JD text yet ranks top because it is contextually close to the ML/data stack described.""",
5: r"""## Summary: TF-IDF ranks distinctive keywords. Embedding similarity measures semantic relevance to the JD.

**Importance is a *relative* property: TF-IDF measures distinctiveness against other roles; embeddings measure closeness to the JD's meaning — and the two agree on the big picture while disagreeing in instructive ways.**

TF-IDF is instant, explainable, and free, but its vocabulary cap can drop rare keywords (TensorFlow vanished at `max_features=30`) and it cannot see synonyms. Embeddings cost a model download and a GPU-free encode pass, but they rank "AWS" top without the word appearing once. For matching, the practical blend is TF-IDF as the fast default and embeddings as the semantic check. Ch. 45 closes the JD side by classifying each requirement's *type* — must-have, preferred, or nice-to-have — the final weights Ch. 46 needs.""",
})

# ============================================================
# 45 - Requirement Classification
# ============================================================
apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_g\45_requirement_classification\45.ipynb", replace={
0: r"""# 45 — Requirement Classification
**Goal:** Classify JD requirements as must-have, nice-to-have, or preferred using zero-shot.

The final JD-side chapter labels each requirement line with its *weight class*: **must-have** (a screening gate), **nice-to-have** (a ranking bonus), or **preferred** (a soft plus). Two approaches are compared head-to-head: **zero-shot classification**, which uses a pretrained natural-language-inference model to judge each line against the three labels with no training data, and **rule-based classification**, which scans for trigger words like "preferred" or "must".

**Why it matters for resumes / ATS:** Ch. 46 cannot score a resume against a JD until each requirement knows its weight. A missing must-have should cap the score; a missing nice-to-have should barely dent it. Misclassifying "PhD preferred" as must-have would reject strong candidates who lack the degree. Zero-shot offers accuracy at the cost of a large model; rules offer instant, offline, explainable verdicts — the trade-off this chapter makes visible.""",
1: r"""## 1. Zero-Shot Classification

Zero-shot classification repurposes an **NLI (natural language inference)** model: `facebook/bart-large-mnli` was trained to decide whether one sentence *entails* another. To classify "PhD in Computer Science preferred", the pipeline treats each label ("must-have", "nice-to-have", "preferred") as a hypothesis and scores how strongly the requirement entails it — no task-specific fine-tuning needed.

**What the code does:**
- `pipeline("zero-shot-classification", model="facebook/bart-large-mnli")` builds the classifier (a multi-hundred-MB download on first use).
- Each requirement is classified against the three labels; `result['labels'][0]` and `result['scores'][0]` give the top label and its confidence.
- A `try/except` wraps everything: if transformers or the model is unavailable, it prints "Transformers not available" and falls back to a keyword rule (words like "preferred"/"plus"/"nice"/"bonus" → nice-to-have, else must-have).

**Expected:** with the model available, the classifier reads meaning rather than keywords: "5+ years experience in Python" → `must-have`; "Published research papers a plus" → `nice-to-have`; and an implicit one like "Ability to work in fast-paced environment" gets judged on content, not trigger words. The price is the download and per-line latency; in environments without the model (like a fresh offline install), the except-branch rule fallback is what actually runs.""",
3: r"""## 2. Rule-Based Classification

The rule-based alternative is a **keyword cascade**: check the soft signals first, then the hard signals, then soft-skill phrases — first hit wins, and anything unmatched defaults to must-have. It is deterministic, instant, and needs no model.

**What the code does:**
- `classify_requirement()` lowercases the text and runs three `any(w in text_lower for w in [...])` checks in priority order: soft words ("preferred", "plus", "nice", "bonus", "desired") → `nice-to-have`; hard words ("must", "required", "essential", "minimum") → `must-have`; phrase signals ("ability to", "strong") → `soft-skill`.
- Unmatched text returns `must-have` as the conservative default — better to over-require than under-require in screening.
- The loop classifies the same six requirements as the zero-shot cell, so the two approaches can be compared line by line.

**Expected:** verified on the shared list: "5+ years experience in Python" and "Experience with AWS or GCP" → `must-have`; "PhD in Computer Science preferred" and "Published research papers a plus" → `nice-to-have`; "Strong communication skills" and "Ability to work in fast-paced environment" → `soft-skill`. The cascade is transparent — every verdict traces to one trigger word — which is exactly its advantage and its limit: rephrase "preferred" as "would be great" and the rule misses it, while the zero-shot model would not.""",
5: r"""## Summary: Zero-shot is more accurate. Rule-based is faster and always available.

**Requirement weighting is the last input Ch. 46 needs — and the choice between zero-shot and rules is a real engineering trade-off, not a stylistic one.**

Zero-shot classification reads semantics and generalizes to unseen phrasing, but needs a large pretrained model and network access; rules are instant, offline, and explainable, but only as good as their trigger-word lists. The verified rule output on the six sample requirements (`must-have` for the hard gates, `nice-to-have` for "preferred"/"plus", `soft-skill` for the soft phrases) shows the cascade is a solid default, with the model as the upgrade path. This completes the JD profile: sections (Ch. 40), skills (Ch. 41), responsibilities (Ch. 42), qualifications (Ch. 43), ranked keywords (Ch. 44), and weighted requirements — ready for Ch. 46, Resume vs JD Matching.""",
})

print("ALL APPLIED")
