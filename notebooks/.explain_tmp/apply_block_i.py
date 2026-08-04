# -*- coding: utf-8 -*-
"""Expand markdown cells of block_i notebooks 50-54 (ch11 exemplar style).
Snapshots code cells, applies markdown replacements, then verifies:
JSON valid, headings intact, every md cell >= 300 chars, code cells byte-identical.
"""
import json
import sys

sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import apply, load

BI = r"D:\Projects\ResAnalyze\notebooks\part2_intelligence\block_i"
EM = "\u2014"  # em dash, as used in original headings

# ---------------------------------------------------------------- 50
p50 = BI + r"\50_ats_rule_design\50.ipynb"
r50 = {
0: (
"# 50 " + EM + " ATS Rule Design\n"
"**Goal:** Design a transparent rule-based ATS scoring system.\n"
"\n"
"Every ATS score should be a story: this resume covers 35% of the required skills, has five years against a three-year bar, and is missing two standard sections. This chapter builds the **rule set** that turns raw resume text into seven interpretable 0\u2013100 scores, each with a fixed, explicit weight. Nothing here is a black box \u2014 every point is produced by a function you can read, test, and defend in a meeting.\n"
"\n"
"**Why it matters for resumes / ATS:** recruiters and candidates both distrust an unexplained number. A transparent rule set is the difference between \"the system says 64\" and \"the system says 64 because you matched 4/4 required skills but missed the summary section.\" Rules are also deterministic and cheap \u2014 the same resume always gets the same score \u2014 which makes them the foundation for everything else in this block: explanations, simulation, and ranking."
),
1: (
"## 1. ATS Scoring Categories\n"
"\n"
"Scoring is **decomposed**: instead of one opaque number, the ATS measures seven independent dimensions, each normalized to 0\u2013100, then combines them with a **weighted sum**. The weights encode business priorities \u2014 skill match is worth seven times the boolean keyword check.\n"
"\n"
"| Dimension | What it measures | Weight |\n"
"|---|---|---|\n"
"| `skill_match` | % of required JD skills found in resume | 35% |\n"
"| `experience` | years of experience vs. requirement | 20% |\n"
"| `education` | degree level match | 15% |\n"
"| `bullet_quality` | STAR compliance of experience bullets | 10% |\n"
"| `format` | parseability, section completeness | 10% |\n"
"| `duration` | employment stability, gaps | 5% |\n"
"| `boolean` | must-have keywords present | 5% |\n"
"\n"
"**What the code does:** prints this dimension table, then instantiates `ATSScorer()` and confirms the weights sum to **1.0** \u2014 a sanity check, because if the weights ever drift off 1.0 the final 0\u2013100 scale silently breaks. Note the header's \"0-100 each\": every dimension must be normalized *before* weighting, or a 200-character resume would be dwarfed by a 50,000-character one."
),
3: (
"## 2. Defining Scoring Rules\n"
"\n"
"Each dimension gets its own **scoring function** \u2014 a small, readable rule instead of a model. `ATSScorer` stores the weights in a dict and implements four of the seven rules; the remaining three (`education`, `bullet_quality`, `duration`) are plugged in later.\n"
"\n"
"**What the code does:**\n"
"- `skill_match_score()` \u2014 case-insensitive overlap of resume skills against JD skills, returned as `matched / len(jd_skills) * 100`; an empty JD list returns 0.\n"
"- `experience_score()` \u2014 ratio of resume years to required years mapped to **bands**: \u22651.5\u00d7 \u2192 100, \u22651.0\u00d7 \u2192 90, \u22650.75\u00d7 \u2192 70, \u22650.5\u00d7 \u2192 50, else 30; no requirement at all defaults to 80. Meeting the bar exactly gives 90, not 100 \u2014 the top band is reserved for candidates who *exceed* it.\n"
"- `format_score()` \u2014 starts at 100 and subtracts 15 per missing section keyword (`summary`, `experience`, `education`, `skills`), 30 for text under 200 chars, 20 for text over 50,000; floors at 0.\n"
"- `boolean_check()` \u2014 fraction of must-have terms found, again as a percentage.\n"
"\n"
"**Try it:** run the cell and check `Weight sum: 1.0`. One trap to note: the section regexes are written `r\"\\\\b\"` \u2014 in a raw string that is an escaped backslash plus `b` (a literal `\\b` pattern), not a word boundary \u2014 so in the Ch. 51 run every section is reported missing. The intended pattern is `r\"\\b\"`."
),
5: (
"## Summary: ATS scoring decomposes match quality into interpretable dimensions with transparent weights.\n"
"\n"
"**Rules before models: a transparent weighted sum is the baseline every smarter scorer must beat.**\n"
"\n"
"Seven normalized dimensions \u00d7 fixed weights = one 0\u2013100 score, with every point attributable to a specific rule. That property \u2014 *decomposability* \u2014 is what makes the rest of this block possible: you can explain a score only if you know which dimension produced it, and you can simulate or rank only if the scoring is repeatable.\n"
"\n"
"This chapter feeds directly into Ch. 51, where each dimension score is paired with a human-readable reason, turning this weight table into a full explanation engine."
),
}

