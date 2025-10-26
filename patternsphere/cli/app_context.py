"""
Application context for dependency injection.

Implements the Singleton pattern to ensure a single instance manages
the application's core components (repository, search engine, loaders).
"""

from typing import Optional
from pathlib import Path
import time

from patternsphere.config import settings
from patternsphere.repository import InMemoryPatternRepository, IPatternRepository
from patternsphere.search import KeywordSearchEngine
from patternsphere.loaders import OORPLoader, LoaderStats


class AppContext:
    """
    Application context singleton.

    Manages the lifecycle of core application components:
    - Pattern repository
    - Search engine
    - Pattern loaders

    Design Pattern: Singleton
    - Ensures single shared instance across the application
    - Lazy initialization of components
    - Thread-safe via Python's module-level singleton

    Example:
        ctx = AppContext.get_instance()
        patterns = ctx.repository.get_all()
        results = ctx.search_engine.search("refactoring")
    """

    _instance: Optional["AppContext"] = None

    def __init__(self):
        """Initialize context (use get_instance() instead)."""
        if AppContext._instance is not None:
            raise RuntimeError("Use AppContext.get_instance() to get the singleton instance")

        self._repository: Optional[IPatternRepository] = None
        self._search_engine: Optional[KeywordSearchEngine] = None
        self._initialized: bool = False
        self._load_stats: Optional[LoaderStats] = None

    @classmethod
    def get_instance(cls) -> "AppContext":
        """
        Get the singleton instance.

        Returns:
            The singleton AppContext instance
        """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._repository = None
            cls._instance._search_engine = None
            cls._instance._initialized = False
            cls._instance._load_stats = None
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        cls._instance = None

    def initialize(self, auto_load: bool = True) -> None:
        """
        Initialize the application context.

        Args:
            auto_load: If True, automatically load patterns from default source

        Design Principle: Dependency Inversion
        - Components depend on abstractions (IPatternRepository)
        - Concrete implementations injected here
        """
        if self._initialized:
            return

        # Create repository
        self._repository = InMemoryPatternRepository()

        # Create search engine
        self._search_engine = KeywordSearchEngine(self._repository)

        # Auto-load patterns if requested
        if auto_load:
            self.load_patterns()

        self._initialized = True

    def load_patterns(self, file_path: Optional[Path] = None) -> LoaderStats:
        """
        Load patterns from a file.

        Args:
            file_path: Path to patterns file (uses default if None)

        Returns:
            LoaderStats with loading statistics

        Raises:
            RuntimeError: If repository not initialized
        """
        if self._repository is None:
            raise RuntimeError("Repository not initialized. Call initialize() first.")

        # Use default path if none provided
        if file_path is None:
            file_path = settings.get_absolute_path(settings.oorp_patterns_file)

        # Create loader and load patterns
        loader = OORPLoader(self._repository)
        self._load_stats = loader.load_from_file(str(file_path))

        return self._load_stats

    @property
    def repository(self) -> IPatternRepository:
        """
        Get the pattern repository.

        Returns:
            The pattern repository instance

        Raises:
            RuntimeError: If not initialized
        """
        if self._repository is None:
            raise RuntimeError("AppContext not initialized. Call initialize() first.")
        return self._repository

    @property
    def search_engine(self) -> KeywordSearchEngine:
        """
        Get the search engine.

        Returns:
            The search engine instance

        Raises:
            RuntimeError: If not initialized
        """
        if self._search_engine is None:
            raise RuntimeError("AppContext not initialized. Call initialize() first.")
        return self._search_engine

    @property
    def load_stats(self) -> Optional[LoaderStats]:
        """Get the statistics from the last pattern load operation."""
        return self._load_stats

    @property
    def is_initialized(self) -> bool:
        """Check if the context is initialized."""
        return self._initialized

    def get_pattern_count(self) -> int:
        """Get the total number of loaded patterns."""
        if self._repository is None:
            return 0
        return self._repository.count()

    def get_categories(self) -> list[str]:
        """Get a list of all unique categories."""
        if self._repository is None:
            return []
        return sorted(self._repository.get_all_categories().keys())

    def get_pattern_count_by_category(self) -> dict[str, int]:
        """Get pattern counts grouped by category."""
        if self._repository is None:
            return {}
        return self._repository.get_all_categories()
