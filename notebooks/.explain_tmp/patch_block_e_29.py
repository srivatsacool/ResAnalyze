from nbtools import apply

apply(r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_e\29_text_normalization_for_resumes\29.ipynb", replace={
3: r"""## 2. Resume Normalizer

`ResumeNormalizer` chains five transforms in a fixed order. The first step is the subtle one: `unicodedata.normalize("NFKD", ...)` followed by an ASCII `encode(..., "ignore")` — this decomposes accented characters and drops everything that still is not ASCII. It strips diacritics (`résumé` → `resume`) and smart punctuation, but it is lossy for genuinely non-Latin text.

**What the code does, step by step:**
- NFKD normalize + ASCII-ignore encode — removes accents and non-ASCII glyphs
- Bullet regex — maps `• ‣ ● ◘ ◙ ➜` to `>`; but the order defeats it: bullets are *already gone* by this step (dropped by the ASCII pass), so the substitution is dead code as written
- `\t|\r` → space; `\n{3,}` → `\n\n`; ` {2,}` → ` `; final `strip()`

**Expected (verified):** the cell as stored has a syntax error — the last line `print(f"After:  {repr(n.normalize(sample))}` is missing its closing `")`, so running it as-is raises `SyntaxError: unterminated f-string literal`. With that typo fixed, `Before:` shows the raw sample with `•` bullets and a tab, and `After:` is `'Srivatsa Gorti\n Python specialist\n NLP engineer\n TensorFlow expert'` — bullets silently removed (leaving a stray space where each was), tab collapsed to a space, double spaces gone. Lesson: transform order is part of the design — the ASCII pass must come *after* any mapping you want to survive it, and an unterminated string at the end of a pipeline cell is exactly the failure that makes a notebook look fine until someone runs it.""",
5: r"""## 3. Abbreviation Expansion

Abbreviations are a vocabulary problem: `Sr.`, `Engr.`, `w/`, `yrs` all need expanding to canonical forms so keyword matching and later stages see one spelling. This cell builds a dictionary-driven expander with a single case-insensitive regex pass over boundary-delimited alternatives.

**What the code does:**
- Compiles the pattern from the map keys using `re.escape` and `re.IGNORECASE`
- Substitutes via a lambda that looks up the lowercased match in `abbrev_map`

**Expected (verified):** both test lines come back **unchanged**. The stored pattern is `r"\\b(sr\.|...|yrs|yr)\\b"` — note the doubled backslash. In a raw string, `\b` is the word-boundary assertion, but `\\b` compiles to a regex that matches a *literal* backslash followed by `b`; no resume text contains that, so no substitution ever fires and the expander silently does nothing. (Even with the intended single `\b`, only word-final keys such as `yrs` would match — abbreviations ending in `.` or `/`, and `&`, can never satisfy the trailing boundary, since `\b` needs a word character after the punctuation.) Lesson: raw strings make backslashes literal, so `r"\\b"` is not a boundary — an escape-doubling pitfall that also shows why you test the exact stored code, not the intended code."""
})

print("patched 29.ipynb md cells 3 and 5")