# ---------------------------------------------------------------- 51
p51 = BI + r"\51_explainable_scoring\51.ipynb"
r51 = {
0: (
"# 51 " + EM + " Explainable Scoring\n"
"**Goal:** Generate human-readable explanations for each resume score.\n"
"\n"
"Ch. 50 produced scores; this chapter makes them **defensible**. `ExplainableScorer` subclasses the Ch. 50 rule set and returns, for every dimension, not just a number but a `reason` string \u2014 \"Matched 1/3 required skills\" \u2014 plus the raw `details` behind it. The output is a structured dict, so a front end can render \"why 46.8?\" without the scorer ever writing prose.\n"
"\n"
"**Why it matters for resumes / ATS:** an unexplained score is a liability. Candidates contest it, recruiters can't act on it, and engineers can't debug it. When every dimension carries a reason, a low score becomes an actionable message (\"add a Summary section, learn SQL\") instead of a mystery \u2014 and a high score becomes evidence you can show a client or a hiring manager."
),
1: (
"![ATS Scoring Engine](../../../assets/images/ats_scoring_engine_1785491176998.png)\n"
"\n"
"> **Figure:** The ATS Scoring Engine " + EM + " showing the rule engine \u2192 semantic scorer \u2192 explainable output breakdown with weighted component scores.\n"
"\n"
"The figure is the architectural map for this whole block: the **rule engine** from Ch. 50 produces the dimension scores, a **semantic scorer** (added in later chapters) refines them, and an **explainable output** layer attaches reasons. The weighted component scores on the right are exactly the dict `score_with_explanations()` returns \u2014 each bar is one `{score, reason}` pair, so what you see in the chart is what you get in the data."
),
2: (
"## 1. Score Breakdown with Explanations\n"
"\n"
"`ExplainableScorer` adds one method to the Ch. 50 `ATSScorer`: `score_with_explanations()`, which returns `(total, explanations)` \u2014 a dict keyed by dimension, each entry holding `score`, `reason`, and sometimes `details`.\n"
"\n"
"**What the code does:**\n"
"- `skill_match` \u2014 calls `skill_match_score()`, then converts the percentage back into a count for the reason: `Matched 1/3 required skills`; `details` carries the raw found/required skill lists.\n"
"- `experience` \u2014 the reason is simply `5 years experience vs 3 required`; the number came from Ch. 50's band table.\n"
"- `format` \u2014 recomputes the missing-section list so the reason can name it: `Missing sections: ['summary', ...]` or `All sections present`.\n"
"- `boolean` \u2014 only present when `must_have_terms` is passed; reason reports `Found 1/2 required terms`.\n"
"- `total` \u2014 weighted sum **over whichever dimensions were computed**; dimensions never measured contribute nothing to the total.\n"
"\n"
"**Expected (verified by running):** with the sample resume the call returns `Total score: 46.8/100` with `skill_match 66.7`, `experience 100.0`, `format 10.0`, `boolean 50.0`. Two things stand out. First, `format` is 10.0: four sections \"missing\" (the `r\"\\\\b\"` word-boundary trap from Ch. 50, confirmed here) plus a 30-point short-text penalty. Second, the total is out of a 70-point budget, not 100 \u2014 `education`, `bullet_quality`, and `duration` were never computed, so 30% of the weight silently vanishes. Explaining every number is exactly how you catch that."
),
4: (
"## 2. Visualization of Score Breakdown\n"
"\n"
"A dict of numbers is still hard to scan; the chart makes the breakdown **visual**. Two side-by-side bar charts answer different questions: *which dimensions scored well?* (raw) versus *which dimensions actually moved the total?* (weighted).\n"
"\n"
"**What the code does:** builds three parallel lists \u2014 `scores` (raw 0\u2013100), `weights`, and `weighted = score \u00d7 weight` \u2014 then draws `ax1` as raw bars and `ax2` as weighted bars, saves the figure to `/tmp/ats_breakdown.png`, and shows it. The right-hand chart is the honest one: `skill_match` at 66.7 looks mediocre on the left but contributes `66.7 \u00d7 0.35 \u2248 23.3` points on the right \u2014 nearly half the total \u2014 while `format`'s 10.0 contributes only 1.0 point. Score \u00d7 weight, not score alone, is what ranking should optimize.\n"
"\n"
"**Caution:** `savefig('/tmp/ats_breakdown.png')` is POSIX-flavored. On Windows the absolute path resolves to the current drive's root (e.g. `D:\\tmp\\ats_breakdown.png`), which usually doesn't exist \u2014 verified: the cell renders the charts, then raises `FileNotFoundError` on the save. Create that directory or change the path."
),
6: (
"## Summary: Every score has an explanation. Transparency builds trust with recruiters and candidates.\n"
"\n"
"**A score without a reason is noise \u2014 attach a `reason` to every dimension and the system becomes auditable.**\n"
"\n"
"`score_with_explanations()` returns structured `{score, reason, details}` entries, so the 46.8 total decomposes into four explainable parts, each traceable to a Ch. 50 rule. That auditability doubles as a debugging tool: the missing `education`/`bullet_quality`/`duration` weights are visible precisely because the explanation dict only contains what was computed.\n"
"\n"
"This chapter feeds Ch. 52, where the same explainable scorer is embedded in a full end-to-end ATS simulation \u2014 parse, extract, score, report."
),
}

