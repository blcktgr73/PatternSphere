"""
Common text formatting utilities.

Follows DRY (Don't Repeat Yourself) principle to eliminate duplication between formatters.

Design Principles:
- Single Responsibility: Each function handles one specific text operation
- Reusability: Shared by all formatter classes
- Testability: Pure functions, easy to test independently
"""

from typing import List
import textwrap


def wrap_text(text: str, width: int = 70, indent: int = 0) -> str:
    """
    Wrap text to specified width with optional indentation.

    Args:
        text: Text to wrap
        width: Maximum width for each line
        indent: Number of spaces to indent each line

    Returns:
        Wrapped text as a single string

    Examples:
        >>> wrap_text("This is a long text", width=10)
        'This is a\\nlong text'
        >>> wrap_text("Short", width=10, indent=2)
        '  Short'
    """
    if not text:
        return ""

    max_width = width - indent
    if max_width <= 0:
        max_width = 20  # Minimum reasonable width

    # Split into paragraphs
    paragraphs = text.split('\n')
    wrapped_paragraphs = []

    for para in paragraphs:
        if not para.strip():
            wrapped_paragraphs.append("")
            continue

        # Simple word-based wrapping
        words = para.split()
        current_line = " " * indent
        lines = []

        for word in words:
            # Check if adding this word would exceed width
            test_line = current_line.strip() + (" " if current_line.strip() else "") + word
            if len(test_line) <= max_width:
                current_line = " " * indent + test_line
            else:
                # Save current line and start new one
                if current_line.strip():
                    lines.append(current_line)
                current_line = " " * indent + word

        # Add final line
        if current_line.strip():
            lines.append(current_line)

        wrapped_paragraphs.append("\n".join(lines))

    return "\n".join(wrapped_paragraphs)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length and add suffix if needed.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated (default: "...")

    Returns:
        Truncated text with suffix if needed

    Examples:
        >>> truncate_text("This is a long text", 10)
        'This is...'
        >>> truncate_text("Short", 10)
        'Short'
    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    return text[:max_length - len(suffix)] + suffix


def indent_lines(text: str, indent: int = 2) -> str:
    """
    Add indentation to all lines of text.

    Args:
        text: Text to indent (can be multi-line)
        indent: Number of spaces to indent each line

    Returns:
        Indented text

    Examples:
        >>> indent_lines("Line 1\\nLine 2", indent=2)
        '  Line 1\\n  Line 2'
    """
    if not text:
        return ""

    indent_str = " " * indent
    lines = text.split("\n")
    return "\n".join(indent_str + line for line in lines)


def format_list(items: List[str], bullet: str = "-", indent: int = 2) -> str:
    """
    Format a list of items with bullets.

    Args:
        items: List of items to format
        bullet: Bullet character(s) to use
        indent: Number of spaces to indent

    Returns:
        Formatted list as string

    Examples:
        >>> format_list(["Item 1", "Item 2"])
        '  - Item 1\\n  - Item 2'
    """
    if not items:
        return ""

    indent_str = " " * indent
    lines = [f"{indent_str}{bullet} {item}" for item in items]
    return "\n".join(lines)


def center_text(text: str, width: int, fill_char: str = " ") -> str:
    """
    Center text within a given width.

    Args:
        text: Text to center
        width: Total width
        fill_char: Character to use for padding

    Returns:
        Centered text

    Examples:
        >>> center_text("Title", 10)
        '  Title   '
    """
    if len(text) >= width:
        return text

    total_padding = width - len(text)
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    return fill_char * left_padding + text + fill_char * right_padding


def create_separator(width: int = 80, char: str = "-") -> str:
    """
    Create a separator line.

    Args:
        width: Width of separator
        char: Character to use for separator

    Returns:
        Separator string

    Examples:
        >>> create_separator(10, "=")
        '=========='
    """
    return char * width
