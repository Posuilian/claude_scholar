---
description: "Compare paper claims with code implementation — find discrepancies and undocumented tricks"
allowed-tools: Read, WebFetch, Agent, Write, Glob
---

# Reproduce Check Workflow

You are orchestrating a paper-to-code comparison workflow.

## Steps

### Step 1: Gather inputs

Ask the user for TWO pieces of information:
1. **Paper location**: URL (arXiv, PDF) or local file path
2. **Code location**: Local directory path containing the implementation

If the user provided arguments, parse them: `$ARGUMENTS`

### Step 2: Analyze the paper

Launch the `paper-analyst` agent to extract the method description:

```
Agent(subagent_type="paper-analyst", description="Extract method details from paper", prompt="Analyze this paper with a focus on extractable implementation details — architecture, loss functions, training strategy, data pipeline. Paper: {paper_location}")
```

Save the agent's output for the next step.

### Step 3: Analyze the code

Launch the `code-explorer` agent to understand the implementation:

```
Agent(subagent_type="code-explorer", description="Analyze code implementation", prompt="Explore this codebase thoroughly. Trace the full pipeline: data loading → model architecture → loss computation → training loop → evaluation. Focus on extracting concrete implementation details that can be compared with a paper. Code directory: {code_location}")
```

Save the agent's output for the next step.

### Step 4: Generate comparison report (in Chinese)

Using the outputs from both agents, generate a structured comparison report:

1. Create a difference table for each dimension (architecture, loss, training, data, evaluation)
2. List undocumented tricks found in code
3. List things described in paper but missing from code
4. Provide an overall reproducibility risk assessment

Save the report to `notes/reproduce-check/` directory:
- Filename: `{paper-short-name}_vs_{repo-name}_{date}.md`
- If the directory doesn't exist, create it

### Step 5: Summary

Present the key findings to the user (in Chinese):
1. Number of discrepancies found (high/medium/low impact)
2. Top 3 most critical differences
3. Undocumented tricks that could affect reproduction
4. Path to the full comparison report
