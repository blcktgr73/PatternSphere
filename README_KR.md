# PatternSphere

> **Note**: English version available: [README.md](README.md)

> 소프트웨어 디자인 패턴을 위한 통합 지식 베이스

**Version 1.0.0** - Production Ready

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-248%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)]()

## 개요

PatternSphere는 소프트웨어 디자인 패턴을 검색하고 탐색하기 위한 강력한 커맨드라인 도구입니다. Phase 1은 8개 카테고리에 걸친 61개의 포괄적인 패턴을 포함하는 **객체지향 리엔지니어링 패턴(OORP)**에 초점을 맞추고 있습니다.

### 주요 기능

- **빠른 키워드 검색**: 관련성 높은 결과를 위한 가중치 필드 스코어링 (<10ms)
- **카테고리 브라우징**: 8개 OORP 카테고리별 패턴 탐색
- **태그 필터링**: OR 로직을 사용한 다중 태그 필터링
- **풍부한 터미널 UI**: 아름다운 테이블과 포맷된 출력
- **패턴 세부정보**: 완전한 패턴 정보 (문제, 해결책, 결과)
- **연관 패턴**: 패턴 간 연결 발견
- **61개 OORP 패턴**: 객체지향 리엔지니어링 패턴의 완전한 커버리지
- **MCP 통합**: AI 지원 패턴 발견을 위한 Claude Code의 MCP 서버로 사용

## 빠른 시작

### 설치

```bash
# 저장소 클론 또는 압축 해제
cd PatternSphere

# 의존성 설치
pip install -r requirements.txt

# 패키지 설치
pip install -e .
```

### 설치 확인

```bash
patternsphere --version
# 출력: PatternSphere v1.0.0
```

### 첫 명령어들

```bash
# 시스템 정보 확인
patternsphere info

# 모든 카테고리 나열
patternsphere categories

# 패턴 검색
patternsphere search refactoring

# 패턴 세부정보 보기
patternsphere view "Read all the Code in One Hour"

# 카테고리별 패턴 나열
patternsphere list --category "First Contact"
```

### MCP 통합 (Claude Code)

PatternSphere는 Claude Code에서 MCP (Model Context Protocol) 서버로 사용할 수 있습니다:

```bash
# 1. 위의 설치 과정 완료
# 2. Claude Code 설정
# 3. Claude Code에서 사용:
#    "레거시 코드 리팩토링을 위한 패턴 찾아줘"
#    "'Read all the Code in One Hour' 패턴 보여줘"
```

**📖 설정 방법은 [MCP Quick Start](docs/mcp/MCP_QUICKSTART_KR.md)를 참조하세요.**

## 사용법

### 패턴 검색

가중치 스코어링을 사용한 모든 패턴 필드 검색:

```bash
# 단순 검색
patternsphere search refactoring

# 카테고리 필터를 사용한 검색
patternsphere search "code quality" --category "First Contact"

# 태그 필터를 사용한 검색
patternsphere search testing --tags "quality,testing"

# 결과 개수 제한
patternsphere search pattern --limit 10

# 관련성 점수 숨기기
patternsphere search code --no-scores
```

**검색 알고리즘:**
- 가중치 필드 스코어링 (name: 5.0, tags: 4.0, intent: 3.0, 등)
- 정확한 단어 일치: 1.0점, 부분 일치: 0.5점
- 관련성 순으로 결과 정렬

### 패턴 나열

필터링과 정렬을 사용한 모든 패턴 브라우징:

```bash
# 모든 패턴 나열
patternsphere list

# 카테고리별 나열
patternsphere list --category "First Contact"

# 카테고리별 정렬
patternsphere list --sort category
```

### 패턴 세부정보 보기

완전한 패턴 정보 표시:

```bash
# 이름으로 보기
patternsphere view "Read all the Code in One Hour"

# ID로 보기
patternsphere view OORP-001
```

