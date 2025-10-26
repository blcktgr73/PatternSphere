"""
Pattern model for PatternSphere.

This module defines the core Pattern model using Pydantic for validation.
Adheres to SOLID principles:
- Single Responsibility: Pattern model only handles pattern data structure
- Open/Closed: Extensible through inheritance and optional fields
- Liskov Substitution: Proper base model design
- Interface Segregation: Focused model with clear purpose
- Dependency Inversion: No dependencies on concrete implementations
"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, ConfigDict


class SourceMetadata(BaseModel):
    """
    Metadata about the source of a pattern.

    Attributes:
        source_name: Name of the pattern source (e.g., "OORP", "GoF")
        authors: List of pattern authors
        publication_year: Year the pattern was published
        url: Optional URL to source material
    """

    model_config = ConfigDict(frozen=False)

    source_name: str = Field(
        ...,
        min_length=1,
        description="Name of the pattern source"
    )
    authors: List[str] = Field(
        default_factory=list,
        description="List of pattern authors"
    )
    publication_year: Optional[int] = Field(
        default=None,
        ge=1950,
        le=2100,
        description="Year the pattern was published"
    )
    url: Optional[str] = Field(
        default=None,
        description="URL to source material"
    )

    @field_validator('authors')
    @classmethod
    def validate_authors(cls, v: List[str]) -> List[str]:
        """Ensure authors list contains valid entries."""
        if not v:
            return v
        if any(not author.strip() for author in v):
            raise ValueError("Author names cannot be empty strings")
        return v


class Pattern(BaseModel):
    """
    Core Pattern model representing a software design pattern.

    This model follows the OORP (Object-Oriented Reengineering Patterns)
    structure and supports comprehensive pattern metadata.

    Attributes:
        id: Unique identifier (UUID) for the pattern
        name: Pattern name (must be unique)
        intent: Brief statement of the pattern's purpose
        problem: Description of the problem the pattern addresses
        context: Situations where the pattern applies
        solution: Description of how the pattern solves the problem
        consequences: Trade-offs and results of applying the pattern
        related_patterns: Names of related patterns
        category: Pattern category for organization
        tags: Tags for filtering and search
        source_metadata: Information about pattern source
        created_at: Timestamp when pattern was created
    """

    model_config = ConfigDict(frozen=False)

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the pattern"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Pattern name"
    )
    intent: str = Field(
        ...,
        min_length=1,
        description="Brief statement of pattern's purpose"
    )
    problem: str = Field(
        ...,
        min_length=1,
        description="Problem the pattern addresses"
    )
    context: str = Field(
        default="",
        description="Situations where the pattern applies"
    )
    solution: str = Field(
        ...,
        min_length=1,
        description="How the pattern solves the problem"
    )
    consequences: str = Field(
        default="",
        description="Trade-offs and results of applying the pattern"
    )
    related_patterns: List[str] = Field(
        default_factory=list,
        description="Names of related patterns"
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Pattern category"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for filtering and search"
    )
    source_metadata: SourceMetadata = Field(
        ...,
        description="Information about pattern source"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when pattern was created"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize pattern name."""
        name = v.strip()
        if not name:
            raise ValueError("Pattern name cannot be empty or whitespace only")
        return name

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Validate and normalize category name."""
        category = v.strip()
        if not category:
            raise ValueError("Category cannot be empty or whitespace only")
        return category

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate and normalize tags."""
        # Remove empty tags and strip whitespace
        cleaned_tags = [tag.strip().lower() for tag in v if tag.strip()]
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in cleaned_tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        return unique_tags

    @field_validator('related_patterns')
    @classmethod
    def validate_related_patterns(cls, v: List[str]) -> List[str]:
        """Validate related patterns list."""
        # Remove empty entries and strip whitespace
        cleaned = [p.strip() for p in v if p.strip()]
        return cleaned

    def matches_search_query(self, query: str) -> bool:
        """
        Check if pattern matches a search query.

        Searches across name, intent, problem, solution, and tags.

        Args:
            query: Search query string (case-insensitive)

        Returns:
            True if pattern matches the query
        """
        query_lower = query.lower()
        searchable_text = " ".join([
            self.name.lower(),
            self.intent.lower(),
            self.problem.lower(),
            self.solution.lower(),
            " ".join(self.tags)
        ])
        return query_lower in searchable_text

    def has_tag(self, tag: str) -> bool:
        """
        Check if pattern has a specific tag.

        Args:
            tag: Tag to check for (case-insensitive)

        Returns:
            True if pattern has the tag
        """
        tag_lower = tag.lower()
        return tag_lower in self.tags

    def to_dict(self) -> dict:
        """
        Convert pattern to dictionary representation.

        Returns:
            Dictionary representation of the pattern (JSON-serializable)
        """
        # Use mode='json' to ensure datetime fields are converted to ISO strings
        return self.model_dump(mode='json')

    @classmethod
    def from_dict(cls, data: dict) -> 'Pattern':
        """
        Create pattern from dictionary.

        Args:
            data: Dictionary containing pattern data

        Returns:
            Pattern instance

        Raises:
            ValidationError: If data is invalid
        """
        return cls.model_validate(data)

    def __str__(self) -> str:
        """String representation of pattern."""
        return f"Pattern(name='{self.name}', category='{self.category}')"

    def __repr__(self) -> str:
        """Developer-friendly representation of pattern."""
        return (
            f"Pattern(id='{self.id}', name='{self.name}', "
            f"category='{self.category}')"
        )
