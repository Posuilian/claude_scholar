---
name: claude-md-authoring
description: "Methodology for writing effective CLAUDE.md files — structure templates, line limits, and overflow strategies"
user-invocable: false
---

# CLAUDE.md Authoring Methodology

This skill provides the methodology for creating and updating CLAUDE.md files. For concrete templates, line limits, eligibility criteria, and anti-patterns, see `.claude_personal/rules/claude-md-standards.md`.

## Core Principle: The "First Try" Test

After reading ONLY the CLAUDE.md files (no other docs), Claude should be able to:

1. Run the tests successfully on first try
2. Build the project without errors
3. Understand the architecture enough to locate where to make a change
4. Know which patterns are sacred and must not be violated

If any of these fail, the CLAUDE.md is incomplete.

## Authoring Workflow

### For New Projects (/init-pro)

1. **Scan first, write second** — use project-scanner to detect actual state, never assume
2. **Populate from data** — every Quick Start command must come from real build manifests
3. **Validate conventions** — sample actual source files, don't guess naming/import styles
4. **Check line counts** — count before writing, extract overflow to `.claude/rules/`

### For Updates (/update-claude-md)

1. **Merge, don't replace** — preserve user-written content, only update stale sections
2. **Minimize diff** — change only what's actually outdated
3. **Detect structural shifts** — new directories, renamed entry points, changed dependencies
4. **Respect existing tone** — if the user wrote a section in a specific style, match it

## When to Create vs Skip a Subdirectory CLAUDE.md

Apply the eligibility criteria from the standards. Additionally:

- **Prefer fewer files**: a single well-written root CLAUDE.md is better than many thin subdirectory files
- **Only create if distinct**: the subdirectory must have patterns or commands that genuinely differ from root
- **Delete if redundant**: if a subdirectory CLAUDE.md only repeats root content, remove it

## Common Mistakes

1. **Writing what you know instead of what you detect** — always base content on scanned data
2. **Forgetting the ancestor chain** — subdirectory files inherit root, so never duplicate
3. **Overloading Key Patterns** — only rules that break things if violated, not style preferences
4. **Stale commands** — Quick Start must be verified against actual build manifests
5. **Ignoring the 200-line limit** — content beyond 200 lines is silently dropped
