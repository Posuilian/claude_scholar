---
description: "Enhanced init — create CLAUDE.md for project root and key subdirectories"
argument-hint: "[--dry-run] [--root-only] [--subdirs-only]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent, AskUserQuestion
---

# /init-pro — Enhanced Project Initialization

Create well-structured CLAUDE.md files for the project root AND key subdirectories. This is an enhanced version of the built-in `/init` that understands monorepos, multi-module projects, and the 200-line best practice.

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:
- `--dry-run` — analyze and show plan, but don't write any files
- `--root-only` — only create/update the root CLAUDE.md
- `--subdirs-only` — only create/update subdirectory CLAUDE.md files (assumes root already exists)

Default (no flags): create both root and subdirectory CLAUDE.md files.

## Step 2: Detect Git Repository & Scope Directories

Before scanning, check if the current directory is a git repository to limit the scan scope:

1. Run `git rev-parse --is-inside-work-tree 2>/dev/null` to check if inside a git repo
2. If **yes** (exit code 0):
   - Run `git ls-files | sed 's|/.*||' | sort -u` to get all top-level directories containing git-tracked files
   - Store the result as `git_tracked_dirs`
   - This list will be passed to the project-scanner agent to restrict its scan scope
3. If **no** (not a git repo):
   - Set `git_tracked_dirs` to empty — no restriction applied, scan all directories

## Step 3: Scan Project Structure

Launch the `project-scanner` agent to analyze the project. If `git_tracked_dirs` is non-empty, include it in the prompt to restrict the scan scope:

```
Agent(subagent_type="project-scanner", description="Analyze project structure for CLAUDE.md generation", prompt="Scan the current project directory thoroughly. Detect project type, languages, frameworks, build commands, coding conventions, and identify which subdirectories need their own CLAUDE.md. Return your findings as structured JSON. Be thorough but efficient — sample files instead of reading everything.

[If git_tracked_dirs is non-empty, append:]
IMPORTANT — Git-scoped scan: This is a git repository. ONLY scan the following top-level directories (ignore all others): {git_tracked_dirs}")
```

Wait for the agent to complete and parse the returned JSON findings.

## Step 4: Handle Existing Files

Check the scanner's `existing_claude_md` results. For each existing CLAUDE.md file that would be overwritten:

Use AskUserQuestion to ask:
- Question: "[path]/CLAUDE.md already exists ({line_count} lines, {health}). What should I do?"
- Options: "Overwrite — replace with newly generated content" / "Merge — keep existing content and add missing sections" / "Skip — leave this file unchanged"

Remember the user's choices for each file.

## Step 5: Generate CLAUDE.md Files

All generated content must follow the standards defined in `.claude_personal/rules/claude-md-standards.md` (templates, line limits, coordination rules).

### 5a: Root CLAUDE.md (unless --subdirs-only)

Using the scanner's findings, generate a root CLAUDE.md following the Root Template (6 sections) from the standards. Populate each section with data from the scanner's JSON output (commands, directory_layout, coding_conventions, etc.).

Write the file using the Write tool.

### 5b: Subdirectory CLAUDE.md Files (unless --root-only)

For each subdirectory in scanner's `subdirectories_needing_claude_md`, generate a focused CLAUDE.md following the Subdirectory Template (5 sections) from the standards.

Write each file using the Write tool.

### 5c: Handle Overflow

After generating each file, count its lines. If any CLAUDE.md exceeds 200 lines, apply the Overflow Strategy from the standards:

1. Identify the least critical sections
2. Extract them to `.claude/rules/{component-name}.md` with appropriate glob frontmatter (see Overflow Strategy in standards)
3. Replace the extracted content in CLAUDE.md with a one-line reference

## Step 6: Dry-Run Output (if --dry-run)

If `--dry-run` was specified, instead of writing files, present the plan as a table:

```
| File                        | Lines | Action   | Key Sections                    |
|-----------------------------|-------|----------|---------------------------------|
| CLAUDE.md                   | ~150  | Create   | Overview, Quick Start, Arch...  |
| packages/api/CLAUDE.md      | ~85   | Create   | Purpose, Commands, Patterns...  |
| packages/web/CLAUDE.md      | ~90   | Create   | Purpose, Commands, Patterns...  |
```

Then show a preview of the root CLAUDE.md content and ask if the user wants to proceed.

## Step 7: Summary

After writing all files, present a summary table:

```
🚀 /init-pro complete!

| File                        | Lines | Status    |
|-----------------------------|-------|-----------|
| CLAUDE.md                   | 142   | ✅ Created |
| packages/api/CLAUDE.md      | 87    | ✅ Created |
| packages/web/CLAUDE.md      | 93    | ✅ Created |
| .claude/rules/api-rules.md  | 45    | ✅ Created (overflow) |

All files are under the 200-line limit.
Run /init-pro --dry-run anytime to check the current state.
```

## Critical Requirements

1. **Use Agent tool for scanner** — DO NOT use bash commands to analyze the project yourself. The project-scanner agent is designed for this.
2. **Respect the 200-line limit** — This is non-negotiable. Count lines before writing.
3. **Detect, don't assume** — All content must come from scanner analysis, not assumptions about what the project might contain.
4. **Ask before overwriting** — Always ask user permission before replacing existing CLAUDE.md files.
5. **Copy-pasteable commands** — Every command in Quick Start / Common Tasks must work when copy-pasted into a terminal.
