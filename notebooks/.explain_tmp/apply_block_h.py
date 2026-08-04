"""Expand markdown cells of block_h notebooks (46-49) following the ch11 exemplar style.
Only touches markdown cells; code cells are never modified (apply() asserts on code indexes).
"""
from nbtools import apply

# ---------------------------------------------------------------------------
# 46 — Resume vs JD Matching
# ---------------------------------------------------------------------------
nb46 = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\46_resume_vs_jd_matching\46.ipynb"

c46_0 = """# 46 — Resume vs JD Matching
**Goal:** Build a complete resume-to-job-description matcher using multiple signals.

A resume and a JD describe the same person from two directions, but they almost never use the same words. A matcher that only checks "does the resume mention Python?" is brittle: it misses synonyms, paraphrases, and the *strength* of a match. This chapter builds a `ResumeJDMatcher` that combines four independent signals — skill overlap, experience, education, and embedding similarity — into one weighted score.

**Why it matters for resumes / ATS:** an ATS's core decision is "how good is this candidate for this role?". A single-signal answer (keyword hit or miss) is easy to game and hard to debug. Weighted multi-signal scoring produces a number you can decompose into *why*: which skills matched, whether the embedding agrees, and which bonus fired. That transparency is what lets a recruiter or hiring manager trust — and tune — the system."""

c46_1 = """![Resume vs JD Matching Pipeline](../../../assets/images/resume_jd_matching_1785491166825.png)

> **Figure:** The semantic matching pipeline — resume and JD are embedded independently, then compared via cosine similarity to produce a match score and skill gap analysis.

The pipeline has three stages. **Embed:** resume and JD texts are encoded into fixed-length vectors by a sentence-transformer model (`all-MiniLM-L6-v2`). **Compare:** cosine similarity measures how close the two vectors are — the geometric proxy for "talks about the same things". **Score:** the similarity is folded into a weighted total alongside keyword-level signals (skill overlap, experience, education) so the final number reflects both *semantic* closeness and *explicit* evidence."""

c46_2 = """## 1. Multi-Signal Matching Strategy

Any single signal can lie. Keyword overlap misses synonyms and typos; embedding similarity is blind to explicit evidence like "5+ years" or "Masters"; experience and education alone say nothing about the actual skills. The fix is to **combine several weak signals** with weights and let them corroborate each other — agreement between signals is what makes a score confident.

**What the code does:** the first cell prints the weighting scheme used by the rest of the chapter:

| Signal | Weight | What it measures |
|---|---|---|
| Skill overlap | 40% | exact + fuzzy keyword matches between resume and JD skills |
| Experience level | 20% | years-of-experience evidence in the resume text |
| Education | 15% | degree keywords (Masters / PhD / Bachelor) |
| Embedding similarity | 25% | semantic closeness of the two full texts |

**Try it:** the weights sum to 100% and the largest share goes to *skills* — the signal most specific to a job. The two smallest weights (experience, education) act as tie-breakers between candidates who are otherwise skill-equivalent."""

c46_4 = """## 2. Building the Matcher

The matcher is a single class, `ResumeJDMatcher`, that keeps the model and the skill vocabulary in one place and exposes three methods: `skill_overlap()`, `embedding_match()`, and `match()`. The class is defensive by design: if the embedding model fails to load, `has_model` flips to `False` and `embedding_match()` returns a neutral 0.5 instead of crashing.

**What the code does:**
- `skill_overlap()` uses `rapidfuzz.fuzz.partial_ratio` with a > 85 threshold, so a resume skill counts as matched when it is a close fuzzy variant of a JD skill — tolerant of typos and inflections.
- `embedding_match()` truncates both texts to 512 chars before encoding, so long resumes do not blow up encode time, and returns `util.cos_sim(emb1, emb2)`.
- `match()` extracts skills by substring lookup against `skills_db`, then combines `skill_score` (0.40x), `emb_score` (0.25x), and two regex bonuses: `\\d\\+?\\s*years?` for experience and `(masters|phd|bachelor)` for education.

**Expected on the sample pair:** both regexes fire ("5+ years", "Masters"), and the resume's Python/NLP/TensorFlow are all required by the JD, so skill overlap is 3/3 and the score lands near the top of the range; the exact total depends on the embedding cosine term."""

