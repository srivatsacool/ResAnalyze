# -*- coding: utf-8 -*-
from nbtools import apply

# ============ NB13 — Chunking & Phrase Extraction ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\13_chunking_and_phrase_extraction\13.ipynb", replace={
0: """# 13 — Chunking & Phrase Extraction

Chunking groups tokens into multi-word units that carry a single meaning: "deep learning expertise" is one chunk, not four unrelated words. Where Ch. 10 tagged parts of speech and Ch. 11 mapped dependencies, this chapter turns that structure into the phrase-level units that skills and job titles are actually made of.

**Why it matters for resumes / ATS:** skill phrases, job titles, and tool names are almost always multi-word ("machine learning", "computer vision", "Senior Data Scientist"). A keyword matcher that only sees single tokens either misses them or matches them spuriously. Chunking gives an ATS clean, complete phrases to index and match.""",
1: """**Goal:** Extract meaningful multi-word phrases (noun chunks, verb phrases) from text.

A resume's signal lives in phrases, not isolated words. This chapter uses spaCy's dependency parse (Ch. 11) to pull out noun chunks (skills, titles) and verb phrases (actions + objects), then shows how phrase-level indexing beats token-level matching for skill lookup.""",
2: """## 1. Noun Chunks with spaCy

A **noun chunk** is a noun plus its modifiers: "Senior data scientist" is one chunk rooted at *scientist*. spaCy builds these directly from the dependency tree via `doc.noun_chunks` — no grammar rules of your own.

**What the code does:** loads `en_core_web_sm`, parses a resume-style sentence, and prints each chunk with its root word and POS tag.
- `'Senior data scientist'` → root `scientist` (NOUN) — the title phrase, exactly as a recruiter would write it.
- `'strong Python skills'` → root `skills` (NOUN); `'deep learning expertise'` → root `expertise` (NOUN).

**Try it:** watch the chunk boundaries — "deep learning" stays together inside "deep learning expertise" instead of being split into separate tokens.""",
4: """## 2. Extracting Skill Phrases from Resumes

Filtering chunks by their root's POS is a cheap, effective skill extractor: keep chunks whose root is a `NOUN` or `PROPN` (proper noun) and you keep skills and tools while dropping descriptive filler.

**What the code does:** `extract_phrases()` runs each sample resume through the pipeline and keeps only noun/proper-noun-rooted chunks.
- "Expert in Python, Machine Learning, and Deep Learning" → `['Expert', 'Python', 'Machine Learning', 'Deep Learning']` — multi-word skills preserved intact.
- "Proficient with TensorFlow, PyTorch, and Cloud Computing" → `['TensorFlow', 'PyTorch']` — "Cloud Computing" is dropped because its root's POS isn't NOUN/PROPN; a production extractor would tune this filter.

**Try it:** the second resume ("Natural Language Processing and Computer Vision") collapses into one long chunk — spaCy's coordination behavior across "and". Know this when you clean output.""",
6: """## 3. Verb Phrase (Action + Object) Extraction

Resume bullets are (action → object) pairs: "Developed ML models", "led teams". Extracting the verb and its direct object gives you the structured achievement unit from Ch. 11's SVO idea, at phrase level.

**What the code does:** `verb_phrases()` iterates tokens; for each `VERB` it looks for a `dobj` (direct object) and a `prep` (preposition) among the verb's children, returning `(verb, object, preposition)`.
- `"Developed ML models with TensorFlow and led teams"` → `[('Developed', None, None), ('led', 'teams', None)]`.

**Try it:** observe the honest failure mode — sentence-initial "Developed" is parsed as a modifier of "models", so it has no `dobj` child and yields `(None, None)`. Parsers are imperfect; production code should fall back to lemmas and accept participle readings.""",
8: """## 4. Keyword Chunking for Resume Search

The payoff: a chunk-level index that matches skills as phrases. Instead of checking whether a single token appears, we check whether a known skill string appears inside any noun chunk — this catches "machine learning" inside "machine learning applications".

**What the code does:** `extract_skill_chunks()` loops over `doc.noun_chunks` and does a case-insensitive substring check against a `skills_db` set, returning `(skill, chunk)` pairs.
- With `skills = {"Python", "Machine Learning", "Deep Learning", "TensorFlow", "NLP"}` and the text "Expert in Python and Machine Learning applications", it returns `{('Python', 'Python'), ('Machine Learning', 'Machine Learning')}`.

**Try it:** "Deep Learning" and "NLP" are in the database but absent from the text, so they are correctly not reported — and the returned chunk is the *full* chunk, ready to be highlighted or indexed.""",
10: """## Key Insight: Chunking preserves multi-word concepts that single-token approaches miss.

**Chunks are the atomic unit of a resume: skills, titles, and tools are phrases, so match at phrase level.**

Token-level features would shred "deep learning" into "deep" + "learning" and lose the concept; chunks keep it whole. Chunking is the bridge between linguistic structure (Ch. 11) and the vector representations that follow — the phrases extracted here are exactly the candidate terms that keyword extraction (Ch. 14) and TF-IDF/BoW features (Ch. 15–16) should operate on."""
})

