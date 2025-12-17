# module/gemini.py
# ---------------------------------------------------
# GitHub Repository: Development-RepositorieRadar
# Author: minjunkim0205, Assadgang
# Description: Gemini API integration with 4 AI features
# Version: 2.0.3 (Enhanced with System Instruction)
# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import json
from google import genai
from google.genai import types

# ---------------------------------------------------
# System Instructions (프롬프트 중앙 관리)
# ---------------------------------------------------
# 각 AI 기능별 시스템 프롬프트 정의
SYSTEM_PROMPTS = {
    # 저장소 구조 분석용 프롬프트
    "repository_analyzer": """You are an expert software architect specializing in code analysis.

Your task:
- Analyze repository structure and identify patterns
- Determine entry points and main files
- Evaluate code organization quality
- Provide clear, actionable insights

You must answer in {language}.""",
    
    # 환경 설정 가이드 생성용 프롬프트
    "environment_guide": """You are a DevOps engineer specializing in development environment setup.

Your task:
- Create step-by-step installation guides
- Identify required dependencies
- Provide configuration instructions
- Include troubleshooting tips

You must answer in {language}.""",
    
    # 코드 흐름 분석용 프롬프트
    "code_flow_analyzer": """You are an expert software engineer specializing in code flow analysis.

Your task:
- Trace execution flow from entry points
- Identify function call chains and dependencies
- Map data flow through the application
- Explain how different modules interact
- Highlight critical paths and bottlenecks

You must answer in {language}.""",
    
    # 이슈 요약용 프롬프트
    "issue_summarizer": """You are a technical project manager specializing in issue analysis.

Your task:
- Summarize issues clearly and concisely
- Categorize issues by type (bug, feature, enhancement)
- Identify priority and severity
- Extract key information (steps to reproduce, expected behavior)
- Provide actionable recommendations

You must answer in {language}."""
}

# ---------------------------------------------------
# Function
# ---------------------------------------------------
def api_check(_key: str) -> bool:
    """
    Gemini API 키 유효성 검사
    
    Args:
        _key: Gemini API 키
    
    Returns:
        bool: API 키가 유효하면 True, 아니면 False
    """
    # API 키 유효성 검사
    if not _key or not isinstance(_key, str):
        return False
    
    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=_key)
        # 테스트 요청 전송
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You must answer in English."
            ),
            contents="ping"
        )
        return True
    except Exception as e:
        return False


def api_repository_structure(_key: str, _file_tree: dict, _language: str = "English") -> str:
    """
    저장소 구조를 AI로 분석
    
    Args:
        _key: Gemini API 키
        _file_tree: 파일 트리 구조 (dict)
        _language: 응답 언어 (기본값: English)
    
    Returns:
        str: 분석 결과 또는 에러 메시지
    """
    # 입력값 검증
    if not _key or not _file_tree:
        return "Error: Invalid input"
    
    # 파일 트리를 JSON 문자열로 변환
    try:
        parsed_file_tree = json.dumps(_file_tree, indent=2, ensure_ascii=False)
    except:
        parsed_file_tree = str(_file_tree)
    
    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=_key)
        
        # 시스템 프롬프트에 언어 설정 적용
        system_instruction = SYSTEM_PROMPTS["repository_analyzer"].format(
            language=_language
        )
        
        # 분석 요청 프롬프트 생성
        prompt = f"""Analyze this repository file tree structure:
```json
{parsed_file_tree}
```

Please provide:
1. **Entry Point**: Main files to start the application
2. **Languages Used**: Primary programming languages
3. **Directory Structure**: Purpose of each directory
4. **Code Organization**: Quality assessment and suggestions
5. **Project Type**: Web app, CLI tool, library, etc."""

        # AI 요청 전송 및 응답 반환
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            ),
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"


