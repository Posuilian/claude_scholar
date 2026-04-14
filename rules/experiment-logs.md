# Glob: results/** experiments/** logs/**

## Experiment Log Standards

### Core Rule

- **APPEND-ONLY** — never modify or delete historical experiment records
- Each record is immutable once written
- If an experiment was wrong, add a new note explaining why — do not edit the original

### Required Fields Per Experiment

Every experiment log entry must include:

1. **Timestamp**: ISO 8601 format (`2024-03-15T14:30:00`)
2. **Config snapshot**: Full path to the config file used, or inline config dump
3. **Git state**: Commit hash + whether working directory was clean
4. **Key metrics**: The primary metrics being tracked (loss, accuracy, FID, etc.)
5. **Brief conclusion**: 1-2 sentences on what this experiment showed

### File Naming

- Format: `{experiment-name}_{YYYYMMDD}_{HHMMSS}.md`
- Or use a single `experiment-log.md` with chronological entries separated by `---`

### Comparison Format

When comparing with baselines, use a markdown table:

```markdown
| Method | Metric-1 | Metric-2 | Notes |
|--------|----------|----------|-------|
| Baseline | ... | ... | ... |
| Ours (exp-name) | ... | ... | ... |
```
