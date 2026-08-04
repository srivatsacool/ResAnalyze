# -*- coding: utf-8 -*-
"""Expand markdown cells of block_j notebooks 55-63 (ch11 exemplar style).
Snapshots code cells, applies markdown replacements, then verifies:
JSON valid, headings intact, every md cell >= 300 chars, code cells byte-identical.
"""
import json
import sys

sys.path.insert(0, r"D:\Projects\ResAnalyze\notebooks\.explain_tmp")
from nbtools import apply, load

BJ = r"D:\Projects\ResAnalyze\notebooks\part3_production\block_j"
EM = "\u2014"  # em dash, as used in original headings

# ---------------------------------------------------------------- 55
p55 = BJ + r"\55_openrouter_setup\55.ipynb"
r55 = {
0: (
"# 55 " + EM + " OpenRouter Setup\n"
"**Goal:** Configure OpenRouter API, select models, manage costs and rate limits.\n"
"\n"
"The previous chapters built the rule-based and semantic layers of the ATS entirely in-process. This chapter opens the door to the **LLM layer**: a single OpenAI-compatible client that fronts 200+ hosted models " + EM + " GPT, Claude, Gemini, Llama, Mistral " + EM + " through one endpoint. Everything downstream in this block (prompt templates, structured JSON, tool calling) speaks to that one client, so getting the plumbing right here pays off for the next eight chapters.\n"
"\n"
"**Why it matters for resumes / ATS:** resume rewriting, skill classification, and STAR generation are *generation* tasks where fixed rules plateau " + EM + " no grammar can produce fluent, quantified bullets. A hosted LLM gateway lets the ATS pick the cheapest adequate model per task, fall back when one provider throttles, and meter every call against a single account. One API, many models, no vendor lock-in " + EM + " that is the infrastructure every later chapter assumes."
),
1: (
"## 1. Why OpenRouter?\n"
"\n"
"OpenRouter is an **aggregator, not a model**: it proxies requests to many providers behind one OpenAI-compatible endpoint. That buys three properties a production ATS needs " + EM + " **portability** (swap `gpt-4o-mini` for `claude-3.5-haiku` by changing one string), **resilience** (automatic fallback when a provider is down or rate-limited), and **cost control** (per-model pricing and usage tracking on one dashboard).\n"
"\n"
"**What the code does:** prints the pitch " + EM + " one endpoint for 200+ models, built-in fallback, cost tracking, no vendor lock-in " + EM + " then maps each resume task family to a concrete model: `GPT-4-mini` for rewriting and generation, `Claude 3 Haiku` for cheap classification, `Llama 3 70B` as the open-source alternative, `Mistral Small` as the budget option. That mapping is the seed of the `pick_model()` helper in section 3."
),
3: (
"## 2. Setting Up the Client\n"
"\n"
"The client is the standard OpenAI SDK pointed at a different `base_url`. The only real configuration is the **API key**, which should come from the environment " + EM + " never hard-coded into a notebook that might be committed.\n"
"\n"
"**What the code does:**\n"
"- `os.getenv(\"OPENROUTER_API_KEY\")` " + EM + " reads the key from the environment, falling back to `OPENAI_API_KEY`; the same client object works for either because the base URL decides the provider.\n"
"- `OpenAI(base_url=\"https://openrouter.ai/api/v1\", api_key=...)` " + EM + " an OpenAI-compatible client that speaks the Chat Completions protocol to OpenRouter.\n"
"- `client.models.list()` " + EM + " the connection test. **Expected:** with a valid key it returns the model catalog and the cell prints the first five free model ids (`... if \"free\" in m.id`); without a key it raises an auth error and the `except` branch prints the message plus the \"(Expected if no API key...)\" note, so the notebook still runs as reference material."
),
5: (
"## 3. Model Selection Helper\n"
"\n"
"Model choice is a **cost/quality trade**, so the code codifies it as three named tiers " + EM + " `cheap`, `balanced`, `best`, each with two interchangeable model ids " + EM + " then maps *task families* to tiers.\n"
"\n"
"**What the code does:**\n"
"- `MODEL_TIERS` " + EM + " dict of tier " + EM + " model list; the first entry of a tier is the default.\n"
"- `pick_model(task, quality=\"balanced\")` " + EM + " looks up the task's recommended tier (`classification " + EM + " cheap`, `extraction " + EM + " balanced`, `rewriting " + EM + " balanced`, `generation " + EM + " best`) and returns that tier's first model; unknown tasks fall back to the caller's `quality` argument.\n"
"\n"
"**Expected (verified by running):** the loop prints `classification -> mistralai/mistral-small-24b-instruct-2501`, `extraction -> openai/gpt-4o-mini`, `rewriting -> openai/gpt-4o-mini`, `generation -> openai/gpt-4o`. The pattern to internalize: classification is the only task deemed cheap enough for a small model " + EM + " generation, where quality shows, always gets the flagship."
),
7: (
"## 4. Cost Tracking\n"
"\n"
"LLM pricing is **per-token and asymmetric**: output tokens typically cost 4" + EM + "10x input tokens. Before shipping a pipeline you need a rough per-call budget, which is what this cell computes from a hard-coded price table.\n"
"\n"
"**What the code does:** `COST_PER_1K` holds USD per 1K tokens for three models; `estimate_cost(model, in, out)` applies `(in/1000 * price_in) + (out/1000 * price_out)` and returns a formatted `$...` string " + EM + " or `\"Check pricing page\"` for models not in the table.\n"
"\n"
"**Expected (verified by running):** for a typical resume rewrite (500 input / 300 output tokens) the estimates are `gpt-4o-mini $0.000255`, `claude-3.5-haiku $0.000500`, `mistral-small-24b $0.000280`. Two lessons: per-call costs are sub-cent (which is why LLM ATS features are viable), but at scale " + EM + " 10,000 resumes times several calls each " + EM + " they add up, so the tier system of section 3 exists to keep the expensive model on the expensive tasks."
),
9: (
"## Summary: OpenRouter gives access to all major models through one API. Pick model by task complexity.\n"
"\n"
"**One OpenAI-compatible client is the entire LLM infrastructure " + EM + " model choice is a routing decision, not an integration decision.**\n"
"\n"
"With a single `base_url`, the ATS can switch providers by editing a string, fall back when a vendor throttles, and meter cost per call. `pick_model()` turns that freedom into a policy: cheap models for classification, balanced for extraction and rewriting, flagship for generation. The numbers back it up " + EM + " a single rewrite costs about a quarter of a millicent " + EM + " so the bottleneck is never the API bill; it is prompt quality.\n"
"\n"
"This chapter feeds Ch. 56, where the same client starts consuming carefully engineered prompts for resume-domain tasks."
),
}

