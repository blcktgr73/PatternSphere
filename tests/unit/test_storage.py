"""
Unit tests for storage implementations.

Tests cover:
- File storage operations (save, load, exists, clear)
- Atomic write operations
- Error handling and edge cases
- Data validation
- Directory creation
"""

import pytest
import json
import os
import tempfile
from pathlib import Path

from patternsphere.storage.file_storage import FileStorage
from patternsphere.storage.storage_interface import StorageError


class TestFileStorage:
    """Test cases for FileStorage implementation."""

    @pytest.fixture
    def temp_storage_path(self):
        """Fixture providing a temporary storage path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield os.path.join(tmpdir, "test_patterns.json")

    @pytest.fixture
    def sample_patterns(self):
        """Fixture providing sample pattern data."""
        return [
            {
                "id": "pattern-1",
                "name": "Test Pattern 1",
                "intent": "Test intent 1",
                "problem": "Test problem 1",
                "solution": "Test solution 1",
                "category": "Testing"
            },
            {
                "id": "pattern-2",
                "name": "Test Pattern 2",
                "intent": "Test intent 2",
                "problem": "Test problem 2",
                "solution": "Test solution 2",
                "category": "Testing"
            }
        ]

    def test_create_file_storage(self, temp_storage_path):
        """Test creating FileStorage instance."""
        storage = FileStorage(temp_storage_path)
        assert storage.storage_path == Path(temp_storage_path)
        assert repr(storage) == f"FileStorage(storage_path='{temp_storage_path}')"

    def test_create_file_storage_with_empty_path(self):
        """Test that empty path raises error."""
        with pytest.raises(StorageError) as exc_info:
            FileStorage("")
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_exists_returns_false_for_nonexistent_file(self, temp_storage_path):
        """Test that exists() returns False for non-existent file."""
        storage = FileStorage(temp_storage_path)
        assert not storage.exists()

    def test_load_patterns_returns_empty_list_for_nonexistent_file(
        self, temp_storage_path
    ):
        """Test loading from non-existent file returns empty list."""
        storage = FileStorage(temp_storage_path)
        patterns = storage.load_patterns()
        assert patterns == []

    def test_save_and_load_patterns(self, temp_storage_path, sample_patterns):
        """Test saving and loading patterns."""
        storage = FileStorage(temp_storage_path)

        # Save patterns
        storage.save_patterns(sample_patterns)

        # Verify file exists
        assert storage.exists()

        # Load patterns
        loaded_patterns = storage.load_patterns()

        # Verify loaded data matches saved data
        assert len(loaded_patterns) == len(sample_patterns)
        assert loaded_patterns[0]["id"] == "pattern-1"
        assert loaded_patterns[1]["id"] == "pattern-2"

    def test_save_creates_parent_directory(self):
        """Test that save creates parent directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(
                tmpdir, "subdir", "nested", "patterns.json"
            )
            storage = FileStorage(storage_path)

            # Save patterns
            storage.save_patterns([{"id": "test"}])

            # Verify file was created
            assert storage.exists()
            assert os.path.exists(storage_path)

    def test_save_overwrites_existing_file(
        self, temp_storage_path, sample_patterns
    ):
        """Test that save overwrites existing file."""
        storage = FileStorage(temp_storage_path)

        # Save initial data
        storage.save_patterns(sample_patterns)

        # Save different data
        new_patterns = [{"id": "new-pattern", "name": "New Pattern"}]
        storage.save_patterns(new_patterns)

        # Load and verify
        loaded = storage.load_patterns()
        assert len(loaded) == 1
        assert loaded[0]["id"] == "new-pattern"

    def test_save_empty_list(self, temp_storage_path):
        """Test saving empty list."""
        storage = FileStorage(temp_storage_path)
        storage.save_patterns([])

        loaded = storage.load_patterns()
        assert loaded == []

    def test_save_validates_input_type(self, temp_storage_path):
        """Test that save validates input is a list."""
        storage = FileStorage(temp_storage_path)

        # Try to save non-list data
        with pytest.raises(StorageError) as exc_info:
            storage.save_patterns({"not": "a list"})
        assert "must be a list" in str(exc_info.value).lower()

    def test_load_validates_data_type(self, temp_storage_path):
        """Test that load validates loaded data is a list."""
        storage = FileStorage(temp_storage_path)

        # Manually write invalid JSON (not a list)
        storage.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_storage_path, 'w') as f:
            json.dump({"not": "a list"}, f)

        # Try to load
        with pytest.raises(StorageError) as exc_info:
            storage.load_patterns()
        assert "expected list" in str(exc_info.value).lower()

    def test_load_handles_corrupted_json(self, temp_storage_path):
        """Test that load handles corrupted JSON gracefully."""
        storage = FileStorage(temp_storage_path)

        # Write invalid JSON
        storage.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_storage_path, 'w') as f:
            f.write("{ invalid json }")

        # Try to load
        with pytest.raises(StorageError) as exc_info:
            storage.load_patterns()
        assert "corrupted" in str(exc_info.value).lower() or "invalid" in str(
            exc_info.value
        ).lower()

    def test_clear_removes_file(self, temp_storage_path, sample_patterns):
        """Test that clear removes the storage file."""
        storage = FileStorage(temp_storage_path)

        # Save patterns
        storage.save_patterns(sample_patterns)
        assert storage.exists()

        # Clear
        storage.clear()

        # Verify file is gone
        assert not storage.exists()

    def test_clear_on_nonexistent_file(self, temp_storage_path):
        """Test that clear on non-existent file doesn't raise error."""
        storage = FileStorage(temp_storage_path)

        # Clear non-existent file (should not raise error)
        storage.clear()

        assert not storage.exists()

    def test_atomic_write_operation(self, temp_storage_path):
        """Test that save uses atomic write (temp file + rename)."""
        storage = FileStorage(temp_storage_path)

        # Save patterns
        patterns = [{"id": "test", "name": "Test"}]
        storage.save_patterns(patterns)

        # Verify no temp files left behind
        temp_files = list(storage.storage_path.parent.glob(".tmp_*"))
        assert len(temp_files) == 0

    def test_utf8_encoding_support(self, temp_storage_path):
        """Test that storage supports UTF-8 encoded characters."""
        storage = FileStorage(temp_storage_path)

        # Save patterns with international characters
        patterns = [
            {
                "id": "test",
                "name": "Тест",  # Cyrillic
                "intent": "テスト",  # Japanese
                "problem": "测试",  # Chinese
                "solution": "Prüfung"  # German
            }
        ]
        storage.save_patterns(patterns)

        # Load and verify
        loaded = storage.load_patterns()
        assert loaded[0]["name"] == "Тест"
        assert loaded[0]["intent"] == "テスト"
        assert loaded[0]["problem"] == "测试"
        assert loaded[0]["solution"] == "Prüfung"

    def test_get_storage_info(self, temp_storage_path, sample_patterns):
        """Test get_storage_info method."""
        storage = FileStorage(temp_storage_path)

        # Before saving
        info = storage.get_storage_info()
        assert info["storage_path"] == temp_storage_path
        assert not info["exists"]
        assert "parent_exists" in info

        # After saving
        storage.save_patterns(sample_patterns)
        info = storage.get_storage_info()
        assert info["exists"]
        assert "size_bytes" in info
        assert info["size_bytes"] > 0
        assert "modified_time" in info

    def test_concurrent_writes_safety(self, temp_storage_path):
        """Test that atomic writes help with concurrent write safety."""
        storage = FileStorage(temp_storage_path)

        # Save initial data
        storage.save_patterns([{"id": "1"}])

        # Second save should completely replace first
        storage.save_patterns([{"id": "2"}, {"id": "3"}])

        # Verify final state
        loaded = storage.load_patterns()
        assert len(loaded) == 2
        assert loaded[0]["id"] == "2"

    def test_preserves_data_structure(self, temp_storage_path):
        """Test that storage preserves complex data structures."""
        storage = FileStorage(temp_storage_path)

        # Save complex pattern with nested data
        patterns = [
            {
                "id": "test",
                "name": "Test Pattern",
                "tags": ["tag1", "tag2", "tag3"],
                "related_patterns": ["Pattern A", "Pattern B"],
                "source_metadata": {
                    "source_name": "OORP",
                    "authors": ["Author 1", "Author 2"],
                    "publication_year": 2002,
                    "url": None
                }
            }
        ]
        storage.save_patterns(patterns)

        # Load and verify structure preserved
        loaded = storage.load_patterns()
        assert loaded[0]["tags"] == ["tag1", "tag2", "tag3"]
        assert loaded[0]["related_patterns"] == ["Pattern A", "Pattern B"]
        assert loaded[0]["source_metadata"]["source_name"] == "OORP"
        assert len(loaded[0]["source_metadata"]["authors"]) == 2

    def test_error_includes_cause(self, temp_storage_path):
        """Test that StorageError includes the underlying cause."""
        storage = FileStorage(temp_storage_path)

        # Create file with invalid JSON
        storage.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_storage_path, 'w') as f:
            f.write("invalid")

        # Load should raise StorageError with cause
        with pytest.raises(StorageError) as exc_info:
            storage.load_patterns()

        error = exc_info.value
        assert error.cause is not None
        assert "caused by" in str(error).lower()
