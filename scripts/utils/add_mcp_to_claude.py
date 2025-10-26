"""
Claude Code 설정에 PatternSphere MCP 서버를 환경 변수와 함께 추가
"""

import json
import sys
from pathlib import Path

# 설정 파일 경로
config_path = Path.home() / ".claude.json"

print(f"Reading config from: {config_path}")

# 현재 설정 읽기
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 프로젝트별 설정 찾기
project_path = r"C:\Projects\PatternSphere"

if project_path not in config.get("projects", {}):
    print(f"Project {project_path} not found in config")
    sys.exit(1)

project_config = config["projects"][project_path]

# MCP 서버 설정
patternsphere_config = {
    "type": "stdio",
    "command": r"c:\Projects\PatternSphere\venv\Scripts\python.exe",
    "args": [r"c:\Projects\PatternSphere\run_mcp_server.py"],
    "env": {
        "PYTHONPATH": r"c:\Projects\PatternSphere",
        "PATTERNSPHERE_DATA_DIR": r"c:\Projects\PatternSphere\data"
    }
}

# mcpServers에 추가
if "mcpServers" not in project_config:
    project_config["mcpServers"] = {}

project_config["mcpServers"]["patternsphere"] = patternsphere_config

# 설정 저장
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print(f"\nPatternSphere MCP server added successfully!")
print(f"\nConfiguration:")
print(json.dumps(patternsphere_config, indent=2))
print(f"\nPlease restart Claude Code to apply changes.")
