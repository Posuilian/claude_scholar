# Glob: **/CLAUDE.md

## CLAUDE.md Standards

Shared rules for creating and updating CLAUDE.md files. Referenced by `/init-pro`, `/update-claude-md`, `claude-md-authoring` skill, and `claude-md-guardian` hook.

## Line Limits

- **Hard cap**: 200 lines — instructions beyond this are silently dropped
- **Root target**: 120-180 lines
- **Subdirectory target**: 60-120 lines
- **Warning threshold**: 180 lines

## Loading Mechanics

- **Ancestor loading (UP)**: At startup, Claude walks UP from CWD to root, loading every CLAUDE.md
- **Descendant loading (DOWN)**: Subdirectory CLAUDE.md files load LAZILY when Claude reads files in those directories
- **Siblings never load**: Working in `frontend/` won't load `backend/CLAUDE.md`
- **Implication**: Never repeat root-level content in subdirectory files

## Root CLAUDE.md Template (6 Sections)

1. **Project Overview** (5-10 lines) — project name, purpose, primary language/framework
2. **Quick Start** (10-20 lines) — exact install/build/test/run commands. Must work on first copy-paste
3. **Architecture** (15-30 lines) — directory layout, key entry points, data flow
4. **Coding Standards** (10-20 lines) — detected actual conventions (naming, imports, types, docs, linter)
5. **Key Patterns** (10-30 lines) — wrapped in `<important>` tags, only genuinely critical rules
6. **Common Tasks** (10-20 lines) — exact copy-pasteable command invocations

If subdirectories have their own CLAUDE.md, add a brief "Subdirectory Guide" section listing them.

## Subdirectory CLAUDE.md Template (5 Sections)

1. **Purpose** (3-5 lines) — role in the larger system
2. **Quick Commands** (5-10 lines) — only commands that differ from root
3. **Key Files** (5-15 lines) — most important files and their roles
4. **Patterns** (5-15 lines) — wrapped in `<important>` for component-specific rules
5. **Dependencies** (3-5 lines) — upstream/downstream components

## Subdirectory Eligibility Criteria

When to create a CLAUDE.md for a subdirectory:

- **YES**: Has its own build manifest (package.json, Cargo.toml, etc.)
- **YES**: Is a monorepo package (packages/*, apps/*, services/*)
- **YES**: Contains >10 source files AND serves a distinct purpose
- **MAYBE**: Conventional directory (src/, lib/, api/, frontend/, backend/) with significant code
- **NO**: Config directory, docs directory, or has <5 source files

## Overflow Strategy

When content exceeds 200 lines, extract to `.claude/rules/{name}.md`:

```yaml
---
globs: ["src/api/**/*.ts"]
description: "API layer conventions"
---
[Extracted content]
```

Replace in CLAUDE.md with: "See `.claude/rules/{name}.md` for detailed patterns."

## Critical Rules Markup

Use `<important>` tags for rules that must not be ignored:

```markdown
<important if="modifying database models">
Always create a migration file when changing model fields.
Never modify existing migrations — create new ones.
</important>
```

## Anti-Patterns

- **Generic advice** ("write clean code") — only project-specific rules
- **Duplicating README** — CLAUDE.md is for Claude, README is for humans
- **Listing every file** — focus on entry points and key abstractions
- **Aspirational rules** — describe what the code actually does, not what you wish
- **Hardcoded absolute paths** — use relative references
- **Exceeding 200 lines** — use overflow strategy instead

## Multi-File Coordination

1. **Root owns**: project-wide conventions, build commands, architecture overview
2. **Subdirectory owns**: component-specific patterns, local commands, local dependencies
3. **Never duplicate**: if root says "use TypeScript strict mode", subdirectory must not repeat it
4. **Cross-reference**: root should list which subdirectories have their own CLAUDE.md

## The "First Try" Test

After reading ONLY the CLAUDE.md files, Claude should be able to:

1. Run the tests successfully on first try
2. Build the project without errors
3. Understand architecture enough to locate where to make a change
4. Know which patterns are sacred and must not be violated
