# PatternSphere File Structure

Last Updated: 2025-10-26

> **Note**: Korean version available: [FILE_STRUCTURE_KR.md](FILE_STRUCTURE_KR.md)

## Project Root

```
PatternSphere/
├── README.md                    # Main project documentation
├── CHANGELOG.md                # Version history
├── setup.py                    # Package installation script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # pytest configuration
├── run_mcp_server.py          # MCP server entry point
└── .gitignore                  # Git ignore patterns
```

## Main Directories

### 📦 patternsphere/ - Main Package

```
patternsphere/
├── __init__.py
├── models/                     # Data models
│   ├── __init__.py
│   └── pattern.py             # Pattern, SourceMetadata
├── repository/                 # Repository layer
│   ├── __init__.py
│   ├── repository_interface.py
│   └── pattern_repository.py
├── storage/                    # Persistence layer
│   ├── __init__.py
│   ├── storage_interface.py
│   └── file_storage.py
├── search/                     # Search engine
│   ├── __init__.py
│   └── search_engine.py
├── loaders/                    # Data loaders
│   ├── __init__.py
│   └── oorp_loader.py
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py
├── cli/                        # CLI interface
│   ├── __init__.py
│   ├── main.py                # CLI entry point
│   ├── commands.py            # 5 CLI commands
│   ├── app_context.py         # Dependency injection context
│   └── formatters/            # Output formatters
│       ├── __init__.py
│       ├── pattern_formatter.py
│       └── search_formatter.py
└── mcp/                        # MCP server implementation
    ├── __init__.py
    └── server.py              # PatternSphereMCPServer
```

### 📚 docs/ - Documentation

```
docs/
├── mcp/                        # MCP server documentation
│   ├── MCP_QUICKSTART.md      # Quick start guide
│   ├── MCP_QUICKSTART_KR.md   # (Korean version)
│   ├── MCP_TEST_GUIDE.md      # Testing guide
│   └── MCP_TEST_GUIDE_KR.md   # (Korean version)
├── development/                # Development documentation
│   ├── CLAUDE.md              # AI pair programming guide (Korean)
│   └── PATTERN_ANALYSIS.md    # Pattern analysis (Korean)
├── FILE_STRUCTURE.md           # This file
├── FILE_STRUCTURE_KR.md        # (Korean version)
├── ORGANIZATION_SUMMARY.md     # Reorganization summary
├── ORGANIZATION_SUMMARY_KR.md  # (Korean version)
├── CLI_Reference.md            # CLI command reference
├── PRD.md                      # Product requirements
└── Phase1_Product_Specification.md  # Phase 1 specification
```

### 🗂️ data/ - Pattern Data

```
data/
└── sources/
    └── oorp/                   # OORP patterns (61 patterns)
        └── oorp_patterns_complete.json
```

### 🧪 tests/ - Test Suite (248 tests)

```
tests/
├── unit/                       # Unit tests (178)
│   ├── test_pattern.py
│   ├── test_repository.py
│   ├── test_search_engine.py
│   ├── test_storage.py
│   ├── test_oorp_loader.py
│   ├── test_cli_commands.py
│   └── test_app_context.py
├── integration/                # Integration tests (55)
│   ├── test_search_flow.py
│   ├── test_cli_integration.py
│   └── test_pattern_loading.py
└── performance/                # Performance tests (15)
    ├── test_search_performance.py
    ├── test_loading_performance.py
    └── test_cli_startup.py
```

### ⚙️ config/ - Configuration Files

```
config/
└── examples/                   # Example configurations
    ├── claude_desktop_config.example.json
    └── claude_desktop_config_with_context7.json
```

### 🔧 scripts/ - Utility Scripts

```
scripts/
├── test_mcp_server.py         # MCP server test script
├── demos/                      # Demo scripts
│   ├── demo_sprint1.py
│   ├── demo_sprint2.py
│   └── demo_sprint3.py
└── utils/                      # Utility scripts
    ├── add_mcp_to_claude.py   # MCP configuration helper
    └── debug_mcp.py            # MCP server debug tool
```

## File Purpose

### Core Files

| File | Purpose |
|------|---------|
| `setup.py` | Package installation and distribution |
| `requirements.txt` | Python dependency list |
| `run_mcp_server.py` | MCP server execution entry point |
| `pytest.ini` | pytest test configuration |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `CHANGELOG.md` | Version change history |
| `docs/FILE_STRUCTURE.md` | This file - file structure explanation |
| `docs/ORGANIZATION_SUMMARY.md` | Project reorganization summary |

