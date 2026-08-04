"""Expand markdown cells of the 5 block_d notebooks (ch21-25) in the ch11 exemplar style.
Only touches markdown cell sources. Code cells are asserted untouched by nbtools.apply."""
from nbtools import apply

# ============================= 21 GloVe =============================
MD21_0 = r"""# 21 — GloVe
**Goal:** Understand global word co-occurrence embeddings and load pre-trained vectors.

GloVe ("Global Vectors") is a **count-based** embedding family: it builds a global word–word co-occurrence matrix over a huge corpus, then factorizes it so each word gets a dense vector whose geometry mirrors co-occurrence statistics. Unlike the predictive Word2Vec of Ch. 19, GloVe's signal comes from *global* counts rather than sliding-window context, which tends to give cleaner behavior on similarity tasks.

**Why it matters for resumes / ATS:** pre-trained GloVe vectors are an instant, dependency-free skill-similarity layer — no training data, no GPU. A matcher can compare `tensorflow` to related words or normalize synonyms by cosine distance instead of exact string match. It is the cheap, fast baseline that the rest of Block D (Ch. 22–24) builds on and then beats."""

MD21_1 = r"""## 1. How GloVe Works

The key insight: the **ratio** of co-occurrence probabilities carries meaning, not the raw counts. If `P(k | ice)` is much larger than `P(k | steam)`, then word `k` behaves like "solid" (ice-like); the reverse picks out "gas"; when the two probabilities are nearly equal (`water`), the word is uninformative for distinguishing the pair. GloVe learns vectors whose dot products reproduce these log-probability ratios across the whole vocabulary.

**What the code does:** this cell is a pure-print cheat-sheet, not a model. It restates the core idea, walks through the ice/steam example as a preview of the math, and ends by hammering the takeaway: the co-occurrence *probability ratio* — not the raw count — is what encodes meaning.

**Try it:** the `solid` / `gas` / `water` trio is the classic illustration from the GloVe paper. Once §2 loads the vectors, probe it directly with `glove.most_similar(positive=["ice"], negative=["steam"])` and see which of the three ranks highest."""

MD21_3 = r"""## 2. Loading Pre-trained GloVe

`gensim.downloader` fetches ready-made vectors over HTTP and caches them locally, so "loading GloVe" is a one-liner. The notebook uses `glove-twitter-25`: 25 dimensions, trained on ~2B tweets — small enough to download fast (~105 MB) and probe interactively.

**What the code does:** `api.load("glove-twitter-25")` downloads on first use, then:
- prints the vocabulary size — `len(glove)` gives **1,193,514** tokens on the reference run;
- prints `glove['python'].shape` — a 25-dimensional vector `(25,)`;
- prints the first 10 dimensions of `python`'s vector — raw floats such as `-0.256 -0.223 0.026 0.229 ...` (Twitter vectors are not normalized to a pretty range).

If the download fails, the `except ValueError` branch lists every model `api.info()` knows about so you can pick a different one.

**Try it:** swap the model string for `glove-wiki-gigaword-100` — 100 dims trained on Wikipedia, noticeably better on technical/professional language, at the cost of a larger download."""

MD21_5 = r"""## 3. GloVe Word Similarity

`most_similar(w)` returns the vocabulary's highest **cosine similarity** neighbors of `w` — the words geometrically closest to it. That single call is the whole "semantic search" primitive: no synonym list, no regex, just vector distance.

**What the code does:** loops `["python", "java", "data", "science", "engineer"]` and prints the top-3 neighbors of each. The reference run on `glove-twitter-25` printed:

| Query | Top neighbors (score) |
|---|---|
| `python` | matrix (0.873), electronic (0.859), osx (0.858) |
| `java` | drupal (0.886), linux (0.867), electronic (0.858) |
| `data` | mobile (0.898), software (0.867), search (0.863) |
| `science` | english (0.920), research (0.918), psychology (0.911) |
| `engineer` | specialist (0.958), developer (0.955), administrator (0.943) |

Two honest observations: `engineer → specialist/developer` is exactly the resume-relevant signal we want, but the Twitter corpus is noisy (`science → english`, `python → matrix`). For professional text, §2's `glove-wiki-gigaword-100` behaves better. The `except NameError` guard only fires if §2 never ran in this session."""

