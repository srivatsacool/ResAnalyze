from nbtools import apply

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\26_pdf_parsing\26.ipynb", replace={
0: r"""# 26 — PDF Parsing
**Goal:** Extract text from PDF resumes while preserving layout.

PDF is the format resumes most often arrive in — and the hardest to parse: the file describes *where glyphs are drawn on a page*, not what the text says. This chapter builds the PDF branch of the extraction pipeline: create a small resume PDF, pull its text back out with `pdfplumber`, and think about what multi-column layouts do to reading order.

**Why it matters for resumes / ATS:** an ATS must extract text before it can index skills or rank candidates. If extraction scrambles column order or silently drops text, every downstream stage — normalization (Ch. 29), language routing (Ch. 30), section detection (Ch. 32) — inherits the damage. Getting the text out in reading order here decides how much of the resume the rest of the pipeline ever sees.""",
1: r"""![Document Parsing Pipeline](../../../assets/images/document_parsing_pipeline_1785491201751.png)

> **Figure:** The Document Parsing Pipeline supporting PDF, DOCX and scanned images as input formats — all feeding the same normalization layer.

Three input formats, one exit: every branch of this pipeline must produce the same thing — clean, linear text for the normalizer. Chapters 26–28 cover the three branches in turn (PDF here, DOCX next, scanned images via OCR after that); the normalization layer they all feed into is Ch. 29.""",
2: r"""## 1. Why PDF is Hard

A PDF is a page-description format, not a text format: the file stores positioned glyphs and drawing commands, with no concept of paragraphs, reading order, or even a guaranteed text layer. Extraction therefore becomes a geometry problem — reconstructing sentences from coordinates.

**What the code does:** prints the standard hazard list for resume parsing:
- No inherent text flow — text is placed line by line, so paragraphs must be re-assembled
- Multi-column layouts — reading order must be recovered from x/y positions
- Tables, headers, footers — content that must be detected and handled deliberately
- Embedded fonts — custom encodings can map glyphs to the wrong Unicode codepoints
- Scanned PDFs — no text layer at all, so the file falls through to OCR (Ch. 28)

It also names the tool tiers: `pdfplumber` (layout-aware, the workhorse for resumes), PyMuPDF (`fitz`, very fast), and `pdfminer` (low-level building blocks). Expected output: the five challenges, then the tools line.""",
4: r"""## 2. Extracting Text with pdfplumber

This cell does a full round-trip: it *generates* a minimal resume PDF with `fpdf`, then reopens it with `pdfplumber` and calls `page.extract_text()` — the layout-aware method that merges glyphs into lines using their positions on the page.

**What the code does:**
- Builds the PDF: a centered name, the email, then bold `PROFESSIONAL SUMMARY` / `EXPERIENCE` headers with body text (`multi_cell` wraps the summary line)
- Saves to `/tmp/test_resume.pdf` and prints the file size in bytes
- Reopens with `pdfplumber.open()` and prints the first 200 characters of each page's extracted text

**Expected:** with the em dash handled, the size prints around 1.3 KB and `Page 1:` is followed by the text in reading order — `Srivatsa Gorti`, the email, the section headers, and the summary line. One version-sensitive trap: `fpdf2 >= 2.7.8` substitutes `Arial` with the built-in Latin-1 `Helvetica`, so the em dash in "Google — Senior Data Scientist" raises `FPDFUnicodeEncodingException` when saving. Replace the dash (or register a Unicode TTF) and the cell runs as described.""",
6: r"""## 3. Multi-Column Layout Handling

A two-column resume is the classic pdfplumber failure: naive extraction walks glyphs in file order, scrambling the two columns together. The fix is to treat extraction as a **layout problem** — cluster words by horizontal position, then read columns top-to-bottom, left-to-right.

**What the code does:** prints the standard column-recovery strategy:
1. Extract words with their bounding boxes (`extract_words()` gives `x0`, `top`, ...)
2. Cluster by x-coordinate into columns
3. Sort by y within each column
4. Merge columns left → right into reading order

**Try it:** `extract_text()` already handles *simple* multi-column pages; for complex ones (nested tables, sidebars) you drop to per-character extraction and implement the clustering yourself. Expected output: the four numbered steps, then the two tooling notes about `extract_text()` and per-character extraction.""",
8: r"""## Summary: Use pdfplumber for layout-aware extraction. PyMuPDF for speed.

**PDF parsing is a layout-reconstruction problem, not a text-reading one.** Choose `pdfplumber` when reading order matters (it always does for resumes) and PyMuPDF when raw speed beats fidelity. Whatever the tool, expect noisy output — stray headers, footer page numbers, column interleaving — which is exactly the mess the normalizer in Ch. 29 is built to clean.

Next up: the easy case. Where PDFs hide their structure, `.docx` files (Ch. 27) carry it explicitly — paragraphs, styles, and tables come back as first-class objects instead of positioned glyphs."""
})

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\27_docx_parsing\27.ipynb", replace={
0: r"""# 27 — DOCX Parsing
**Goal:** Extract text and structure from .docx resumes.

After PDF (Ch. 26), the second most common resume format is the Word `.docx` — and it is far friendlier to parse. A `.docx` is a ZIP archive of XML files in which paragraphs, styles, tables, headers, and footers are explicit objects, not positioned glyphs. This chapter creates a resume in that format and reads its structure back with `python-docx`.

**Why it matters for resumes / ATS:** section headers and skill matrices are real, queryable objects in DOCX — a heading is a `Heading 1` paragraph, a skills matrix is a table. That structure maps almost one-to-one onto the sections an ATS needs to build (Ch. 32), which makes DOCX the highest-fidelity input path in the whole extraction pipeline.""",
1: r"""## 1. Understanding DOCX Structure

Unzip a `.docx` and you find an XML package: `word/document.xml` holds the body content, `word/styles.xml` the formatting definitions, and `word/header*.xml` the running headers. `python-docx` wraps all of it so you work with `Document`, `Paragraph`, and `Table` objects instead of raw XML.

**What the code does:** prints that ZIP layout one line per part, then the punchline — DOCX is much easier than PDF because *sections, styles, and tables are explicit*: a heading knows it is a heading, a cell knows it is a cell.

**Expected output:** the three XML paths (`document.xml`, `styles.xml`, `header*.xml`), then the note that `python-docx` handles all of it. Compare with Ch. 26: nothing here needs coordinate math.""",
3: r"""## 2. Creating and Extracting DOCX

Round-trip time: the cell writes a small resume with `python-docx`, saves it, reopens the same file, and prints every non-empty paragraph with its **style name**. The style name is the key — it is stored in the XML and comes back intact, so `Title` and `Heading 1` paragraphs announce themselves.

**What the code does:**
- Sets the `Normal` style to Arial 11pt, then adds a `level=0` heading (the name), a contact line, `level=1` headings (`PROFESSIONAL SUMMARY`, `EXPERIENCE`) and body paragraphs
- Uses `add_run(...).bold = True` for the employer line — runs carry inline formatting inside a paragraph
- Saves to `/tmp/test_resume.docx` (about 37 KB in this environment — mostly XML boilerplate)
- Reopens and prints `[style] text` for each non-empty paragraph

**Expected:** `[Title] Srivatsa Gorti`, a `[Normal]` contact line, `[Heading 1] PROFESSIONAL SUMMARY`, the summary paragraph, `[Heading 1] EXPERIENCE`, and the job lines — the section skeleton of the resume recovered for free.""",
5: r"""## 3. Table Extraction

Skills matrices are the most table-shaped part of a resume, and DOCX stores them as real tables. `doc.tables` gives every table in the document; each one exposes `rows`, `columns`, and `row.cells` — no coordinate math required.

**What the code does:**
- Builds a 4×3 "Skills Matrix" table with the `Light Grid Accent 1` style, fills a header row (Skill / Level / Years) and three data rows
- Saves and reopens it, then iterates `doc4.tables`, printing each table's dimensions and every row's cell texts

**Expected:** `Table 1: 4 rows x 3 cols`, then the header row followed by the three skill rows (`Python`/`Expert`/`5`, `TensorFlow`/`Advanced`/`3`, `NLP`/`Advanced`/`4`). Rows-of-cells like this are ready to become structured skill lists for keyword matching — no parsing needed, just iteration.""",
7: r"""## Summary: DOCX preserves structure. python-docx handles paragraphs, styles, tables, headers, footers.

**DOCX gives you structure for free — so use it.** Where PDF parsing (Ch. 26) reconstructs paragraphs from coordinates, `python-docx` hands you `Paragraph`, `style.name`, and `Table` objects directly. The style names alone (`Title`, `Heading 1`) are a credible section map, which Ch. 32 will build on for section detection.

One caveat: not every resume reaches you as a `.docx`. Scanned pages and image-only files have no structure to preserve — those need OCR, which is exactly the fallback path in Ch. 28."""
})

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\28_ocr_basics\28.ipynb", replace={
0: r"""# 28 — OCR Basics
**Goal:** Extract text from scanned resume images using OCR.

Some resumes never contain text at all: they are scans, faxes, or screenshots of a printed page. Optical Character Recognition (OCR) is the branch of the pipeline that turns pixels back into characters so the rest of the NLP stack can process them like any other document.

**Why it matters for resumes / ATS:** older CVs, internationally mailed applications, and image-only exports all arrive as scans. If the pipeline has no OCR fallback, those resumes silently disappear from indexing. OCR is the safety net that keeps extraction complete — and, as this chapter shows, the noisiest input the normalizer (Ch. 29) has to clean.""",
1: r"""## 1. When to Use OCR

OCR is only needed when there is no text layer: scanned PDFs (an image wrapped in PDF syntax) and image-only files (PNG/JPG screenshots). If `extract_text()` returns empty or gibberish, that is the signal to switch branches. The cell also surveys the tool landscape — Tesseract (open-source, fast), EasyOCR (deep-learning, more accurate), and cloud Document AI (most accurate, but a service call).

**What the code does:** prints the two trigger cases, then the tool list with the two trade-off lines: accuracy `EasyOCR > Tesseract`, speed `Tesseract > EasyOCR`.

**Expected output:** the two trigger cases, the three tool names, and the accuracy/speed comparison. Takeaway: pick the cheapest tool that clears your accuracy bar — clean scans usually pass with Tesseract; handwriting or noisy scans justify the heavier engines.""",
3: r"""## 2. OCR with Tesseract

The cell synthesizes the whole scenario: it *draws* a fake resume with PIL (name, title, skills), saves it as PNG, and runs `pytesseract.image_to_string()` over it — the same call you would make on a real scan. Note the defensive structure: `ImportError` catches missing Python packages, and a bare `except` catches the missing Tesseract *system binary*, so the cell degrades to a printed hint instead of crashing the notebook.

**What the code does:**
- Creates a 400×200 white RGB image, draws three text lines with an Arial TTF (falling back to `ImageFont.load_default()` if the font is absent), saves to `/tmp/test_resume.png`
- OCRs the image and prints `=== OCR Result ===` plus the recognized text

**Expected:** on a machine without the Tesseract binary this prints `OCR error: tesseract is not installed or it's not in your PATH (needs Tesseract system install)` — the graceful-degradation path. With Tesseract installed, `image_to_string` returns the three drawn lines, typically with minor spacing/character artifacts; OCR output is never as clean as a native text layer.""",
5: r"""## 3. Image Preprocessing for Better OCR

OCR accuracy is decided before OCR runs: Tesseract performs best on clean, high-contrast, binarized input. The standard chain is grayscale → contrast enhancement → thresholding, turning a gray-on-white scan into black-on-white pixels.

**What the code does:**
- Opens the PNG from the previous cell and converts it to grayscale (`"L"` mode)
- Builds a `high_contrast` copy via `ImageEnhance.Contrast(...).enhance(2.0)`
- Thresholds with `gray.point(lambda x: 255 if x > 128 else 0)` — a hard cutoff at level 128 producing a binary image
- Prints the preprocessing note; the whole body is wrapped in `try/except: pass` so a missing file fails silently

**Watch:** the threshold is applied to the original `gray` image, not to the `high_contrast` copy — a common off-by-one in this chain. In practice, binarizing the *enhanced* image gives Tesseract the better input. Expected output: the single preprocessing line.""",
7: r"""## Summary: OCR is a fallback for scanned PDFs. Preprocess images for best results.

**OCR is the last-resort extraction path — and the noisiest.** Only route to it when the file has no text layer; preprocess (grayscale → contrast → threshold) before running Tesseract; and treat the output as provisional, because character errors are guaranteed on real scans. It is also the path with the most moving parts (Python package + system binary), so error handling matters — Ch. 31 builds exactly that machinery.

Whatever branch produced the text — PDF (Ch. 26), DOCX (Ch. 27), or OCR — it now needs cleaning before any NLP runs. That cleaning is Ch. 29: text normalization for resumes."""
})

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\29_text_normalization_for_resumes\29.ipynb", replace={
0: r"""# 29 — Text Normalization for Resumes
**Goal:** Domain-specific cleaning for messy resume text.

Everything Ch. 26–28 extracted is raw: bullet glyphs, ALL-CAPS headers, abbreviations, pipes and slashes splitting skill lists, tabs left over from PDF column reconstruction. Normalization is the layer that turns that mess into predictable, NLP-ready text — without losing the content the downstream stages need.

**Why it matters for resumes / ATS:** an ATS matches keywords, and matching fails on formatting. `Python|NLP/TensorFlow` will not hit a "Python" keyword index as reliably as `Python, NLP, TensorFlow`. Normalizing separators, expanding abbreviations, and collapsing whitespace is cheap and improves every later stage — tokenization, section detection (Ch. 32), and skill matching.""",
1: r"""## 1. Resume-Specific Challenges

General-purpose text cleaning is not enough — resumes have a distinctive noise profile: decorative bullet glyphs, abbreviations (`Sr.`, `Engr.`, `w/`), ALL-CAPS section headers, and skill lists whose separators are punctuation soup (`|`, `/`, `.`). A normalizer has to know these patterns and decide what to do with each.

**What the code does:** prints the five issue classes as a checklist — bullet symbols, abbreviations, all-caps headers, skill-list separators, and mixed separators.

**Expected output:** the `Resume text issues:` header followed by the five bullets. The deeper point: two of these classes are *noise* (bullets, whitespace) and two are *signal* — ALL-CAPS headers are the section map Ch. 32 will read, and abbreviations expand into the canonical terms an ATS index expects. Normalization must tell them apart.""",
3: r"""## 2. Resume Normalizer

`ResumeNormalizer` chains five transforms in a fixed order. The first step is the subtle one: `unicodedata.normalize("NFKD", ...)` followed by an ASCII `encode(..., "ignore")` — this decomposes accented characters and drops everything that still is not ASCII. It strips diacritics (`résumé` → `resume`) and smart punctuation, but it is lossy for genuinely non-Latin text.

**What the code does, step by step:**
- NFKD normalize + ASCII-ignore encode — removes accents and non-ASCII glyphs
- Bullet regex — maps `• ‣ ● ◘ ◙ ➜` to `>`; note the order: bullets are *already gone* by this step (dropped by the ASCII pass), so this regex is dead code as written
- `\t|\r` → space; `\n{3,}` → `\n\n`; ` {2,}` → ` `; final `strip()`

**Expected (verified):** `Before:` shows the raw sample with `•` bullets and a tab; `After:` is `'Srivatsa Gorti\n Python specialist\n NLP engineer\n TensorFlow expert'` — bullets silently removed (leaving a stray space where each was), tab collapsed to a space, double spaces gone. Lesson: transform order is part of the design — the ASCII pass must come *after* any mapping you want to survive it.""",
5: r"""## 3. Abbreviation Expansion

Abbreviations are a vocabulary problem: `Sr.`, `Engr.`, `w/`, `yrs` all need expanding to canonical forms so keyword matching and later stages see one spelling. This cell builds a dictionary-driven expander with a single case-insensitive regex pass over `\b`-delimited alternatives.

**What the code does:**
- Compiles `\b(sr\.|jr\.|...|yrs|yr)\b` from the map keys using `re.escape` and `re.IGNORECASE`
- Substitutes via a lambda that looks up the lowercased match in `abbrev_map`

**Expected (verified):** only the word-final entries fire — `'Sr. ML Engr. w/ 10+ yrs exp.'` → `'Sr. ML Engr. w/ 10+ years exp.'`, and `'B.Tech CSE & M.S. Data Science'` comes back unchanged. The reason is instructive: `\b` is a boundary *between* a word character and a non-word character, so any abbreviation ending in `.` or `/` (and `&`) never satisfies the trailing `\b` — there is no word character after the period. Matching the period inside the pattern (e.g. `sr\.(?=\s|$)`) fixes it; a classic regex-boundary pitfall.""",
7: r"""## Summary: Resume normalization must preserve content while removing noise. Light touch is better.

**Normalize light — preserve signal, remove noise.** Collapse whitespace and unify separators, expand abbreviations to canonical terms, and strip decorative glyphs; but do not lowercase everything or crush ALL-CAPS headers, because those carry the section structure Ch. 32's section detection depends on. Over-aggressive cleaning (stemming, stopword removal) belongs to a later stage, not this one.

The output of this chapter — clean, predictable text — is the input contract for everything that follows: language detection (Ch. 30) decides which NLP model sees it, and section detection (Ch. 32) finally rebuilds the structured profile."""
})

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\30_language_detection\30.ipynb", replace={
0: r"""# 30 — Language Detection
**Goal:** Detect resume language for correct NLP pipeline selection.

Resumes arrive in many languages, and every NLP stage after this one is language-specific: a spaCy model trained on English mangles French, and the abbreviation expander from Ch. 29 is meaningless for German. Language detection is the router that picks the right model before any parsing or matching happens.

**Why it matters for resumes / ATS:** a multinational candidate pool means multilingual resumes are the norm, not the edge case. Detecting the language up front lets the pipeline load `fr_core_news_sm` for a French CV instead of silently running English NLP on it — the difference between a parsed profile and garbage.""",
1: r"""## 1. Language Detection Basics

`langdetect` is a Python port of Google's language-detection library: it profiles text by character **n-gram frequencies** and scores languages with a naive-Bayes-style model trained on many languages. `detect()` returns a single ISO-639-1 code; `detect_langs()` returns the full ranked list with probabilities.

**What the code does:** runs three parallel sentences (English, French, German) through both functions, prints the top language and its confidence, and marks the row `OK` when the detected code equals the *expected* code.

**Expected (verified):** all three are detected correctly with ~0.9999 confidence (`en`, `fr`, `de`). But the German row prints a blank `OK` flag — the check uses `expected[:2].lower()`, i.e. `"German"[:2] == "ge"`, which is not Germany's code `de`. The *detector* is right; the *test* is a naive name→code guess. Detection confidence on short fragments is far lower, which is exactly the failure mode the next section's routing can trigger.""",
3: r"""## 2. Multi-Language Pipeline Selection

Detection is only useful if it changes behavior. This cell builds the router: detect the language, look up the matching spaCy model in `LANG_MODELS`, and fall back to the English model for anything unknown or empty.

**What the code does:**
- Maps ISO codes to spaCy models (`en`→`en_core_web_sm`, `fr`→`fr_core_news_sm`, `de`→`de_core_news_sm`, `es`→`es_core_news_sm`)
- `select_pipeline(text)` detects the language (defaulting to `"en"` for blank text) and returns `LANG_MODELS.get(lang, "en_core_web_sm")` — the fallback catches unsupported languages
- Prints the model to load for three test phrases

**Expected (verified):** `'I love Python'` → `en_core_web_sm` and `'Ich liebe Python'` → `de_core_news_sm`; but `'J'adore Python'` is so short that `langdetect` mis-routes it to `en_core_web_sm`. That is the classic short-text failure — a single shared word (`Python`) dominates the n-gram profile. A production router guards with a minimum text length or a confidence threshold. Note also: `fr_core_news_sm` and friends must be downloaded separately (`python -m spacy download fr_core_news_sm`) — this cell only selects the name.""",
5: r"""## Summary: Langdetect is fast and accurate enough for resume language routing.

**Detect the language before you choose the NLP pipeline — and never trust a single short fragment.** `langdetect` is fast and accurate on real resume-length text (~0.9999 confidence), but degrades on tiny inputs, so route with a length/confidence guard and a sensible default (English). The chosen model name becomes a parameter for every later stage: normalization conventions (Ch. 29), tokenization, and section detection (Ch. 32).

One more reality check before the pipeline is complete: parsers fail. Corrupt files, empty uploads, and mislabeled extensions are normal in production — Ch. 31 builds the error handling so a single bad resume never takes down the batch."""
})

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\31_parsing_error_handling\31.ipynb", replace={
0: r"""# 31 — Parsing Error Handling
**Goal:** Gracefully handle corrupt files, empty documents, and edge cases.

Chapters 26–30 assumed the input is a valid PDF, DOCX, or image. Real resume uploads are not that polite: truncated downloads, password-protected files, 0-byte uploads, and mislabeled extensions happen constantly. This chapter hardens the extraction layer so a single bad file degrades to a warning instead of crashing a batch run.

**Why it matters for resumes / ATS:** a parsing pipeline that throws on one corrupt resume stops the whole batch — every candidate after it goes unprocessed. Error handling is not boilerplate here; it is what separates a demo script from a service you can point at a production inbox.""",
1: r"""## 1. Common Failure Modes

The failures cluster at different layers, which decides where you catch them. Container corruption (broken ZIP/PDF structure) fails at open; 0-byte and truncated files fail at read; password protection fails at decrypt; image-only PDFs fail at `extract_text()` with an *empty result, not an exception*; wrong extensions fail at dispatch — you hand a PDF parser a `.docx`; encoding errors fail at decode.

**What the code does:** prints the seven failure classes as a checklist — corrupt PDF/DOCX, empty files, password-protected documents, image-only files, wrong extension, truncated downloads, non-UTF8 content.

**Expected output:** the bullet list of all seven. Notice the shape: some modes raise, some return empty text, some return garbage — so a robust parser must handle all three outcomes, not just exceptions. That asymmetry drives the design in section 3.""",
3: r"""## 2. Magic Byte File Detection

Extensions are untrusted input — anyone can name a `.docx` file `.pdf`. Magic bytes are the file's own signature: `%PDF` for PDF, `PK\x03\x04` for any ZIP-based format (`.docx`, `.xlsx`, `.pptx`), `\x89PNG` for PNG, `\xff\xd8\xff` for JPEG. `detect_type()` reads the first 4 bytes and matches prefixes against that table.

**What the code does:**
- Writes a fake `%PDF-1.4` payload to a temp file whose *name* ends in `.pdf`
- Runs `detect_type()` and prints the detected type next to the extension

**Expected (verified):** `Detected: pdf (vs extension: .pdf)` — trivially matching here, but the same check catches the real danger: a `.pdf`-named file whose bytes start `PK\x03\x04` (a ZIP, i.e. actually a DOCX) reports `docx`. That mismatch tells you the parser must be chosen by *content*, not name. Four bytes are enough for these signatures; other formats need longer prefixes.""",
5: r"""## 3. Robust Document Parser with Fallbacks

The parser as a **strategy chain**: register extractors in order of preference, try them one by one, keep the first one that returns non-empty text, and log-and-continue on failure. If every strategy fails, return `""` — a defined fallback rather than a crash. This mirrors the Ch. 26–28 tool stack: `pdfplumber` → PyMuPDF → OCR is the natural chain, each step slower but more tolerant than the last.

**What the code does:**
- `SafeParser` holds an ordered `strategies` list; `add(name, fn)` appends an extractor
- `parse(filepath)` loops the strategies, catches any `Exception` per strategy (printing `name failed: ...`), and returns the first non-empty result
- Registers three stub extractors and calls `parse("test.pdf")`

**Expected:** `Result: 'extracted pdf text'` — the first strategy succeeds immediately. With the stubs replaced by real parsers, a corrupt PDF prints `pdfplumber failed: ...`, then `PyMuPDF failed: ...`, then falls through to OCR or `""`. Note the guard `if text and text.strip()` — it treats *empty* output as failure too, catching the image-only-PDF case that raises nothing.""",
7: r"""## Summary: Always validate file types by magic bytes, not extension. Layer fallbacks.

**Assume every file is hostile until proven otherwise.** Validate by magic bytes, not extension; treat empty output as failure just like exceptions; and chain fallback strategies (PDF → PyMuPDF → OCR) so a single corrupt file costs one warning, not the whole batch. Defined fallbacks — `""` for text, `"unknown"` for type — keep downstream stages from crashing on missing data.

This closes the extraction half of the pipeline: from file bytes (Ch. 26–28) through cleaning (Ch. 29) and routing (Ch. 30), everything now produces *clean, language-aware text* — or a graceful failure. The next chapter finally gives that text meaning: Ch. 32, Section Detection, turns it into a structured profile."""
})

print("apply_block_e.py executed OK")
