"""
Integration tests for complete search flow.

This test suite verifies the end-to-end search workflow:
1. Load patterns from file using OORPLoader
2. Search patterns using KeywordSearchEngine
3. Verify search results and performance
"""

import pytest
from pathlib import Path

from patternsphere.loaders.oorp_loader import OORPLoader
from patternsphere.search.search_engine import KeywordSearchEngine
from patternsphere.repository.pattern_repository import InMemoryPatternRepository


class TestSearchFlowIntegration:
    """Integration tests for complete search flow."""

    @pytest.fixture
    def oorp_patterns_file(self):
        """Get path to OORP patterns file."""
        # Use the 20-pattern dataset created in TASK-011
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_20.json")
        assert patterns_file.exists(), f"Pattern file not found: {patterns_file}"
        return str(patterns_file)

    @pytest.fixture
    def loaded_repository(self, oorp_patterns_file):
        """Create repository and load OORP patterns."""
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)

        # Load patterns
        stats = loader.load_from_file(oorp_patterns_file)

        # Verify loading was successful
        assert stats.loaded_successfully == 20
        assert stats.failed_patterns == 0
        assert repository.count() == 20

        return repository

    @pytest.fixture
    def search_engine(self, loaded_repository):
        """Create search engine with loaded patterns."""
        return KeywordSearchEngine(loaded_repository)

    def test_load_and_search_workflow(self, oorp_patterns_file):
        """Test complete workflow: load patterns then search."""
        # Step 1: Create repository
        repository = InMemoryPatternRepository()

        # Step 2: Load patterns
        loader = OORPLoader(repository)
        load_stats = loader.load_from_file(oorp_patterns_file)

        assert load_stats.loaded_successfully == 20
        assert load_stats.failed_patterns == 0
        assert repository.count() == 20

        # Step 3: Create search engine
        search_engine = KeywordSearchEngine(repository)

        # Step 4: Perform searches
        all_results = search_engine.search(query="")
        assert len(all_results) == 20

        # Search for specific patterns
        refactor_results = search_engine.search(query="refactor")
        assert len(refactor_results) > 0
        assert all(r.score > 0 for r in refactor_results)

    def test_search_oorp_first_contact_patterns(self, search_engine):
        """Test searching for First Contact category patterns."""
        results = search_engine.search(query="", category="First Contact")

        # Should find First Contact patterns
        assert len(results) >= 4  # We have several First Contact patterns
        assert all(r.pattern.category == "First Contact" for r in results)

        # Verify some expected patterns
        pattern_names = [r.pattern.name for r in results]
        assert "Read all the Code in One Hour" in pattern_names
        assert "Skim the Documentation" in pattern_names

    def test_search_oorp_by_keyword_code(self, search_engine):
        """Test searching OORP patterns by keyword 'code'."""
        results = search_engine.search(query="code")

        # Should find patterns mentioning code
        assert len(results) > 0
        assert all(r.score > 0 for r in results)

        # Top results should be highly relevant
        top_result = results[0]
        assert "code" in top_result.pattern.name.lower() or \
               "code" in top_result.pattern.intent.lower() or \
               "code" in top_result.pattern.problem.lower()

    def test_search_oorp_by_keyword_refactoring(self, search_engine):
        """Test searching OORP patterns by keyword 'refactoring'."""
        results = search_engine.search(query="refactoring")

        # Should find refactoring-related patterns
        assert len(results) > 0

        # Verify results are sorted by score
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_oorp_by_tag(self, search_engine):
        """Test searching OORP patterns by tag."""
        # Search for patterns with specific tags
        results = search_engine.search(query="", tags=["testing"])

        # Should find patterns tagged with testing
        assert len(results) > 0
        assert all("testing" in r.pattern.tags for r in results)

    def test_search_oorp_by_tag_refactoring(self, search_engine):
        """Test searching for refactoring tag."""
        results = search_engine.search(query="", tags=["refactoring"])

        # Should find refactoring patterns
        assert len(results) >= 2  # Multiple refactoring patterns
        assert all("refactoring" in r.pattern.tags for r in results)

    def test_search_oorp_multiple_keywords(self, search_engine):
        """Test searching with multiple keywords."""
        results = search_engine.search(query="system design")

        # Should find patterns mentioning system or design
        assert len(results) > 0
        assert all(r.score > 0 for r in results)

    def test_search_oorp_with_filters(self, search_engine):
        """Test searching with both query and filters."""
        results = search_engine.search(
            query="pattern",
            category="First Contact"
        )

        # Should only return First Contact patterns that match "pattern"
        assert all(r.pattern.category == "First Contact" for r in results)
        assert all(r.score > 0 for r in results)

    def test_search_oorp_case_insensitive(self, search_engine):
        """Test search is case-insensitive."""
        results_lower = search_engine.search(query="documentation")
        results_upper = search_engine.search(query="DOCUMENTATION")

        # Should return same results
        assert len(results_lower) == len(results_upper)
        if results_lower:
            assert results_lower[0].pattern.name == results_upper[0].pattern.name

    def test_search_pattern_by_exact_name(self, search_engine):
        """Test searching for pattern by exact name."""
        results = search_engine.search(query="Read all the Code in One Hour")

        # Should find the specific pattern with high score
        assert len(results) > 0
        assert results[0].pattern.name == "Read all the Code in One Hour"
        # Name field has highest weight (5.0)
        assert "name" in results[0].matched_fields

    def test_search_business_rules_pattern(self, search_engine):
        """Test searching for business rules pattern."""
        results = search_engine.search(query="business rules")

        # Should find "Record Business Rules as Tests"
        assert len(results) > 0
        pattern_names = [r.pattern.name for r in results]
        assert "Record Business Rules as Tests" in pattern_names

    def test_search_god_class_pattern(self, search_engine):
        """Test searching for God Class pattern."""
        results = search_engine.search(query="god class")

        # Should find "Split Up God Class"
        assert len(results) > 0
        assert results[0].pattern.name == "Split Up God Class"

    def test_search_with_tag_filter_multiple(self, search_engine):
        """Test searching with multiple tags."""
        results = search_engine.search(
            query="",
            tags=["onboarding", "documentation"]
        )

        # Should find patterns with either tag (OR logic)
        assert len(results) > 0
        for result in results:
            assert "onboarding" in result.pattern.tags or \
                   "documentation" in result.pattern.tags

    def test_search_all_categories_represented(self, search_engine):
        """Test that all OORP categories are represented in patterns."""
        # Get all categories
        repo = search_engine.repository
        categories = repo.get_all_categories()

        # Should have multiple categories
        assert len(categories) >= 5  # OORP has 8 categories, we have at least 5

        # Verify some expected categories
        expected_categories = [
            "First Contact",
            "Initial Understanding",
            "Detailed Model Capture",
            "Redistribute Responsibilities",
            "Migration Strategies"
        ]

        for category in expected_categories:
            assert category in categories
            assert categories[category] > 0

    def test_search_performance_20_patterns(self, search_engine):
        """Test search performance with 20 patterns."""
        import time

        # Perform multiple searches and measure time
        queries = [
            "code",
            "pattern",
            "refactoring",
            "system design",
            "business rules"
        ]

        for query in queries:
            start = time.perf_counter()
            results = search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000

            # Should be well under 100ms for 20 patterns
            assert duration_ms < 100, \
                f"Search for '{query}' took {duration_ms:.2f}ms (expected < 100ms)"

    def test_load_performance_20_patterns(self, oorp_patterns_file):
        """Test loading performance for 20 patterns."""
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)

        # Load and measure time
        stats = loader.load_from_file(oorp_patterns_file)

        # Should be well under 500ms for 20 patterns
        assert stats.duration_ms < 500, \
            f"Loading took {stats.duration_ms:.2f}ms (expected < 500ms)"

        # Verify all patterns loaded
        assert stats.loaded_successfully == 20
        assert stats.failed_patterns == 0

    def test_search_results_relevance_ranking(self, search_engine):
        """Test that search results are ranked by relevance."""
        results = search_engine.search(query="pattern")

        # Should have multiple results
        assert len(results) > 1

        # First result should have highest score
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score

        # Patterns with "pattern" in name should score higher
        # than patterns with "pattern" only in description
        name_matches = [r for r in results if "name" in r.matched_fields]
        if name_matches:
            other_matches = [r for r in results if "name" not in r.matched_fields]
            if other_matches:
                # Name matches should generally score higher
                assert name_matches[0].score > other_matches[-1].score

    def test_search_empty_results(self, search_engine):
        """Test search with no matches returns empty list."""
        results = search_engine.search(query="nonexistent_xyz_term")

        assert len(results) == 0

    def test_verify_pattern_completeness(self, loaded_repository):
        """Test that all loaded patterns have complete data."""
        patterns = loaded_repository.list_all_patterns()

        for pattern in patterns:
            # Verify required fields are present
            assert pattern.name
            assert pattern.intent
            assert pattern.problem
            assert pattern.solution
            assert pattern.category
            assert pattern.source_metadata
            assert pattern.source_metadata.source_name == "OORP"

            # Verify tags are present
            assert len(pattern.tags) > 0

    def test_search_by_related_patterns(self, search_engine):
        """Test that patterns have related_patterns defined."""
        # Get all patterns
        repo = search_engine.repository
        patterns = repo.list_all_patterns()

        # At least some patterns should have related patterns
        patterns_with_relations = [
            p for p in patterns
            if len(p.related_patterns) > 0
        ]

        assert len(patterns_with_relations) > 0

    def test_end_to_end_workflow_example(self, oorp_patterns_file):
        """Test complete end-to-end workflow example."""
        # Simulate real-world usage

        # 1. Initialize system
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        search_engine = KeywordSearchEngine(repository)

        # 2. Load patterns
        load_stats = loader.load_from_file(oorp_patterns_file)
        assert load_stats.success_rate == 100.0

        # 3. Browse all patterns
        all_patterns = search_engine.search(query="")
        assert len(all_patterns) == 20

        # 4. Search for refactoring patterns
        refactoring = search_engine.search(query="refactoring")
        assert len(refactoring) > 0

        # 5. Filter by category
        first_contact = search_engine.search(
            query="",
            category="First Contact"
        )
        assert len(first_contact) > 0

        # 6. Combined search
        specific = search_engine.search(
            query="code",
            category="First Contact"
        )
        assert all(r.pattern.category == "First Contact" for r in specific)

        # 7. Tag-based search
        tagged = search_engine.search(
            query="",
            tags=["testing"]
        )
        assert all("testing" in r.pattern.tags for r in tagged)
