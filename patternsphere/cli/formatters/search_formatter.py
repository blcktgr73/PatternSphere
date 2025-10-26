"""
Search results formatter.

Formats search results for terminal display with optional Rich formatting.
"""

from typing import List
from patternsphere.search import SearchResult
from patternsphere.config import settings


class SearchResultsFormatter:
    """
    Formats search results for terminal display.

    Design Principle: Single Responsibility
    - Only responsible for formatting search results
    - Delegates actual searching to SearchEngine

    Features:
    - Terminal width awareness
    - Text truncation for long content
    - Rich formatting support (fallback to plain text)
    - Result numbering
    - Score display
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

    def format(self, results: List[SearchResult], show_scores: bool = True) -> str:
        """
        Format search results as a string.

        Args:
            results: List of search results to format
            show_scores: Whether to display relevance scores

        Returns:
            Formatted string ready for display
        """
        if not results:
            return "No patterns found matching your search criteria."

        output_lines = []
        output_lines.append(f"Found {len(results)} pattern(s):\n")

        for idx, result in enumerate(results, 1):
            output_lines.append(self._format_result(idx, result, show_scores))
            if idx < len(results):
                output_lines.append("")  # Blank line between results

        return "\n".join(output_lines)

    def _format_result(self, index: int, result: SearchResult, show_scores: bool) -> str:
        """
        Format a single search result.

        Args:
            index: Result number (1-based)
            result: SearchResult to format
            show_scores: Whether to show relevance score

        Returns:
            Formatted result string
        """
        pattern = result.pattern
        lines = []

        # Header line with number, name, and optional score
        if show_scores:
            header = f"{index}. {pattern.name} (score: {result.score:.1f})"
        else:
            header = f"{index}. {pattern.name}"
        lines.append(header)

        # Category and tags
        tags_str = ", ".join(pattern.tags[:5])  # Show first 5 tags
        lines.append(f"   Category: {pattern.category}")
        lines.append(f"   Tags: {tags_str}")

        # Intent (truncated if too long)
        intent_preview = self._truncate_text(pattern.intent, 100)
        lines.append(f"   Intent: {intent_preview}")

        # Matched fields (if available)
        if result.matched_fields:
            matched = ", ".join(sorted(result.matched_fields))
            lines.append(f"   Matched in: {matched}")

        return "\n".join(lines)

    def _truncate_text(self, text: str, max_length: int) -> str:
        """
        Truncate text to maximum length, adding ellipsis if needed.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    def format_summary(self, results: List[SearchResult]) -> str:
        """
        Format a brief summary of search results.

        Args:
            results: List of search results

        Returns:
            Summary string
        """
        if not results:
            return "No results found."

        categories = set(r.pattern.category for r in results)
        avg_score = sum(r.score for r in results) / len(results) if results else 0

        lines = [
            f"Results: {len(results)} pattern(s)",
            f"Categories: {len(categories)}",
            f"Average score: {avg_score:.1f}"
        ]

        return "\n".join(lines)

    def format_compact(self, results: List[SearchResult], limit: int = 10) -> str:
        """
        Format results in compact mode (name and score only).

        Args:
            results: List of search results
            limit: Maximum number of results to show

        Returns:
            Compact formatted string
        """
        if not results:
            return "No patterns found."

        output_lines = [f"Found {len(results)} pattern(s):\n"]

        for idx, result in enumerate(results[:limit], 1):
            line = f"{idx}. {result.pattern.name} ({result.score:.1f})"
            output_lines.append(line)

        if len(results) > limit:
            output_lines.append(f"\n... and {len(results) - limit} more")

        return "\n".join(output_lines)