# ---------------------------------------------------------------- 56
p56 = BJ + r"\56_prompt_engineering\56.ipynb"
r56 = {
0: (
"# 56 " + EM + " Prompt Engineering\n"
"**Goal:** Design effective prompts for resume-domain LLM tasks.\n"
"\n"
"Ch. 55 gave us a client; this chapter gives it something worth saying. An LLM's output quality is bounded by the **prompt contract**: the role, the examples, the context, and the output format you specify. For resume work the contract has to fight the model's default behavior " + EM + " vague verbs, unquantified claims, free-form prose " + EM + " so every prompt in this chapter is built from the same five components: system role, few-shot examples, context, instruction, and output format.\n"
"\n"
"**Why it matters for resumes / ATS:** prompts are the only place the ATS's domain knowledge (STAR format, quantified results, skill categories) meets the model. A classifier told to \"return only the category\" is parseable; one left to free-associate produces junk that needs cleaning. Prompt structure is the cheapest quality lever in the whole block " + EM + " no retraining, no new models, just disciplined templates."
),
1: (
"![LLM Prompt Engineering Pipeline](../../../assets/images/llm_prompt_pipeline_1785491212825.png)\n"
"\n"
"> **Figure:** The LLM prompt pipeline " + EM + " from resume+JD context through versioned templates, OpenRouter API, to validated structured JSON output.\n"
"\n"
"The figure is the road map for the rest of this block: resume + JD text enters a **template** (this chapter), the template is versioned so changes are trackable (Ch. 57), the call goes out through the single OpenRouter client from Ch. 55, and the response is validated against a JSON contract (Ch. 58) before any downstream consumer touches it. Each stage is a chapter; the pipeline as a whole is what turns raw text into dependable structured resume data."
),
2: (
"## 1. Prompt Structure Patterns\n"
"\n"
"Every resume-task prompt decomposes into the same five parts, in the same order: **system** (role + constraints), **few-shot examples** (demonstrate the pattern), **context** (the resume data), **instruction** (what to do with it), and **output format** (the shape of the answer). Omitting any one invites a specific failure: no system role " + EM + " the model argues with you; no examples " + EM + " format drift; no output format " + EM + " prose you must parse.\n"
"\n"
"**What the code does:** prints the five components and the four canonical resume task patterns " + EM + " `Classification` (\"Classify this skill as technical/soft/tool\"), `Extraction` (\"Extract years of experience\"), `Rewriting` (\"Rewrite this bullet using STAR\"), `Generation` (\"Generate interview questions\"). These four task types map 1:1 onto Ch. 55's tier policy " + EM + " classification is the cheap task, generation the flagship one."
),
4: (
"## 2. Building a Prompt Template System\n"
"\n"
"Templates are **parameterized prompts**: a fixed skeleton with slots for the input. `PROMPT_TEMPLATES` stores each template's `system` role and `examples` (input/output pairs), and `format_prompt()` assembles a full prompt from them " + EM + " so the same template serves any input text with zero prompt-writing per call.\n"
"\n"
"**What the code does:**\n"
"- `skill_classify` " + EM + " the system role demands one of four categories and \"Return only the category\"; four examples pin the taxonomy (`Python " + EM + " technical`, `Team Leadership " + EM + " soft`, `TensorFlow " + EM + " tool`, `NLP " + EM + " domain_knowledge`).\n"
"- `bullet_rewrite` " + EM + " the system role is a \"professional resume coach\" rewriting to quantified STAR; one example shows the transformation (\"Responsible for ML models\" " + EM + " \"Developed ML models achieving 95% accuracy...\").\n"
"- `format_prompt(template, input)` " + EM + " builds `System: ...`, then one `Input:/Output:` block per example, then the live `Input: {text}\\nOutput:` ending.\n"
"\n"
"**Expected (verified by running):** formatting `bullet_rewrite` with \"Was responsible for data pipelines\" yields a prompt that ends in `Input: Was responsible for data pipelines\\nOutput:` " + EM + " the model is expected to continue after the colon, which is exactly how you get a single answer instead of a chatty one."
),
6: (
"## 3. Testing Prompts\n"
"\n"
"Prompts are code " + EM + " they regress. The discipline here is borrowed from software testing: a **golden test set** of 20" + EM + "50 known (input " + EM + " expected output) pairs, run against every prompt variant, scored on accuracy, consistency, robustness, and cost.\n"
"\n"
"**What the code does:** prints the methodology: build the golden set, run each variant against it, score outputs (exact match, semantic similarity, or human rating), and track versions in a registry. The four test dimensions matter for different reasons: `Accuracy` is extraction correctness, `Consistency` is same-input-same-output (LLMs are stochastic, so you measure variance), `Robustness` is behavior on empty or malformed input (a resume parser will receive garbage), and `Cost` is tokens per call " + EM + " measurable with Ch. 55's price table.\n"
"\n"
"**Try it:** run a golden set through `format_prompt()` from section 2 and eyeball two outputs per input " + EM + " identical prompts should produce near-identical answers; if not, your temperature or prompt is too loose."
),
8: (
"## Summary: Structured prompt templates improve consistency. Test prompts systematically against golden datasets.\n"
"\n"
"**A prompt is a function " + EM + " parameterize it, and test it like one.**\n"
"\n"
"Five components (system, examples, context, instruction, format) become a reusable template, and every template ships with a golden set that measures accuracy, consistency, robustness, and cost. That combination " + EM + " templating plus tests " + EM + " is what makes LLM behavior *predictable enough* to ship: the model still samples, but the variance is bounded by the contract you wrote.\n"
"\n"
"Templates that get tested tend to get edited, which is exactly the problem Ch. 57 solves: versioning prompts in a registry with regression checks."
),
}