c46_6 = """## 3. Testing on Multiple JDs

A matcher that only scores well on one hand-written pair proves nothing. The real test is the same resume run against **diverse JDs** — a data-science role it should match, and Java-backend, DevOps, and frontend roles it should mostly reject.

**What the code does:** loops over four JD strings, calls `matcher.match(resume, jd_text)` for each, and prints the score next to the JD text.

**Expected behavior:** JD 1 ("Data Scientist — Python, ML, NLP, TensorFlow") should score far above the others, because Python/NLP/TensorFlow appear on both sides — a 3/3 skill overlap worth the full 0.40. The Java-backend and frontend JDs share no skills with the resume, so their scores rest almost entirely on the embedding term plus whatever bonuses fire — a clear, interpretable gap.

**Why this matters:** the *relative ordering* across JDs is what a ranking system consumes. If the wrong JD wins, the `details` dict shows exactly which signal misled you."""

c46_8 = """## Summary: Multi-signal matching with weighted scoring. Transparent, debuggable, no black box.

The chapter assembled a working matcher from four signals: fuzzy skill overlap (40%), embedding similarity (25%), experience (20%), and education (15%). Because every component is a plain function returning a number you can print, a low score is never a mystery — `match()` returns a `details` dict with each signal's contribution and the exact skill lists found on both sides. That decomposability is the difference between a scoring *tool* and a scoring *black box*, and it is what makes the approach safe to put in front of recruiters."""

c46_key = """## Key Insight

**Match scores must be decomposable — a number without a breakdown is a guess.**

A weighted blend of skill overlap, experience, education, and embedding similarity is only useful because each signal is inspectable in isolation. When scores misrank candidates, the `details` breakdown tells you which signal was wrong and how to re-weight it. This transparency is the foundation for the rest of the block: vector search (47–48) accelerates how the embedding signal is computed at scale, and the benchmark (49) measures whether that embedding signal is trustworthy. All of it converges in Ch. 50 — ATS Rule Design."""

# ---------------------------------------------------------------------------
# 47 — FAISS Vector Search
# ---------------------------------------------------------------------------
nb47 = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\47_faiss_vector_search\47.ipynb"

c47_0 = """# 47 — FAISS Vector Search
**Goal:** Use FAISS for fast semantic similarity search over resume embeddings.

Chapter 46 computed one cosine similarity per resume–JD pair. That is fine for a handful of candidates, but an ATS may hold hundreds of thousands of resumes — brute-force comparison becomes the bottleneck. FAISS (Facebook AI Similarity Search) is a C++ library with a Python wrapper, built exactly for this: finding the nearest neighbors of a query vector in a large, high-dimensional collection in milliseconds.

**Why it matters for resumes / ATS:** "find the best 50 candidates for this JD" is a nearest-neighbor query over resume embeddings. FAISS turns it from an O(N) scan into an index lookup, and its approximate index types (IVF, HNSW) trade a little accuracy for orders of magnitude in speed — the standard trick for keeping talent search interactive at scale."""

c47_1 = """## 1. FAISS Basics

FAISS separates the **index** (the data structure holding all vectors) from the **search** (nearest-neighbor queries against that structure). Different index types sit on a speed-versus-accuracy spectrum:

| Index type | Search | Accuracy | Notes |
|---|---|---|---|
| `IndexFlatL2` | exact, brute force | best | L2 distance; O(N) per query |
| `IndexFlatIP` | exact, brute force | best | inner product; equals cosine after L2-normalizing |
| `IndexIVFFlat` | approximate | good | clusters vectors, probes only nearby clusters |
| `IndexHNSWFlat` | approximate | good–best | graph-based; fast and accurate, heavier memory |

**What the code does:** prints this design summary — FAISS's purpose, the index-type table, and the rule of thumb that `IndexFlatIP` is the right default below ~100K resumes because exact search is still fast enough."""

c47_3 = """## 2. Building a FAISS Index

Building an index is a two-step routine: pick the metric, then `add()` the vectors. The chapter uses `IndexFlatIP` (inner product) with **L2-normalized** vectors, which makes inner product equivalent to cosine similarity — the same metric Ch. 46 used for matching.

**What the code does:**
- Sets `d = 384`, the output dimension of `all-MiniLM-L6-v2`, and creates an empty `IndexFlatIP(d)`.
- Simulates 10 resume embeddings as `np.random.randn(10, d)` with a fixed seed, casts them to `float32` (FAISS requires this dtype), then normalizes each row with `faiss.normalize_L2`.
- Adds the matrix and prints `index.ntotal` and `index.d`.

**Expected:** the first print shows `ntotal = 0` with `dimension 384`; after `add()` it shows `ntotal = 10`. A real pipeline would use `model.encode()` (as in Ch. 46) instead of `randn` — the random vectors only demonstrate the mechanics."""

