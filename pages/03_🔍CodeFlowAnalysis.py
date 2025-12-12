# pages/03_🔍CodeFlowAnalysis.py
# ---------------------------------------------------
# 모듈 임포트
# ---------------------------------------------------
import streamlit as st
import json
import requests
from pathlib import Path
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="Code Flow Analysis",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------------------
# 세션 상태 불러오기
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# 사이드바 (API, URL 입력)
# ---------------------------------------------------
st.sidebar.title("Input")
api_key = st.sidebar.text_input(
    "🔑 GPT/Gemini API token", 
    value=options.get("api_key", ""), 
    type="password", 
    disabled=True,
    help="Set in Home page"
)
repository_url = st.sidebar.text_input(
    "📊 Github Repository URL", 
    value=options.get("repository_url", ""), 
    disabled=True,
    help="Set in Home page"
)

# 언어 선택
language = st.sidebar.selectbox(
    "Response Language",
    ["English", "Korean"],
    index=1 if options.get("language") == "Korean" else 0
)

st.sidebar.divider()

# 레포지토리 정보 표시
if repository_url:
    try:
        owner, repo = repository_url.replace("https://github.com/", "").split("/")[:2]
        st.sidebar.success(f"✅ Repository: `{owner}/{repo}`")
    except:
        st.sidebar.error("❌ Invalid URL format")

# ---------------------------------------------------
# 헬퍼 함수들
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    """GitHub URL에서 owner와 repo 추출"""
    if not url:
        return None
    try:
        parts = url.replace("https://github.com/", "").split("/")
        return {
            "owner": parts[0],
            "repo": parts[1]
        }
    except:
        return None


def fetch_repository_tree(owner: str, repo: str, branch: str = "main") -> dict:
    """GitHub API로 저장소의 파일 트리 가져오기"""
    # GitHub API 엔드포인트
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    
    try:
        response = requests.get(url, timeout=15)
        
        # main 브랜치 실패 시 master 시도
        if response.status_code in [401, 404]:
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        # 파일 트리를 계층 구조로 변환
        tree = {}
        
        for item in data.get("tree", []):
            path = item["path"]
            item_type = item["type"]
            
            # 불필요한 파일/폴더 필터링
            ignore_patterns = ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 
                             '.idea', '.vscode', 'dist', 'build', '.DS_Store']
            
            if any(ignore in path for ignore in ignore_patterns):
                continue
            
            # 경로를 계층 구조로 변환
            parts = path.split("/")
            current = tree
            
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # 파일 또는 디렉토리 추가
                    if item_type == "blob":
                        current[part] = {
                            "type": "file",
                            "size": item.get("size", 0),
                            "extension": Path(part).suffix,
                            "path": path
                        }
                    else:
                        if part not in current:
                            current[part] = {
                                "type": "directory",
                                "contents": {}
                            }
                else:
                    # 중간 디렉토리 생성
                    if part not in current:
                        current[part] = {
                            "type": "directory",
                            "contents": {}
                        }
                    current = current[part].get("contents", current[part])
        
        return tree
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ GitHub API Error: {str(e)}")
        return {}


