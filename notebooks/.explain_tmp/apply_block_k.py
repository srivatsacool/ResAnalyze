# -*- coding: utf-8 -*-
"""Expand markdown cells of block_k notebooks (ch64-69) following ch11 exemplar style.
Code cells are never touched (apply asserts markdown type). No appends needed —
every notebook already ends with a Summary markdown cell (kept verbatim, expanded below)."""
from nbtools import apply

K = r"D:\Projects\ResAnalyze\notebooks\part3_production\block_k"

# ============================ 64 ============================
n64 = K + r"\64_precision_and_recall_for_nlp\64.ipynb"
R64 = {
0: r"""# 64 — Precision & Recall for NLP
**Goal:** Measure entity extraction accuracy with precision, recall, and F1.

A skill extractor that "finds skills" is useless until you measure how often it is right. This chapter introduces the three canonical extraction metrics — **precision**, **recall**, and **F1** — and applies them to the resume-skill use case, first as aggregate scores, then broken down per skill category.

**Why it matters for resumes / ATS:** an ATS acts on extracted skills (filtering, matching, ranking), so every extraction error has a real cost. A **false positive** invents a skill the candidate never claimed — a hallucinated "Docker" can surface a candidate who cannot back it up. A **false negative** drops a real skill ("Java") and silently hides an otherwise strong match. Choosing whether to prioritize precision or recall is a product decision: conservative screening prefers high precision, broad matching prefers high recall, and F1 gives you one number to optimize when both matter.""",
1: r"""## 1. Why Metrics Matter

A naive "how many skills did we find" count conflates two very different failure modes: finding *wrong* things and missing *right* ones. **Precision** answers "of everything we extracted, how much was correct?" while **recall** answers "of everything that was actually there, how much did we find?" **F1** is their harmonic mean — it stays low if *either* is low, so it punishes systems that cheat by extracting everything (max recall, terrible precision) or nothing (perfect precision, zero recall).

**What the code does:** the first cell prints the worked example used throughout the chapter — a resume with `[Python, Java, TensorFlow]`, a system that returns `[Python, TensorFlow, Docker]`, and the arithmetic: 2 of 3 returned skills are correct (precision 0.67) and 2 of 3 real skills are found (recall 0.67). The `Docker` mention is the false positive; the missed `Java` is the false negative.

**Try it:** change the example — a system that returns only `[Python]` has precision 1.0 but recall 0.33: perfect precision is easy, and useless alone.""",
3: r"""## 2. Computing Metrics

`compute_metrics()` is the reusable core of the chapter. It converts both lists to sets, then counts the three confusion cells with pure set algebra: `tp` = intersection, `fp` = predicted-minus-gold, `fn` = gold-minus-predicted. The guard clauses (`if (tp + fp) > 0`, etc.) matter — precision and recall are undefined when there is nothing to divide, and a division by zero would crash a batch run on exactly the edge cases you most want to measure.

**What the code does:** the test loop runs five deliberately chosen cases — empty/empty, perfect match, a partial miss, a resume with no prediction, and an empty gold set with a spurious prediction. Running it reports: perfect → P=1.00 R=1.00 F1=1.00; partial (`gold [Python, Java, SQL]` vs `[Python, TensorFlow]`) → P=0.50, R=0.33, F1=0.40 — note F1 sits *below* both, the harmonic-mean penalty; the empty and one-sided cases all floor at 0.00, a correct non-crashing answer for degenerate input.

**Try it:** the "hallucination" case (empty gold, one prediction) is exactly the failure mode of an LLM that invents skills for a resume that lists none.""",
5: r"""## 3. Per-Category Breakdown

Aggregate F1 hides structure: a system can score perfectly on programming languages while missing every cloud skill, and the single headline number will not tell you. Breaking metrics down per category turns evaluation from a score into a diagnosis — it shows *where* the pipeline degrades, which is what you actually fix.

**What the code does:** each gold item is bucketed via `categories.get(item, "other")`, so `Docker` and `SQL` — absent from the category map — land in `other`. The gold loop counts tp/fn per bucket; the predicted loop counts fp. Running it reports: programming P=1.00 R=0.50 F1=0.67 (`Java` was missed), nlp and ml at 1.00, cloud at 0.00 (`AWS` missed), and `other` at 0.00 — both false positives (`Docker`, `SQL`) park in `other` because they were never part of the taxonomy.

**Try it:** treat the `other` bucket as a warning light — every fp parked there means the extractor is finding skills the evaluation schema does not even model.""",
7: r"""## Summary: Precision, recall, F1 are the standard NLP evaluation metrics. Track per-category for insights.

**Precision and recall are two views of the same error, and F1 forces you to balance them.**

A production resume parser needs both numbers because each hides what the other shows: high precision alone can be achieved by extracting nothing, high recall alone by extracting everything. The set-based `compute_metrics()` — tp/fp/fn from set operations — is the smallest implementation that gets the edge cases right, and the per-category breakdown is what turns a score into an action plan. With this machinery in hand, the next chapter generalizes from one-vs-rest skill matching to the full **confusion matrix** for multi-class section classification, where these same tp/fp/fn counts are laid out as a grid.""",
}

