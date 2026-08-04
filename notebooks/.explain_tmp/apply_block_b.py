"""Expand markdown cells of 8 block_b notebooks (04,05,06,07,08,09,10,12).
Mirrors ch11 exemplar style. NEVER touches code cells. Ch11 untouched."""
from nbtools import apply

# ============================================================ 04 — NLP Introduction
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\04_nlp_introduction\04.ipynb", replace={
0: r"""# 04  NLP Introduction
**Goal:** Understand what NLP is and see the full pipeline in action.

Natural Language Processing (NLP) is the discipline of getting computers to read, interpret, and extract meaning from human language. Resumes are unstructured text, but they follow a very stable template — contact block, headline, skills list, experience with action-verb bullets — which makes them an unusually tractable NLP target. A well-built pipeline converts a raw resume export into structured fields (name, title, skills, employers) that an ATS can index and match against job descriptions.

This chapter runs the whole pipeline on a realistic resume in a few lines of spaCy, then demonstrates why preprocessing *order* matters. Every later chapter in this block (05–13) unpacks one stage in depth; treat this notebook as the map.

**Why it matters for resumes / ATS:** an ATS does not "read" a resume — it extracts and matches keywords and structured attributes. Each pipeline stage (preprocessing → tokenization → POS → NER → parsing → extraction) converts free text into a queryable record: *who* worked *where*, doing *what*, with *which skills*. Understanding the whole chain before tuning any single stage is what separates a demo from a deployable extractor.""",
1: r"""![NLP Pipeline Overview](../../../assets/images/nlp_pipeline_diagram_1785491141457.png)

> **Figure:** The NLP processing pipeline — from raw resume text to structured data. Each stage in this notebook maps to a step in this pipeline.

The pipeline is strictly sequential because each stage feeds the next: **preprocessing** cleans raw text, **tokenization** splits it into words, **POS tagging** labels each word, **NER** finds real-world entities (people, companies, dates), and **parsing** recovers grammatical structure before final **extraction** produces structured fields. Skipping a stage — or running it out of order — silently degrades everything downstream; the last section of this notebook demonstrates a concrete failure case. Keep this diagram in mind: every notebook in Block B zooms into exactly one of these boxes.""",
2: r"""## 2. The NLP Pipeline in Action

This cell runs the entire pipeline on a realistic resume in about five lines: spaCy's single `nlp(resume)` call performs tokenization, POS tagging, NER, and dependency parsing in one pass. The pipeline is less about calling five libraries and more about knowing which stage to interrogate at each step.

**What the code does:**
- loads the small English model once via `spacy.load("en_core_web_sm")` and parses the multi-line `resume` string
- counts sections with `re.split(r'\\n{2,}', resume)` — the stored output prints `Sections: 1`, because the pattern here is written with a doubled backslash and matches a literal backslash rather than newlines; the resume *does* contain a blank line before `EXPERIENCE`, and a correct `r'\n{2,}'` would report 2
- prints the first 8 entities from `doc.ents` with their labels, plus a non-space token count (56 tokens)

**Try it:** the stored output reports 13 entities, and several labels are visibly wrong — `Python -> GPE`, `TensorFlow -> ORG`, `Machine Learning -> PERSON`, `Data Scientist -> ORG`. The base model is guessing on spans it was never trained on; that is the motivation for the custom skill extraction built in Ch. 12.""",
4: r"""## 3. Text Preprocessing Order Matters

Preprocessing steps are not commutative: lowercasing before expanding contractions destroys the apostrophe that the expansion depends on. The demo sentence "I wasn't loving the team's performance... But NOW I do!" is run through two orderings so the difference is visible.

**What the code does:**
- `wrong`: lowercases first, then strips non-word characters — `wasn't` becomes `wasnt` and `team's` becomes `teams`, with inflection and possession silently glued away
- `right`: expands contractions first (`n't` → ` not`, `'s` → ` is`), then lowercases and strips punctuation — the fragments survive as separate words

**Read the stored output carefully:** both lines print `'wssw'`. That is not the ordering lesson — it is a regex-escape bug in the notebook itself. The pattern is written as the raw string `r"[^\\w\\s]"` with a doubled backslash, so the regex matches "anything except a literal backslash, `w`, or `s`" and deletes every other character, leaving only the `w`/`s` letters. With a correct `[^\w\s]`, the right path yields readable text (`"i was not loving the team is performance but now i do"`) while the wrong path still mutilates `wasn't`. Two lessons for the price of one: order matters, and always sanity-check regex escapes against the output.""",
6: r"""## Summary: NLP pipeline = raw text -> preprocessing -> tokenization -> POS -> NER -> parsing -> extraction

That chain is the backbone of the whole block. Raw text arrives dirty (encodings, bullets, contractions); **preprocessing** normalizes it; **tokenization** splits it into units; **POS** and **NER** add grammatical and semantic labels; **parsing** recovers structure; **extraction** emits structured fields. Two lessons from this chapter carry forward: stages are strictly ordered, and library defaults (models, regex, tokenizers) are only as good as the inspection you give them — both demos here failed in instructive ways that would have gone unnoticed without reading the output.

The next seven chapters walk this chain left to right: Ch. 05 tokenization, Ch. 06 normalization, Ch. 07 stop words, Ch. 08 lemmatization, Ch. 09 stemming, Ch. 10 POS tagging, then parsing and NER (Ch. 11–12) before extraction.""",
})