표시 내용:
- 메타데이터 (ID, 카테고리, 태그, 출처)
- 의도
- 문제
- 해결책
- 결과
- 연관 패턴

### 카테고리 탐색

사용 가능한 카테고리 탐색:

```bash
patternsphere categories
```

패턴 개수와 함께 모든 8개 OORP 카테고리 표시:
- Detailed Model Capture (10개 패턴)
- First Contact (6개 패턴)
- Initial Understanding (6개 패턴)
- Migration Strategies (8개 패턴)
- Redistribute Responsibilities (10개 패턴)
- Setting Direction (10개 패턴)
- Tests: Your Life Insurance! (6개 패턴)
- Transform Conditionals to Polymorphism (5개 패턴)

### 시스템 정보

애플리케이션 정보와 통계 표시:

```bash
patternsphere info
```

표시 내용:
- 버전 정보
- 전체 패턴 및 카테고리 개수
- 로딩 성능
- 데이터 소스 정보

## 패턴 카테고리

### 1. First Contact (6개 패턴)

낯선 코드베이스의 초기 탐색.

**주요 패턴:**
- Read all the Code in One Hour
- Skim the Documentation
- Interview During Demo
- Do a Mock Installation
- Chat with the Maintainers

**사용 시기:**
- 새 프로젝트 작업 시작
- 레거시 시스템 온보딩
- 초기 평가 수행

### 2. Initial Understanding (6개 패턴)

시스템 구조에 대한 깊은 이해 구축.

**주요 패턴:**
- Analyze the Persistent Data
- Study the Exceptional Entities
- Refactor to Understand
- Speculate about Business Rules
- Look for the Contracts
- Record Business Rules as Tests

**사용 시기:**
- 데이터 모델 이해 필요
- 시스템 아키텍처 조사
- 리팩토링 계획 수립

### 3. Detailed Model Capture (10개 패턴)

시스템의 상세 모델 캡처.

**주요 패턴:**
- Learn from the Past
- Visualize Code as Dotplots
- Speculate about Design
- Interview During Demo
- Read all the Code in One Hour

**사용 시기:**
- 문서 작성
- 아키텍처 역공학
- 주요 변경 계획

### 4. Redistribute Responsibilities (10개 패턴)

클래스 및 모듈 디자인 개선.

**주요 패턴:**
- Split Up God Class
- Move Behavior Close to Data
- Extract Method Object
- Eliminate Navigation Code
- Encapsulate Field

**사용 시기:**
- 대형 클래스 리팩토링
- 응집도 향상
- 결합도 감소

### 5. Transform Conditionals to Polymorphism (5개 패턴)

조건문을 다형성 디자인으로 대체.

**주요 패턴:**
- Replace Conditional with Polymorphism
- Introduce Null Object
- Factor out State
- Factor out Strategy

**사용 시기:**
- 복잡한 조건문 단순화
- Strategy 패턴 구현
- 확장성 향상

### 6. Migration Strategies (8개 패턴)

레거시 시스템 마이그레이션 전략.

**주요 패턴:**
- Always Have a Running Version
- Migrate Systems Incrementally
- Present the Right Interface
- Distinguish Public from Published Interface
- Deprecate Obsolete Interfaces

**사용 시기:**
- 시스템 마이그레이션 계획
- 레거시 코드 현대화
- 기술 부채 관리

### 7. Setting Direction (10개 패턴)

리엔지니어링 프로젝트를 위한 전략 패턴.

**주요 패턴:**
- Appoint a Navigator
- Build Confidence
- Most Valuable First
- Repair What's Broken First
- If It Ain't Broke, Don't Fix It

**사용 시기:**
- 리엔지니어링 프로젝트 시작
- 이해관계자 관리
- 우선순위 계획

### 8. Tests: Your Life Insurance! (6개 패턴)

레거시 시스템을 위한 테스팅 전략.

