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
    # This is a very long line that exceeds the 88 character limit and should trigger a ruff error for line length
    unused_variable = "this variable is never used and should trigger a ruff warning"
    import os  # Import should be at top of file
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


if __name__ == "__main__":
    main()
