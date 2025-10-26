"""
Unit tests for OORP pattern loader.

This test suite verifies the OORPLoader functionality including:
- Loading patterns from JSON files
- Statistics tracking
- Error handling and recovery
- Performance requirements
"""

import json
import pytest
import tempfile
from pathlib import Path

from patternsphere.loaders.oorp_loader import OORPLoader, LoaderStats
from patternsphere.repository.pattern_repository import InMemoryPatternRepository
from patternsphere.models.pattern import Pattern, SourceMetadata


class TestLoaderStats:
    """Test LoaderStats dataclass."""

    def test_loader_stats_creation(self):
        """Test creating LoaderStats."""
        stats = LoaderStats(
            total_patterns=10,
            loaded_successfully=8,
            failed_patterns=2,
            duration_ms=100.5,
            errors=["Error 1", "Error 2"]
        )

        assert stats.total_patterns == 10
        assert stats.loaded_successfully == 8
        assert stats.failed_patterns == 2
        assert stats.duration_ms == 100.5
        assert len(stats.errors) == 2

    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        stats = LoaderStats(
            total_patterns=10,
            loaded_successfully=8,
            failed_patterns=2,
            duration_ms=100.0,
            errors=[]
        )

        assert stats.success_rate == 80.0

    def test_success_rate_zero_patterns(self):
        """Test success rate with zero patterns."""
        stats = LoaderStats(
            total_patterns=0,
            loaded_successfully=0,
            failed_patterns=0,
            duration_ms=0.0,
            errors=[]
        )

        assert stats.success_rate == 0.0

    def test_success_rate_all_failed(self):
        """Test success rate when all patterns fail."""
        stats = LoaderStats(
            total_patterns=5,
            loaded_successfully=0,
            failed_patterns=5,
            duration_ms=50.0,
            errors=["Error"] * 5
        )

        assert stats.success_rate == 0.0

    def test_success_rate_all_success(self):
        """Test success rate when all patterns succeed."""
        stats = LoaderStats(
            total_patterns=5,
            loaded_successfully=5,
            failed_patterns=0,
            duration_ms=50.0,
            errors=[]
        )

        assert stats.success_rate == 100.0

    def test_loader_stats_string_representation(self):
        """Test string representation of LoaderStats."""
        stats = LoaderStats(
            total_patterns=10,
            loaded_successfully=8,
            failed_patterns=2,
            duration_ms=123.45,
            errors=[]
        )

        stats_str = str(stats)
        assert "total=10" in stats_str
        assert "loaded=8" in stats_str
        assert "failed=2" in stats_str
        assert "duration=123.45ms" in stats_str
        assert "success_rate=80.0%" in stats_str