MD21_7 = r"""## 4. GloVe Analogies

Word-vector arithmetic encodes relations: if `king − man + woman ≈ queen`, then adding and subtracting vectors moves you along a semantic axis. `most_similar(positive=[...], negative=[...])` implements exactly that — positives are added, negatives subtracted, and the closest vocabulary words are returned.

**What the code does:** computes `python + developer − language` and prints the top-3. On the reference run with `glove-twitter-25` the result was **vmware (0.896), cnc (0.876), hyperion (0.854)** — not the textbook "programmer" answer. That is the lesson: analogies are *corpus-dependent*, and a 25-d Twitter model is too small and too colloquial to reproduce clean relations. The `except NameError` branch prints the intended concept (`python − language + developer → programmer`) for sessions where §2 never loaded the vectors.

**Try it:** the classic `berlin − germany + france ≈ paris` relation fails on many small models too — run it and watch the answer change with the corpus."""

MD21_9 = r"""## 5. GloVe vs Word2Vec — When to Use Which

Both families produce **static** (context-free) word vectors; they differ in *how* they learn them. Word2Vec is **predictive** — a shallow network learns to guess a word from its neighbors, so it trains fast and works on small corpora. GloVe is **count-based** — it factorizes the global co-occurrence matrix, so it needs the full corpus statistics but often yields smoother similarity behavior.

**What the code does:** prints a side-by-side comparison table (type, training signal, speed, memory, pre-trained availability). The practical translation for this project:

| Situation | Choose |
|---|---|
| Tiny corpus, fast iteration, local training | Word2Vec (Ch. 19) |
| Pre-trained quality, similarity tasks | GloVe (this chapter) |
| Phrases, OOV words, context sensitivity | Sentence Transformers (Ch. 22) |

For resume analysis the printed verdict is right: GloVe's global statistics usually beat Word2Vec on *skill similarity* — but both lose to contextual models once phrases and abbreviations enter the picture."""

MD21_11 = r"""## Key Insight: GloVe captures global word statistics. Use pre-trained for resume similarity tasks.

**Static vectors are the cheapest semantic layer you can bolt onto a matcher — load them, don't train them.**

GloVe turns co-occurrence statistics into geometry: `engineer` sits near `specialist` and `developer`, and a cosine threshold becomes an "is this skill close enough" test with zero training data. The cost is that vectors are frozen per word — no phrase handling, no context, no OOV coverage. That is exactly what Ch. 22's Sentence Transformers fix, and Ch. 23 benchmarks both families head-to-head on resume-specific pairs."""

# ============================= 22 Sentence Transformers =============================
MD22_0 = r"""# 22 — Sentence Transformers
**Goal:** Generate dense sentence embeddings using transformer models.

A sentence embedding is one dense vector (384 or 768 dims) that represents the *meaning* of a whole sentence. Sentence Transformers fine-tune a BERT-style model with a pooling layer on top, so "Python is great for NLP" and "I love Python" land close together even though they share almost no words. This is the step up from Ch. 21: GloVe gives one vector per *word*; here we get one vector per *sentence*.

**Why it matters for resumes / ATS:** the core ATS operation is matching a resume line against a job-description line, and those rarely share exact vocabulary ("ML" vs "machine learning", "pytorch" vs "torch"). Sentence-level embeddings make that comparison semantic instead of lexical — and the resume-vs-JD cells in this chapter are the template the rest of the project builds on."""

MD22_1 = r"""## 1. What is a Sentence Embedding?

A sentence embedding compresses a variable-length sentence into a **fixed-size vector**: the transformer encodes each token, then a pooling layer (mean or CLS) collapses them into one vector. Fixed size matters — downstream code (similarity, clustering, storage) never needs to know how long the input was.

**What the code does:** prints a cheat-sheet contrasting sentence embeddings with BoW/TF-IDF:
- **semantics, not keyword overlap** — paraphrases get high similarity;
- **fixed-size vector** regardless of sentence length;
- dimension is model-specific: `all-MiniLM-L6-v2` → 384, larger models → 768+.

**Why it matters for resumes / ATS:** a skills line "Python, TensorFlow, SQL" and a JD line "experience with Python and deep learning frameworks" produce close vectors even with one word in common — BoW cosine would score them near zero."""