# ============ NB14 — Keyword Extraction ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\14_keyword_extraction\14.ipynb", replace={
0: """# 14 — Keyword Extraction

Given a document, which words or phrases carry the signal? Keyword extraction ranks the vocabulary so the top terms are the ones a human — or an ATS — would use to describe the text. Three families are shown: TF-IDF (frequency statistics), RAKE (phrase scoring), and KeyBERT (neural embeddings).

**Why it matters for resumes / ATS:** a resume's keywords are its ATS currency. Extraction gives you a ranked, reviewable list of what the document is "about" — what matching engines use to decide whether a resume fits a job description, and what human screeners scan for in seconds.""",
1: """**Goal:** Extract the most important words/phrases from a document automatically.

The extracted keywords are the first unsupervised feature set that can stand in for the whole document: instead of matching against 300 raw tokens, an ATS matches against the 5–10 highest-ranked phrases. This chapter compares a statistical method (TF-IDF), a rule-based one (RAKE), and a semantic one (KeyBERT).""",
2: """## 1. TF-IDF Keyword Extraction

TF-IDF (detailed in Ch. 16) rewards terms that appear often in one document but rarely across the corpus. Ranked TF-IDF scores are a fast, interpretable keyword extractor with zero training.

**What the code does:** `TfidfVectorizer(stop_words="english", max_features=20)` builds the document-term matrix over three resume-like docs, sums each column, and sorts term-score pairs.
- "learning" tops the list at `0.764`, then "machine" and "python" at `0.682` — the technical core of the corpus.
- Generic words are suppressed: "experience" scores only `0.471` despite appearing in a doc, because IDF punishes corpus-wide terms.

**Try it:** the ranking reads like a one-line resume summary — that's the whole point. Change `max_features` to see the tail of the ranking.""",
4: """## 2. RAKE (Rapid Automatic Keyword Extraction)

RAKE is rule-based: split text into candidate phrases on punctuation, drop stopwords and short words, then score what's left. It needs no training data and no external model — just a stopword list.

**What the code does:** `rake()` splits on punctuation via `re.split(r"[.,!?;:()]", ...)`, filters tokens by stopwords and length, and returns the most frequent surviving phrases via `Counter`.
- On "This candidate has strong Python and machine learning skills..." it returns `[('this candidate has strong python machine learning skills with deep learning expertise', 1)]`.

**Try it:** this naive implementation only splits on punctuation, so a punctuation-free sentence collapses into one giant "keyword". The classic RAKE improvement is to also split on stopwords, which yields `['strong python', 'machine learning skills', 'deep learning expertise']`-style phrases. Add that split and re-run.""",
6: """## 3. KeyBERT (BERT-based Keyword Extraction)

KeyBERT embeds the document and candidate phrases with a transformer model (`all-MiniLM-L6-v2` here) and returns the candidates with the highest cosine similarity to the document — keywords by *meaning*, not by frequency.

**What the code does:** wraps the call in `try/except` so the notebook survives environments where `keybert` (or its model) is missing.
- With KeyBERT installed: `extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=5)` prints the top 5 scored phrases.
- Without it: prints "KeyBERT not installed. Install with: pip install keybert" and points back to the TF-IDF cell — the graceful-degradation pattern you want in real pipelines too.

**Try it:** compare KeyBERT's top phrases with TF-IDF's on the same text — the two often agree on the head of the list but diverge in the tail, which is why this chapter's summary says to use both.""",
8: """## Summary: TF-IDF = fast & interpretable. KeyBERT = semantic but slower. Use both.

**There is no single best keyword extractor — pick by constraint: TF-IDF when you need speed and auditability, KeyBERT when you need meaning, both when you can afford it.**

TF-IDF is deterministic, dependency-free, and explainable ("learning ranked first at 0.764"); KeyBERT understands synonyms ("ML" ≈ "machine learning") but loads a transformer and is slower per document. In an ATS, TF-IDF-style extraction is typically the first pass — and the extracted keywords become the features that Ch. 15–16 vectorize next."""
})