# ---------------------------------------------------------------- 52
p52 = BI + r"\52_ats_simulation_mode\52.ipynb"
r52 = {
0: (
"# 52 " + EM + " ATS Simulation Mode\n"
"**Goal:** Simulate how a real ATS processes and scores a resume.\n"
"\n"
"So far the pieces were built in isolation; this chapter wires them into one **pipeline**. `ATSSimulator` runs the four stages a real ATS performs \u2014 parse the document into sections, extract skills from a canonical vocabulary, score with the Ch. 51 explainable scorer, and print a report \u2014 as a single visible, reproducible pass over one resume + JD pair.\n"
"\n"
"**Why it matters for resumes / ATS:** a simulation is the cheapest way to test the whole system before it touches real candidates: every stage's intermediate state (detected sections, extracted skills, per-dimension reasons) is visible, which is exactly what you need for demos and for debugging a rule change. It is also the first honest end-to-end view of what a recruiter's ATS would actually see."
),
1: (
"## 1. Full ATS Pipeline\n"
"\n"
"`ATSSimulator.run(resume_text, jd_text)` is a scripted four-step pipeline that prints its own progress and returns a structured result dict.\n"
"\n"
"**What the code does:**\n"
"- **Parse** \u2014 scans for six section keywords with word-boundary regexes and prints `Sections detected: [...]`.\n"
"- **Extract** \u2014 matches resume and JD text against a 10-skill `skills_db` by case-insensitive substring, so \"Python\" is picked up regardless of formatting.\n"
"- **Score** \u2014 delegates to `ExplainableScorer.score_with_explanations()` (Ch. 51), with `must_have_terms` set to the first three JD skills.\n"
"- **Report** \u2014 prints `FINAL ATS SCORE` plus one line per dimension with its reason, and returns `{score, dimensions, skills}` for programmatic use.\n"
"\n"
"**Expected (verified by running):** on the sample resume/JD the run reports `FINAL ATS SCORE: 64.0/100` with `skill_match 100.0` (4/4), `experience 100.0`, `format 40.0`, `boolean 100.0` (3/3). Two surprises worth learning from: `Sections detected: []` despite the resume containing `SUMMARY`/`EXPERIENCE`/`SKILLS`/`EDUCATION` \u2014 the same `r\"\\\\b\"` word-boundary trap from Ch. 50, which also explains `format 40.0` (four sections counted missing, 4 \u00d7 15 deducted) \u2014 and the 64.0 total is out of a 70-point budget because `education`, `bullet_quality`, and `duration` are never computed. **Prerequisite:** this cell assumes `ATSScorer`, `ExplainableScorer`, and `re` are already in the kernel from Ch. 50\u201351; run those first or the class definition raises `NameError`."
),
3: (
"## Summary: ATS simulation makes the scoring pipeline visible end-to-end. Useful for debugging and demos.\n"
"\n"
"**A pipeline you can watch is a pipeline you can fix \u2014 simulation turns scoring into a visible, repeatable run.**\n"
"\n"
"With parse \u2192 extract \u2192 score \u2192 report in one method, every intermediate value (detected sections, extracted skills, dimension reasons) is inspectable, and the same run that scores 64.0 also surfaces the two live bugs in the rule set: the broken word-boundary regex and the missing dimension weights. That is Ch. 51's explainability applied at pipeline scale.\n"
"\n"
"This chapter's extract stage feeds Ch. 53, where the extracted skill list is diffed against career-path requirements to find what is missing."
),
}