MD22_3 = r"""## 2. Loading Sentence Transformers

`SentenceTransformer("all-MiniLM-L6-v2")` loads a pre-trained model (first call downloads ~90 MB) and wraps encoding, pooling, and normalization behind one object. MiniLM-L6 is this project's workhorse: 6 transformer layers, 384-dim output, fast on CPU.

**What the code does:** loads the model, reports its configuration, then encodes one resume phrase:
- `model.max_seq_length` — expected **256** (the model's documented truncation limit);
- `model.get_sentence_embedding_dimension()` — expected **384**;
- `model.encode("Python developer with NLP experience")` — a single vector of shape `(384,)`, and the cell prints its first 5 values (model-specific floats, roughly in `[-1, 1]`).

**Try it:** swap in `"all-mpnet-base-v2"` (768 dims, better quality, ~2× slower) or `"paraphrase-MiniLM-L6-v2"` (tuned for paraphrase similarity) and compare the reported numbers."""

MD22_5 = r"""## 3. Semantic Similarity

Semantic similarity = **cosine similarity** between two sentence embeddings. `util.cos_sim(A, B)` returns a matrix of pairwise scores; it is the one primitive the whole matching stack reduces to.

**What the code does:** encodes four resume-like sentences, computes the full 4×4 matrix via `util.cos_sim(embeddings, embeddings)`, and prints each pair once with a ✓ marker when similarity exceeds **0.5**. Expected ranking:
- S1 (Python + ML) vs S2 (data scientist, Python + NLP) — **highest**: both are Python/ML profiles;
- S1 vs S3 (Java backend, Spring Boot) — **lowest**: disjoint skills;
- S3 vs S4 (ML engineer, deep learning) — in between: shared "engineer/ML" flavor, different tools.

The 0.5 threshold is a guess, not a law — production pipelines tune it on labeled data, and Ch. 23 gives the tooling for exactly that."""

MD22_7 = r"""## 4. Resume vs JD Matching with Sentence Transformers

This is the production use case in miniature: one resume embedding, several job embeddings, pick the highest cosine. No keyword lists, no hand-written rules — the model does the semantic work.

**What the code does:** encodes a data-science resume and three jobs, then `util.cos_sim(res_emb, job_embs)[0]` extracts the row of scores. It prints each job with `✓✓` when the score exceeds 0.5. Expected outcome:
- Job 1 (Data Scientist — Python, ML, NLP, TensorFlow) — **highest**: overlaps the resume on nearly every term;
- Job 3 (ML Engineer — Deep Learning, PyTorch, MLOps) — second: same neighborhood, different tooling;
- Job 2 (Java Backend — Spring, Microservices, AWS) — **lowest**: unrelated stack.

**Try it:** add a job that mentions the same tools in a different domain ("Python automation tester") and watch the score drop — the model separates "Python as ML" from "Python as glue code"."""

MD22_9 = r"""## 5. Finding the Best Matching Resume Section

Ranking whole resumes is coarse — recruiters also want to know *which part* of a resume matched. The fix: embed each section separately and compare it to the JD.

**What the code does:** stores four sections (`summary`, `experience`, `skills`, `education`) in a dict, encodes the JD once, then encodes each section and prints its cosine vs the JD. Expected ordering:
- `skills` ("Python, TensorFlow, PyTorch, SQL, AWS") and `summary` ("data scientist with Python and ML") — **top**: direct hits on the JD's "Python ML engineer with NLP and cloud";
- `experience` — middle: mentions NLP but also off-topic detail;
- `education` ("M.S. Computer Science, Stanford") — **lowest**: no skill terms at all.

Section-level matching is how a real ATS answers "why did this resume match?" — each score becomes an explainable highlight."""

MD22_11 = r"""## Key Insight: Sentence Transformers are the gold standard for semantic matching. The rest of this project uses them extensively.

**One model, one primitive — cosine over sentence embeddings — replaces keyword matching, synonym lists, and hand-tuned rules.**

The chapter's three patterns (pairwise similarity, resume-vs-JD, section-vs-JD) cover most of what a semantic ATS needs, and the 0.5 thresholds are deliberately arbitrary. Ch. 23 turns those choices into evidence: it benchmarks Sentence Transformers against Ch. 19/21's static vectors on resume-specific pairs, so the model pick and threshold become measured decisions instead of guesses."""