# ============ NB15 — Bag of Words ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\15_bag_of_words\15.ipynb", replace={
0: """# 15 — Bag of Words (BoW)

Bag of Words turns text into a fixed-size numeric vector: count how often each vocabulary term appears, and that vector is the document. The order of words is discarded — hence "bag". Simple, fast, and the foundation every later representation (TF-IDF, embeddings) builds on.

**Why it matters for resumes / ATS:** BoW is the baseline every matching engine starts from. A resume and a job description can be compared as vectors; skills that appear in both push the vectors closer. Understanding BoW's strengths (cheap, exact) and limits (no order, no semantics) tells you when to use it and when to reach for Ch. 16 and beyond.""",
1: """![Text Representation Evolution](../../../assets/images/text_representation_evolution_1785491155497.png)

> **Figure:** Evolution of text representation methods. Bag of Words is the starting point — Blocks C and D cover each level in sequence.

The figure places BoW at the bottom of the representation ladder: counts first, then TF-IDF weighting (Ch. 16), n-grams (Ch. 17), and dense embeddings (Ch. 19–22). Each level fixes a weakness of the one below — keep this map in mind as the chapters progress.""",
2: """**Goal:** Convert text into numerical feature vectors using CountVectorizer.

Vectorizing is the prerequisite for any math on text: similarity, ranking, and classification all need numbers. After this chapter you can build a document-term matrix with `CountVectorizer` and read it like a table — rows are documents, columns are vocabulary terms, cells are counts.""",
3: """## 1. How BoW Works

`CountVectorizer` does two jobs: builds the vocabulary (unique terms across all documents) and counts occurrences per document into a matrix. Each cell is a raw term frequency.

**What the code does:** fits on three short docs and prints the vocabulary, matrix shape, and the first document's row.
- Vocabulary: 9 unique terms — `['for', 'fun', 'great', 'is', 'learning', 'machine', 'nlp', 'python', 'with']` (lowercased, punctuation stripped).
- Shape `(3, 9)`: 3 documents × 9 vocabulary terms; doc 1 ("Python is great for NLP") is `[1, 0, 1, 1, 0, 0, 1, 1, 0]` — 1 where the term appears, 0 elsewhere.

**Try it:** count by hand — "python", "is", "great", "for", "nlp" each appear once, so doc 1's row has five 1s. The position of the 1s is meaningless; only the counts matter.""",
5: """## 2. Vocabulary Size vs Sparsity

Real text vectors are mostly zeros: a 10,000-term vocabulary, a 300-word resume, so ~97% of the matrix is empty. Sparsity is the number to watch — it drives memory and speed.

**What the code does:** re-fits `CountVectorizer` with `max_features` 5→50 and prints vocab size and sparsity `1 - nnz/(rows*cols)`.
- On this toy corpus the vocabulary saturates at 6 terms and sparsity at `0.500` — modest, because 3 tiny documents can't fill a large vocabulary.

**Try it:** the code's printout claims ">90% zeros", but the measured sparsity here is only ~50%. That claim is true for real corpora (thousands of docs, thousands of terms) — this toy set is too small to show it. Scale up the document list and watch sparsity climb.""",
7: """## 3. BoW for Resume Comparison

With `binary=True` each cell records *presence* (1/0) instead of count — a resume says "TensorFlow" once or ten times; either way the candidate knows it. Binary vectors make overlap counting trivial: element-wise products sum to the number of shared terms.

**What the code does:** vectorizes three resumes into a 3×14 binary matrix and computes shared-term counts between resume 1 and the others.
- Resume 1 ("Data scientist Python TensorFlow...") and resume 2 ("Python developer Django Flask...") share **1** word (`python`).
- Resume 1 and resume 3 ("ML engineer TensorFlow PyTorch...") share **2** words (`tensorflow`, `learning`).

**Try it:** read the printed 0/1 matrix — resume 1's row has 1s at `data, learning, machine, python, scientist, tensorflow`, which is exactly the set the sharing counts come from.""",
9: """## Key Insight: BoW is simple but loses word order and semantics. Use as a baseline.

**BoW is the honest baseline: cheap, exact, and blind — it sees "not skilled in Python" as a Python hit.**

The bag discards word order ("Python data science" and "data science Python" are identical) and any notion of meaning (synonyms never match). That's why every later chapter fixes a specific blind spot: TF-IDF weights terms (Ch. 16), n-grams restore local order (Ch. 17), and embeddings restore semantics (Ch. 19+). Keep BoW as your benchmark — any fancier method must beat it on the same metric."""
})

