"""
Tests for text formatting utilities.

Tests the shared text utility functions used across all formatters.
"""

import pytest
from patternsphere.cli.formatters.text_utils import (
    wrap_text,
    truncate_text,
    indent_lines,
    format_list,
    center_text,
    create_separator
)


class TestWrapText:
    """Tests for wrap_text function."""

    def test_wrap_text_basic(self):
        """Test basic text wrapping."""
        text = "This is a very long text that should be wrapped to fit within the specified width limit."
        wrapped = wrap_text(text, width=30)

        # Should contain newlines
        assert "\n" in wrapped
        # Each line should be <= 30 chars
        for line in wrapped.split("\n"):
            assert len(line) <= 30

    def test_wrap_text_short_text(self):
        """Test wrapping text that's already short."""
        text = "Short text"
        wrapped = wrap_text(text, width=50)

        # Should not add newlines
        assert wrapped == text

    def test_wrap_text_with_indent(self):
        """Test wrapping with indentation."""
        text = "This is a long text that needs wrapping with indentation applied."
        wrapped = wrap_text(text, width=30, indent=4)

        # All lines should start with 4 spaces
        for line in wrapped.split("\n"):
            if line:  # Skip empty lines
                assert line.startswith("    ")

    def test_wrap_text_preserves_paragraphs(self):
        """Test that paragraph breaks are preserved."""
        text = "First paragraph.\n\nSecond paragraph."
        wrapped = wrap_text(text, width=50)

        # Should preserve double newline
        assert "\n\n" in wrapped

    def test_wrap_text_empty_string(self):
        """Test wrapping empty string."""
        wrapped = wrap_text("", width=50)
        assert wrapped == ""

    def test_wrap_text_single_word_longer_than_width(self):
        """Test wrapping when a single word is longer than width."""
        text = "Supercalifragilisticexpialidocious"
        wrapped = wrap_text(text, width=10)

        # Should still wrap (word gets its own line)
        assert wrapped == text

    def test_wrap_text_multiple_paragraphs(self):
        """Test wrapping multiple paragraphs."""
        text = "Para 1 line 1.\nPara 1 line 2.\n\nPara 2 line 1."
        wrapped = wrap_text(text, width=20)

        # Should preserve paragraph structure
        assert "\n\n" in wrapped

    def test_wrap_text_width_too_small(self):
        """Test wrapping with very small width."""
        text = "Test text here"
        wrapped = wrap_text(text, width=5, indent=0)

        # Should use minimum reasonable width
        assert wrapped is not None


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_truncate_text_short_text(self):
        """Test truncating text that's already short."""
        text = "Short text"
        truncated = truncate_text(text, 100)

        # Should not be truncated
        assert truncated == text

    def test_truncate_text_long_text(self):
        """Test truncating long text."""
        text = "A" * 200
        truncated = truncate_text(text, 100)

        # Should be exactly 100 chars
        assert len(truncated) == 100
        # Should end with ellipsis
        assert truncated.endswith("...")
        # Content should be truncated
        assert truncated[:97] == "A" * 97

    def test_truncate_text_exact_length(self):
        """Test text that's exactly max_length."""
        text = "A" * 100
        truncated = truncate_text(text, 100)

        # Should not be truncated
        assert truncated == text

    def test_truncate_text_custom_suffix(self):
        """Test truncating with custom suffix."""
        text = "A" * 100
        truncated = truncate_text(text, 50, suffix="[...]")

        # Should be exactly 50 chars
        assert len(truncated) == 50
        # Should end with custom suffix
        assert truncated.endswith("[...]")

    def test_truncate_text_max_length_smaller_than_suffix(self):
        """Test when max_length is smaller than suffix."""
        text = "Test text here"
        truncated = truncate_text(text, 2, suffix="...")

        # Should return truncated suffix
        assert truncated == ".."
        assert len(truncated) == 2

    def test_truncate_text_empty_string(self):
        """Test truncating empty string."""
        truncated = truncate_text("", 10)
        assert truncated == ""

    def test_truncate_text_unicode(self):
        """Test truncating text with unicode characters."""
        text = "한글 텍스트입니다" * 10
        truncated = truncate_text(text, 20)

        assert len(truncated) == 20
        assert truncated.endswith("...")


class TestIndentLines:
    """Tests for indent_lines function."""

    def test_indent_lines_single_line(self):
        """Test indenting single line."""
        text = "Single line"
        indented = indent_lines(text, indent=2)

        assert indented == "  Single line"

    def test_indent_lines_multiple_lines(self):
        """Test indenting multiple lines."""
        text = "Line 1\nLine 2\nLine 3"
        indented = indent_lines(text, indent=4)

        lines = indented.split("\n")
        assert len(lines) == 3
        for line in lines:
            assert line.startswith("    ")

    def test_indent_lines_empty_string(self):
        """Test indenting empty string."""
        indented = indent_lines("", indent=2)
        assert indented == ""

    def test_indent_lines_with_empty_lines(self):
        """Test indenting text with empty lines."""
        text = "Line 1\n\nLine 3"
        indented = indent_lines(text, indent=2)

        lines = indented.split("\n")
        assert lines[0] == "  Line 1"
        assert lines[1] == "  "  # Empty line also gets indent
        assert lines[2] == "  Line 3"

    def test_indent_lines_zero_indent(self):
        """Test with zero indentation."""
        text = "Test line"
        indented = indent_lines(text, indent=0)

        assert indented == text

    def test_indent_lines_large_indent(self):
        """Test with large indentation."""
        text = "Test"
        indented = indent_lines(text, indent=10)

        assert indented == " " * 10 + "Test"


