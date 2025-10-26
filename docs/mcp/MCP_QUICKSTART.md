# PatternSphere MCP 서버 - 빠른 시작 가이드

## ✅ 성공! MCP 서버가 연결되었습니다

PatternSphere MCP 서버가 Claude Code에 성공적으로 연결되었습니다!

```bash
$ claude mcp list
Checking MCP server health...

context7: https://mcp.context7.com/mcp (HTTP) - ✓ Connected
patternsphere: c:\Projects\PatternSphere\venv\Scripts\python.exe c:\Projects\PatternSphere\run_mcp_server.py - ✓ Connected
```

---

## 1단계: 설치 (완료)

```bash
# 프로젝트 디렉토리로 이동
cd c:\Projects\PatternSphere

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 패키지 설치
pip install -e .

# 설치 확인
patternsphere info
```

## 2단계: Claude Code CLI로 MCP 서버 추가 (1분)

**단 한 줄의 명령으로 설정 완료!**

```bash
claude mcp add --transport stdio patternsphere -e "PYTHONPATH=c:\\Projects\\PatternSphere" -e "PATTERNSPHERE_DATA_DIR=c:\\Projects\\PatternSphere\\data" -- "c:\\Projects\\PatternSphere\\venv\\Scripts\\python.exe" "c:\\Projects\\PatternSphere\\run_mcp_server.py"
```

**⚠️ 중요:**
- 경로의 백슬래시는 이중으로 (`\\`) 작성
- 프로젝트 경로가 다르면 위 명령의 경로를 수정
- 명령 실행 후 "Added stdio MCP server patternsphere..." 메시지 확인

**설정 확인:**
```bash
claude mcp list
```

예상 출력:
```
Checking MCP server health...
patternsphere: c:\Projects\PatternSphere\venv\Scripts\python.exe ... - ✓ Connected
```

## 3단계: VSCode 재시작 (필수!)

**Claude Code는 VSCode 확장이므로 VSCode를 재시작해야 합니다:**

1. **방법 1:** VSCode 명령 팔레트 (`Ctrl+Shift+P`) → "Developer: Reload Window"
2. **방법 2:** VSCode 완전 종료 후 재시작

재시작 후 다시 확인:
```bash
claude mcp list
```

이제 두 서버 모두 ✓ Connected 상태여야 합니다!

## 4단계: 사용 시작!

### 예시 대화:

**사용자:**
> 레거시 코드를 이해하는데 도움이 되는 패턴을 찾아줘

**Claude (자동으로 MCP 도구 사용):**
```
search_patterns({
  "query": "legacy code understanding",
  "category": "First Contact",
  "limit": 5
})
```

**결과:**
- Read all the Code in One Hour
- Interview During Demo
- Skim the Documentation
- (등등...)

---

## 문제 해결

### ✗ Failed to connect 오류

**증상:**
```bash
claude mcp list
# patternsphere: ... - ✗ Failed to connect
```

**원인:** MCP 서버 초기화 버그 (이미 수정됨)

**해결 방법:**

1. **서버가 수동으로 실행되는지 확인:**
   ```bash
   cd c:\Projects\PatternSphere
   venv\Scripts\activate
   python run_mcp_server.py
   ```

   **오류 발생 시:**
   ```
   RuntimeError: AppContext not initialized. Call initialize() first.
   ```

   → `patternsphere/mcp/server.py` 파일의 `__init__` 메서드에 `self.app_context.initialize()` 추가 필요

2. **수정 후 정상 출력 확인:**
   ```json
   {"jsonrpc": "2.0", "method": "initialize", ...}
   ```

   `Ctrl+C`로 종료

3. **VSCode 재시작:**
   - `Ctrl+Shift+P` → "Developer: Reload Window"
   - 또는 VSCode 완전 재시작

### MCP 서버 설정 확인

**Claude Code 설정 파일 위치:**
```
C:\Users\<사용자명>\.claude.json
```

**설정 내용 확인:**
```bash
claude mcp list
```

**설정 제거 (재설정 필요 시):**
```bash
claude mcp remove patternsphere
```

### 패턴을 찾을 수 없음

**데이터 파일 확인:**
```bash
dir c:\Projects\PatternSphere\data\sources\oorp\oorp_patterns_complete.json
```

파일이 있어야 합니다 (약 200KB).

---

## 사용 가능한 기능

| 기능 | 설명 | 예시 질문 |
|------|------|----------|
| **search_patterns** | 키워드로 패턴 검색 | "리팩토링 관련 패턴 찾아줘" |
| **get_pattern** | 특정 패턴 상세 조회 | "'Split Up God Class' 패턴 알려줘" |
| **list_categories** | 카테고리 목록 | "어떤 카테고리들이 있어?" |
| **list_patterns** | 패턴 목록 조회 | "First Contact 카테고리의 패턴들 보여줘" |
| **get_pattern_recommendations** | 문제 기반 추천 | "거대한 클래스를 어떻게 리팩토링하지?" |

---

## 더 알아보기

- **상세 테스트 가이드:** [MCP_TEST_GUIDE.md](MCP_TEST_GUIDE.md)
- **CLI 사용법:** [../CLI_Reference.md](../CLI_Reference.md)
- **전체 문서:** [../../README.md](../../README.md)

---

## 빠른 체크리스트

- [ ] 가상환경 생성 및 활성화
- [ ] `pip install -r requirements.txt`
- [ ] `pip install -e .`
- [ ] `patternsphere info` 실행 확인
- [ ] `claude mcp add` 명령으로 MCP 서버 추가
- [ ] `claude mcp list`로 연결 확인
- [ ] VSCode 재시작 (Reload Window)
- [ ] 다시 `claude mcp list`로 ✓ Connected 확인
- [ ] 첫 질문 시도!

---

## 🐛 수정된 버그 및 개선 사항

**v1.0.2 (2025-10-26):**
- **문제:** MCP 서버가 Claude Code와 연결 실패
- **원인:** MCP 프로토콜 초기화 핸드셰이크 미구현
- **수정:**
  1. [server.py:340-423](patternsphere/mcp/server.py#L340-L423)에서 표준 MCP 프로토콜 구현
  2. `initialize` 메서드 요청/응답 추가
  3. `tools/list` 메서드 추가
  4. 프로토콜 버전 2024-11-05 준수
- **영향:** Claude Code와 정상 연결, 5개 도구 사용 가능

**이전 수정 (v1.0.1):**
- `AppContext` 초기화 누락 문제 해결
- 검색 엔진 API 수정 (불필요한 `patterns` 인자 제거)
- JSON 직렬화 오류 수정 (`set` → `list` 변환)

---

설정 완료 후 Claude Code에서 패턴을 자연어로 검색하고 조회할 수 있습니다! 🎉
