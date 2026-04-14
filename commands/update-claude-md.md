---
description: "Update existing CLAUDE.md files — incremental by default, --full for full rescan"
argument-hint: "[--full] [--dry-run] [--since-commit N]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent, AskUserQuestion
---

# /update-claude-md — Incremental CLAUDE.md Updater

Update existing CLAUDE.md files based on code changes. Preserves hand-written content while updating stale sections.

All generated content must follow the standards defined in `.claude_personal/rules/claude-md-standards.md`.

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:
- `--full` — full rescan via project-scanner, compare and update all CLAUDE.md files
- `--dry-run` — analyze and show what would change, but don't write any files
- `--since-commit N` — use git commit history (`HEAD~N..HEAD`) instead of working tree diff

Default (no flags): incremental update based on **working tree changes** (staged + unstaged + untracked files).

## Step 2: Detect Git Repository & Scope Directories

1. Run `git rev-parse --is-inside-work-tree 2>/dev/null` to check if inside a git repo
2. If **yes** (exit code 0):
   - Run `git ls-files | sed 's|/.*||' | sort -u` to get all top-level directories containing git-tracked files
   - Store the result as `git_tracked_dirs`
3. If **no** (not a git repo):
   - Set `git_tracked_dirs` to empty — no restriction applied

## Step 3: Determine Changed Scope

### Incremental mode (default)

1. Detect changed directories from the **working tree** (all uncommitted modifications):
   ```bash
   { git diff --name-only; git diff --cached --name-only; git ls-files --others --exclude-standard; } 2>/dev/null | sed 's|/.*||' | sort -u
   ```
   - `git diff --name-only` → unstaged modifications
   - `git diff --cached --name-only` → staged changes
   - `git ls-files --others --exclude-standard` → new untracked files
2. If working tree is clean (no output), **fall back** to recent commits:
   - `git diff --name-only HEAD~3..HEAD 2>/dev/null | sed 's|/.*||' | sort -u`
   - If that also fails, treat as full mode
3. Store as `changed_dirs`
4. Check for new git-tracked directories that don't have a CLAUDE.md yet:
   - Compare `git_tracked_dirs` against existing CLAUDE.md locations
   - Add any new directories to `changed_dirs`

### `--since-commit N` mode

Use git commit history instead of working tree:
1. Run `git diff --name-only HEAD~N..HEAD 2>/dev/null | sed 's|/.*||' | sort -u`
2. If HEAD~N fails, fall back to `git diff --name-only HEAD~1..HEAD`
3. Store as `changed_dirs`

### Full mode (--full)

Launch the `project-scanner` agent (same as init-pro Step 3) with `git_tracked_dirs` scope. Use its output to identify all directories needing updates.

## Step 4: Analyze & Update

Launch the `claude-md-updater` agent:

```
Agent(subagent_type="claude-md-updater", description="Incrementally update CLAUDE.md files", prompt="Analyze the following directories for CLAUDE.md updates. For each directory, read the existing CLAUDE.md (if any) and the current code state, then produce updated content.

Mode: {incremental|full}
Changed directories: {changed_dirs or scanner output}
Git-tracked directories: {git_tracked_dirs}

For each CLAUDE.md that needs updating, return a JSON array with:
- path: file path
- action: 'update' | 'create' | 'skip'
- reason: why this file needs updating
- content: the new file content (if action != 'skip')

Rules:
- MERGE, don't replace — preserve user-written content, only update stale sections
- Follow the standards in .claude_personal/rules/claude-md-standards.md
- For new subdirectories: create CLAUDE.md only if they meet the eligibility criteria in the standards
- For existing files: update sections that are outdated based on code changes
- Never exceed 200 lines per file")
```

Wait for the agent to return. Parse the JSON results.

## Step 5: Apply Changes (unless --dry-run)

For each file in the agent's results where action is 'update' or 'create':

1. If the file exists and action is 'update':
   - Use AskUserQuestion: "{path} needs updating ({reason}). Apply changes?"
   - Options: "Yes — apply the update" / "Preview — show me the diff first" / "Skip — leave unchanged"
2. If action is 'create':
   - Use AskUserQuestion: "New CLAUDE.md suggested for {path} ({reason}). Create it?"
   - Options: "Yes — create it" / "Preview — show me the content first" / "Skip"
3. Write approved changes using the Write or Edit tool

### Handle Overflow

After writing each file, count lines. If any exceeds 200 lines, apply the overflow strategy from the standards (extract to `.claude/rules/`).

## Step 6: Dry-Run Output (if --dry-run)

Present the plan as a table without writing files:

```
| File                   | Action | Reason                          | Lines |
|------------------------|--------|---------------------------------|-------|
| CLAUDE.md              | Update | New subdirectory added           | ~155  |
| packages/api/CLAUDE.md | Create | New package with 23 source files | ~85   |
| lib/CLAUDE.md          | Skip   | No significant changes           | 72    |
```

## Step 7: Summary

After all changes are applied:

```
/update-claude-md complete!

| File                   | Lines | Status      |
|------------------------|-------|-------------|
| CLAUDE.md              | 155   | Updated     |
| packages/api/CLAUDE.md | 85    | Created     |

Updated 1 file, created 1 file, skipped 3 files.
```