class TestOORPLoader:
    """Test OORPLoader functionality."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryPatternRepository()

    @pytest.fixture
    def loader(self, repository):
        """Create a loader for each test."""
        return OORPLoader(repository)

    @pytest.fixture
    def sample_pattern_data(self):
        """Create sample pattern data."""
        return {
            "name": "Test Pattern",
            "intent": "Test pattern for unit testing",
            "problem": "Need to test pattern loading",
            "context": "Testing context",
            "solution": "Use a test pattern",
            "consequences": "Tests pass",
            "related_patterns": ["Other Pattern"],
            "category": "Testing",
            "tags": ["test", "sample"],
            "source_metadata": {
                "source_name": "OORP",
                "authors": ["Test Author"],
                "publication_year": 2003,
                "url": "http://example.com"
            }
        }

    def test_loader_initialization(self, loader, repository):
        """Test loader initialization."""
        assert loader.repository is repository

    def test_load_from_dict_single_pattern(self, loader, repository, sample_pattern_data):
        """Test loading a single pattern from dict."""
        stats = loader.load_from_dict([sample_pattern_data])

        assert stats.total_patterns == 1
        assert stats.loaded_successfully == 1
        assert stats.failed_patterns == 0
        assert len(stats.errors) == 0
        assert stats.success_rate == 100.0

        # Verify pattern was added to repository
        assert repository.count() == 1
        pattern = repository.get_pattern_by_name("Test Pattern")
        assert pattern is not None
        assert pattern.intent == "Test pattern for unit testing"

    def test_load_from_dict_multiple_patterns(self, loader, repository):
        """Test loading multiple patterns from dict."""
        patterns_data = []
        for i in range(5):
            patterns_data.append({
                "name": f"Pattern {i}",
                "intent": f"Intent {i}",
                "problem": f"Problem {i}",
                "solution": f"Solution {i}",
                "category": "Test",
                "tags": ["test"],
                "source_metadata": {
                    "source_name": "OORP",
                    "authors": [],
                    "publication_year": 2003
                }
            })

        stats = loader.load_from_dict(patterns_data)

        assert stats.total_patterns == 5
        assert stats.loaded_successfully == 5
        assert stats.failed_patterns == 0
        assert repository.count() == 5

    def test_load_from_dict_with_invalid_pattern(self, loader, repository):
        """Test loading continues when a pattern is invalid."""
        patterns_data = [
            {
                "name": "Valid Pattern",
                "intent": "Valid",
                "problem": "Valid",
                "solution": "Valid",
                "category": "Test",
                "source_metadata": {"source_name": "OORP"}
            },
            {
                # Missing required fields
                "name": "Invalid Pattern"
            },
            {
                "name": "Another Valid Pattern",
                "intent": "Valid",
                "problem": "Valid",
                "solution": "Valid",
                "category": "Test",
                "source_metadata": {"source_name": "OORP"}
            }
        ]

        stats = loader.load_from_dict(patterns_data)

        assert stats.total_patterns == 3
        assert stats.loaded_successfully == 2
        assert stats.failed_patterns == 1
        assert len(stats.errors) == 1
        assert repository.count() == 2

    def test_load_from_dict_with_duplicate_names(self, loader, repository, sample_pattern_data):
        """Test loading fails when patterns have duplicate names."""
        # Load same pattern twice
        patterns_data = [sample_pattern_data, sample_pattern_data.copy()]

        stats = loader.load_from_dict(patterns_data)

        # First should succeed, second should fail due to duplicate name
        assert stats.total_patterns == 2
        assert stats.loaded_successfully == 1
        assert stats.failed_patterns == 1
        assert len(stats.errors) == 1
        assert "already exists" in stats.errors[0].lower()

    def test_load_from_dict_invalid_input_type(self, loader):
        """Test loading raises error for invalid input type."""
        with pytest.raises(ValueError, match="Expected list"):
            loader.load_from_dict("not a list")

    def test_load_from_dict_performance(self, loader, repository):
        """Test loading performance for 20 patterns."""
        # Create 20 patterns
        patterns_data = []
        for i in range(20):
            patterns_data.append({
                "name": f"Pattern {i}",
                "intent": f"Intent {i}",
                "problem": f"Problem {i}",
                "solution": f"Solution {i}",
                "category": "Test",
                "tags": ["test", "performance"],
                "source_metadata": {
                    "source_name": "OORP",
                    "authors": ["Author"],
                    "publication_year": 2003
                }
            })

        stats = loader.load_from_dict(patterns_data)

        assert stats.loaded_successfully == 20
        # Should be much faster than 500ms for 20 patterns
        assert stats.duration_ms < 500

    def test_load_from_file_success(self, loader, repository, sample_pattern_data):
        """Test loading patterns from a JSON file."""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump([sample_pattern_data], f)
            temp_file = f.name

        try:
            stats = loader.load_from_file(temp_file)

            assert stats.total_patterns == 1
            assert stats.loaded_successfully == 1
            assert stats.failed_patterns == 0
            assert repository.count() == 1

        finally:
            # Clean up temp file
            Path(temp_file).unlink()

    def test_load_from_file_not_found(self, loader):
        """Test loading from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            loader.load_from_file("nonexistent_file.json")

    def test_load_from_file_invalid_json(self, loader):
        """Test loading from file with invalid JSON raises error."""
        # Create temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write("not valid json {")
            temp_file = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                loader.load_from_file(temp_file)

        finally:
            Path(temp_file).unlink()

    def test_load_from_file_not_array(self, loader):
        """Test loading from file that doesn't contain array raises error."""
        # Create temporary file with JSON object instead of array
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump({"not": "an array"}, f)
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="Expected JSON array"):
                loader.load_from_file(temp_file)

        finally:
            Path(temp_file).unlink()

    def test_load_from_file_multiple_patterns(self, loader, repository):
        """Test loading multiple patterns from file."""
        patterns_data = [
            {
                "name": "Pattern 1",
                "intent": "Intent 1",
                "problem": "Problem 1",
                "solution": "Solution 1",
                "category": "Test",
                "source_metadata": {"source_name": "OORP"}
            },
            {
                "name": "Pattern 2",
                "intent": "Intent 2",
                "problem": "Problem 2",
                "solution": "Solution 2",
                "category": "Test",
                "source_metadata": {"source_name": "OORP"}
            },
            {
                "name": "Pattern 3",
                "intent": "Intent 3",
                "problem": "Problem 3",
                "solution": "Solution 3",
                "category": "Test",
                "source_metadata": {"source_name": "OORP"}
            }
        ]

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump(patterns_data, f)
            temp_file = f.name

        try:
            stats = loader.load_from_file(temp_file)

            assert stats.total_patterns == 3
            assert stats.loaded_successfully == 3
            assert stats.failed_patterns == 0
            assert repository.count() == 3

        finally:
            Path(temp_file).unlink()

    def test_loader_repr(self, loader, repository):
        """Test string representation of loader."""
        loader_repr = repr(loader)
        assert "OORPLoader" in loader_repr
        assert "repository" in loader_repr.lower()