### Configuration Files

| File | Purpose |
|------|---------|
| `config/examples/claude_desktop_config.example.json` | Claude Desktop MCP configuration example |
| `.gitignore` | Git version control exclusion patterns |

### Test/Development Files

| File | Purpose |
|------|---------|
| `scripts/test_mcp_server.py` | Comprehensive MCP server testing |
| `scripts/demos/demo_sprint*.py` | Sprint demo scripts |
| `scripts/utils/add_mcp_to_claude.py` | MCP configuration automation |

## Git Ignore Patterns

Items included in `.gitignore`:

- `__pycache__/` - Python cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `venv/`, `env/` - Virtual environments
- `.pytest_cache/` - pytest cache
- `.coverage`, `htmlcov/`, `coverage.json` - Coverage reports
- `dist/`, `build/`, `*.egg-info/` - Build artifacts
- `.vscode/`, `.idea/` - IDE settings
- `.DS_Store`, `Thumbs.db` - OS metadata

## Directory Creation History

**2025-10-26**: Project reorganization
- Created `docs/mcp/` - Separated MCP documentation
- Created `docs/development/` - Separated development guides
- Created `config/examples/` - Separated configuration examples
- Created `scripts/` - Separated utility scripts
  - `scripts/demos/` - Demo scripts
  - `scripts/utils/` - Utility tools

## File Movement Log

### 2025-10-26 Reorganization

**Documentation files moved:**
- `CLAUDE.md` → `docs/development/CLAUDE.md`
- `PATTERN_ANALYSIS.md` → `docs/development/PATTERN_ANALYSIS.md`
- `MCP_QUICKSTART.md` → `docs/mcp/MCP_QUICKSTART.md`
- `MCP_TEST_GUIDE.md` → `docs/mcp/MCP_TEST_GUIDE.md`

**Configuration files moved:**
- `claude_desktop_config.example.json` → `config/examples/`
- `claude_desktop_config_with_context7.json` → `config/examples/`

**Script files moved:**
- `test_mcp_server.py` → `scripts/test_mcp_server.py`
- `demo_sprint1.py` → `scripts/demos/demo_sprint1.py`
- `demo_sprint2.py` → `scripts/demos/demo_sprint2.py`
- `demo_sprint3.py` → `scripts/demos/demo_sprint3.py`
- `add_mcp_to_claude.py` → `scripts/utils/add_mcp_to_claude.py`
- `debug_mcp.py` → `scripts/utils/debug_mcp.py`

**Files removed:**
- `coverage.json` - Added to `.gitignore`

## Notes

### Path Reference Updates

After file movement, the following references were updated:

1. **scripts/test_mcp_server.py**:
   - `run_mcp_server.py` path: `Path(__file__).parent.parent / "run_mcp_server.py"`
   - Config file path: `Path(__file__).parent.parent / "config" / "examples" / ...`

2. **README.md**:
   - MCP documentation links: `docs/mcp/MCP_QUICKSTART.md`
   - Development documentation links: `docs/development/CLAUDE.md`
   - Demo script references: `scripts/demos/`

3. **docs/mcp/MCP_QUICKSTART.md**:
   - Relative paths updated: `../../README.md`, `../CLI_Reference.md`

### Build and Deployment

To build/deploy the project, from the root directory:

```bash
python setup.py sdist bdist_wheel
```

### Running Tests

Run all tests:

```bash
pytest
```

Specific categories:

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

### Running MCP Server

From root directory:

```bash
python run_mcp_server.py
```

Or for testing:

```bash
python scripts/test_mcp_server.py
```

## Documentation Languages

- **English**: Primary documentation language for broader accessibility
- **Korean (_KR.md)**: Korean versions provided for key documents:
  - `FILE_STRUCTURE_KR.md` - This file in Korean
  - `ORGANIZATION_SUMMARY_KR.md` - Reorganization summary in Korean
  - `MCP_QUICKSTART_KR.md` - MCP quick start in Korean
  - `MCP_TEST_GUIDE_KR.md` - MCP test guide in Korean

---

**See Also**:
- [README.md](../README.md) - Main project documentation
- [ORGANIZATION_SUMMARY.md](ORGANIZATION_SUMMARY.md) - Reorganization details
- [CLI_Reference.md](CLI_Reference.md) - CLI command reference