def api_environment_setup(_key: str, _file_tree: dict, _readme: str, _language: str = "English") -> str:
    """
    환경 설정 가이드를 AI로 생성
    
    Args:
        _key: Gemini API 키
        _file_tree: 파일 트리 구조
        _readme: README 파일 내용
        _language: 응답 언어
    
    Returns:
        str: 설정 가이드 또는 에러 메시지
    """
    # 입력값 검증
    if not _key or not _file_tree:
        return "Error: Invalid input"
    
    # 파일 트리를 JSON 문자열로 변환
    try:
        parsed_file_tree = json.dumps(_file_tree, indent=2, ensure_ascii=False)
    except:
        parsed_file_tree = str(_file_tree)
    
    # README 없을 시 기본 메시지 설정
    if not _readme:
        _readme = "(No README file found)"
    
    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=_key)
        
        # 시스템 프롬프트에 언어 설정 적용
        system_instruction = SYSTEM_PROMPTS["environment_guide"].format(
            language=_language
        )
        
        # 환경 설정 가이드 생성 프롬프트
        prompt = f"""Based on the following information, create a comprehensive setup guide:

README:
{_readme}

File Structure:
```json
{parsed_file_tree}
```

Please provide:
1. **System Requirements**: OS, software versions
2. **Installation Steps**: Numbered, detailed instructions
3. **Configuration**: Environment variables, config files
4. **Running the Application**: Commands to start
5. **Troubleshooting**: Common issues and solutions"""

        # AI 요청 전송 및 응답 반환
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.5
            ),
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"


def api_code_flow_analysis(_key: str, _file_tree: dict, _source_code: dict = None, _language: str = "English") -> str:
    """
    코드 실행 흐름을 AI로 분석
    
    Args:
        _key: API 키
        _file_tree: 파일 트리 구조
        _source_code: 실제 소스 코드 내용 (선택적)
                     예: {"main.py": "code content...", "utils.py": "..."}
        _language: 응답 언어
    
    Returns:
        str: 코드 흐름 분석 결과
    """
    # 입력값 검증
    if not _key or not _file_tree:
        return "Error: Invalid input"
    
    # 파일 트리를 JSON 문자열로 변환
    try:
        parsed_file_tree = json.dumps(_file_tree, indent=2, ensure_ascii=False)
    except:
        parsed_file_tree = str(_file_tree)
    
    # 소스 코드가 제공된 경우 프롬프트에 추가
    source_info = ""
    if _source_code and isinstance(_source_code, dict):
        source_info = "\n\nSource Code Samples:\n"
        for filename, code in _source_code.items():
            # 각 파일의 첫 1000자만 포함
            source_info += f"\n--- {filename} ---\n{code[:1000]}\n"
    
    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=_key)
        
        # 시스템 프롬프트에 언어 설정 적용
        system_instruction = SYSTEM_PROMPTS["code_flow_analyzer"].format(
            language=_language
        )
        
        # 코드 흐름 분석 프롬프트
        prompt = f"""Analyze the code flow and execution path of this project:

File Structure:
```json
{parsed_file_tree}
```
{source_info}

Please provide:
1. **Execution Flow**: Step-by-step execution path from entry point
2. **Module Dependencies**: How modules depend on each other
3. **Data Flow**: How data moves through the application
4. **Key Functions**: Important functions and their roles
5. **Interaction Diagram**: Describe how components interact
6. **Critical Paths**: Performance bottlenecks or important execution paths
7. **Recommendations**: Suggestions for improving code flow"""

        # AI 요청 전송 및 응답 반환
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6
            ),
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"


def api_issue_summary(_key: str, _issues: list, _language: str = "English") -> str:
    """
    이슈 목록을 AI로 요약 및 분석
    
    Args:
        _key: API 키
        _issues: 이슈 목록
                예: [
                    {"title": "Bug: Login fails", "description": "...", "labels": ["bug"]},
                    {"title": "Feature: Add dark mode", "description": "...", "labels": ["enhancement"]}
                ]
        _language: 응답 언어
    
    Returns:
        str: 이슈 요약 및 분석 결과
    """
    # 입력값 검증
    if not _key or not _issues:
        return "Error: Invalid input"
    
    # 이슈 목록을 JSON 문자열로 변환
    try:
        parsed_issues = json.dumps(_issues, indent=2, ensure_ascii=False)
    except:
        parsed_issues = str(_issues)
    
    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=_key)
        
        # 시스템 프롬프트에 언어 설정 적용
        system_instruction = SYSTEM_PROMPTS["issue_summarizer"].format(
            language=_language
        )
        
        # 이슈 분석 프롬프트
        prompt = f"""Analyze and summarize the following project issues:
```json
{parsed_issues}
```

Please provide:
1. **Overall Summary**: High-level overview of all issues
2. **Categorization**: Group by type (bugs, features, enhancements, etc.)
3. **Priority Analysis**: Identify high-priority issues
4. **Common Themes**: Recurring patterns or related issues
5. **Statistics**: Count of each issue type
6. **Action Items**: Recommended next steps
7. **Critical Issues**: Issues that need immediate attention

Format the response in a clear, structured way."""

        # AI 요청 전송 및 응답 반환
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.5
            ),
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"
