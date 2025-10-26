"""
Search engine for PatternSphere.

This module implements a keyword-based search engine with weighted scoring
and filtering capabilities.

Design Principles Applied:
- Single Responsibility: Focuses only on search functionality
- Dependency Inversion: Depends on IPatternRepository abstraction
- Strategy Pattern: Scoring algorithm is encapsulated and extensible
- Open/Closed: Can be extended with new scoring strategies
"""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional, Set

from patternsphere.models.pattern import Pattern
from patternsphere.repository.repository_interface import IPatternRepository


logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """
    Search result containing a pattern and its relevance score.

    Attributes:
        pattern: The pattern that matched the search
        score: Relevance score (higher is better)
        matched_fields: Set of field names that contributed to the match
    """
    pattern: Pattern
    score: float
    matched_fields: Set[str] = field(default_factory=set)

    def __str__(self) -> str:
        """Human-readable string representation."""
        fields_str = ", ".join(sorted(self.matched_fields))
        return (
            f"SearchResult(pattern='{self.pattern.name}', "
            f"score={self.score:.2f}, "
            f"matched_fields=[{fields_str}])"
        )

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return self.__str__()


class KeywordSearchEngine:
    """
    Keyword-based search engine with weighted field scoring.

    This search engine implements a weighted scoring algorithm where matches
    in different fields contribute different amounts to the total score:

    Field Weights:
    - name: 5.0 (highest priority)
    - tags: 4.0
    - intent: 3.0
    - category: 2.5
    - problem: 2.0
    - solution: 1.5

    Match Types:
    - Exact word match: 1.0 points
    - Partial match: 0.5 points

    The search is case-insensitive and supports filtering by category and tags.

    Attributes:
        repository: Pattern repository to search
    """

    # Field weights for scoring (following technical design)
    FIELD_WEIGHTS = {
        'name': 5.0,
        'intent': 3.0,
        'problem': 2.0,
        'solution': 1.5,
        'tags': 4.0,
        'category': 2.5
    }

    # Match type scores
    EXACT_MATCH_SCORE = 1.0
    PARTIAL_MATCH_SCORE = 0.5

    def __init__(self, repository: IPatternRepository):
        """
        Initialize search engine.

        Args:
            repository: Pattern repository to search
        """
        self.repository = repository
        logger.info("KeywordSearchEngine initialized")

    def search(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Search patterns with keyword matching and optional filters.

        Args:
            query: Search query string (case-insensitive, space-separated keywords)
            category: Optional category filter
            tags: Optional list of tags to filter by (OR logic - match any tag)

        Returns:
            List of SearchResult objects sorted by score (highest first)
        """
        start_time = time.perf_counter()

        # Get base set of patterns (apply category filter first)
        if category:
            patterns = self.repository.get_patterns_by_category(category)
            logger.debug(f"Filtered to {len(patterns)} patterns in category '{category}'")
        else:
            patterns = self.repository.list_all_patterns()
            logger.debug(f"Searching across {len(patterns)} patterns")

        # Apply tag filter if specified
        if tags:
            patterns = self._filter_by_tags(patterns, tags)
            logger.debug(f"After tag filter: {len(patterns)} patterns")

        # If no query, return all filtered patterns with zero score
        if not query or not query.strip():
            results = [
                SearchResult(pattern=p, score=0.0, matched_fields=set())
                for p in patterns
            ]
            # Sort by name for consistent ordering
            results.sort(key=lambda r: r.pattern.name)

            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                f"Search complete: {len(results)} results in {duration_ms:.2f}ms "
                f"(no query, filters only)"
            )
            return results

        # Score each pattern based on query match
        results = []
        query_terms = self._normalize_query(query)

        for pattern in patterns:
            score, matched_fields = self._score_pattern(pattern, query_terms)

            if score > 0:  # Only include patterns with matches
                results.append(
                    SearchResult(
                        pattern=pattern,
                        score=score,
                        matched_fields=matched_fields
                    )
                )

        # Sort by score (descending), then by name for ties
        results.sort(key=lambda r: (-r.score, r.pattern.name))

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"Search complete: {len(results)} results in {duration_ms:.2f}ms "
            f"(query: '{query}')"
        )

        return results

    def _normalize_query(self, query: str) -> List[str]:
        """
        Normalize query into searchable terms.

        Args:
            query: Raw query string

        Returns:
            List of normalized search terms (lowercase, stripped)
        """
        # Split on whitespace and normalize
        terms = [term.strip().lower() for term in query.split()]
        # Remove empty terms
        terms = [t for t in terms if t]
        return terms

    def _score_pattern(
        self,
        pattern: Pattern,
        query_terms: List[str]
    ) -> tuple[float, Set[str]]:
        """
        Score a pattern against query terms.

        Calculates weighted score based on matches in different fields.

        Args:
            pattern: Pattern to score
            query_terms: Normalized query terms

        Returns:
            Tuple of (total_score, matched_fields)
        """
        total_score = 0.0
        matched_fields = set()

        # Check each searchable field
        for field_name, weight in self.FIELD_WEIGHTS.items():
            field_score = self._score_field(
                pattern,
                field_name,
                query_terms
            )

            if field_score > 0:
                total_score += field_score * weight
                matched_fields.add(field_name)

        return total_score, matched_fields

    def _score_field(
        self,
        pattern: Pattern,
        field_name: str,
        query_terms: List[str]
    ) -> float:
        """
        Score a single field against query terms.

        Args:
            pattern: Pattern to score
            field_name: Name of field to check
            query_terms: Normalized query terms

        Returns:
            Field score (before applying weight)
        """
        # Get field value
        if field_name == 'tags':
            # Tags are a list
            field_text = " ".join(pattern.tags).lower()
        else:
            # Other fields are strings
            field_value = getattr(pattern, field_name, "")
            field_text = field_value.lower()

        if not field_text:
            return 0.0

        # Split field into words for exact matching
        field_words = set(field_text.split())

        # Score each query term
        field_score = 0.0

        for term in query_terms:
            # Check for exact word match
            if term in field_words:
                field_score += self.EXACT_MATCH_SCORE
            # Check for partial match (substring)
            elif term in field_text:
                field_score += self.PARTIAL_MATCH_SCORE

        return field_score

    def _filter_by_tags(
        self,
        patterns: List[Pattern],
        tags: List[str]
    ) -> List[Pattern]:
        """
        Filter patterns by tags (OR logic - match any tag).

        Args:
            patterns: List of patterns to filter
            tags: List of tags to filter by

        Returns:
            Filtered list of patterns
        """
        if not tags:
            return patterns

        # Normalize tags to lowercase
        tags_lower = [tag.lower() for tag in tags]

        # Filter patterns that have at least one of the tags
        filtered = [
            p for p in patterns
            if any(p.has_tag(tag) for tag in tags_lower)
        ]

        return filtered

    def get_search_stats(self) -> dict:
        """
        Get statistics about the search engine.

        Returns:
            Dictionary with search engine statistics
        """
        return {
            "total_patterns": self.repository.count(),
            "field_weights": self.FIELD_WEIGHTS,
            "exact_match_score": self.EXACT_MATCH_SCORE,
            "partial_match_score": self.PARTIAL_MATCH_SCORE,
        }

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"KeywordSearchEngine("
            f"patterns={self.repository.count()})"
        )
