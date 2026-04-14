# Glob: data/** checkpoints/** weights/** pretrained/**

## Data and Model Protection

These directories contain irreplaceable assets. Strict rules apply:

- **NEVER** modify, delete, overwrite, or move any file in these directories
- **NEVER** run commands that could alter these files (e.g., `rm`, `mv`, `cp` to overwrite)
- Read and analyze only — use `Read`, `Glob`, `Grep` tools
- If a task requires changing data, create a **new** file in a different directory instead
- When debugging data loading issues, inspect the data but do not fix it by modifying the source files

## Allowed Operations

- Reading file contents and metadata
- Listing directory structure
- Analyzing data formats and statistics
- Checking file integrity (checksums, shapes, etc.)
