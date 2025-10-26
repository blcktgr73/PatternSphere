"""
OORP Pattern Loader for PatternSphere.

This module provides functionality to load OORP patterns from JSON files
into the pattern repository.

Design Principles Applied:
- Single Responsibility: Handles only pattern loading from JSON
- Dependency Inversion: Depends on IPatternRepository abstraction
- Open/Closed: Extensible for other file formats
- Error Handling: Continues loading even if individual patterns fail
"""

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from patternsphere.models.pattern import Pattern
from patternsphere.repository.repository_interface import (
    IPatternRepository,
    RepositoryError
)


logger = logging.getLogger(__name__)


@dataclass
class LoaderStats:
    """
    Statistics from a pattern loading operation.

    Attributes:
        total_patterns: Total number of patterns in the source file
        loaded_successfully: Number of patterns loaded successfully
        failed_patterns: Number of patterns that failed to load
        duration_ms: Time taken to load patterns in milliseconds
        errors: List of error messages for failed patterns
    """
    total_patterns: int
    loaded_successfully: int
    failed_patterns: int
    duration_ms: float
    errors: List[str]

    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        if self.total_patterns == 0:
            return 0.0
        return (self.loaded_successfully / self.total_patterns) * 100

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"LoaderStats(total={self.total_patterns}, "
            f"loaded={self.loaded_successfully}, "
            f"failed={self.failed_patterns}, "
            f"duration={self.duration_ms:.2f}ms, "
            f"success_rate={self.success_rate:.1f}%)"
        )


class OORPLoader:
    """
    Loader for OORP patterns from JSON files.

    This class handles loading patterns from JSON format and adding them
    to a pattern repository. It tracks statistics about the loading process
    and continues loading even if individual patterns fail.

    Attributes:
        repository: Pattern repository to load patterns into
    """

    def __init__(self, repository: IPatternRepository):
        """
        Initialize OORP loader.

        Args:
            repository: Pattern repository to load patterns into
        """
        self.repository = repository
        logger.info("OORPLoader initialized")

    def load_from_file(self, file_path: str) -> LoaderStats:
        """
        Load patterns from a JSON file.

        This method reads patterns from a JSON file and adds them to the
        repository. It continues loading even if individual patterns fail,
        collecting error information for reporting.

        Args:
            file_path: Path to JSON file containing pattern data

        Returns:
            LoaderStats object with loading statistics

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
            ValueError: If the file format is invalid
        """
        start_time = time.perf_counter()

        # Validate file exists
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Pattern file not found: {file_path}")

        logger.info(f"Loading patterns from: {file_path}")

        # Load JSON data
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {e}")
            raise

        # Validate data structure
        if not isinstance(data, list):
            raise ValueError(
                f"Expected JSON array of patterns, got {type(data).__name__}"
            )

        # Load patterns
        total_patterns = len(data)
        loaded_successfully = 0
        failed_patterns = 0
        errors = []

        for i, pattern_dict in enumerate(data, 1):
            try:
                # Create pattern from dictionary
                pattern = Pattern.from_dict(pattern_dict)

                # Add to repository
                self.repository.add_pattern(pattern)
                loaded_successfully += 1

                logger.debug(
                    f"Loaded pattern {i}/{total_patterns}: {pattern.name}"
                )

            except (ValueError, RepositoryError) as e:
                failed_patterns += 1
                pattern_name = pattern_dict.get('name', f'pattern_{i}')
                error_msg = f"Failed to load '{pattern_name}': {str(e)}"
                errors.append(error_msg)

                logger.warning(error_msg)
                # Continue loading other patterns

        # Calculate duration
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000

        # Create statistics
        stats = LoaderStats(
            total_patterns=total_patterns,
            loaded_successfully=loaded_successfully,
            failed_patterns=failed_patterns,
            duration_ms=duration_ms,
            errors=errors
        )

        logger.info(
            f"Loading complete: {loaded_successfully}/{total_patterns} patterns "
            f"loaded in {duration_ms:.2f}ms"
        )

        if errors:
            logger.warning(f"{failed_patterns} patterns failed to load")

        return stats

    def load_from_dict(self, patterns_data: List[Dict[str, Any]]) -> LoaderStats:
        """
        Load patterns from a list of dictionaries.

        This is useful for testing or when pattern data is already loaded
        from another source.

        Args:
            patterns_data: List of pattern dictionaries

        Returns:
            LoaderStats object with loading statistics

        Raises:
            ValueError: If patterns_data is not a list
        """
        start_time = time.perf_counter()

        if not isinstance(patterns_data, list):
            raise ValueError(
                f"Expected list of pattern dicts, got {type(patterns_data).__name__}"
            )

        logger.info(f"Loading {len(patterns_data)} patterns from dictionaries")

        total_patterns = len(patterns_data)
        loaded_successfully = 0
        failed_patterns = 0
        errors = []

        for i, pattern_dict in enumerate(patterns_data, 1):
            try:
                # Create pattern from dictionary
                pattern = Pattern.from_dict(pattern_dict)

                # Add to repository
                self.repository.add_pattern(pattern)
                loaded_successfully += 1

                logger.debug(
                    f"Loaded pattern {i}/{total_patterns}: {pattern.name}"
                )

            except (ValueError, RepositoryError) as e:
                failed_patterns += 1
                pattern_name = pattern_dict.get('name', f'pattern_{i}')
                error_msg = f"Failed to load '{pattern_name}': {str(e)}"
                errors.append(error_msg)

                logger.warning(error_msg)
                # Continue loading other patterns

        # Calculate duration
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000

        # Create statistics
        stats = LoaderStats(
            total_patterns=total_patterns,
            loaded_successfully=loaded_successfully,
            failed_patterns=failed_patterns,
            duration_ms=duration_ms,
            errors=errors
        )

        logger.info(
            f"Loading complete: {loaded_successfully}/{total_patterns} patterns "
            f"loaded in {duration_ms:.2f}ms"
        )

        return stats

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"OORPLoader(repository={self.repository})"
