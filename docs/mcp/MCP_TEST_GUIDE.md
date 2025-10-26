# PatternSphere MCP 서버 테스트 가이드

## 개요

이 문서는 PatternSphere MCP (Model Context Protocol) 서버를 테스트하고 Claude Desktop/Claude Code와 연결하는 방법을 설명합니다.

## 테스트 환경

- Python: 3.9 이상
- 운영체제: Windows, macOS, Linux
- 필수 패키지: `patternsphere` 및 의존성

## 1. 빠른 테스트 실행

전체 테스트 스위트를 실행하려면:

```bash
python test_mcp_server.py
```

### 테스트 항목

테스트 스위트는 다음 4가지 영역을 검증합니다:

1. **서버 초기화**: MCP 서버가 정상적으로 초기화되고 도구가 등록되는지 확인
2. **도구 호출**: 각 MCP 도구가 올바르게 작동하는지 검증
3. **프로토콜 통신**: JSON-RPC 프로토콜로 서버와 통신이 가능한지 확인
4. **Claude Desktop 설정**: 설정 파일과 경로가 유효한지 검증

### 예상 출력

모든 테스트가 통과하면 다음과 같은 출력을 볼 수 있습니다:

```
============================================================
테스트 결과 요약
============================================================
[PASS] - 서버 초기화
[PASS] - 도구 호출
[PASS] - 프로토콜 통신
[PASS] - Claude Desktop 설정

전체 성공률: 100.0% (4/4)

[SUCCESS] 모든 테스트 통과! MCP 서버가 정상 작동합니다.
```

## 2. 개별 테스트

### 2.1 서버 초기화 테스트

서버가 정상적으로 초기화되는지만 확인:

```python
from patternsphere.mcp.server import PatternSphereMCPServer

server = PatternSphereMCPServer()
tools = server.get_tools()

print(f"등록된 도구 개수: {len(tools)}")
for tool in tools:
    print(f"  - {tool['name']}: {tool['description']}")
```

### 2.2 도구 호출 테스트

특정 도구를 직접 호출하여 테스트:

```python
from patternsphere.mcp.server import PatternSphereMCPServer

server = PatternSphereMCPServer()

# 패턴 검색
result = server.handle_tool_call("search_patterns", {
    "query": "refactoring",
    "limit": 5
})
print(result)

# 특정 패턴 조회
result = server.handle_tool_call("get_pattern", {
    "pattern_name": "Read all the Code in One Hour"
})
print(result)

# 카테고리 목록
result = server.handle_tool_call("list_categories", {})
print(result)

# 패턴 추천
result = server.handle_tool_call("get_pattern_recommendations", {
    "problem": "understand legacy code",
    "limit": 3
})
print(result)
```

### 2.3 프로토콜 통신 테스트

실제 JSON-RPC 프로토콜로 통신:

```bash
# 서버 시작
python run_mcp_server.py

# 다른 터미널에서 요청 전송 (수동 테스트)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_patterns","arguments":{"query":"test","limit":2}}}' | python run_mcp_server.py
```

## 3. Claude Desktop 연결

### 3.1 설정 파일 위치

Claude Desktop의 MCP 서버 설정 파일:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 3.2 설정 추가

1. `claude_desktop_config.example.json` 파일을 열어 내용 복사:

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

2. 경로를 자신의 환경에 맞게 수정:
   - `command`: Python 가상환경의 `python.exe` 절대 경로
   - `args[0]`: `run_mcp_server.py` 절대 경로
   - `env.PYTHONPATH`: PatternSphere 프로젝트 루트 경로
   - `env.PATTERNSPHERE_DATA_DIR`: 패턴 데이터 디렉토리 경로

3. Claude Desktop 설정 파일에 추가 (기존 설정이 있다면 병합)

4. Claude Desktop 재시작

### 3.3 연결 확인

Claude Desktop에서:

```
사용 가능한 MCP 도구를 보여줘
```

또는

```
patternsphere 서버가 연결되어 있나?
```

## 4. 사용 가능한 MCP 도구

### 4.1 search_patterns

키워드로 패턴 검색:

```
"refactoring" 관련 패턴을 검색해줘
```

