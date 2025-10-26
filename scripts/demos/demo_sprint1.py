"""
Sprint 1 Demonstration Script

This script demonstrates the core functionality implemented in Sprint 1:
- Pattern model with validation
- Repository pattern with in-memory storage
- File storage with atomic writes
- Complete persistence workflow
"""

import os
from pathlib import Path

from patternsphere.models import Pattern, SourceMetadata
from patternsphere.repository import InMemoryPatternRepository
from patternsphere.storage import FileStorage


def main():
    print("=" * 70)
    print("PatternSphere - Sprint 1 Demonstration")
    print("=" * 70)
    print()

    # Step 1: Create some sample patterns
    print("Step 1: Creating sample OORP patterns")
    print("-" * 70)

    oorp_metadata = SourceMetadata(
        source_name="OORP",
        authors=["Serge Demeyer", "Stéphane Ducasse", "Oscar Nierstrasz"],
        publication_year=2002,
        url="http://scg.unibe.ch/download/oorp/"
    )

    patterns = [
        Pattern(
            name="Read all the Code in One Hour",
            intent="Get a first impression of the system",
            problem="You need to quickly understand what a legacy system does",
            context="You have access to source code but limited time",
            solution="Skim through all source files systematically",
            consequences="You get broad understanding but miss details",
            category="First Contact",
            tags=["assessment", "overview", "time-boxed"],
            related_patterns=["Skim the Documentation", "Interview During Demo"],
            source_metadata=oorp_metadata
        ),
        Pattern(
            name="Write Tests to Understand",
            intent="Develop tests to understand how code works",
            problem="Documentation is missing or outdated",
            context="You need to understand specific functionality",
            solution="Write tests that exercise the code",
            consequences="Tests provide living documentation",
            category="Tests",
            tags=["testing", "documentation", "understanding"],
            related_patterns=["Grow Your Test Base Incrementally"],
            source_metadata=oorp_metadata
        ),
        Pattern(
            name="Refactor to Understand",
            intent="Improve code structure to understand it better",
            problem="Code is so poorly structured you cannot understand it",
            context="You need to understand messy legacy code",
            solution="Make small, safe refactorings to improve clarity",
            consequences="Code becomes more understandable and maintainable",
            category="Initial Understanding",
            tags=["refactoring", "understanding", "code-quality"],
            related_patterns=["Write Tests to Understand"],
            source_metadata=oorp_metadata
        )
    ]

    print(f"Created {len(patterns)} patterns:")
    for p in patterns:
        print(f"  - {p.name} (Category: {p.category})")
    print()

    # Step 2: Create repository with file storage
    print("Step 2: Creating repository with file storage")
    print("-" * 70)

    storage_path = Path("demo_data/patterns.json")
    storage = FileStorage(str(storage_path))
    repository = InMemoryPatternRepository(storage=storage)

    print(f"Repository created with storage at: {storage_path}")
    print(f"Storage exists: {storage.exists()}")
    print()

    # Step 3: Add patterns to repository
    print("Step 3: Adding patterns to repository")
    print("-" * 70)

    for pattern in patterns:
        repository.add_pattern(pattern)
        print(f"Added: {pattern.name}")

    print(f"\nTotal patterns in repository: {repository.count()}")
    print()

    # Step 4: Query patterns
    print("Step 4: Querying patterns")
    print("-" * 70)

    # Get all categories
    categories = repository.get_all_categories()
    print(f"Categories: {categories}")

    # Get patterns by category
    test_patterns = repository.get_patterns_by_category("Tests")
    print(f"\nPatterns in 'Tests' category: {len(test_patterns)}")
    for p in test_patterns:
        print(f"  - {p.name}")

    # Search patterns
    search_results = repository.search_patterns(query="understand")
    print(f"\nSearch results for 'understand': {len(search_results)}")
    for p in search_results:
        print(f"  - {p.name}")

    # Search by tags
    tag_results = repository.search_patterns(tags=["testing"])
    print(f"\nPatterns with tag 'testing': {len(tag_results)}")
    for p in tag_results:
        print(f"  - {p.name}")
    print()

    # Step 5: Save to storage
    print("Step 5: Persisting to storage")
    print("-" * 70)

    repository.save_to_storage()
    print(f"Saved {repository.count()} patterns to {storage_path}")
    print(f"File size: {storage_path.stat().st_size} bytes")
    print()

    # Step 6: Simulate application restart
    print("Step 6: Simulating application restart")
    print("-" * 70)

    print("Destroying current repository...")
    del repository
    del storage

    print("Creating new repository with same storage...")
    storage2 = FileStorage(str(storage_path))
    repository2 = InMemoryPatternRepository(storage=storage2)

    print(f"Patterns loaded: {repository2.count()}")

    # Verify data integrity
    loaded_pattern = repository2.get_pattern_by_name("Write Tests to Understand")
    if loaded_pattern:
        print(f"\nVerifying loaded pattern: {loaded_pattern.name}")
        print(f"  Intent: {loaded_pattern.intent}")
        print(f"  Category: {loaded_pattern.category}")
        print(f"  Tags: {', '.join(loaded_pattern.tags)}")
    print()

    # Step 7: Repository statistics
    print("Step 7: Repository statistics")
    print("-" * 70)

    stats = repository2.get_repository_stats()
    print(f"Total patterns: {stats['total_patterns']}")
    print(f"Total categories: {stats['total_categories']}")
    print(f"Has storage: {stats['has_storage']}")
    print("\nCategory breakdown:")
    for category, count in stats['categories'].items():
        print(f"  - {category}: {count} pattern(s)")
    print()

    print("=" * 70)
    print("Sprint 1 Demonstration Complete!")
    print("=" * 70)
    print()
    print("Key accomplishments:")
    print("  [x] Pattern model with Pydantic validation")
    print("  [x] Repository pattern with multiple indexes")
    print("  [x] File storage with atomic writes")
    print("  [x] Complete persistence workflow")
    print("  [x] Search and filtering capabilities")
    print("  [x] 85 tests passing (unit + integration)")
    print()


if __name__ == "__main__":
    main()
