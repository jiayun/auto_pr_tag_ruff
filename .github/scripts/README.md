# Ruff Diff Check Script

This script (`ruff-diff-check.py`) is designed to run Ruff linting and formatting checks only on lines that have been modified in a git diff, rather than checking entire files.

## Purpose

When working with existing codebases, you often want to ensure that your changes don't introduce new linting issues without being forced to fix all existing issues in the files you touch. This script allows you to run Ruff checks only on the lines you've actually modified.

## How it works

1. **Detect Changed Lines**: Uses `git diff` to identify which lines were added, modified, or removed in each file
2. **Run Ruff**: Executes both `ruff check` and `ruff format --check` on the specified files
3. **Filter Results**: Only reports issues that occur on changed lines or within 2 lines of a change (to handle cases like import sorting)
4. **Report**: Outputs the filtered results in a format suitable for CI/CD pipelines

## Features

- ✅ Handles both committed and unstaged changes
- ✅ Supports multiple files
- ✅ Detects import sorting issues that affect nearby lines
- ✅ Returns appropriate exit codes for CI/CD integration
- ✅ Works with both absolute and relative file paths
- ✅ CI environment compatibility with `GITHUB_BASE_REF` support
- ✅ Improved error handling with warning messages

## Usage

```bash
python .github/scripts/ruff-diff-check.py <file1> [file2] [file3] ...
```

## Environment Variables

- `GITHUB_BASE_REF`: When set (typically in GitHub Actions PR context), the script will compare against `origin/{GITHUB_BASE_REF}` instead of `HEAD~1`. This allows proper comparison against the target branch in pull requests.

## Integration with GitHub Actions

The script is integrated into the `lab-ruff-check.yml` workflow and automatically runs on changed Python files when pushing to the `lab` branch.

## Exit Codes

- `0`: No issues found on changed lines
- `1`: Issues found on changed lines (causes CI to fail)