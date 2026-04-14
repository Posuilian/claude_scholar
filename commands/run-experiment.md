---
description: "Execute an experiment with proper config validation, logging, and result tracking"
argument-hint: "[config-path]"
allowed-tools: Read, Write, Edit, Bash, Agent, Glob
---

# Run Experiment Workflow

You are orchestrating an experiment execution workflow.

## Steps

### Step 1: Get the config

The user should provide a config file path as the argument: `$ARGUMENTS`

If no argument was provided, ask the user:
- "Please provide the path to your experiment config file (YAML or JSON)."

### Step 2: Validate before running

Before launching the experiment, perform these checks yourself:
1. Read and validate the config file
2. Check that data paths in the config actually exist
3. Run `nvidia-smi` to verify GPU availability
4. Run `git status` to check if the working directory is clean
5. Record the git commit hash

If anything fails, report to the user and ask how to proceed.

### Step 3: Confirm with user

Show the user a summary of what will be executed:
- Config file path and key hyperparameters
- Expected GPU usage
- Git state
- Estimated runtime (if determinable from config)

Ask: "Ready to launch? (Describe any modifications needed, or confirm to proceed)"

### Step 4: Execute

Launch the `experiment-runner` agent:

```
Agent(subagent_type="experiment-runner", description="Run experiment", prompt="Execute the experiment with config at {config_path}. Git commit: {commit_hash}. Follow the experiment-tracking standards for all logging. Save results to results/ directory.")
```

### Step 5: Record results (in Chinese)

After the experiment completes:
1. Verify the results were saved properly in `results/`
2. Present a summary to the user: key metrics, runtime, any issues encountered
3. If there are existing results to compare against, generate a comparison table
