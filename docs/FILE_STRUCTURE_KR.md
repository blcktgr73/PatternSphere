# PatternSphere 파일 구조

마지막 업데이트: 2025-10-26

## 프로젝트 루트

```
PatternSphere/
├── README.md                    # 프로젝트 메인 문서
├── CHANGELOG.md                # 버전 히스토리
├── setup.py                    # 패키지 설치 스크립트
├── requirements.txt            # Python 의존성
├── pytest.ini                  # pytest 설정
├── run_mcp_server.py          # MCP 서버 진입점
└── .gitignore                  # Git 무시 파일 목록
```

## 주요 디렉토리

### 📦 patternsphere/ - 메인 패키지

```
patternsphere/
├── __init__.py
├── models/                     # 데이터 모델
│   ├── __init__.py
│   └── pattern.py             # Pattern, SourceMetadata
├── repository/                 # 저장소 계층
│   ├── __init__.py
│   ├── repository_interface.py
│   └── pattern_repository.py
├── storage/                    # 영속성 계층
│   ├── __init__.py
│   ├── storage_interface.py
│   └── file_storage.py
├── search/                     # 검색 엔진
│   ├── __init__.py
│   └── search_engine.py
├── loaders/                    # 데이터 로더
│   ├── __init__.py
│   └── oorp_loader.py
├── config/                     # 설정 관리
│   ├── __init__.py
│   └── settings.py
├── cli/                        # CLI 인터페이스
│   ├── __init__.py
│   ├── main.py                # CLI 진입점
│   ├── commands.py            # 5개 CLI 커맨드
│   ├── app_context.py         # 의존성 주입 컨텍스트
│   └── formatters/            # 출력 포매터
│       ├── __init__.py
│       ├── pattern_formatter.py
│       └── search_formatter.py
└── mcp/                        # MCP 서버 구현
    ├── __init__.py
    └── server.py              # PatternSphereMCPServer
```

### 📚 docs/ - 문서

```
docs/
├── mcp/                        # MCP 서버 문서
│   ├── MCP_QUICKSTART.md      # 빠른 시작 가이드
│   └── MCP_TEST_GUIDE.md      # 테스트 가이드
├── development/                # 개발 문서
│   ├── CLAUDE.md              # AI 페어 프로그래밍 가이드
│   └── PATTERN_ANALYSIS.md    # 패턴 적용 분석
├── CLI_Reference.md            # CLI 커맨드 레퍼런스
├── PRD.md                      # 제품 요구사항 문서
└── Phase1_Product_Specification.md  # Phase 1 스펙
```

### 🗂️ data/ - 패턴 데이터

```
data/
└── sources/
    └── oorp/                   # OORP 패턴 (61개)
        └── oorp_patterns_complete.json
```

### 🧪 tests/ - 테스트 스위트 (248 tests)

```
tests/
├── unit/                       # 단위 테스트 (178개)
│   ├── test_pattern.py
│   ├── test_repository.py
│   ├── test_search_engine.py
│   ├── test_storage.py
│   ├── test_oorp_loader.py
│   ├── test_cli_commands.py
│   └── test_app_context.py
├── integration/                # 통합 테스트 (55개)
│   ├── test_search_flow.py
│   ├── test_cli_integration.py
│   └── test_pattern_loading.py
└── performance/                # 성능 테스트 (15개)
    ├── test_search_performance.py
    ├── test_loading_performance.py
    └── test_cli_startup.py
```

### ⚙️ config/ - 설정 파일

```
config/
└── examples/                   # 예제 설정 파일
    ├── claude_desktop_config.example.json
    └── claude_desktop_config_with_context7.json
```

### 🔧 scripts/ - 유틸리티 스크립트

```
scripts/
├── test_mcp_server.py         # MCP 서버 테스트 스크립트
├── demos/                      # 데모 스크립트
│   ├── demo_sprint1.py
│   ├── demo_sprint2.py
│   └── demo_sprint3.py
└── utils/                      # 유틸리티 스크립트
    ├── add_mcp_to_claude.py   # MCP 서버 설정 헬퍼
    └── debug_mcp.py            # MCP 서버 디버그 도구
```

## 파일 용도

### 핵심 파일

| 파일 | 용도 |
|------|------|
| `setup.py` | 패키지 설치 및 배포 |
| `requirements.txt` | Python 의존성 목록 |
| `run_mcp_server.py` | MCP 서버 실행 진입점 |
| `pytest.ini` | pytest 테스트 설정 |