# ============ NB16 — TF-IDF Deep Dive ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\16_tf-idf_deep_dive\16.ipynb", replace={
0: """# 16 — TF-IDF Deep Dive

TF-IDF (term frequency × inverse document frequency) re-weights raw counts: a term is important if it appears often in *this* document but rarely in *other* documents. It is the most widely used text representation in classical ML and the default feature set for resume–JD matching.

**Why it matters for resumes / ATS:** raw counts rank "experience" and "data" as highly as "tensorflow" — nonsense for matching. TF-IDF demotes generic resume words and promotes distinctive skills, so the similarity between a resume and a job description is driven by what makes the resume specific, not by filler.""",
1: """**Goal:** Understand TF-IDF weighting — the most popular text representation in classical ML.

This chapter goes from the math (TF and IDF by hand) to the library (`TfidfVectorizer`) to the application (resume–JD similarity). By the end you can explain why "java" scores 0.681 in one document while "data" scores 0.447 — and use that intuition to build a matcher.""",
2: """## 1. TF-IDF Manually

TF is how often a word appears in a document (normalized by length); IDF is a corpus-level rarity penalty. The smoothed variant here is `log(N / (1 + df)) + 1`, which keeps IDF positive and dampens the zero-document case.

**What the code does:** defines `tf()` and `idf()` from scratch and scores the word "python" across three documents.
- Doc 1: `0.1250 × 1.0000 = 0.1250`; Doc 2: `0.1111 × 1.0000 = 0.1111`; Doc 3: `0.0000` (python absent).
- IDF is exactly `1.0000` everywhere because "python" appears in 2 of 3 documents: `log(3/(1+2)) + 1 = 1`. The +1 smoothing is why it never collapses to zero.

**Try it:** TF differs between docs (0.1250 vs 0.1111) because of the length normalization, while IDF is constant for the word across the corpus. That separation — local frequency vs global rarity — is the whole idea.""",
4: """## 2. TF-IDF with scikit-learn

`TfidfVectorizer` applies the same idea with the library's normalization (L2 by default): each document vector is scaled to unit length, so vector comparisons measure term *mix* rather than document *length*.

**What the code does:** fits on the three docs with `stop_words="english", max_features=10` and prints each document's top-5 weighted terms.
- Vocabulary: `['data', 'java', 'language', 'learning', 'machine', 'programming', 'python', 'science', 'used']`.
- Doc 3's top term is `java` at `0.681` — it appears in only one document, so its IDF is maximal; shared words like `data` (`0.447`) rank lower.

**Try it:** compare doc 1 (five top terms tied at 0.447) with doc 3 (`java` 0.681, `language`/`programming` 0.518) — the document with a rare distinctive term has the sharpest weights.""",
6: """## 3. TF-IDF for Resume-JD Matching

The canonical ATS operation: vectorize the resume and the job description into the *same* TF-IDF space, then measure their cosine similarity. Shared skills push the vectors together; generic terms barely matter.

**What the code does:** fits one `TfidfVectorizer` on `[resume, jd]`, prints the shared vocabulary, and computes cosine similarity between the two rows.
- Shared keywords include `python`, `tensorflow`, `machine`, `learning`, `nlp`, `data`, `science` — the actual overlap between candidate and job.
- `Resume-JD TF-IDF similarity: 0.617` — a solid match, driven by the tech-stack overlap.

**Try it:** swap one resume term for a synonym ("pytorch" instead of "tensorflow") and watch the score drop — TF-IDF has no synonym awareness. That limitation motivates the embedding chapters (Ch. 19+).""",
8: """## Key Insight: TF-IDF downweights common words ('experience', 'data') and highlights distinctive ones (skills, tech).

**TF-IDF's superpower is selectivity: it makes a document's identity come from its rare, meaningful terms.**

For resumes this is exactly right — "experience" tells you nothing, "tensorflow" tells you everything. The weighted vectors are what Ch. 18's cosine similarity consumes, and the ranking idea is what Ch. 14's keyword extraction used. Next, Ch. 17 adds word order back via n-grams, fixing TF-IDF's other blind spot."""
})