# ============================================================ 05 — Tokenization
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\05_tokenization\05.ipynb", replace={
0: r"""# 05 — Tokenization
**Goal:** Master word, sentence, and subword tokenization.

Tokenization splits text into atomic units — **tokens** — and it is the first decision that shapes everything downstream: POS tagging, lemmatization, NER, and keyword matching all operate on whatever the tokenizer produced. "Word" is not a well-defined concept: contractions, abbreviations, emails, and `C++` each demand different treatment, and different tools draw the boundaries differently.

**Why it matters for resumes / ATS:** ATS keyword matching compares tokens against job-description terms. If the tokenizer splits `scikit-learn` into `scikit`, `-`, `learn` or mangles `C++`, the literal match against a JD keyword fails even though the skill is present. Tokenization is where resume-specific vocabulary (hyphens, slashes, plus signs, version numbers) meets the real world — and where naive whitespace splitting quietly loses matches.""",
1: r"""## 1. Word Tokenization — Comparing Approaches

Three tokenizers, three different notions of "word". Python's `str.split()` cuts on whitespace only; NLTK's `word_tokenize` uses the Punkt model trained on general English; spaCy's tokenizer is a statistical model trained on web text — so it has seen emails, URLs, and contractions in the wild.

**What the code does:** after downloading the Punkt data (`nltk.download("punkt_tab", quiet=True)`), it tokenizes the same sentence three ways:
- whitespace split keeps `Don't` and `john.smith@email.com` whole, but leaves punctuation glued to words (`forget:`, `(work)`)
- NLTK splits the contraction (`Don't` → `Do`, `n't`) and the possessive (`Smith's` → `Smith`, `'s`), but breaks the email into `john.smith`, `@`, `email.com`
- spaCy handles the contraction identically, yet keeps the email address as one token

**Try it:** compare the two lists in the stored output — the email line is the differentiator: `john.smith@email.com` survives as a single token only in spaCy, which matters when resumes list `name@domain.com` contact lines.""",
3: r"""## 2. spaCy Handles Resume Edge Cases

Resumes are dense with non-standard tokens: hyphenated library names, `C++`, slash-separated cloud stacks, "5+ years" ranges, city suffixes. How a tokenizer splits these determines whether downstream keyword matching ever sees the full string.

**What the code does:** parses five resume-typical tokens and prints the spaCy tokenization of each:
- `scikit-learn` → `['scikit', '-', 'learn']` — hyphens split, so the full library name is never a single token
- `C++` → `['C++']` — kept whole; the plus signs are not split off
- `AWS/GCP/Azure` → `['AWS', '/', 'GCP', '/', 'Azure']` — slashes separate, but each cloud name stays intact
- `5+ years` → `['5', '+', 'years']` and `New York-based` → `['New', 'York', '-', 'based']`

**Try it:** if your matcher uses exact token equality, `scikit-learn` will never match a JD line — plan for phrase-level matching (Ch. 13) or a custom matcher for hyphenated skills. `C++` staying whole is the pleasant surprise; do not assume it.""",
5: r"""## 3. Sentence Tokenization

Sentence boundaries look trivial and are not: periods inside abbreviations (`Mr.`, `Dr.`), interjections, and mixed punctuation all fool naive splitting. Sentence segmentation matters because downstream steps (bullet-level analysis, the SVO extraction of Ch. 11) assume each sentence is one unit.

**What the code does:** runs NLTK's `sent_tokenize` and spaCy's `doc.sents` on the same string containing `Mr.`, `Dr.`, `!`, and `?`:
- NLTK returns 3 sentences, correctly refusing to split after `Mr.` and `Dr.`
- spaCy returns the identical 3 sentences — both tools learned that an abbreviation period is not a sentence end

**Try it:** the stored outputs line up exactly: sentence 1 ends at `2020.`, sentence 2 at `promotion!`, sentence 3 at `enough?`. On resume text, sentence counts usually equal bullet counts — a quick sanity metric for later parsing stages.""",
7: r"""## 4. Subword Tokenization (BPE / WordPiece)

Modern transformer models do not tokenize into words at all. **WordPiece** (used by BERT) splits rare or unseen words into frequent subword fragments bounded by a fixed vocabulary; continuations are marked with `##`. The trade-off: near-infinite coverage of novel words at the cost of tokens that no longer correspond to dictionary words.

**What the code does:** loads the `bert-base-uncased` tokenizer via `transformers.AutoTokenizer.from_pretrained(...)` and tokenizes four resume-relevant words:
- `embeddings` → `['em', '##bed', '##ding', '##s']`
- `tokenization` → `['token', '##ization']`
- `scikit-learn` → `['sci', '##kit', '-', 'learn']`
- `TensorFlow` → `['tensor', '##flow']` — uncased, so the capital T is dropped

**Try it:** the first-run noise (PyTorch-version warning, HF Hub download progress bars) is harmless — the tokenizer downloads its vocab files on first use. The takeaway: subword tokens are great for LLM embeddings, but keyword matching against JDs still wants the whole-word view from §1–2.""",
9: r"""## Summary: Choose spaCy for resume tokenization. It handles domain-specific tokens (C++, hyphens, slashes) correctly.

Whitespace splitting glues punctuation to words, NLTK splits emails and some contractions, and BPE subwords are built for embeddings, not matching. spaCy's statistical tokenizer keeps emails whole, handles `C++` and slashes sensibly, and produces tokens that align with how skills are actually written — the right default for resume processing. Hyphenated skills (`scikit-learn`) remain the known gap and need phrase-level handling later.

Tokenization is the foundation everything else stands on: in production, Ch. 06 normalization cleans text *before* it reaches the tokenizer, and the tokens produced here are exactly what POS tagging (Ch. 10) and NER (Ch. 12) will label.""",
})

