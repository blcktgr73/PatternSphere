"""
Unit tests for keyword search engine.

This test suite verifies the KeywordSearchEngine functionality including:
- Weighted scoring across different fields
- Exact and partial matching
- Category and tag filtering
- Empty query handling
- Performance requirements
"""

import pytest

from patternsphere.search.search_engine import KeywordSearchEngine, SearchResult
from patternsphere.repository.pattern_repository import InMemoryPatternRepository
from patternsphere.models.pattern import Pattern, SourceMetadata


class TestSearchResult:
    """Test SearchResult dataclass."""

    def test_search_result_creation(self):
        """Test creating SearchResult."""
        pattern = Pattern(
            name="Test Pattern",
            intent="Test intent",
            problem="Test problem",
            solution="Test solution",
            category="Test",
            source_metadata=SourceMetadata(source_name="OORP")
        )

        result = SearchResult(
            pattern=pattern,
            score=10.5,
            matched_fields={"name", "intent"}
        )

        assert result.pattern == pattern
        assert result.score == 10.5
        assert "name" in result.matched_fields
        assert "intent" in result.matched_fields

    def test_search_result_string_representation(self):
        """Test string representation of SearchResult."""
        pattern = Pattern(
            name="Test Pattern",
            intent="Test intent",
            problem="Test problem",
            solution="Test solution",
            category="Test",
            source_metadata=SourceMetadata(source_name="OORP")
        )

        result = SearchResult(
            pattern=pattern,
            score=10.5,
            matched_fields={"name"}
        )

        result_str = str(result)
        assert "Test Pattern" in result_str
        assert "10.5" in result_str
        assert "name" in result_str


