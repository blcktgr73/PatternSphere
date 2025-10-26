"""
Repository interface for PatternSphere.

This module defines the abstract repository interface following SOLID principles:
- Single Responsibility: Repository handles pattern data access logic only
- Interface Segregation: Focused interface for pattern operations
- Dependency Inversion: Services depend on this abstraction, not concrete implementations
- Open/Closed: Can be extended with new repository implementations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from patternsphere.models.pattern import Pattern


class IPatternRepository(ABC):
    """
    Abstract repository interface for pattern data access.

    This interface defines the contract for all pattern repository implementations,
    enabling dependency inversion and facilitating testing through mocking.

    The repository pattern provides a collection-like interface to domain objects,
    abstracting data access details from business logic.
    """

    @abstractmethod
    def add_pattern(self, pattern: Pattern) -> None:
        """
        Add a pattern to the repository.

        Args:
            pattern: Pattern to add

        Raises:
            RepositoryError: If pattern with same ID already exists
        """
        pass

    @abstractmethod
    def get_pattern_by_id(self, pattern_id: str) -> Optional[Pattern]:
        """
        Retrieve a pattern by its ID.

        Args:
            pattern_id: Unique pattern identifier

        Returns:
            Pattern if found, None otherwise
        """
        pass

    @abstractmethod
    def get_pattern_by_name(self, name: str) -> Optional[Pattern]:
        """
        Retrieve a pattern by its name.

        Args:
            name: Pattern name (case-sensitive)

        Returns:
            Pattern if found, None otherwise
        """
        pass

    @abstractmethod
    def list_all_patterns(self) -> List[Pattern]:
        """
        List all patterns in the repository.

        Returns:
            List of all patterns
        """
        pass

    @abstractmethod
    def get_patterns_by_category(self, category: str) -> List[Pattern]:
        """
        Get all patterns in a specific category.

        Args:
            category: Category name

        Returns:
            List of patterns in the category
        """
        pass

    @abstractmethod
    def get_all_categories(self) -> Dict[str, int]:
        """
        Get all categories with pattern counts.

        Returns:
            Dictionary mapping category names to pattern counts
        """
        pass

    @abstractmethod
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
            List of matching patterns
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get total number of patterns in repository.

        Returns:
            Number of patterns
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all patterns from the repository.

        This is primarily used for testing purposes.
        """
        pass


class RepositoryError(Exception):
    """
    Exception raised for repository-related errors.

    This exception provides clear separation between repository errors
    and other application errors.
    """

    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize RepositoryError.

        Args:
            message: Error message describing what went wrong
            cause: Optional underlying exception that caused this error
        """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """String representation of error."""
        if self.cause:
            return f"{super().__str__()} (caused by: {self.cause})"
        return super().__str__()
