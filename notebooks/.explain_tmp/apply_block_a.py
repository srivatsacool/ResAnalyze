# apply_block_a.py — expand markdown cells in the 4 block_a notebooks.
# Keeps every existing markdown line EXACTLY (extends, never rewrites headings),
# never touches code cells, appends Key Insight where missing.
import json
from nbtools import load, apply

CH00 = r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\00_environment_setup\00.ipynb"
CH01 = r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\01_python_engineering_refresher\01.ipynb"
CH02 = r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\02_pandas_&_numpy\02.ipynb"
CH03 = r"D:\Projects\ResAnalyze\notebooks\part1_foundations\block_a\03_regex_mastery\03.ipynb"

PATHS = [CH00, CH01, CH02, CH03]


def extend(path, additions, append=None):
    """additions: {cell_index: extra_markdown}; keeps existing source, appends extra."""
    nb = load(path)
    replace = {}
    for idx, extra in additions.items():
        src = "".join(nb["cells"][idx]["source"])
        if src.strip():
            replace[idx] = src.rstrip("\n") + "\n\n" + extra
        else:
            replace[idx] = extra
    return apply(path, replace=replace, append=append)


# ---------------------------------------------------------------- snapshot
snapshot = {}
for p in PATHS:
    nb = load(p)
    snapshot[p] = {
        "code": ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"],
        "md": ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"],
    }
with open(r"D:\Projects\ResAnalyze\notebooks\.explain_tmp\snapshot.json", "w", encoding="utf-8") as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=1)

# ================================================================ CH00
add00 = {
0: r"""Every notebook in this series runs on the stack you assemble here: a Python interpreter >= 3.10, an isolated environment, the numeric/ML/NLP libraries, spaCy's English model, NLTK's data packs, and Git for versioning. The cells below verify each layer in turn, so when something fails in a later chapter you know exactly which layer to blame.

**Why a solid environment matters:** nothing you build later — tokenizers, parsers, the ATS scoring engine — runs without this foundation, and a reproducible setup is what lets you ship consistent output. It is also a standard screening topic: interviewers probe how you manage virtual environments, package versions, and model/data downloads. Get this chapter right and every following notebook "just works" — that is the point.""",
1: r"""Python 3.10+ is the floor for this curriculum: the type hints, dataclasses, and modern typing used throughout (plus current NumPy, pandas, and spaCy releases) all assume it. The cell prints the interpreter's identity so a version mismatch never becomes a mystery later.

**What the code does:**
- `sys.version` prints the full build string — the stored output shows **Python 3.12.3** on **win32**.
- `sys.executable` resolves the exact interpreter path (`c:\Users\MSI\AppData\Local\Programs\Python\Python312\python.exe` here) — the first thing to check when `python` on your PATH points somewhere unexpected.
- `assert sys.version_info >= (3, 10)` hard-stops the notebook on older interpreters with a clear message.

**Try it:** the trailing `✓ Python version OK` line confirms the assertion passed on this machine. Run the same cell in any other environment you plan to use for the project.""",
3: r"""**Why isolate at all:** different projects pin different — sometimes conflicting — versions of NumPy or spaCy. An environment keeps each project's dependencies self-contained, and a `requirements.txt` or `environment.yml` makes the setup reproducible for anyone cloning the repo.

| | venv | conda |
|---|---|---|
| Ships with | Python stdlib | Anaconda / Miniconda |
| Package source | pip (PyPI) | conda + pip |
| Best for | lightweight, single-version projects | data/ML stacks with non-Python deps |

The exact tool matters less than consistency: this repository's notebooks assume one activated environment, with every dependency either already installed or installed by the next cell.""",
4: r"""This list is the project's dependency contract: `numpy`/`pandas` for tabular data, `scikit-learn` for ML models, `spacy`/`nltk` for NLP, `matplotlib`/`seaborn` for visualization, and `jupyter`/`nbformat` for the notebook tooling itself.

**What the code does:**
- `importlib.import_module(pkg.replace("-", "_"))` probes each package without importing at module level — an `ImportError` means *not installed*.
- On failure it falls back to `subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])`, so the notebook self-heals on a fresh machine.
- The stored output shows most packages already present; `scikit-learn` was installed on the fly.

**Why it matters:** every later notebook opens with imports from this list — if a cell here fails, fix it before moving on, not in Ch. 04.""",
6: r"""spaCy ships as code *plus* a trained model: `en_core_web_sm` is the small English pipeline whose components (tagger, parser, NER) power Ch. 10–12. The `sm` suffix means speed over accuracy; `md`/`lg` trade up as needed.

**What the code does:**
- `spacy.load("en_core_web_sm")` inside `try`/`except OSError` — a missing model raises `OSError`, which triggers a one-time `python -m spacy download`, then loads.
- A smoke test parses a sentence: the stored output shows 8 tokens and the entity `('NLP', 'ORG')` — spaCy's NER already recognizes *NLP* as an organization, zero extra code.

**Try it:** entity extraction like this is exactly the Ch. 12 named-entity material — running here with one line.""",
8: r"""NLTK is code plus *data*: tokenizers, stopword lists, and WordNet are downloaded once per machine. Each `nltk.download(...)` call is idempotent, and `quiet=True` suppresses repeat-download chatter.

**What the code does:**
- Pulls `punkt_tab` (sentence/word tokenizer data), `stopwords`, `wordnet` (the Ch. 08 lemmatizer's lexicon), and `averaged_perceptron_tagger_eng` (the Ch. 10 POS tagger).
- The final import verifies the download: the stored output reports **198 English stopwords** — the exact list Ch. 07 will filter on.

**Try it:** rerun the cell — downloads are skipped once the data exists, which is why reruns stay quiet.""",
10: r"""Git records *who* changed what: `user.name` and `user.email` are stamped onto every commit. Unset, commits get a generic identity and `git blame` / PR tooling becomes useless.

**What the code does:**
- Two `git config --global` calls set the identity; `--global` applies to every repo on this machine.
- `git config --list | findstr user` filters the config to the identity lines — the Windows cousin of `grep user`.
- The stored output shows the placeholder values: **replace `Your Name` / `your.email@example.com` with your real identity** before your first commit.

**Try it:** run `git config user.name` afterwards to confirm the value stuck.""",
12: r"""The layout mirrors the learning path: **Part I** builds the NLP toolbox (foundations → pipeline → text representation → embeddings), **Part II** assembles it into the ATS stack (parsing → extraction → matching → scoring). Each numbered folder is one notebook; `block_a` (00–03) is the environment and language tooling this chapter is standing on.

Keep this map in mind when later chapters reference "the extractor from Ch. 03" or "the scoring engine from Ch. 54" — every piece has a home, and the numbering keeps dependencies one-directional.""",
13: r"""The final gate: import every core library in one cell and print its version. This turns "my code broke" into "which library is the wrong version" — the first question in any debugging session.

**What the code does:**
- One import block covering the whole stack, then `__version__` per library: the stored output shows NumPy **1.26.4**, pandas **2.2.3**, scikit-learn **1.7.2**, spaCy **3.8.14**, NLTK **3.10.0**.
- Those version numbers pin what the rest of the curriculum was written and tested against.

**Try it:** run this after any environment change (new machine, new conda env, `pip upgrade`) — it should always end with the ready message.""",
}
append00 = [r"""## Key Insight

**A reproducible environment is the silent dependency of every result in this curriculum.**

Everything that follows — tokenizers, parsers, the scoring engine — runs on exactly this stack: interpreter, isolated environment, pinned library versions, downloaded models, and a committed Git identity. When a later notebook misbehaves, this chapter is the checklist: version mismatch, missing model, unset identity. With the foundation verified, the next chapter sharpens the language the pipeline is written in — Ch. 01, Python Engineering Refresher."""]

