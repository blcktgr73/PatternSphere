"""
Pattern detail view formatter.

Formats complete pattern details for terminal display.
"""

from patternsphere.models import Pattern
from patternsphere.config import settings


class PatternViewFormatter:
    """
    Formats pattern details for terminal display.

    Design Principle: Single Responsibility
    - Only responsible for formatting pattern details
    - Clean separation from pattern data model

    Features:
    - Complete pattern information display
    - Section-based layout
    - Terminal width awareness
    - Related patterns display
    """

    def __init__(self, terminal_width: int = 80, use_rich: bool = True):
        """
        Initialize the formatter.

        Args:
            terminal_width: Maximum width for output
            use_rich: Whether to use Rich library for formatting
        """
        self.terminal_width = terminal_width
        self.use_rich = use_rich

    def format(self, pattern: Pattern) -> str:
        """
        Format complete pattern details.

        Args:
            pattern: Pattern to format

        Returns:
            Formatted string ready for display
        """
        lines = []

        # Header
        lines.append("=" * min(self.terminal_width, 80))
        lines.append(f"Pattern: {pattern.name}")
        lines.append("=" * min(self.terminal_width, 80))
        lines.append("")

        # Metadata section
        lines.append("METADATA")
        lines.append("-" * 40)
        lines.append(f"ID: {pattern.id}")
        lines.append(f"Category: {pattern.category}")
        lines.append(f"Tags: {', '.join(pattern.tags)}")
        if pattern.source_metadata:
            lines.append(f"Source: {pattern.source_metadata.source_name}")
        lines.append("")

        # Intent section
        lines.append("INTENT")
        lines.append("-" * 40)
        lines.append(self._wrap_text(pattern.intent))
        lines.append("")

        # Problem section
        lines.append("PROBLEM")
        lines.append("-" * 40)
        lines.append(self._wrap_text(pattern.problem))
        lines.append("")

        # Solution section
        lines.append("SOLUTION")
        lines.append("-" * 40)
        lines.append(self._wrap_text(pattern.solution))
        lines.append("")

        # Consequences section
        if pattern.consequences:
            lines.append("CONSEQUENCES")
            lines.append("-" * 40)
            lines.append(self._wrap_text(pattern.consequences))
            lines.append("")

        # Related patterns section
        if pattern.related_patterns:
            lines.append("RELATED PATTERNS")
            lines.append("-" * 40)
            for related in pattern.related_patterns:
                lines.append(f"  - {related}")
            lines.append("")

        lines.append("=" * min(self.terminal_width, 80))

        return "\n".join(lines)

    def _wrap_text(self, text: str, indent: int = 0) -> str:
        """
        Wrap text to terminal width.

        Args:
            text: Text to wrap
            indent: Number of spaces to indent

        Returns:
            Wrapped text
        """
        # Simple line-based wrapping
        # For production, could use textwrap module
        max_width = min(self.terminal_width, 80) - indent

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
                if len(current_line.strip()) + len(word) + 1 <= max_width:
                    if current_line.strip():
                        current_line += " " + word
                    else:
                        current_line = " " * indent + word
                else:
                    if current_line.strip():
                        lines.append(current_line)
                    current_line = " " * indent + word

            if current_line.strip():
                lines.append(current_line)

            wrapped_paragraphs.append("\n".join(lines))

        return "\n".join(wrapped_paragraphs)

    def format_compact(self, pattern: Pattern) -> str:
        """
        Format pattern in compact mode (metadata and intent only).

        Args:
            pattern: Pattern to format

        Returns:
            Compact formatted string
        """
        lines = []
        lines.append(f"Pattern: {pattern.name}")
        lines.append(f"Category: {pattern.category}")
        lines.append(f"Tags: {', '.join(pattern.tags[:5])}")
        lines.append("")
        lines.append(f"Intent: {pattern.intent[:200]}...")

        return "\n".join(lines)