class TestFormatList:
    """Tests for format_list function."""

    def test_format_list_basic(self):
        """Test basic list formatting."""
        items = ["Item 1", "Item 2", "Item 3"]
        formatted = format_list(items)

        lines = formatted.split("\n")
        assert len(lines) == 3
        assert lines[0] == "  - Item 1"
        assert lines[1] == "  - Item 2"
        assert lines[2] == "  - Item 3"

    def test_format_list_empty(self):
        """Test formatting empty list."""
        formatted = format_list([])
        assert formatted == ""

    def test_format_list_custom_bullet(self):
        """Test formatting with custom bullet."""
        items = ["One", "Two"]
        formatted = format_list(items, bullet="*")

        lines = formatted.split("\n")
        assert lines[0] == "  * One"
        assert lines[1] == "  * Two"

    def test_format_list_custom_indent(self):
        """Test formatting with custom indentation."""
        items = ["A", "B"]
        formatted = format_list(items, indent=4)

        lines = formatted.split("\n")
        assert lines[0] == "    - A"
        assert lines[1] == "    - B"

    def test_format_list_numbered(self):
        """Test formatting with numbered bullets."""
        items = ["First", "Second", "Third"]
        formatted = format_list(items, bullet="1.")

        lines = formatted.split("\n")
        assert lines[0] == "  1. First"
        assert lines[1] == "  1. Second"  # Uses same bullet
        assert lines[2] == "  1. Third"

    def test_format_list_single_item(self):
        """Test formatting single item."""
        items = ["Only item"]
        formatted = format_list(items)

        assert formatted == "  - Only item"


class TestCenterText:
    """Tests for center_text function."""

    def test_center_text_basic(self):
        """Test basic text centering."""
        text = "Title"
        centered = center_text(text, width=11)

        assert len(centered) == 11
        assert centered == "   Title   "

    def test_center_text_even_padding(self):
        """Test centering with even padding."""
        text = "Test"
        centered = center_text(text, width=10)

        assert len(centered) == 10
        assert centered.strip() == text

    def test_center_text_odd_padding(self):
        """Test centering with odd padding."""
        text = "Hi"
        centered = center_text(text, width=7)

        assert len(centered) == 7
        # Left padding might be one less than right
        assert "Hi" in centered

    def test_center_text_exact_width(self):
        """Test text that's exactly the width."""
        text = "Exact"
        centered = center_text(text, width=5)

        assert centered == text

    def test_center_text_longer_than_width(self):
        """Test text longer than width."""
        text = "Very long text"
        centered = center_text(text, width=5)

        # Should return original text
        assert centered == text

    def test_center_text_custom_fill_char(self):
        """Test centering with custom fill character."""
        text = "Test"
        centered = center_text(text, width=10, fill_char="=")

        assert len(centered) == 10
        assert centered.strip("=") == text
        assert "=" in centered

    def test_center_text_empty_string(self):
        """Test centering empty string."""
        centered = center_text("", width=10)

        assert len(centered) == 10
        assert centered == " " * 10


class TestCreateSeparator:
    """Tests for create_separator function."""

    def test_create_separator_basic(self):
        """Test basic separator creation."""
        separator = create_separator(width=10)

        assert separator == "-" * 10
        assert len(separator) == 10

    def test_create_separator_custom_char(self):
        """Test separator with custom character."""
        separator = create_separator(width=20, char="=")

        assert separator == "=" * 20
        assert len(separator) == 20

    def test_create_separator_various_chars(self):
        """Test separator with various characters."""
        chars = ["*", "#", "_", "~", "+"]

        for char in chars:
            separator = create_separator(width=15, char=char)
            assert separator == char * 15

    def test_create_separator_default_width(self):
        """Test separator with default width."""
        separator = create_separator()

        assert len(separator) == 80
        assert separator == "-" * 80

    def test_create_separator_zero_width(self):
        """Test separator with zero width."""
        separator = create_separator(width=0)

        assert separator == ""

    def test_create_separator_single_char(self):
        """Test separator with width of 1."""
        separator = create_separator(width=1, char="X")

        assert separator == "X"


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_formatted_section_creation(self):
        """Test creating a formatted section with multiple utilities."""
        title = "Test Section"
        content = "This is a long piece of text that needs to be wrapped and formatted properly."

        # Create formatted section
        separator = create_separator(width=50, char="=")
        centered_title = center_text(title, width=50)
        wrapped_content = wrap_text(content, width=50, indent=2)

        section = f"{separator}\n{centered_title}\n{separator}\n{wrapped_content}"

        # Verify structure
        lines = section.split("\n")
        assert lines[0] == "=" * 50
        assert "Test Section" in lines[1]
        assert lines[2] == "=" * 50
        assert all(len(line) <= 50 for line in lines if line)

    def test_list_with_wrapped_items(self):
        """Test formatting list with wrapped long items."""
        items = [
            "This is a very long item that needs wrapping",
            "Short item",
            "Another long item that will definitely need to be wrapped"
        ]

        # Format and wrap
        formatted_items = []
        for item in items:
            truncated = truncate_text(item, 40)
            formatted_items.append(truncated)

        result = format_list(formatted_items, indent=2)

        lines = result.split("\n")
        assert len(lines) == 3
        for line in lines:
            assert len(line) <= 44  # 2 indent + 2 "- " + 40 text

    def test_complex_formatting_pipeline(self):
        """Test complex formatting pipeline."""
        # Simulate formatting a pattern section
        raw_text = "This is a very long description of a pattern that includes multiple sentences and needs proper formatting."

        # Process through pipeline
        truncated = truncate_text(raw_text, 80)
        wrapped = wrap_text(truncated, width=60, indent=4)

        # Verify result
        assert len(truncated) <= 80
        for line in wrapped.split("\n"):
            assert len(line) <= 60
            if line.strip():
                assert line.startswith("    ")
