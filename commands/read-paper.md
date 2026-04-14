---
description: "Analyze a research paper — extract methods, contributions, and implementation details"
argument-hint: "[local-pdf-path]"
allowed-tools: Agent, Write
---

# Read Paper Workflow

You are orchestrating a paper analysis workflow.

## Steps

### Step 1: Get the paper

The user should provide a local PDF file path as the argument: `$ARGUMENTS`

If no argument was provided, ask the user:
- "Please provide the local PDF file path (use wget/curl to download first if needed)."

### Step 2: Analyze the paper

Launch the `paper-analyst` agent to read and analyze the PDF:

```
Agent(subagent_type="paper-analyst", description="Analyze research paper", prompt="Read and analyze the following PDF paper using your pdf skill and paper-reading methodology. PDF path: $ARGUMENTS")
```

### Step 3: Save results (in Chinese)

Translate the agent's analysis into Chinese, then save to `notes/paper-analysis/` directory:
- Filename: `{first-author}_{year}_{short-title}.md`
- If the `notes/paper-analysis/` directory doesn't exist, create it
- The entire analysis document must be written in Chinese (including section headings)
- Keep technical terms, model names, dataset names, and equations in their original English form

### Step 4: Summary

Present a brief summary to the user (in Chinese):
1. One-sentence summary of the paper
2. Core contribution
3. Key concerns or notes for reproduction
4. Path to the saved analysis file
