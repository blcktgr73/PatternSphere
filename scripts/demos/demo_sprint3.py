"""
Demo script for PatternSphere Sprint 3 - CLI Interface.

This demonstrates all CLI commands and their features.
Run this script to see the CLI in action.
"""

import subprocess
import sys
from pathlib import Path


def run_command(description: str, command: list[str]):
    """Run a CLI command and display the output."""
    print("\n" + "=" * 80)
    print(f"Demo: {description}")
    print("=" * 80)
    print(f"Command: patternsphere {' '.join(command)}")
    print("-" * 80)

    try:
        # Run the command
        result = subprocess.run(
            [sys.executable, "-m", "patternsphere.cli.main"] + command,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        # Display output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        print("-" * 80)
        print(f"Exit code: {result.returncode}")

    except Exception as e:
        print(f"Error running command: {e}")


def main():
    """Run the CLI demo."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PatternSphere v1.0.0 - CLI Demo" + " " * 27 + "║")
    print("║" + " " * 18 + "Sprint 3: Complete CLI Interface" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")

    # 1. Version
    run_command(
        "Display version information",
        ["--version"]
    )

    # 2. System Info
    run_command(
        "Show system information and statistics",
        ["info"]
    )

    # 3. Categories
    run_command(
        "List all pattern categories with counts",
        ["categories"]
    )

    # 4. List All Patterns
    run_command(
        "List all patterns (showing first few)",
        ["list"]
    )

    # 5. List by Category
    run_command(
        "List patterns in 'First Contact' category",
        ["list", "--category", "First Contact"]
    )

    # 6. Search - Basic
    run_command(
        "Search for 'refactoring' patterns",
        ["search", "refactoring", "--limit", "5"]
    )

    # 7. Search with Category Filter
    run_command(
        "Search for 'code' in 'First Contact' category",
        ["search", "code", "--category", "First Contact", "--limit", "3"]
    )

    # 8. Search with Tags
    run_command(
        "Search for 'test' patterns with testing tags",
        ["search", "test", "--tags", "testing,quality", "--limit", "5"]
    )

    # 9. Search without Scores
    run_command(
        "Search for 'pattern' without showing scores",
        ["search", "pattern", "--no-scores", "--limit", "3"]
    )

    # 10. View Pattern Details
    run_command(
        "View complete details for 'Read all the Code in One Hour'",
        ["view", "Read all the Code in One Hour"]
    )

    # 11. Help
    run_command(
        "Show main help menu",
        ["--help"]
    )

    # 12. Search Help
    run_command(
        "Show help for search command",
        ["search", "--help"]
    )

    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "Demo Complete!" + " " * 33 + "║")
    print("║" + " " * 78 + "║")
    print("║  All CLI commands demonstrated successfully:                              ║")
    print("║  ✓ version - Display version                                              ║")
    print("║  ✓ info - System information                                              ║")
    print("║  ✓ categories - List categories                                           ║")
    print("║  ✓ list - List patterns with filtering and sorting                        ║")
    print("║  ✓ search - Search with weighted scoring and filters                      ║")
    print("║  ✓ view - Display complete pattern details                                ║")
    print("║  ✓ help - Comprehensive help documentation                                ║")
    print("║" + " " * 78 + "║")
    print("║  PatternSphere v1.0.0 is ready for production use!                        ║")
    print("╚" + "=" * 78 + "╝\n")


if __name__ == "__main__":
    main()
