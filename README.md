# PatternSphere

> A unified knowledge base for software design patterns

**Version 1.0.0** - Production Ready

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-248%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)]()

## Overview

PatternSphere is a powerful command-line tool for searching, browsing, and exploring software design patterns. Phase 1 focuses on **Object-Oriented Reengineering Patterns (OORP)** with 61 comprehensive patterns across 8 categories.

### Key Features

- **Fast Keyword Search**: Weighted field scoring for relevant results (<10ms)
- **Category Browsing**: Explore patterns by 8 OORP categories
- **Tag Filtering**: Filter by multiple tags with OR logic
- **Rich Terminal UI**: Beautiful tables and formatted output
- **Pattern Details**: Complete pattern information (problem, solution, consequences)
- **Related Patterns**: Discover connections between patterns
- **61 OORP Patterns**: Complete coverage of Object-Oriented Reengineering Patterns
- **MCP Integration**: Use as MCP server in Claude Code for AI-assisted pattern discovery

## Quick Start

### Installation

```bash
# Clone or extract the repository
cd PatternSphere

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Verify Installation

```bash
patternsphere --version
# Output: PatternSphere v1.0.0
```

### First Commands

```bash
# Get system information
patternsphere info

# List all categories
patternsphere categories

# Search for patterns
patternsphere search refactoring

# View pattern details
patternsphere view "Read all the Code in One Hour"

# List patterns in a category
patternsphere list --category "First Contact"
```

### MCP Integration (Claude Code)

PatternSphere can be used as an MCP (Model Context Protocol) server in Claude Code:

```bash
# 1. Complete the installation above
# 2. Configure Claude Code
# 3. Use in Claude Code:
#    "Find patterns for refactoring legacy code"
#    "Show me the 'Read all the Code in One Hour' pattern"
```

**📖 See [MCP Quick Start](docs/mcp/MCP_QUICKSTART.md) for setup instructions.**

## Usage

### Search Patterns

Search across all pattern fields with weighted scoring:

```bash
# Simple search
patternsphere search refactoring

# Search with category filter
patternsphere search "code quality" --category "First Contact"

# Search with tag filter
patternsphere search testing --tags "quality,testing"

# Limit results
patternsphere search pattern --limit 10

# Hide relevance scores
patternsphere search code --no-scores
```

**Search Algorithm:**
- Weighted field scoring (name: 5.0, tags: 4.0, intent: 3.0, etc.)
- Exact word match: 1.0 points, partial match: 0.5 points
- Results sorted by relevance

### List Patterns

Browse all patterns with filtering and sorting:

```bash
# List all patterns
patternsphere list

# List by category
patternsphere list --category "First Contact"

# Sort by category
patternsphere list --sort category
```

### View Pattern Details

Display complete pattern information:

```bash
# View by name
patternsphere view "Read all the Code in One Hour"

