"""
Integration tests for storage persistence workflow.

These tests verify the complete end-to-end workflow:
1. Creating patterns
2. Adding to repository
3. Saving to storage
4. Loading from storage in new repository instance
5. Verifying data integrity

Tests the integration between:
- Pattern model
- Repository
- Storage backend
"""

import pytest
import os
import tempfile
from pathlib import Path

from patternsphere.models.pattern import Pattern, SourceMetadata
from patternsphere.repository.pattern_repository import InMemoryPatternRepository
from patternsphere.storage.file_storage import FileStorage


class TestStoragePersistence:
    """Integration tests for storage persistence workflow."""

    @pytest.fixture
    def temp_storage_path(self):
        """Fixture providing a temporary storage path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield os.path.join(tmpdir, "data", "patterns.json")

    @pytest.fixture
    def source_metadata(self):
        """Fixture providing OORP source metadata."""
        return SourceMetadata(
            source_name="OORP",
            authors=[
                "Serge Demeyer",
                "Stéphane Ducasse",
                "Oscar Nierstrasz"
            ],
            publication_year=2002,
            url="https://example.com/oorp"
        )

    @pytest.fixture
    def sample_patterns(self, source_metadata):
        """Fixture providing sample OORP patterns."""
        return [
            Pattern(
                name="Read all the Code in One Hour",
                intent="Get a first impression of the system by reading all the code in one hour",
                problem="You need to quickly understand what a legacy system does",
                context="You have access to source code but limited time",
                solution="Skim through all source files systematically to get an overview",
                consequences="You get a broad understanding but miss details",
                category="First Contact",
                tags=["assessment", "overview", "time-boxed"],
                related_patterns=["Skim the Documentation", "Interview During Demo"],
                source_metadata=source_metadata
            ),
            Pattern(
                name="Speculate about Design",
                intent="Form hypotheses about the system design to guide further investigation",
                problem="You need direction for detailed analysis of unfamiliar code",
                context="You have done initial assessment but lack deep understanding",
                solution="Make educated guesses about architecture and verify them",
                consequences="Helps focus investigation but may lead to wrong assumptions",
                category="Initial Understanding",
                tags=["analysis", "hypothesis", "architecture"],
                related_patterns=["Read all the Code in One Hour", "Analyze the Persistent Data"],
                source_metadata=source_metadata
            ),
            Pattern(
                name="Write Tests to Understand",
                intent="Develop tests to understand how code works",
                problem="Documentation is missing or outdated for legacy code",
                context="You need to understand specific functionality",
                solution="Write tests that exercise the code and document behavior",
                consequences="Tests provide living documentation and safety net for refactoring",
                category="Tests",
                tags=["testing", "documentation", "understanding"],
                related_patterns=["Write Tests to Enable Evolution", "Grow Your Test Base Incrementally"],
                source_metadata=source_metadata
            ),
        ]

    @pytest.mark.integration
    def test_save_and_load_patterns_roundtrip(
        self, temp_storage_path, sample_patterns
    ):
        """
        Test complete save and load roundtrip.

        Workflow:
        1. Create repository with storage
        2. Add patterns
        3. Save to storage
        4. Create new repository with same storage
        5. Verify patterns loaded correctly
        """
        # Step 1: Create repository with storage
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)

        # Step 2: Add patterns
        for pattern in sample_patterns:
            repo1.add_pattern(pattern)

        assert repo1.count() == 3

        # Step 3: Save to storage
        repo1.save_to_storage()

        # Verify file exists
        assert os.path.exists(temp_storage_path)

        # Step 4: Create new repository with same storage
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        # Step 5: Verify patterns loaded correctly
        assert repo2.count() == 3

        # Verify each pattern
        for original_pattern in sample_patterns:
            loaded = repo2.get_pattern_by_name(original_pattern.name)
            assert loaded is not None
            assert loaded.name == original_pattern.name
            assert loaded.intent == original_pattern.intent
            assert loaded.problem == original_pattern.problem
            assert loaded.solution == original_pattern.solution
            assert loaded.category == original_pattern.category
            assert loaded.tags == original_pattern.tags
            assert loaded.related_patterns == original_pattern.related_patterns

    @pytest.mark.integration
    def test_persistence_preserves_all_pattern_fields(
        self, temp_storage_path, source_metadata
    ):
        """Test that all pattern fields are preserved through save/load cycle."""
        # Create pattern with all fields populated
        pattern = Pattern(
            name="Complex Pattern",
            intent="Test all fields",
            problem="Need to verify all data persists",
            context="When testing persistence",
            solution="Save and load pattern with all fields",
            consequences="Confidence in data integrity",
            category="Testing",
            tags=["persistence", "integration", "testing"],
            related_patterns=["Pattern A", "Pattern B", "Pattern C"],
            source_metadata=source_metadata
        )

        # Save
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        repo1.add_pattern(pattern)
        repo1.save_to_storage()

        # Load
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        # Verify all fields
        loaded = repo2.get_pattern_by_id(pattern.id)
        assert loaded is not None
        assert loaded.id == pattern.id
        assert loaded.name == pattern.name
        assert loaded.intent == pattern.intent
        assert loaded.problem == pattern.problem
        assert loaded.context == pattern.context
        assert loaded.solution == pattern.solution
        assert loaded.consequences == pattern.consequences
        assert loaded.category == pattern.category
        assert loaded.tags == pattern.tags
        assert loaded.related_patterns == pattern.related_patterns
        assert loaded.source_metadata.source_name == pattern.source_metadata.source_name
        assert loaded.source_metadata.authors == pattern.source_metadata.authors
        assert loaded.source_metadata.publication_year == pattern.source_metadata.publication_year

    @pytest.mark.integration
    def test_multiple_save_cycles(self, temp_storage_path, sample_patterns):
        """Test multiple save/load cycles maintain data integrity."""
        storage = FileStorage(temp_storage_path)

        # First cycle: Add 2 patterns
        repo1 = InMemoryPatternRepository(storage=storage)
        repo1.add_pattern(sample_patterns[0])
        repo1.add_pattern(sample_patterns[1])
        repo1.save_to_storage()

        # Second cycle: Load and add 1 more pattern
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)
        assert repo2.count() == 2
        repo2.add_pattern(sample_patterns[2])
        repo2.save_to_storage()

        # Third cycle: Verify all 3 patterns
        storage3 = FileStorage(temp_storage_path)
        repo3 = InMemoryPatternRepository(storage=storage3)
        assert repo3.count() == 3

        # Verify each pattern exists
        for pattern in sample_patterns:
            loaded = repo3.get_pattern_by_name(pattern.name)
            assert loaded is not None

    @pytest.mark.integration
    def test_category_index_persists(self, temp_storage_path, sample_patterns):
        """Test that category indexing works after loading from storage."""
        # Save patterns
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        for pattern in sample_patterns:
            repo1.add_pattern(pattern)
        repo1.save_to_storage()

        # Load and test category filtering
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        # Test category queries
        first_contact = repo2.get_patterns_by_category("First Contact")
        assert len(first_contact) == 1
        assert first_contact[0].name == "Read all the Code in One Hour"

        tests = repo2.get_patterns_by_category("Tests")
        assert len(tests) == 1
        assert tests[0].name == "Write Tests to Understand"

        # Test category counts
        categories = repo2.get_all_categories()
        assert categories["First Contact"] == 1
        assert categories["Initial Understanding"] == 1
        assert categories["Tests"] == 1

    @pytest.mark.integration
    def test_search_functionality_after_load(
        self, temp_storage_path, sample_patterns
    ):
        """Test that search works correctly on loaded patterns."""
        # Save patterns
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        for pattern in sample_patterns:
            repo1.add_pattern(pattern)
        repo1.save_to_storage()

        # Load and test search
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        # Search by query
        results = repo2.search_patterns(query="test")
        assert len(results) == 1
        assert "Tests" in results[0].name

        # Search by category
        results = repo2.search_patterns(category="First Contact")
        assert len(results) == 1

        # Search by tags
        results = repo2.search_patterns(tags=["testing"])
        assert len(results) == 1

        # Combined search
        results = repo2.search_patterns(
            query="understand",
            tags=["testing"]
        )
        assert len(results) >= 1

    @pytest.mark.integration
    def test_empty_repository_persistence(self, temp_storage_path):
        """Test that empty repository can be saved and loaded."""
        # Save empty repository
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        repo1.save_to_storage()

        # Load and verify
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)
        assert repo2.count() == 0
        assert repo2.list_all_patterns() == []

    @pytest.mark.integration
    def test_unicode_patterns_persist(self, temp_storage_path):
        """Test that patterns with Unicode characters persist correctly."""
        # Create pattern with Unicode content
        metadata = SourceMetadata(
            source_name="国际化测试",  # Chinese
            authors=["Müller", "Søren"],  # German, Danish
            publication_year=2020
        )

        pattern = Pattern(
            name="Интернационализация",  # Russian
            intent="パターンのテスト",  # Japanese
            problem="Проверка Unicode",  # Russian
            solution="UTF-8 кодирование",  # Russian
            category="Тестирование",  # Russian
            tags=["国际化", "тест"],  # Chinese, Russian
            source_metadata=metadata
        )

        # Save
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        repo1.add_pattern(pattern)
        repo1.save_to_storage()

        # Load and verify
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)
        loaded = repo2.get_pattern_by_name("Интернационализация")

        assert loaded is not None
        assert loaded.intent == "パターンのテスト"
        assert loaded.problem == "Проверка Unicode"
        assert loaded.source_metadata.source_name == "国际化测试"

    @pytest.mark.integration
    def test_storage_survives_application_restart(
        self, temp_storage_path, sample_patterns
    ):
        """
        Test that data survives simulated application restart.

        This simulates the real-world scenario where the application
        is stopped and restarted, relying on persistent storage.
        """
        # Simulate first application session
        storage1 = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage1)
        for pattern in sample_patterns:
            repo1.add_pattern(pattern)
        repo1.save_to_storage()
        del repo1  # Simulate application shutdown
        del storage1

        # Simulate application restart
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        # Verify all data survived
        assert repo2.count() == len(sample_patterns)
        for pattern in sample_patterns:
            loaded = repo2.get_pattern_by_name(pattern.name)
            assert loaded is not None
            assert loaded.intent == pattern.intent

    @pytest.mark.integration
    def test_repository_stats_after_load(
        self, temp_storage_path, sample_patterns
    ):
        """Test that repository statistics are correct after loading."""
        # Save patterns
        storage = FileStorage(temp_storage_path)
        repo1 = InMemoryPatternRepository(storage=storage)
        for pattern in sample_patterns:
            repo1.add_pattern(pattern)
        repo1.save_to_storage()

        # Load and check stats
        storage2 = FileStorage(temp_storage_path)
        repo2 = InMemoryPatternRepository(storage=storage2)

        stats = repo2.get_repository_stats()
        assert stats["total_patterns"] == 3
        assert stats["total_categories"] == 3
        assert stats["has_storage"] is True
        assert len(stats["categories"]) == 3
