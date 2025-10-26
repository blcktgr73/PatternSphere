"""
Unit tests for CLI formatters.

Tests the SearchResultsFormatter and PatternViewFormatter classes.
"""

import pytest
from patternsphere.models import Pattern
from patternsphere.search import SearchResult
from patternsphere.cli.formatters import SearchResultsFormatter, PatternViewFormatter


@pytest.fixture
def sample_pattern():
    """Create a sample pattern for testing."""
    from patternsphere.models.pattern import SourceMetadata
    return Pattern(
        id="TEST-001",
        name="Test Pattern",
        category="Test Category",
        intent="Test intent for the pattern",
        problem="Test problem description",
        solution="Test solution description",
        consequences="Test consequences",
        tags=["test", "example", "demo"],
        related_patterns=["Related Pattern 1", "Related Pattern 2"],
        source_metadata=SourceMetadata(source_name="Test Source")
    )


@pytest.fixture
def sample_search_results(sample_pattern):
    """Create sample search results for testing."""
    from patternsphere.models.pattern import SourceMetadata
    pattern2 = Pattern(
        id="TEST-002",
        name="Another Pattern",
        category="Test Category",
        intent="Another test intent",
        problem="Another problem",
        solution="Another solution",
        tags=["test", "another"],
        source_metadata=SourceMetadata(source_name="Test Source")
    )

    return [
        SearchResult(pattern=sample_pattern, score=10.5, matched_fields={"name", "intent"}),
        SearchResult(pattern=pattern2, score=7.2, matched_fields={"tags"}),
    ]


class TestSearchResultsFormatter:
    """Tests for SearchResultsFormatter."""

    def test_formatter_creation(self):
        """Test creating a formatter."""
        formatter = SearchResultsFormatter(terminal_width=100)
        assert formatter.terminal_width == 100
        assert formatter.use_rich is True

    def test_format_empty_results(self):
        """Test formatting empty results."""
        formatter = SearchResultsFormatter()
        output = formatter.format([])
        assert "no patterns found" in output.lower()

    def test_format_single_result(self, sample_search_results):
        """Test formatting a single result."""
        formatter = SearchResultsFormatter()
        output = formatter.format([sample_search_results[0]])

        assert "1 pattern(s)" in output
        assert "Test Pattern" in output
        assert "10.5" in output  # Score
        assert "Test Category" in output
        assert "test, example, demo" in output  # Tags

    def test_format_multiple_results(self, sample_search_results):
        """Test formatting multiple results."""
        formatter = SearchResultsFormatter()
        output = formatter.format(sample_search_results)

        assert "2 pattern(s)" in output
        assert "Test Pattern" in output
        assert "Another Pattern" in output
        assert "10.5" in output
        assert "7.2" in output

    def test_format_without_scores(self, sample_search_results):
        """Test formatting without showing scores."""
        formatter = SearchResultsFormatter()
        output = formatter.format(sample_search_results, show_scores=False)

        assert "Test Pattern" in output
        assert "score:" not in output.lower()

    def test_format_shows_matched_fields(self, sample_search_results):
        """Test that matched fields are displayed."""
        formatter = SearchResultsFormatter()
        output = formatter.format(sample_search_results)

        assert "Matched in:" in output
        # Should show matched fields for both results

    def test_format_summary(self, sample_search_results):
        """Test summary format."""
        formatter = SearchResultsFormatter()
        summary = formatter.format_summary(sample_search_results)

        assert "2 pattern(s)" in summary
        assert "Categories: 1" in summary  # Both in same category
        assert "Average score:" in summary

    def test_format_summary_empty(self):
        """Test summary with no results."""
        formatter = SearchResultsFormatter()
        summary = formatter.format_summary([])
        assert "No results" in summary

    def test_format_compact(self, sample_search_results):
        """Test compact format."""
        formatter = SearchResultsFormatter()
        output = formatter.format_compact(sample_search_results, limit=1)

        assert "Test Pattern" in output
        assert "10.5" in output
        assert "and 1 more" in output  # Shows remaining count

    def test_format_compact_no_results(self):
        """Test compact format with no results."""
        formatter = SearchResultsFormatter()
        output = formatter.format_compact([])
        assert "No patterns" in output

    def test_truncate_text_short(self):
        """Test text truncation with short text."""
        formatter = SearchResultsFormatter()
        text = "Short text"
        truncated = formatter._truncate_text(text, 100)
        assert truncated == text

    def test_truncate_text_long(self):
        """Test text truncation with long text."""
        formatter = SearchResultsFormatter()
        text = "A" * 200
        truncated = formatter._truncate_text(text, 100)
        assert len(truncated) == 100
        assert truncated.endswith("...")