# ============ NB17 — N-Grams ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\17_n-grams\17.ipynb", replace={
0: """# 17 — N-Grams

N-grams are contiguous sequences of n tokens — "machine", "machine learning", "machine learning is" for n=1,2,3. They restore a slice of word order that the bag of words (Ch. 15) threw away, at the cost of a larger, sparser vocabulary.

**Why it matters for resumes / ATS:** the most important resume terms are multi-word: "machine learning", "data science", "computer vision". A unigram-only index can't distinguish "deep learning" from "deep" + "learning" — n-grams capture the exact phrases recruiters and ATS dictionaries look for.""",
1: """**Goal:** Capture word order and multi-word expressions using n-grams.

This chapter covers the three n-gram flavors (unigrams/bigrams/trigrams), skill detection with `ngram_range=(1,3)`, and a character-level overlap score that stays robust to word-level differences. The takeaway: `(1,2)` is the sweet spot for most resume work.""",
2: """## 1. Unigrams, Bigrams, Trigrams

`CountVectorizer(ngram_range=(n, n))` builds a vocabulary of n-word windows. Higher n captures more context but fragments fast — a 10-word sentence yields 10 unigrams but only 8 trigrams, and the vocabulary explodes with corpus size.

**What the code does:** fits three vectorizers on one sentence and prints the first 10 features of each n.
- 1-grams (7): `['and', 'deep', 'fun', 'is', 'learning', 'machine', 'powerful']` — unique tokens.
- 2-grams (7): `['and deep', 'deep learning', 'fun and', 'is fun', ...]` — note `machine learning` survives as a unit.
- 3-grams (7): `['and deep learning', 'deep learning is', ...]` — longer context, zero hits outside the sentence.

**Try it:** "machine learning" appears as a bigram while its unigrams (`machine`, `learning`) also exist separately — that redundancy is why n-gram vocabularies grow so fast.""",
4: """## 2. N-Grams for Skill Detection

Scoring n-gram features by corpus frequency surfaces the multi-word skills: "machine learning" and "deep learning" should rank high, while accidental bigrams ("experience natural") should sink. This is the feature-extraction step that feeds classifiers in later chapters.

**What the code does:** fits `CountVectorizer(ngram_range=(1, 3), stop_words="english")` on three skill sentences and ranks features by summed counts.
- "learning" leads with count 2, followed by single-hit bigrams and trigrams like `computer vision`, `data science`, `deep learning`.

**Try it (known issue):** this cell calls `np.array(...)` but never imports numpy in this notebook, so a fresh kernel raises `NameError: name 'np' is not defined`. Add `import numpy as np` at the top to see the ranking — the intent is a summed-count ranking of n-gram features.""",
6: """## 3. N-Gram Overlap for Resume Comparison

Jaccard overlap on **character** n-grams (via `analyzer="char"`) measures surface similarity between two strings: "data scientist python" vs "data analyst python" share most character bigrams even though they differ at the word level. This is a classic fuzzy-matching trick for near-duplicate text.

**What the code does:** `ngram_overlap()` builds character n-gram sets for both strings and returns `|A ∩ B| / |A ∪ B|`.
- Bigram overlap: `0.462`; trigram overlap: `0.385`.

**Try it:** the overlap is high but not 1 — the shared "data ... python" skeleton dominates, while the scientist/analyst difference shows up in the drop from 0.462 (bigrams) to 0.385 (trigrams). Lower n = more forgiving.""",
8: """## Summary: Use ngram_range=(1,2) for most resume tasks — captures bi-gram skills like 'machine learning'.

**The (1,2) range is the default: unigrams catch single skills, bigrams catch the multi-word ones that actually matter.**

Trigrams add context but multiply vocabulary and sparsity for little gain on resumes; character n-grams are reserved for fuzzy and typo-tolerant matching. Combined with TF-IDF weighting (Ch. 16), n-gram features are the classic classical-ML resume representation — and exactly the vectors Ch. 18 will measure with cosine similarity."""
})