c47_5 = """## 3. Querying with a JD

With the index built, retrieval is one call: `index.search(query_vector, k)` returns the `k` nearest neighbors as two arrays — `scores` (the similarity values) and `indices` (which resume rows they belong to).

**What the code does:**
- Encodes the "JD" as a single random `(1, d)` vector, normalized exactly like the index contents.
- Searches with `k = 3` and prints each hit's rank, resume id, and score.

**Expected behavior:** you get 3 results ranked by descending inner product; because all vectors are unit-length, scores fall in the cosine range [-1, 1]. One caveat worth stating plainly: with random embeddings the "matches" carry no meaning — the point is the mechanics. Feeding real embeddings from Ch. 46's matcher would make the top hit the resume that genuinely talks about the same topics as the JD."""

c47_7 = """## 4. Index Persistence

An index built in memory dies with the process. FAISS persists indices to disk with `write_index()` / `read_index()`, so a nightly re-embedding job can build once and serve queries all day.

**What the code does:**
- Saves the flat index to `/tmp/resume_index.faiss` and reloads it, verifying that `ntotal` and `d` survived the round trip.
- Builds a second, approximate index: `IndexIVFFlat(quantizer, d, nlist=2, METRIC_INNER_PRODUCT)`, which partitions the space into 2 clusters. IVF **must be trained** (`ivf_index.train()`) before `add()` — the quantizer needs data to learn cluster centroids.
- Sets `nprobe = 1`, meaning each query inspects only 1 of the 2 clusters.

**Expected:** the reloaded index reports the same 10 vectors; the IVF search returns similar-but-not-necessarily-identical results to the exact search, because probing one cluster skips vectors in the other. Higher `nprobe` = more accuracy, slower queries — the core knob of approximate search."""

c47_9 = """## Summary: FAISS enables fast resume retrieval from large candidate pools. IVF scales to millions.

FAISS indexes resume embeddings once, then answers "closest resumes to this JD" in milliseconds: `IndexFlatIP` gives exact cosine search for pools up to ~100K, and `IndexIVFFlat` (or HNSW) trades a little accuracy for the ability to scale to millions by clustering and probing only nearby regions. The index is persistable, so production systems build offline and serve online. What FAISS does *not* provide is metadata handling — filtering by role, seniority, or location requires separate bookkeeping or a database layer, which is exactly the gap Ch. 48 (ChromaDB) fills."""

c47_key = """## Key Insight

**At scale, search speed is a product feature — FAISS is how you keep it interactive.**

For a candidate pool measured in thousands or millions, exact per-pair scoring (Ch. 46) stops being viable; nearest-neighbor indexes turn the same cosine similarity into a sub-linear lookup. The design lesson is the speed–accuracy trade-off: flat indexes are exact but O(N), IVF/HNSW are approximate but fast, and `nprobe` lets you dial between them per workload. This chapter's indexes store vectors only; Ch. 48 layers metadata and persistence on top, and Ch. 49 benchmarks whether the embeddings being searched are good."""

# ---------------------------------------------------------------------------
# 48 — ChromaDB
# ---------------------------------------------------------------------------
nb48 = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\48_chromadb\48.ipynb"

c48_0 = """# 48 — ChromaDB
**Goal:** Use ChromaDB for persistent vector storage with metadata filtering.

Chapter 47 ended with a fast vector index and an open gap: FAISS stores vectors, but not the structured facts attached to them — role, years of experience, skills. ChromaDB is an embedded, open-source vector database that keeps embeddings *and* their metadata together, persists them to disk, and filters queries by both at once.

**Why it matters for resumes / ATS:** real talent search is never "similar to this text" alone; it is "similar *and* senior *and* in Berlin". ChromaDB's `where` filters make that a single query rather than a two-stage post-filter, and its persistence means the resume corpus survives restarts without a re-embedding job. It is the pragmatic middle ground between raw FAISS and a hosted vector DB like Pinecone or Weaviate."""

c48_1 = """## 1. Setting Up ChromaDB

ChromaDB is a client-style library that also runs fully **embedded** — a plain Python process, no external service to install. The unit of organization is a **collection**, roughly a named table of vectors.

**What the code does:**
- Creates a `chromadb.Client` with `Settings(anonymized_telemetry=False)` to keep usage telemetry off.
- Tries `create_collection("resumes")` and falls back to `get_collection("resumes")` on error, so re-running the cell is harmless (idempotent setup).

**Try it:** the try/except pattern is the standard way to handle "collection may already exist" in scripts and notebooks. In production you would typically version collection names (`resumes_v2`) or recreate deliberately, rather than silently reusing stale data."""

