# Claude Desktop Setup Guide

Connect PatternSphere MCP server to Claude Desktop to search and explore design patterns using natural language.

## Quick Setup (5 minutes)

### Step 1: Install PatternSphere

```bash
# Navigate to project directory
cd c:\Projects\PatternSphere

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Verify installation
patternsphere info
```

Expected output:
```
PatternSphere v1.0.0
Total patterns: 61
Categories: 8
Sources: OORP
```

### Step 2: Configure Claude Desktop

#### Windows

1. **Locate configuration file:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   Full path example: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`

2. **Edit the file** (create if it doesn't exist):

   ```json
   {
     "mcpServers": {
       "patternsphere": {
         "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
         "args": [
           "c:\\Projects\\PatternSphere\\run_mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "c:\\Projects\\PatternSphere",
           "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data"
         }
       }
     }
   }
   ```

   **⚠️ Important:**
   - Replace `c:\\Projects\\PatternSphere` with your actual project path
   - Use double backslashes (`\\`) in Windows paths
   - Ensure `python.exe` path points to your virtual environment

#### macOS

1. **Locate configuration file:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Edit the file:**

   ```json
   {
     "mcpServers": {
       "patternsphere": {
         "command": "/Users/yourname/Projects/PatternSphere/venv/bin/python",
         "args": [
           "/Users/yourname/Projects/PatternSphere/run_mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/Users/yourname/Projects/PatternSphere",
           "PATTERNSPHERE_DATA_DIR": "/Users/yourname/Projects/PatternSphere/data"
         }
       }
     }
   }
   ```

   **⚠️ Important:**
   - Replace `/Users/yourname/Projects/PatternSphere` with your actual project path
   - Use forward slashes (`/`) in macOS/Linux paths

#### Linux

1. **Locate configuration file:**
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Edit the file:** (same format as macOS above)

### Step 3: Restart Claude Desktop

1. **Completely quit** Claude Desktop (not just close the window)
2. **Restart** Claude Desktop
3. Wait a few seconds for MCP servers to initialize

### Step 4: Verify Connection

Start a new conversation in Claude Desktop and ask:

```
Can you list available MCP tools?
```

You should see 5 PatternSphere tools:
- `search_patterns` - Search patterns by keywords
- `get_pattern` - Get detailed pattern information
- `list_categories` - List all pattern categories
- `list_patterns` - List patterns (optionally filtered by category)
- `get_pattern_recommendations` - Get pattern recommendations based on problem description

## Usage Examples

### Example 1: Search for Patterns

**You:**
> Find patterns for refactoring legacy code

**Claude (uses `search_patterns`):**
> I found several OORP patterns for legacy code refactoring:
>
> 1. **Read all the Code in One Hour** (OORP-001)
>    - Category: First Contact
>    - Intent: Obtain a rough understanding of a large code base in a short time
>
> 2. **Skim the Documentation** (OORP-002)
>    - Category: First Contact
>    - Intent: Quickly understand system architecture through available documentation
>
> 3. **Interview During Demo** (OORP-003)
>    - Category: First Contact
>    - Intent: Learn about the system by observing a demonstration

### Example 2: Get Pattern Details

**You:**
> Tell me more about the "Split Up God Class" pattern

**Claude (uses `get_pattern`):**
> **Split Up God Class (OORP-045)**
>
> **Category:** Redistribute Responsibilities
>
> **Intent:** Break down a God Class into multiple focused classes with single responsibilities
>
> **Problem:**
> A single class has grown too large and handles too many responsibilities, making it:
> - Difficult to understand
> - Hard to maintain
> - Prone to bugs
> - Resistant to change
>
> **Solution:**
> 1. Identify distinct responsibilities within the God Class
> 2. Extract each responsibility into a new class
> 3. Redistribute dependencies and collaborations
> 4. Ensure each new class has a single, well-defined responsibility
>
> **Related Patterns:**
> - Extract Method
> - Move Method
> - Extract Class

### Example 3: Get Recommendations

**You:**
> I have a huge class with thousands of lines. How should I refactor it?

**Claude (uses `get_pattern_recommendations`):**
> For a large class with thousands of lines, I recommend these patterns:
>
> 1. **Split Up God Class** - Break it into focused classes with single responsibilities
> 2. **Extract Method** - Identify and extract cohesive method groups
> 3. **Move Method** - Relocate methods to more appropriate classes
> 4. **Redistribute Responsibilities** - Analyze and redistribute the class's responsibilities

### Example 4: List Categories

**You:**
> What pattern categories are available?

**Claude (uses `list_categories`):**
> PatternSphere currently has 8 OORP categories:
>
> 1. **First Contact** (7 patterns) - Initial system understanding
> 2. **Initial Understanding** (9 patterns) - Building comprehension
> 3. **Detailed Model Capture** (8 patterns) - Creating detailed models
> 4. **Redistribute Responsibilities** (11 patterns) - Reorganizing code
> 5. **Transform Conditionals to Polymorphism** (6 patterns) - OOP refactoring
> 6. **Migration Strategies** (8 patterns) - System migration approaches
> 7. **Setting Direction** (5 patterns) - Planning and strategy
> 8. **Tests: Your Life Insurance!** (7 patterns) - Testing strategies

## Troubleshooting

### Connection Failed

**Symptoms:**
- Tools don't appear in Claude Desktop
- Error messages about MCP server

**Solutions:**

1. **Check configuration file syntax:**
   - Ensure valid JSON (use a JSON validator)
   - Check for missing commas or brackets
   - Verify path format (double backslashes on Windows)

2. **Test server manually:**
   ```bash
   cd c:\Projects\PatternSphere
   venv\Scripts\activate
   python run_mcp_server.py
   ```

   Should output JSON-RPC messages (not errors)

3. **Check paths:**
   - Verify `python.exe` path exists
   - Verify `run_mcp_server.py` path exists
   - Verify `data` directory exists

4. **Restart Claude Desktop completely:**
   - Quit (not just close)
   - Wait 5 seconds
   - Restart

### Data Not Found

**Symptoms:**
- "No patterns found" errors
- Empty search results

**Solutions:**

1. **Verify data file exists:**
   ```bash
   dir c:\Projects\PatternSphere\data\sources\oorp\oorp_patterns_complete.json
   ```
   File should be ~200KB

2. **Check environment variable in config:**
   ```json
   "env": {
     "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data"
   }
   ```

### Permission Errors

**Windows:** Run as Administrator (right-click Claude Desktop → "Run as administrator")

**macOS/Linux:** Ensure config file has correct permissions:
```bash
chmod 644 ~/.config/Claude/claude_desktop_config.json
```

## Configuration Examples

### Multiple MCP Servers

You can configure multiple MCP servers in Claude Desktop:

```json
{
  "mcpServers": {
    "patternsphere": {
      "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
      "args": ["c:\\Projects\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Projects\\PatternSphere",
        "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data"
      }
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/other/server.js"]
    }
  }
}
```

### Custom Data Directory

To use a custom data directory:

```json
{
  "mcpServers": {
    "patternsphere": {
      "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
      "args": ["c:\\Projects\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Projects\\PatternSphere",
        "PATTERNSPHERE_DATA_DIR": "c:\\CustomData\\patterns"
      }
    }
  }
}
```

## Advanced: Debug Mode

To enable debug logging:

**Windows:**
```json
{
  "mcpServers": {
    "patternsphere": {
      "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
      "args": ["c:\\Projects\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Projects\\PatternSphere",
        "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

Logs will appear in:
```
%APPDATA%\Claude\logs\mcp-server-patternsphere.log
```

## More Information

- **MCP Protocol Documentation:** https://modelcontextprotocol.io
- **PatternSphere Repository:** https://github.com/yourusername/PatternSphere
- **Issue Tracker:** https://github.com/yourusername/PatternSphere/issues
- **CLI Reference:** [../CLI_Reference.md](../CLI_Reference.md)
- **Full Documentation:** [../../README.md](../../README.md)

## Related Guides

- **Claude Code (VSCode) Setup:** [MCP_QUICKSTART.md](MCP_QUICKSTART.md)
- **MCP Testing Guide:** [MCP_TEST_GUIDE.md](MCP_TEST_GUIDE.md)
- **Project Structure:** [../FILE_STRUCTURE.md](../FILE_STRUCTURE.md)

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section above.
