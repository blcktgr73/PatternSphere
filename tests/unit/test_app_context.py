"""
Unit tests for AppContext.

Tests the application context singleton and dependency injection.
"""

import pytest
from pathlib import Path
from patternsphere.cli.app_context import AppContext
from patternsphere.repository import InMemoryPatternRepository
from patternsphere.search import KeywordSearchEngine


@pytest.fixture(autouse=True)
def reset_context():
    """Reset AppContext singleton before and after each test."""
    AppContext.reset_instance()
    yield
    AppContext.reset_instance()


class TestAppContext:
    """Tests for AppContext singleton."""

    def test_get_instance_returns_singleton(self):
        """Test that get_instance returns the same instance."""
        ctx1 = AppContext.get_instance()
        ctx2 = AppContext.get_instance()
        assert ctx1 is ctx2

    def test_reset_instance(self):
        """Test resetting the singleton instance."""
        ctx1 = AppContext.get_instance()
        AppContext.reset_instance()
        ctx2 = AppContext.get_instance()
        assert ctx1 is not ctx2

    def test_initial_state(self):
        """Test initial state of context."""
        ctx = AppContext.get_instance()
        assert not ctx.is_initialized
        assert ctx.load_stats is None

    def test_initialize_creates_components(self):
        """Test that initialize creates components."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=False)

        assert ctx.is_initialized
        assert isinstance(ctx.repository, InMemoryPatternRepository)
        assert isinstance(ctx.search_engine, KeywordSearchEngine)

    def test_initialize_auto_loads_patterns(self):
        """Test that initialize auto-loads patterns when enabled."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        assert ctx.is_initialized
        assert ctx.load_stats is not None
        assert ctx.load_stats.loaded_successfully > 0
        assert ctx.get_pattern_count() > 0

    def test_initialize_idempotent(self):
        """Test that multiple initialize calls are safe."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=False)
        count1 = ctx.get_pattern_count()

        # Second initialize should be no-op
        ctx.initialize(auto_load=False)
        count2 = ctx.get_pattern_count()

        assert count1 == count2

    def test_repository_property_before_init_raises(self):
        """Test accessing repository before init raises error."""
        ctx = AppContext.get_instance()
        with pytest.raises(RuntimeError, match="not initialized"):
            _ = ctx.repository

    def test_search_engine_property_before_init_raises(self):
        """Test accessing search_engine before init raises error."""
        ctx = AppContext.get_instance()
        with pytest.raises(RuntimeError, match="not initialized"):
            _ = ctx.search_engine

    def test_load_patterns_before_init_raises(self):
        """Test loading patterns before init raises error."""
        ctx = AppContext.get_instance()
        with pytest.raises(RuntimeError, match="not initialized"):
            ctx.load_patterns()

    def test_load_patterns_with_default_path(self):
        """Test loading patterns with default path."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=False)

        stats = ctx.load_patterns()
        assert stats.loaded_successfully > 0
        assert stats.success_rate == 100.0

    def test_load_patterns_with_custom_path(self, tmp_path):
        """Test loading patterns with custom path."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=False)

        # Create a simple test file
        test_file = tmp_path / "test_patterns.json"
        test_file.write_text("""
        [
            {
                "id": "TEST-001",
                "name": "Test Pattern",
                "category": "Test",
                "intent": "Test intent",
                "problem": "Test problem",
                "solution": "Test solution",
                "tags": ["test"],
                "source_metadata": {
                    "source_name": "Test"
                }
            }
        ]
        """)

        stats = ctx.load_patterns(test_file)
        assert stats.loaded_successfully == 1

    def test_get_pattern_count(self):
        """Test getting pattern count."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        count = ctx.get_pattern_count()
        assert count > 0
        assert count == len(ctx.repository.list_all_patterns())

    def test_get_pattern_count_before_init(self):
        """Test getting pattern count before initialization."""
        ctx = AppContext.get_instance()
        assert ctx.get_pattern_count() == 0

    def test_get_categories(self):
        """Test getting categories."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        categories = ctx.get_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert all(isinstance(c, str) for c in categories)
        # Should be sorted
        assert categories == sorted(categories)

    def test_get_categories_before_init(self):
        """Test getting categories before initialization."""
        ctx = AppContext.get_instance()
        categories = ctx.get_categories()
        assert categories == []

    def test_get_pattern_count_by_category(self):
        """Test getting pattern counts by category."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        counts = ctx.get_pattern_count_by_category()
        assert isinstance(counts, dict)
        assert len(counts) > 0
        assert all(isinstance(k, str) for k in counts.keys())
        assert all(isinstance(v, int) for v in counts.values())
        assert all(v > 0 for v in counts.values())

    def test_get_pattern_count_by_category_before_init(self):
        """Test getting category counts before initialization."""
        ctx = AppContext.get_instance()
        counts = ctx.get_pattern_count_by_category()
        assert counts == {}

    def test_load_stats_property(self):
        """Test load_stats property."""
        ctx = AppContext.get_instance()
        assert ctx.load_stats is None

        ctx.initialize(auto_load=True)
        assert ctx.load_stats is not None
        assert ctx.load_stats.loaded_successfully > 0

    def test_is_initialized_property(self):
        """Test is_initialized property."""
        ctx = AppContext.get_instance()
        assert not ctx.is_initialized

        ctx.initialize(auto_load=False)
        assert ctx.is_initialized

    def test_repository_and_search_engine_share_repository(self):
        """Test that search engine uses the same repository instance."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        # Both should reference the same repository
        assert ctx.search_engine.repository is ctx.repository

    def test_context_survives_multiple_operations(self):
        """Test context remains valid across multiple operations."""
        ctx = AppContext.get_instance()
        ctx.initialize(auto_load=True)

        # Perform multiple operations
        count1 = ctx.get_pattern_count()
        categories = ctx.get_categories()
        count2 = ctx.get_pattern_count()

        # Should remain consistent
        assert count1 == count2
        assert len(categories) > 0
        assert ctx.is_initialized
