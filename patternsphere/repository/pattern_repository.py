"""
Pattern repository implementation for PatternSphere.

This module implements the IPatternRepository interface with in-memory storage
and optional persistence through the storage layer.

Design Principles Applied:
- Single Responsibility: Manages pattern collection and queries
- Dependency Inversion: Depends on IStorage abstraction
- Open/Closed: Extensible through inheritance
- Performance: Multiple indexes for fast lookups
"""

import logging
from collections import defaultdict
from typing import List, Optional, Dict

from patternsphere.models.pattern import Pattern
from patternsphere.repository.repository_interface import (
    IPatternRepository,
    RepositoryError
)
from patternsphere.storage.storage_interface import IStorage, StorageError


logger = logging.getLogger(__name__)


class InMemoryPatternRepository(IPatternRepository):
    """
    In-memory pattern repository with optional persistence.

    This implementation provides fast pattern access through multiple indexes:
    - ID index: O(1) lookup by pattern ID
    - Name index: O(1) lookup by pattern name
    - Category index: O(1) lookup by category

    Supports persistence through an optional storage backend following
    the Dependency Inversion principle.

    Attributes:
        storage: Optional storage backend for persistence
        patterns: Primary storage indexed by pattern ID
        name_index: Index mapping pattern names to IDs
        category_index: Index mapping categories to pattern IDs
    """

    def __init__(self, storage: Optional[IStorage] = None):
        """
        Initialize repository.

        Args:
            storage: Optional storage backend for persistence
        """
        self.storage = storage
        self._patterns: Dict[str, Pattern] = {}
        self._name_index: Dict[str, str] = {}  # name -> pattern_id
        self._category_index: Dict[str, List[str]] = defaultdict(list)

        logger.info("InMemoryPatternRepository initialized")

        # Load patterns from storage if available
        if self.storage:
            self._load_from_storage()

    def add_pattern(self, pattern: Pattern) -> None:
        """
        Add a pattern to the repository.

        Updates all indexes to maintain consistency.

        Args:
            pattern: Pattern to add

        Raises:
            RepositoryError: If pattern with same ID already exists
        """
        if pattern.id in self._patterns:
            raise RepositoryError(
                f"Pattern with ID '{pattern.id}' already exists"
            )

        # Check for name collision
        if pattern.name in self._name_index:
            existing_id = self._name_index[pattern.name]
            raise RepositoryError(
                f"Pattern with name '{pattern.name}' already exists "
                f"(ID: {existing_id})"
            )

        # Add to primary storage
        self._patterns[pattern.id] = pattern

        # Update indexes
        self._name_index[pattern.name] = pattern.id
        self._category_index[pattern.category].append(pattern.id)

        logger.debug(f"Added pattern: {pattern.name} (ID: {pattern.id})")

    def get_pattern_by_id(self, pattern_id: str) -> Optional[Pattern]:
        """
        Retrieve a pattern by its ID.

        Args:
            pattern_id: Unique pattern identifier

        Returns:
            Pattern if found, None otherwise
        """
        return self._patterns.get(pattern_id)

    def get_pattern_by_name(self, name: str) -> Optional[Pattern]:
        """
        Retrieve a pattern by its name.

        Args:
            name: Pattern name (case-sensitive)

        Returns:
            Pattern if found, None otherwise
        """
        pattern_id = self._name_index.get(name)
        if pattern_id:
            return self._patterns.get(pattern_id)
        return None

    def list_all_patterns(self) -> List[Pattern]:
        """
        List all patterns in the repository.

        Returns:
            List of all patterns (sorted by name)
        """
        patterns = list(self._patterns.values())
        patterns.sort(key=lambda p: p.name)
        return patterns

    def get_patterns_by_category(self, category: str) -> List[Pattern]:
        """
        Get all patterns in a specific category.

        Args:
            category: Category name

        Returns:
            List of patterns in the category (sorted by name)
        """
        pattern_ids = self._category_index.get(category, [])
        patterns = [
            self._patterns[pid]
            for pid in pattern_ids
            if pid in self._patterns
        ]
        patterns.sort(key=lambda p: p.name)
        return patterns

    def get_all_categories(self) -> Dict[str, int]:
        """
        Get all categories with pattern counts.

        Returns:
            Dictionary mapping category names to pattern counts
        """
        return {
            category: len(pattern_ids)
            for category, pattern_ids in self._category_index.items()
        }

    def search_patterns(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Pattern]:
        """
        Search patterns with optional filters.

        Args:
            query: Search query string (searches name, intent, problem, solution)
            category: Optional category filter
            tags: Optional list of tags to filter by (OR logic)

        Returns:
            List of matching patterns (sorted by relevance, then name)
        """
        # Start with all patterns or category-filtered patterns
        if category:
            patterns = self.get_patterns_by_category(category)
        else:
            patterns = list(self._patterns.values())

        # Filter by tags if specified (OR logic - match any tag)
        if tags:
            tags_lower = [tag.lower() for tag in tags]
            patterns = [
                p for p in patterns
                if any(p.has_tag(tag) for tag in tags_lower)
            ]

        # Filter by search query if specified
        if query:
            patterns = [
                p for p in patterns
                if p.matches_search_query(query)
            ]

        # Sort by name (relevance ranking could be added later)
        patterns.sort(key=lambda p: p.name)

        return patterns

    def count(self) -> int:
        """
        Get total number of patterns in repository.

        Returns:
            Number of patterns
        """
        return len(self._patterns)

    def clear(self) -> None:
        """
        Remove all patterns from the repository.

        Clears all indexes and primary storage.
        """
        self._patterns.clear()
        self._name_index.clear()
        self._category_index.clear()
        logger.info("Repository cleared")

    def save_to_storage(self) -> None:
        """
        Persist patterns to storage backend.

        Raises:
            RepositoryError: If no storage backend configured or save fails
        """
        if not self.storage:
            raise RepositoryError("No storage backend configured")

        try:
            # Convert patterns to dictionaries
            pattern_dicts = [
                pattern.to_dict()
                for pattern in self._patterns.values()
            ]

            # Save to storage
            self.storage.save_patterns(pattern_dicts)
            logger.info(f"Saved {len(pattern_dicts)} patterns to storage")

        except StorageError as e:
            logger.error(f"Failed to save to storage: {e}", exc_info=True)
            raise RepositoryError(
                f"Failed to save patterns to storage: {e}",
                cause=e
            )

    def _load_from_storage(self) -> None:
        """
        Load patterns from storage backend.

        This is called automatically during initialization if storage is configured.

        Raises:
            RepositoryError: If load fails
        """
        try:
            pattern_dicts = self.storage.load_patterns()

            for pattern_dict in pattern_dicts:
                try:
                    pattern = Pattern.from_dict(pattern_dict)
                    self.add_pattern(pattern)
                except Exception as e:
                    logger.warning(
                        f"Failed to load pattern {pattern_dict.get('name', 'unknown')}: {e}"
                    )
                    # Continue loading other patterns

            logger.info(
                f"Loaded {len(self._patterns)} patterns from storage"
            )

        except StorageError as e:
            logger.error(f"Failed to load from storage: {e}", exc_info=True)
            raise RepositoryError(
                f"Failed to load patterns from storage: {e}",
                cause=e
            )

    def get_repository_stats(self) -> Dict[str, any]:
        """
        Get repository statistics.

        Returns:
            Dictionary with repository statistics
        """
        return {
            "total_patterns": len(self._patterns),
            "total_categories": len(self._category_index),
            "categories": self.get_all_categories(),
            "has_storage": self.storage is not None,
        }

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"InMemoryPatternRepository("
            f"patterns={len(self._patterns)}, "
            f"categories={len(self._category_index)}, "
            f"has_storage={self.storage is not None})"
        )
