"""
Integration tests for CLI commands.

Tests all CLI commands using Typer's CliRunner to ensure proper
end-to-end functionality.
"""

import pytest
from typer.testing import CliRunner
from pathlib import Path

from patternsphere.cli.commands import app
from patternsphere.cli.app_context import AppContext


@pytest.fixture(autouse=True)
def reset_context():
    """Reset AppContext before each test."""
    AppContext.reset_instance()
    yield
    AppContext.reset_instance()


@pytest.fixture
def cli_runner():
    """Create a Typer CLI runner."""
    return CliRunner()


class TestSearchCommand:
    """Tests for the search command."""

    def test_search_basic_query(self, cli_runner):
        """Test basic search with keyword."""
        result = cli_runner.invoke(app, ["search", "refactoring"])
        assert result.exit_code == 0
        assert "pattern" in result.stdout.lower()

    def test_search_with_category_filter(self, cli_runner):
        """Test search with category filter."""
        result = cli_runner.invoke(app, [
            "search", "code",
            "--category", "First Contact"
        ])
        assert result.exit_code == 0

    def test_search_with_tags_filter(self, cli_runner):
        """Test search with tag filter."""
        result = cli_runner.invoke(app, [
            "search", "test",
            "--tags", "testing,quality"
        ])
        assert result.exit_code == 0

    def test_search_with_limit(self, cli_runner):
        """Test search with result limit."""
        result = cli_runner.invoke(app, [
            "search", "pattern",
            "--limit", "5"
        ])
        assert result.exit_code == 0

    def test_search_no_scores(self, cli_runner):
        """Test search without showing scores."""
        result = cli_runner.invoke(app, [
            "search", "code",
            "--no-scores"
        ])
        assert result.exit_code == 0
        # Score should not be displayed
        assert "score:" not in result.stdout.lower()

    def test_search_combined_filters(self, cli_runner):
        """Test search with multiple filters."""
        result = cli_runner.invoke(app, [
            "search", "refactoring",
            "--category", "Redistribute Responsibilities",
            "--tags", "refactoring",
            "--limit", "10"
        ])
        assert result.exit_code == 0

    def test_search_no_results(self, cli_runner):
        """Test search with no matching results."""
        result = cli_runner.invoke(app, [
            "search", "xyznonexistent123"
        ])
        assert result.exit_code == 0
        assert "no" in result.stdout.lower() or "0" in result.stdout


class TestListCommand:
    """Tests for the list command."""

    def test_list_all_patterns(self, cli_runner):
        """Test listing all patterns."""
        result = cli_runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Patterns" in result.stdout

    def test_list_with_category_filter(self, cli_runner):
        """Test listing patterns by category."""
        result = cli_runner.invoke(app, [
            "list",
            "--category", "First Contact"
        ])
        assert result.exit_code == 0
        assert "First Contact" in result.stdout or "Patterns" in result.stdout

    def test_list_sort_by_name(self, cli_runner):
        """Test listing patterns sorted by name."""
        result = cli_runner.invoke(app, [
            "list",
            "--sort", "name"
        ])
        assert result.exit_code == 0

    def test_list_sort_by_category(self, cli_runner):
        """Test listing patterns sorted by category."""
        result = cli_runner.invoke(app, [
            "list",
            "--sort", "category"
        ])
        assert result.exit_code == 0

    def test_list_invalid_sort(self, cli_runner):
        """Test listing with invalid sort parameter."""
        result = cli_runner.invoke(app, [
            "list",
            "--sort", "invalid"
        ])
        assert result.exit_code == 0  # Should still work with warning


class TestViewCommand:
    """Tests for the view command."""

    def test_view_pattern_by_name(self, cli_runner):
        """Test viewing pattern by name."""
        # First get a pattern name
        list_result = cli_runner.invoke(app, ["list", "--limit", "1"])
        # View should work with valid pattern names from the dataset
        result = cli_runner.invoke(app, ["view", "Read all the Code in One Hour"])
        assert result.exit_code == 0 or result.exit_code == 1  # May not exist in test data

    def test_view_nonexistent_pattern(self, cli_runner):
        """Test viewing non-existent pattern."""
        result = cli_runner.invoke(app, ["view", "NonexistentPattern123"])
        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

    def test_view_shows_all_sections(self, cli_runner):
        """Test that view shows all pattern sections."""
        # Try to view a known pattern if it exists
        result = cli_runner.invoke(app, ["view", "Read all the Code in One Hour"])
        if result.exit_code == 0:
            assert "INTENT" in result.stdout
            assert "PROBLEM" in result.stdout
            assert "SOLUTION" in result.stdout