# ============================================================ 06 — Text Normalization
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\06_text_normalization\06.ipynb", replace={
0: r"""# 06 — Text Normalization
**Goal:** Clean messy real-world text into consistent form.

Normalization removes surface variation so that texts which differ only cosmetically compare equal: `PYTHON`, `python`, and `Python` should match; `café` and `café` should match; a bullet glyph should not leak into your tokens. Resumes arrive as PDF/DOCX exports full of curly quotes, en-dashes, ligatures, and Unicode accents — every one of those is a matching failure waiting to happen.

**Why it matters for resumes / ATS:** ATS keyword matching is string comparison. "python" vs "Python" vs "PYTHON" must collide, and a smart quote or accent in a skill name must not break the match. Normalization is the cheapest recall win in the entire pipeline — it runs before tokenization and before any matcher, and it costs one pass over the text.""",
1: r"""## 1. Case Normalization Trade-offs

Lowercasing maximizes recall but throws away information: acronyms (`AWS`, `NLP`, `PhD`) and proper names carry meaning in their casing. The robust pattern is not blind lowercasing — it is a **canonical form map**: lowercase for lookup, canonical spelling for output.

**What the code does:** builds `term_map = {t.lower(): t for t in terms}` from a curated set, then lowercases the sample and resolves each word through the map:
- `aws` → `AWS` — canonical casing restored
- `python,` → `python,` — no match, because the trailing comma makes `python,` a different key than `python`

**Try it:** the `python,` line is the real lesson — punctuation must be stripped *before* the case lookup runs (or the map must be built on cleaned tokens). Case normalization and punctuation handling are inseparable, which is why Ch. 05's tokenization decisions feed directly into matching.""",
3: r"""## 2. Unicode Normalization

The same character can be stored two ways: precomposed (`é` as one code point) or decomposed (`e` + combining accent). Add ligatures (`ﬁ`) and smart quotes, and a resume can contain several spellings of the same text. **NFKD** decomposes everything, and encoding to ASCII with `ignore` then keeps only the plain letters.

**What the code does:** for each sample, `unicodedata.normalize("NFKD", s)` followed by `.encode("ascii", "ignore").decode()`:
- `café` → `cafe` and `café` → `cafe` — the two spellings finally collide
- `ﬁle` → `file`, and smart quotes become plain quotes
- `Straße` → `Strae` — `ß` has no ASCII equivalent, so it is dropped

**Try it:** `Straße` is the lossy case — deterministic, but it will never match `Strasse`. For resume text this is usually acceptable; names and cities are the risky cases, so keep a small mapping for common non-ASCII names rather than trusting the drop.""",
5: r"""## 3. Bullet Symbol Normalization

Resumes use `•`, `-`, `*`, and `→` interchangeably as bullet markers. If those glyphs survive into tokens, "• Python" and "- Python" never compare equal and the marker pollutes downstream matching. Normalizing all markers to one canonical symbol makes bullet lists uniform.

**What the code does:** one regex, `r'[\s]*[•\-*→][\s]*'`, matches an optional whitespace run, any of the four marker characters, and a trailing whitespace run, replacing the whole thing with `'> '`:
- `• Python` → `>  Python`, `- Led team` → `>  Led team`
- `* Published` → `>  Published`, `→ Reduced latency` → `>  Reduced latency`

**Try it:** the stored outputs show all four markers canonicalized to a single `'> '` prefix (note the doubled space — the sample's own spacing survives the substitution). A `+` quantifier or a whitespace-collapse step cleans that up; the point here is that all four bullet styles now share one prefix.""",
7: r"""## 4. Complete ResumeCleaner

Production normalization combines every trick above into one reusable component. A class like `ResumeCleaner` is the first thing a real resume pipeline instantiates — it runs before the tokenizer so every later stage sees consistent text.

**What the code does:** `clean()` chains four steps: NFKD-decompose, ASCII-encode with `ignore`, map bullet glyphs (`•`, `‣`, `●`) to `>`, then collapse whitespace runs with `\s+` and strip:
- input `José's résumé • Python & NLP  Sr. ML Engineer` → `Jose's resume  Python & NLP  Sr. ML Engineer`

**Read the stored output carefully:** two details are worth noticing. First, no `>` appears — the `•` was dropped by the ASCII step *before* the bullet-mapping regex runs, so that mapping is dead code in this order. Second, the doubled spaces survive — the collapse pattern in the notebook is written as `r"\\s+"` with a doubled backslash, which matches a literal backslash rather than whitespace. Fixing the escape makes the output fully clean; spotting both is exactly the output-level verification Ch. 04 warned about.""",
}, append=[
r"""## Key Insight

**Normalization is where resume-matching recall is won or lost — and order matters as much as the steps themselves.**

Every character-level difference between a resume and a job description is a missed match: casing, Unicode spellings, bullet glyphs, whitespace. But the tools are blunt: blind lowercasing erases acronym case, ASCII-dropping eats `ß` and bullets, and a doubled backslash in a raw-string regex silently disables the step. Normalize in a fixed order — Unicode first, case via canonical maps, markers, then whitespace — and verify against real output before trusting the pipeline.

This feeds directly into Ch. 07: once the text is clean, the next question is which *words* carry meaning — and which common words should be dropped.""",
])