### 문서 파일

| 파일 | 용도 |
|------|------|
| `README.md` | 프로젝트 메인 문서 |
| `CHANGELOG.md` | 버전 변경 이력 |
| `FILE_STRUCTURE.md` | 이 파일 - 파일 구조 설명 |

### 설정 파일

| 파일 | 용도 |
|------|------|
| `config/examples/claude_desktop_config.example.json` | Claude Desktop MCP 설정 예제 |
| `.gitignore` | Git 버전 관리 제외 파일 |

### 테스트/개발 파일

| 파일 | 용도 |
|------|------|
| `scripts/test_mcp_server.py` | MCP 서버 종합 테스트 |
| `scripts/demos/demo_sprint*.py` | 각 스프린트 데모 스크립트 |
| `scripts/utils/add_mcp_to_claude.py` | MCP 설정 자동화 |

## Git 무시 파일

`.gitignore`에 포함된 항목:

- `__pycache__/` - Python 캐시
- `*.pyc`, `*.pyo` - 컴파일된 Python 파일
- `venv/`, `env/` - 가상 환경
- `.pytest_cache/` - pytest 캐시
- `.coverage`, `htmlcov/`, `coverage.json` - 커버리지 보고서
- `dist/`, `build/`, `*.egg-info/` - 빌드 결과물
- `.vscode/`, `.idea/` - IDE 설정
- `.DS_Store`, `Thumbs.db` - OS 메타데이터

## 디렉토리 생성 이력

**2025-10-26**: 프로젝트 재구성
- `docs/mcp/` 생성 - MCP 관련 문서 분리
- `docs/development/` 생성 - 개발 가이드 분리
- `config/examples/` 생성 - 설정 예제 분리
- `scripts/` 생성 - 유틸리티 스크립트 분리
  - `scripts/demos/` - 데모 스크립트
  - `scripts/utils/` - 유틸리티 도구

## 파일 이동 로그

### 2025-10-26 재구성

**문서 파일 이동:**
- `CLAUDE.md` → `docs/development/CLAUDE.md`
- `PATTERN_ANALYSIS.md` → `docs/development/PATTERN_ANALYSIS.md`
- `MCP_QUICKSTART.md` → `docs/mcp/MCP_QUICKSTART.md`
- `MCP_TEST_GUIDE.md` → `docs/mcp/MCP_TEST_GUIDE.md`

**설정 파일 이동:**
- `claude_desktop_config.example.json` → `config/examples/`
- `claude_desktop_config_with_context7.json` → `config/examples/`

**스크립트 파일 이동:**
- `test_mcp_server.py` → `scripts/test_mcp_server.py`
- `demo_sprint1.py` → `scripts/demos/demo_sprint1.py`
- `demo_sprint2.py` → `scripts/demos/demo_sprint2.py`
- `demo_sprint3.py` → `scripts/demos/demo_sprint3.py`
- `add_mcp_to_claude.py` → `scripts/utils/add_mcp_to_claude.py`
- `debug_mcp.py` → `scripts/utils/debug_mcp.py`

**삭제된 파일:**
- `coverage.json` - `.gitignore`에 추가됨

## 참고사항

### 경로 참조 업데이트

파일 이동 후 다음 참조가 업데이트됨:

1. **scripts/test_mcp_server.py**:
   - `run_mcp_server.py` 경로: `Path(__file__).parent.parent / "run_mcp_server.py"`
   - 설정 파일 경로: `Path(__file__).parent.parent / "config" / "examples" / ...`

2. **README.md**:
   - MCP 문서 링크: `docs/mcp/MCP_QUICKSTART.md`
   - 개발 문서 링크: `docs/development/CLAUDE.md`
   - 데모 스크립트 참조: `scripts/demos/`

3. **docs/mcp/MCP_QUICKSTART.md**:
   - 상대 경로 업데이트: `../../README.md`, `../CLI_Reference.md`

### 빌드 및 배포

프로젝트를 빌드/배포할 때는 루트 디렉토리에서:

```bash
python setup.py sdist bdist_wheel
```

### 테스트 실행

모든 테스트 실행:

```bash
pytest
```

특정 카테고리:

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

### MCP 서버 실행

루트 디렉토리에서:

```bash
python run_mcp_server.py
```

또는 테스트:

```bash
python scripts/test_mcp_server.py
```
