#!/usr/bin/env python3
"""
claude-md-guardian: Stop hook that checks CLAUDE.md health after every Claude response.

Fires on the Stop event. Cross-project reusable — uses CLAUDE_PROJECT_DIR env var.
Uses git diff as a fast short-circuit: no file changes → no output → zero noise.

Output: JSON with additionalContext field containing recommendations.
Only surfaces issues — does NOT auto-edit files.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Directories to always skip
EXCLUDE_DIRS = frozenset({
    "node_modules", "vendor", ".git", "dist", "build", "__pycache__",
    "target", ".next", "venv", ".venv", "env", "coverage", ".cache",
    ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "site-packages",
    ".claude", ".claude_personal",
})

# Source file extensions for counting
SRC_EXTENSIONS = frozenset({
    ".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".java",
    ".cpp", ".c", ".cs", ".rb", ".swift", ".kt", ".scala", ".php",
    ".vue", ".svelte", ".dart", ".zig", ".lua", ".sh", ".bash",
})

# Candidate subdirectory patterns to check for missing CLAUDE.md
CANDIDATE_PATTERNS = [
    "packages/*", "apps/*", "services/*", "crates/*", "libs/*",
    "modules/*", "plugins/*", "workspaces/*",
]
CANDIDATE_DIRS = [
    "src", "lib", "api", "frontend", "backend", "server", "client",
    "web", "mobile", "core", "shared", "common", "internal",
]

LINE_LIMIT = 200
LINE_WARNING = 180
MIN_HEADINGS = 2
MIN_SOURCE_FILES_FOR_SUGGESTION = 5


def should_skip(path_parts: list[str]) -> bool:
    """Check if any path component is in the exclude set."""
    return any(p in EXCLUDE_DIRS for p in path_parts)


def has_git_changes(project_dir: str) -> bool:
    """Quick check: are there any uncommitted changes or new files?"""
    try:
        # Check both staged + unstaged changes, plus untracked files
        result = subprocess.run(
            ["git", "status", "--porcelain", "--short"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return bool(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        # If git isn't available or times out, skip the short-circuit
        # and run checks anyway (safer default)
        return True


def check_line_counts(project_dir: Path) -> list[str]:
    """Check all CLAUDE.md files for line count and structure issues."""
    issues = []

    for claude_md in project_dir.rglob("CLAUDE.md"):
        rel = claude_md.relative_to(project_dir)
        parts = list(rel.parts)

        if should_skip(parts):
            continue

        try:
            content = claude_md.read_text(encoding="utf-8")
            lines = content.splitlines()
            line_count = len(lines)

            # Line count checks
            if line_count > LINE_LIMIT:
                issues.append(
                    f"⚠️ {rel}: {line_count} lines (exceeds {LINE_LIMIT}-line limit). "
                    f"Extract overflow to .claude/rules/."
                )
            elif line_count > LINE_WARNING:
                issues.append(
                    f"⚡ {rel}: {line_count} lines (approaching {LINE_LIMIT}-line limit)."
                )

            # Structure check: enough section headings?
            headings = [l for l in lines if l.startswith("## ")]
            if len(headings) < MIN_HEADINGS and line_count > 20:
                issues.append(
                    f"📋 {rel}: Only {len(headings)} section heading(s) — "
                    f"structure may be degraded."
                )

            # Root CLAUDE.md: does it have build/test commands?
            if str(rel) == "CLAUDE.md":
                content_lower = content.lower()
                has_commands = any(
                    kw in content_lower
                    for kw in ["test", "build", "run", "install", "setup", "start"]
                )
                if not has_commands:
                    issues.append(
                        f"🔧 {rel}: Missing build/test/setup commands — "
                        f"'run the tests' may fail on first try."
                    )

        except (IOError, OSError, UnicodeDecodeError):
            continue

    return issues


def count_source_files(directory: Path, limit: int = MIN_SOURCE_FILES_FOR_SUGGESTION + 1) -> int:
    """Count source files in a directory, with early exit for efficiency."""
    count = 0
    try:
        for root, dirs, files in os.walk(directory):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if Path(f).suffix in SRC_EXTENSIONS:
                    count += 1
                    if count >= limit:
                        return count
    except (OSError, PermissionError):
        pass
    return count


def check_missing_claude_md(project_dir: Path) -> list[str]:
    """Check if significant subdirectories are missing CLAUDE.md."""
    issues = []

    candidates = []

    # Glob-based patterns (monorepo packages)
    for pattern in CANDIDATE_PATTERNS:
        candidates.extend(project_dir.glob(pattern))

    # Named directories
    for dirname in CANDIDATE_DIRS:
        candidate = project_dir / dirname
        if candidate.is_dir():
            candidates.append(candidate)

    for d in candidates:
        if not d.is_dir():
            continue

        rel_d = d.relative_to(project_dir)
        if should_skip(list(rel_d.parts)):
            continue

        claude_md_path = d / "CLAUDE.md"
        if claude_md_path.exists():
            continue

        src_count = count_source_files(d)
        if src_count > MIN_SOURCE_FILES_FOR_SUGGESTION:
            issues.append(
                f"📁 {rel_d}/: {src_count}+ source files but no CLAUDE.md. "
                f"Consider running /init-pro --subdirs-only."
            )

    return issues


def main():
    # Read stdin (hook input JSON) — may be empty for some hook types
    try:
        stdin_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        stdin_data = {}

    # Determine project directory
    project_dir = os.environ.get(
        "CLAUDE_PROJECT_DIR",
        stdin_data.get("cwd", os.getcwd()),
    )
    project_path = Path(project_dir)

    if not project_path.is_dir():
        sys.exit(0)

    # Fast short-circuit: no file changes → no checks needed
    if not has_git_changes(project_dir):
        sys.exit(0)

    # Run checks
    issues = []
    issues.extend(check_line_counts(project_path))
    issues.extend(check_missing_claude_md(project_path))

    # Output recommendations via additionalContext
    if issues:
        header = "🛡️ **CLAUDE.md Guardian** — issues detected:"
        body = "\n".join(f"  {issue}" for issue in issues)
        msg = f"{header}\n{body}"

        output = {"additionalContext": msg}
        print(json.dumps(output))

    # Always exit 0 — never block Claude's response
    sys.exit(0)


if __name__ == "__main__":
    main()