# ============================================================ 07 — Stop Words
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\07_stop_words\07.ipynb", replace={
0: r"""# 07 — Stop Words
**Goal:** Understand when to remove (and NOT remove) common words.

Stop words are high-frequency function words — `the`, `and`, `of`, `with` — that carry little standalone meaning. Removing them shrinks the vocabulary, speeds up matching and TF-IDF-style pipelines, and is a standard step in classic NLP. The catch: "little standalone meaning" is context-dependent, and on resumes the context is everything.

**Why it matters for resumes / ATS:** a bullet like "Reduced costs **by** 20%" loses its metric if `by` is deleted, and "Experience **with** Python" loses the tool signal if `with` goes. Default stop lists are tuned for news articles; using them unmodified on resumes actively destroys structured information. This chapter shows when removal helps and when it hurts.""",
1: r"""## 1. NLTK vs spaCy Stop Lists

Every library ships a stop list, and they disagree. NLTK's is curated from general corpora; spaCy's `Defaults.stop_words` is larger because it also covers contractions and common verb forms. Neither list was built with resumes in mind.

**What the code does:** materializes both lists and prints their sizes:
- `nltk_stops = set(stopwords.words("english"))` → 198 words
- `spacy_stops = spacy.load("en_core_web_sm").Defaults.stop_words` → 326 words

**Try it:** a 128-word gap is a real difference in downstream filtering — spaCy marks roughly 40% more tokens as removable. Whatever you choose, treat the library list as a starting point, not a contract: the next two sections show why.""",
3: r"""## 2. The Problem — Stop Words That Matter

Function words become load-bearing on resumes. `of` quantifies team size, `by` introduces the improvement metric, `with` introduces the tool. Deleting them by rule destroys exactly the structured facts an ATS is trying to extract.

**What the code does:** parses three bullets and collects the tokens spaCy flags as `is_stop`:
- `Managed team of 5 engineers` → `['of']` — the team-size signal
- `Reduced costs by 20%` → `['by']` — the improvement metric
- `Experience with Python` → `['with']` — the tool-usage signal

**Try it:** in all three cases the "stop word" is the word that makes the bullet a measurable claim. A rule that strips stop words before matching turns these into `Managed team 5 engineers`, `Reduced costs 20%`, `Experience Python` — matchable, but semantically gutted for any structured extraction.""",
5: r"""## 3. Custom Resume Stop Words

The fix is a two-tier custom list: generic noise (`a`, `an`, `the`, `very`, `really`, `just` — words with no matching value in any resume) plus resume filler — self-marketing words that pad bullets without adding keywords an ATS can match (`experienced`, `years`, `including`, `various`, `highly`, `motivated`).

**What the code does:** defines both sets, tokenizes the phrase with `lower().split()`, and filters out every token in either set:
- Before: `['highly', 'motivated', 'team', 'player', 'with', '5', 'years', 'experience']` (8 tokens)
- After: `['team', 'player', 'with', '5', 'experience']` (5 tokens)

**Try it:** note `with` survives — deliberately, because §2 showed `with` signals tool usage. The custom list encodes domain judgment: what to drop is a *product decision* about what your matcher should see, not a linguistics default.""",
7: r"""## Key Insight: Default stop lists designed for news articles. Customize for resumes.

**Stop-word removal is a recall trade-off, and the defaults are tuned for prose, not resumes.** `of`, `by`, and `with` are stop words in a news corpus — and the carriers of team size, metrics, and tool usage in a resume. Removing them before matching is a one-way door: the information is gone and no later stage can recover it.

The discipline that works: keep function words that precede numbers or nouns of interest, drop only words with provably no matching value, and test the list against real bullets before deploying. Once the noise is gone, the remaining content words still carry inflection — `develop`, `developing`, `developed` — which is exactly what Ch. 08 lemmatization normalizes next.""",
})