# ============ NB18 — Cosine Similarity ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\18_cosine_similarity\18.ipynb", replace={
0: """# 18 — Cosine Similarity

Cosine similarity measures the angle between two vectors: cos(θ) = a·b / (|a||b|). It ranges from 1 (same direction) to -1 (opposite), with 0 meaning orthogonal. Because it normalizes by magnitude, it compares *profiles* regardless of document length.

**Why it matters for resumes / ATS:** resume–JD matching is a vector-similarity problem. Cosine gives a single 0–1 score for "how well does this resume fit this job" — the number an ATS ranks candidates by, and the same score Ch. 16's TF-IDF vectors were built to feed.""",
1: """**Goal:** Measure document similarity using vector dot products.

Starting from the formula in plain numpy, this chapter builds up to a 4×4 resume similarity matrix and a resume-vs-JD scorer. Two implementation notes worth keeping: length normalization is what makes cosine fair across short and long documents, and the same score powers keyword extraction (Ch. 14) and sentence embeddings (Ch. 22).""",
2: """## 1. Cosine Similarity from Scratch

The formula is three operations: dot product (shared magnitude), product of norms (scaling), and the ratio (the angle's cosine). Zero-vector inputs return 0.0 by convention — the guard `if norm > 0 else 0.0` prevents division by zero.

**What the code does:** implements `cosine_sim()` and checks three edge cases.
- Identical vectors `[1,2,3]` vs `[1,2,3]` → `1.000` — maximum similarity.
- Orthogonal `[0,0,1]` vs `[1,0,0]` → `0.000` — no shared direction.
- Opposite `[1,0]` vs `[-1,0]` → `-1.000` — anti-correlated.

**Try it:** multiply `a` by 10 and recompute — the score stays 1.000 because cosine ignores magnitude. That invariance is the entire reason it works on documents of different lengths.""",
4: """## 2. Resume Similarity with TF-IDF + Cosine

TF-IDF vectors (Ch. 16) are already length-normalized, and `cosine_similarity(X)` computes the full pairwise matrix in one call: `sim_matrix[i][j]` is the similarity between resumes i and j.

**What the code does:** vectorizes four resumes (Google/Python/NLP, Amazon/Python/ML/TF, Oracle/Java/Spring, Microsoft/MLOps), fits a 50-feature TF-IDF model, and builds the 4×4 matrix.
- Measured values: diagonal 1.000, R1↔R2 = `0.331`, R1↔R3 = `0.175`, R1↔R4 = `0.075` — the Python/ML resumes are closest, the Java resume is nearly orthogonal to the ML resumes.

**Note (known issue):** the cell's print loop formats an integer with `{i+1:15s}`, which raises `ValueError` in Python 3 — use `{i+1:<15}` to render the table. The matrix computation itself is correct.""",
6: """## 3. Resume vs JD Scoring

The real ATS operation: one resume, many job descriptions. Vectorize everything in the same space, take the first row of the similarity matrix, and rank the jobs by score.

**What the code does:** fits TF-IDF on `[resume, jd_ml, jd_java]` and reads row 0 of `cosine_similarity(X)`.
- Resume vs ML job: `0.510` — strong overlap on python/tensorflow/machine learning.
- Resume vs Java job: `0.000` — zero shared vocabulary after stopword removal, i.e. completely different stacks.

**Try it:** the ML job wins by a wide margin, and the 0.000 vs the Java job is a clean, explainable miss — no shared terms at all. That's cosine similarity doing its job on the exact features from Ch. 16.""",
8: """## Key Insight: Cosine similarity = angle between vectors, not magnitude. Handles different document lengths gracefully.

**Score by direction, not size: a short resume and a long JD can still align perfectly if their term profiles match.**

Magnitude normalization is what makes this fair — a 5-page CV doesn't automatically beat a 1-page one. Cosine on TF-IDF vectors is the workhorse of classical resume matching, and the exact same score is reused by KeyBERT (Ch. 14) and sentence transformers (Ch. 22). Next, Ch. 19 replaces the sparse TF-IDF vectors with dense learned embeddings."""
})