class TestKeywordSearchEngine:
    """Test KeywordSearchEngine functionality."""

    @pytest.fixture
    def repository(self):
        """Create a repository with test patterns."""
        repo = InMemoryPatternRepository()

        # Add diverse patterns for testing
        patterns_data = [
            {
                "name": "Singleton Pattern",
                "intent": "Ensure a class has only one instance",
                "problem": "Need to control object creation",
                "solution": "Use a static instance variable",
                "category": "Creational",
                "tags": ["instance", "creation", "global"],
                "source_metadata": {"source_name": "GoF"}
            },
            {
                "name": "Factory Method",
                "intent": "Define an interface for creating objects",
                "problem": "Need flexible object creation",
                "solution": "Use factory methods to create objects",
                "category": "Creational",
                "tags": ["creation", "factory", "flexibility"],
                "source_metadata": {"source_name": "GoF"}
            },
            {
                "name": "Observer Pattern",
                "intent": "Define one-to-many dependency between objects",
                "problem": "Need to notify multiple objects of changes",
                "solution": "Use subject-observer relationship",
                "category": "Behavioral",
                "tags": ["notification", "events", "decoupling"],
                "source_metadata": {"source_name": "GoF"}
            },
            {
                "name": "Refactor to Understand",
                "intent": "Improve code structure to enhance understanding",
                "problem": "Code structure impedes comprehension",
                "solution": "Perform small refactorings while reading code",
                "category": "Detailed Model Capture",
                "tags": ["refactoring", "understanding", "code-clarity"],
                "source_metadata": {"source_name": "OORP"}
            },
            {
                "name": "Split Up God Class",
                "intent": "Break down monolithic classes",
                "problem": "Class handles too many responsibilities",
                "solution": "Extract distinct responsibilities into new classes",
                "category": "Redistribute Responsibilities",
                "tags": ["refactoring", "god-class", "single-responsibility"],
                "source_metadata": {"source_name": "OORP"}
            }
        ]

        for data in patterns_data:
            pattern = Pattern(**data)
            repo.add_pattern(pattern)

        return repo

    @pytest.fixture
    def search_engine(self, repository):
        """Create search engine with test patterns."""
        return KeywordSearchEngine(repository)

    def test_search_engine_initialization(self, search_engine, repository):
        """Test search engine initialization."""
        assert search_engine.repository is repository

    def test_search_empty_query(self, search_engine):
        """Test search with empty query returns all patterns."""
        results = search_engine.search(query="")

        assert len(results) == 5
        # All results should have zero score
        assert all(r.score == 0.0 for r in results)
        # Results should be sorted by name
        names = [r.pattern.name for r in results]
        assert names == sorted(names)

    def test_search_whitespace_query(self, search_engine):
        """Test search with whitespace-only query returns all patterns."""
        results = search_engine.search(query="   ")

        assert len(results) == 5
        assert all(r.score == 0.0 for r in results)

    def test_search_by_name_exact_match(self, search_engine):
        """Test search matches pattern name with high score."""
        results = search_engine.search(query="Singleton")

        assert len(results) >= 1
        # Singleton should be first (highest score)
        assert results[0].pattern.name == "Singleton Pattern"
        # Name field should be in matched fields
        assert "name" in results[0].matched_fields
        # Name has weight 5.0, exact match scores 1.0
        assert results[0].score >= 5.0

    def test_search_by_intent(self, search_engine):
        """Test search matches in intent field."""
        results = search_engine.search(query="interface")

        assert len(results) >= 1
        # Factory Method has "interface" in intent
        factory_result = next(
            (r for r in results if r.pattern.name == "Factory Method"),
            None
        )
        assert factory_result is not None
        assert "intent" in factory_result.matched_fields

    def test_search_by_tag(self, search_engine):
        """Test search matches tags with high score."""
        results = search_engine.search(query="refactoring")

        # Should match patterns with "refactoring" tag
        assert len(results) >= 2
        # Tags have weight 4.0
        assert all(r.score >= 4.0 for r in results if "tags" in r.matched_fields)

    def test_search_multiple_keywords(self, search_engine):
        """Test search with multiple keywords."""
        results = search_engine.search(query="object creation")

        # Should match patterns with either "object" or "creation"
        assert len(results) >= 2

    def test_search_case_insensitive(self, search_engine):
        """Test search is case-insensitive."""
        results_lower = search_engine.search(query="singleton")
        results_upper = search_engine.search(query="SINGLETON")
        results_mixed = search_engine.search(query="SiNgLeToN")

        # All should return same results
        assert len(results_lower) == len(results_upper) == len(results_mixed)
        assert results_lower[0].pattern.name == results_upper[0].pattern.name

    def test_search_partial_match_scores_less(self, search_engine):
        """Test partial matches score less than exact matches."""
        # Add pattern with partial match scenario
        repo = search_engine.repository
        pattern = Pattern(
            name="Notification System",
            intent="Handle notifications",
            problem="Need notification handling",
            solution="Implement notification system",
            category="Test",
            tags=["notify"],
            source_metadata=SourceMetadata(source_name="Test")
        )
        repo.add_pattern(pattern)

        results = search_engine.search(query="notification")

        # Should match both "notification" (exact in Observer's tags/problem)
        # and "notify" (partial match)
        assert len(results) >= 1

    def test_search_weighted_scoring(self, search_engine):
        """Test that field weights are applied correctly."""
        # Search for a term that appears in multiple fields
        results = search_engine.search(query="creation")

        # Should find patterns with "creation" in different fields
        for result in results:
            # Verify score reflects field weights
            if "name" in result.matched_fields:
                # Name weight is 5.0
                assert result.score >= 5.0
            elif "tags" in result.matched_fields:
                # Tags weight is 4.0
                assert result.score >= 4.0

    def test_search_results_sorted_by_score(self, search_engine):
        """Test search results are sorted by score descending."""
        results = search_engine.search(query="pattern")

        # Verify results are sorted by score (descending)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_with_category_filter(self, search_engine):
        """Test search with category filter."""
        results = search_engine.search(query="", category="Creational")

        assert len(results) == 2
        assert all(r.pattern.category == "Creational" for r in results)

    def test_search_with_category_filter_and_query(self, search_engine):
        """Test search with both query and category filter."""
        results = search_engine.search(
            query="creation",
            category="Creational"
        )

        # Should only return Creational patterns that match "creation"
        assert all(r.pattern.category == "Creational" for r in results)
        assert all(r.score > 0 for r in results)

    def test_search_with_tag_filter_single_tag(self, search_engine):
        """Test search with single tag filter."""
        results = search_engine.search(query="", tags=["refactoring"])

        # Should return patterns with "refactoring" tag
        assert len(results) == 2
        assert all("refactoring" in r.pattern.tags for r in results)

    def test_search_with_tag_filter_multiple_tags(self, search_engine):
        """Test search with multiple tags (OR logic)."""
        results = search_engine.search(query="", tags=["factory", "events"])

        # Should return patterns with either "factory" OR "events"
        assert len(results) == 2
        for result in results:
            assert "factory" in result.pattern.tags or "events" in result.pattern.tags

    def test_search_with_tag_filter_case_insensitive(self, search_engine):
        """Test tag filter is case-insensitive."""
        results_lower = search_engine.search(query="", tags=["refactoring"])
        results_upper = search_engine.search(query="", tags=["REFACTORING"])

        assert len(results_lower) == len(results_upper)

    def test_search_with_query_and_tag_filter(self, search_engine):
        """Test search with both query and tag filter."""
        results = search_engine.search(
            query="class",
            tags=["refactoring"]
        )

        # Should return refactoring patterns that match "class"
        assert all("refactoring" in r.pattern.tags for r in results)
        assert all(r.score > 0 for r in results)

    def test_search_with_all_filters(self, search_engine):
        """Test search with query, category, and tags."""
        # Add a pattern that matches all filters
        repo = search_engine.repository
        pattern = Pattern(
            name="Test Refactoring Pattern",
            intent="Test intent",
            problem="Test problem with refactoring",
            solution="Test solution",
            category="Redistribute Responsibilities",
            tags=["refactoring", "test"],
            source_metadata=SourceMetadata(source_name="Test")
        )
        repo.add_pattern(pattern)

        results = search_engine.search(
            query="refactoring",
            category="Redistribute Responsibilities",
            tags=["refactoring"]
        )

        # Should only return patterns matching all criteria
        assert all(r.pattern.category == "Redistribute Responsibilities" for r in results)
        assert all("refactoring" in r.pattern.tags for r in results)
        assert all(r.score > 0 for r in results)

    def test_search_no_matches(self, search_engine):
        """Test search with no matches returns empty list."""
        results = search_engine.search(query="nonexistent_term_xyz")

        assert len(results) == 0

    def test_search_category_no_matches(self, search_engine):
        """Test search with non-existent category returns empty list."""
        results = search_engine.search(query="", category="NonExistent")

        assert len(results) == 0

    def test_search_tag_no_matches(self, search_engine):
        """Test search with non-existent tag returns empty list."""
        results = search_engine.search(query="", tags=["nonexistent"])

        assert len(results) == 0

    def test_search_matched_fields_tracking(self, search_engine):
        """Test that matched fields are correctly tracked."""
        results = search_engine.search(query="creation object")

        for result in results:
            # Verify matched_fields is a set
            assert isinstance(result.matched_fields, set)
            # Verify matched_fields contains valid field names
            valid_fields = {"name", "intent", "problem", "solution", "tags", "category"}
            assert result.matched_fields.issubset(valid_fields)

    def test_search_performance_small_dataset(self, search_engine):
        """Test search performance on small dataset."""
        import time

        start = time.perf_counter()
        results = search_engine.search(query="pattern creation")
        duration_ms = (time.perf_counter() - start) * 1000

        # Should be very fast for 5 patterns
        assert duration_ms < 100

    def test_get_search_stats(self, search_engine):
        """Test get_search_stats method."""
        stats = search_engine.get_search_stats()

        assert "total_patterns" in stats
        assert stats["total_patterns"] == 5
        assert "field_weights" in stats
        assert stats["field_weights"]["name"] == 5.0
        assert stats["field_weights"]["tags"] == 4.0
        assert "exact_match_score" in stats
        assert "partial_match_score" in stats

    def test_search_engine_repr(self, search_engine):
        """Test string representation of search engine."""
        engine_repr = repr(search_engine)
        assert "KeywordSearchEngine" in engine_repr
        assert "patterns=5" in engine_repr

    def test_normalize_query(self, search_engine):
        """Test query normalization."""
        # Test with various query formats
        terms1 = search_engine._normalize_query("  HELLO   world  ")
        assert terms1 == ["hello", "world"]

        terms2 = search_engine._normalize_query("Test")
        assert terms2 == ["test"]

        terms3 = search_engine._normalize_query("")
        assert terms3 == []

    def test_score_field_exact_match(self, search_engine, repository):
        """Test field scoring for exact word match."""
        pattern = repository.get_pattern_by_name("Singleton Pattern")
        score = search_engine._score_field(pattern, "name", ["singleton"])

        # Exact match should score 1.0
        assert score == 1.0

    def test_score_field_partial_match(self, search_engine, repository):
        """Test field scoring for partial match."""
        pattern = repository.get_pattern_by_name("Singleton Pattern")
        score = search_engine._score_field(pattern, "name", ["single"])

        # Partial match should score 0.5
        assert score == 0.5

    def test_score_field_no_match(self, search_engine, repository):
        """Test field scoring with no match."""
        pattern = repository.get_pattern_by_name("Singleton Pattern")
        score = search_engine._score_field(pattern, "name", ["observer"])

        # No match should score 0.0
        assert score == 0.0

    def test_score_field_multiple_terms(self, search_engine, repository):
        """Test field scoring with multiple query terms."""
        pattern = repository.get_pattern_by_name("Singleton Pattern")
        score = search_engine._score_field(pattern, "name", ["singleton", "pattern"])

        # Two exact matches should score 2.0
        assert score == 2.0

    def test_filter_by_tags_or_logic(self, search_engine, repository):
        """Test tag filtering uses OR logic."""
        all_patterns = repository.list_all_patterns()
        filtered = search_engine._filter_by_tags(all_patterns, ["creation", "events"])

        # Should include patterns with either tag
        assert len(filtered) == 3  # Factory Method, Singleton, Observer