# ============================ 65 ============================
n65 = K + r"\65_f1_score_and_confusion_matrix\65.ipynb"
R65 = {
0: r"""# 65 — F1 & Confusion Matrix
**Goal:** Multi-class evaluation with confusion matrices.

Chapter 64 measured extraction against a single set of gold entities. Real resume pipelines also *classify* — assigning each bullet or section a label (skill, experience, education, summary). This chapter generalizes precision/recall/F1 to the multi-class setting and introduces the **confusion matrix**, the canonical grid that shows not just *how many* errors occur, but *which pairs of classes* get confused.

**Why it matters for resumes / ATS:** section and entity classification is the backbone of structured profile building — an ATS must know which text is a skill and which is a work experience before it can match anything. The confusion matrix reveals the *direction* of errors: "experience classified as skill" and "skill classified as experience" are the classic swaps, and a matrix exposes them at a glance. When classes are imbalanced — most resumes contain far more skill mentions than summary blocks — the averaging scheme you pick for F1 changes what your headline number actually means.""",
1: r"""## 1. Confusion Matrix Basics

A **confusion matrix** is a grid where rows are true labels, columns are predicted labels, and the diagonal holds the correct classifications. Every off-diagonal cell names a specific error pair — read a row to see what a class *was mistaken for*, read a column to see what *got mislabeled as* it. For binary problems it degenerates to the four counts tp/fp/fn/tn; for multi-class problems it is the only compact way to see the full error structure at once.

**What the code does:** it builds gold and predicted label lists for a 10-bullet resume (4 skill, 3 experience, 2 education, 1 summary) and calls `confusion_matrix(..., labels=classes)` with an explicit label order, then prints the grid by hand without matplotlib. Running it gives `[[3,1,0,0],[1,2,0,0],[0,0,2,0],[0,0,0,1]]`: 8 of 10 bullets on the diagonal (80% accuracy), and both errors are skill/experience swaps — one true-skill bullet labeled experience, one true-experience bullet labeled skill.

**Try it:** the `labels=` argument matters — without it sklearn infers an arbitrary order from the data, and a matrix whose axes are sorted differently is unreadable.""",
3: r"""## 2. Classification Report

The matrix shows *where* errors land; the **classification report** turns each row into the per-class precision, recall, and F1 from Chapter 64, plus `support` — the number of true instances of each class. Per-class numbers are the honest view: the overall accuracy of 0.80 is dragged down entirely by the two skill/experience confusions, and the per-class F1 tells you which class suffers most and from what.

**What the code does:** one `classification_report()` call over the same labels. The run reports: skill P/R/F1 = 0.75 on support 4 (three gold bullets kept, one lost to the swap), experience 0.67 on support 3 (two of three), education 1.00 on support 2, summary 1.00 on support 1. The macro average (0.85) exceeds the weighted average (0.80) precisely because the small, easy classes — education and summary — get equal votes under macro but barely move weighted.

**Try it:** compare the report to the matrix cell-by-cell — each off-diagonal cell must show up as a precision loss in its column's class and a recall loss in its row's class.""",
5: r"""## 3. Macro vs Micro vs Weighted F1

With several classes you must decide how to combine their F1 scores, and the choice is not cosmetic:

| Average | How it is computed | Bias |
|---|---|---|
| `macro` | mean of per-class F1, each class equal weight | rare classes count as much as common ones |
| `micro` | global tp/fp/fn pooled across all classes | dominated by the most common class |
| `weighted` | per-class F1 weighted by support | reflects the real data distribution |

**What the code does:** `f1_score(y_true, y_pred, average=...)` on a 10-sample numeric dataset returns macro 0.802, micro 0.800, weighted 0.797. They differ only in the third decimal because the classes are near-balanced; on a real resume corpus, where "skill" massively outnumbers "summary", the gap widens. The notebook's guidance is the right default: **use weighted F1** so the headline reflects the distribution you actually serve.

**Try it:** flip two labels between the minority and majority classes and watch macro move far more than micro — that is the "rare class gets a vote" effect.""",
7: r"""## Summary: Confusion matrices show WHERE errors happen. Use weighted F1 for imbalanced resume data.

**The matrix names your errors; the averaging scheme decides what your score means.**

Two bullets mislabeled in a skill/experience swap is not noise — it is a systematic signature of a classifier that cannot reliably separate adjacent section types, and the matrix surfaces it in two cells instead of burying it in an accuracy number. Per-class reports localize the damage, and weighted F1 keeps the headline honest on skewed corpora. The next chapter shifts from measuring *wrong answers* to measuring *made-up answers*: hallucination testing, where the failure is not classification error but output that is not grounded in the resume at all.""",
}