# ============================================================ 08 — Lemmatization
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\08_lemmatization\08.ipynb", replace={
0: r"""# 08 — Lemmatization
**Goal:** Reduce words to dictionary base form using vocabulary + morphology.

Lemmatization maps inflected forms to their dictionary base form — the **lemma**: `running` and `ran` → `run`, `mice` → `mouse`. Unlike stemming (Ch. 09), it consults a vocabulary and the word's part of speech, so the result is always a real word. The catch: it needs a POS signal, which is why Ch. 10 sits where it does in the pipeline.

**Why it matters for resumes / ATS:** resumes and job descriptions say the same skill in every inflection — "Developed", "developing", "develops". Lemma-normalizing makes all three collide with the JD keyword `develop`. But the tool is dangerous: lemmatizing proper nouns (`TensorFlow`, `Google`) silently lowercases and corrupts brand names that must match exactly.""",
1: r"""## 1. spaCy Lemmatization

`token.lemma_` is the lemmatized form, and it is **POS-aware**: spaCy tags the token first, then looks up the lemma for that tag. That is why the same surface word can have different lemmas in different contexts — and why irregular forms resolve correctly.

**What the code does:** parses single words and prints `lemma_` with the tag that drove it:
- `running` → `run` (VERB) and `ran` → `run` (VERB) — inflection collapsed, regular and irregular alike
- `better` → `well` (ADV) and `best` → `well` (ADV) — irregular, and *not* `good`
- `was` → `be` (AUX), `mice` → `mouse` (NOUN) — irregular auxiliaries and plurals
- `analyses` → `analysis` (NOUN), `programming` → `programming` (NOUN) — an `-ing` noun is already its own base form

**Try it:** the `better`/`best` → `well` lines are the proof this is vocabulary + morphology, not suffix chopping: no rule-based stemmer gets there (compare Ch. 09).""",
3: r"""## 2. spaCy vs NLTK

NLTK's `WordNetLemmatizer` needs the POS passed in — the default is noun. If you lemmatize verbs without saying so, they come back untouched. spaCy infers the POS from context automatically, which is the whole difference in practice.

**What the code does:** compares spaCy against NLTK with noun and verb POS on five words:
- `developed`: spaCy `develop`; NLTK(noun) `developed`; NLTK(verb) `develop` — the default noun call does nothing
- `analyses`: spaCy `analysis`; NLTK(verb) `analyse` — WordNet's British spelling
- `better`: spaCy `well`; NLTK returns `better` either way — no adverb rule wired in by default
- `deployment`: unchanged everywhere — already a base form

**Try it:** the `developed` row is the takeaway — `lem.lemmatize(w)` without `pos='v'` silently no-ops on verbs, the most common source of "why is my lemmatization not working" bugs. spaCy's automatic tagging removes the entire class of error.""",
5: r"""## 3. When NOT to Lemmatize

Proper nouns — company names, tech brands, product names — must match *exactly* as written. Lemmatizing them lowercases and reshapes them, so `TensorFlow` becomes `tensorflow` and an exact match against the JD fails. The rule: lemmatize content words, preserve `PROPN`.

**What the code does:** first checks each term's lemma against its lowercased form, flagging any change:
- `Google` → `Google` — flagged CHANGED because the lemma keeps its capital (differs from `google`)
- `TensorFlow` → `tensorflow` — the case is stripped; flagged unchanged only because the lemma equals the lowercased input
- `Developer` / `Engineering` → lowercased as well

Then `smart_lem()` lemmatizes only non-PROPN tokens. In the stored run both pipelines print the same sentence (`Google develop TensorFlow for develop ML model`) — the hazard is invisible on this sample and shows up on the next unseen brand name, which is precisely why the guard is worth having.""",
7: r"""## Key Insight: Always preserve proper nouns (PROPN). Never lemmatize company names or tech brands.

**Lemmatization wins on content words and destroys proper nouns — so preserve `PROPN` and lemmatize the rest.** Inflection collapsing makes `Developed` and `developing` match `develop`; lemmatizing `TensorFlow` makes it match nothing. The pattern from this chapter — `t.lemma_ if t.pos_ != "PROPN" else t.text` — is the one to ship.

Resume keywords split cleanly along the same line: skills and action verbs benefit from lemmas; company names, tools, and product names need their exact surface form. The next chapter, Ch. 09 stemming, solves the same problem with rules instead of vocabulary — faster, cruder, and mostly wrong for this use case.""",
8: r"""**Quick reference — lemma behavior**

| Input | Lemma | POS | Note |
|---|---|---|---|
| `running`, `ran` | `run` | VERB | regular + irregular collapsed |
| `better`, `best` | `well` | ADV | irregular; not `good` |
| `was` | `be` | AUX | auxiliary normalized |
| `mice` | `mouse` | NOUN | irregular plural |
| `analyses` | `analysis` | NOUN | Latin plural, singular lemma |
| `programming` | `programming` | NOUN | `-ing` noun is already base |
| `TensorFlow` | `tensorflow` | PROPN | case stripped — preserve instead |

Use this table as a sanity checklist: if your lemmatizer output for any of these rows differs, your pipeline (POS model, vocabulary, or custom rules) has drifted from the baseline this chapter establishes.""",
9: r"""**Pitfalls that cost real matching accuracy**

- Forgetting POS: `WordNetLemmatizer` defaults to noun, so verbs pass through unchanged — always pass `pos='v'` or use a tagger-driven lemmatizer like spaCy.
- Lowercasing brands: a lemma of `tensorflow` will never match the JD text `TensorFlow` under exact comparison; route proper nouns around the lemmatizer.
- Lemmatizing acronyms and version strings: `AWS`, `C++`, `Python 3.11` — lemmatization has nothing to add and can only corrupt them; skip tokens whose shape is already canonical.
- Trusting output blindly: the stored outputs in this chapter are ground truth for the installed spaCy version; a model upgrade can change lemmas (especially irregulars), so re-verify the table above after any environment change.""",
10: r"""**Next up — Ch. 09 Stemming**

Lemmatization is the accurate but heavier tool: it needs a vocabulary and a POS tag per token. **Stemming** does the same job with pure suffix-stripping rules — no dictionary, no POS — which makes it fast and vocabulary-free but crude: `engineering` → `engin`, `happily` → `happili`. The next chapter runs Porter vs Snowball on the same resume vocabulary to show exactly where the speed comes from and what it costs. After that, Ch. 10 POS tagging explains how the lemmatizer gets the POS signal it depends on.""",
})