# ============ NB19 — Word2Vec ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\19_word2vec\19.ipynb", replace={
0: """# 19 — Word2Vec

Word2Vec learns dense, low-dimensional vectors where words that appear in similar contexts end up close together: "python" sits near "nlp" and "tensorflow" because they co-occur in the same sentences. Unlike BoW (Ch. 15) it captures *meaning*, and unlike TF-IDF (Ch. 16) the vectors are learned, not counted.

**Why it matters for resumes / ATS:** exact-keyword matching fails on synonyms ("pytorch" vs "torch", "ML" vs "machine learning"). Embeddings let a matcher say "this resume mentions things semantically close to what the JD asks for" — the difference between a keyword grep and a semantic search.""",
1: """**Goal:** Learn dense vector representations that capture semantic meaning.

Using gensim on a tiny 6-sentence toy corpus, this chapter trains a model, inspects the vectors, and probes them with similarity, nearest-neighbor, and document-level queries. The corpus is small on purpose: the *mechanics* are what matter here; scale comes in Ch. 21–22 with pretrained models.""",
2: """## 1. Training a Small Word2Vec Model

`Word2Vec(sentences, vector_size=50, window=3, min_count=1, epochs=100)` trains by predicting each word from its neighbors (CBOW) or neighbors from the word (skip-gram). `window=3` sets the context radius, `min_count=1` keeps every token in this toy corpus, and 100 epochs let the tiny dataset converge.

**What the code does:** trains on six hand-written sentences and reports the vocabulary and a sample vector.
- Vocabulary size: `26` unique tokens.
- `model.wv['python']` has shape `(50,)`; its first 10 dims are small floats like `[-0.016, 0.009, -0.008, ...]` — dense and distributed, nothing like the 0/1 BoW rows.

**Try it:** each dimension means something only in combination — the "meaning" is spread across all 50 floats. Values vary run-to-run because training starts from a random init.""",
4: """## 2. Word Similarity

`model.wv.similarity(w1, w2)` returns the cosine of the two learned vectors. In a well-trained model, semantically related words score higher than unrelated ones.

**What the code does:** scores "python" against five partners from the toy corpus.
- This run: `sim('python', 'great') = 0.235`, `sim('python', 'code') = 0.018`, `sim('python', 'data') = -0.170` — values shift between runs, but the relative ordering reflects the tiny corpus's co-occurrence structure.

**Try it:** with only 6 sentences, similarities are noisy — "python" appears with "nlp" and "machine learning" but also with "great" and "code". Don't over-read exact numbers; the API and the direction of the signal are the lesson.""",
6: """## 3. Most Similar Words

`most_similar(word, topn=k)` ranks the whole vocabulary by cosine to the query and returns the k nearest neighbors — the model's own guess at what "goes with" a word.

**What the code does:** queries three words and prints their top-3 neighbors.
- This run: near `'python'`: `great (0.235)`, `builds (0.229)`, `scientist (0.161)`; near `'learning'`: `uses (0.279)`, `works (0.225)`, `tensorflow (0.198)`.

**Try it:** the neighbors of "learning" lean technical (`tensorflow`) while "python" picks up both technical and generic words — the corpus's co-occurrence structure showing through. Exact numbers vary per run.""",
8: """## 4. Word Analogies

The classic embedding demo is vector arithmetic: `king - man + woman ≈ queen`. Here the notebook applies the same `most_similar(positive=[...])` API in a simpler form — "what's closest to 'python'?" — because a 6-sentence toy corpus is too small for reliable analogies.

**What the code does:** wraps `most_similar(positive=["python"], topn=3)` in a `try/except KeyError` guard for words missing from the vocabulary.
- This run: `[('great', 0.235), ('builds', 0.229), ('scientist', 0.161)]` — the same neighbors as the plain similarity query, since `positive=[...]` is exactly that query.

**Try it:** on a pretrained model (Ch. 21) try `most_similar(positive=["queen"], negative=["king"], topn=3)`-style arithmetic; here the point is the API shape and the `KeyError` guard on out-of-vocabulary words.""",
10: """## 5. Averaging Word Vectors for Document Similarity

To turn word vectors into a document vector, average the word vectors: `doc_vector()` filters to known words and takes the mean. It's crude but effective — the standard baseline before sentence transformers (Ch. 22).

**What the code does:** builds vectors for three docs and computes pairwise cosine similarity.
- Doc1 vs Doc2 (ML-related): this run ≈ `0.14`; Doc1 vs Doc3 (Java/backend): ≈ `0.14` — nearly tied, because the toy model's vectors are noisy and doc 3's words (`java`, `spring`, `backend`) are mostly out of vocabulary, so its vector is built from almost nothing.

**Try it (known issue):** this cell calls `cosine_similarity`, but that import lives in Ch. 18's notebook, not here — add `from sklearn.metrics.pairwise import cosine_similarity` to run it. It also silently drops OOV words, which is why doc 3's "vector" is mostly the single known word `developer`.""",
12: """## Key Insight: Word2Vec captures semantics — 'python' is close to 'nlp' AND 'tensorflow'.

**Dense embeddings turn "related in text" into "close in vector space" — the first semantic representation in this series.**

Even on six sentences, the mechanics are clear: context-based training, cosine probes, nearest neighbors, vector arithmetic, and document-level averaging. The limits (tiny vocabulary, no OOV handling, noisy similarities) are exactly what Ch. 20's FastText subwords and Ch. 21–22's pretrained transformers fix."""
})