# ---------------------------------------------------------------- 57
p57 = BJ + r"\57_prompt_versioning\57.ipynb"
r57 = {
0: (
"# 57 " + EM + " Prompt Versioning\n"
"**Goal:** Track prompt versions with a registry, golden test sets, and regression checks.\n"
"\n"
"Ch. 56 produced prompt templates; this chapter treats them as **versioned artifacts**. `register_prompt()` stores each prompt's system text, template, test cases, and a content hash in a registry keyed `name@version`, so you can always say *which* prompt produced *which* output " + EM + " the reproducibility requirement for a system whose answers influence hiring decisions.\n"
"\n"
"**Why it matters for resumes / ATS:** an untracked prompt change can silently degrade extraction quality across every resume processed. With a registry, a \"small tweak\" becomes a diffable, testable event: register v2.0, run both versions against the golden set, and only promote v2.0 if it wins. Versioning is what lets prompt engineering scale past one person's notebook."
),
1: (
"## 1. Prompt Registry\n"
"\n"
"A registry is a dict keyed by `name@version`. Each entry captures the **system prompt**, the **template**, the **test cases** that define correct behavior, and a **hash** of the prompt content " + EM + " a fingerprint that changes whenever the text changes.\n"
"\n"
"**What the code does:**\n"
"- `register_prompt(name, version, system_prompt, template, test_cases)` " + EM + " builds an entry and stores it under `f\"{name}@v{version}\"`; the hash is `sha256(system_prompt + template).hexdigest()[:12]`, so two entries with identical content are detectable by eye.\n"
"- Registers `skill_extract@v1.0` (with test `(\"Python developer\", [\"Python\"])`) and `bullet_rewrite@v1.0` (with test `(\"Responsible for ML\", \"Developed ML models achieving...\")`).\n"
"\n"
"**Expected (verified by running):** the registry ends with 2 entries; the printed keys are `skill_extract@v1.0` and `bullet_rewrite@v1.0` with hashes `150ca689d6c8` and `f4b34b5fada2`. Note the test cases are stored *with* the prompt " + EM + " a prompt without its tests is a claim without evidence."
),
3: (
"## 2. Version Comparison\n"
"\n"
"Prompts change, and each change is a **hypothesis**: \"this wording improves extraction.\" The comparison protocol makes that hypothesis testable " + EM + " run old and new against the same golden set and compare on accuracy, cost, and consistency.\n"
"\n"
"**What the code does:** prints the diffing workflow: register the new version (`skill_extract@v2.0`), run both versions on the golden test set, compare metrics (accuracy, cost, consistency), and only promote v2.0 to default if it is >= v1.0 on *all* metrics. The closing rules are the operational ones: **keep old versions** (rollback is free if you never delete) and **always test before deploying**.\n"
"\n"
"**Why it matters:** a prompt that improves F1 by 2 points but doubles token cost is a business decision, not a code change " + EM + " and you can only make that call if both versions exist with measured numbers."
),
5: (
"## Summary: Version prompts like code. Registry + golden tests prevent regression.\n"
"\n"
"**Every prompt change is a deploy " + EM + " give it a version, a hash, and a test run.**\n"
"\n"
"The registry keys prompts as `name@version`, fingerprints content with a SHA-256 hash, and stores test cases alongside the text, so any output can be traced to an exact prompt revision and any change can be validated against the golden set before it becomes the default. That is the difference between prompt *editing* and prompt *engineering*.\n"
"\n"
"This chapter feeds Ch. 58, where the output side gets the same rigor: instead of trusting free-form LLM prose, the response is forced into a JSON contract and validated with Pydantic."
),
}

