"""
PatternSphere MCP Server 테스트 스크립트

MCP 서버의 초기화, 프로토콜 통신, 도구 호출을 테스트합니다.
"""

import json
import subprocess
import sys
import io
from pathlib import Path

# Windows 콘솔 인코딩 문제 해결
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_1_server_initialization():
    """테스트 1: MCP 서버 초기화 테스트"""
    print("\n" + "="*60)
    print("테스트 1: MCP 서버 초기화")
    print("="*60)

    try:
        from patternsphere.mcp.server import PatternSphereMCPServer

        server = PatternSphereMCPServer()
        tools = server.get_tools()

        print(f"[OK] 서버 초기화 성공")
        print(f"[OK] 등록된 도구 개수: {len(tools)}")
        print(f"\n등록된 도구 목록:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

        return True

    except Exception as e:
        print(f"[FAIL] 서버 초기화 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_2_tool_calls():
    """테스트 2: 도구 호출 테스트"""
    print("\n" + "="*60)
    print("테스트 2: 도구 호출 테스트")
    print("="*60)

    try:
        from patternsphere.mcp.server import PatternSphereMCPServer

        server = PatternSphereMCPServer()

        # 테스트 케이스들
        test_cases = [
            {
                "name": "list_categories",
                "tool": "list_categories",
                "args": {}
            },
            {
                "name": "search_patterns",
                "tool": "search_patterns",
                "args": {"query": "refactoring", "limit": 3}
            },
            {
                "name": "get_pattern",
                "tool": "get_pattern",
                "args": {"pattern_name": "Read all the Code in One Hour"}
            },
            {
                "name": "list_patterns",
                "tool": "list_patterns",
                "args": {}
            },
            {
                "name": "get_pattern_recommendations",
                "tool": "get_pattern_recommendations",
                "args": {"problem": "understand legacy code", "limit": 3}
            }
        ]

        results = []
        for test_case in test_cases:
            print(f"\n테스트: {test_case['name']}")
            print(f"  도구: {test_case['tool']}")
            print(f"  인자: {test_case['args']}")

            result = server.handle_tool_call(test_case['tool'], test_case['args'])

            if result.get("success"):
                print(f"  [OK] 성공")
                if "count" in result:
                    print(f"    결과 개수: {result['count']}")
                if "results" in result:
                    print(f"    첫 번째 결과: {result['results'][0]['name'] if result['results'] else 'N/A'}")
                if "pattern" in result:
                    print(f"    패턴명: {result['pattern']['name']}")
                if "recommendations" in result:
                    print(f"    추천 패턴: {[r['name'] for r in result['recommendations'][:2]]}")
                results.append(True)
            else:
                print(f"  [FAIL] 실패: {result.get('error')}")
                results.append(False)

        success_rate = sum(results) / len(results) * 100
        print(f"\n성공률: {success_rate:.1f}% ({sum(results)}/{len(results)})")

        return all(results)

    except Exception as e:
        print(f"[FAIL] 도구 호출 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_protocol_simulation():
    """테스트 3: MCP 프로토콜 통신 시뮬레이션"""
    print("\n" + "="*60)
    print("테스트 3: MCP 프로토콜 통신 시뮬레이션")
    print("="*60)

    try:
        # MCP 서버 프로세스 시작
        python_exe = sys.executable
        # 스크립트가 scripts/ 폴더에 있으므로 상위 디렉토리의 run_mcp_server.py를 참조
        server_script = Path(__file__).parent.parent / "run_mcp_server.py"

        print(f"서버 실행: {python_exe} {server_script}")

        process = subprocess.Popen(
            [python_exe, str(server_script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # 초기화 메시지 읽기
        init_line = process.stdout.readline()
        print(f"\n초기화 응답:")
        init_response = json.loads(init_line)
        print(json.dumps(init_response, indent=2, ensure_ascii=False))

        if init_response.get("method") == "initialize":
            print("[OK] 초기화 성공")
            tools = init_response.get("params", {}).get("capabilities", {}).get("tools", [])
            print(f"[OK] 도구 개수: {len(tools)}")

        # 테스트 요청 전송
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "search_patterns",
                "arguments": {
                    "query": "refactoring",
                    "limit": 2
                }
            }
        }

        print(f"\n테스트 요청 전송:")
        print(json.dumps(test_request, indent=2, ensure_ascii=False))

        process.stdin.write(json.dumps(test_request) + "\n")
        process.stdin.flush()

        # 응답 읽기
        response_line = process.stdout.readline()
        print(f"\n응답 수신:")
        response = json.loads(response_line)
        print(json.dumps(response, indent=2, ensure_ascii=False))

        # 프로세스 종료
        process.terminate()
        process.wait(timeout=5)

        if response.get("result"):
            print("\n[OK] 프로토콜 통신 성공")
            return True
        else:
            print("\n[FAIL] 프로토콜 통신 실패")
            return False

    except Exception as e:
        print(f"[FAIL] 프로토콜 시뮬레이션 실패: {e}")
        import traceback
        traceback.print_exc()
        if 'process' in locals():
            process.terminate()
        return False


def test_4_claude_desktop_config():
    """테스트 4: Claude Desktop 설정 검증"""
    print("\n" + "="*60)
    print("테스트 4: Claude Desktop 설정 검증")
    print("="*60)

    try:
        # 설정 파일이 config/examples/ 폴더로 이동됨
        config_file = Path(__file__).parent.parent / "config" / "examples" / "claude_desktop_config.example.json"

        if not config_file.exists():
            print(f"[FAIL] 설정 파일 없음: {config_file}")
            return False

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print(f"[OK] 설정 파일 로드 성공")

        # 설정 검증
        if "mcpServers" not in config:
            print("[FAIL] mcpServers 키가 없습니다")
            return False

        if "patternsphere" not in config["mcpServers"]:
            print("[FAIL] patternsphere 서버 설정이 없습니다")
            return False

        ps_config = config["mcpServers"]["patternsphere"]

        # 경로 검증
        python_exe = Path(ps_config.get("command", ""))
        server_script = Path(ps_config.get("args", [""])[0])

        print(f"\n설정 검증:")
        print(f"  Python 실행 파일: {python_exe}")
        print(f"    존재 여부: {python_exe.exists()}")

        print(f"  서버 스크립트: {server_script}")
        print(f"    존재 여부: {server_script.exists()}")

        env_vars = ps_config.get("env", {})
        print(f"\n  환경 변수:")
        for key, value in env_vars.items():
            path_value = Path(value)
            print(f"    {key}: {value}")
            if "PATH" in key or "DIR" in key:
                print(f"      존재 여부: {path_value.exists()}")

        # 실제 실행 가능 여부 테스트
        print(f"\n실행 테스트:")
        result = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"  [OK] Python 실행 성공: {result.stdout.strip()}")
        else:
            print(f"  [FAIL] Python 실행 실패")
            return False

        # 서버 스크립트 문법 체크
        result = subprocess.run(
            [str(python_exe), "-m", "py_compile", str(server_script)],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"  [OK] 서버 스크립트 문법 검증 성공")
        else:
            print(f"  [FAIL] 서버 스크립트 문법 오류: {result.stderr}")
            return False

        print("\n[OK] Claude Desktop 설정 검증 완료")
        print("\n[NOTE] Claude Desktop에서 사용하려면:")
        print(f"   1. Claude Desktop 설정 파일 위치로 이동")
        print(f"   2. {config_file.name}의 내용을 복사")
        print(f"   3. Claude Desktop 재시작")

        return True

    except Exception as e:
        print(f"[FAIL] 설정 검증 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """모든 테스트 실행"""
    print("\n" + "="*60)
    print("PatternSphere MCP Server 테스트 스위트")
    print("="*60)

    tests = [
        ("서버 초기화", test_1_server_initialization),
        ("도구 호출", test_2_tool_calls),
        ("프로토콜 통신", test_3_protocol_simulation),
        ("Claude Desktop 설정", test_4_claude_desktop_config),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n테스트 '{test_name}' 예외 발생: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False

    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)

    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())
    success_rate = (passed / total * 100) if total > 0 else 0

    print(f"\n전체 성공률: {success_rate:.1f}% ({passed}/{total})")

    if success_rate == 100:
        print("\n[SUCCESS] 모든 테스트 통과! MCP 서버가 정상 작동합니다.")
    elif success_rate >= 75:
        print("\n[WARNING] 대부분의 테스트 통과. 일부 문제 확인 필요.")
    else:
        print("\n[ERROR] 여러 테스트 실패. 서버 설정 점검 필요.")

    return success_rate == 100


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
