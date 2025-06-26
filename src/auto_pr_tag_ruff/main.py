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
    
    # NEW TEST: More violations to verify fixed action-ruff
    very_long_line_that_exceeds_88_characters_limit_and_should_trigger_E501_error_for_testing_purposes = "test"  # E501
    import sys  # E402 - import not at top
    unused_new_var = "this should trigger F841"  # F841
    
    # FAIL TEST: These should cause CI to fail
    import json   # E402 - another import not at top
    x=1+2+3+4+5  # E225 - missing spaces around operators
    super_long_variable_name_that_definitely_exceeds_the_line_length_limit_and_should_cause_E501_error = "fail test"  # E501
    another_unused_variable = "this will trigger F841 unused variable error"  # F841


if __name__ == "__main__":
    main()