# ---------------------------------------------------------------- 58
p58 = BJ + r"\58_json_structured_output\58.ipynb"
r58 = {
0: (
"# 58 " + EM + " JSON Structured Output\n"
"**Goal:** Get structured JSON from LLMs using response_format and Pydantic parsing.\n"
"\n"
"Everything downstream " + EM + " scoring, gap analysis, ranking " + EM + " wants a dict, not prose. This chapter makes the LLM produce JSON at generation time (`response_format`) and validates it at the boundary with **Pydantic** models, so a malformed or hallucinated response fails loudly instead of corrupting the pipeline.\n"
"\n"
"**Why it matters for resumes / ATS:** free-form LLM text is the classic integration hazard: one run returns `{\"skills\": [...]}`, the next returns \"Here are the skills: ...\" in markdown. A structured contract means the extraction stage either yields typed, validated `ResumeSkill` objects or a caught `ValidationError` " + EM + " never a silent parse failure mid-pipeline."
),
1: (
"## 1. Why Structured Output?\n"
"\n"
"Unconstrained LLM output has three recurring failure modes: **format drift** (the shape of the answer changes between calls), **parse failures** (markdown fences, truncated JSON, trailing prose), and **hallucinated field names** (`skill` vs `skills` vs `Skill`). All three are fixable at the generation or validation layer.\n"
"\n"
"**What the code does:** prints the failure modes and the four mitigation strategies, in increasing strictness: prompt-only JSON (\"Respond in JSON: ...\"), `response_format` (`json_object` / `json_schema` on OpenAI-compatible APIs), Pydantic-based libraries like `instructor`, and constrained generation like `outlines` (which restricts the token sampler itself). The order matters: prompt-only is the cheapest and weakest; constrained generation is the strongest and most work. This chapter uses `response_format` + Pydantic " + EM + " the pragmatic middle."
),
3: (
"## 2. Using response_format\n"
"\n"
"The idea: tell the API *at request time* that the answer must be valid JSON, then parse it into a typed object. `SkillExtract` declares the contract " + EM + " `skill_name`, `years_experience`, `proficiency` " + EM + " and doubles as both the schema and the parse target.\n"
"\n"
"**What the code does:**\n"
"- Defines `SkillExtract(BaseModel)` " + EM + " three fields: `str`, `int`, `str`. Pydantic generates the JSON Schema for the model (printed via `model_json_schema(indent=2)`), so the schema lives in one place instead of being hand-copied into the prompt.\n"
"- The live call is left commented out because it needs an API key: `client.chat.completions.create(..., response_format={\"type\": \"json_object\"})`, then `json.loads(response.choices[0].message.content)`.\n"
"\n"
"**Expected (with a key):** the request returns a JSON object with exactly `skill_name`, `years_experience`, and `proficiency` " + EM + " for \"5 years Python\", something like `{\"skill_name\": \"Python\", \"years_experience\": 5, \"proficiency\": \"...\"}`. The contract: the model is *encouraged* to emit valid JSON, but nothing guarantees field correctness " + EM + " that is Pydantic's job in section 3. **Note (verified by running):** on pydantic 2.13 the schema print itself crashes with `TypeError: BaseModel.model_json_schema() got an unexpected keyword argument 'indent'` " + EM + " drop the `indent=2` argument on that line to see the schema."
),
5: (
"## 3. Pydantic Parsing\n"
"\n"
"Generation-time hints reduce JSON syntax errors; **Pydantic catches the rest**. `ResumeExtraction` nests a list of `ResumeSkill` objects plus `total_years`, and `model_validate_json()` parses *and* validates in one call " + EM + " wrong types, missing required fields, and wrong shapes all raise `ValidationError` with a machine-readable list of errors.\n"
"\n"
"**What the code does:**\n"
"- `ResumeSkill` " + EM + " `name: str`, `category: str`, `years: Optional[int] = None`; optional fields tolerate LLMs that omit them.\n"
"- `ResumeExtraction` " + EM + " `skills: List[ResumeSkill]`, `total_years: int`.\n"
"- Valid path: `model_validate_json(valid_json)` " + EM + " **expected (verified by running):** prints `Parsed: Python -> 5 years`.\n"
"- Invalid path: `'{\"skills\": \"Python\"}'` " + EM + " `skills` is a string, not a list, so validation fails; **expected (verified by running):** the caught error message is `Input should be a valid array`. The pipeline never sees the bad data " + EM + " it sees a typed exception it can log and retry.\n"
"\n"
"**Try it:** mutate `valid_json` (drop `total_years`, make `years` a string) and watch each failure surface as a precise Pydantic error instead of a crash downstream."
),
7: (
"## Summary: Structured output is essential for production LLM use. Pydantic parsing catches errors at the boundary.\n"
"\n"
"**Two layers, one contract: ask for JSON at generation time, enforce it at parse time.**\n"
"\n"
"`response_format` reduces syntax errors; Pydantic models turn the response into typed, validated objects and convert the rest into caught `ValidationError`s with exact messages " + EM + " bad shapes become events you can log and retry, never silent corruption. Because the schema is generated from the model, the contract cannot drift between the prompt and the parser.\n"
"\n"
"Structured output is the plumbing Ch. 59 builds on: tool calling hands the LLM typed arguments, and the same Pydantic discipline applies to tool-call payloads."
),
}