**주요 패턴:**
- Write Tests to Enable Evolution
- Write Tests to Understand
- Test Fuzzy Features
- Retest Persistent Problems
- Test the Interface, Not the Implementation

**사용 시기:**
- 테스트되지 않은 코드 작업
- 테스트 커버리지 추가
- 안전한 리팩토링 활성화

## 일반적인 워크플로우

### 1. 새로운 코드베이스 탐색

```bash
# First Contact 패턴으로 시작
patternsphere list --category "First Contact"

# 주요 패턴 보기
patternsphere view "Read all the Code in One Hour"
patternsphere view "Interview During Demo"

# 특정 기술 검색
patternsphere search documentation --category "First Contact"
```

### 2. 리팩토링 계획

```bash
# 리팩토링 패턴 찾기
patternsphere search refactoring --limit 15

# 책임 재분배 탐색
patternsphere list --category "Redistribute Responsibilities"

# 특정 리팩토링 패턴 보기
patternsphere view "Split Up God Class"
patternsphere view "Move Behavior Close to Data"
```

### 3. 레거시 코드에 테스트 추가

```bash
# 테스팅 패턴 찾기
patternsphere search test --tags "testing,quality"

# 테스팅 카테고리 보기
patternsphere list --category "Tests: Your Life Insurance!"

# 특정 기술 학습
patternsphere view "Write Tests to Enable Evolution"
patternsphere view "Test Fuzzy Features"
```

### 4. 패턴 발견

```bash
# 카테고리별 탐색
patternsphere categories

# 카테고리별로 정렬된 모든 패턴 나열
patternsphere list --sort category

# 광범위한 주제 검색
patternsphere search "code quality"

# 연관 패턴 탐색 (view 출력에 표시됨)
```

## 아키텍처

### 컴포넌트 개요

```
PatternSphere
├── Models (Pydantic 검증을 사용한 패턴 데이터 모델)
├── Repository (O(1) 조회를 사용한 패턴 저장소)
├── Search Engine (가중치 키워드 검색)
├── Loaders (OORP 패턴 로더)
├── Storage (원자적 쓰기를 사용한 파일 기반 영속성)
├── CLI (커맨드라인 인터페이스)
│   ├── Commands (5개 주요 명령어)
│   ├── Formatters (출력 포맷팅)
│   └── AppContext (의존성 주입)
└── Config (설정 및 구성)
```

### 디자인 원칙

PatternSphere는 **SOLID 원칙**과 클린 아키텍처를 따라 구축되었습니다:

**Single Responsibility (단일 책임)**
- 각 컴포넌트는 하나의 명확한 목적을 가짐
- Pattern 모델: 데이터 구조와 검증만
- Repository: 컬렉션 관리와 쿼리
- Storage: 파일 I/O 작업만
- Formatter는 포맷만, 검색은 검색만

**Open/Closed (개방/폐쇄)**
- 새로운 패턴 소스에 대한 확장 가능 (PDF, 웹 등)
- 데코레이터를 통해 새 명령어 쉽게 추가
- IStorage 인터페이스가 새로운 저장소 백엔드 허용
- IPatternRepository가 대체 구현 허용

**Liskov Substitution (리스코프 치환)**
- Repository 인터페이스가 다중 구현 가능
- 모든 IStorage 구현이 상호 교환 가능
- 향후 저장소 백엔드 가능 (SQLite, PostgreSQL)

**Interface Segregation (인터페이스 분리)**
- 집중된 인터페이스 (IPatternRepository, IStorage)
- 비대한 인터페이스 없음
- IStorage는 최소한의 집중된 인터페이스

**Dependency Inversion (의존성 역전)**
- 컴포넌트는 추상화에 의존
- AppContext가 모든 의존성 관리
- Repository는 IStorage 추상화에 의존
- 목(mock) 저장소로 테스팅 가능

### 주요 디자인 패턴

