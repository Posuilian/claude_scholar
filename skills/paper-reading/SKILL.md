---
name: paper-reading
description: Methodology for analyzing research papers
user-invocable: false
---

# Paper Reading Methodology

## Analysis Framework

When analyzing a research paper, follow this structured approach:

### Step 1: High-Level Understanding (2 min)
- Read title, abstract, and conclusion first
- Identify: What problem? What approach? What claim?

### Step 2: Method Deep-Dive
Extract the following in order:

1. **Problem formulation**: Mathematical definition of the task (input → output)
2. **Architecture**: Network structure, key modules, dimensions
3. **Loss function**: Exact loss terms, weighting, any auxiliary losses
4. **Training strategy**: Optimizer, scheduler, batch size, epochs, warmup
5. **Data pipeline**: Augmentations, preprocessing, dataset splits
6. **Inference details**: Any test-time tricks (TTA, ensembling, post-processing)

### Step 3: Critical Analysis

Look specifically for:
- **Claim vs evidence gaps**: Are all claims supported by experiments?
- **Missing ablations**: Which components are NOT ablated?
- **Hidden tricks**: Footnotes, appendix details, "we found that..." phrases
- **Reproducibility concerns**: Missing hyperparameters, vague descriptions
- **Unfair comparisons**: Different backbones, training data, or compute budgets vs baselines

### Step 4: Implementation Notes

Extract details that matter for reproduction:
- Exact layer configurations (not just "ResNet backbone")
- Initialization methods
- Gradient clipping, weight decay, specific optimizer settings
- Any data filtering or cleaning mentioned

## Output Format

```markdown
# Paper Analysis: [Title]

## One-Sentence Summary
[What this paper does in one sentence]

## Problem
[Mathematical formulation or clear description]

## Core Method
[Key architectural/algorithmic contribution]

## Loss Function
[Exact loss formulation with all terms]

## Training Details
| Parameter | Value |
|-----------|-------|
| Optimizer | ... |
| Learning rate | ... |
| Batch size | ... |
| Epochs | ... |
| ... | ... |

## Key Results
[Main quantitative results, with comparison to baselines]

## Critical Notes
- [Gaps, concerns, hidden tricks found]

## Implementation Priorities
- [What to focus on if reproducing this paper]
```
