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


class PatternSphereMCPServer:
    """
    PatternSphere MCP 서버

    Claude Code에서 디자인 패턴을 검색하고 조회할 수 있는
    MCP 도구를 제공합니다.
    """

    def __init__(self):
        """MCP 서버 초기화"""
        self.app_context = AppContext()
        self.app_context.initialize()
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
            # 태그 파싱
            tag_list = None
            if tags:
                tag_list = [t.strip() for t in tags.split(",")]

            # 검색 수행 (search_engine이 repository에서 직접 가져옴)
            results = self.search_engine.search(
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
                    "matched_fields": list(result.matched_fields)  # set을 list로 변환
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
            # 문제 설명으로 검색 (search_engine이 repository에서 직접 가져옴)
            results = self.search_engine.search(
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
                    "why_relevant": f"Matches: {', '.join(sorted(result.matched_fields))}"
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
        # 요청 처리 루프
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")

                if method == "initialize":
                    # 초기화 요청에 응답
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "serverInfo": self.server_info,
                            "capabilities": {
                                "tools": {}
                            }
                        }
                    }
                    print(json.dumps(response), flush=True)

                elif method == "tools/list":
                    # 도구 목록 요청
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "tools": self.get_tools()
                        }
                    }
                    print(json.dumps(response), flush=True)

                elif method == "tools/call":
                    # 도구 호출 요청
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
                                    "text": json.dumps(result, indent=2, ensure_ascii=True)
                                }
                            ]
                        }
                    }

                    print(json.dumps(response, ensure_ascii=True), flush=True)

                else:
                    # 알 수 없는 메서드
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)

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
