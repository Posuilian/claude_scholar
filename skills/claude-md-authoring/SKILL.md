---
name: claude-md-authoring
description: "Methodology for writing effective CLAUDE.md files — structure templates, line limits, and overflow strategies"
user-invocable: false
---

# CLAUDE.md Authoring Methodology

## The 200-Line Contract

Every CLAUDE.md file MUST stay under 200 lines. This is a hard technical requirement — only the first ~200 lines are reliably injected into Claude's system prompt at startup. Going over means instructions silently drop off.

- **Target**: 120-180 lines for root, 60-120 lines for subdirectories
- **Hard cap**: 200 lines — no exceptions
- **If you're over**: extract to `.claude/rules/` (see Overflow Strategy below)

## Loading Mechanics

Understand how CLAUDE.md files are loaded to write them effectively:

- **Ancestor loading (UP)**: At startup, Claude walks UP from CWD to root, loading every CLAUDE.md
- **Descendant loading (DOWN)**: Subdirectory CLAUDE.md files load LAZILY when Claude reads files in those directories
- **Siblings never load**: Working in `frontend/` won't load `backend/CLAUDE.md`
- **Implication**: Don't repeat root-level content in subdirectory files — it's already loaded via ancestor path

## Root CLAUDE.md Template (6 Sections)

```markdown
# CLAUDE.md

## Project Overview
[1-3 sentences: what this is, primary language/framework, purpose]

## Quick Start
[Exact commands for: install dependencies, build, run tests, start dev server]
[This section is the most important — "run the tests" must work first try]

## Architecture
[Directory layout with brief annotations]
[Key entry points and data flow summary]
[Important boundaries between components]

## Coding Standards
[Detected actual conventions — not aspirational rules]
[Import order, naming, type usage, doc style]
[Linter/formatter config references]

## Key Patterns
<important if="modifying source code">
[Critical rules that MUST be followed — things that break if violated]
[Framework-specific patterns, state management, error handling]
</important>

## Common Tasks
[Exact command invocations for: test, lint, deploy, generate, migrate]
[Each command should be copy-pasteable]
```

## Subdirectory CLAUDE.md Template (5 Sections)

```markdown
# CLAUDE.md — [Component Name]

## Purpose
[What this component does in the larger system, 2-3 sentences]

## Quick Commands
[Component-specific test/build/run — only commands that differ from root]

## Key Files
[Most important files and their roles — entry points, not exhaustive listings]

## Patterns
<important if="editing files in [this-directory]">
[Component-specific rules that differ from or extend root conventions]
</important>

## Dependencies
[What this component depends on, what depends on it]
[API contracts or interfaces with other components]
```

## The "First Try" Test

After reading ONLY the CLAUDE.md files (no other docs), Claude should be able to:

1. Run the tests successfully on first try
2. Build the project without errors
3. Understand the architecture enough to locate where to make a change
4. Know which patterns are sacred and must not be violated

If any of these fail, the CLAUDE.md is incomplete.

## Anti-Patterns

- **Generic advice** ("write clean code", "follow best practices") — only project-specific rules
- **Duplicating README** — CLAUDE.md is for Claude, README is for humans
- **Listing every file** — focus on entry points and key abstractions
- **Aspirational rules** — describe what the code actually does, not what you wish it did
- **Hardcoded paths** — use relative references, not absolute paths
- **Exceeding 200 lines** — if you're over, use the overflow strategy

## Overflow Strategy

When content won't fit in 200 lines, create `.claude/rules/{name}.md`:

```yaml
# .claude/rules/{name}.md
---
globs: ["src/api/**/*.ts", "src/api/**/*.tsx"]
description: "API layer conventions and patterns"
---
[Content that was extracted from CLAUDE.md]
```

Rules files are loaded automatically when Claude touches matching files (glob pattern). This gives you effectively unlimited instruction space while keeping CLAUDE.md focused.

## Wrap Critical Rules

Use `<important if="...">` tags for rules that Claude tends to ignore as files grow longer:

```markdown
<important if="modifying database models">
Always create a migration file when changing model fields.
Never modify existing migrations — create new ones.
</important>
```

## Multi-CLAUDE.md Coordination

When creating multiple CLAUDE.md files in a project:

1. **Root owns**: project-wide conventions, build commands, architecture overview
2. **Subdirectory owns**: component-specific patterns, local commands, local dependencies
3. **Never duplicate**: if root says "use TypeScript strict mode", subdirectory should not repeat it
4. **Cross-reference**: root should list which subdirectories have their own CLAUDE.md
