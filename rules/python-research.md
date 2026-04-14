# Glob: **/*.py

## Python Research Code Standards

### Documentation

- Every function and class must have a Google-style docstring
- Include `Args:`, `Returns:`, and `Raises:` sections for non-trivial functions
- Add inline comments for non-obvious mathematical operations or algorithmic steps

### Configuration

- Hyperparameters must come from config files or CLI arguments, never hardcoded
- Use `dataclass` or YAML-based configs, not scattered `argparse` definitions
- Default values should match the paper's reported settings

### Code Quality

- Import order: stdlib → third-party → local (one blank line between groups)
- Use type hints for all function signatures
- Use `logging` module instead of `print()` for any experiment output
- Prefer `pathlib.Path` over string paths

### Before Modifying Training Code

- Read and understand the COMPLETE training loop before making changes
- Identify all places where the modified component is used
- Check if the change affects evaluation or inference code too
- Consider backward compatibility with existing checkpoints
