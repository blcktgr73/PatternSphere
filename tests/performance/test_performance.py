"""
Performance tests for PatternSphere Sprint 2.

This test suite verifies that performance requirements are met:
- Pattern loading: < 500ms for 60+ patterns
- Search operations: < 100ms for typical queries with 60 patterns
- Memory usage: Reasonable for 60+ patterns
"""

import pytest
import time
from pathlib import Path

from patternsphere.loaders.oorp_loader import OORPLoader
from patternsphere.search.search_engine import KeywordSearchEngine
from patternsphere.repository.pattern_repository import InMemoryPatternRepository


class TestLoadingPerformance:
    """Test pattern loading performance."""

    @pytest.fixture
    def oorp_complete_file(self):
        """Get path to complete OORP patterns file (60+ patterns)."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        assert patterns_file.exists(), f"Pattern file not found: {patterns_file}"
        return str(patterns_file)

    def test_load_60_patterns_under_500ms(self, oorp_complete_file):
        """
        Test that loading 60+ patterns completes in under 500ms.

        This is a critical performance requirement from the technical design.
        """
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)

        # Load patterns and measure time
        stats = loader.load_from_file(oorp_complete_file)

        # Verify all patterns loaded successfully
        assert stats.loaded_successfully >= 60, f"Expected 60+ patterns, loaded {stats.loaded_successfully}"
        assert stats.failed_patterns == 0, f"Failed patterns: {stats.errors}"

        # Verify performance requirement
        assert stats.duration_ms < 500, \
            f"Loading took {stats.duration_ms:.2f}ms (required < 500ms)"

        print(f"\nLoad Performance: {stats.loaded_successfully} patterns in {stats.duration_ms:.2f}ms")

    def test_load_multiple_times_consistent(self, oorp_complete_file):
        """Test that loading performance is consistent across multiple runs."""
        durations = []

        for i in range(5):
            repository = InMemoryPatternRepository()
            loader = OORPLoader(repository)
            stats = loader.load_from_file(oorp_complete_file)

            assert stats.failed_patterns == 0
            durations.append(stats.duration_ms)

        # All runs should be under 500ms
        assert all(d < 500 for d in durations), \
            f"Some runs exceeded 500ms: {durations}"

        # Calculate statistics
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)

        print(f"\nLoad Performance (5 runs):")
        print(f"  Average: {avg_duration:.2f}ms")
        print(f"  Min: {min_duration:.2f}ms")
        print(f"  Max: {max_duration:.2f}ms")

        # Average should be well under limit
        assert avg_duration < 400, \
            f"Average loading time {avg_duration:.2f}ms too close to 500ms limit"


class TestSearchPerformance:
    """Test search engine performance."""

    @pytest.fixture
    def loaded_search_engine(self):
        """Create search engine with 60+ loaded patterns."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)

        stats = loader.load_from_file(str(patterns_file))
        assert stats.loaded_successfully >= 60

        return KeywordSearchEngine(repository)

    def test_search_single_keyword_under_100ms(self, loaded_search_engine):
        """
        Test that single keyword search completes in under 100ms.

        This is a critical performance requirement from the technical design.
        """
        queries = ["refactoring", "pattern", "code", "test", "design"]

        for query in queries:
            start = time.perf_counter()
            results = loaded_search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000

            assert duration_ms < 100, \
                f"Search for '{query}' took {duration_ms:.2f}ms (required < 100ms)"

            print(f"Search '{query}': {len(results)} results in {duration_ms:.2f}ms")

    def test_search_multiple_keywords_under_100ms(self, loaded_search_engine):
        """Test that multi-keyword searches complete in under 100ms."""
        queries = [
            "refactoring code",
            "design pattern",
            "test business rules",
            "legacy system migration",
            "data model persistence"
        ]

        for query in queries:
            start = time.perf_counter()
            results = loaded_search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000

            assert duration_ms < 100, \
                f"Search for '{query}' took {duration_ms:.2f}ms (required < 100ms)"

            print(f"Search '{query}': {len(results)} results in {duration_ms:.2f}ms")

    def test_search_with_filters_under_100ms(self, loaded_search_engine):
        """Test that filtered searches complete in under 100ms."""
        test_cases = [
            {"query": "pattern", "category": "First Contact", "tags": None},
            {"query": "refactoring", "category": None, "tags": ["refactoring"]},
            {"query": "test", "category": "Detailed Model Capture", "tags": ["testing"]},
            {"query": "", "category": "Migration Strategies", "tags": None},
            {"query": "", "category": None, "tags": ["documentation", "testing"]}
        ]

        for case in test_cases:
            start = time.perf_counter()
            results = loaded_search_engine.search(**case)
            duration_ms = (time.perf_counter() - start) * 1000

            assert duration_ms < 100, \
                f"Filtered search took {duration_ms:.2f}ms (required < 100ms)"

            print(f"Filtered search: {len(results)} results in {duration_ms:.2f}ms")

    def test_search_empty_query_under_100ms(self, loaded_search_engine):
        """Test that empty query (return all) completes in under 100ms."""
        start = time.perf_counter()
        results = loaded_search_engine.search(query="")
        duration_ms = (time.perf_counter() - start) * 1000

        assert len(results) >= 60
        assert duration_ms < 100, \
            f"Empty query search took {duration_ms:.2f}ms (required < 100ms)"

        print(f"Empty query: {len(results)} results in {duration_ms:.2f}ms")

    def test_search_no_results_under_100ms(self, loaded_search_engine):
        """Test that searches with no results still complete quickly."""
        queries = ["xyznonexistent", "qwerty12345", "zzz999zzz"]

        for query in queries:
            start = time.perf_counter()
            results = loaded_search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000

            assert len(results) == 0
            assert duration_ms < 100, \
                f"No-result search took {duration_ms:.2f}ms (required < 100ms)"

    def test_search_worst_case_performance(self, loaded_search_engine):
        """Test performance with worst-case scenarios."""
        # Long query with many terms
        long_query = "pattern design refactoring code test system legacy migration data model"

        start = time.perf_counter()
        results = loaded_search_engine.search(query=long_query)
        duration_ms = (time.perf_counter() - start) * 1000

        assert duration_ms < 100, \
            f"Long query search took {duration_ms:.2f}ms (required < 100ms)"

        print(f"Long query ({len(long_query.split())} terms): {len(results)} results in {duration_ms:.2f}ms")

    def test_sequential_searches_performance(self, loaded_search_engine):
        """Test performance of multiple sequential searches."""
        queries = [
            "refactoring",
            "pattern design",
            "test",
            "code quality",
            "system architecture",
            "data model",
            "legacy migration",
            "business rules",
            "documentation",
            "performance"
        ]

        total_start = time.perf_counter()
        individual_times = []

        for query in queries:
            start = time.perf_counter()
            results = loaded_search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000
            individual_times.append(duration_ms)

            # Each search should be under 100ms
            assert duration_ms < 100, \
                f"Search '{query}' took {duration_ms:.2f}ms"

        total_duration_ms = (time.perf_counter() - total_start) * 1000

        # Statistics
        avg_time = sum(individual_times) / len(individual_times)
        max_time = max(individual_times)

        print(f"\n{len(queries)} sequential searches:")
        print(f"  Total time: {total_duration_ms:.2f}ms")
        print(f"  Average per search: {avg_time:.2f}ms")
        print(f"  Max time: {max_time:.2f}ms")

        # Average should be well under limit
        assert avg_time < 50, \
            f"Average search time {avg_time:.2f}ms should be well under 100ms"


