"""
Main entry point for PatternSphere CLI.

This module provides the CLI entry point that is registered as a console script.
"""

from patternsphere.cli.commands import app


def cli():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    cli()
