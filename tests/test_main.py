"""Tests for the main module."""


from auto_pr_tag_ruff.main import add, greet


class TestGreet:
    """Test cases for the greet function."""

    def test_greet_with_name(self):
        """Test greeting with a name."""
        assert greet("Alice") == "Hello, Alice!"

    def test_greet_with_empty_string(self):
        """Test greeting with empty string."""
        assert greet("") == "Hello, !"


class TestAdd:
    """Test cases for the add function."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-1, -1) == -2

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert add(10, -5) == 5

    def test_add_zero(self):
        """Test adding with zero."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