# ================================================================ CH01
add01 = {
0: r"""This chapter is a *language* refresher, not an NLP one: the Python idioms production NLP code is written in. Typed functions, dataclasses, comprehensions, generators, context managers, narrow exception handling, and function composition all reappear throughout the series — usually without explanation.

**Why it matters for resumes / ATS:** the mini resume parser at the end of this chapter is the project's first artifact, built exclusively from these idioms. Interviewers probe exactly this material (type hints, the mutable-default trap, generator memory, pipeline composition) when they ask you to walk through parsing code — and this chapter is where you build that answer.""",
1: r"""Type hints document *intent* at the signature: readers and tools (`mypy`, IDE autocomplete) see what a function consumes and returns without reading its body. They are not enforced at runtime — they are contracts for humans and linters.

**What the code does:**
- `extract_skills` (untyped) vs `extract_skills_typed(text: str) -> List[str]`: same job, but the typed version also strips empties and declares its contract up front.
- `Optional[str]` is the honest signature for a function that may return `None` — the stored output shows both branches: a match returns the email, no match returns `None`.
- The email regex (`[\w.+-]+@[\w-]+\.[\w.]+`) is Ch. 03 material; here it just feeds the typing lesson.

**Try it:** the two `Email found:` lines in the output — one match, one `None` — show exactly why the return type must be `Optional`.""",
3: r"""A `@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__` from field annotations — a plain class would need ~15 lines of boilerplate for the same result. Mutable defaults must go through `field(default_factory=list)`, or every instance shares one list (the classic Python gotcha).

**What the code does:**
- `Skill` (name, category, confidence) and `Resume` (name, email, skills) model a parsed resume as typed records.
- `Resume.add_skill(...)` appends a `Skill`; `top_skills(threshold=0.8)` filters on confidence.
- The stored output shows the auto-generated `repr` and `Top skills: ['Python', 'NLP']` — the 0.95/0.88-confidence skills clear the 0.8 bar while Java (0.6) drops out.

**Why it matters:** structured records like these are what every later extractor emits — dataclasses are this project's standard container.""",
5: r"""Comprehensions are loops that *return a value* — and in CPython they run in C-accelerated bytecode, faster than an equivalent `for` + `append` and usually clearer. Dict and set comprehensions extend the same syntax to the other container types.

**What the code does:**
- The loop and the comprehension produce identical output (`['Python', 'NLP', 'Machine Learning']`) after stripping whitespace and dropping the empty string.
- `skill_lengths = {s: len(s) for s in cleaned}` builds a length lookup — the stored output shows `'Machine Learning': 16`, spaces and all.
- The set comprehension collapses every character across all skills: the output's **15 unique chars** is the deduplicated alphabet of the skill list.

**Try it:** compare line counts of the two versions — then note the comprehension is also the one you can nest inside a larger expression.""",
7: r"""Generators produce values *lazily*: nothing is computed until `next()` is called, so a generator over a huge corpus costs constant memory. `yield` turns any function into a generator; generator expressions (`(x for x in ...)`) do the same inline.

**What the code does:**
- `read_chunks` yields 100-character slices of a 30 KB string; `type(chunks)` reports `<class 'generator'>` — no list was ever materialized.
- `next(chunks)` pulls one chunk at a time, as the two printed chunks show.
- `sum(1 for chunk in ... if "NLP" in chunk)` counts matching chunks without building any intermediate list — the whole point.

**Why it matters:** resumes, job-description corpora, and training text are processed chunk-by-chunk exactly this way when they don't fit in memory.""",
9: r"""The `with` statement guarantees the file is closed even when the body raises — manual `f.close()` in `try/finally` is the error-prone alternative. Files also stream: `for line in f` reads lazily, one line at a time, which is how you process files larger than RAM.

**What the code does:**
- Writes a sample resume with `open(..., 'w')`, then reads it back.
- Deliberately demonstrates the **file-pointer trap**: after `f.read()` consumes the stream, `f.readlines()` returns `[]` — the inline comment flags it as a demo of stateful file objects.
- The correct read reopens the file and iterates lines lazily; the stored output prints each stripped line of the resume.

**Try it:** delete the second `with` block and rerun — you will see the empty `readlines()` result the notebook warns about.""",
11: r"""Production parsing assumes hostile input: `None`, wrong types, empty strings, malformed lines. The pattern is *raise early with a specific exception, catch narrowly, degrade gracefully* — and never swallow `Exception` silently.

**What the code does:**
- `safe_extract_email` validates first: `TypeError` for non-strings, `ValueError` for empty text, then the regex.
- The `except (TypeError, ValueError)` branch logs a warning and returns `None`; a catch-all `except Exception` is the last resort.
- The stored output walks the three cases: a real email extracts; `""` prints `Warning: Empty text` then `None`; `123` prints `Warning: Expected string, got <class 'int'>` then `None`.

**Why it matters:** every extractor in Ch. 03–13 inherits this shape — bad input must degrade to a missing field, never crash the pipeline.""",
13: r"""Functions are values: passable as arguments, storable, returnable. That makes *composition* trivial — `build_pipeline` chains any number of callables into one function, the same idea behind `sklearn.pipeline` and spaCy's component pipeline.

**What the code does:**
- `clean_text` (strip + lowercase) and `remove_numbers` (regex `\d+` removal) are plain functions.
- `build_pipeline(*functions)` returns a closure applying each function in order; `cleaner = build_pipeline(clean_text, remove_numbers)` fixes the pipeline once and reuses it.
- The stored output `Cleaned: 'hello  world!'` shows the double-space artifact left after digits are removed — a real reminder that composed transforms interact.

**Try it:** add a third function (e.g. collapse repeated spaces) to the pipeline and watch the artifact disappear.""",
15: r"""This cell is the chapter's payoff: a first working resume parser built only from the idioms above. It is deliberately *heuristic* — name = first line with 2–3 words, contact = regexes, skills = substring match against a known list — and that honesty matters: it works on clean samples and stumbles on messy reality, which is exactly why the rest of Part I exists.

**What the code does:**
- `ContactInfo` / `SimpleResume` dataclasses hold the structured result.
- `extract_name` takes the first non-empty line if it has 2–3 words; `extract_contact` regexes email and phone (`[+]?[\d\s()-]{7,}`); `extract_skills` case-folds the text and checks membership against `known_skills`.
- The stored output is the full parse: **Srivatsa Gorti**, `srivatsa@email.com`, `+91-9876543210`, and 5 of 10 known skills — `Java`, `Spark`, `Docker`, `Kubernetes` correctly absent.

**Try it:** feed it a resume whose first line is a title ("Senior Data Scientist") — the heuristic returns the title as the name. That failure mode motivates everything from Ch. 03 onward.""",
17: r"""These patterns are the vocabulary of every notebook in this series: dataclasses for records, comprehensions for transforms, generators for streaming, context managers for I/O, narrow exceptions for hostile input, and composition for pipelines.

The next chapter swaps the *language* for the *data* layer — Ch. 02, Pandas & NumPy, vectorizes all of this over candidate and job-description tables.""",
}
append01 = [r"""## Key Insight

**Idiomatic Python is the difference between a demo and a pipeline.**

Every pattern in this chapter exists because production parsing code is typed, lazy, defensive, and composable: dataclasses give extractors a structured contract, generators keep corpora streamable, narrow exceptions keep hostile input from crashing a batch run, and function composition turns a sequence of transforms into a reusable pipeline — the exact shape of the ATS stack in Part II. This is also the code style later notebooks assume without comment. Next, the data layer those pipelines operate on — Ch. 02, Pandas & NumPy."""]