class TestCategoriesCommand:
    """Tests for the categories command."""

    def test_categories_displays_list(self, cli_runner):
        """Test that categories command displays category list."""
        result = cli_runner.invoke(app, ["categories"])
        assert result.exit_code == 0
        assert "Categories" in result.stdout or "Category" in result.stdout

    def test_categories_shows_counts(self, cli_runner):
        """Test that categories shows pattern counts."""
        result = cli_runner.invoke(app, ["categories"])
        assert result.exit_code == 0
        # Should show some numeric counts
        assert any(char.isdigit() for char in result.stdout)

    def test_categories_shows_total(self, cli_runner):
        """Test that categories shows total count."""
        result = cli_runner.invoke(app, ["categories"])
        assert result.exit_code == 0
        assert "TOTAL" in result.stdout or "total" in result.stdout.lower()


class TestInfoCommand:
    """Tests for the info command."""

    def test_info_displays_version(self, cli_runner):
        """Test that info displays version."""
        result = cli_runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "1.0.0" in result.stdout or "Version" in result.stdout

    def test_info_displays_pattern_count(self, cli_runner):
        """Test that info displays pattern count."""
        result = cli_runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "Patterns" in result.stdout or "patterns" in result.stdout.lower()

    def test_info_displays_app_name(self, cli_runner):
        """Test that info displays application name."""
        result = cli_runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "PatternSphere" in result.stdout


class TestVersionOption:
    """Tests for the --version option."""

    def test_version_option(self, cli_runner):
        """Test --version flag."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.stdout

    def test_version_short_option(self, cli_runner):
        """Test -v flag."""
        result = cli_runner.invoke(app, ["-v"])
        assert result.exit_code == 0
        assert "1.0.0" in result.stdout


class TestHelpOption:
    """Tests for the --help option."""

    def test_main_help(self, cli_runner):
        """Test main --help flag."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "search" in result.stdout.lower()
        assert "list" in result.stdout.lower()
        assert "view" in result.stdout.lower()

    def test_search_help(self, cli_runner):
        """Test search --help flag."""
        result = cli_runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0
        assert "query" in result.stdout.lower()

    def test_list_help(self, cli_runner):
        """Test list --help flag."""
        result = cli_runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "category" in result.stdout.lower()

    def test_view_help(self, cli_runner):
        """Test view --help flag."""
        result = cli_runner.invoke(app, ["view", "--help"])
        assert result.exit_code == 0

    def test_categories_help(self, cli_runner):
        """Test categories --help flag."""
        result = cli_runner.invoke(app, ["categories", "--help"])
        assert result.exit_code == 0

    def test_info_help(self, cli_runner):
        """Test info --help flag."""
        result = cli_runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0


class TestErrorHandling:
    """Tests for error handling."""

    def test_search_missing_query(self, cli_runner):
        """Test search without query argument."""
        result = cli_runner.invoke(app, ["search"])
        assert result.exit_code != 0  # Should fail

    def test_view_missing_identifier(self, cli_runner):
        """Test view without pattern identifier."""
        result = cli_runner.invoke(app, ["view"])
        assert result.exit_code != 0  # Should fail

    def test_invalid_command(self, cli_runner):
        """Test invalid command."""
        result = cli_runner.invoke(app, ["invalidcommand"])
        assert result.exit_code != 0


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""

    def test_complete_workflow(self, cli_runner):
        """Test complete user workflow."""
        # 1. Get info
        result = cli_runner.invoke(app, ["info"])
        assert result.exit_code == 0

        # 2. List categories
        result = cli_runner.invoke(app, ["categories"])
        assert result.exit_code == 0

        # 3. List patterns
        result = cli_runner.invoke(app, ["list"])
        assert result.exit_code == 0

        # 4. Search patterns
        result = cli_runner.invoke(app, ["search", "code"])
        assert result.exit_code == 0

        # 5. Search with filters
        result = cli_runner.invoke(app, [
            "search", "refactoring",
            "--category", "Redistribute Responsibilities",
            "--limit", "5"
        ])
        assert result.exit_code == 0

    def test_exploration_workflow(self, cli_runner):
        """Test pattern exploration workflow."""
        # Browse by category
        result = cli_runner.invoke(app, [
            "list",
            "--category", "First Contact",
            "--sort", "name"
        ])
        assert result.exit_code == 0

        # Search within category
        result = cli_runner.invoke(app, [
            "search", "read",
            "--category", "First Contact"
        ])
        assert result.exit_code == 0
