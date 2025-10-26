"""
Unit tests for repository implementations.

Tests cover:
- Pattern CRUD operations
- Indexing and lookup performance
- Search functionality
- Category filtering
- Error handling
- Storage integration
"""

import pytest
from unittest.mock import Mock, MagicMock

from patternsphere.models.pattern import Pattern, SourceMetadata
from patternsphere.repository.pattern_repository import InMemoryPatternRepository
from patternsphere.repository.repository_interface import RepositoryError
from patternsphere.storage.storage_interface import IStorage, StorageError


class TestInMemoryPatternRepository:
    """Test cases for InMemoryPatternRepository."""

    @pytest.fixture
    def source_metadata(self):
        """Fixture providing source metadata."""
        return SourceMetadata(
            source_name="OORP",
            authors=["Test Author"],
            publication_year=2002
        )

    @pytest.fixture
    def sample_pattern(self, source_metadata):
        """Fixture providing a sample pattern."""
        return Pattern(
            name="Test Pattern",
            intent="To test the repository",
            problem="Need to validate repository",
            solution="Create comprehensive tests",
            category="Testing",
            tags=["test", "validation"],
            source_metadata=source_metadata
        )

    @pytest.fixture
    def repository(self):
        """Fixture providing a repository without storage."""
        return InMemoryPatternRepository()

    def test_create_repository_without_storage(self):
        """Test creating repository without storage backend."""
        repo = InMemoryPatternRepository()
        assert repo.count() == 0
        assert repo.storage is None

    def test_create_repository_with_storage(self):
        """Test creating repository with storage backend."""
        mock_storage = Mock(spec=IStorage)
        mock_storage.load_patterns.return_value = []

        repo = InMemoryPatternRepository(storage=mock_storage)
        assert repo.storage is not None
        mock_storage.load_patterns.assert_called_once()

    def test_add_pattern(self, repository, sample_pattern):
        """Test adding a pattern to repository."""
        repository.add_pattern(sample_pattern)

        assert repository.count() == 1
        assert repository.get_pattern_by_id(sample_pattern.id) == sample_pattern

    def test_add_pattern_with_duplicate_id_raises_error(
        self, repository, sample_pattern
    ):
        """Test that adding pattern with duplicate ID raises error."""
        repository.add_pattern(sample_pattern)

        # Create another pattern with same ID
        duplicate = Pattern(
            id=sample_pattern.id,
            name="Different Name",
            intent="Different",
            problem="Different",
            solution="Different",
            category="Different",
            source_metadata=sample_pattern.source_metadata
        )

        with pytest.raises(RepositoryError) as exc_info:
            repository.add_pattern(duplicate)
        assert "already exists" in str(exc_info.value).lower()

    def test_add_pattern_with_duplicate_name_raises_error(
        self, repository, sample_pattern, source_metadata
    ):
        """Test that adding pattern with duplicate name raises error."""
        repository.add_pattern(sample_pattern)

        # Create another pattern with same name but different ID
        duplicate = Pattern(
            name=sample_pattern.name,
            intent="Different",
            problem="Different",
            solution="Different",
            category="Different",
            source_metadata=source_metadata
        )

        with pytest.raises(RepositoryError) as exc_info:
            repository.add_pattern(duplicate)
        assert "name" in str(exc_info.value).lower()
        assert "already exists" in str(exc_info.value).lower()

    def test_get_pattern_by_id(self, repository, sample_pattern):
        """Test retrieving pattern by ID."""
        repository.add_pattern(sample_pattern)

        retrieved = repository.get_pattern_by_id(sample_pattern.id)
        assert retrieved == sample_pattern
        assert retrieved.name == "Test Pattern"

    def test_get_pattern_by_id_returns_none_for_nonexistent(self, repository):
        """Test that getting non-existent pattern returns None."""
        result = repository.get_pattern_by_id("nonexistent-id")
        assert result is None

    def test_get_pattern_by_name(self, repository, sample_pattern):
        """Test retrieving pattern by name."""
        repository.add_pattern(sample_pattern)

        retrieved = repository.get_pattern_by_name("Test Pattern")
        assert retrieved == sample_pattern
        assert retrieved.id == sample_pattern.id

    def test_get_pattern_by_name_returns_none_for_nonexistent(self, repository):
        """Test that getting non-existent pattern by name returns None."""
        result = repository.get_pattern_by_name("Nonexistent Pattern")
        assert result is None

    def test_list_all_patterns(self, repository, source_metadata):
        """Test listing all patterns."""
        # Add multiple patterns
        patterns = []
        for i in range(3):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent=f"Intent {i}",
                problem=f"Problem {i}",
                solution=f"Solution {i}",
                category="Testing",
                source_metadata=source_metadata
            )
            patterns.append(pattern)
            repository.add_pattern(pattern)

        # List all patterns
        all_patterns = repository.list_all_patterns()
        assert len(all_patterns) == 3
        # Should be sorted by name
        assert all_patterns[0].name == "Pattern 0"
        assert all_patterns[1].name == "Pattern 1"
        assert all_patterns[2].name == "Pattern 2"

    def test_list_all_patterns_returns_empty_list_when_empty(self, repository):
        """Test that listing patterns on empty repository returns empty list."""
        patterns = repository.list_all_patterns()
        assert patterns == []

    def test_get_patterns_by_category(self, repository, source_metadata):
        """Test filtering patterns by category."""
        # Add patterns in different categories
        categories = ["Category A", "Category B", "Category A"]
        for i, category in enumerate(categories):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent=f"Intent {i}",
                problem=f"Problem {i}",
                solution=f"Solution {i}",
                category=category,
                source_metadata=source_metadata
            )
            repository.add_pattern(pattern)

        # Get patterns by category
        category_a_patterns = repository.get_patterns_by_category("Category A")
        assert len(category_a_patterns) == 2
        assert all(p.category == "Category A" for p in category_a_patterns)

        category_b_patterns = repository.get_patterns_by_category("Category B")
        assert len(category_b_patterns) == 1
        assert category_b_patterns[0].category == "Category B"

    def test_get_patterns_by_nonexistent_category(self, repository):
        """Test getting patterns by non-existent category returns empty list."""
        patterns = repository.get_patterns_by_category("Nonexistent")
        assert patterns == []

    def test_get_all_categories(self, repository, source_metadata):
        """Test getting all categories with counts."""
        # Add patterns in different categories
        categories = ["Category A", "Category B", "Category A", "Category C"]
        for i, category in enumerate(categories):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent=f"Intent {i}",
                problem=f"Problem {i}",
                solution=f"Solution {i}",
                category=category,
                source_metadata=source_metadata
            )
            repository.add_pattern(pattern)

        # Get all categories
        all_categories = repository.get_all_categories()
        assert len(all_categories) == 3
        assert all_categories["Category A"] == 2
        assert all_categories["Category B"] == 1
        assert all_categories["Category C"] == 1

    def test_search_patterns_by_query(self, repository, source_metadata):
        """Test searching patterns by query string."""
        # Add patterns
        pattern1 = Pattern(
            name="Refactoring Pattern",
            intent="To refactor code",
            problem="Bad code",
            solution="Refactor it",
            category="Refactoring",
            source_metadata=source_metadata
        )
        pattern2 = Pattern(
            name="Testing Pattern",
            intent="To test code",
            problem="Untested code",
            solution="Write tests",
            category="Testing",
            source_metadata=source_metadata
        )
        repository.add_pattern(pattern1)
        repository.add_pattern(pattern2)

        # Search for "refactor"
        results = repository.search_patterns(query="refactor")
        assert len(results) == 1
        assert results[0].name == "Refactoring Pattern"

        # Search for "code"
        results = repository.search_patterns(query="code")
        assert len(results) == 2  # Both match

    def test_search_patterns_by_category(self, repository, source_metadata):
        """Test searching patterns with category filter."""
        # Add patterns
        for i in range(3):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent="Test",
                problem="Test",
                solution="Test",
                category="Category A" if i < 2 else "Category B",
                source_metadata=source_metadata
            )
            repository.add_pattern(pattern)

        # Search with category filter
        results = repository.search_patterns(category="Category A")
        assert len(results) == 2
        assert all(p.category == "Category A" for p in results)

    def test_search_patterns_by_tags(self, repository, source_metadata):
        """Test searching patterns by tags."""
        # Add patterns with different tags
        pattern1 = Pattern(
            name="Pattern 1",
            intent="Test",
            problem="Test",
            solution="Test",
            category="Test",
            tags=["refactoring", "testing"],
            source_metadata=source_metadata
        )
        pattern2 = Pattern(
            name="Pattern 2",
            intent="Test",
            problem="Test",
            solution="Test",
            category="Test",
            tags=["design", "architecture"],
            source_metadata=source_metadata
        )
        repository.add_pattern(pattern1)
        repository.add_pattern(pattern2)

        # Search by tags (OR logic)
        results = repository.search_patterns(tags=["refactoring"])
        assert len(results) == 1
        assert results[0].name == "Pattern 1"

        # Search with multiple tags
        results = repository.search_patterns(tags=["refactoring", "design"])
        assert len(results) == 2  # OR logic

    def test_search_patterns_with_combined_filters(
        self, repository, source_metadata
    ):
        """Test searching with query, category, and tags combined."""
        pattern = Pattern(
            name="Refactoring Pattern",
            intent="To refactor code",
            problem="Bad code",
            solution="Refactor it",
            category="Refactoring",
            tags=["refactoring", "code-quality"],
            source_metadata=source_metadata
        )
        repository.add_pattern(pattern)

        # Search with all filters
        results = repository.search_patterns(
            query="refactor",
            category="Refactoring",
            tags=["code-quality"]
        )
        assert len(results) == 1
        assert results[0].name == "Refactoring Pattern"

    def test_search_patterns_returns_empty_list_for_no_matches(self, repository):
        """Test that search with no matches returns empty list."""
        results = repository.search_patterns(query="nonexistent")
        assert results == []

    def test_count(self, repository, source_metadata):
        """Test counting patterns."""
        assert repository.count() == 0

        # Add patterns
        for i in range(5):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent="Test",
                problem="Test",
                solution="Test",
                category="Test",
                source_metadata=source_metadata
            )
            repository.add_pattern(pattern)

        assert repository.count() == 5

    def test_clear(self, repository, sample_pattern):
        """Test clearing repository."""
        repository.add_pattern(sample_pattern)
        assert repository.count() == 1

        repository.clear()

        assert repository.count() == 0
        assert repository.get_pattern_by_id(sample_pattern.id) is None
        assert repository.get_all_categories() == {}

    def test_save_to_storage(self, sample_pattern):
        """Test saving patterns to storage."""
        mock_storage = Mock(spec=IStorage)
        mock_storage.load_patterns.return_value = []
        mock_storage.save_patterns = Mock()

        repo = InMemoryPatternRepository(storage=mock_storage)
        repo.add_pattern(sample_pattern)

        # Save to storage
        repo.save_to_storage()

        # Verify storage was called
        mock_storage.save_patterns.assert_called_once()
        saved_data = mock_storage.save_patterns.call_args[0][0]
        assert len(saved_data) == 1
        assert saved_data[0]["name"] == "Test Pattern"

    def test_save_to_storage_without_storage_raises_error(
        self, repository, sample_pattern
    ):
        """Test that saving without storage configured raises error."""
        repository.add_pattern(sample_pattern)

        with pytest.raises(RepositoryError) as exc_info:
            repository.save_to_storage()
        assert "no storage" in str(exc_info.value).lower()

    def test_save_to_storage_handles_storage_errors(self, sample_pattern):
        """Test that storage errors are wrapped in RepositoryError."""
        mock_storage = Mock(spec=IStorage)
        mock_storage.load_patterns.return_value = []
        mock_storage.save_patterns.side_effect = StorageError("Save failed")

        repo = InMemoryPatternRepository(storage=mock_storage)
        repo.add_pattern(sample_pattern)

        with pytest.raises(RepositoryError) as exc_info:
            repo.save_to_storage()
        assert "save failed" in str(exc_info.value).lower()

    def test_load_from_storage_on_initialization(self, source_metadata):
        """Test that patterns are loaded from storage on initialization."""
        # Prepare mock storage with pattern data
        pattern_data = {
            "id": "test-id",
            "name": "Loaded Pattern",
            "intent": "Test",
            "problem": "Test",
            "solution": "Test",
            "category": "Test",
            "tags": [],
            "related_patterns": [],
            "context": "",
            "consequences": "",
            "source_metadata": {
                "source_name": "OORP",
                "authors": [],
                "publication_year": 2002,
                "url": None
            },
            "created_at": "2024-01-01T00:00:00"
        }

        mock_storage = Mock(spec=IStorage)
        mock_storage.load_patterns.return_value = [pattern_data]

        # Create repository (should load from storage)
        repo = InMemoryPatternRepository(storage=mock_storage)

        assert repo.count() == 1
        loaded = repo.get_pattern_by_name("Loaded Pattern")
        assert loaded is not None
        assert loaded.id == "test-id"

    def test_load_from_storage_handles_invalid_patterns(self):
        """Test that invalid patterns are skipped during load."""
        invalid_pattern = {"name": "Invalid"}  # Missing required fields

        mock_storage = Mock(spec=IStorage)
        mock_storage.load_patterns.return_value = [invalid_pattern]

        # Should not raise error, just skip invalid pattern
        repo = InMemoryPatternRepository(storage=mock_storage)
        assert repo.count() == 0

    def test_get_repository_stats(self, repository, source_metadata):
        """Test getting repository statistics."""
        # Add some patterns
        for i in range(3):
            pattern = Pattern(
                name=f"Pattern {i}",
                intent="Test",
                problem="Test",
                solution="Test",
                category=f"Category {i % 2}",
                source_metadata=source_metadata
            )
            repository.add_pattern(pattern)

        stats = repository.get_repository_stats()
        assert stats["total_patterns"] == 3
        assert stats["total_categories"] == 2
        assert stats["has_storage"] is False
        assert "categories" in stats

    def test_repr(self, repository):
        """Test string representation of repository."""
        repr_str = repr(repository)
        assert "InMemoryPatternRepository" in repr_str
        assert "patterns=0" in repr_str
        assert "has_storage=False" in repr_str
