"""
Unit tests for Pattern models.

Tests cover:
- Model validation
- Field constraints
- Custom validators
- Model methods
- Edge cases and error conditions
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from patternsphere.models.pattern import Pattern, SourceMetadata


class TestSourceMetadata:
    """Test cases for SourceMetadata model."""

    def test_create_source_metadata_minimal(self):
        """Test creating SourceMetadata with only required fields."""
        metadata = SourceMetadata(source_name="OORP")
        assert metadata.source_name == "OORP"
        assert metadata.authors == []
        assert metadata.publication_year is None
        assert metadata.url is None

    def test_create_source_metadata_complete(self):
        """Test creating SourceMetadata with all fields."""
        metadata = SourceMetadata(
            source_name="OORP",
            authors=["Serge Demeyer", "Stéphane Ducasse", "Oscar Nierstrasz"],
            publication_year=2002,
            url="https://example.com/oorp"
        )
        assert metadata.source_name == "OORP"
        assert len(metadata.authors) == 3
        assert metadata.publication_year == 2002
        assert metadata.url == "https://example.com/oorp"

    def test_source_name_required(self):
        """Test that source_name is required."""
        with pytest.raises(ValidationError) as exc_info:
            SourceMetadata()
        assert "source_name" in str(exc_info.value)

    def test_source_name_not_empty(self):
        """Test that source_name cannot be empty."""
        with pytest.raises(ValidationError) as exc_info:
            SourceMetadata(source_name="")
        assert "source_name" in str(exc_info.value)

    def test_publication_year_validation(self):
        """Test publication year range validation."""
        # Valid year
        metadata = SourceMetadata(source_name="Test", publication_year=2000)
        assert metadata.publication_year == 2000

        # Too old
        with pytest.raises(ValidationError):
            SourceMetadata(source_name="Test", publication_year=1900)

        # Too new
        with pytest.raises(ValidationError):
            SourceMetadata(source_name="Test", publication_year=2150)

    def test_authors_validation(self):
        """Test authors list validation."""
        # Valid authors
        metadata = SourceMetadata(
            source_name="Test",
            authors=["Author One", "Author Two"]
        )
        assert len(metadata.authors) == 2

        # Empty string in authors should raise error
        with pytest.raises(ValidationError) as exc_info:
            SourceMetadata(source_name="Test", authors=["Valid Author", ""])
        assert "empty strings" in str(exc_info.value).lower()


class TestPattern:
    """Test cases for Pattern model."""

    @pytest.fixture
    def valid_source_metadata(self):
        """Fixture providing valid source metadata."""
        return SourceMetadata(
            source_name="OORP",
            authors=["Serge Demeyer"],
            publication_year=2002
        )

    @pytest.fixture
    def minimal_pattern_data(self, valid_source_metadata):
        """Fixture providing minimal valid pattern data."""
        return {
            "name": "Test Pattern",
            "intent": "To test the pattern model",
            "problem": "We need to validate the pattern works",
            "solution": "Create comprehensive tests",
            "category": "Testing",
            "source_metadata": valid_source_metadata
        }

    def test_create_pattern_minimal(self, minimal_pattern_data):
        """Test creating a pattern with only required fields."""
        pattern = Pattern(**minimal_pattern_data)

        assert pattern.name == "Test Pattern"
        assert pattern.intent == "To test the pattern model"
        assert pattern.problem == "We need to validate the pattern works"
        assert pattern.solution == "Create comprehensive tests"
        assert pattern.category == "Testing"
        assert pattern.context == ""
        assert pattern.consequences == ""
        assert pattern.related_patterns == []
        assert pattern.tags == []
        assert isinstance(pattern.id, str)
        assert len(pattern.id) > 0
        assert isinstance(pattern.created_at, datetime)

    def test_create_pattern_complete(self, valid_source_metadata):
        """Test creating a pattern with all fields."""
        pattern = Pattern(
            name="Complete Pattern",
            intent="Test all fields",
            problem="Need complete testing",
            context="When testing thoroughly",
            solution="Use all fields",
            consequences="Better test coverage",
            related_patterns=["Pattern A", "Pattern B"],
            category="Testing",
            tags=["test", "validation", "complete"],
            source_metadata=valid_source_metadata
        )

        assert pattern.name == "Complete Pattern"
        assert pattern.context == "When testing thoroughly"
        assert pattern.consequences == "Better test coverage"
        assert len(pattern.related_patterns) == 2
        assert len(pattern.tags) == 3

    def test_pattern_id_auto_generation(self, minimal_pattern_data):
        """Test that pattern IDs are auto-generated and unique."""
        pattern1 = Pattern(**minimal_pattern_data)
        pattern2 = Pattern(**minimal_pattern_data)

        assert pattern1.id != pattern2.id
        assert len(pattern1.id) == 36  # UUID format

    def test_name_required(self, minimal_pattern_data):
        """Test that name field is required."""
        del minimal_pattern_data["name"]
        with pytest.raises(ValidationError) as exc_info:
            Pattern(**minimal_pattern_data)
        assert "name" in str(exc_info.value)

    def test_name_not_empty(self, minimal_pattern_data):
        """Test that name cannot be empty or whitespace only."""
        minimal_pattern_data["name"] = ""
        with pytest.raises(ValidationError):
            Pattern(**minimal_pattern_data)

        minimal_pattern_data["name"] = "   "
        with pytest.raises(ValidationError):
            Pattern(**minimal_pattern_data)

    def test_name_validation_strips_whitespace(self, minimal_pattern_data):
        """Test that name is stripped of leading/trailing whitespace."""
        minimal_pattern_data["name"] = "  Test Pattern  "
        pattern = Pattern(**minimal_pattern_data)
        assert pattern.name == "Test Pattern"

    def test_name_length_limit(self, minimal_pattern_data):
        """Test that name has a maximum length."""
        minimal_pattern_data["name"] = "A" * 201
        with pytest.raises(ValidationError):
            Pattern(**minimal_pattern_data)

    def test_intent_required(self, minimal_pattern_data):
        """Test that intent field is required."""
        del minimal_pattern_data["intent"]
        with pytest.raises(ValidationError) as exc_info:
            Pattern(**minimal_pattern_data)
        assert "intent" in str(exc_info.value)

    def test_problem_required(self, minimal_pattern_data):
        """Test that problem field is required."""
        del minimal_pattern_data["problem"]
        with pytest.raises(ValidationError) as exc_info:
            Pattern(**minimal_pattern_data)
        assert "problem" in str(exc_info.value)

    def test_solution_required(self, minimal_pattern_data):
        """Test that solution field is required."""
        del minimal_pattern_data["solution"]
        with pytest.raises(ValidationError) as exc_info:
            Pattern(**minimal_pattern_data)
        assert "solution" in str(exc_info.value)

    def test_category_required(self, minimal_pattern_data):
        """Test that category field is required."""
        del minimal_pattern_data["category"]
        with pytest.raises(ValidationError) as exc_info:
            Pattern(**minimal_pattern_data)
        assert "category" in str(exc_info.value)

    def test_category_validation(self, minimal_pattern_data):
        """Test category validation."""
        # Empty category should fail
        minimal_pattern_data["category"] = ""
        with pytest.raises(ValidationError):
            Pattern(**minimal_pattern_data)

        # Whitespace only should fail
        minimal_pattern_data["category"] = "   "
        with pytest.raises(ValidationError):
            Pattern(**minimal_pattern_data)

        # Valid category with whitespace should be stripped
        minimal_pattern_data["category"] = "  Testing  "
        pattern = Pattern(**minimal_pattern_data)
        assert pattern.category == "Testing"

    def test_tags_normalization(self, minimal_pattern_data):
        """Test that tags are normalized (lowercased, stripped, deduplicated)."""
        minimal_pattern_data["tags"] = [
            "Test",
            "VALIDATION",
            "  cleanup  ",
            "test",  # duplicate
            "",  # empty
            "Validation"  # duplicate with different case
        ]
        pattern = Pattern(**minimal_pattern_data)

        assert len(pattern.tags) == 3  # duplicates and empty removed
        assert "test" in pattern.tags
        assert "validation" in pattern.tags
        assert "cleanup" in pattern.tags

    def test_related_patterns_cleanup(self, minimal_pattern_data):
        """Test that related patterns are cleaned up."""
        minimal_pattern_data["related_patterns"] = [
            "Pattern A",
            "  Pattern B  ",
            "",  # should be removed
            "Pattern C"
        ]
        pattern = Pattern(**minimal_pattern_data)

        assert len(pattern.related_patterns) == 3
        assert "" not in pattern.related_patterns
        assert "Pattern B" in pattern.related_patterns

    def test_matches_search_query(self, minimal_pattern_data):
        """Test search query matching."""
        minimal_pattern_data["tags"] = ["refactoring", "testing"]
        pattern = Pattern(**minimal_pattern_data)

        # Should match on name
        assert pattern.matches_search_query("Test")
        assert pattern.matches_search_query("test")  # case insensitive

        # Should match on intent
        assert pattern.matches_search_query("pattern model")

        # Should match on problem
        assert pattern.matches_search_query("validate")

        # Should match on solution
        assert pattern.matches_search_query("comprehensive")

        # Should match on tags
        assert pattern.matches_search_query("refactoring")

        # Should not match
        assert not pattern.matches_search_query("nonexistent")

    def test_has_tag(self, minimal_pattern_data):
        """Test tag checking."""
        minimal_pattern_data["tags"] = ["refactoring", "testing"]
        pattern = Pattern(**minimal_pattern_data)

        assert pattern.has_tag("refactoring")
        assert pattern.has_tag("REFACTORING")  # case insensitive
        assert pattern.has_tag("testing")
        assert not pattern.has_tag("nonexistent")

    def test_to_dict(self, minimal_pattern_data):
        """Test conversion to dictionary."""
        pattern = Pattern(**minimal_pattern_data)
        data = pattern.to_dict()

        assert isinstance(data, dict)
        assert data["name"] == "Test Pattern"
        assert data["intent"] == "To test the pattern model"
        assert "id" in data
        assert "created_at" in data

    def test_from_dict(self, minimal_pattern_data):
        """Test creation from dictionary."""
        # First create a pattern and convert to dict
        pattern1 = Pattern(**minimal_pattern_data)
        data = pattern1.to_dict()

        # Create new pattern from dict
        pattern2 = Pattern.from_dict(data)

        assert pattern2.id == pattern1.id
        assert pattern2.name == pattern1.name
        assert pattern2.intent == pattern1.intent

    def test_from_dict_with_invalid_data(self):
        """Test that from_dict raises error with invalid data."""
        invalid_data = {
            "name": "Test",
            # missing required fields
        }

        with pytest.raises(ValidationError):
            Pattern.from_dict(invalid_data)

    def test_string_representation(self, minimal_pattern_data):
        """Test __str__ method."""
        pattern = Pattern(**minimal_pattern_data)
        str_repr = str(pattern)

        assert "Test Pattern" in str_repr
        assert "Testing" in str_repr

    def test_repr_representation(self, minimal_pattern_data):
        """Test __repr__ method."""
        pattern = Pattern(**minimal_pattern_data)
        repr_str = repr(pattern)

        assert "Pattern(" in repr_str
        assert pattern.id in repr_str
        assert "Test Pattern" in repr_str
        assert "Testing" in repr_str

    def test_pattern_immutability_not_enforced(self, minimal_pattern_data):
        """Test that pattern fields can be modified (not frozen)."""
        pattern = Pattern(**minimal_pattern_data)
        original_name = pattern.name

        # Should be able to modify
        pattern.name = "Modified Name"
        assert pattern.name == "Modified Name"
        assert pattern.name != original_name

    def test_source_metadata_integration(self):
        """Test that source metadata is properly integrated."""
        metadata = SourceMetadata(
            source_name="OORP",
            authors=["Author One"],
            publication_year=2002
        )

        pattern = Pattern(
            name="Test",
            intent="Test",
            problem="Test",
            solution="Test",
            category="Test",
            source_metadata=metadata
        )

        assert pattern.source_metadata.source_name == "OORP"
        assert pattern.source_metadata.publication_year == 2002
        assert len(pattern.source_metadata.authors) == 1