# ============================================================ 09 — Stemming
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\09_stemming\09.ipynb", replace={
0: r"""# 09 — Stemming
**Goal:** Understand rule-based word reduction.

Stemming reduces words by stripping suffixes with rules — no dictionary, no part-of-speech awareness. Porter (1980) and Snowball (Porter2) are the classic algorithms, and they are extremely fast: a pure string transform applicable to any vocabulary in any domain. The cost of that speed is crudeness — stems are frequently not real words.

**Why it matters for resumes / ATS:** stemming is a legitimate choice for high-volume search indexing where recall-per-byte beats precision. But resume–JD matching is exact-keyword matching on real words, and a stem like `engin` never appears in a job description. This chapter builds the case that Ch. 08's lemmatization — not stemming — belongs in the resume pipeline.""",
1: r"""## 1. Porter vs Snowball

Porter and Snowball are sibling rule sets: Snowball (Porter2) is a cleaner, better-documented rewrite of Porter with improved rules for common English endings. On most words they agree; the differences show up on edge cases. Both share the fundamental limitation — rules only, no vocabulary.

**What the code does:** stems seven words with `PorterStemmer()` and `SnowballStemmer("english")`:
- `running` → `run` (both), `programming` → `program` (both) — suffix stripping at its best
- `ran` → `ran` — no rule covers irregulars; stemming cannot know `ran` is `run`
- `better` → `better` — not `good`
- `happily` → `happili` — a non-word; the `ily` ending is chopped but no dictionary repairs it
- `analyses` → `analys`, `leaves` → `leav`

**Try it:** the `happili` and `ran` rows are the whole story: stems are not words, and irregulars are invisible to rules.""",
3: r"""## 2. The Crudeness Problem

Aggressive suffix stripping over-conflates: words that should stay distinct collapse onto the same stem, and technical vocabulary gets mangled past recognition. For resume keywords — where `engineering` must match `engineer`, not `engin` — this is a precision disaster.

**What the code does:** stems six resume-adjacent words with Porter:
- `university` → `univers` and `universal` → `univers` — a school and an adjective are now identical
- `organization` → `organ` and `organize` → `organ` — conflated, and the stem is a body part
- `engineering` → `engin` and `engineer` → `engin` — the stem is not even a word

**Try it:** these pairs are the argument in miniature: any exact match against a JD fails, and the false conflations merge concepts an ATS must keep separate. When your stems stop looking like words, the algorithm has stopped serving the task.""",
5: r"""## Decision Guide
- STEMMING: Fast search indexing, TF-IDF vocab reduction
- LEMMATIZATION: Production NLP, resume matching, NER
- **Use lemmatization for resume analysis**

The line is speed vs correctness. Stemming is a single string transform — no model, no vocabulary, no POS — so it wins wherever you process millions of documents and only need token *groups* (TF-IDF vocabulary reduction, inverted-index recall). Lemmatization needs a vocabulary and a tagger but returns real words, which is what keyword matching, resume–JD comparison, and NER all require.

For this project the decision is made: lemmatize (Ch. 08) and preserve proper nouns. Stemming remains the fallback for languages or domains without a lemmatizer — and it closes the word-form trilogy (Ch. 07 stop words → Ch. 08 lemmas → Ch. 09 stems). Ch. 10 POS tagging next explains the signal that makes lemmatization accurate.""",
})