# ============================= 23 Embedding Benchmarks =============================
MD23_0 = r"""# 23 — Embedding Benchmarks
**Goal:** Compare Word2Vec, GloVe, and Sentence Transformers on resume-specific tasks.

Chapters 19–22 each claimed their embeddings capture "meaning". This chapter stops trusting claims: it defines a tiny hand-labeled benchmark of resume-skill pairs, runs every model through the same pairs, and lets cosine similarity speak. The benchmark is mini by design — six pairs, a handful of models — but the *methodology* is the deliverable: fixed pairs, expected ratings, one scoring function.

**Why it matters for resumes / ATS:** an embedding choice is a product decision. Sentence Transformers cost a ~90 MB model and CPU time per call; GloVe is instant but weak on phrases and out-of-vocabulary words. Measuring both on *resume-specific* pairs (acronym vs full form, related tools, unrelated words) tells you which failure modes you are buying into before you ship the matcher."""

MD23_1 = r"""## 1. Building a Mini Benchmark

A benchmark is just: fixed inputs, expected outputs, and a scoring rule. The test pairs here encode the failure modes a resume matcher actually faces — the same skill in different casing ("python" vs "Python programming"), related-but-different ("tensorflow" vs "deep learning"), acronym vs full form ("nlp" vs "natural language processing"), and a hard negative ("python" vs "cooking").

**What the code does:** `test_pairs` holds `(w1, w2, expected_rating)` tuples with ratings from 0.0 (unrelated) to 0.9 (same skill). `evaluate_embeddings()` looks both words up in a dict of vectors, computes `cosine_similarity`, and appends only pairs where both words exist — missing words are **skipped silently by design**. The cell prints a status line; note the helper is scaffold — §3's real loop duplicates this logic inline rather than calling `evaluate_embeddings`."""

MD23_3 = r"""## 2. Loading All Models

The benchmark needs every embedding family behind one dict so the scoring loop treats them uniformly. Note what this cell actually loads — and what it doesn't: Sentence Transformers and GloVe. **Word2Vec is named in the chapter title but never loaded here** — gensim's `word2vec-google-news-300` is a ~1.6 GB download, so the notebook skips it and the Summary's "Word2Vec" refers conceptually to Ch. 19's locally trained toy model.

**What the code does:** two `try/except` blocks append to `models`:
- `SentenceTransformer("all-MiniLM-L6-v2")` under the key `"SentenceTransformer"` (needs `pip install sentence-transformers`);
- `api.load("glove-twitter-25")` under its model name (first use downloads ~105 MB).

It finally prints how many models made it in. Expected: **2** when both dependencies are installed, fewer otherwise — the guards exist so a missing library degrades to a warning, not a crash."""

MD23_5 = r"""## 3. Running the Benchmark

The loop dispatches on API shape: sentence transformers expose `.encode()` (text in, vector out); gensim keyed vectors are indexed directly with `model[w]` (word in, vector out). Both produce a vector, so the same `cosine_similarity` call scores them.

**What the code does:** for each model, for each pair: encode/index both words, cosine, print with the expected rating. Two behaviors to expect:

- **Sentence Transformer handles everything** — it embeds phrases ("Python programming", "deep learning", "natural language processing") as full sentences, so all six pairs produce scores. Expected ordering: `nlp` vs "natural language processing" and `tensorflow` vs "deep learning" high; `python` vs "Java" low; `python` vs "cooking" lowest.
- **GloVe fails loudly on phrases** — keyed-vector lookup of a multi-word string raises `KeyError`, which the `except` prints as `ERROR` lines; the same happens for casing or rare tokens outside the Twitter vocabulary. That OOV gap is the single strongest argument for context-aware models.

If `models` ends up empty, the cell prints setup guidance instead of crashing."""

MD23_7 = r"""## Key Insight: Sentence Transformers > GloVe > Word2Vec for most resume tasks. But all have use cases.

**Benchmarking embeds the model choice in evidence — same pairs, same metric, every family.**

The measured story: sentence transformers score every pair (phrases, acronyms, casing included) while static GloVe vectors throw `KeyError` on anything outside their vocabulary — but GloVe stays useful when latency and memory matter and the vocabulary covers the domain. Ch. 24 changes the game again: zero-shot classification attacks a different problem (labeling text into categories) with NLI models, where no embedding-similarity benchmark applies at all."""

