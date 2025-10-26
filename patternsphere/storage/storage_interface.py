"""
Storage interface for PatternSphere.

This module defines the abstract storage interface following SOLID principles:
- Interface Segregation: Focused interface for storage operations
- Dependency Inversion: High-level modules depend on this abstraction
- Open/Closed: Can be extended with new storage backends without modification
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IStorage(ABC):
    """
    Abstract storage interface for pattern data persistence.

    This interface defines the contract for all storage backends,
    enabling dependency inversion and facilitating testing through mocking.

    Implementations must support atomic write operations to prevent data corruption.
    """

    @abstractmethod
    def save_patterns(self, patterns: List[Dict[str, Any]]) -> None:
        """
        Save patterns to storage.

        Args:
            patterns: List of pattern dictionaries to save

        Raises:
            StorageError: If save operation fails
        """
        pass

    @abstractmethod
    def load_patterns(self) -> List[Dict[str, Any]]:
        """
        Load patterns from storage.

        Returns:
            List of pattern dictionaries

        Raises:
            StorageError: If load operation fails
        """
        pass

    @abstractmethod
    def exists(self) -> bool:
        """
        Check if storage exists.

        Returns:
            True if storage exists and is accessible
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all patterns from storage.

        Raises:
            StorageError: If clear operation fails
        """
        pass


class StorageError(Exception):
    """
    Exception raised for storage-related errors.

    This exception provides a clear separation between storage errors
    and other application errors, following the fail-fast principle.
    """

    def __init__(self, message: str, cause: Exception = None):
        """
        Initialize StorageError.

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
