# PatternSphere CLI Reference

Complete reference for all PatternSphere command-line interface commands.

## Table of Contents

- [Installation](#installation)
- [Commands](#commands)
  - [search](#search)
  - [list](#list)
  - [view](#view)
  - [categories](#categories)
  - [info](#info)
- [Global Options](#global-options)
- [Configuration](#configuration)
- [Examples](#examples)

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Install from Source

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

---

## Commands

### search

Search patterns by keywords with optional filtering.

**Syntax:**
```bash
patternsphere search <query> [OPTIONS]
```

**Arguments:**
- `<query>`: Search keywords (required)

**Options:**
- `--category, -c <name>`: Filter by category
- `--tags, -t <tags>`: Filter by tags (comma-separated)
- `--limit, -l <number>`: Maximum results (default: 20)
- `--scores / --no-scores`: Show/hide relevance scores (default: show)

**Examples:**

Search for refactoring patterns:
```bash
patternsphere search refactoring
```

Search in specific category:
```bash
patternsphere search "code quality" --category "First Contact"
```

Search with tag filter:
```bash
patternsphere search testing --tags "quality,testing"
```

Limit results:
```bash
patternsphere search pattern --limit 10
```

Hide scores:
```bash
patternsphere search code --no-scores
```

**Output Format:**
```
Found 15 pattern(s):

1. Pattern Name (score: 8.5)
   Category: First Contact
   Tags: refactoring, code-reading, analysis
   Intent: Brief description of the pattern intent...
   Matched in: name, intent, tags

2. Another Pattern (score: 7.2)
   ...
```

**Search Algorithm:**

PatternSphere uses weighted field scoring:
- **name**: 5.0 (highest weight)
- **tags**: 4.0
- **intent**: 3.0
- **category**: 2.5
- **problem**: 2.0
- **solution**: 1.5

Match types:
- Exact word match: 1.0 points
- Partial match: 0.5 points

Results are sorted by total score (descending).

---

### list

List all patterns or filter by category.

**Syntax:**
```bash
patternsphere list [OPTIONS]
```

**Options:**
- `--category, -c <name>`: Filter by category
- `--sort, -s <field>`: Sort by field (name, category) (default: name)

**Examples:**

List all patterns:
```bash
patternsphere list
```

List patterns in specific category:
```bash
patternsphere list --category "First Contact"
```

Sort by category:
```bash
patternsphere list --sort category
```

**Output Format:**

Displays a table with columns:
- No.: Sequential number
- Name: Pattern name
- Category: Pattern category
- Tags: First 3 tags (with "..." if more)

```
                    Patterns (61 total)
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ No.┃ Name                     ┃ Category      ┃ Tags            ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1  │ Read all the Code...     │ First Contact │ code-reading... │
│ 2  │ Skim the Documentation   │ First Contact │ documentation...│
...
```

---

### view

Show complete details for a specific pattern.

**Syntax:**
```bash
patternsphere view <pattern-id-or-name>
```

**Arguments:**
- `<pattern-id-or-name>`: Pattern ID (e.g., OORP-001) or name (required)

**Examples:**

View by name:
```bash
patternsphere view "Read all the Code in One Hour"
```

View by ID:
```bash
patternsphere view OORP-001
```

**Output Format:**

Displays complete pattern information:
```
================================================================================
Pattern: Read all the Code in One Hour
================================================================================

METADATA
----------------------------------------
ID: OORP-001
Category: First Contact
Tags: code-reading, analysis, onboarding
Source: OORP

INTENT
----------------------------------------
Quickly understand the overall structure and organization of a large codebase
by systematically reading through all the code in one hour.

PROBLEM
----------------------------------------
When you first encounter a new codebase, it's overwhelming and you don't know
where to start...

SOLUTION
----------------------------------------
Set a timer for one hour and read through the entire codebase systematically...

CONSEQUENCES
----------------------------------------
You gain a high-level understanding of the system architecture and can identify
areas that need deeper investigation...

RELATED PATTERNS
----------------------------------------
  - Skim the Documentation
  - Interview During Demo
  - Refactor to Understand

================================================================================
```

**Tips:**
- Use `list` to find available pattern names
- Pattern names are case-insensitive
- Tab completion works with installed shell completion

---

### categories

List all categories with pattern counts.

**Syntax:**
```bash
patternsphere categories
```

**Options:**
None

**Examples:**

Show all categories:
```bash
patternsphere categories
```

**Output Format:**

Displays a table of categories sorted alphabetically:
```
                Pattern Categories
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Category                     ┃ Patterns ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Detailed Model Capture       │       10 │
│ First Contact                │        6 │
│ Initial Understanding        │        6 │
│ Migration Strategies         │        8 │
│ Redistribute Responsibilities│       10 │
│ Setting Direction            │       10 │
│ Tests: Your Life Insurance!  │        6 │
│ Transform Conditionals...    │        5 │
│ TOTAL                        │       61 │
└──────────────────────────────┴──────────┘
```

**Use Cases:**
- Explore available categories
- Understand pattern distribution
- Choose categories for filtered searches

---

### info

Show system information and statistics.

**Syntax:**
```bash
patternsphere info
```

**Options:**
None

**Examples:**

Display system info:
```bash
patternsphere info
```

**Output Format:**

```
                PatternSphere v1.0.0
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property        ┃ Value                                 ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Application     │ PatternSphere                         │
│ Version         │ 1.0.0                                 │
│ Description     │ A unified knowledge base for soft...  │
│ Total Patterns  │ 61                                    │
│ Categories      │ 8                                     │
│ Load Time       │ 2.35ms                                │
│ Load Success... │ 100.0%                                │
│ Data Source     │ OORP (Object-Oriented Reengineering...)│
└─────────────────┴───────────────────────────────────────┘

Available Categories: Detailed Model Capture, First Contact, Initial Understanding, ...
```

**Information Displayed:**
- Application name and version
- Total pattern count
- Number of categories
- Pattern loading statistics
- Data source information
- Available categories list

---

## Global Options

### --version, -v

Display version and exit.

```bash
patternsphere --version
# Output: PatternSphere v1.0.0
```

### --help

Display help information.

```bash
patternsphere --help                # Main help
patternsphere search --help         # Command-specific help
```

---

## Configuration

### Environment Variables

PatternSphere supports configuration via environment variables:

**PATTERNSPHERE_DATA_DIR**
- Override default data directory
- Default: `data/`

**PATTERNSPHERE_DEFAULT_LIMIT**
- Default result limit for searches
- Default: `20`

**PATTERNSPHERE_TERMINAL_WIDTH**
- Terminal width for formatting
- Default: `80`

**Example:**
```bash
export PATTERNSPHERE_DATA_DIR=/custom/data/path
export PATTERNSPHERE_DEFAULT_LIMIT=50
patternsphere search refactoring
```

### Configuration File

Create a `.env` file in the project root:

```env
PATTERNSPHERE_DATA_DIR=data
PATTERNSPHERE_DEFAULT_LIMIT=20
PATTERNSPHERE_TERMINAL_WIDTH=80
```

---

## Examples

### Common Workflows

**1. Explore Available Patterns**

```bash
# See all categories
patternsphere categories

# List patterns in a category
patternsphere list --category "First Contact"

# View pattern details
patternsphere view "Read all the Code in One Hour"
```

**2. Search for Specific Topics**

```bash
# Find refactoring patterns
patternsphere search refactoring --limit 10

# Find testing patterns
patternsphere search test --tags "testing,quality"

# Find patterns in specific category
patternsphere search analysis --category "Initial Understanding"
```

**3. Pattern Discovery**

```bash
# Browse all patterns
patternsphere list --sort category

# Search broad topics
patternsphere search code quality

# Explore related patterns from view output
patternsphere view "Refactor to Understand"
```

**4. Quick Reference**

```bash
# System info
patternsphere info

# Version check
patternsphere --version

# Help on any command
patternsphere search --help
```

### Advanced Use Cases

**Chaining Commands with Shell**

Find and view top result:
```bash
# Search for a pattern, then view it
patternsphere search "god class" --limit 1
patternsphere view "Split Up God Class"
```

**Filtering and Sorting**

Find all testing patterns:
```bash
patternsphere search test --category "Tests: Your Life Insurance!"
```

Find migration patterns:
```bash
patternsphere list --category "Migration Strategies" --sort name
```

**Quick Pattern Lookup**

```bash
# Direct access by name
patternsphere view "Always Have a Running Version"

# Search and limit
patternsphere search refactor --limit 5 --no-scores
```

---

## Tips and Best Practices

### Search Tips

1. **Use Specific Keywords**: More specific queries yield better results
   ```bash
   # Good
   patternsphere search "split god class"

   # Less specific
   patternsphere search class
   ```

2. **Combine Filters**: Use category and tags together
   ```bash
   patternsphere search test --category "Tests: Your Life Insurance!" --tags "testing"
   ```

3. **Adjust Limits**: Start with low limits for quick overview
   ```bash
   patternsphere search refactor --limit 5
   ```

### Navigation Tips

1. **Start Broad, Then Narrow**:
   - `categories` → `list --category` → `view`
   - `search broad` → `search with filters`

2. **Use Related Patterns**: View output shows related patterns for exploration

3. **Sort by Category**: Groups related patterns together
   ```bash
   patternsphere list --sort category
   ```

### Performance

- First command initializes the app (~1 second)
- Subsequent commands are fast (<100ms)
- Search performance: <10ms average
- All 61 patterns loaded in ~2ms

---

## Troubleshooting

### Pattern Not Found

If `view` can't find a pattern:

1. Use `list` to see exact names
2. Check spelling and capitalization
3. Use partial name in `search` first

```bash
patternsphere list | grep -i "pattern name"
patternsphere search "partial name"
```

### No Results

If search returns no results:

1. Try broader keywords
2. Remove filters
3. Check available categories

```bash
patternsphere categories
patternsphere search keyword --category "CategoryName"
```

### Initialization Errors

If app fails to initialize:

1. Check data files exist
2. Verify installation
3. Check environment variables

```bash
# Verify installation
patternsphere --version

# Check data directory
ls data/sources/oorp/
```

---

## Exit Codes

- `0`: Success
- `1`: Error (pattern not found, initialization failed, etc.)
- `2`: Command line usage error

---

## Further Reading

- [README.md](../README.md) - Quick start guide
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [SPRINT3_COMPLETE.md](../SPRINT3_COMPLETE.md) - Implementation details

---

**Version**: 1.0.0
**Last Updated**: 2025-10-25
**PatternSphere** - A unified knowledge base for software design patterns