# ============================================================ 10 — POS Tagging
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\10_pos_tagging\10.ipynb", replace={
0: r"""# 10 — POS Tagging
**Goal:** Label every word with its part of speech.

Part-of-speech tagging assigns each token a grammatical class — noun, verb, adjective, determiner. It is the first stage in the pipeline that reasons about *syntax* rather than strings: the same word can be a noun in one sentence and a verb in another, and only context decides. Modern taggers (spaCy's) are sequence models trained on annotated text, so they are fast, accurate, and need no rule lists.

**Why it matters for resumes / ATS:** resume bullets are written as action-verb leads — "Developed…", "Reduced…", "Collaborated…". POS is what lets software find the action word in each bullet, verify that a bullet starts with a verb, and separate skills (nouns) from actions. It is also the input Ch. 08's lemmatizer needs and the foundation Ch. 11's dependency parsing builds on.""",
1: r"""## 1. Context Determines POS

A word's POS is not a property of the word — it is a property of the sentence. `book` is a verb in "I will book a flight" and a noun in "That book is interesting". A tagger resolves this from surrounding context; a rule or regex cannot.

**What the code does:** parses three sentences containing the same surface word and prints `token.text` + `token.pos_`:
- `book` → VERB, VERB, NOUN across the three sentences — the identical word flips class by context
- supporting cast: `will` → AUX, `is` → AUX, `interesting` → ADJ, `Please` → INTJ, `flight`/`restaurant` → NOUN

**Try it:** the stored output is the demonstration — same token, three labels, zero ambiguity for the model. This context-sensitivity is why POS tagging sits before lemmatization and dependency parsing in the pipeline.""",
3: r"""## 2. Action Verbs from Resume Bullets

Resume style guides demand bullets that open with a past-tense action verb. POS tagging turns that stylistic rule into an automatable check: parse the bullet, look at the first token's POS, and flag bullets that fail.

**What the code does:** for each of four bullets, finds the first `VERB` token and tests whether `doc[0].pos_ == "VERB"`:
- `Developed ML models using TensorFlow` — First verb `Developed`, starts with verb ✓
- `Led a team of 5 data scientists` — ✓
- `Reduced inference latency by 40%` — First verb: `None`, starts with verb: False
- `Collaborated with cross-functional teams` — ✓

**Try it:** the `Reduced` row is the interesting failure: spaCy tags the past participle as an adjective here (it reads "reduced latency" as a modified noun), so the heuristic misses a perfectly good action bullet. The check is cheap and useful, but it inherits the tagger's errors — treat it as a signal for review, not an oracle.""",
}, append=[
r"""## Key Insight

**POS turns words into grammar, and grammar into structure.**

Tagging is the pivot of the whole pipeline: it gives the lemmatizer its POS signal (Ch. 08), tells dependency parsing which words to connect (Ch. 11), and enables cheap, interpretable quality checks like "every bullet starts with a verb" — checks an ATS can run over thousands of resumes without any ML beyond the tagger itself.

The catch this chapter showed: taggers are statistical, and their errors propagate. A mis-tagged participle silently flips a bullet's quality flag. Next, Ch. 11 — Dependency Parsing — builds on these labels to recover who-did-what, the structure that turns tagged words into extractable facts.""",
])