# ============================ 66 ============================
n66 = K + r"\66_hallucination_testing\66.ipynb"
R66 = {
0: r"""# 66 — Hallucination Testing
**Goal:** Detect and quantify LLM hallucinations in resume output.

Chapters 64–65 measured errors of *selection*: extracting or classifying the wrong thing. LLMs introduce a worse failure mode — errors of *invention*, where the model emits plausible content that is not in the source resume at all. This chapter defines the hallucination taxonomy for resume tasks and implements two automated detectors: a **grounding check** (is the output supported by the source text?) and a **consistency check** (are facts stable across rephrasings?).

**Why it matters for resumes / ATS:** a resume an LLM "improves" by inventing TensorFlow experience, a 5-year tenure, or a 40% metric is not just wrong — it misrepresents the candidate to employers and is a legal and reputational liability for any service that produces it. Automated hallucination checks are the guardrail that lets you keep the LLM rewrite while discarding the fabrication. In a pipeline that feeds extracted facts into matching or screening, an ungrounded fact is worse than a missed one: it actively lies about the candidate.""",
1: r"""## 1. Types of Hallucination

Hallucinations are not one phenomenon — they come in distinct flavors with distinct costs. The code lists the four that matter for resumes: **skill hallucination** (claiming a skill absent from the resume), **experience hallucination** (inventing job details or titles), **date hallucination** (wrong or fabricated tenure), and **metric hallucination** (fabricated numbers such as "40% improvement"). The last two are the most dangerous because a reader cannot spot them by eye.

**What the code does:** prints the taxonomy alongside three detection strategies. A **grounding check** asks whether output content exists in the source text; a **consistency check** re-runs the task on paraphrases and compares facts across calls; a **factual check** validates against external knowledge (company locations, standard job titles). The three form a ladder: grounding is cheap and local, consistency catches stable-but-wrong inventions, and factual checks catch errors neither can see.

**Try it:** classify a few LLM outputs into the four types before running the detectors — the type shapes which detector can catch it.""",
3: r"""## 2. Grounding Checker

The grounding check implements the simplest faithful test: extract candidate claims from the model output and verify each appears verbatim in the source text. This version extracts claims with a regex for capitalized phrases (proper nouns and title-case spans), lowercases both sides for a case-insensitive match, and reports `grounded_pct` — the share of detected claims supported by the source. 100% means every claim the extractor found is backed by the resume.

**What the code does:** given the source "Python developer with NLP experience at Google" and an output that adds "TensorFlow" and "(5 years)", the regex `\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b` finds only `Python` and `Google` — both grounded, so it reports 100%. The catch is instructive: `TensorFlow` (mixed-case) and `NLP` (all-caps acronym) never match the `[A-Z][a-z]+` pattern, so the fabricated skill and the fabricated tenure are *invisible to the claim extractor*. A grounding check is only as strong as its claim splitter.

**Try it:** extend the pattern (e.g. allow interior capitals or acronym runs) and `TensorFlow` reappears — now flagged as ungrounded. The detector's blind spots are part of the result.""",
5: r"""## 3. Consistency Testing

A model that hallucinates the *same* way every time can defeat keyword-overlap grounding checks. Consistency testing exploits a different property of invention: it is unstable under paraphrase. Run the task several times with rephrased inputs; if the extracted facts stay identical across runs they are more likely true, and if facts appear, vanish, or change, that variation is the fingerprint of hallucination.

**What the code does:** extracts the skill set from the original text with a skill-vocabulary regex, then compares each paraphrase's skill set for equality. On the given example it reports consistency 67% (2 of 3): the first two variants preserve `{python, nlp, tensorflow}`, while the third — "Java developer with Spring Boot" — swaps in `{java}`. One inconsistent run in three is a loud signal that the model does not reliably preserve the resume's skill facts under reformulation.

**Try it:** note the equality test is strict — casing and order are normalized, but any added or dropped skill fails. For skills, "close" is not good enough.""",
7: r"""## Summary: Hallucination testing catches LLM fabrications. Always ground-check outputs against source text.

**Faithfulness is a measurable property — measure it, or ship fabrication.**

Grounding and consistency checks are the two cheapest automated guards in the hallucination toolbox: one verifies output against the source, the other verifies stability across paraphrases, and each catches failure modes the other cannot see. The worked examples also expose the tooling's blind spots — regex claim extraction misses mixed-case and acronym tokens — so treat these scores as lower bounds on suspicion, not certificates of truth. These detectors are the evaluation counterpart to the LLM rewriting steps of earlier blocks: they let you keep the rewrite while discarding the invention. The next chapter turns to optimizing prompts themselves, with A/B testing against a golden set.""",
}