# ---------------------------------------------------------------- 53
p53 = BI + r"\53_skill_gap_analysis\53.ipynb"
r53 = {
0: (
"# 53 " + EM + " Skill Gap Analysis\n"
"**Goal:** Identify missing skills and generate upskilling recommendations.\n"
"\n"
"Scoring says *how far* a candidate is from the job; this chapter says *what exactly is missing*. `SkillGapAnalyzer` matches the resume text against a curated **skills taxonomy** (six categories), compares what was found against the core and advanced skill lists of a target **career path**, and returns a coverage ratio plus explicit recommendations.\n"
"\n"
"**Why it matters for resumes / ATS:** gap analysis is the coaching layer of the ATS. A recruiter can tell a candidate \"you matched 50%\" \u2014 but only a per-skill breakdown can say \"you're missing Kubernetes, MLOps, and CI/CD; learn those first.\" The same machinery powers candidate coaching, hiring-manager debriefs, and internal upskilling programs."
),
1: (
"## 1. Finding Skill Gaps\n"
"\n"
"`analyze_gaps(resume_text, target_role)` works in three steps: **scan** the resume for taxonomy skills (case-insensitive substring match), **look up** the target role's `core`/`advanced` requirement lists, and **compare** to produce `coverage`, met/gap lists, and recommendations.\n"
"\n"
"**What the code does:**\n"
"- `skills_taxonomy` \u2014 6 categories (programming, ml_dl, nlp, data, cloud_devops, databases) with ~30 curated skills; only skills in this list can ever be detected.\n"
"- `career_paths` \u2014 3 roles (`data_scientist`, `ml_engineer`, `nlp_engineer`), each with a `core` and an `advanced` list; an unknown role returns `{\"error\": ...}` instead of crashing.\n"
"- `coverage` \u2014 `(core_found + adv_found) / (core_total + adv_total)`, rounded to 2 decimals.\n"
"- `recommendations` \u2014 `\"Learn {skill}\"` for missing core skills (blockers) and `\"Consider {skill}\"` for missing advanced ones (nice-to-haves) \u2014 the verb encodes priority.\n"
"\n"
"**Expected (verified by running):** with the sample resume targeting `ml_engineer`, the output is `Coverage: 50%`, `Core met: ['Python', 'TensorFlow', 'Docker']`, `Core gaps: []`, `Advanced gaps: ['Kubernetes', 'MLOps', 'CI/CD']`, and three \"Consider\" recommendations. The core list is fully met \u2014 the resume is job-ready on the essentials \u2014 so every recommendation is a `Consider ...` item; had a core skill been missing it would have been promoted to `Learn ...`. Note `coverage` counts core and advanced equally: a candidate missing every core skill but knowing all advanced ones still scores 50%, which is why the met/gap lists matter more than the single number."
),
3: (
"## Summary: Skill gap analysis identifies specific missing skills and career path recommendations.\n"
"\n"
"**Know the gap, not just the score \u2014 per-skill comparison turns a 50% coverage number into a learning plan.**\n"
"\n"
"By diffing found skills against a role's core/advanced lists, `analyze_gaps()` produces actionable output: which skills to `Learn` (core blockers) versus `Consider` (advanced optional), plus the raw met/gap lists for any custom logic downstream. The taxonomy constraint is the honest trade-off \u2014 detection is only as good as the curated skill list, and anything outside it is invisible.\n"
"\n"
"This chapter feeds Ch. 54, where per-candidate skill data is aggregated into a single ranking across a whole applicant pool."
),
}