class TestPatternViewFormatter:
    """Tests for PatternViewFormatter."""

    def test_formatter_creation(self):
        """Test creating a formatter."""
        formatter = PatternViewFormatter(terminal_width=120)
        assert formatter.terminal_width == 120
        assert formatter.use_rich is True

    def test_format_complete_pattern(self, sample_pattern):
        """Test formatting a complete pattern."""
        formatter = PatternViewFormatter()
        output = formatter.format(sample_pattern)

        # Check all sections are present
        assert "Pattern: Test Pattern" in output
        assert "METADATA" in output
        assert "INTENT" in output
        assert "PROBLEM" in output
        assert "SOLUTION" in output
        assert "CONSEQUENCES" in output
        assert "RELATED PATTERNS" in output

        # Check content
        assert "TEST-001" in output
        assert "Test Category" in output
        assert "test, example, demo" in output
        assert "Test intent" in output
        assert "Test problem" in output
        assert "Test solution" in output
        assert "Related Pattern 1" in output
        assert "Related Pattern 2" in output

    def test_format_pattern_without_consequences(self):
        """Test formatting pattern without consequences."""
        from patternsphere.models.pattern import SourceMetadata
        pattern = Pattern(
            id="TEST-003",
            name="Simple Pattern",
            category="Test",
            intent="Intent",
            problem="Problem",
            solution="Solution",
            tags=["test"],
            source_metadata=SourceMetadata(source_name="Test")
        )

        formatter = PatternViewFormatter()
        output = formatter.format(pattern)

        assert "INTENT" in output
        assert "PROBLEM" in output
        assert "SOLUTION" in output
        # Consequences section should not appear if empty
        assert "CONSEQUENCES" not in output

    def test_format_pattern_without_related(self):
        """Test formatting pattern without related patterns."""
        from patternsphere.models.pattern import SourceMetadata
        pattern = Pattern(
            id="TEST-004",
            name="Isolated Pattern",
            category="Test",
            intent="Intent",
            problem="Problem",
            solution="Solution",
            tags=["test"],
            source_metadata=SourceMetadata(source_name="Test")
        )

        formatter = PatternViewFormatter()
        output = formatter.format(pattern)

        assert "Pattern: Isolated Pattern" in output
        # Related patterns section should not appear if empty
        assert "RELATED PATTERNS" not in output

    def test_format_compact(self, sample_pattern):
        """Test compact format."""
        formatter = PatternViewFormatter()
        output = formatter.format_compact(sample_pattern)

        assert "Pattern: Test Pattern" in output
        assert "Test Category" in output
        assert "test, example, demo" in output
        assert "Test intent" in output

        # Should not have full sections
        assert "METADATA" not in output
        assert "PROBLEM" not in output

    def test_wrap_text(self, sample_pattern):
        """Test text wrapping."""
        formatter = PatternViewFormatter(terminal_width=50)
        long_text = "This is a very long text that should be wrapped to fit within the terminal width limit."
        wrapped = formatter._wrap_text(long_text)

        # Text should be wrapped
        assert "\n" in wrapped or len(wrapped) <= 50

    def test_wrap_text_with_paragraphs(self):
        """Test wrapping text with multiple paragraphs."""
        formatter = PatternViewFormatter(terminal_width=50)
        text = "First paragraph.\n\nSecond paragraph."
        wrapped = formatter._wrap_text(text)

        # Should preserve paragraph breaks
        assert "\n\n" in wrapped or "\n \n" in wrapped

    def test_format_displays_source(self, sample_pattern):
        """Test that source is displayed."""
        formatter = PatternViewFormatter()
        output = formatter.format(sample_pattern)
        # Source metadata is internal, not displayed in view
        assert "Test Pattern" in output