# View by ID
patternsphere view OORP-001
```

Shows:
- Metadata (ID, category, tags, source)
- Intent
- Problem
- Solution
- Consequences
- Related patterns

### Browse Categories

Explore available categories:

```bash
patternsphere categories
```

Shows all 8 OORP categories with pattern counts:
- Detailed Model Capture (10 patterns)
- First Contact (6 patterns)
- Initial Understanding (6 patterns)
- Migration Strategies (8 patterns)
- Redistribute Responsibilities (10 patterns)
- Setting Direction (10 patterns)
- Tests: Your Life Insurance! (6 patterns)
- Transform Conditionals to Polymorphism (5 patterns)

### System Information

Display application info and statistics:

```bash
patternsphere info
```

Shows:
- Version information
- Total patterns and categories
- Loading performance
- Data source information

## Pattern Categories

### 1. First Contact (6 patterns)

Initial exploration of an unfamiliar codebase.

**Key Patterns:**
- Read all the Code in One Hour
- Skim the Documentation
- Interview During Demo
- Do a Mock Installation
- Chat with the Maintainers
- Read all the Code in One Hour

**Use When:**
- Starting work on a new project
- Onboarding to a legacy system
- Performing initial assessment

### 2. Initial Understanding (6 patterns)

Building deeper understanding of system structure.

**Key Patterns:**
- Analyze the Persistent Data
- Study the Exceptional Entities
- Refactor to Understand
- Speculate about Business Rules
- Look for the Contracts
- Record Business Rules as Tests

**Use When:**
- Need to understand data models
- Investigating system architecture
- Planning refactoring efforts

### 3. Detailed Model Capture (10 patterns)

Capturing detailed models of the system.

**Key Patterns:**
- Learn from the Past
- Visualize Code as Dotplots
- Speculate about Design
- Interview During Demo
- Read all the Code in One Hour

**Use When:**
- Creating documentation
- Reverse engineering architecture
- Planning major changes

### 4. Redistribute Responsibilities (10 patterns)

Improving class and module design.

**Key Patterns:**
- Split Up God Class
- Move Behavior Close to Data
- Extract Method Object
- Eliminate Navigation Code
- Encapsulate Field

**Use When:**
- Refactoring large classes
- Improving cohesion
- Reducing coupling

### 5. Transform Conditionals to Polymorphism (5 patterns)

Replacing conditionals with polymorphic designs.

**Key Patterns:**
- Replace Conditional with Polymorphism
- Introduce Null Object
- Factor out State
- Factor out Strategy

**Use When:**
- Simplifying complex conditionals
- Implementing Strategy pattern
- Improving extensibility

### 6. Migration Strategies (8 patterns)

Strategies for migrating legacy systems.

**Key Patterns:**
- Always Have a Running Version
- Migrate Systems Incrementally
- Present the Right Interface
- Distinguish Public from Published Interface
- Deprecate Obsolete Interfaces

**Use When:**
- Planning system migrations
- Modernizing legacy code
- Managing technical debt

### 7. Setting Direction (10 patterns)

Strategic patterns for reengineering projects.

**Key Patterns:**
- Appoint a Navigator
- Build Confidence
- Most Valuable First
- Repair What's Broken First
- If It Ain't Broke, Don't Fix It

**Use When:**
- Starting reengineering projects
- Managing stakeholders
- Planning priorities

### 8. Tests: Your Life Insurance! (6 patterns)

Testing strategies for legacy systems.

**Key Patterns:**
- Write Tests to Enable Evolution
- Write Tests to Understand
- Test Fuzzy Features
- Retest Persistent Problems
- Test the Interface, Not the Implementation

**Use When:**
- Working with untested code
- Adding test coverage
- Enabling safe refactoring

## Common Workflows

### 1. Exploring a New Codebase

```bash
# Start with First Contact patterns
patternsphere list --category "First Contact"

# View key patterns
patternsphere view "Read all the Code in One Hour"
patternsphere view "Interview During Demo"

# Search for specific techniques
patternsphere search documentation --category "First Contact"
```

### 2. Planning Refactoring

```bash
# Find refactoring patterns
patternsphere search refactoring --limit 15

# Explore responsibility redistribution
patternsphere list --category "Redistribute Responsibilities"

# View specific refactoring patterns
patternsphere view "Split Up God Class"
patternsphere view "Move Behavior Close to Data"
```

### 3. Adding Tests to Legacy Code

```bash
# Find testing patterns
patternsphere search test --tags "testing,quality"

# View testing category
patternsphere list --category "Tests: Your Life Insurance!"

# Learn specific techniques
patternsphere view "Write Tests to Enable Evolution"
patternsphere view "Test Fuzzy Features"
```

### 4. Pattern Discovery

```bash
# Browse by category
patternsphere categories

# List all patterns sorted by category
patternsphere list --sort category

# Search broad topics
patternsphere search "code quality"

