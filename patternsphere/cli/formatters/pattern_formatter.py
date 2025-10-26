"""
Pattern detail view formatter.

Formats complete pattern details for terminal display.
"""

from patternsphere.models import Pattern
from patternsphere.config import settings
from patternsphere.cli.formatters.text_utils import wrap_text, truncate_text


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
        lines.append(wrap_text(pattern.intent, width=min(self.terminal_width, 80)))
        lines.append("")

        # Problem section
        lines.append("PROBLEM")
        lines.append("-" * 40)
        lines.append(wrap_text(pattern.problem, width=min(self.terminal_width, 80)))
        lines.append("")

        # Solution section
        lines.append("SOLUTION")
        lines.append("-" * 40)
        lines.append(wrap_text(pattern.solution, width=min(self.terminal_width, 80)))
        lines.append("")

        # Consequences section
        if pattern.consequences:
            lines.append("CONSEQUENCES")
            lines.append("-" * 40)
            lines.append(wrap_text(pattern.consequences, width=min(self.terminal_width, 80)))
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
        lines.append(f"Intent: {truncate_text(pattern.intent, 200)}")

        return "\n".join(lines)