def fetch_file_content(owner: str, repo: str, file_path: str, branch: str = "main") -> str:
    """GitHub API로 특정 파일의 내용 가져오기"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # main 브랜치 실패 시 master 시도
        if response.status_code in [401, 404]:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref=master"
            response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        data = response.json()
        
        # Base64 디코딩하여 파일 내용 반환
        import base64
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content
    
    except Exception as e:
        return f"# Error fetching file: {str(e)}"


def find_source_files(tree: dict, extensions: list, current_path: str = "") -> list:
    """파일 트리에서 특정 확장자의 파일 경로 찾기"""
    files = []
    
    for name, value in tree.items():
        if isinstance(value, dict):
            if value.get("type") == "file":
                # 확장자 매칭 확인
                if any(name.endswith(ext) for ext in extensions):
                    full_path = f"{current_path}/{name}" if current_path else name
                    files.append((name, value.get("path", full_path)))
            
            elif value.get("type") == "directory":
                # 하위 디렉토리 재귀 탐색
                sub_path = f"{current_path}/{name}" if current_path else name
                files.extend(find_source_files(value.get("contents", {}), extensions, sub_path))
    
    return files


def count_files(tree: dict) -> int:
    """파일 트리의 총 파일 개수 계산"""
    count = 0
    for key, value in tree.items():
        if isinstance(value, dict):
            if value.get("type") == "file":
                count += 1
            elif value.get("type") == "directory":
                count += count_files(value.get("contents", {}))
    return count


# ---------------------------------------------------
# 사전 조건 확인
# ---------------------------------------------------
if not (options.get("api_key") and options.get("repository_url")):
    st.error("⛔ API Token 과 GitHub URL을 입력해야 이 페이지를 이용할 수 있습니다.")
    st.stop()

# API 키 유효성 검사
with st.spinner("Validating API key..."):
    if not gemini.api_check(api_key):
        st.error("❌ Invalid API Key. Please check your Gemini API key.")
        st.stop()

# GitHub URL 파싱
parsed_url = parse_github_url(repository_url)
if not parsed_url:
    st.error("❌ Invalid GitHub URL format")
    st.stop()

owner = parsed_url["owner"]
repo = parsed_url["repo"]

# ---------------------------------------------------
# 페이지 헤더 (UI 개선)
# ---------------------------------------------------
st.title("📡 Repositorie Radar")
st.write("GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.")
st.divider()

st.title("🔍 CodeFlow Analysis")

# ---------------------------------------------------
# 레포지토리 정보 표시
# ---------------------------------------------------
with st.expander("📦 Repository Information", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Repository URL:**")
        st.code(repository_url, language=None)
    with col2:
        st.markdown(f"**Owner:** `{owner}`")
        st.markdown(f"**Repository:** `{repo}`")

st.divider()

# ---------------------------------------------------
# 분석 옵션 설정
# ---------------------------------------------------
st.header("⚙️ Analysis Options")

col1, col2 = st.columns([1, 1])

with col1:
    analysis_depth = st.selectbox(
        "Analysis Depth",
        ["Basic (File Tree Only)", "Detailed (Include Source Code)"],
        help="Basic: Analyze file structure only. Detailed: Include actual source code."
    )

with col2:
    max_files = st.slider(
        "Maximum Files to Analyze",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of source files to include (Detailed mode only)"
    )

# 분석할 파일 확장자 선택
file_extensions = st.multiselect(
    "File Extensions to Analyze (Detailed mode)",
    [".py", ".js", ".java", ".cpp", ".ts", ".go", ".rs", ".rb", ".php"],
    default=[".py"],
    help="Select file types to include in detailed analysis"
)

# 브랜치 선택
branch = st.text_input(
    "Branch",
    value="main",
    help="Branch to analyze (default: main)"
)

st.divider()

# ---------------------------------------------------
# AI 분석 섹션 (UI 개선 - header만 변경)
# ---------------------------------------------------
st.header("🤖 AI Comment")

if st.button("🔍 Start Code Flow Analysis", type="primary", use_container_width=True):
    
    # 1단계: GitHub에서 파일 트리 가져오기
    with st.status("📁 Fetching repository structure from GitHub...", expanded=True) as status:
        st.write(f"Repository: {owner}/{repo}")
        st.write(f"Branch: {branch}")
        st.write("Fetching file tree via GitHub API...")
        
        try:
            file_tree = fetch_repository_tree(owner, repo, branch)
            
            if not file_tree:
                st.error("❌ Failed to fetch repository structure. Check if repository is public and URL is correct.")
                st.stop()
            
            file_count = count_files(file_tree)
            st.write(f"✅ Found {file_count} files")
            
            # 파일 트리 미리보기
            with st.expander("📂 File Tree Preview", expanded=False):
                st.json(file_tree)
            
            status.update(label=f"✅ File tree loaded! ({file_count} files)", state="complete")
        
        except Exception as e:
            st.error(f"❌ Error loading file tree: {str(e)}")
            st.stop()
    
    # 2단계: 소스 코드 가져오기 (Detailed 모드일 경우)
    source_code = None
    
    if analysis_depth == "Detailed (Include Source Code)":
        with st.status("💻 Fetching source code from GitHub...", expanded=True) as status:
            st.write(f"Looking for files with extensions: {', '.join(file_extensions)}")
            
            try:
                # 파일 트리에서 해당 확장자 파일 찾기
                source_files = find_source_files(file_tree, file_extensions)
                
                if not source_files:
                    st.warning(f"⚠️ No files found with extensions: {file_extensions}")
                    st.info("Continuing with file tree analysis only...")
                else:
                    source_code = {}
                    files_fetched = 0
                    
                    # 각 파일의 내용 가져오기
                    for filename, filepath in source_files[:max_files]:
                        st.write(f"📥 Fetching: `{filepath}`")
                        
                        content = fetch_file_content(owner, repo, filepath, branch)
                        
                        if content and not content.startswith("# Error"):
                            # 파일 내용 2000자 제한
                            source_code[filepath] = content[:2000]
                            files_fetched += 1
                            st.write(f"✅ Fetched: `{filepath}` ({len(content)} chars)")
                        else:
                            st.warning(f"⚠️ Could not fetch: `{filepath}`")
                        
                        if files_fetched >= max_files:
                            break
                    
                    if source_code:
                        st.write(f"✅ Successfully fetched {len(source_code)} files")
                    else:
                        st.warning("⚠️ No source files fetched. Using file tree only.")
                
                status.update(label=f"✅ Fetched {len(source_code) if source_code else 0} source files", state="complete")
            
            except Exception as e:
                st.warning(f"⚠️ Could not fetch source code: {str(e)}")
                st.info("Continuing with file tree analysis only...")
    
    # 3단계: AI 분석 실행
    with st.status("🤖 Analyzing code flow with Gemini AI...", expanded=True) as status:
        st.write("Sending data to Gemini AI...")
        st.write(f"Language: {language}")
        st.write(f"Mode: {analysis_depth}")
        st.write(f"Files in analysis: {count_files(file_tree)}")
        if source_code:
            st.write(f"Source code samples: {len(source_code)}")
        
        try:
            # Gemini API 호출
            result = gemini.api_code_flow_analysis(
                _key=api_key,
                _file_tree=file_tree,
                _source_code=source_code,
                _language=language
            )
            
            if result.startswith("Error:"):
                st.error(f"❌ Analysis failed: {result}")
                st.stop()
            
            status.update(label="✅ Analysis complete!", state="complete")
        
        except Exception as e:
            st.error(f"❌ AI Analysis error: {str(e)}")
            st.stop()
    
    # 4단계: 분석 결과 표시
    st.success("✅ Code Flow Analysis Complete!")
    
    st.divider()
    st.markdown("## 📊 Analysis Results")
    
    # 결과를 탭으로 구분하여 표시
    tab1, tab2, tab3 = st.tabs(["📝 Full Analysis", "📥 Download", "ℹ️ Info"])
    
    with tab1:
        st.markdown(result)
    
    with tab2:
        st.markdown("### Download Analysis Report")
        
        # 분석 보고서 생성
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Code Flow Analysis Report

**Repository:** {repository_url}
**Owner:** {owner}
**Repository Name:** {repo}
**Branch:** {branch}
**Analysis Date:** {timestamp}
**Language:** {language}
**Analysis Mode:** {analysis_depth}
**Files Analyzed:** {count_files(file_tree)}

---

{result}

---

## File Tree Structure
```json
{json.dumps(file_tree, indent=2, ensure_ascii=False)}
```

---

*Generated by Repository Radar using Gemini AI*
"""
        
        col1, col2 = st.columns(2)
        
        # 마크다운 파일 다운로드
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=report,
                file_name=f"code_flow_analysis_{owner}_{repo}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # 텍스트 파일 다운로드
        with col2:
            st.download_button(
                label="📥 Download as Text",
                data=result,
                file_name=f"code_flow_analysis_{owner}_{repo}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with tab3:
        st.markdown("""
        ### 📊 What is Code Flow Analysis?
        
        Code Flow Analysis provides:
        
        1. **Execution Flow**: Step-by-step path from entry point
        2. **Module Dependencies**: How modules interact
        3. **Data Flow**: How data moves through the app
        4. **Key Functions**: Important functions and roles
        5. **Interaction Diagram**: Component relationships
        6. **Critical Paths**: Performance bottlenecks
        7. **Recommendations**: Improvement suggestions
        
        ### 🎯 Use Cases
        
        - Understanding unfamiliar codebases
        - Planning refactoring
        - Identifying bottlenecks
        - Documenting architecture
        - Code reviews
        
        ### 🔄 Analysis Process
        
        1. **Fetch from GitHub**: Automatically fetch repository structure
        2. **Parse Structure**: Convert to hierarchical tree
        3. **Fetch Source**: Download key source files (Detailed mode)
        4. **AI Analysis**: Gemini analyzes flow and dependencies
        5. **Generate Report**: Create comprehensive analysis
        """)

# ---------------------------------------------------
# 추가 기능 및 팁
# ---------------------------------------------------
st.divider()

with st.expander("💡 Tips for Better Analysis"):
    st.markdown("""
    **For Best Results:**
    
    1. **Use Public Repositories**: GitHub API works best with public repos
    2. **Check Branch Name**: Default is 'main', but some repos use 'master'
    3. **Select Relevant Extensions**: Focus on main language files
    4. **Limit File Count**: 3-5 files recommended for detailed analysis
    5. **Include Entry Points**: Files like `main.py`, `app.py`, `index.js`
    
    **What Gets Analyzed:**
    
    - 📁 Directory structure and organization
    - 🔗 Module imports and dependencies
    - 📊 Function call chains
    - 🔄 Data flow between components
    - ⚡ Performance critical paths
    - 🎯 Entry points and initialization
    
    **GitHub API Limits:**
    
    - Rate limit: 60 requests/hour (unauthenticated)
    - Repository must be public
    - Large files may be truncated
    """)

# ---------------------------------------------------
# footer
# ---------------------------------------------------
st.divider()
st.caption(f"Powered by Gemini AI | Code Flow Analysis v2.0 | Repository: {owner}/{repo}")