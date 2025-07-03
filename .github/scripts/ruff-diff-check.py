#!/usr/bin/env python3
"""Script to run ruff only on changed lines in a git diff.

This script parses git diff output to identify changed line ranges,
then runs ruff and filters the output to only include issues on those lines.
"""

import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Set


def get_changed_lines(file_path: str) -> Set[int]:
    """Get the set of changed line numbers for a file."""
    # Use environment variables for base ref, with fallback to HEAD~1
    base_ref = os.environ.get('GITHUB_BASE_REF')
    if base_ref:
        # In PR context, compare against the base branch
        base_ref = f"origin/{base_ref}"
    else:
        # Fallback to previous commit for local development
        base_ref = "HEAD~1"
    
    try:
        # Get the diff for this specific file
        result = subprocess.run(
            ["git", "diff", base_ref, "HEAD", "--", file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        changed_lines = set()
        current_line = 0

        for line in result.stdout.split("\n"):
            # Look for hunk headers like @@ -1,4 +1,6 @@
            hunk_match = re.match(r"^@@\s+-\d+(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s+@@", line)
            if hunk_match:
                current_line = int(hunk_match.group(1))
                continue

            # Lines starting with + are additions (except +++)
            if line.startswith("+") and not line.startswith("+++"):
                changed_lines.add(current_line)
                current_line += 1
            # Lines starting with space are context (no change)
            elif line.startswith(" "):
                current_line += 1
            # Lines starting with - are deletions (don't increment line number)

        # If no diff output, check if file is new or has unstaged changes
        if not result.stdout.strip():
            # Try to get unstaged changes
            result = subprocess.run(
                ["git", "diff", "--", file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            for line in result.stdout.split("\n"):
                # Look for hunk headers like @@ -1,4 +1,6 @@
                hunk_match = re.match(
                    r"^@@\s+-\d+(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s+@@", line
                )
                if hunk_match:
                    current_line = int(hunk_match.group(1))
                    continue

                # Lines starting with + are additions (except +++)
                if line.startswith("+") and not line.startswith("+++"):
                    changed_lines.add(current_line)
                    current_line += 1
                # Lines starting with space are context (no change)
                elif line.startswith(" "):
                    current_line += 1

        return changed_lines
    except subprocess.CalledProcessError as e:
        print(f"Warning: git diff failed for {file_path}: {e}", file=sys.stderr)
        return set()


def run_ruff_check(files: List[str]) -> List[Dict]:
    """Run ruff check and return the results as JSON."""
    try:
        result = subprocess.run(
            ["ruff", "check", "--output-format=json", *files],
            capture_output=True,
            text=True,
        )

        if result.stdout:
            return json.loads(result.stdout)
        return []
    except subprocess.CalledProcessError as e:
        print(f"Warning: ruff check failed: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Warning: failed to parse ruff check output as JSON: {e}", file=sys.stderr)
        return []


def run_ruff_format_check(files: List[str]) -> List[str]:
    """Run ruff format --check --diff and return lines that have format issues."""
    try:
        result = subprocess.run(
            ["ruff", "format", "--check", "--diff", *files],
            capture_output=True,
            text=True,
        )

        format_issues = []
        current_file = None

        for line in result.stdout.split("\n"):
            # Look for file headers
            if line.startswith("---") or line.startswith("+++"):
                continue
            elif line.startswith("@@"):
                # Parse hunk header to get line numbers
                match = re.match(r"^@@\s+-\d+(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s+@@", line)
                if match and current_file:
                    line_num = int(match.group(1))
                    format_issues.append(
                        f"{current_file}:{line_num}: Format issue detected"
                    )
            elif line.startswith("diff --git"):
                # Extract filename from diff header
                match = re.search(r"b/(.+)$", line)
                if match:
                    current_file = match.group(1)

        return format_issues
    except subprocess.CalledProcessError as e:
        print(f"Warning: ruff format check failed: {e}", file=sys.stderr)
        return []


def filter_ruff_results(
    ruff_results: List[Dict], changed_files: List[str]
) -> List[Dict]:
    """Filter ruff results to only include issues on changed lines."""
    filtered_results = []

    for result in ruff_results:
        file_path = result.get("filename", "")
        line_number = result.get("location", {}).get("row", 0)

        # Check if this file is in our list of changed files
        # (handle both absolute and relative paths)
        is_changed_file = False
        for changed_file in changed_files:
            if (
                file_path.endswith(changed_file)
                or changed_file.endswith(file_path)
                or file_path == changed_file
            ):
                is_changed_file = True
                # Use the changed_file path for consistency
                file_path = changed_file
                break

        if is_changed_file:
            changed_lines = get_changed_lines(file_path)

            # If no changed lines detected, include all results (file might be new)
            if not changed_lines:
                filtered_results.append(result)
            else:
                # Include issues that are on changed lines or within a few
                # lines of changes. This handles cases where adding a line
                # affects nearby code (like import sorting)
                for changed_line in changed_lines:
                    # Within 2 lines of a change
                    if abs(line_number - changed_line) <= 2:
                        filtered_results.append(result)
                        break

    return filtered_results


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: ruff-diff-check.py <file1> [file2] ...")
        sys.exit(1)

    files = sys.argv[1:]

    # Run ruff check
    ruff_results = run_ruff_check(files)
    filtered_results = filter_ruff_results(ruff_results, files)

    # Run ruff format check
    format_issues = run_ruff_format_check(files)

    # Report results
    exit_code = 0

    if filtered_results:
        print("Ruff check issues on changed lines:")
        for result in filtered_results:
            filename = result.get("filename", "")
            location = result.get("location", {})
            row = location.get("row", 0)
            column = location.get("column", 0)
            code = result.get("code", "")
            message = result.get("message", "")

            print(f"{filename}:{row}:{column}: {code} {message}")
        exit_code = 1

    if format_issues:
        print("\nRuff format issues on changed lines:")
        for issue in format_issues:
            print(issue)
        exit_code = 1

    if exit_code == 0:
        print("No ruff issues found on changed lines.")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
