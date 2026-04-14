---
name: experiment-tracking
description: Standards for logging and tracking experiments
user-invocable: false
---

# Experiment Tracking Standards

## Pre-Experiment Setup

Before running any experiment, capture:

```bash
# 1. Git state
git rev-parse HEAD          # commit hash
git status --short          # working directory status
git diff --stat             # uncommitted changes summary

# 2. Environment
python --version
pip list | grep -E "torch|transformers|accelerate|numpy"  # key packages
nvidia-smi --query-gpu=name,memory.total --format=csv     # GPU info

# 3. Config validation
# Verify the config file is valid YAML/JSON and all paths exist
```

## Experiment Log Format

Each experiment record in `results/` should follow this structure:

```markdown
# Experiment: {experiment-name}
Date: {YYYY-MM-DD HH:MM}
Git Commit: {hash} (clean: yes/no)
Config: {path-to-config-file}

## Setup
- GPU: {gpu-type} x {count}
- Training time: {hours}h {minutes}m
- Effective batch size: {batch_size * grad_accum * gpu_count}

## Config Summary
{Key hyperparameters in table format}

## Results

### Primary Metrics
| Metric | Value |
|--------|-------|
| ... | ... |

### Training Curve Notes
- Converged at epoch: ...
- Final train loss: ...
- Best validation score at epoch: ...

## Comparison with Baselines
| Method | Metric-1 | Metric-2 | Notes |
|--------|----------|----------|-------|
| Baseline | ... | ... | paper-reported |
| Ours | ... | ... | this run |

## Observations
- [What worked, what didn't, surprising findings]

## Next Steps
- [What to try next based on these results]
```

## File Naming

- Single experiment: `results/{exp-name}_{YYYYMMDD}.md`
- Experiment series: `results/{series-name}/run_{NNN}.md`

## Quick Comparison Script

When comparing multiple experiments, generate a summary table:

```markdown
# Experiment Comparison: {series-name}

| Run | Date | Key Change | Metric-1 | Metric-2 | Notes |
|-----|------|-----------|----------|----------|-------|
| run_001 | ... | baseline | ... | ... | ... |
| run_002 | ... | +augment | ... | ... | ... |
| run_003 | ... | +lr-decay | ... | ... | ... |
```

## Rules

- NEVER modify an existing experiment record — create a new entry or add a correction note
- ALWAYS save the full config, not just the diff from default
- If a run crashes, still log it with the error message and partial results
- Tag failed runs clearly: `Status: FAILED — {reason}`