**매개변수:**
- `query` (필수): 검색 키워드
- `category` (선택): 카테고리 필터
- `tags` (선택): 태그 필터 (쉼표로 구분)
- `limit` (선택): 결과 개수 제한 (기본값: 10)

### 4.2 get_pattern

특정 패턴의 상세 정보 조회:

```
"Read all the Code in One Hour" 패턴의 상세 정보를 보여줘
```

**매개변수:**
- `pattern_name` (필수): 패턴 이름 또는 ID

### 4.3 list_categories

모든 카테고리와 패턴 개수 조회:

```
패턴 카테고리 목록을 보여줘
```

### 4.4 list_patterns

패턴 목록 조회:

```
"Tests: Your Life Insurance!" 카테고리의 모든 패턴을 보여줘
```

**매개변수:**
- `category` (선택): 카테고리 필터

### 4.5 get_pattern_recommendations

문제 상황에 맞는 패턴 추천:

```
레거시 코드를 이해하는데 도움이 되는 패턴을 추천해줘
```

**매개변수:**
- `problem` (필수): 문제 설명
- `limit` (선택): 추천 개수 (기본값: 5)

## 5. 트러블슈팅

### 5.1 서버 초기화 실패

**증상**: `[FAIL] 서버 초기화 실패`

**해결 방법:**
1. Python 가상환경이 활성화되어 있는지 확인
2. 필수 패키지가 설치되어 있는지 확인:
   ```bash
   pip install -e .
   ```
3. 데이터 디렉토리가 존재하는지 확인

### 5.2 도구 호출 실패

**증상**: `[FAIL] 실패: KeywordSearchEngine.search() got an unexpected keyword argument`

**해결 방법:**
- MCP 서버 코드가 최신 버전인지 확인
- `patternsphere.mcp.server.py`에서 `search()` 호출 시 `patterns` 인자를 제거

### 5.3 프로토콜 통신 실패

**증상**: `[FAIL] 프로토콜 통신 실패` 또는 `Object of type set is not JSON serializable`

**해결 방법:**
- `matched_fields`를 JSON 직렬화 가능한 `list`로 변환했는지 확인
- MCP 서버에서 반환하는 모든 데이터가 JSON 직렬화 가능한지 검증

### 5.4 Claude Desktop 연결 실패

**증상**: Claude Desktop에서 patternsphere 도구를 사용할 수 없음

**해결 방법:**
1. 설정 파일 경로가 올바른지 확인
2. Python 경로와 스크립트 경로가 절대 경로인지 확인
3. Claude Desktop을 완전히 재시작 (작업 관리자에서 프로세스 종료 후 재실행)
4. Claude Desktop 로그 확인:
   - Windows: `%APPDATA%\Claude\logs`
   - macOS: `~/Library/Logs/Claude`

### 5.5 Windows 인코딩 문제

**증상**: `UnicodeEncodeError: 'cp949' codec can't encode character`

**해결 방법:**
- 테스트 스크립트에 UTF-8 인코딩 설정 추가됨 (이미 수정됨)
- Windows 콘솔에서 `chcp 65001` 명령으로 UTF-8 코드 페이지 설정

## 6. 추가 정보

### 6.1 로그 확인

MCP 서버는 구조적 로깅을 사용합니다:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 6.2 성능 모니터링

검색 엔진은 자동으로 실행 시간을 로깅합니다:

```
Search complete: 3 results in 5.23ms (query: 'refactoring')
```

### 6.3 데이터 업데이트

패턴 데이터를 업데이트하려면:

1. `data/patterns/` 디렉토리에 YAML 파일 추가/수정
2. MCP 서버 재시작 (또는 Claude Desktop 재시작)

## 7. 다음 단계

- [ ] Claude Code에서 MCP 서버 테스트
- [ ] 추가 패턴 데이터 추가
- [ ] 검색 알고리즘 개선 (의미론적 검색)
- [ ] 성능 최적화 (캐싱)
- [ ] 모니터링 및 메트릭 수집

## 참고 자료

- [Model Context Protocol (MCP) 공식 문서](https://modelcontextprotocol.io/)
- [Claude Desktop MCP 서버 가이드](https://docs.anthropic.com/claude/docs/mcp)
- [PatternSphere README](README.md)
