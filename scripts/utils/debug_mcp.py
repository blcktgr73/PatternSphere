"""
MCP 서버 디버깅 스크립트 - stderr로 로그 출력
"""

import sys
import json
import logging
import traceback

# stderr로 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

try:
    logger.info("=== MCP Server Debug Start ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Working directory: {sys.path}")

    # PatternSphere 임포트 시도
    logger.info("Attempting to import patternsphere.mcp.server...")
    from patternsphere.mcp.server import PatternSphereMCPServer
    logger.info("Import successful!")

    # 서버 초기화
    logger.info("Initializing server...")
    server = PatternSphereMCPServer()
    logger.info("Server initialized successfully!")

    # 도구 확인
    tools = server.get_tools()
    logger.info(f"Tools registered: {len(tools)}")
    for tool in tools:
        logger.info(f"  - {tool['name']}")

    # 서버 실행
    logger.info("Starting server main loop...")
    server.run()

except Exception as e:
    logger.error(f"Error occurred: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)