# ============================= 24 Zero-Shot Classification =============================
MD24_0 = r"""# 24 — Zero-Shot Classification
**Goal:** Classify text into categories without any training data.

Zero-shot classification labels text with categories the model has *never been trained on*. Instead of learning a classifier, it reuses **Natural Language Inference (NLI)**: the model decides whether a candidate label's claim ("This text is about Data Science") is entailed by the input. No labeled data, no fine-tuning — just a list of candidate labels per query.

**Why it matters for resumes / ATS:** resume data arrives unlabeled — sections, skill types, and JD-requirement severity all need categories, and hand-labeling costs time and drifts between job markets. Zero-shot turns every classification problem into a label-engineering problem: write good candidate labels and the model sorts the text. That is the difference between a hard-coded section regex and a classifier that understands "Published 5 papers…" is Publications."""

MD24_1 = r"""## 1. What is Zero-Shot Classification?

NLI asks: given a **premise** (the text) and a **hypothesis** (a label phrased as a claim), does the premise entail the hypothesis? Zero-shot classification scores every label's hypothesis against the text and returns the scores — the best label wins. The trick is that entailment reasoning transfers: the model doesn't "recognize" TensorFlow, it reasons that "Built ML models with TensorFlow" implies "This is about machine learning".

**What the code does:** prints a cheat-sheet showing the premise/hypothesis mechanics and lists the resume use cases this chapter exercises: section classification (Experience/Education/Skills), skill categorization (technical/soft/tool/domain), requirement severity (must-have/nice-to-have), and seniority detection. The 0.92 score in the example is illustrative — real scores depend on model and text.

**Why it matters for resumes / ATS:** one model, no training loop, and the label list is the entire "config" — swap `["must-have", "nice-to-have", "preferred"]` for `["Junior", "Mid", "Senior", "Lead"]` and the same pipeline classifies something completely different."""

MD24_3 = r"""## 2. Setting Up the Pipeline

`transformers.pipeline("zero-shot-classification")` bundles model + tokenizer + scoring into one callable. The default here is `facebook/bart-large-mnli` — a BART model fine-tuned on the MultiNLI entailment corpus — the standard zero-shot workhorse (~1.6 GB on first download, CPU-friendly at inference).

**What the code does:** loads the pipeline, then classifies one resume line ("Built NLP pipelines processing 10M documents daily using Python and TensorFlow") against four labels. `result['labels']` and `result['scores']` come back **sorted best-first**, and the scores are normalized to sum to 1. Expected: **Data Science** first — the text is dense with ML/NLP vocabulary — with Software Engineering second, and Management/Research trailing; the print loop shows all four with their scores.

**Try it:** add `"Data Engineering"` as a fifth label and watch the score mass redistribute — labels compete, so adding a strong candidate lowers the others."""

MD24_5 = r"""## 3. Resume Section Classification

Section detection is usually regex-driven ("EDUCATION" headers) and breaks the moment formatting varies. Zero-shot sectioning replaces the regex with semantics: any line can be scored against the section vocabulary.

**What the code does:** four resume lines, each tagged with its true section, are classified against five categories (`Experience`, `Education`, `Skills`, `Publications`, `Summary`). The cell prints predicted vs true with a ✓ when they agree. Expected: all four lines classified correctly — "Senior Data Scientist at Google, 2020-Present" → **Experience**, "M.S. in Computer Science, Stanford University" → **Education**, the bare skill list → **Skills**, and "Published 5 papers in top-tier NLP conferences" → **Publications**. The cues the model leans on (dates/companies vs degrees vs tool lists) are exactly the ones a human reader uses.

**Try it:** reorder `categories` and note the prediction is stable — zero-shot output depends on label *wording*, not label order."""

MD24_7 = r"""## 4. Skill Category Detection

Skill taxonomies (technical / soft / tool / domain) are a classic hand-curated list that rots over time. Zero-shot categorizes individual skills against the taxonomy with no list maintenance.

**What the code does:** eight skills are each classified against `["technical", "soft skill", "tool", "domain knowledge"]`; the top label and its confidence are printed. Expected pattern:
- **technical** — Python, TensorFlow, PyTorch;
- **soft skill** — Team Leadership, Communication, Project Management, Critical Thinking;
- **tool** — Docker (and Kubernetes-adjacent infrastructure);
- **domain knowledge** — little or nothing in this list.

The honest caveat: single-word inputs give the NLI model almost no context, so expect **lower confidence** for short skills like "Python" than for the sentence-length examples of §2–3. Zero-shot is strongest on text that carries its own context."""