# ================================================================ CH02
add02 = {
0: r"""NumPy is the numerical engine under everything — pandas, scikit-learn, even spaCy's internals. Pandas adds labeled, tabular structure on top. Together they turn candidate and job-description data into something analysis-ready.

**Why it matters for resumes / ATS:** the ATS pipeline is a data problem before it is an ML problem — hundreds of resumes, each with extracted skills, experience, and scores, stored in a DataFrame, filtered with boolean masks, grouped by role, and correlated with outcomes. The Part II scoring engine is built almost entirely from the operations in this chapter.""",
1: r"""An `ndarray` is a fixed-type, contiguous block of memory — unlike a Python list (pointers to arbitrary objects), every element is the same C type, which is what makes vector math fast and cache-friendly.

**What the code does:**
- Construction idioms: `np.array` from a list, `np.zeros((3, 4))` / `np.ones((2, 3))` for blank canvases, `np.arange(0, 10, 2)` for ranges (`[0 2 4 6 8]`), `np.linspace(0, 1, 5)` for evenly spaced floats (`0, 0.25, 0.5, 0.75, 1`).
- `np.random.seed(42)` makes the following `randn(5)` reproducible — the stored output's five values are identical on every machine that runs this cell.

**Try it:** drop the seed and rerun — new values every time; restore it and the exact stored output returns. That determinism is what makes experiments comparable.""",
3: r"""Vectorized operations push the loop into NumPy's compiled C code, avoiding Python-level iteration overhead per element. On 10 million elements the difference is stark.

**What the code does:**
- The list comprehension `[x * 2 + 1 for x in data]` times at **3.566s** in the stored output; the vectorized `data * 2 + 1` finishes in **0.186s** — roughly **19× faster** on this machine.
- The printed `~10000x` banner is a hard-coded constant in the cell, not a measurement — trust the two timings, not the label.

**Why it matters:** every pandas operation in this chapter is vectorized underneath; scoring thousands of resumes stays instant only because of this.""",
5: r"""A boolean mask is an array of `True`/`False` used as an index: `scores[scores > 60]` keeps exactly the positions where the comparison holds. Combine conditions with `&` (and), `|` (or), `~` (not) — always parenthesized, because NumPy comparisons bind tighter than Python's `and`/`or`.

**What the code does:**
- `scores > 60` yields `[82 91 67 78 95]` — the five passing scores in the stored output.
- `(scores >= 80) & (scores <= 100)` narrows to `[82 91 95]`.
- `np.where(condition, 'Pass', 'Fail')` replaces elementwise; the output shows the full grade array.
- `.mean()` / `.std()` / `.min()` / `.max()` summarize: mean **68.2**, std **20.8**, range 33–95.

**Why it matters:** filtering a candidate pool ("scores above 80") is this exact operation applied to a DataFrame column.""",
7: r"""A Series is a 1D array with a *label per value* — the index. Labels make operations self-describing: `skills[skills > 0.8]` returns not just values but *which* skills qualify.

**What the code does:**
- Builds a `confidence` Series keyed by skill names; the stored output prints the labeled table plus `dtype: float64`.
- Boolean masking works exactly as in NumPy: `skills[skills > 0.8]` keeps `Python (0.95), NLP (0.88), TensorFlow (0.91)` and drops SQL (0.76) and Java (0.62).
- `.mean()` collapses to a scalar — **0.824** average confidence.

**Why it matters:** a skill→confidence mapping is the natural output of any skill extractor (Ch. 03, 10); a Series is its native container.""",
9: r"""A DataFrame is a 2D table of aligned Series whose columns may hold different types — `bool` next to `int` next to `str` — which is exactly what real candidate data looks like.

**What the code does:**
- Builds a 4-candidate table from a dict of lists; each dict key becomes a column.
- `df.shape` reports **(4, 5)** — four candidates, five fields.
- `df.describe()` summarizes the numeric columns (count/mean/std/min/quartiles/max); `ats_score` spans 45–91 with mean **71.25**.

**Why it matters:** this is the canonical shape of the project's data — one row per candidate, one column per extracted feature — the exact schema the Part II scoring engine consumes.""",
11: r"""Real pipelines rarely build DataFrames from scratch — they read them. `to_csv` / `read_csv` are the workhorses; the same API family covers Excel, JSON, Parquet, and SQL via `pd.read_*`.

**What the code does:**
- `Path("../../assets/tmp")` builds a repo-relative path; `mkdir(parents=True, exist_ok=True)` creates it if missing — `exist_ok` keeps reruns safe.
- `df.to_csv(tmp_path, index=False)` writes without the row index, so the round-trip reads back exactly 4 rows, as the stored output confirms (`Read back: 4 rows`).

**Try it:** rerun the cell — the ✓ still prints because the directory already exists. Then open `candidates.csv` in an editor: it is plain text, which is why CSVs are the lingua franca of data exchange.""",
13: r"""Real extracted data is exactly this messy: whitespace, mixed case, `None`, unparseable strings, duplicates, inconsistent formats. Cleaning is not glamorous — it is most of the job.

**What the code does:**
- `str.strip().str.title()` normalizes names (`"  Alice "` → `Alice`, `DIANA` → `Diana`); the `.str` accessor vectorizes string methods over a column.
- `pd.to_numeric(..., errors='coerce')` converts `"82"` → `82` and turns the unparseable `"ninety-one"` into `NaN` — visible in the stored after-cleaning table.
- `drop_duplicates(subset=['email'])` removes the duplicate `alice@work.com` row; `dropna(subset=['email'])` drops the row with `None` email.

**Why it matters:** every resume or JD an ATS ingests passes through this sequence — normalize, coerce, dedupe, drop — before any scoring happens.""",
15: r"""`groupby` splits a DataFrame into groups, applies a function per group, and combines the results — split-apply-combine. `agg` lets each column have its own aggregations, which is why the stored output's header is two levels tall.

**What the code does:**
- Synthesizes 100 resumes under `np.random.seed(42)` for reproducibility.
- `groupby('role').agg({...})` computes mean years, mean/min/max skills count, mean score, and the *sum* of `has_portfolio` (a boolean summed = count of True) per role — the stored output shows Analyst at **6.2** mean years and **7.8** mean skills.
- `resumes[resumes['score'] > 80].sort_values('score', ascending=False)` filters and ranks, and the output reports the top-candidate count.

**Why it matters:** role-wise benchmarks ("Analysts average 6.2 years") are the insights section of any ATS dashboard.""",
17: r"""`.apply` runs a Python function over each element (or row/column) — the escape hatch when no vectorized method exists, and where the Ch. 01 composition habits pay off.

**What the code does:**
- `score_category` buckets each score into Strong / Good / Average / Weak; the stored `value_counts()` shows **Strong 30, Good 32, Average 25, Weak 13**.
- A lambda `lambda x: int(x)` truncates `years_exp` to whole years — the head shows `3.0 → 3` and `0.1 → 0` (truncation, not rounding).

**Why it matters:** rule-based ATS scoring (Ch. 50s) is literally a `score_category` applied to extracted features — this is the pattern the scoring engine will use.""",
19: r"""Pandas plotting is a thin wrapper over matplotlib: `DataFrame.plot`-family methods (`.boxplot`, `.hist`) turn columns into figures in one line. Visualization is how score distributions get communicated to non-technical stakeholders.

**What the code does:**
- `resumes.boxplot(column='score', by='role')` draws per-role ATS score distributions; `plt.suptitle('')` suppresses matplotlib's auto-added supertitle.
- `resumes['years_exp'].hist(bins=20)` plots the experience histogram with labeled axes.
- The stored outputs show the two `<Figure size 800x400 with 1 Axes>` objects — the plots render inline above.

**Try it:** change `bins=20` to `bins=5` and rerun — the story (right-skewed experience) stays, but the histogram gets coarser.""",
21: r"""Pearson correlation measures linear association in [-1, 1]: near ±1 means "move together", near 0 means "no linear relationship". A correlation matrix shows every pairwise combination at once.

**What the code does:**
- `resumes[numeric_cols].corr()` returns the 3×3 matrix; `.round(3)` trims it for reading.
- The diagonal is 1.000 by definition — every column correlates perfectly with itself.
- The stored output shows `score` vs `years_exp` at **-0.022** and `score` vs `skills_count` at **-0.084** — indistinguishable from zero.

**Why it matters:** here the near-zero values are by construction — `score` was drawn independently of experience and skills — and that is the lesson: correlation tells you which features carry signal, and these two do not. A real ATS must engineer features (Ch. 13+) that actually correlate with outcomes.""",
23: r"""NumPy and pandas are the substrate for everything that follows: every extraction result in Part I lands in a Series or DataFrame, and every Part II model reads from one. Masks, `groupby`/`agg`, `.apply`, cleaning chains, and correlation are the daily vocabulary of the pipeline.

The next chapter layers the *text* skill on top of this data layer — Ch. 03, Regex Mastery, turns raw resume text into the structured fields you will store in tables like these.""",
}
append02 = [r"""## Key Insight

**Resume analytics is a table problem before it is an ML problem.**

Every ATS decision — filter, rank, score, match — reduces to vectorized operations over rows: masks to filter, `groupby` to benchmark, `.apply` to score, `.corr` to sanity-check features. If you can express the question as a pandas operation, you can ship it; the chapters ahead keep returning to exactly these shapes. Next, the missing input — turning raw text into those structured rows: Ch. 03, Regex Mastery."""]