# ============================ 67 ============================
n67 = K + r"\67_a-b_prompt_testing\67.ipynb"
R67 = {
0: r"""# 67 — A/B Prompt Testing
**Goal:** Quantitatively compare prompt variants on a golden test set.

Prompt engineering without measurement is just editing. This chapter builds a small **A/B testing framework**: a fixed **golden set** of (input, expected-output) pairs, a harness that runs any prompt variant over that set, and a score that says which variant is better. It then adds the statistical machinery needed to decide whether an observed score difference is real or just noise.

**Why it matters for resumes / ATS:** the wording of a rewriting or extraction prompt is a product decision — "Developed" vs "Created" changes how a candidate is presented to employers. A/B testing makes that decision evidence-based: instead of arguing about prompt style, you run both variants on a golden set of representative resume bullets and let the scores decide. The golden set also becomes a regression net: any future prompt edit that drops its score is caught immediately — the evaluation equivalent of a unit test.""",
1: r"""## 1. A/B Testing Framework

The `PromptABTest` class is the whole loop in 20 lines: hold a golden set of `(input, expected_output)` pairs, run a prompt variant over every pair, and mark each output `exact` only if it matches the expected string byte-for-byte after stripping. Accuracy is the fraction of exact matches. The design deliberately separates the *prompt template* from the *model function* (`llm_fn`), so the same harness measures a template change, a model change, or a system-prompt change without touching the golden set.

**What the code does:** the golden set holds three weak bullets ("Responsible for ML models") paired with strong impact-phrased rewrites ("Developed ML models achieving 95% accuracy"). Variant A swaps in aggressive verbs (`Developed`, `Built`, `Led`); variant B uses conservative ones (`Created`, `Designed`, `Managed`). Running the harness reports **0% accuracy for both variants**: neither produces the expected strings, because the gold rewrites add impact phrases ("achieving 95% accuracy") that simple verb substitution cannot generate. The framework is working as intended — exact match is brutally strict, and the result forces you to align the metric with the task's real success criterion.

**Try it:** relax the comparison to "expected verb appears in the output" and both variants jump — the metric should encode what you actually care about.""",
3: r"""## 2. Statistical Significance

One run per variant proves nothing: LLM outputs are stochastic, so a single golden-set score is a sample, not a measurement. The standard fix is to repeat the evaluation several times and ask whether the two score distributions differ more than chance would predict. The **independent two-sample t-test** compares the means while accounting for variance; the **p-value** is the probability of seeing a difference this large if the variants were actually identical.

**What the code does:** ten score observations per variant — A clustered near 0.859, B near 0.823. The test returns a t-statistic of 7.453 and p ≈ 0.0000 (below 0.0001), so the branch prints "Statistically significant (p<0.05)". With tightly clustered scores the conclusion is robust: A is genuinely better, not lucky. The lesson applies in reverse too — with noisy real-world evaluations and n=10, many observed gaps will *not* be significant, and the honest answer is "keep collecting data".

**Try it:** nudge two of B's scores up to 0.86 and the p-value jumps — small samples turn real differences into coin flips.""",
5: r"""## Summary: A/B test prompts against golden datasets. Use statistical tests to confirm significance.

**Prompt changes should be adopted on evidence, not vibes — and evidence means repeated runs, not one score.**

The golden set turns prompt engineering into a measurable loop, and the framework's strict exact-match scoring shows why the metric must be designed together with the task: the right test for a rewriting prompt is not byte equality but "did the rewrite do the job." Statistical testing separates real gains from sampling noise, and the same golden set doubles as a regression net for future prompt edits. What this chapter cannot score is *quality* — whether "Developed ML models achieving 95% accuracy" is a true, defensible claim. That judgment requires humans, and it is the subject of the next chapter: human evaluation protocols.""",
}