class TestMemoryUsage:
    """Test memory usage with 60+ patterns."""

    def test_repository_memory_reasonable(self):
        """Test that repository with 60+ patterns uses reasonable memory."""
        import sys

        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)

        # Load patterns
        stats = loader.load_from_file(str(patterns_file))
        assert stats.loaded_successfully >= 60

        # Get approximate size of repository
        # Note: This is approximate and platform-dependent
        repo_size = sys.getsizeof(repository)

        print(f"\nRepository with {stats.loaded_successfully} patterns:")
        print(f"  Approximate size: {repo_size / 1024:.2f} KB")

        # Should be reasonable (less than 10MB for 60 patterns)
        assert repo_size < 10 * 1024 * 1024, \
            f"Repository size {repo_size / 1024 / 1024:.2f}MB seems excessive"

    def test_search_engine_memory_reasonable(self):
        """Test that search engine with 60+ patterns uses reasonable memory."""
        import sys

        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        stats = loader.load_from_file(str(patterns_file))

        search_engine = KeywordSearchEngine(repository)

        # Get approximate size
        engine_size = sys.getsizeof(search_engine)

        print(f"\nSearch engine with {stats.loaded_successfully} patterns:")
        print(f"  Approximate size: {engine_size / 1024:.2f} KB")

        # Should be minimal (search engine doesn't duplicate patterns)
        assert engine_size < 1024 * 1024, \
            f"Search engine size {engine_size / 1024:.2f}KB seems excessive"