# ============ NB20 — FastText ============
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_c\20_fasttext\20.ipynb", replace={
0: """# 20 — FastText

FastText extends Word2Vec with **subword information**: each word's vector is built from the vectors of its character n-grams (e.g. "python" → "<py", "pyt", "yth", ..., "on>"). Unknown words are never truly "out of vocabulary" — their vectors are synthesized from their parts.

**Why it matters for resumes / ATS:** resumes are full of typos ("Tensorflo", "Pytorch", "progamming") and rare technical terms. Word2Vec throws a `KeyError` on those; FastText infers a vector, matches them to the right skill, and keeps the matcher alive.""",
1: """**Goal:** Handle rare words and typos using subword information.

This chapter trains FastText on a tiny corpus, shows vectors being recovered for misspelled words that Word2Vec would reject, measures typo similarity with cosine, and digs into the character n-grams that make it all work. By the end you can explain why a typo like "pyton" still lands near "python". """,
2: """## 1. Training FastText with Gensim

The gensim API is nearly identical to Word2Vec: `FastText(sentences, vector_size=50, window=3, min_count=1, epochs=100)`. The difference is internal — alongside whole-word vectors it learns vectors for character n-grams, so every word is represented by a sum of its parts.

**What the code does:** trains on four sentences and reports vocabulary size and vector shape.
- Vocabulary: `15` tokens; `ft.wv['python']` has shape `(50,)`, the same layout as Word2Vec — the upgrade is invisible until you query an unknown word (next section).

**Try it:** the training API is identical to Ch. 19 — the subword machinery is what changed, not the interface.""",
4: """## 2. FastText Handles Out-of-Vocabulary Words

The payoff: query a word the trainer never saw and FastText still returns a vector, composed from its character n-grams. `pythoning`, `pyton`, `tensorflo`, `lernin`, `progamming` are all recoverable — and the model's nearest neighbors show it understands them.

**What the code does:** probes five misspellings and prints whether a vector was found and the top-2 neighbors.
- All five → `VECTOR FOUND (via subwords)`. This run: `'pythoning'` → `python (0.749)`, `'progamming'` → `programming (0.478)` — the typo maps straight back to the correct skill.

**Try it:** Word2Vec (Ch. 19) would raise `KeyError` on every one of these. That single difference — graceful degradation on messy input — is why FastText is the resume-parsing favorite.""",
6: """## 3. FastText vs Word2Vec on Typos

Quantifying the advantage: cosine similarity between a correct word and its misspelling. High scores mean the typo is "close enough" to the real term to match safely.

**What the code does:** scores three (correct, typo) pairs and contrasts with Word2Vec behavior.
- This run: `sim('python', 'pyton') = 0.233`, `sim('learning', 'lernin') = 0.114`, `sim('tensorflow', 'tensorflo') = 0.837` — the more shared character n-grams, the higher the score.
- Word2Vec: `KeyError` on all three — the contrast line the notebook prints.

**Try it:** `tensorflow`/`tensorflo` share almost every n-gram, hence 0.837; `lernin` loses more subwords, hence 0.114. That gradient is exactly what a typo-tolerant skill matcher should exploit.""",
8: """## 4. Subword Details

Character n-grams with special boundary markers (`<`, `>`) are what make all of this work. "python" at n=3..6 produces `<py`, `pyt`, `yth`, `tho`, `hon`, `on>`, `<pyt`, `pyth`, ..., `ython>` — and "pyton" shares most of them.

**What the code does:** calls `compute_ngrams(word, 3, 6)` and prints the n-gram list.
- `compute_ngrams('python', 3, 6)` returns `['<py', 'pyt', 'yth', 'tho', 'hon', 'on>', '<pyt', 'pyth', 'ytho', 'thon', 'hon>', ...]` — 16 subword units per word.

**Try it (known issue):** on gensim ≥ 4.0 the guard `hasattr(ft.wv, 'ngrams')` is False — the attribute was removed — so the in-notebook listing is skipped and only the header and conclusion print. Call `compute_ngrams` directly (as shown) to see the list.""",
10: """## Summary: Use FastText for resume parsing — resumes often have typos ('Tensorflo', 'Pytorch').

**Subword embeddings buy typo tolerance at the price of a larger, slower model — the right trade for messy resume text.**

FastText keeps Word2Vec's semantic vectors (Ch. 19) and adds character-level robustness, so "progamming" still matches "programming". It is the last self-trained embedding in the series: Ch. 21 (GloVe) shows how to leverage *pretrained* embeddings at scale, and Ch. 22 moves to contextual sentence embeddings entirely."""
})
