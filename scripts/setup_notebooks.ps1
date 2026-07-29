$basePath = $PSScriptRoot + "\.."

# ── Part 1: Foundations & NLP Mastery ────────────────────────
$part1 = @(
    "part1_foundations/block_a/00_environment_setup",
    "part1_foundations/block_a/01_python_refresher",
    "part1_foundations/block_a/02_pandas_numpy",
    "part1_foundations/block_a/03_regex_mastery",
    "part1_foundations/block_b/04_nlp_introduction",
    "part1_foundations/block_b/05_tokenization",
    "part1_foundations/block_b/06_text_normalization",
    "part1_foundations/block_b/07_stop_words",
    "part1_foundations/block_b/08_lemmatization",
    "part1_foundations/block_b/09_stemming",
    "part1_foundations/block_b/10_pos_tagging",
    "part1_foundations/block_b/11_dependency_parsing",
    "part1_foundations/block_b/12_named_entity_recognition",
    "part1_foundations/block_c/13_chunking_phrase_extraction",
    "part1_foundations/block_c/14_keyword_extraction",
    "part1_foundations/block_c/15_bag_of_words",
    "part1_foundations/block_c/16_tfidf",
    "part1_foundations/block_c/17_ngrams",
    "part1_foundations/block_c/18_cosine_similarity",
    "part1_foundations/block_c/19_word2vec",
    "part1_foundations/block_c/20_fasttext",
    "part1_foundations/block_d/21_glove",
    "part1_foundations/block_d/22_sentence_transformers",
    "part1_foundations/block_d/23_embedding_benchmarks",
    "part1_foundations/block_d/24_zero_shot_classification",
    "part1_foundations/block_d/25_error_handling_nlp"
)

# ── Part 2: Resume & Job Intelligence ─────────────────────────
$part2 = @(
    "part2_intelligence/block_e/26_pdf_parsing",
    "part2_intelligence/block_e/27_docx_parsing",
    "part2_intelligence/block_e/28_ocr_basics",
    "part2_intelligence/block_e/29_text_normalization_resumes",
    "part2_intelligence/block_e/30_language_detection",
    "part2_intelligence/block_e/31_parsing_error_handling",
    "part2_intelligence/block_f/32_section_detection",
    "part2_intelligence/block_f/33_skill_extraction_rules",
    "part2_intelligence/block_f/34_skill_normalization_engine",
    "part2_intelligence/block_f/35_education_parsing",
    "part2_intelligence/block_f/36_experience_parsing",
    "part2_intelligence/block_f/37_bullet_parsing_star_scoring",
    "part2_intelligence/block_f/38_project_extraction",
    "part2_intelligence/block_f/39_resume_json_schema",
    "part2_intelligence/block_g/40_jd_parsing",
    "part2_intelligence/block_g/41_jd_skill_extraction",
    "part2_intelligence/block_g/42_responsibility_detection",
    "part2_intelligence/block_g/43_qualification_detection",
    "part2_intelligence/block_g/44_keyword_ranking",
    "part2_intelligence/block_g/45_requirement_classification",
    "part2_intelligence/block_h/46_resume_vs_jd_matching",
    "part2_intelligence/block_h/47_faiss",
    "part2_intelligence/block_h/48_chromadb",
    "part2_intelligence/block_h/49_embedding_evaluation",
    "part2_intelligence/block_i/50_ats_rule_design",
    "part2_intelligence/block_i/51_explainable_scoring",
    "part2_intelligence/block_i/52_ats_simulation_mode",
    "part2_intelligence/block_i/53_skill_gap_analysis",
    "part2_intelligence/block_i/54_resume_ranking"
)

# ── Part 3: LLM Engineering & Production ──────────────────────
$part3 = @(
    "part3_production/block_j/55_openrouter_setup",
    "part3_production/block_j/56_prompt_engineering",
    "part3_production/block_j/57_prompt_versioning",
    "part3_production/block_j/58_json_structured_output",
    "part3_production/block_j/59_function_tool_calling",
    "part3_production/block_j/60_weak_bullet_rewriter",
    "part3_production/block_j/61_star_bullet_generator",
    "part3_production/block_j/62_career_advisor",
    "part3_production/block_j/63_model_comparison",
    "part3_production/block_k/64_precision_recall",
    "part3_production/block_k/65_f1_confusion_matrix",
    "part3_production/block_k/66_hallucination_testing",
    "part3_production/block_k/67_ab_prompt_testing",
    "part3_production/block_k/68_human_evaluation",
    "part3_production/block_k/69_latency_profiling",
    "part3_production/block_l/70_end_to_end_pipeline",
    "part3_production/block_l/71_pipeline_config_pattern",
    "part3_production/block_l/72_caching_layer",
    "part3_production/block_l/73_feedback_loop",
    "part3_production/block_l/74_modularization",
    "part3_production/block_l/75_api_prototype"
)

$allDirs = $part1 + $part2 + $part3

foreach ($rel in $allDirs) {
    $full = Join-Path $basePath "notebooks\$rel"
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Force -Path $full | Out-Null
    }
    $gk = Join-Path $full ".gitkeep"
    if (-not (Test-Path $gk)) {
        New-Item -ItemType File -Force -Path $gk | Out-Null
    }
}

# Shared assets dir
$assetsPath = Join-Path $basePath "notebooks\assets"
if (-not (Test-Path $assetsPath)) {
    New-Item -ItemType Directory -Force -Path $assetsPath | Out-Null
    New-Item -ItemType File -Force -Path (Join-Path $assetsPath ".gitkeep") | Out-Null
}

Write-Host "Notebook directories created: $($allDirs.Count + 1) total"