# ---------------------------------------------------------------- 54
p54 = BI + r"\54_resume_ranking\54.ipynb"
r54 = {
0: (
"# 54 " + EM + " Resume Ranking\n"
"**Goal:** Rank multiple resumes against a job description for candidate shortlisting.\n"
"\n"
"Individual scoring answers \"is this candidate viable?\"; **ranking** answers \"which candidates first?\" `ResumeRanker` loops over a batch of `(name, text)` resumes, scores each against one JD, sorts descending, and labels each with a shortlist status \u2014 the classic recruiter triage view.\n"
"\n"
"**Why it matters for resumes / ATS:** a hiring pipeline sees hundreds of resumes per role. Ranking turns the scoring machinery into a single sortable list with a defensible threshold (\u226580 SHORTLIST, \u226560 MAYBE, else PASS), so recruiters can work from the top down and candidates can see exactly what separated first from last."
),
1: (
"## 1. Batch Resume Ranking\n"
"\n"
"`rank(resumes, jd_text)` scores every resume in the batch, sorts by score descending, and returns a list of dicts \u2014 `name`, `score`, `skills_found`.\n"
"\n"
"**What the code does:**\n"
"- `__init__` tries to attach a `ResumeJDMatcher` (a semantic matcher from later chapters) but checks `'ResumeJDMatcher' in dir()` \u2014 and inside a method `dir()` sees only **local** names, so that is never true here and the simplified scorer always runs. The hook is ready for a real matcher imported at module level.\n"
"- The simplified path reuses a fixed 6-skill vocabulary: `skill_ratio = matched JD skills / total JD skills`, then `score = ratio * 80 + 10`. The +10 floor guarantees even a zero-match resume scores 10; the \u00d780 cap means the top score is 90, leaving headroom for a future embedding term (`details[\"embedding\"]` is hard-coded to `0.5` as a placeholder).\n"
"- `skills_found` counts the resume's hits against that same vocabulary.\n"
"- Sorting is `reverse=True` on score; Python's sort is stable, so ties keep input order.\n"
"\n"
"**Expected (verified by running):** against the sample JD the output is `#1 Alice 90.0`, `#2 Diana 63.3`, `#3 Charlie 36.7`, `#4 Bob 10.0`. Alice matches all three JD skills (Python, NLP, TensorFlow); Diana matches two; Charlie's three hits (Python, SQL, AWS) overlap the JD by only Python; Bob (Java/Spring) matches none and gets the 10-point floor. `skills_found` counts vocabulary hits, not JD hits \u2014 Charlie shows 3 yet ranks below Diana's 2."
),
3: (
"## 2. Display Results\n"
"\n"
"Ranking is only useful if a human can scan it \u2014 this cell renders the sorted list as a **status table** with recruiter-style thresholds.\n"
"\n"
"**What the code does:** prints a header row, then for each ranked candidate a `Rank`/`Name`/`Score`/`Status` row, where status is assigned by band: `score >= 80 \u2192 SHORTLIST`, `>= 60 \u2192 MAYBE`, else `PASS`. The thresholds are deliberately simple \u2014 a transparent cut rule the whole team can argue about, exactly like the Ch. 50 weights.\n"
"\n"
"**Expected (verified by running):** Alice (90.0) is `SHORTLIST`, Diana (63.3) is `MAYBE`, Charlie (36.7) and Bob (10.0) are `PASS`. The cutoff logic runs *after* sorting, so the table reads top-down as a funnel: two candidates worth a call, two parked."
),
5: (
"## Summary: Resume ranking aggregates all ATS dimensions into a single sortable score.\n"
"\n"
"**Ranking is the payoff of everything before it \u2014 one sortable score per candidate, with thresholds anyone can read.**\n"
"\n"
"`ResumeRanker` batches Ch. 50's rules, Ch. 51's explainability, and Ch. 52's pipeline into a single descending list, and the 80/60 bands turn that list into a triage funnel (SHORTLIST / MAYBE / PASS). The simplified scorer is honest about its limits: vocabulary-only matching, a 90-point ceiling, and an `embedding: 0.5` placeholder waiting for real semantics.\n"
"\n"
"That placeholder is the bridge to what comes next: Ch. 55 (OpenRouter Setup) introduces the LLM layer that will replace hard-coded skill lists and heuristic scores with semantic, generative matching."
),
}