# ============================ 68 ============================
n68 = K + r"\68_human_evaluation_protocol\68.ipynb"
R68 = {
0: r"""# 68 — Human Evaluation Protocol
**Goal:** Design annotation guidelines and measure inter-annotator agreement.

Automated metrics measure how well a system matches a reference — but the reference itself must come from somewhere. This chapter covers the **gold standard** of NLP evaluation: humans. It lays out an annotation protocol for resume data (schema, guidelines, training, quality control) and introduces **inter-annotator agreement** — the statistical tool that tells you whether your human labels are trustworthy enough to serve as a gold set at all.

**Why it matters for resumes / ATS:** every metric in Chapters 64–67 is only as good as the labels it is computed against. If two human annotators cannot agree on where a skill mention starts or whether a bullet is STAR-compliant, then no automated score built on those labels means anything. A measurable agreement target (typically Cohen's kappa ≥ 0.8 on the training batch) is the quality gate that makes the whole evaluation stack — golden sets, A/B tests, hallucination checks — trustworthy.""",
1: r"""## 1. Annotation Guidelines

Human evaluation fails silently without a written protocol. The code prints the four-part structure: (1) an **annotation schema** defining exactly what gets labeled — skill entities, section boundaries, and STAR-compliant bullet quality on a 1–5 scale; (2) a **guidelines document** with examples, edge cases, and rules for ambiguous cases; (3) **annotator training**, including jointly labeling 10 samples and discussing disagreements until agreement exceeds 0.8; and (4) ongoing **quality control** with 10% overlap between annotators, weekly calibration, and per-annotator drift tracking.

**What the code does:** prints the protocol as reference material for the chapter. The key idea: schema and guidelines come *first*, because ambiguous labels ("is '5 years' part of the skill mention?") are the main source of disagreement — and disagreement is measurable, so guidelines can be iterated until it shrinks.

**Try it:** write your own edge-case rule for "Python (pandas)" — is the parenthetical a separate skill? Whatever you decide, the guidelines must say so, or your annotators will each decide differently.""",
3: r"""## 2. Inter-Annotator Agreement

If two annotators label the same items, their agreement measures label quality. **Simple agreement** (fraction of identical labels) is intuitive but misleading: two annotators who both just guess the most common label will agree by chance. **Cohen's kappa** corrects for that, computing agreement *beyond chance*: `(observed - expected_chance) / (1 - expected_chance)`. The code applies the standard scale — ≥0.8 almost perfect, ≥0.6 substantial, ≥0.4 moderate (needs calibration), below that poor (revisit the guidelines).

**What the code does:** two annotators rate 10 bullets on the 0–5 quality scale. The run reports simple agreement 60% but kappa 0.444 — the gap is the chance correction at work: both annotators lean on the same common ratings, so about 28% agreement is expected by chance alone. Kappa lands in the "moderate — needs calibration" band: the labels are usable but not yet trustworthy enough to build a golden set on.

**Try it:** make the annotators disagree on exactly two more items and watch kappa collapse toward 0 — near-chance agreement is a red flag that the rubric is ambiguous.""",
5: r"""## 3. Annotation Workflow

Agreement measured on 10 items is a warm-up; production annotation needs an end-to-end workflow. The code prints a five-phase plan for a 200-resume annotation project: **PREP** (schema, guidelines, tooling such as Doccano, Label Studio, or Prodigy), **TRAIN** (20 shared samples annotated together, then 20 annotated separately and measured — iterate the guidelines until kappa > 0.8 *before* scaling up), **ANNOTATE** (split the remaining 160 samples, keep a 10% overlap for ongoing quality control, check agreement weekly), **ANALYZE** (compile the golden dataset, compute per-category metrics, identify systematic errors), and **ITERATE** (fix systematic issues, retrain annotators, expand the dataset).

**What the code does:** prints the plan, but the structure is the teaching: training and analysis bookend the annotation itself, and the 10% overlap is a continuous quality sensor, not an afterthought. The golden dataset this workflow produces is exactly what Chapter 67's A/B harness and Chapter 64's metrics consume.

**Try it:** note how the numbers scale — 20 + 20 training, 160 production, 10% overlap is the smallest project that still measures annotator drift.""",
7: r"""## Summary: Human evaluation is the gold standard. Cohen's Kappa measures agreement beyond chance.

**Labels are only as trustworthy as the humans who made them — measure that trust before building on it.**

Simple agreement flatters; kappa, by correcting for chance, exposes whether annotators are genuinely following the same rubric. The 60%-vs-0.444 gap in this chapter's example is the entire lesson: raw agreement can look acceptable while the labels remain too noisy for a golden set. A protocol with schema, guidelines, training, and overlap QC turns individual judgments into a reusable evaluation resource — the gold sets that every earlier metric and the A/B harness depend on. The final chapter of this block zooms out from accuracy to production health: latency profiling, because a perfect evaluator is worthless if the pipeline it guards is too slow to serve.""",
}