# ---------------------------------------------------------------- 59
p59 = BJ + r"\59_tool_calling_for_resume_tasks\59.ipynb"
r59 = {
0: (
"# 59 " + EM + " Tool Calling for Resume Tasks\n"
"**Goal:** Use function calling to route LLM decisions to specialized engines.\n"
"\n"
"Tool calling (a.k.a. function calling) reverses the usual flow: the **LLM decides** which deterministic engine to invoke, and the engines " + EM + " skill lookup, ATS scoring, bullet generation " + EM + " stay as plain, testable Python. The model is the router; the code is the worker.\n"
"\n"
"**Why it matters for resumes / ATS:** LLMs are unreliable at arithmetic and exact database lookups but excellent at understanding intent. Tool calling exploits that split: the model parses \"does this resume match the JD?\" into a `score_ats(resume_text, jd_text)` call with typed arguments, and the deterministic engine returns ground truth. Hallucination risk shrinks because the model never computes the score " + EM + " it only selects the tool."
),
1: (
"## 1. The Tool Pattern\n"
"\n"
"The loop has four stages: the LLM analyzes the user's request, **decides** which tool to call, the tool executes a specialized engine, and the LLM formats the result for the user. The model is never asked to *do* the work the tool does " + EM + " only to route to it.\n"
"\n"
"**What the code does:** prints the pattern and catalogs the resume-domain tool set the rest of the block uses:\n"
"- `search_skills_db(query)` " + EM + " canonical skill-name lookup (the taxonomy from Ch. 53)\n"
"- `parse_resume(file)` " + EM + " structured extraction\n"
"- `score_ats(resume, jd)` " + EM + " the rule engine from Ch. 50" + EM + "52\n"
"- `get_skill_trends(skill)` " + EM + " market data\n"
"- `generate_star_bullet(context)` " + EM + " bullet generation (Ch. 60" + EM + "61)\n"
"\n"
"Each tool is a function with a *name* and a *description* " + EM + " and that description is what the LLM reads when choosing, so writing it well is prompt engineering in disguise."
),
3: (
"## 2. Tool Definitions\n"
"\n"
"Tools are declared to the API as **JSON Schema** objects in the `tools` argument of the chat request. The schema is the contract the model must fill: it declares the function name, a natural-language description, the parameter types, and which parameters are required.\n"
"\n"
"**What the code does:**\n"
"- `score_ats` " + EM + " parameters `resume_text` (string) and `jd_text` (string), both `required`; the description tells the model when to reach for it: \"Score a resume against a job description\".\n"
"- `search_skills` " + EM + " one parameter, `query`; \"Search canonical skill taxonomy\".\n"
"- The cell then prints each tool's name + description " + EM + " **expected (verified by running):** two lines, `score_ats: Score a resume against a job description` and `search_skills: Search canonical skill taxonomy`.\n"
"\n"
"**Why it matters:** the parameter schema is what the model fills in " + EM + " a missing `required` list is how you get tool calls with no arguments. Declaring types (`string`) also lets the API reject malformed calls before your code sees them."
),
5: (
"## 3. Tool Execution Engine\n"
"\n"
"The schema is the interface; `execute_tool()` is the implementation. A real agent loop would: (1) send the request with `tools`, (2) get back `tool_calls` with a name plus arguments JSON, (3) call `execute_tool(name, args)`, (4) return the result to the model. This cell stubs the middle so the routing contract is testable without an API key.\n"
"\n"
"**What the code does:** `execute_tool(name, args)` dispatches through a dict of lambdas " + EM + " `score_ats` returns a hard-coded `{\"score\": 85, \"confidence\": 0.9}` (a stand-in for the Ch. 50" + EM + "52 engine) and `search_skills` wraps its query as `\"TensorFlow (canonical)\"` (a stand-in for the Ch. 53 taxonomy). Unknown names hit the `{\"error\": ...}` fallback.\n"
"\n"
"**Expected (verified by running):** `score_ats` returns `{'score': 85, 'confidence': 0.9}`, `search_skills` returns `{'results': ['TensorFlow (canonical)']}`, and an unknown tool returns `{'error': 'Unknown tool: nope'}` " + EM + " the routing never raises, it reports."
),
7: (
"## Summary: Tool calling lets LLMs delegate to specialized engines. Clean separation of concerns.\n"
"\n"
"**The LLM decides, the code executes " + EM + " routing intent to deterministic engines.**\n"
"\n"
"Each capability is a JSON-Schema tool definition (name, description, typed parameters) backed by a plain Python function in `execute_tool()`. The model selects the tool and fills the arguments; the engine returns ground truth; unknown tools fail gracefully. Separation of concerns is the payoff: prompts can change without touching the scorers, and the scorers can be tested without the model.\n"
"\n"
"Tool calling is the orchestration pattern Ch. 60 puts to work, where the LLM rewrites only the bullets the rule-based scorer flags as weak."
),
}

# ---------------------------------------------------------------- 60
p60 = BJ + r"\60_weak_bullet_rewriter\60.ipynb"
r60 = {
0: (
"# 60 " + EM + " Weak Bullet Rewriter\n"
"**Goal:** Selectively rewrite only low-scoring resume bullets using LLM.\n"
"\n"
"Ch. 37 built a STAR scorer; this chapter adds the LLM as a **surgical editor**: score every bullet, send only the weak ones to the model, keep the strong ones verbatim, and let a human accept or reject each rewrite. The LLM is not rewriting the resume " + EM + " it is proposing fixes for the bullets that need them.\n"
"\n"
"**Why it matters for resumes / ATS:** rewriting everything costs money and, worse, erases the candidate's voice. Selective rewriting spends LLM budget only where the rule-based scorer found measurable weakness, so the output stays authentic where it was already good " + EM + " and the accept/reject step keeps a human in the loop over text that will represent a real person."
),
1: (
"## 1. Detection-First Strategy\n"
"\n"
"The pipeline is deliberately asymmetric: cheap deterministic scoring runs on **every** bullet; expensive LLM rewriting runs on **few**. Score with the Ch. 37 STAR scorer, send only bullets below the threshold (here `< 0.5`), preserve the rest, then review proposed changes.\n"
"\n"
"**What the code does:** prints the five-step pipeline (score " + EM + " filter " + EM + " rewrite " + EM + " preserve " + EM + " review) and its three motivations:\n"
"- **Cost-effective** " + EM + " the notebook estimates only ~40% of bullets typically need rewriting, so the LLM bill roughly halves.\n"
"- **Preserves authentic writing** " + EM + " strong bullets keep the candidate's original words.\n"
"- **Focuses the LLM** " + EM + " model effort lands where it measurably adds value.\n"
"\n"
"The threshold is the knob: lower it and you save money but ship weaker text; raise it and quality improves at linear cost."
),
3: (
"## 2. Bullet Scoring + Selective Rewrite\n"
"\n"
"`score_bullet()` is a transparent 0" + EM + "1 heuristic: three independent quality signals, each adding a fixed amount, capped at 1.0. No model, no magic " + EM + " a recruiter can read why a bullet scored low.\n"
"\n"
"**What the code does:**\n"
"- `+0.3` if the first word is in `ACTION_VERBS` (`developed`, `led`, `reduced`, ...) " + EM + " the single strongest signal of a good bullet.\n"
"- `+0.3` if the text contains a quantified result " + EM + " regex for `%`, `million`, `billion`, `$`.\n"
"- `+0.15` if a tool is mentioned after `using`/`with`/`via` + a capital letter.\n"
"\n"
"**Expected (verified by running):** all three sample bullets score below the 0.5 threshold (`0.30`, `0.00`, `0.00`), so all are sent to the LLM " + EM + " including \"Reduced model latency by 40% through TensorFlow optimization\". The reason is a live bug: the regexes are written `r\"\\\\d+\\\\s*(%|million|billion|\\\\$)\"` and `r\"(using|with|via)\\\\s+[A-Z]\"`, where the doubled backslash in a raw string means a *literal backslash* " + EM + " so the quantified-result and tool-mention checks never fire, and the strongest bullet scores 0.30. With the intended `\\d`/`\\s` patterns it would score 0.75 and be skipped. A scoring bug that under-scores is cheap; one that over-scores ships bad text."
),
5: (
"## 3. LLM Rewrite Prompt\n"
"\n"
"The rewrite prompt is the whole product in one template: it states the output contract (STAR), the style constraints (strong verb, quantified result, specific technology), and the input slot. Nothing else " + EM + " no examples here, because Ch. 56 showed few-shot belongs in the template registry, and this prompt is short enough to inline.\n"
"\n"
"**What the code does:** defines `BULLET_REWRITE_PROMPT` with an `{bullet}` slot, prints \"Prompt template ready.\", and prints an example rewrite in the source (`Architected and deployed ML models achieving 95% accuracy, reducing manual review time by 40% using TensorFlow`).\n"
"\n"
"**Expected (with a key):** sending \"Was responsible for ML model development\" through the template returns a rewritten bullet that starts with an action verb and carries a quantified result " + EM + " the exact transformation Ch. 56's `bullet_rewrite` template demonstrated. Without a key the cell is inert by design: it documents the contract rather than calling the API."
),
7: (
"## Summary: Selective rewriting cuts costs and preserves authentic writing. Only rewrite what's weak.\n"
"\n"
"**Detect cheap, rewrite rarely " + EM + " the LLM edits only where the scorer found weakness.**\n"
"\n"
"Rule-based scoring filters every bullet; the model rewrites only those under threshold; humans accept or reject each proposal. That asymmetry keeps the LLM bill proportional to the *problem*, not the resume length, and preserves authentic writing in the bullets that were already strong.\n"
"\n"
"The rewrites this chapter proposes are generated in STAR shape " + EM + " which is exactly the format Ch. 61 industrializes, generating full STAR bullets from raw experience data."
),
}

