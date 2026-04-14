---
name: code-review
description: Methodology for comparing paper descriptions with code implementations
user-invocable: false
---

# Paper-to-Code Comparison Methodology

## Comparison Dimensions

When comparing a paper's description with its code implementation, check each dimension:

### 1. Architecture
- Layer types and configurations: do they match the paper?
- Hidden dimensions, number of heads, number of layers
- Activation functions (paper says ReLU but code uses GELU?)
- Normalization (BatchNorm vs LayerNorm vs GroupNorm)
- Skip connections or residual connections

### 2. Loss Computation
- Loss function formula: exact match with the paper?
- Loss weighting: are the λ coefficients the same?
- Auxiliary losses: any losses in code not mentioned in paper?
- Gradient handling: detach/stop_gradient on any terms?

### 3. Data Pipeline
- Augmentations: which ones are applied? In what order?
- Preprocessing: normalization values, resize strategies
- Dataset splits: same split ratios as paper?
- Filtering: any samples removed that paper doesn't mention?

### 4. Training Strategy
- Optimizer and its exact settings (betas, epsilon, weight decay)
- Learning rate schedule: warmup steps, decay type
- Batch size: effective batch size with gradient accumulation?
- Mixed precision: FP16/BF16 usage
- EMA (exponential moving average) of weights?

### 5. Evaluation
- Metrics: calculated the same way as paper claims?
- Test-time augmentation or ensembling?
- Post-processing steps
- Evaluation frequency and best-model selection criteria

## What to Look For

### Red Flags (paper doesn't mention but code has)
- Extra loss terms or regularization
- Custom initialization schemes
- Data filtering or hard example mining
- Gradient clipping or norm constraints
- Learning rate warmup not mentioned in paper

### Common Discrepancies
- Paper reports "batch size 256" but code uses 32 with 8x gradient accumulation
- Paper says "Adam" but code uses AdamW (different weight decay behavior)
- Paper's "random crop" is actually a very specific crop strategy in code
- "Standard augmentation" in paper maps to a specific augmentation pipeline

## Output Format

```markdown
# Code vs Paper Comparison: [Paper Title]

## Architecture Differences
| Component | Paper Says | Code Does | Impact |
|-----------|-----------|-----------|--------|
| ... | ... | ... | High/Med/Low |

## Training Differences
| Aspect | Paper Says | Code Does | Impact |
|--------|-----------|-----------|--------|
| ... | ... | ... | High/Med/Low |

## Undocumented Tricks Found
1. [Trick description and location in code]

## Missing from Code
1. [Things paper describes but code doesn't implement]

## Reproduction Risk Assessment
- Overall reproducibility: [High/Medium/Low]
- Key risks: [List the biggest concerns]
```
