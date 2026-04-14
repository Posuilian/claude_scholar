# CLAUDE.md

## Project Structure

Standard directory layout for research projects:

```
project/
├── src/              # Source code (models, training, evaluation)
├── configs/          # Experiment configurations (YAML)
├── data/             # Datasets (READ-ONLY — never modify via Claude)
├── checkpoints/      # Model weights (READ-ONLY — never delete)
├── results/          # Experiment results (APPEND-ONLY)
├── scripts/          # Shell scripts for job submission
├── notes/            # Paper analysis and research notes
└── tests/            # Unit tests
```

## Code Standards

- All functions must have docstrings (Google style)
- Use type hints for function signatures
- Hyperparameters come from config files, never hardcoded
- Use `logging` module, not `print()`, for experiment output
- Import order: stdlib → third-party → local (separated by blank lines)

## Experiment Management

- Config format: YAML files in `configs/`
- Naming: `{model}_{dataset}_{date}_{brief-description}`
- Every experiment must log: git commit hash, full config, hardware info
- Results are append-only — never modify historical records

## Data Safety

- **NEVER** modify, delete, or overwrite files in `data/`, `checkpoints/`, or `weights/`
- Before modifying training code, read and understand the full training loop first
- Before modifying configs, check which experiments depend on them

## Context Management

- Perform `/compact` at ~50% context usage
- Before compacting: save important conclusions to this CLAUDE.md
- After plan discussions: extract decisions into this file, then compact
- Pattern: discuss → decide → write to CLAUDE.md → /compact → execute

## Key Commands

- `/read-paper [url-or-path]` — Analyze a research paper
- `/reproduce-check` — Compare paper claims with code implementation
- `/run-experiment [config-path]` — Execute experiment with auto-logging

## Project-Specific

<!-- Fill in when you start a new project -->
<!-- Example entries: -->
<!-- - Framework: PyTorch 2.x + Accelerate -->
<!-- - Task: Image generation / NLP / RL / etc. -->
<!-- - Key baselines: ... -->
<!-- - Evaluation metrics: ... -->
<!-- - Cluster: SLURM / PBS / local -->