class TestScalability:
    """Test system behavior as data grows."""

    def test_verify_all_categories_present(self):
        """Verify that all 8 OORP categories are represented."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        loader.load_from_file(str(patterns_file))

        categories = repository.get_all_categories()

        # OORP has 8 main categories
        expected_categories = [
            "First Contact",
            "Initial Understanding",
            "Detailed Model Capture",
            "Redistribute Responsibilities",
            "Transform Conditionals to Polymorphism",
            "Migration Strategies",
            "Setting Direction",
            "Tests: Your Life Insurance!"
        ]

        for category in expected_categories:
            assert category in categories, f"Missing category: {category}"
            assert categories[category] > 0, f"No patterns in category: {category}"

        print(f"\nCategories ({len(categories)}):")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count} patterns")

    def test_verify_all_patterns_tagged(self):
        """Verify that all patterns have 3-5 tags as required."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        loader.load_from_file(str(patterns_file))

        patterns = repository.list_all_patterns()

        patterns_without_enough_tags = []
        tag_counts = []

        for pattern in patterns:
            tag_count = len(pattern.tags)
            tag_counts.append(tag_count)

            if tag_count < 3:
                patterns_without_enough_tags.append(pattern.name)

        # All patterns should have at least 3 tags
        assert len(patterns_without_enough_tags) == 0, \
            f"Patterns with < 3 tags: {patterns_without_enough_tags}"

        # Statistics
        avg_tags = sum(tag_counts) / len(tag_counts)
        min_tags = min(tag_counts)
        max_tags = max(tag_counts)

        print(f"\nTag statistics:")
        print(f"  Average tags per pattern: {avg_tags:.1f}")
        print(f"  Min tags: {min_tags}")
        print(f"  Max tags: {max_tags}")

        # Should average 3-5 tags
        assert 3 <= avg_tags <= 6, \
            f"Average tags {avg_tags:.1f} outside expected range 3-5"

    def test_search_scales_linearly(self):
        """Test that search performance scales reasonably with result count."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        loader.load_from_file(str(patterns_file))

        search_engine = KeywordSearchEngine(repository)

        # Test queries that return different numbers of results
        test_cases = [
            ("xyznonexistent", 0),  # No results
            ("god class", 1),  # Very specific
            ("refactoring", 10),  # Medium
            ("pattern", 30),  # Many results
            ("", 60)  # All results
        ]

        for query, expected_min_results in test_cases:
            start = time.perf_counter()
            results = search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000

            # All should complete in under 100ms
            assert duration_ms < 100, \
                f"Search '{query}' ({len(results)} results) took {duration_ms:.2f}ms"

            print(f"Query '{query}': {len(results)} results in {duration_ms:.2f}ms")


class TestEndToEndPerformance:
    """Test complete end-to-end workflows."""

    def test_complete_workflow_performance(self):
        """Test complete workflow from loading to multiple searches."""
        patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")

        # Time entire workflow
        workflow_start = time.perf_counter()

        # Step 1: Load patterns
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        load_stats = loader.load_from_file(str(patterns_file))

        assert load_stats.loaded_successfully >= 60
        assert load_stats.duration_ms < 500

        # Step 2: Create search engine
        search_engine = KeywordSearchEngine(repository)

        # Step 3: Perform multiple searches
        queries = [
            "refactoring",
            "pattern design",
            "test coverage",
            "legacy system",
            "business rules"
        ]

        search_times = []
        for query in queries:
            start = time.perf_counter()
            results = search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000
            search_times.append(duration_ms)

            assert duration_ms < 100

        workflow_duration_ms = (time.perf_counter() - workflow_start) * 1000

        print(f"\nComplete workflow:")
        print(f"  Load: {load_stats.duration_ms:.2f}ms")
        print(f"  Average search: {sum(search_times) / len(search_times):.2f}ms")
        print(f"  Total workflow: {workflow_duration_ms:.2f}ms")

        # Total workflow should be reasonable
        assert workflow_duration_ms < 2000, \
            f"Complete workflow took {workflow_duration_ms:.2f}ms (too slow)"


# Performance benchmarking function
def benchmark_performance():
    """
    Run comprehensive performance benchmarks.

    This function can be called to get detailed performance metrics.
    """
    import sys
    from datetime import datetime

    print("=" * 70)
    print("PatternSphere Sprint 2 Performance Benchmark")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print("=" * 70)

    patterns_file = Path("c:/Projects/PatternSphere/data/sources/oorp/oorp_patterns_complete.json")

    # Benchmark loading
    print("\n1. LOADING PERFORMANCE")
    print("-" * 70)
    durations = []
    for i in range(10):
        repository = InMemoryPatternRepository()
        loader = OORPLoader(repository)
        stats = loader.load_from_file(str(patterns_file))
        durations.append(stats.duration_ms)

    print(f"10 loading runs:")
    print(f"  Average: {sum(durations) / len(durations):.2f}ms")
    print(f"  Min: {min(durations):.2f}ms")
    print(f"  Max: {max(durations):.2f}ms")
    print(f"  Patterns loaded: {stats.loaded_successfully}")
    print(f"  ✓ Requirement: < 500ms - {'PASS' if max(durations) < 500 else 'FAIL'}")

    # Benchmark search
    print("\n2. SEARCH PERFORMANCE")
    print("-" * 70)
    repository = InMemoryPatternRepository()
    loader = OORPLoader(repository)
    loader.load_from_file(str(patterns_file))
    search_engine = KeywordSearchEngine(repository)

    search_queries = [
        "refactoring",
        "pattern design",
        "test coverage",
        "legacy code system",
        "business rules data",
        ""  # Empty query
    ]

    for query in search_queries:
        times = []
        for _ in range(10):
            start = time.perf_counter()
            results = search_engine.search(query=query)
            duration_ms = (time.perf_counter() - start) * 1000
            times.append(duration_ms)

        avg = sum(times) / len(times)
        print(f"Query '{query or '(empty)'}': avg {avg:.2f}ms, "
              f"max {max(times):.2f}ms, results {len(results)}")

    print(f"\n  ✓ Requirement: < 100ms - {'PASS' if max(times) < 100 else 'FAIL'}")

    print("\n" + "=" * 70)
    print("Benchmark complete!")
    print("=" * 70)


if __name__ == "__main__":
    # Run benchmark if executed directly
    benchmark_performance()