# Explore related patterns (shown in view output)
```

## Architecture

### Component Overview

```
PatternSphere
├── Models (Pattern data model with Pydantic validation)
├── Repository (Pattern storage with O(1) lookups)
├── Search Engine (Weighted keyword search)
├── Loaders (OORP pattern loader)
├── Storage (File-based persistence with atomic writes)
├── CLI (Command-line interface)
│   ├── Commands (5 main commands)
│   ├── Formatters (Output formatting)
│   └── AppContext (Dependency injection)
└── Config (Settings and configuration)
```

### Design Principles

PatternSphere is built following **SOLID principles** and clean architecture:

**Single Responsibility**
- Each component has one clear purpose
- Pattern model: Data structure and validation only
- Repository: Collection management and queries
- Storage: File I/O operations only
- Formatters only format, search only searches

**Open/Closed**
- Extensible for new pattern sources (PDF, web, etc.)
- New commands easily added via decorators
- IStorage interface allows new storage backends
- IPatternRepository allows alternative implementations

**Liskov Substitution**
- Repository interface enables multiple implementations
- Any IStorage implementation can be used interchangeably
- Future storage backends possible (SQLite, PostgreSQL)

**Interface Segregation**
- Focused interfaces (IPatternRepository, IStorage)
- No bloated interfaces
- IStorage has minimal, focused interface

**Dependency Inversion**
- Components depend on abstractions
- AppContext manages all dependencies
- Repository depends on IStorage abstraction
- Enables testing with mock storage

### Key Design Patterns

**Repository Pattern**
- Abstracts pattern data access
- `IPatternRepository` interface
- `InMemoryPatternRepository` implementation
- Collection-like interface with multiple indexes

**Singleton Pattern**
- `AppContext` manages application state
- Single instance across CLI session

**Strategy Pattern**
- Weighted search scoring algorithm
- Extensible for new scoring strategies

**Dependency Injection**
- Components receive dependencies via constructors
- Testable and maintainable
- No global state

## Performance

PatternSphere is optimized for speed:

| Operation | Performance | Requirement | Result |
|-----------|-------------|-------------|--------|
| Pattern Loading | ~2ms | <500ms | 250x faster ✅ |
| Search (average) | <10ms | <100ms | 10x faster ✅ |
| CLI Startup | ~650ms | <1s | 35% faster ✅ |
| Memory Usage | <100KB | Minimal | Excellent ✅ |

**All requirements exceeded by 10-250x!**

## Testing

Comprehensive test suite ensures reliability:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=patternsphere --cov-report=html

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

**Test Statistics:**
- **Total Tests**: 248
- **Test Coverage**: 91%
- **All Tests**: Passing ✅
- **Execution Time**: ~1.6 seconds

**Test Categories:**
- Unit tests (178) - models, repository, storage, search, loaders, CLI
- Integration tests (55) - search flow, CLI commands, end-to-end workflows
- Performance tests (15) - loading, search, scalability

**Coverage Breakdown:**
- Pattern models: 100%
- Repository: 97%
- Search engine: 97%
- Loaders: 92%
- CLI components: 86-100%
- Overall: 91%

## Configuration

### Environment Variables

Configure PatternSphere via environment variables:

```bash
export PATTERNSPHERE_DATA_DIR=/custom/data/path
export PATTERNSPHERE_DEFAULT_LIMIT=50
export PATTERNSPHERE_TERMINAL_WIDTH=100
```

**Available Variables:**
- `PATTERNSPHERE_DATA_DIR`: Data directory path
- `PATTERNSPHERE_DEFAULT_LIMIT`: Default search result limit
- `PATTERNSPHERE_TERMINAL_WIDTH`: Terminal width for formatting

### Configuration File

Create `.env` file in project root:

```env
PATTERNSPHERE_DATA_DIR=data
PATTERNSPHERE_DEFAULT_LIMIT=20
PATTERNSPHERE_TERMINAL_WIDTH=80
```

## Project Structure

```
PatternSphere/
├── patternsphere/          # Main package
│   ├── models/            # Pattern data models (Pydantic)
│   ├── repository/        # Repository pattern implementation
│   ├── storage/           # File storage
│   ├── search/            # Search engine
│   ├── loaders/           # Pattern loaders
│   ├── config/            # Configuration
│   ├── cli/               # CLI interface
│   └── mcp/               # MCP server implementation
├── data/                  # Pattern data
│   └── sources/oorp/      # OORP patterns (61 patterns)
├── tests/                 # Test suite (248 tests)
│   ├── unit/             # Unit tests (178)
│   ├── integration/      # Integration tests (55)
│   └── performance/      # Performance tests (15)
├── docs/                  # Documentation
│   ├── mcp/              # MCP server documentation
│   │   ├── MCP_QUICKSTART.md
│   │   └── MCP_TEST_GUIDE.md
│   ├── development/      # Development guides
│   │   ├── CLAUDE.md
│   │   └── PATTERN_ANALYSIS.md
│   ├── CLI_Reference.md
│   ├── PRD.md
│   └── Phase1_Product_Specification.md
├── config/                # Configuration files
│   └── examples/         # Example configurations
├── scripts/               # Utility scripts
│   ├── test_mcp_server.py
│   ├── demos/            # Demo scripts
│   └── utils/            # Utility scripts
├── README.md             # This file
├── CHANGELOG.md          # Version history
├── requirements.txt      # Dependencies
├── setup.py              # Package setup
└── run_mcp_server.py     # MCP server entry point
```

## Documentation

### User Documentation
- **[CLI Reference](docs/CLI_Reference.md)**: Complete command reference with examples
- **[MCP Quick Start](docs/mcp/MCP_QUICKSTART.md)**: MCP server setup and usage ([한글](docs/mcp/MCP_QUICKSTART_KR.md))
- **[MCP Test Guide](docs/mcp/MCP_TEST_GUIDE.md)**: MCP server testing and troubleshooting ([한글](docs/mcp/MCP_TEST_GUIDE_KR.md))
- **[File Structure](docs/FILE_STRUCTURE.md)**: Project organization and file reference ([한글](docs/FILE_STRUCTURE_KR.md))

### Development Documentation
- **[Development Guide](docs/development/CLAUDE_EN.md)**: AI pair programming and transformation patterns ([한글](CLAUDE.md))
- **[Pattern Analysis](docs/development/PATTERN_ANALYSIS.md)**: Project pattern analysis and recommendations ([한글](docs/development/PATTERN_ANALYSIS_KR.md))
- **[Organization Summary](docs/ORGANIZATION_SUMMARY.md)**: Project reorganization details ([한글](docs/ORGANIZATION_SUMMARY_KR.md))
- **[CHANGELOG](CHANGELOG.md)**: Version history and changes
- **[PRD](docs/PRD.md)**: Product requirements (includes Phase 2 PDF support)
- **[Product Spec](docs/Phase1_Product_Specification.md)**: Phase 1 specification
- **Sprint Reports**: SPRINT1_COMPLETE.md, SPRINT2_COMPLETE.md, SPRINT3_COMPLETE.md

## Development

### Setup Development Environment

```bash
# Clone repository
cd PatternSphere

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black patternsphere/