# ---------------------------------------------------------------- 61
p61 = BJ + r"\61_star_bullet_generator\61.ipynb"
r61 = {
0: (
"# 61 " + EM + " STAR Bullet Generator\n"
"**Goal:** Generate STAR-format resume bullets from minimal input.\n"
"\n"
"Ch. 60 rewrote existing bullets; this chapter generates them from scratch. Given a role, company, duration, and a one-line context, the LLM produces three STAR-compliant bullets " + EM + " each with a strong action verb, a quantified result, and a different angle (technical, leadership, process). The output parser then turns the model's numbered list into clean bullet strings.\n"
"\n"
"**Why it matters for resumes / ATS:** candidates who \"did things\" rarely know how to say it " + EM + " the gap between \"Built ML models\" and \"Developed production NLP models at Google processing 10M+ daily queries, reducing response latency by 35%\" is exactly what an ATS scores on. STAR generation closes that gap automatically and consistently, which is also why every generated bullet is *required* to carry a metric."
),
1: (
"## 1. STAR Structure\n"
"\n"
"STAR is a four-slot template for a single bullet: **Situation** (context: team size, scope, timeframe), **Task** (what needed doing), **Action** (what *you* did " + EM + " the verb), **Result** (quantified outcome: %, $, time saved). In practice the four slots compress into one dense sentence " + EM + " the Situation and Task anchor it, the Action verb leads it, the Result closes it with a number.\n"
"\n"
"**What the code does:** prints the four components and demonstrates the compression on raw input: `\"Built ML models at Google\"` " + EM + " a fully-formed bullet that injects `(T)` for the task (\"production ML models\"), `(S)` for the context (\"at Google\"), `(A)` for the tooling (\"using TensorFlow\"), and `(R)` twice for results (\"95% accuracy\", \"10M+ daily predictions\"). Note the ordering " + EM + " the ATS reads action first, so the verb leads even though STAR spells Situation first."
),
3: (
"## 2. Generator Prompt Template\n"
"\n"
"`STAR_PROMPT` is a `.format()`-able template: four named slots (`role`, `company`, `duration`, `context`) plus four hard requirements " + EM + " every bullet starts with a strong action verb, every bullet includes a quantified result, STAR is used *naturally within* each bullet (not as labeled sections), and the three bullets cover different aspects: technical achievement, leadership, and process improvement.\n"
"\n"
"**What the code does:**\n"
"- The template ends with `Generate exactly 3 bullets:` " + EM + " the count constraint is explicit because \"exactly\" is the only way to get a predictable number back.\n"
"- `experience` holds the sample record (`Senior Data Scientist`, `Google`, `2020-2023`, NLP-team context) and `STAR_PROMPT.format(**experience)` fills the slots.\n"
"\n"
"**Expected (verified by running):** the printed prompt is the full template with the four fields substituted. **With a key**, the model is expected to return exactly three numbered bullets " + EM + " one technical, one leadership, one process, each with a metric; the \"different aspects\" requirement exists to stop the model from generating three near-duplicates."
),
5: (
"## 3. Output Parser\n"
"\n"
"Models return numbered lists; the pipeline needs plain bullets. `parse_star_bullets()` filters the response to list-like lines and strips the leading markers " + EM + " with two caveats worth knowing.\n"
"\n"
"**What the code does:**\n"
"- Keeps only non-empty lines that start with a digit, `-`, or `*` " + EM + " this is what drops the model's preamble (\"Here are your bullets:\") and trailing commentary.\n"
"- Strips leading markers with `re.sub(r\"^[\\\\d\\\\.\\\\s\\\\-\\\\*]+\", \"\", b)` and drops anything shorter than 20 chars.\n"
"\n"
"**Expected (verified by running):** on the three-bullet sample the parser returns all three lines " + EM + " *including* the `1. `, `2. `, `3. ` prefixes, because the regex's `\\\\d` is a doubled backslash in a raw string (a literal backslash, not a digit class), so the numbering is never stripped. The `len(b) > 20` filter hides the damage, but the prefixes still leak into the final bullets; the intended pattern is `r\"^[\\d.\\s\\-\\*]+\"`. Also note the cell uses `re` without importing it " + EM + " run it in a kernel that already has `re` (e.g. after Ch. 60) or it raises `NameError`."
),
7: (
"## Summary: STAR generator turns raw experience into quantified, impactful bullets. Always require metrics.\n"
"\n"
"**A metric per bullet " + EM + " the number is what makes a claim verifiable.**\n"
"\n"
"Given role, company, duration, and context, the generator produces three bullets that each start with an action verb, embed STAR naturally, and carry a quantified result " + EM + " and the parser turns the model's numbered output into clean strings. Requiring a metric on every bullet is the guardrail: it forces the model to invent (or at least commit to) a number, which is exactly what ATS scoring and human recruiters reward.\n"
"\n"
"This chapter's generation machinery feeds Ch. 62, where the same LLM turns a full resume + JD analysis into role-aware career advice."
),
}

