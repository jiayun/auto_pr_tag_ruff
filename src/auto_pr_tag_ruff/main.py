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
    
    # Testing filter_mode: added with changed_files: true
    import datetime  # E402 - import should be at top (NEW LINE)
    added_test_var = "this variable is added but unused"  # F841 - never used (NEW LINE)
    print("This is a completely new extremely long line that should definitely trigger the E501 line length error for our testing")  # E501 (NEW LINE)
    
    # Additional new violations to test 'added' filter mode
    z=5*6  # E225 - missing spaces around operator (NEW LINE)
    brand_new_unused="testing added filter mode"  # F841 - unused variable (NEW LINE)
    print("Testing added filter mode successfully!")


if __name__ == "__main__":
    main()