c48_3 = """## 2. Adding Resumes with Metadata

The `add()` call is where ChromaDB earns its keep: one call ingests documents, their embeddings (computed automatically by ChromaDB's default embedding function when you pass text), and arbitrary metadata as a dict per row.

**What the code does:** adds three resumes with:
- `documents` — the raw resume text,
- `metadatas` — structured dicts: `role`, `years`, and a comma-joined `skills` string,
- `ids` — stable string keys (`resume_001` ...) that later `get` / `update` / `delete` calls use to address rows.

**Expected:** `collection.count()` returns 3. Notice the metadata schema is arbitrary — you could store `location`, `salary_expectation`, `last_updated`, anything you want to query later. That flexibility is what FAISS from Ch. 47 lacks out of the box."""

c48_5 = """## 3. Querying with Metadata Filtering

The payoff for storing metadata: `collection.query()` accepts `query_texts` (which it embeds internally) and a `where` filter applied **during** the search, not after it. Only vectors matching the filter are candidates, so the result count can be smaller than `n_results`.

**What the code does:**
- Queries with `query_texts=["looking for NLP expert with Python"]`, `n_results=2`, and `where={"role": "data_scientist"}`.
- Prints each returned document, its metadata, and its distance.

**Expected behavior:** exactly one document matches the filter — `resume_001` is the only row with `role == "data_scientist"` — so the loop prints a single result even though `n_results=2`; its distance reflects how close that resume text is to the query. Filters work on any metadata key, with numeric comparisons (e.g. `years > 3`) supported alongside string equality."""

c48_7 = """## 4. Updating and Deleting

Resumes change — candidates gain skills, move jobs, or withdraw. ChromaDB supports `update()` to replace a row's document and metadata, `get()` to fetch rows by id, and `delete()` to remove them.

**What the code does:**
- `update()` rewrites `resume_001` with a new document and metadata (`years` bumped from 5 to 6, `skills` trimmed) — the count is unchanged because the id is preserved.
- `get(ids=["resume_001"], include=["documents", "metadatas"])` fetches that row back to verify the new content.

**Expected:** the count stays 3 after the update, and the `get` returns the six-year version. The heading promises deletion too — in ChromaDB that is `collection.delete(ids=[...])`; it is not exercised here but follows the same id-addressed pattern."""

c48_9 = """## Summary: ChromaDB adds metadata filtering on top of vector search. Good for production MVPs.

ChromaDB delivers what FAISS left open in Ch. 47: embeddings, metadata, and persistence in one embedded package. `create_collection` / `add` / `query` / `update` / `get` cover the full CRUD cycle, and `where` filters make hybrid searches ("similar text AND role = data scientist") a single call. Because it runs in-process with zero infrastructure, it is the fastest path from prototype to a real ATS backend — you can swap in a hosted vector DB later without changing the shape of your queries."""

c48_key = """## Key Insight

**Vectors are only half the database — metadata is what makes search usable.**

A resume corpus queried purely by similarity returns noise; filtering by role, years, or skills is what turns retrieval into recruiting. ChromaDB's contribution is combining both in one query and persisting the result, at the cost of nothing but a pip install. That metadata awareness previews how a real ATS organizes candidates, and it sets up the question Ch. 49 answers: how do we know the similarity scores underneath are any good?"""

# ---------------------------------------------------------------------------
# 49 — Embedding Evaluation & Benchmark
# ---------------------------------------------------------------------------
nb49 = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_h\49_embedding_evaluation_and_benchmark\49.ipynb"

c49_0 = """# 49 — Embedding Evaluation & Benchmark
**Goal:** Build a systematic benchmark comparing embedding models on resume matching tasks.

Chapters 46–48 used `all-MiniLM-L6-v2` as the embedding model, but "it works" is not a decision criterion. Different models trade accuracy, speed, and size differently, and a model that ranks well on generic text may rank poorly on resume–JD pairs. This chapter builds a tiny, repeatable benchmark: fixed resume–JD pairs with human-judged match scores, run through any model, and summarized with one number — RMSE.

**Why it matters for resumes / ATS:** the embedding model is the foundation of every score in this block; a weak foundation caps the quality of matching, retrieval, and filtering no matter how clever the surrounding code. Benchmarking makes the choice evidence-based and, repeated over time, catches regressions when models or libraries are upgraded — a model that silently degrades is worse than one you never trusted."""