# ============================================================ 12 — Named Entity Recognition
apply(r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_b\12_named_entity_recognition\12.ipynb", replace={
0: r"""# 12 — NER
**Goal:** Identify and classify named entities (people, companies, skills).

Named Entity Recognition (NER) locates spans of text that refer to real-world things — people, organizations, locations, dates — and classifies them. spaCy's statistical NER does this out of the box for general categories: the model tags `doc.ents` with `.text`, `.label_`, and character offsets.

**Why it matters for resumes / ATS:** an ATS profile is essentially an entity list: who (PERSON), where they worked (ORG), when (DATE), and what they know (skills). The base model covers the first three but is blind to skills — `Python`, `TensorFlow`, `AWS` are not in its label set. This chapter closes that gap with rule-based and hybrid extraction, which is what production resume parsers actually ship.""",
1: r"""## 1. Built-in spaCy NER

Out of the box, `doc.ents` gives typed spans for the categories spaCy was trained on — PERSON, ORG, GPE (cities/regions), DATE, and more. `spacy.explain(label)` decodes the three-letter codes into plain English, which matters when you read or debug extraction output.

**What the code does:** parses "Srivatsa Gorti worked at Google in Mountain View, CA from 2020 to 2023." and iterates `doc.ents`, printing each entity's text, label, and explanation:
- the name resolves to PERSON, `Google` to ORG, the location to GPE, and the year spans to DATE
- `spacy.explain(e.label_)` turns each code into a human-readable description

Note that this notebook's cells have no stored output — run them to see the extraction live. The contact block of any resume (name, employer, location, dates) lights up immediately; that is the part NER handles natively.""",
3: r"""## 2. The Problem: Skills Not Detected

Run the base model on a skills-heavy sentence and the pattern is unmistakable: companies and dates are found, skills are not. `Python`, `TensorFlow`, `AWS` are not entities in spaCy's ontology — the model was never trained to see them — so they vanish from `doc.ents` entirely.

**What the code does:** parses "Expert in Python, TensorFlow, and AWS at Microsoft since 2020." and prints whatever entities the base model finds, ending with the explicit print statement: "Notice: Python, TensorFlow, AWS are NOT found - they need custom NER!". Expect `Microsoft` → ORG and `2020` → DATE; the three skills produce no spans at all.

**Why:** skills are an open, fast-moving vocabulary — thousands of libraries, tools, and frameworks — that general news-corpus training data barely covers. No off-the-shelf model ships a skills label; that is a domain problem, and the next two sections solve it with rules.""",
5: r"""## 3. Adding Custom Skills with EntityRuler

`EntityRuler` is spaCy's rule-based entity component: you feed it patterns, it matches them, and its entities are merged into `doc.ents`. Added `before="ner"`, its matches take precedence over the statistical model — deterministic skill detection on top of probabilistic person/org detection.

**What the code does:** creates a second pipeline `nlp2`, adds the ruler before `ner`, and registers five SKILL patterns:
- string patterns for single tokens: `Python`, `TensorFlow`, `AWS`
- token-attribute patterns for multi-word skills: `[{"LOWER": "machine"}, {"LOWER": "learning"}]` — matches case-insensitively regardless of capitalization

Re-parsing the same sentence now yields the three skills as SKILL entities alongside Microsoft/2020. **Try it:** add "machine learning" to the test sentence in either case — the LOWER-based pattern catches it; a plain string pattern would not.""",
7: r"""## 4. Hybrid Regex + NER Extractor

Production resume extraction is hybrid: use the statistical NER for open classes (people, organizations — too varied for rules) and a curated dictionary plus regex for closed vocabularies (skills — finite and precise). The `ResumeNER` class packages exactly that split.

**What the code does:** `extract()` collects PERSON spans into `people` and ORG spans into `orgs` from `doc.ents`, then scans for each of 7 `known_skills` with `re.search(r'\b' + re.escape(s) + r'\b', text, re.IGNORECASE)` — word-boundary anchored, case-insensitive, and safe for skills containing special characters. Results accumulate into sets, so duplicates collapse.

Run it on "Srivatsa knows Python, AWS, and Docker. He worked at Google." and expect a dict of three sets: the name under people, Google under orgs, and Python, AWS, Docker under skills. The regex layer is transparent and auditable — you can see exactly which skills matched and why — which is a feature when clients ask how the extraction works.""",
}, append=[
r"""## Key Insight

**Base NER for open classes, curated rules for the closed vocabulary — that is the production pattern.**

Default spaCy NER gives the skeleton — person, employer, location, dates — the exact contact block every ATS needs. Skills are the domain gap: absent from the model, trivially added with `EntityRuler` patterns or a regex dictionary, and best handled by the hybrid that keeps both layers auditable.

This closes the extraction half of the pipeline: preprocessing → tokens → lemmas → POS → dependencies → entities. Next, Ch. 13 — Chunking & Phrase Extraction — packages entities and noun phrases into the clean structured fields (title, skills, achievements) an ATS can consume directly.""",
])

print("apply_block_b.py ran OK")