**Repository Pattern (저장소 패턴)**
- 패턴 데이터 접근 추상화
- `IPatternRepository` 인터페이스
- `InMemoryPatternRepository` 구현
- 다중 인덱스를 사용한 컬렉션 유사 인터페이스

**Singleton Pattern (싱글톤 패턴)**
- `AppContext`가 애플리케이션 상태 관리
- CLI 세션 전체에서 단일 인스턴스

**Strategy Pattern (전략 패턴)**
- 가중치 검색 스코어링 알고리즘
- 새로운 스코어링 전략에 대한 확장 가능

**Dependency Injection (의존성 주입)**
- 컴포넌트는 생성자를 통해 의존성 받음
- 테스트 가능하고 유지보수 가능
- 전역 상태 없음

## 성능

PatternSphere는 속도에 최적화되어 있습니다:

| 작업 | 성능 | 요구사항 | 결과 |
|------|------|----------|------|
| 패턴 로딩 | ~2ms | <500ms | 250배 빠름 ✅ |
| 검색 (평균) | <10ms | <100ms | 10배 빠름 ✅ |
| CLI 시작 | ~650ms | <1s | 35% 빠름 ✅ |
| 메모리 사용 | <100KB | 최소화 | 우수 ✅ |

**모든 요구사항을 10-250배 초과 달성!**

## 테스팅

포괄적인 테스트 스위트가 신뢰성을 보장합니다:

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=patternsphere --cov-report=html

# 특정 테스트 타입 실행
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

**테스트 통계:**
- **전체 테스트**: 248개
- **테스트 커버리지**: 91%
- **모든 테스트**: 통과 ✅
- **실행 시간**: ~1.6초

**테스트 카테고리:**
- 단위 테스트 (178) - 모델, 저장소, 저장, 검색, 로더, CLI
- 통합 테스트 (55) - 검색 플로우, CLI 명령어, 엔드투엔드 워크플로우
- 성능 테스트 (15) - 로딩, 검색, 확장성

**커버리지 분석:**
- 패턴 모델: 100%
- Repository: 97%
- 검색 엔진: 97%
- Loaders: 92%
- CLI 컴포넌트: 86-100%
- 전체: 91%

## 설정

### 환경 변수

환경 변수를 통한 PatternSphere 설정:

```bash
export PATTERNSPHERE_DATA_DIR=/custom/data/path
export PATTERNSPHERE_DEFAULT_LIMIT=50
export PATTERNSPHERE_TERMINAL_WIDTH=100
```

**사용 가능한 변수:**
- `PATTERNSPHERE_DATA_DIR`: 데이터 디렉토리 경로
- `PATTERNSPHERE_DEFAULT_LIMIT`: 기본 검색 결과 제한
- `PATTERNSPHERE_TERMINAL_WIDTH`: 포맷팅을 위한 터미널 너비

### 설정 파일

프로젝트 루트에 `.env` 파일 생성:

```env
PATTERNSPHERE_DATA_DIR=data
PATTERNSPHERE_DEFAULT_LIMIT=20
PATTERNSPHERE_TERMINAL_WIDTH=80
```

## 프로젝트 구조