MD24_9 = r"""## 5. Requirement Classification

JDs mix hard requirements ("5+ years Python"), soft asks ("strong communication"), and hedged preferences ("PhD preferred"). Sorting these automatically changes what a matcher can promise — must-haves gate, nice-to-haves rank.

**What the code does:** five JD requirements are classified against `["must-have", "nice-to-have", "preferred"]`. Expected:
- "5+ years experience in Python" → **must-have**;
- "Experience with AWS or GCP" → **must-have**;
- "Strong communication skills" → **nice-to-have** (or must-have — the boundary is fuzzy);
- "Ability to work in fast-paced environment" → **nice-to-have**;
- "PhD in Computer Science preferred" → **preferred** — the word "preferred" in the input is the strongest cue the model can get.

The fuzzier cases are the interesting ones: severity is genuinely ambiguous, and the confidence score tells you when to route to a human instead of auto-deciding."""

MD24_11 = r"""## Key Insight: Zero-shot classification works surprisingly well for resume tasks. Requires no training data.

**NLI turns classification into label engineering — the label list is the only thing you tune.**

One `pipeline` call labels sections, skills, and JD requirements without a single labeled example, and the same model is reused across all three tasks by swapping candidate labels. The limits are real: short inputs get lower confidence, and label wording matters more than label order. Ch. 25 keeps this in perspective — a classifier is only as production-ready as the error handling around it, which is exactly the next chapter's subject."""

# ============================= 25 Error Handling in NLP =============================
MD25_0 = r"""# 25 — Error Handling in NLP
**Goal:** Build robust NLP pipelines that handle real-world messy data.

Every chapter so far assumed clean text. Real resumes are not clean: empty files, binary payloads, wrong encodings, all-caps walls, and stray control characters arrive from PDF/DOCX extractors and email attachments. This chapter is the reality check — it enumerates the failure modes, then builds decoding, fallback, and validation layers that let a pipeline *degrade gracefully* instead of crash.

**Why it matters for resumes / ATS:** a parser that throws on one malformed resume fails the whole batch — or worse, silently writes garbage into the candidate record. Defensive coding here is the difference between a demo and a product: the layers built in this chapter (safe decode → fallback NLP → validate → flag) are exactly what Ch. 26–27's PDF/DOCX pipelines will need, since document extractors are the messiest input source of all."""

MD25_1 = r"""## 1. Common Resume Parsing Failures

Before defending, enumerate the enemy. Each failure mode here is a real artifact of resume ingestion: empty documents (scanned-but-blank pages), binary fragments (wrong file type opened as text), non-UTF-8 encodings (latin-1 "José" mangled by a Windows extractor), all-caps text (poorly OCR'd headers), missing section structure, and punctuation-only noise.

**What the code does:** builds `error_cases`, a list of `(name, text)` pairs, and prints each with `repr(text[:30])`. The `repr` matters: it shows escape sequences literally, so `"\x00\x01\x02\x03"` prints as backslash-escapes rather than invisible control characters, and `"Jos\xe9"` reveals the latin-1 byte that UTF-8 decoding will reject. The cell only *surveys* the cases; §2–5 build the defenses.

**Try it:** append your own worst case — a resume with an emoji, a lone `\xff` byte, or a 1 MB single line — and watch each later handler deal with it."""

MD25_3 = r"""## 2. Safe Encoding Handler

Text arrives as bytes, and bytes have no encoding until you say so. UTF-8 is the sane default, but real documents arrive in latin-1, cp1252, or worse. The fix is a **fallback chain**: try the standard, detect on failure, degrade to lossy as a last resort.

**What the code does:** `safe_decode(data)` implements the chain:
1. empty bytes → `""` (no error, no work);
2. `data.decode("utf-8")` — the happy path;
3. on `UnicodeDecodeError`, `chardet.detect(data)` guesses the encoding and prints a warning with its **confidence**;
4. decode with the detected encoding;
5. if even that fails, `decode("utf-8", errors="ignore")` — lossy but never crashing.

Reference run on `b"Jos\xe9's r\xe9sum\xe9"`: chardet guessed `cp1250` at confidence **0.08** (low — short strings give a detector almost nothing to work with), and the function still returned `"José's résumé"` correctly, since cp1250 maps byte `0xE9` to `é`. The lesson: detection is a guess, so always keep the `errors="ignore"` safety net."""

