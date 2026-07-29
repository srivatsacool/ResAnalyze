$dirs = @(
    "docs/architecture", "docs/api", "docs/deployment", "docs/research", "docs/diagrams", "docs/references", "docs/images",
    "notebooks/00_environment_setup", "notebooks/01_python_refresh", "notebooks/02_data_preprocessing", "notebooks/03_regex",
    "notebooks/04_nlp_basics", "notebooks/05_vectorization", "notebooks/06_embeddings", "notebooks/07_resume_parsing",
    "notebooks/08_job_description", "notebooks/09_similarity", "notebooks/10_skill_extraction", "notebooks/11_ats_scoring",
    "notebooks/12_resume_rewriting", "notebooks/13_llm_experiments", "notebooks/14_evaluation", "notebooks/15_complete_pipeline",
    "notebooks/assets",
    "datasets/raw", "datasets/processed", "datasets/external", "datasets/resume", "datasets/jobs", "datasets/skills",
    "datasets/universities", "datasets/companies", "datasets/certifications", "datasets/locations",
    "experiments", "prompts", "backend", "frontend", "mcp", "deployment", "docker", "evaluation", "tests", "scripts", "shared"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $gitkeep = Join-Path $dir ".gitkeep"
    if (-not (Test-Path $gitkeep)) {
        New-Item -ItemType File -Force -Path $gitkeep | Out-Null
    }
}

Write-Host "Directory structure created successfully!"