```
PatternSphere/
├── patternsphere/          # 메인 패키지
│   ├── models/            # 패턴 데이터 모델 (Pydantic)
│   ├── repository/        # Repository 패턴 구현
│   ├── storage/           # 파일 저장소
│   ├── search/            # 검색 엔진
│   ├── loaders/           # 패턴 로더
│   ├── config/            # 설정
│   ├── cli/               # CLI 인터페이스
│   └── mcp/               # MCP 서버 구현
├── data/                  # 패턴 데이터
│   └── sources/oorp/      # OORP 패턴 (61개)
├── tests/                 # 테스트 스위트 (248개)
│   ├── unit/             # 단위 테스트 (178)
│   ├── integration/      # 통합 테스트 (55)
│   └── performance/      # 성능 테스트 (15)
├── docs/                  # 문서
│   ├── mcp/              # MCP 서버 문서
│   │   ├── MCP_QUICKSTART_KR.md
│   │   └── MCP_TEST_GUIDE_KR.md
│   ├── development/      # 개발 가이드
│   │   ├── CLAUDE.md
│   │   └── PATTERN_ANALYSIS_KR.md
│   ├── CLI_Reference.md
│   ├── PRD.md
│   └── Phase1_Product_Specification.md
├── config/                # 설정 파일
│   └── examples/         # 예제 설정
├── scripts/               # 유틸리티 스크립트
│   ├── test_mcp_server.py
│   ├── demos/            # 데모 스크립트
│   └── utils/            # 유틸리티 스크립트
├── README_KR.md          # 이 파일
├── README.md             # 영문 버전
├── CHANGELOG.md          # 버전 히스토리
├── requirements.txt      # 의존성
├── setup.py              # 패키지 설정
└── run_mcp_server.py     # MCP 서버 진입점
```

## 문서

### 사용자 문서
- **[CLI Reference](docs/CLI_Reference.md)**: 예제와 함께 완전한 명령어 참조
- **[MCP Quick Start](docs/mcp/MCP_QUICKSTART_KR.md)**: MCP 서버 설정 및 사용법 ([English](docs/mcp/MCP_QUICKSTART.md))
- **[MCP Test Guide](docs/mcp/MCP_TEST_GUIDE_KR.md)**: MCP 서버 테스팅 및 문제 해결 ([English](docs/mcp/MCP_TEST_GUIDE.md))
- **[File Structure](docs/FILE_STRUCTURE_KR.md)**: 프로젝트 구조 및 파일 참조 ([English](docs/FILE_STRUCTURE.md))

### 개발 문서
- **[Development Guide](CLAUDE.md)**: AI 페어 프로그래밍 및 변환 패턴 ([English](docs/development/CLAUDE_EN.md))
- **[Pattern Analysis](docs/development/PATTERN_ANALYSIS_KR.md)**: 프로젝트 패턴 분석 및 권장사항 ([English](docs/development/PATTERN_ANALYSIS.md))
- **[Organization Summary](docs/ORGANIZATION_SUMMARY_KR.md)**: 프로젝트 재구성 세부사항 ([English](docs/ORGANIZATION_SUMMARY.md))
- **[CHANGELOG](docs/CHANGELOG.md)**: 버전 히스토리 및 변경사항
- **[PRD](docs/PRD.md)**: 제품 요구사항 (Phase 2 PDF 지원 포함)
- **[Product Spec](docs/Phase1_Product_Specification.md)**: Phase 1 명세
- **Sprint Reports**: SPRINT1_COMPLETE.md, SPRINT2_COMPLETE.md, SPRINT3_COMPLETE.md

## 개발

### 개발 환경 설정

```bash
# 저장소 클론
cd PatternSphere

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발 모드로 설치
pip install -e .

# 테스트 실행
pytest
```

### 코드 품질

```bash
# 코드 포맷
black patternsphere/

# 타입 체킹
mypy patternsphere/

# 린팅
flake8 patternsphere/
```

### 테스트 실행

```bash
# 모든 테스트
pytest

# 커버리지와 함께
pytest --cov=patternsphere

# 특정 테스트 파일
pytest tests/unit/test_search_engine.py

# 성능 테스트
pytest tests/performance/ -v

# 통합 테스트
pytest tests/integration/ -v
```

### 프로젝트 통계

| 메트릭 | 값 |
|--------|-----|
| 전체 소스 라인 | 2,638 |
| 전체 테스트 라인 | 4,037 |
| 테스트/코드 비율 | 1.53:1 |
| 전체 패턴 | 61 |
| 카테고리 | 8 |
| 명령어 | 5 |
| 테스트 커버리지 | 91% |

## 요구사항