MD25_5 = r"""## 3. Graceful NLP Pipeline with Fallbacks

Model failures are a second failure class: the spaCy model may be missing, or a pathological input may make it produce nothing usable. `RobustNLPPipeline` wraps every step so the pipeline keeps producing *something*.

**What the code does:** in `__init__`, `spacy.load("en_core_web_sm")` runs inside `try/except OSError` — a missing model means `spacy_ok=False` and regex-only mode. `extract_entities` then:
- returns `[]` for blank/whitespace input;
- runs spaCy on `text[:100000]` (a hard cap against OOM on huge documents), catching any exception;
- **only if spaCy returned nothing**, falls back to regex patterns for EMAIL / URL / PHONE.

The reference run exposes the design's blind spot: on `"Contact: john@email.com, Phone: +1-555-1234"` the small spaCy model produced `[('Phone', 'ORG'), ('+1-555-1234', 'NORP')]` — wrong labels, and it missed the email entirely — but because the entity list was *non-empty*, the regex fallback never ran. A production version should merge and validate rather than trust the first non-empty result."""

MD25_7 = r"""## 4. Validation Layer for Extracted Data

Extraction produces strings; the database wants typed, normalized values. Validation is the gate that rejects nonsense before it poisons downstream matching — an email like "not-an-email" or a year like "12" should never reach the profile store.

**What the code does:** three validators, each returning the cleaned value or `None`:
- `validate_email` — strip, lowercase, then a full regex anchored with `^...$`;
- `validate_phone` — keeps only digits and `+`, then requires **7–15** characters;
- `validate_year` — parses to int, accepts only **1950–2030**.

The test loop feeds each input through all three validators and prints the first that accepts it. Reference run: `john@email.com` → valid email; `not-an-email` → invalid; `+1-555-123-4567` → `+15551234567` (13 digits — the test table's masked `+155****4567` is a display label; the function returns the full string); `12` → invalid everywhere; `2020` → year `2020`."""

MD25_9 = r"""## 5. Empty Section Detection

The last failure mode is structural: a resume with headers but no content — "Skills" followed by nothing. A matcher that reads an empty section as "no skills listed" silently discounts the candidate; flagging it keeps the record honest.

**What the code does:** `detect_empty_sections(text)` splits on `\n(?=[A-Z][A-Za-z /]+\n)` — a lookahead that cuts *before* any line shaped like a section header (capitalized, letters/spaces/slashes). For each part it treats line 0 as the header and counts lines longer than **10 chars** as content; a header with no such lines is reported empty. On the sample resume the reference run flags **Skills, Education, and Certifications** while keeping Professional Summary and Experience (their content lines exceed 10 chars).

**Try it:** the `len(l) > 10` threshold is arbitrary — drop it to 5 and a one-word placeholder like "N/A" suddenly counts as real content. That false-positive/false-negative trade-off is the kind of knob this chapter wants you to notice."""

MD25_11 = r"""## Key Insight: Production NLP needs error handling at every stage. Defensive coding prevents pipeline failures.

**Robustness is a pipeline property, not a library feature — decode safely, fall back, validate, then flag.**

Each layer answers one question: can it crash? (decode: never), can it degrade? (NLP: regex fallback), can it lie? (validators return `None`), can it hide? (empty-section detection flags). The honest caveat from §3 — a fallback that only runs when the primary path returns *nothing* — is the classic production bug. Ch. 26–27 carry these layers into PDF and DOCX parsing, where binary formats and extractor quirks make every one of them mandatory."""

apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\21_glove\21.ipynb",
      replace={0: MD21_0, 1: MD21_1, 3: MD21_3, 5: MD21_5, 7: MD21_7, 9: MD21_9, 11: MD21_11})
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\22_sentence_transformers\22.ipynb",
      replace={0: MD22_0, 1: MD22_1, 3: MD22_3, 5: MD22_5, 7: MD22_7, 9: MD22_9, 11: MD22_11})
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\23_embedding_benchmarks\23.ipynb",
      replace={0: MD23_0, 1: MD23_1, 3: MD23_3, 5: MD23_5, 7: MD23_7})
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\24_zero-shot_classification\24.ipynb",
      replace={0: MD24_0, 1: MD24_1, 3: MD24_3, 5: MD24_5, 7: MD24_7, 9: MD24_9, 11: MD24_11})
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_d\25_error_handling_in_nlp\25.ipynb",
      replace={0: MD25_0, 1: MD25_1, 3: MD25_3, 5: MD25_5, 7: MD25_7, 9: MD25_9, 11: MD25_11})
print("all block_d notebooks updated")