# ---------------------------------------------------------------- 62
p62 = BJ + r"\62_career_advisor\62.ipynb"
r62 = {
0: (
"# 62 " + EM + " Career Advisor\n"
"**Goal:** Generate role-aware career guidance from resume + JD analysis.\n"
"\n"
"Earlier chapters asked *\"how well does this resume fit this job?\"*; this chapter asks *\"what should this person do next?\"* The advisor combines the data-driven layers of the stack " + EM + " resume parsing, skill-gap analysis against a target role (Ch. 53) " + EM + " with LLM-generated natural-language recommendations, so the advice is grounded in the candidate's actual skills rather than generic career platitudes.\n"
"\n"
"**Why it matters for resumes / ATS:** a score tells a candidate they are 50% matched; a recommendation tells them what to learn, what to certify, and what to build. That coaching layer is what turns an ATS from a gatekeeper into a service " + EM + " and it only works if every suggestion traces back to a real gap in the data."
),
1: (
"## 1. Advisor Architecture\n"
"\n"
"The pipeline is a straight line with one branch: **parse** the resume into a structured schema, **analyze** skill gaps against the target role (reusing the Ch. 53 machinery), **generate** recommendations, and only then hand the results to the LLM for natural-language phrasing " + EM + " every LLM claim is grounded in computed facts.\n"
"\n"
"**What the code does:** prints the five-stage pipeline:\n"
"1. Parse resume " + EM + " structured `ResumeSchema`\n"
"2. Analyze skill gaps vs target role (Notebook 53)\n"
"3. Generate recommendations " + EM + " skill gaps to fill, certifications, project ideas, career trajectories\n"
"4. Use the LLM for natural language\n"
"5. Ground everything in real data (skills, experience)\n"
"\n"
"The ordering is the point: recommendations come from the *analysis*, and the LLM is the last stage, not the first " + EM + " put the model first and the advice drifts from the resume."
),
3: (
"## 2. Recommendation Builder\n"
"\n"
"`CareerAdvisor` is the deterministic core: a small knowledge base of career paths, each with `core` and `nice` skill lists, and an `analyze()` method that diffs the candidate's skills against the target path " + EM + " no LLM required for the gap computation itself.\n"
"\n"
"**What the code does:**\n"
"- `career_paths` " + EM + " three roles (`data_scientist`, `ml_engineer`, `nlp_engineer`), each with core and nice-to-have skills; an unknown role returns `{}`, which yields empty gaps instead of a crash.\n"
"- `analyze(resume_skills, target_role)` " + EM + " computes `core_gaps` (missing essentials) and `nice_gaps` (missing optional), then maps them to recommendations: `\"Learn {gap}\"` for core gaps (blockers), `\"Consider {gap}\"` for nice gaps (optional) " + EM + " the verb encodes priority.\n"
"\n"
"**Expected (verified by running):** with `[\"Python\", \"NLP\"]` targeting `ml_engineer`, the output is `Core gaps: ['MLOps', 'Docker']`, `Nice-to-have: ['Kubernetes', 'CI/CD']`, and four recommendations " + EM + " `Learn MLOps`, `Learn Docker`, `Consider Kubernetes`, `Consider CI/CD`. The split is deliberate: learn the blockers, consider the differentiators."
),
5: (
"## 3. LLM-Enhanced Recommendations\n"
"\n"
"The deterministic gaps from section 2 are *data*; the LLM turns them into *advice*. The prompt contract is a three-part structure: a **system role** (career coach for data professionals), a **context block** with the computed facts (`role`, `skills`, `gaps`, `target_role`), and a **structured output spec** " + EM + " three quick wins, two strategic moves, one moonshot.\n"
"\n"
"**What the code does:** prints the prompt template, which follows Ch. 56's five-component pattern: system, context, and output format " + EM + " and deliberately *no* few-shot examples, because career advice is open-ended and the numbered output spec (`1. ... 2. ... 3. ...`) is the only structure needed.\n"
"\n"
"**Expected (with a key):** the call is expected to return exactly three numbered quick wins (skills learnable in under a month, derived from the gaps), two strategic moves (certifications, projects), and one long-term moonshot " + EM + " the same `gaps` dict that produced `Learn MLOps` now appears as fluent prose, grounded in the same data."
),
7: (
"## Summary: Career advisor combines data-driven gap analysis with LLM-generated natural language recommendations.\n"
"\n"
"**Compute the gaps deterministically; let the LLM write the advice " + EM + " never the reverse.**\n"
"\n"
"`CareerAdvisor.analyze()` produces the facts (core vs nice gaps, Learn vs Consider recommendations) from a small career-path knowledge base, and the LLM only rephrases those facts into structured coaching output (quick wins, strategic moves, moonshot). Because the model never computes the gaps, the advice cannot hallucinate them " + EM + " it can only embellish what the data already said.\n"
"\n"
"This chapter feeds Ch. 63, where the block's model choices are stress-tested: the same resume tasks are compared across models on quality, cost, and latency."
),
}

