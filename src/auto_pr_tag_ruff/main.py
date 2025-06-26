"""Main module for the application."""

from auto_pr_tag_ruff import __version__


def greet(name: str) -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b


def get_version() -> str:
    """Get the application version.

    Returns:
        The version string.
    """
    return f"Version: {__version__}"


def main() -> None:
    """Main entry point of the application."""
    print(get_version())
    print(greet("World"))
    print(f"2 + 3 = {add(2, 3)}")
    print("Tag will point to branch HEAD commit, not merge commit!")
    print("All ruff errors have been fixed!")
    
    # Testing diff_context with fetch-depth: 0
    import json  # E402 - import in wrong place
    test_var = "unused variable for testing"  # F841 - never used
    print("This line is intentionally very very very very very very very very long to test E501 error detection")  # E501
    
    # Additional test with different error types
    x=1+2  # E225 - missing spaces around operator
    another_unused="test"  # F841 - another unused variable


if __name__ == "__main__":
    main()
