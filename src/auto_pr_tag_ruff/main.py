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
    
    # Testing diff_context with changed_files: false
    import sys  # E402 - import should be at top
    new_test_var = "this is a new unused variable"  # F841 - never used
    print("This is yet another extremely long line that should trigger the line length error E501 for testing purposes")  # E501
    
    # More test violations for diff_context
    y=3*4  # E225 - missing spaces around operator  
    final_unused_var="testing diff context filtering"  # F841 - unused variable
    print("Final test line with violations!")


if __name__ == "__main__":
    main()