c49_1 = """## 1. Defining the Benchmark

A benchmark is only as good as its ground truth. Here, each pair is `(resume_text, jd_text, expected_score)` where `expected` is a human judgment on a 0–1 scale — how well the resume matches the JD.

**What the code does:** defines `eval_pairs` with five cases deliberately spanning the difficulty range:
- two strong matches (`0.9`, `0.8`) — Python/NLP and Java/Spring,
- one partial match (`0.6`) — DevOps vs cloud infrastructure,
- two clear mismatches (`0.2`, `0.1`) — data scientist vs frontend, project manager vs ML engineer.

**Try it:** these pairs are the test set of the chapter. Notice they stress *semantic* understanding, not keyword overlap — "Data scientist with TensorFlow" and "Frontend React developer" share almost no vocabulary, so a bag-of-words model fails where a good embedding model succeeds."""

c49_3 = """## 2. Evaluating Models

`evaluate_model()` is the harness: load a model, encode both sides of every pair, compare the cosine similarity to the human label, and reduce all errors to a single RMSE.

**What the code does:**
- For each pair: `model.encode(resume)` and `model.encode(jd)`, then `util.cos_sim(emb1, emb2).item()` — the model's predicted match score.
- Records `abs(sim - expected)` per pair and computes `RMSE = sqrt(mean((sim - expected)^2))` — lower is better, and squaring punishes large disagreements disproportionately.
- Wraps everything in `try/except`; a model that fails to load (e.g. no network for the HuggingFace download) returns `RMSE = inf` and is reported as SKIPPED rather than crashing the loop.

**Expected:** three models are attempted — `all-MiniLM-L6-v2`, `all-mpnet-base-v2`, `multi-qa-MiniLM-L6-cos-v1`. The first run downloads each from HuggingFace, so network access is required; on a machine without it you will see the SKIPPED path, which is the harness working as designed."""

c49_5 = """## 3. Results Visualization

Numbers alone are hard to compare; the chapter closes by rendering RMSE as a sorted, ASCII bar chart.

**What the code does:**
- Uses a hardcoded `results` dict (`all-MiniLM-L6-v2: 0.12`, `all-mpnet-base-v2: 0.09`, `multi-qa-MiniLM-L6-cos-v1: 0.15`) — **note these are illustrative placeholders baked into the notebook, not the output of Section 2**; in a real run you would fill this dict from `evaluate_model()` results.
- Sorts by RMSE ascending (best first) and draws `int((1 - rmse) * 20)` bar characters per model.
- Ends with the code's own takeaway: `all-mpnet-base-v2` is often the most accurate but slower, while `all-MiniLM-L6-v2` is the production speed/accuracy trade-off.

**Try it:** replace the hardcoded dict with the real scores from Section 2 and the chart updates automatically — that is the whole point of keeping the visualization separate from the evaluation."""

c49_7 = """## Summary: Systematic benchmarks prevent regression. Track RMSE across model versions.

This chapter made model choice a measurement instead of an opinion: a fixed set of human-labeled resume–JD pairs, a reusable `evaluate_model()` harness, and RMSE as the single comparison metric. The same harness rerun after a model, library, or data change tells you immediately whether the system got better or worse. That discipline is what separates a maintained ATS from a demo — the benchmark is the regression test for the entire embedding layer built in Ch. 46–48."""

c49_key = """## Key Insight

**Benchmark before you trust — an embedding model is a scored hypothesis, not a fact.**

RMSE over a small human-labeled pair set is a proxy for matching quality, and tracking it across model versions turns "which model?" into a number, not a preference. The practical winner is usually a speed/accuracy compromise: `all-MiniLM-L6-v2` for production latency, heavier models like `all-mpnet-base-v2` when quality dominates. With retrieval (47), storage (48), and evaluation (49) in place, Ch. 50 — ATS Rule Design — assembles them into the screening rules a hiring system enforces."""

# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
apply(nb46, replace={0: c46_0, 1: c46_1, 2: c46_2, 4: c46_4, 6: c46_6, 8: c46_8}, append=[c46_key])
apply(nb47, replace={0: c47_0, 1: c47_1, 3: c47_3, 5: c47_5, 7: c47_7, 9: c47_9}, append=[c47_key])
apply(nb48, replace={0: c48_0, 1: c48_1, 3: c48_3, 5: c48_5, 7: c48_7, 9: c48_9}, append=[c48_key])
apply(nb49, replace={0: c49_0, 1: c49_1, 3: c49_3, 5: c49_5, 7: c49_7}, append=[c49_key])

print("All 4 notebooks applied OK")
