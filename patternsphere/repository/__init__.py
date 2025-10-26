"""
Repository module for PatternSphere.

Implements the Repository pattern for pattern data access.
"""

from patternsphere.repository.repository_interface import (
    IPatternRepository,
    RepositoryError
)
from patternsphere.repository.pattern_repository import InMemoryPatternRepository

__all__ = ["IPatternRepository", "RepositoryError", "InMemoryPatternRepository"]