# Type checking
mypy patternsphere/

# Linting
flake8 patternsphere/
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=patternsphere

# Specific test file
pytest tests/unit/test_search_engine.py

# Performance tests
pytest tests/performance/ -v

# Integration tests
pytest tests/integration/ -v
```

### Project Statistics

| Metric | Value |
|--------|-------|
| Total Source Lines | 2,638 |
| Total Test Lines | 4,037 |
| Test/Code Ratio | 1.53:1 |
| Total Patterns | 61 |
| Categories | 8 |
| Commands | 5 |
| Test Coverage | 91% |

## Requirements

**Runtime:**
- **Python**: 3.9 or higher
- **Dependencies**:
  - pydantic >= 2.0.0 (Data validation)
  - pydantic-settings >= 2.0.0 (Configuration)
  - pyyaml >= 6.0 (YAML support)
  - typer >= 0.9.0 (CLI framework)
  - rich >= 13.0.0 (Terminal formatting)

**Development:**
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- mypy >= 1.5.0
- flake8 >= 6.1.0

## Roadmap

### Phase 1 (Complete) ✅
- OORP pattern loading
- Keyword search with weighted scoring
- CLI interface with 5 commands
- 61 OORP patterns with comprehensive tags
- File-based storage with atomic writes
- 248 comprehensive tests
- Complete documentation

### Phase 2 (Future - Planned in PRD)
- **PDF Integration**:
  - PDF pattern extraction
  - Gang of Four (GoF) patterns
  - Enterprise Integration Patterns
  - Pattern-Oriented Software Architecture (POSA)
  - Manual pattern definition workflow
  - PDF page linking

- **Multi-Source Architecture**:
  - Knowledge source abstraction layer
  - Source plugin architecture
  - Conflict resolution
  - Multiple sources simultaneously

### Phase 3 (Future)
- Semantic search using embeddings
- Pattern relationship visualization
- Web interface
- Pattern recommendations based on code analysis
- Code example integration

### Phase 4 (Future)
- User-contributed patterns
- Pattern comparison tool
- Export to various formats
- IDE plugins
- Collaborative pattern curation

## Contributing

PatternSphere is designed for extensibility:

**Adding New Pattern Sources:**
1. Create loader in `patternsphere/loaders/`
2. Implement loader following `OORPLoader` structure
3. Add patterns to `data/sources/<source-name>/`
4. Register source in configuration

**Adding New Commands:**
1. Add command function in `patternsphere/cli/commands.py`
2. Use `@app.command()` decorator
3. Follow existing command patterns
4. Add tests in `tests/integration/test_cli.py`

**Adding Tests:**
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Performance tests: `tests/performance/`
- Follow existing test structure

## License

MIT License - See LICENSE file for details

## Acknowledgments

**Pattern Sources:**
- **OORP**: Object-Oriented Reengineering Patterns by Serge Demeyer, Stéphane Ducasse, and Oscar Nierstrasz (2003)

**Technologies:**
- [Typer](https://typer.tiangolo.com/) - Modern CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal UI
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [pytest](https://pytest.org/) - Testing framework

## Support

**Getting Help:**
```bash
# Main help
patternsphere --help

# Command help
patternsphere search --help

# System info
patternsphere info
```

**Documentation:**
- Check [CLI Reference](docs/CLI_Reference.md) for detailed command help
- Review test examples in `tests/` directory
- See demo scripts in `scripts/demos/`: demo_sprint1.py, demo_sprint2.py, demo_sprint3.py

---

**PatternSphere v1.0.0**
*A unified knowledge base for software design patterns*

Built with ❤️ following SOLID principles and clean architecture.