# ---------------------------------------------------------------- 63
p63 = BJ + r"\63_model_comparison\63.ipynb"
r63 = {
0: (
"# 63 " + EM + " Model Comparison\n"
"**Goal:** Compare LLM models on resume tasks " + EM + " quality, cost, and speed.\n"
"\n"
"Eight chapters of LLM engineering have assumed a model choice; this chapter makes the choice **evidence-based**. It lays out the evaluation dimensions that matter for resume tasks, prints a comparison matrix, and distills the results into per-task recommendations " + EM + " the payoff of Ch. 55's tier system, now backed by numbers instead of vibes.\n"
"\n"
"**Why it matters for resumes / ATS:** model choice is a real cost line once resumes scale. The cheapest model that hits your extraction accuracy target at your latency budget is the one to ship " + EM + " and \"cheapest\" is only knowable if you benchmark on *your* tasks, because leaderboard rankings do not transfer to niche resume formats."
),
1: (
"## 1. Evaluation Framework\n"
"\n"
"The comparison has five dimensions, and all five are *task-specific*: a model can be excellent at creative generation and mediocre at structured extraction. **Accuracy** (does extraction match ground truth?), **Consistency** (same input, same output?), **Cost** (dollars per 1K calls), **Latency** (time to first token), and **Context window** (can it hold a full resume?).\n"
"\n"
"**What the code does:** prints those five dimensions plus the four resume tasks worth benchmarking: skill extraction (structured output), bullet rewriting (generation), section classification (routing), and STAR generation (creative). The pairing matters " + EM + " a task and a dimension only mean something together: e.g. consistency matters most for classification, latency matters most for interactive rewriting, context window matters for whole-resume analysis."
),
3: (
"## 2. Building a Comparison Matrix\n"
"\n"
"The matrix is the block's one-stop decision table: rows are models, columns are the five dimensions, and the printout formats them into a readable grid. **Caveat up front:** the numbers in this cell are hard-coded example data (the comment says so), not measured results " + EM + " treat them as illustrative and re-benchmark on your own golden set before choosing.\n"
"\n"
"**What the code does:**\n"
"- `comparison` dict " + EM + " three models (`gpt-4o-mini`, `claude-3-haiku`, `mistral-small`) with `extraction_f1`, `rewrite_quality`, `cost_per_1k`, `latency_ms`, `context` values.\n"
"- The f-string header plus a loop prints one aligned row per model.\n"
"\n"
"**Expected (verified by running):** the printed grid shows `gpt-4o-mini 0.94 F1, 4.2/5, $0.15, 800ms, 128k context`; `claude-3-haiku 0.93 F1, 4.0/5, $0.25, 600ms, 200k context`; `mistral-small 0.89 F1, 3.5/5, $0.05, 400ms, 32k context`. Read it as a trade-off surface, not a ranking: the cheapest model is also the slowest on quality, and the cheapest per call (mistral) has the smallest context window."
),
5: (
"## 3. Recommendation by Task\n"
"\n"
"A single winner is the wrong question " + EM + " the right question is *which model for which task*. This cell prints a recommendation matrix that routes each of the five resume workloads to its best model and runner-up.\n"
"\n"
"**What the code does:** prints the matrix, which pairs tasks with winners: skill extraction " + EM + " GPT-4o-mini (runner-up Mistral Small); bullet rewrite " + EM + " Claude 3 Haiku; STAR generation " + EM + " GPT-4o-mini; classification " + EM + " Mistral Small; career advice " + EM + " GPT-4o-mini. It closes with the rule of thumb: `GPT-4o-mini is the best all-rounder for resume tasks`, with `Mistral Small` for batch classification (cheap, fast).\n"
"\n"
"**Why it matters:** this matrix is exactly what Ch. 55's `pick_model()` encodes as tiers " + EM + " the `cheap` tier serves classification, `balanced` serves extraction and rewriting, `best` serves generation " + EM + " so the policy in code and the benchmark here agree by construction."
),
7: (
"## Summary: Benchmark models on your specific tasks. Don't assume " + EM + " measure cost, quality, and latency.\n"
"\n"
"**The cheapest model that meets your accuracy bar on *your* tasks is the right model " + EM + " measure, don't assume.**\n"
"\n"
"Five dimensions (accuracy, consistency, cost, latency, context) across four resume tasks, summarized into a per-task recommendation matrix that mirrors Ch. 55's tier policy: cheap models for classification, balanced for extraction and rewriting, flagship for generation. The example data is illustrative, but the method is the deliverable " + EM + " a golden set, a matrix, and a routing rule.\n"
"\n"
"This chapter closes the LLM engineering block; Ch. 64 (Precision and Recall for NLP) turns the qualitative \"accuracy\" dimension into proper evaluation metrics for the extraction tasks built here."
),
}

REPLACE = {}
for nb, r in [(p55, r55), (p56, r56), (p57, r57), (p58, r58), (p59, r59),
              (p60, r60), (p61, r61), (p62, r62), (p63, r63)]:
    REPLACE[nb] = r

if __name__ == "__main__":
    for nb, r in REPLACE.items():
        res = apply(nb, replace=r)
        print(nb.split("\\")[-2], "->", json.dumps(res))
    # verify
    for nb in REPLACE:
        d = load(nb)
        md = [c for c in d["cells"] if c["cell_type"] == "markdown"]
        short = [i for i, c in enumerate(d["cells"]) if c["cell_type"] == "markdown" and len("".join(c["source"])) < 300]
        print(nb.split("\\")[-2], "md cells:", len(md), "short(<300):", short)