# ================================================================ CH03
add03 = {
0: r"""This chapter turns raw resume text into structured fields using regular expressions — the fastest, most deterministic, and most explainable extraction tool in the NLP toolbox. You build patterns piece by piece, then assemble them into a complete resume extractor.

**Why it matters for resumes / ATS:** ATS keyword matching, contact parsing, and date normalization are regex problems. Regex is also the tool interviewers expect you to reach for first when asked to parse text — and the `re` skills here are the foundation the statistical chapters (Ch. 04+) build on.""",
1: r"""`re.search` finds the *first* match anywhere in a string and returns a `Match` object; `re.findall` returns every non-overlapping match as a list. The `Match` object carries the matched text (`.group()`) and its position (`.span()`).

**What the code does:**
- Searches the email pattern in a contact line: the stored output shows `john.doe@email.com` at span `(14, 32)` — character offsets into the original string, useful when you need to locate a field in raw text.
- `re.findall` with the same pattern confirms one email on the line.

**Try it:** give the text two emails and rerun — `search` still returns only the first, `findall` returns both. That difference decides which function each extractor uses.""",
3: r"""Inside `r"..."` backslashes are literal, so `r"\d"` is backslash-plus-d — the two characters the regex engine reads as "digit". Without the `r`, Python interprets escapes first: `"\n"` becomes a newline character, and your pattern silently changes meaning.

**What the code does:**
- `repr()` of normal vs raw: `'\n'` (one newline character) vs `'\\n'` (backslash + n) — the stored output shows the pair.
- Metacharacters (`. ^ $ * + ? { } [ ] \ | ( )`) carry special meaning unless escaped; `re.search(r"\(3\.11\)", text)` matches the literal `(3.11)` in "Python (3.11) is [great]".

**Try it:** drop the backslashes (`r"(3.11)"`) and the parentheses become a *capture group* — different result, same characters.""",
5: r"""`[...]` matches exactly one character from the set; `[a-z]` is a range; `[^...]` matches anything *not* in the set. Shorthand classes `\d` (digit), `\w` (word char), `\s` (whitespace) and their uppercase negations (`\D`, `\W`, `\S`) cover the common cases.

**What the code does:**
- `[Pp]ython` on "Python, pytHon, pYTHON" matches only `Python` — the stored output's one-item list shows case-sensitivity in action (`pytHon` fails on the lowercase `t`).
- `[0-9]+` pulls every digit run from "Room 42, Floor 7, Building 101": `['42', '7', '101']`.
- `[\d()]+` on the phone line groups digits and parentheses: `['(555)', '123', '4567']` — the raw material for the phone normalizer in section 7.

**Try it:** extend `[0-9]` to `[0-9a-f]` and it starts matching hex digits — classes are just sets.""",
7: r"""Quantifiers attach to the preceding token: `*` (0 or more), `+` (1 or more), `?` (0 or 1), plus `{n}`, `{n,}`, `{n,m}`. Greedy quantifiers consume as much as possible; a trailing `?` makes them lazy (`.*?` stops at the first opportunity).

**What the code does:**
- On "Python is great!!! Really?? Yes." both `Python.*great` and `Python.*?great` return `'Python is great'` — on this short string greedy and lazy land on the same span; the difference shows when a string has *multiple* "great" occurrences.
- The email pattern `[\w.+-]+@[\w-]+\.[\w.]+` uses `+` per component; the stored output parses all three addresses, including the 17-character domain `long-domain-name.com`.

**Try it:** add a second "great" to the text — greedy spans both, lazy stops at the first. That distinction is the classic regex interview question.""",
9: r"""Parentheses do two jobs: *grouping* (apply a quantifier to a unit) and *capturing* (keep the matched substring for later). Named groups `(?P<name>...)` make captures self-documenting; `(?:...)` groups without capturing.

**What the code does:**
- `Name: (?P<name>[^,]+), Email: (?P<email>[\w.@]+)` captures two named fields; `match.group('name')` / `match.group('email')` return `Srivatsa Gorti` and `srivatsa@email.com` per the stored output.
- `(?:Name|Email): ([^, ]+)` alternates the labels but captures only the value — `findall` returns `['Srivatsa', 'srivatsa@email.com']`.

**Why it matters:** named groups are how production extractors label fields — the output of this cell is already a mini structured record.""",
11: r"""The Ch. 01 email pattern was a teaching tool; this one is production-grade: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`. The `{2,}` on the top-level domain rejects one-letter TLDs like `x@y.z` — which the looser section-4 pattern happily matched.

**What the code does:**
- Runs against a multi-line contact block and finds three real addresses; the multi-part TLD in `john.doe@company.co.uk` is matched whole.
- `list(set(emails))` deduplicates — the stored `Unique:` line shows the same three in different order, because set ordering is arbitrary.

**Try it:** swap this pattern for the section-1 pattern and feed it `x@y.z` — the `{2,}` TLD requirement is the difference between "works" and "production".""",
13: r"""Phone formats are chaos: `+1 (555) 123-4567`, `555-123-4567`, `+91 98765 43210`, `1.800.555.1234`. The tolerant pattern `[+]?[\d\s()-]{7,}[\d]` accepts digits, spaces, parentheses, and hyphens — at least 7 of them, then one final digit. Normalization then strips everything except digits and a leading `+`.

**What the code does:**
- Extracts three of the four lines — **`1.800.555.1234` is skipped** because `.` is not in the pattern's character class. A deliberate limitation worth remembering.
- `normalize_phone` applies `re.sub(r'[^\d+]', '', phone)` — keep digits and `+`, drop the rest; the stored output shows the normalized digit strings.

**Why it matters:** contact fields must be normalized before matching — the same phone formatted four ways is one phone, and ATS comparison needs them comparable.""",
15: r"""`https?://` matches both `http://` and `https://`; `[\w./-]+` then consumes the rest of the URL. Links are high-value resume signals — LinkedIn, GitHub, portfolio — and easy to categorize by substring.

**What the code does:**
- Finds three URLs from the block — **`www.buildsrivatsa.qzz.io` is missed** because it has no scheme; a `www\.` alternative in the pattern would catch it.
- Categorization is a plain `if "linkedin" in url.lower()` chain; the stored output labels the LinkedIn and GitHub links and leaves the portfolio uncategorized.

**Try it:** extend the pattern with `|www\.` and the fourth link appears — small pattern changes, big recall differences.""",
17: r"""Employment history is the heart of a resume, and date ranges are its structure. The pattern `([A-Z][a-z]+\s+\d{4})\s*-\s*([A-Z][a-z]+\s+\d{4}|Present)` captures start and end as two groups; the `|Present` alternative handles current roles.

**What the code does:**
- Month-year spans: `Jan 2020 → Present` and `June 2017 → August 2017` from the stored output.
- The looser year-only pattern `(\d{4})\s*-\s*(\d{4}|Present)` catches the bare-year lines: `2020 → Present`, `2018 → 2020`, `2016 → 2020` — the last from the education line.

**Why it matters:** tenure calculation (years per role) starts from these two capture groups — the raw material for experience scoring later in the project.""",
19: r"""Skill extraction is dictionary matching done right: for each known skill, build `\b` + `re.escape(skill)` + `\b` and search with `re.IGNORECASE`. The `\b` word boundary stops `Python` from matching inside `Pythonic`; `re.escape` neutralizes regex metacharacters in skill names like `C++`.

**What the code does:**
- Scans a summary plus technical-skills block against 29 known skills and returns 12 sorted matches — the stored output lists them (`AWS`, `Deep Learning`, `TensorFlow`, ...).
- Case-folding via `re.IGNORECASE` lets one pattern cover `Python`, `python`, `PYTHON`.

**Why it matters:** this is the exact mechanism behind resume–JD keyword matching — a skill found in both documents is a match, and `\b` is what keeps the match honest.""",
21: r"""Degree extraction is harder than it looks: abbreviations vary (`B.Tech`, `BE`, `M.S.`, `PhD`), and a naive alternation matches *anywhere* — including inside unrelated words.

**What the code does:**
- `(B\.?Tech|M\.?S\.?|PhD|B\.?E\.?|M\.?Tech|MBA|B\.?Sc|M\.?Com)[^,]*` with `re.IGNORECASE` finds `B.Tech`, `M.S.`, `PhD` — and the stored output shows the failure mode: **`mba` appears twice**, matched inside *Mumbai* and *Bombay*.
- The institution pattern `(?:from|at)\s+([A-Z][A-Za-z\s.]+?)` finds **nothing** — the sample says "B.Tech *in* Computer Science, IIT Bombay", i.e. `in`, not `at`/`from`. Patterns are literal; the surface form must match.

**Why it matters:** two real lessons in one cell — anchor patterns to context (line start, degree keywords), and test against the actual text formats your data uses.""",
23: r"""Location lines are usually structured enough for a city/state pattern: capitalized words, a comma, then either a 2-letter state code (`CA`) or another capitalized name (`India`).

**What the code does:**
- `([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2}|[A-Z][a-z]+)` handles multi-word cities via the inner `(?:\s+...)*` group.
- The stored output extracts `San Francisco, CA` and `Mumbai, India` — and skips `US ***` (work authorization) and `Yes` (relocation), since neither is a capitalized phrase before a comma.

**Why it matters:** location feeds relocation-eligibility and geographic matching in the ATS — cheap signal, easy to extract.""",
25: r"""This is the chapter's deliverable: `ExtractedResume`, a dataclass holding every field, and `extract_all()`, which runs all the section patterns over one text in a single pass. It is the direct ancestor of the Part II extraction pipeline.

**What the code does:**
- Name via the first-line heuristic; emails/phones/URLs via `list(set(re.findall(...)))` (dedupe included); skills via the `\b` + `re.escape` loop; degrees and locations via the section patterns.
- The stored output parses the sample completely: **Srivatsa Gorti**, one email, one phone, one LinkedIn URL, five skills.
- Education shows the section-11 leak again: `['B.Tech', 'mba', 'mba']` — `mba` from *Mumbai* and *Bombay*, duplicates included because this loop does not dedupe.

**Try it:** keep this extractor as your baseline — later chapters replace its heuristics (name, degrees) with statistical models, and this is what you diff against.""",
27: r"""**How to use this sheet:** every pattern in this book is a combination of these pieces — class + quantifier + anchor + group — so this table is the reference for all of Part I. The summary below is the chapter's contract: regex is fast, deterministic, and explainable, which is why it stays the primary text tool for Parts I and II.""",
28: r"""## Debugging Regex Like a Pro

Regex bugs are silent: a pattern that *almost* matches returns nothing, not an error. A short discipline fixes most of them.

- **Start minimal, grow slowly** — build `\d{4}` before `(\d{4})\s*-\s*(\d{4}|Present)`; each added piece is a testable hypothesis.
- **Test against the real text** — the section-11 institution pattern failed because the sample said `in`, not `at`; patterns are literal, so sample data must be representative.
- **Anchor unanchored alternations** — `(B\.?Tech|MBA|...)` matched *Mumbai*; use `^`, `\b`, or surrounding context when match location matters.
- **Prefer named groups and `re.VERBOSE`** for multi-part patterns — `(?P<field>...)` turns a match into a labeled record.
- **Escape user content** — `re.escape(skill)` before embedding a skill name in a pattern.

The section-11 and section-13 stored outputs above are worked examples of every rule in this list.""",
29: r"""## Limits of Regex

Regex is literal and context-free: it matches *characters*, not *meaning*. It cannot tell `mba` inside *Mumbai* from an MBA degree, cannot know that "develop" and "development" share a root, and cannot handle paraphrase.

Every failure in this chapter is a regex limit: degree false positives inside city names, the missed `www.` URL, the institution pattern beaten by `in` instead of `at`, phone formats with dots. Each is a *surface-form* problem — same information, different string.

**Why it matters:** this is exactly why the next chapters exist — normalization (Ch. 06), lemmatization (Ch. 08), and statistical parsing (Ch. 10–12) handle the variation regex cannot. Regex owns the structured fields; NLP takes the ambiguous ones.""",
30: r"""## Key Insight

**Regex is the fastest path from raw text to structured fields — and its limits define the NLP pipeline that follows.**

The extractor you built here — contact, URLs, dates, skills, degrees, locations — is a complete, explainable ATS field-extraction layer in a few dozen lines. Its failures are not bugs but boundaries: where surface forms vary, statistical NLP takes over. The patterns and the discipline (anchoring, escaping, testing on real text) carry into every later chapter.

Next, Ch. 04 — NLP Introduction — frames where regex ends and language models begin.""",
}

# ================================================================ run
results = {}
results["ch00"] = extend(CH00, add00, append=append00)
results["ch01"] = extend(CH01, add01, append=append01)
results["ch02"] = extend(CH02, add02, append=append02)
results["ch03"] = extend(CH03, add03)  # no append — cell 30 is the Key Insight
print(json.dumps(results, indent=1))