# ---------------------------------------------------------------- apply
PLAN = [(p50, r50), (p51, r51), (p52, r52), (p53, r53), (p54, r54)]

HEADINGS = {
    p50: {0: "# 50 " + EM + " ATS Rule Design", 1: "## 1. ATS Scoring Categories",
          3: "## 2. Defining Scoring Rules",
          5: "## Summary: ATS scoring decomposes match quality into interpretable dimensions with transparent weights."},
    p51: {0: "# 51 " + EM + " Explainable Scoring", 1: "![ATS Scoring Engine]",
          2: "## 1. Score Breakdown with Explanations", 4: "## 2. Visualization of Score Breakdown",
          6: "## Summary: Every score has an explanation. Transparency builds trust with recruiters and candidates."},
    p52: {0: "# 52 " + EM + " ATS Simulation Mode", 1: "## 1. Full ATS Pipeline",
          3: "## Summary: ATS simulation makes the scoring pipeline visible end-to-end. Useful for debugging and demos."},
    p53: {0: "# 53 " + EM + " Skill Gap Analysis", 1: "## 1. Finding Skill Gaps",
          3: "## Summary: Skill gap analysis identifies specific missing skills and career path recommendations."},
    p54: {0: "# 54 " + EM + " Resume Ranking", 1: "## 1. Batch Resume Ranking", 3: "## 2. Display Results",
          5: "## Summary: Resume ranking aggregates all ATS dimensions into a single sortable score."},
}

report = []
for path, repl in PLAN:
    # snapshot code cells before any change
    nb0 = load(path)
    code0 = [json.dumps(c, ensure_ascii=False) for c in nb0["cells"] if c["cell_type"] == "code"]
    md_idx0 = [i for i, c in enumerate(nb0["cells"]) if c["cell_type"] == "markdown"]

    apply(path, replace=repl)

    nb1 = load(path)
    code1 = [json.dumps(c, ensure_ascii=False) for c in nb1["cells"] if c["cell_type"] == "code"]
    assert code0 == code1, f"{path}: CODE CELLS CHANGED"
    assert [i for i, c in enumerate(nb1["cells"]) if c["cell_type"] == "markdown"] == md_idx0, f"{path}: md layout changed"

    md_cells = [c for c in nb1["cells"] if c["cell_type"] == "markdown"]
    lengths = {}
    for i, c in enumerate(nb1["cells"]):
        if c["cell_type"] == "markdown":
            src = "".join(c["source"])
            lengths[i] = len(src)
            assert len(src) >= 300, f"{path} cell {i}: only {len(src)} chars"
            for hk, hv in HEADINGS[path].items():
                if i == hk:
                    assert src.startswith(hv), f"{path} cell {i}: heading changed: {src[:60]!r} vs {hv[:60]!r}"
    total_md = sum(lengths.values())
    report.append((path, len(md_cells), total_md, min(lengths.values()), lengths))

print("ALL CHECKS PASSED")
for path, n, tot, mn, lengths in report:
    print(f"{path.split(chr(92))[-2]}: md cells={n} total_md_chars={tot} min_cell_chars={mn} lens={lengths}")
