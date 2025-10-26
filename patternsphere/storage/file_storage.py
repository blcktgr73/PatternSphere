"""
File-based storage implementation for PatternSphere.

This module implements the IStorage interface using JSON file storage
with atomic write operations to prevent data corruption.

Design Principles Applied:
- Single Responsibility: Handles file I/O operations only
- Dependency Inversion: Implements IStorage abstraction
- Fail-Fast: Validates data before writing
- Atomic Operations: Uses temp file + rename pattern for atomic writes
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from patternsphere.storage.storage_interface import IStorage, StorageError


logger = logging.getLogger(__name__)


class FileStorage(IStorage):
    """
    File-based storage backend using JSON format.

    This implementation provides persistent storage with the following guarantees:
    - Atomic writes using temp file + rename pattern
    - UTF-8 encoding for international character support
    - Automatic directory creation
    - Data validation before writing

    Attributes:
        storage_path: Path to the JSON storage file
    """

    def __init__(self, storage_path: str):
        """
        Initialize file storage.

        Args:
            storage_path: Path to JSON file for storage

        Raises:
            StorageError: If storage_path is invalid
        """
        if not storage_path:
            raise StorageError("Storage path cannot be empty")

        self.storage_path = Path(storage_path)
        logger.info(f"FileStorage initialized with path: {self.storage_path}")

    def save_patterns(self, patterns: List[Dict[str, Any]]) -> None:
        """
        Save patterns to JSON file using atomic write operation.

        Uses temp file + rename pattern to ensure atomicity:
        1. Write to temporary file in same directory
        2. If write succeeds, rename temp file to target file
        3. Rename is atomic on most filesystems

        Args:
            patterns: List of pattern dictionaries to save

        Raises:
            StorageError: If save operation fails
        """
        try:
            # Ensure parent directory exists
            self._ensure_directory_exists()

            # Validate that patterns is a list
            if not isinstance(patterns, list):
                raise StorageError(
                    f"Patterns must be a list, got {type(patterns).__name__}"
                )

            # Create temp file in same directory as target
            # This ensures temp file is on same filesystem (required for atomic rename)
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.storage_path.parent,
                prefix=".tmp_",
                suffix=".json"
            )

            try:
                # Write to temp file
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(patterns, f, indent=2, ensure_ascii=False)

                # Atomic rename (overwrites existing file)
                # On Windows, need to remove target first if it exists
                if os.name == 'nt' and self.storage_path.exists():
                    os.replace(temp_path, str(self.storage_path))
                else:
                    os.rename(temp_path, str(self.storage_path))

                logger.info(
                    f"Successfully saved {len(patterns)} patterns to "
                    f"{self.storage_path}"
                )

            except Exception as e:
                # Clean up temp file if rename failed
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass  # Best effort cleanup
                raise e

        except StorageError:
            raise
        except Exception as e:
            logger.error(f"Failed to save patterns: {e}", exc_info=True)
            raise StorageError(f"Failed to save patterns: {e}", cause=e)

    def load_patterns(self) -> List[Dict[str, Any]]:
        """
        Load patterns from JSON file.

        Returns:
            List of pattern dictionaries (empty list if file doesn't exist)

        Raises:
            StorageError: If load operation fails (corrupted file, permission issues)
        """
        try:
            if not self.exists():
                logger.info(
                    f"Storage file {self.storage_path} does not exist, "
                    "returning empty list"
                )
                return []

            with open(self.storage_path, 'r', encoding='utf-8') as f:
                patterns = json.load(f)

            # Validate that loaded data is a list
            if not isinstance(patterns, list):
                raise StorageError(
                    f"Storage file contains invalid data: expected list, "
                    f"got {type(patterns).__name__}"
                )

            logger.info(
                f"Successfully loaded {len(patterns)} patterns from "
                f"{self.storage_path}"
            )
            return patterns

        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse JSON from {self.storage_path}: {e}",
                exc_info=True
            )
            raise StorageError(
                f"Storage file is corrupted or contains invalid JSON: {e}",
                cause=e
            )
        except StorageError:
            raise
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}", exc_info=True)
            raise StorageError(f"Failed to load patterns: {e}", cause=e)

    def exists(self) -> bool:
        """
        Check if storage file exists.

        Returns:
            True if storage file exists and is a file
        """
        return self.storage_path.exists() and self.storage_path.is_file()

    def clear(self) -> None:
        """
        Clear storage by removing the file.

        Raises:
            StorageError: If clear operation fails
        """
        try:
            if self.exists():
                self.storage_path.unlink()
                logger.info(f"Cleared storage at {self.storage_path}")
            else:
                logger.info(
                    f"Storage file {self.storage_path} does not exist, "
                    "nothing to clear"
                )
        except Exception as e:
            logger.error(f"Failed to clear storage: {e}", exc_info=True)
            raise StorageError(f"Failed to clear storage: {e}", cause=e)

    def _ensure_directory_exists(self) -> None:
        """
        Ensure parent directory exists, creating it if necessary.

        Raises:
            StorageError: If directory creation fails
        """
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {self.storage_path.parent}")
        except Exception as e:
            logger.error(
                f"Failed to create directory {self.storage_path.parent}: {e}",
                exc_info=True
            )
            raise StorageError(
                f"Failed to create storage directory: {e}",
                cause=e
            )

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about storage state.

        Returns:
            Dictionary with storage information (useful for debugging)
        """
        info = {
            "storage_path": str(self.storage_path),
            "exists": self.exists(),
            "parent_exists": self.storage_path.parent.exists(),
        }

        if self.exists():
            info["size_bytes"] = self.storage_path.stat().st_size
            info["modified_time"] = self.storage_path.stat().st_mtime

        return info

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"FileStorage(storage_path='{self.storage_path}')"
