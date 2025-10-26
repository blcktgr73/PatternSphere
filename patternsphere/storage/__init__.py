"""
Storage module for PatternSphere.

Provides abstraction layer for data persistence.
"""

from patternsphere.storage.storage_interface import IStorage, StorageError
from patternsphere.storage.file_storage import FileStorage

__all__ = ["IStorage", "StorageError", "FileStorage"]
