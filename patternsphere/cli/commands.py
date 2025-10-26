"""
CLI commands for PatternSphere.

Implements all user-facing commands using Typer framework.
"""

import sys
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table

from patternsphere.cli.app_context import AppContext
from patternsphere.cli.formatters import SearchResultsFormatter, PatternViewFormatter
from patternsphere.config import settings

# Create console for rich output
console = Console()

# Create Typer app
app = typer.Typer(
    name="patternsphere",
    help="A unified knowledge base for software design patterns",
    add_completion=False,
)


def get_context() -> AppContext:
    """
    Get initialized application context.

    Design Pattern: Dependency Injection
    - Commands depend on AppContext abstraction
    - Context manages all component dependencies

    Returns:
        Initialized AppContext instance
    """
    ctx = AppContext.get_instance()
    if not ctx.is_initialized:
        try:
            ctx.initialize(auto_load=True)
        except Exception as e:
            console.print(f"[red]Error initializing application: {e}[/red]")
            raise typer.Exit(code=1)
    return ctx


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query (keywords)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Filter by tags (comma-separated)"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results"),
    show_scores: bool = typer.Option(True, "--scores/--no-scores", help="Show relevance scores"),
):
    """
    Search patterns by keywords.

    Search across pattern names, intents, problems, solutions, tags, and categories.
    Results are ranked by relevance with weighted field scoring.

    Examples:
        patternsphere search refactoring
        patternsphere search "code quality" --category "First Contact"
        patternsphere search testing --tags "quality,testing" --limit 10
    """
    ctx = get_context()

    # Parse tags if provided
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]

    try:
        # Perform search
        results = ctx.search_engine.search(
            query=query,
            category=category,
            tags=tag_list
        )

        # Limit results
        results = results[:limit]

        # Format and display
        formatter = SearchResultsFormatter(
            terminal_width=settings.terminal_width,
            use_rich=True
        )
        output = formatter.format(results, show_scores=show_scores)
        console.print(output)

    except Exception as e:
        console.print(f"[red]Error performing search: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def list(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    sort: str = typer.Option("name", "--sort", "-s", help="Sort by: name, category"),
):
    """
    List all patterns or filter by category.

    Shows a table of all patterns with their categories and tags.
    Can be filtered by category and sorted by different fields.

    Examples:
        patternsphere list
        patternsphere list --category "First Contact"
        patternsphere list --sort category
    """
    ctx = get_context()

    try:
        # Get all patterns
        patterns = ctx.repository.list_all_patterns()

        # Filter by category if specified
        if category:
            patterns = [p for p in patterns if p.category == category]

        # Sort patterns
        if sort == "name":
            patterns = sorted(patterns, key=lambda p: p.name.lower())
        elif sort == "category":
            patterns = sorted(patterns, key=lambda p: (p.category, p.name.lower()))
        else:
            console.print(f"[yellow]Warning: Unknown sort field '{sort}', using 'name'[/yellow]")
            patterns = sorted(patterns, key=lambda p: p.name.lower())

        # Create table
        table = Table(title=f"Patterns ({len(patterns)} total)")
        table.add_column("No.", style="cyan", width=4)
        table.add_column("Name", style="green")
        table.add_column("Category", style="blue")
        table.add_column("Tags", style="yellow")

        for idx, pattern in enumerate(patterns, 1):
            tags_str = ", ".join(pattern.tags[:3])  # Show first 3 tags
            if len(pattern.tags) > 3:
                tags_str += "..."
            table.add_row(
                str(idx),
                pattern.name,
                pattern.category,
                tags_str
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing patterns: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def view(
    pattern_identifier: str = typer.Argument(..., help="Pattern ID or name"),
):
    """
    Show complete pattern details.

    Displays full information about a pattern including problem, solution,
    consequences, and related patterns. Works with both pattern ID and name.

    Examples:
        patternsphere view "Read all the Code in One Hour"
        patternsphere view OORP-001
    """
    ctx = get_context()

    try:
        # Try to find pattern by ID first, then by name
        pattern = None

        # Try by ID
        pattern = ctx.repository.get_pattern_by_id(pattern_identifier)

        # If not found, try by name (case-insensitive)
        if pattern is None:
            patterns = ctx.repository.list_all_patterns()
            for p in patterns:
                if p.name.lower() == pattern_identifier.lower():
                    pattern = p
                    break

        if pattern is None:
            console.print(f"[red]Pattern not found: {pattern_identifier}[/red]")
            console.print("\n[yellow]Hint:[/yellow] Use 'patternsphere list' to see all available patterns")
            raise typer.Exit(code=1)

        # Format and display
        formatter = PatternViewFormatter(
            terminal_width=settings.terminal_width,
            use_rich=True
        )
        output = formatter.format(pattern)
        console.print(output)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error viewing pattern: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def categories():
    """
    List all categories with pattern counts.

    Shows all available categories sorted alphabetically with the number
    of patterns in each category.

    Examples:
        patternsphere categories
    """
    ctx = get_context()

    try:
        # Get category counts
        category_counts = ctx.get_pattern_count_by_category()

        # Create table
        table = Table(title="Pattern Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Patterns", style="green", justify="right")

        # Sort by category name
        for category in sorted(category_counts.keys()):
            count = category_counts[category]
            table.add_row(category, str(count))

        # Add total row
        total = sum(category_counts.values())
        table.add_row("[bold]TOTAL[/bold]", f"[bold]{total}[/bold]")

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing categories: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def info():
    """
    Show system information.

    Displays application version, pattern count, loaded sources,
    and other system information.

    Examples:
        patternsphere info
    """
    ctx = get_context()

    try:
        # Create info table
        table = Table(title=f"{settings.app_name} v{settings.app_version}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        # Add rows
        table.add_row("Application", settings.app_name)
        table.add_row("Version", settings.app_version)
        table.add_row("Description", settings.app_description)
        table.add_row("Total Patterns", str(ctx.get_pattern_count()))
        table.add_row("Categories", str(len(ctx.get_categories())))

        # Load stats if available
        if ctx.load_stats:
            table.add_row("Load Time", f"{ctx.load_stats.duration_ms:.2f}ms")
            table.add_row("Load Success Rate", f"{ctx.load_stats.success_rate:.1f}%")

        # Data source
        table.add_row("Data Source", "OORP (Object-Oriented Reengineering Patterns)")

        console.print(table)

        # Show categories
        categories = ctx.get_categories()
        if categories:
            console.print(f"\n[cyan]Available Categories:[/cyan] {', '.join(categories)}")

    except Exception as e:
        console.print(f"[red]Error displaying info: {e}[/red]")
        raise typer.Exit(code=1)


# Add callback for version option
def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"{settings.app_name} v{settings.app_version}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    ),
):
    """
    PatternSphere - A unified knowledge base for software design patterns.

    Use commands to search, browse, and explore design patterns.
    Run 'patternsphere COMMAND --help' for detailed help on any command.
    """
    pass


if __name__ == "__main__":
    app()