# ============================ 69 ============================
n69 = K + r"\69_latency_profiling\69.ipynb"
R69 = {
0: r"""# 69 — Latency Profiling
**Goal:** Profile pipeline latency — find bottlenecks in parsing, embedding, and LLM calls.

Accuracy is only half of production readiness: a resume pipeline that scores 99% F1 but takes 30 seconds per document is a demo, not a product. This chapter closes the Evaluation block with **latency profiling** — measuring where time actually goes across parsing, section detection, extraction, embedding, search, and LLM calls — then shows two profiling techniques and a bottleneck-by-bottleneck optimization playbook.

**Why it matters for resumes / ATS:** batch resume processing has real throughput requirements (thousands of documents, cost per call), and interactive products have real response-time budgets (a candidate or recruiter waiting on a rewrite). Profiling replaces guesswork: the data decides whether you spend engineering effort on caching embeddings or on swapping the PDF parser. It also quantifies the price of the LLM step earlier chapters added — the rewrite that improves quality has a latency cost, and you should know it.""",
1: r"""## 1. Why Latency Matters

Latency is not one number — it is a budget across pipeline stages, and the budget is dominated by a few expensive stages. The code prints an illustrative per-stage budget: PDF parsing ~200ms, OCR ~2–5s when needed, section detection ~10ms, regex skill extraction ~5ms, normalization ~50ms, embedding ~100ms, LLM rewriting ~1–3s, and FAISS search ~10ms at 1M vectors. The totals tell the product story: roughly 300ms without an LLM step, 2–4s with one.

**What the code does:** prints the budget table and flags the three bottlenecks — OCR, LLM calls, and embedding generation. Read the numbers by *order of magnitude*: OCR and LLM calls live in seconds, everything else in milliseconds. That single observation dictates the entire optimization strategy of this chapter: optimize the seconds first.

**Try it:** sanity-check your own pipeline against this budget — if your section detection or regex extraction shows up in the seconds range, something is structurally wrong, not merely slow.""",
3: r"""## 2. Simple Profiling

The first profiling tool is `time.time()` around each stage — coarse, but it answers the only question that matters: which stage owns the runtime? The code wraps four stages in timers: normalization, simulated section detection (a 5ms sleep), regex skill extraction, and a simulated 50ms embedding step, then prints each stage's time and share of the total.

**What the code does:** running it yields roughly 60ms total, with the simulated embedding at ~51ms — about 85% of runtime — and section detection ~9ms; normalization and skill extraction are below timer resolution. One real finding worth noting: the printed percentages come out inflated (embedding shows as thousands of percent) because the cell computes `pct = t / total * 100` and then formats with `:.0%`, which scales by 100 a second time. The relative ordering is still the lesson — embedding dominates, everything else is noise.

**Try it:** delete the two `time.sleep()` calls and rerun — the remaining stages are so fast that timer noise dominates, which is exactly when you need the function-level profiler in the next section.""",
5: r"""## 3. Profiling with cProfile

Wall-clock timing around stages tells you *which stage* is slow; `cProfile` tells you *which function* inside it is slow. It records every function call with its cumulative time, and `pstats` formats the result sorted by `cumtime` — total time spent in a function including everything it calls. That sort order is the right default: it surfaces the true cost of a call chain, not just a leaf function's own time.

**What the code does:** profiles `slow_function()` — 1000 iterations of `sum(range(i * 100))`. The profile reports roughly 2000 function calls dominated by the built-in `sum` and `range` invocations inside the loop (the observed runtime here was ~1.65s on the venv machine; the number varies by hardware, the structure does not). The takeaway: even trivial pure-Python work shows up clearly in cProfile, so there is no excuse for guessing where time goes in a real pipeline.

**Try it:** point the same `cProfile.Profile()` pattern at `profile_pipeline()` from the previous section — the simulated sleeps now appear as real wall time attributed to their call sites.""",
7: r"""## 4. Optimizing Bottlenecks

Optimization rule: profile first, then fix the biggest bottleneck, then profile again — never optimize blind. The code prints the playbook for the three expensive stages identified in Section 1. For **PDF parsing**: cache parsed text keyed by file hash, prefer PyMuPDF over pdfplumber, and parse multiple documents in parallel. For **embedding**: precompute and cache all resume embeddings, swap to a smaller model (MiniLM instead of MPNet) when quality allows, and batch encode with `model.encode(list_of_texts)` instead of looping single calls. For **LLM calls**: stream for real-time apps, cap `max_tokens` low for extraction tasks, cache common queries, and route simple tasks to cheaper models.

**What the code does:** prints the three strategies. Two patterns recur across every stage — **caching** (never recompute what you already computed) and **batching** (amortize fixed costs over many items). Together they typically buy an order of magnitude before any algorithmic change is needed.

**Try it:** apply the rules to the Section 2 profile: the embedding stage is the bottleneck, so the highest-leverage fix is caching embeddings, not micro-optimizing the regex.""",
9: r"""## Summary: Profile before optimizing. Target the biggest bottleneck first. Cache aggressively.

**Measure before you optimize — and let the profile, not intuition, pick the bottleneck.**

The pipeline's latency is dominated by a handful of stages — OCR, LLM calls, embedding — and every optimization playbook in this chapter (caching, batching, cheaper models, faster parsers) targets those, not the millisecond stages profiling shows are already cheap. Simple wall-clock timing finds the stage; cProfile finds the function; the percent-formatting quirk in Section 2 is a reminder that profiling output deserves scrutiny too. This closes the Evaluation block: accuracy metrics, error analysis, hallucination guards, prompt A/B testing, human agreement, and now latency — the complete checklist for judging whether the resume pipeline is correct, trustworthy, and fast enough to ship.""",
}

apply(n64, R64)
apply(n65, R65)
apply(n66, R66)
apply(n67, R67)
apply(n68, R68)
apply(n69, R69)
print("all six notebooks applied OK")
