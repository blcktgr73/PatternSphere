# PatternSphere MCP Server 설정 가이드

이 가이드는 PatternSphere를 MCP (Model Context Protocol) 서버로 설정하여 Claude Code에서 사용하는 방법을 안내합니다.

## 목차

1. [MCP 서버 구현](#1-mcp-서버-구현)
2. [로컬 설치](#2-로컬-설치)
3. [Claude Code MCP 설정](#3-claude-code-mcp-설정)
4. [사용 방법](#4-사용-방법)
5. [문제 해결](#5-문제-해결)

---

## 1. MCP 서버 구현

### 1.1 MCP 서버 파일 생성

PatternSphere를 MCP 서버로 사용하려면 MCP 프로토콜을 구현해야 합니다.

**파일 생성**: `patternsphere/mcp/server.py`

```python
"""
PatternSphere MCP Server

MCP (Model Context Protocol) 서버 구현으로 Claude Code에서
패턴 검색 및 조회 기능을 제공합니다.
"""

import sys
import json
from typing import Any, Dict, List, Optional
from pathlib import Path

# PatternSphere 컴포넌트 임포트
from patternsphere.cli.app_context import AppContext
from patternsphere.search.search_engine import KeywordSearchEngine


class PatternSphereMCPServer:
    """
    PatternSphere MCP 서버

    Claude Code에서 디자인 패턴을 검색하고 조회할 수 있는
    MCP 도구를 제공합니다.
    """

    def __init__(self):
        """MCP 서버 초기화"""
        self.app_context = AppContext()
        self.search_engine = self.app_context.search_engine
        self.repository = self.app_context.repository

        # 서버 정보
        self.server_info = {
            "name": "patternsphere",
            "version": "1.0.0",
            "description": "Design pattern knowledge base with 61 OORP patterns"
        }

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        MCP 도구 목록 반환

        Claude Code에서 사용할 수 있는 도구들을 정의합니다.
        """
        return [
            {
                "name": "search_patterns",
                "description": "Search for software design patterns by keywords, category, or tags. Returns relevant patterns with descriptions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search keywords (e.g., 'refactoring', 'testing', 'code quality')"
                        },
                        "category": {
                            "type": "string",
                            "description": "Filter by category (e.g., 'First Contact', 'Tests: Your Life Insurance!')",
                            "enum": [
                                "First Contact",
                                "Initial Understanding",
                                "Detailed Model Capture",
                                "Redistribute Responsibilities",
                                "Transform Conditionals to Polymorphism",
                                "Migration Strategies",
                                "Setting Direction",
                                "Tests: Your Life Insurance!"
                            ]
                        },
                        "tags": {
                            "type": "string",
                            "description": "Filter by tags, comma-separated (e.g., 'testing,quality')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_pattern",
                "description": "Get complete details of a specific pattern by name or ID. Returns full pattern information including problem, solution, and consequences.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern_name": {
                            "type": "string",
                            "description": "Pattern name or ID (e.g., 'Read all the Code in One Hour', 'OORP-001')"
                        }
                    },
                    "required": ["pattern_name"]
                }
            },
            {
                "name": "list_categories",
                "description": "List all pattern categories with pattern counts. Useful for discovering available pattern categories.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "list_patterns",
                "description": "List all patterns or filter by category. Returns pattern names and categories.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter by category (optional)"
                        }
                    }
                }
            },
            {
                "name": "get_pattern_recommendations",
                "description": "Get pattern recommendations based on a problem description or context.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "problem": {
                            "type": "string",
                            "description": "Description of the problem or situation (e.g., 'need to understand legacy codebase', 'refactor large class')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of recommendations (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["problem"]
                }
            }
        ]

    def search_patterns(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """패턴 검색"""
        try:
            # 모든 패턴 가져오기
            patterns = self.repository.list_all_patterns()

            # 태그 파싱
            tag_list = None
            if tags:
                tag_list = [t.strip() for t in tags.split(",")]

            # 검색 수행
            results = self.search_engine.search(
                patterns=patterns,
                query=query,
                category=category,
                tags=tag_list
            )

            # 결과 제한
            results = results[:limit]

            # 결과 포맷팅
            formatted_results = []
            for result in results:
                pattern = result.pattern
                formatted_results.append({
                    "name": pattern.name,
                    "category": pattern.category,
                    "intent": pattern.intent,
                    "tags": pattern.tags,
                    "relevance_score": round(result.score, 2),
                    "matched_fields": result.matched_fields
                })

            return {
                "success": True,
                "count": len(formatted_results),
                "query": query,
                "results": formatted_results
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_pattern(self, pattern_name: str) -> Dict[str, Any]:
        """특정 패턴 조회"""
        try:
            # ID 또는 이름으로 검색
            pattern = self.repository.get_pattern_by_name(pattern_name)

            if not pattern:
                # ID로 시도
                pattern = self.repository.get_pattern_by_id(pattern_name)

            if not pattern:
                return {
                    "success": False,
                    "error": f"Pattern not found: {pattern_name}"
                }

            # 패턴 정보 반환
            return {
                "success": True,
                "pattern": {
                    "id": pattern.id,
                    "name": pattern.name,
                    "category": pattern.category,
                    "intent": pattern.intent,
                    "problem": pattern.problem,
                    "context": pattern.context,
                    "solution": pattern.solution,
                    "consequences": pattern.consequences,
                    "related_patterns": pattern.related_patterns,
                    "tags": pattern.tags,
                    "source": {
                        "name": pattern.source_metadata.source_name,
                        "authors": pattern.source_metadata.authors,
                        "year": pattern.source_metadata.publication_year,
                        "url": pattern.source_metadata.url
                    }
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_categories(self) -> Dict[str, Any]:
        """카테고리 목록 조회"""
        try:
            categories = self.repository.get_all_categories()

            return {
                "success": True,
                "total_categories": len(categories),
                "categories": [
                    {"name": name, "count": count}
                    for name, count in categories.items()
                ]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_patterns(self, category: Optional[str] = None) -> Dict[str, Any]:
        """패턴 목록 조회"""
        try:
            if category:
                patterns = self.repository.get_patterns_by_category(category)
            else:
                patterns = self.repository.list_all_patterns()

            return {
                "success": True,
                "count": len(patterns),
                "category": category,
                "patterns": [
                    {
                        "name": p.name,
                        "category": p.category,
                        "intent": p.intent,
                        "tags": p.tags
                    }
                    for p in patterns
                ]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_pattern_recommendations(
        self,
        problem: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """문제 기반 패턴 추천"""
        try:
            # 문제 설명으로 검색
            patterns = self.repository.list_all_patterns()
            results = self.search_engine.search(
                patterns=patterns,
                query=problem
            )

            # 상위 N개 결과
            results = results[:limit]

            recommendations = []
            for result in results:
                pattern = result.pattern
                recommendations.append({
                    "name": pattern.name,
                    "category": pattern.category,
                    "intent": pattern.intent,
                    "relevance_score": round(result.score, 2),
                    "why_relevant": f"Matches: {', '.join(result.matched_fields)}"
                })

            return {
                "success": True,
                "problem": problem,
                "count": len(recommendations),
                "recommendations": recommendations
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출 처리"""
        if tool_name == "search_patterns":
            return self.search_patterns(**arguments)
        elif tool_name == "get_pattern":
            return self.get_pattern(**arguments)
        elif tool_name == "list_categories":
            return self.list_categories()
        elif tool_name == "list_patterns":
            return self.list_patterns(**arguments)
        elif tool_name == "get_pattern_recommendations":
            return self.get_pattern_recommendations(**arguments)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

    def run(self):
        """
        MCP 서버 실행

        stdin/stdout을 통해 JSON-RPC 프로토콜로 통신합니다.
        """
        print(json.dumps({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "serverInfo": self.server_info,
                "capabilities": {
                    "tools": self.get_tools()
                }
            }
        }), flush=True)

        # 요청 처리 루프
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                if method == "tools/call":
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})

                    result = self.handle_tool_call(tool_name, arguments)

                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2, ensure_ascii=False)
                                }
                            ]
                        }
                    }

                    print(json.dumps(response, ensure_ascii=False), flush=True)

            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response), flush=True)


def main():
    """MCP 서버 메인 함수"""
    server = PatternSphereMCPServer()
    server.run()


if __name__ == "__main__":
    main()
```

### 1.2 MCP 서버 엔트리 포인트 생성

**파일 생성**: `patternsphere/mcp/__init__.py`

```python
"""PatternSphere MCP Server Package"""

from patternsphere.mcp.server import PatternSphereMCPServer, main

__all__ = ["PatternSphereMCPServer", "main"]
```

### 1.3 MCP 실행 스크립트 생성

**파일 생성**: `run_mcp_server.py` (프로젝트 루트)

```python
"""
PatternSphere MCP Server 실행 스크립트

Claude Code에서 사용할 MCP 서버를 시작합니다.
"""

from patternsphere.mcp.server import main

if __name__ == "__main__":
    main()
```

---

## 2. 로컬 설치

### 2.1 기본 설치

```bash
# 1. 프로젝트 디렉토리로 이동
cd c:\Projects\PatternSphere

# 2. 가상환경 생성 (선택사항이지만 권장)
python -m venv venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate

# 4. 의존성 설치
pip install -r requirements.txt

# 5. 개발 모드로 패키지 설치
pip install -e .
```

### 2.2 설치 확인

```bash
# CLI 버전 확인
patternsphere --version
# 출력: PatternSphere v1.0.0

# 패턴 개수 확인
patternsphere info
```

### 2.3 MCP 서버 테스트

```bash
# MCP 서버 직접 실행 (테스트용)
python run_mcp_server.py
```

성공하면 다음과 같은 JSON이 출력됩니다:
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "serverInfo": {
      "name": "patternsphere",
      "version": "1.0.0",
      "description": "Design pattern knowledge base with 61 OORP patterns"
    },
    "capabilities": {
      "tools": [...]
    }
  }
}
```

`Ctrl+C`로 종료합니다.

---

## 3. Claude Code MCP 설정

### 3.1 Claude Code 설정 파일 위치

Claude Code의 MCP 설정은 다음 파일에 저장됩니다:

**Windows:**
```
C:\Users\<사용자명>\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 3.2 설정 파일 편집

설정 파일을 열고 다음 내용을 추가합니다:

```json
{
  "mcpServers": {
    "patternsphere": {
      "command": "python",
      "args": [
        "c:\\Projects\\PatternSphere\\run_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "c:\\Projects\\PatternSphere"
      }
    }
  }
}
```

**주의사항:**
- Windows 경로는 백슬래시를 이중으로 (`\\`) 사용합니다
- 가상환경을 사용하는 경우 `python` 대신 가상환경의 Python 경로를 지정합니다:
  ```json
  "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe"
  ```

### 3.3 가상환경 사용 시 설정 (권장)

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

### 3.4 Claude Code 재시작

설정 파일을 저장한 후 **Claude Code를 완전히 종료하고 다시 시작**합니다.

---

## 4. 사용 방법

### 4.1 MCP 도구 확인

Claude Code를 재시작한 후, 대화창에서 다음을 확인할 수 있습니다:

```
🔧 Available MCP Tools:
- patternsphere: search_patterns
- patternsphere: get_pattern
- patternsphere: list_categories
- patternsphere: list_patterns
- patternsphere: get_pattern_recommendations
```

### 4.2 사용 예시

#### 예시 1: 패턴 검색

**사용자 입력:**
```
레거시 코드베이스를 이해하는데 도움이 되는 패턴을 찾아줘
```

**Claude의 응답 (MCP 도구 사용):**
```
search_patterns({
  "query": "legacy codebase understanding",
  "category": "First Contact",
  "limit": 5
})
```

**결과:**
```json
{
  "success": true,
  "count": 5,
  "results": [
    {
      "name": "Read all the Code in One Hour",
      "category": "First Contact",
      "intent": "Assess the state of a software system through a time-boxed code reading session",
      "relevance_score": 8.5
    },
    ...
  ]
}
```

#### 예시 2: 특정 패턴 상세 조회

**사용자 입력:**
```
"Read all the Code in One Hour" 패턴의 상세 내용을 알려줘
```

**Claude의 응답 (MCP 도구 사용):**
```
get_pattern({
  "pattern_name": "Read all the Code in One Hour"
})
```

**결과: 패턴의 전체 내용 (problem, solution, consequences 포함)**

#### 예시 3: 카테고리 탐색

**사용자 입력:**
```
어떤 패턴 카테고리들이 있어?
```

**Claude의 응답 (MCP 도구 사용):**
```
list_categories({})
```

**결과:**
```json
{
  "success": true,
  "total_categories": 8,
  "categories": [
    {"name": "First Contact", "count": 6},
    {"name": "Tests: Your Life Insurance!", "count": 6},
    ...
  ]
}
```

#### 예시 4: 문제 기반 추천

**사용자 입력:**
```
거대한 God Class를 리팩토링하려고 하는데 어떤 패턴을 사용하면 좋을까?
```

**Claude의 응답 (MCP 도구 사용):**
```
get_pattern_recommendations({
  "problem": "refactor god class large class split responsibilities",
  "limit": 5
})
```

**결과: 관련성 높은 패턴 추천 목록**

### 4.3 통합 워크플로우 예시

**시나리오: 레거시 프로젝트 리팩토링 계획**

```
사용자: 10년된 레거시 Java 프로젝트를 리팩토링하려고 해.
       어디서부터 시작해야 할지 패턴을 추천해줘.

Claude: [list_categories 호출]
        먼저 사용 가능한 패턴 카테고리를 확인하겠습니다.

        레거시 프로젝트 리팩토링을 위한 패턴 카테고리:
        1. First Contact (6개) - 초기 평가
        2. Setting Direction (10개) - 전략 수립
        3. Tests: Your Life Insurance! (6개) - 테스트 전략

        [search_patterns 호출: query="legacy refactoring start"]

        추천 순서:
        1. "Read all the Code in One Hour" - 전체 구조 파악
        2. "Interview During Demo" - 도메인 이해
        3. "Write Tests to Enable Evolution" - 안전한 변경 준비

        각 패턴의 상세 내용을 보시겠습니까?

사용자: "Write Tests to Enable Evolution" 패턴 상세 내용 보여줘

Claude: [get_pattern 호출]

        [패턴 상세 내용 표시]

        이 패턴에 따르면:
        - 문제: 테스트 없이는 리팩토링이 위험
        - 해결책: 변경하려는 코드부터 테스트 작성
        - 관련 패턴: "Test Fuzzy Features", "Retest Persistent Problems"

        다음 단계로 관련 패턴도 확인해볼까요?
```

---

## 5. 문제 해결

### 5.1 MCP 서버가 시작되지 않음

**증상:** Claude Code에서 patternsphere 도구가 보이지 않음

**해결 방법:**

1. **설정 파일 경로 확인**
   ```bash
   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json

   # 또는 PowerShell
   Get-Content $env:APPDATA\Claude\claude_desktop_config.json
   ```

2. **JSON 형식 검증**
   - JSON 파일이 올바른 형식인지 확인 (쉼표, 괄호 등)
   - [JSONLint](https://jsonlint.com/)에서 검증

3. **Python 경로 확인**
   ```bash
   # 가상환경 Python 위치 확인
   where python

   # 또는
   c:\Projects\PatternSphere\venv\Scripts\python.exe --version
   ```

4. **수동 테스트**
   ```bash
   # MCP 서버가 정상 실행되는지 확인
   cd c:\Projects\PatternSphere
   venv\Scripts\activate
   python run_mcp_server.py
   ```

### 5.2 패턴을 찾을 수 없음

**증상:** "Pattern not found" 오류

**해결 방법:**

1. **데이터 파일 확인**
   ```bash
   # 패턴 파일이 존재하는지 확인
   dir c:\Projects\PatternSphere\data\sources\oorp\oorp_patterns_complete.json
   ```

2. **환경 변수 설정**
   ```json
   {
     "mcpServers": {
       "patternsphere": {
         "env": {
           "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data"
         }
       }
     }
   }
   ```

### 5.3 느린 응답 속도

**증상:** MCP 도구 호출이 느림

**해결 방법:**

1. **패턴 로딩 확인**
   - 첫 호출 시 패턴 로딩에 ~2ms 소요 (정상)
   - 이후 호출은 캐시 사용으로 빠름

2. **성능 테스트**
   ```bash
   patternsphere info
   # Loading time 확인
   ```

### 5.4 Claude Code 로그 확인

**Windows 로그 위치:**
```
%APPDATA%\Claude\logs\
```

**로그에서 MCP 관련 오류 확인:**
```bash
# PowerShell
Get-Content "$env:APPDATA\Claude\logs\main.log" | Select-String "patternsphere"
```

### 5.5 일반적인 오류 메시지

| 오류 | 원인 | 해결 |
|------|------|------|
| `FileNotFoundError` | Python 스크립트 경로 오류 | 설정 파일의 `args` 경로 확인 |
| `ModuleNotFoundError` | 패키지 미설치 | `pip install -e .` 재실행 |
| `JSON parsing error` | 설정 파일 문법 오류 | JSON 검증 도구로 확인 |
| `Permission denied` | 파일 권한 문제 | 관리자 권한으로 실행 |

---

## 6. 고급 설정

### 6.1 여러 환경 설정

개발/프로덕션 환경 분리:

```json
{
  "mcpServers": {
    "patternsphere-dev": {
      "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
      "args": ["c:\\Projects\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PATTERNSPHERE_DATA_DIR": "c:\\Projects\\PatternSphere\\data"
      }
    },
    "patternsphere-prod": {
      "command": "python",
      "args": ["c:\\Production\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PATTERNSPHERE_DATA_DIR": "c:\\Production\\PatternSphere\\data"
      }
    }
  }
}
```

### 6.2 로깅 활성화

디버깅을 위한 로깅 추가:

```json
{
  "mcpServers": {
    "patternsphere": {
      "command": "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe",
      "args": ["c:\\Projects\\PatternSphere\\run_mcp_server.py"],
      "env": {
        "PYTHONPATH": "c:\\Projects\\PatternSphere",
        "PATTERNSPHERE_LOG_LEVEL": "DEBUG",
        "PATTERNSPHERE_LOG_FILE": "c:\\Projects\\PatternSphere\\mcp_server.log"
      }
    }
  }
}
```

### 6.3 성능 최적화

패턴 캐싱 및 사전 로딩 설정:

```json
{
  "mcpServers": {
    "patternsphere": {
      "env": {
        "PATTERNSPHERE_PRELOAD_PATTERNS": "true",
        "PATTERNSPHERE_CACHE_SIZE": "100"
      }
    }
  }
}
```

---

## 7. 사용 팁

### 7.1 효과적인 검색 쿼리

**좋은 예시:**
- "refactoring large classes" ✅
- "testing legacy code" ✅
- "understand unfamiliar codebase" ✅

**나쁜 예시:**
- "pattern" ❌ (너무 일반적)
- "help" ❌ (구체적이지 않음)

### 7.2 카테고리 활용

각 상황에 맞는 카테고리:

- **프로젝트 시작**: "First Contact"
- **리팩토링**: "Redistribute Responsibilities"
- **테스트 추가**: "Tests: Your Life Insurance!"
- **마이그레이션**: "Migration Strategies"

### 7.3 관련 패턴 탐색

패턴 상세 조회 시 `related_patterns` 필드를 확인하여 연관 패턴을 탐색하세요.

---

## 8. 참고 자료

- **MCP 공식 문서**: https://modelcontextprotocol.io/
- **Claude Code 문서**: https://docs.claude.com/claude-code
- **PatternSphere CLI Reference**: [docs/CLI_Reference.md](CLI_Reference.md)
- **PatternSphere README**: [README.md](../README.md)

---

## 요약

1. **MCP 서버 구현**: `patternsphere/mcp/server.py` 생성
2. **로컬 설치**: `pip install -e .`
3. **설정 파일**: `claude_desktop_config.json` 편집
4. **Claude Code 재시작**: 설정 적용
5. **사용**: Claude에게 패턴 검색/조회 요청

**완료 후 사용 가능한 기능:**
- 키워드로 패턴 검색
- 특정 패턴 상세 조회
- 카테고리 탐색
- 패턴 목록 확인
- 문제 기반 패턴 추천

PatternSphere MCP 서버 설정이 완료되었습니다! 🎉