**런타임:**
- **Python**: 3.9 이상
- **의존성**:
  - pydantic >= 2.0.0 (데이터 검증)
  - pydantic-settings >= 2.0.0 (설정)
  - pyyaml >= 6.0 (YAML 지원)
  - typer >= 0.9.0 (CLI 프레임워크)
  - rich >= 13.0.0 (터미널 포맷팅)

**개발:**
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- mypy >= 1.5.0
- flake8 >= 6.1.0

## 로드맵

### Phase 1 (완료) ✅
- OORP 패턴 로딩
- 가중치 스코어링을 사용한 키워드 검색
- 5개 명령어를 가진 CLI 인터페이스
- 포괄적인 태그를 가진 61개 OORP 패턴
- 원자적 쓰기를 사용한 파일 기반 저장소
- 248개의 포괄적인 테스트
- 완전한 문서

### Phase 2 (미래 - PRD에 계획됨)
- **PDF 통합**:
  - PDF 패턴 추출
  - Gang of Four (GoF) 패턴
  - Enterprise Integration Patterns
  - Pattern-Oriented Software Architecture (POSA)
  - 수동 패턴 정의 워크플로우
  - PDF 페이지 링킹

- **다중 소스 아키텍처**:
  - 지식 소스 추상화 레이어
  - 소스 플러그인 아키텍처
  - 충돌 해결
  - 다중 소스 동시 사용

### Phase 3 (미래)
- 임베딩을 사용한 시맨틱 검색
- 패턴 관계 시각화
- 웹 인터페이스
- 코드 분석 기반 패턴 추천
- 코드 예제 통합

### Phase 4 (미래)
- 사용자 기여 패턴
- 패턴 비교 도구
- 다양한 포맷으로 내보내기
- IDE 플러그인
- 협업 패턴 큐레이션

## 기여

PatternSphere는 확장성을 위해 설계되었습니다:

**새로운 패턴 소스 추가:**
1. `patternsphere/loaders/`에 로더 생성
2. `OORPLoader` 구조를 따라 로더 구현
3. `data/sources/<source-name>/`에 패턴 추가
4. 설정에 소스 등록

**새로운 명령어 추가:**
1. `patternsphere/cli/commands.py`에 명령어 함수 추가
2. `@app.command()` 데코레이터 사용
3. 기존 명령어 패턴 따르기
4. `tests/integration/test_cli.py`에 테스트 추가

**테스트 추가:**
- 단위 테스트: `tests/unit/`
- 통합 테스트: `tests/integration/`
- 성능 테스트: `tests/performance/`
- 기존 테스트 구조 따르기

## 라이선스

MIT License - 자세한 내용은 LICENSE 파일 참조

## 감사의 글

**패턴 출처:**
- **OORP**: Object-Oriented Reengineering Patterns by Serge Demeyer, Stéphane Ducasse, and Oscar Nierstrasz (2003)

**기술:**
- [Typer](https://typer.tiangolo.com/) - 현대적인 CLI 프레임워크
- [Rich](https://rich.readthedocs.io/) - 아름다운 터미널 UI
- [Pydantic](https://docs.pydantic.dev/) - 데이터 검증
- [pytest](https://pytest.org/) - 테스팅 프레임워크

## 지원

**도움말:**
```bash
# 메인 도움말
patternsphere --help

# 명령어 도움말
patternsphere search --help

# 시스템 정보
patternsphere info
```

**문서:**
- 자세한 명령어 도움말은 [CLI Reference](docs/CLI_Reference.md) 확인
- `tests/` 디렉토리의 테스트 예제 검토
- `scripts/demos/`의 데모 스크립트 참조: demo_sprint1.py, demo_sprint2.py, demo_sprint3.py

---

**PatternSphere v1.0.0**
*소프트웨어 디자인 패턴을 위한 통합 지식 베이스*

SOLID 원칙과 클린 아키텍처를 따라 ❤️로 구축되었습니다.
