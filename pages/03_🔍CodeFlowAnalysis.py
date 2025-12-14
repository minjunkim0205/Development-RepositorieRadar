# pages/03_🔍CodeFlowAnalysis.py
<<<<<<< Updated upstream
=======
# ---------------------------------------------------
# GitHub Repository: Development-RepositorieRadar
# Author: minjunkim0205, Assadgang, Gplexs, han183536-ux
# Description: 코드 자동 분석 밎 흐름 시각화
# Version: 1.0.1 
# ---------------------------------------------------
>>>>>>> Stashed changes
# ---------------------------------------------------
# 모듈 임포트
# ---------------------------------------------------
import streamlit as st
import json
import requests
from pathlib import Path
<<<<<<< Updated upstream
=======
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import re
>>>>>>> Stashed changes
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
<<<<<<< Updated upstream
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
=======
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Code Flow Analysis",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------------------
# 세련된 분석 도구 디자인을 위한 커스텀 CSS (Home.py와 동일)
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* 전역 스타일 */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #e8eaed;
    }
    
    /* 메인 타이틀 */
    .main-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    /* 서브타이틀 */
    .subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem;
        color: #9aa0a6;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* 섹션 헤더 */
    .section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #e8eaed;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(0, 245, 255, 0.2);
    }
    
    /* 코드 블록 스타일 */
    .stCodeBlock {
        background: rgba(26, 31, 58, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(0, 245, 255, 0.1);
    }
    
    code {
        background: rgba(26, 31, 58, 0.6) !important;
        color: #e8eaed !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* JSON viewer */
    pre {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #e8eaed !important;
    }
    
    /* Expander 스타일 */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 58, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        border: 1px solid rgba(0, 245, 255, 0.1) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #e8eaed !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 245, 255, 0.3) !important;
        background: rgba(26, 31, 58, 0.8) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 31, 58, 0.4) !important;
        border: 1px solid rgba(0, 245, 255, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* 스피너 스타일 */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #0a0e27 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 245, 255, 0.3);
    }
    
    /* 정보 박스 스타일 */
    .stAlert {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.2) !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e8eaed !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 31, 58, 0.4);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        background: transparent !important;
        border-radius: 8px !important;
        color: #9aa0a6 !important;
        padding: 0.75rem 1.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 245, 255, 0.1) !important;
        color: #667eea !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #0a0e27 !important;
    }
    
    /* Download 버튼 */
    .stDownloadButton > button {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.2) !important;
        color: #667eea !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: rgba(0, 245, 255, 0.5) !important;
        background: rgba(26, 31, 58, 0.8) !important;
        transform: translateY(-2px);
    }
    
    /* Status 컨테이너 */
    .stStatus {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* 섹션 타이틀 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e8eaed !important;
    }
    
    /* 일반 텍스트 */
    p, li {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #bdc1c6;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%) !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #e8eaed !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #bdc1c6;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Input 박스 스타일 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #e8eaed !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: rgba(0, 245, 255, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(0, 245, 255, 0.3) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: rgba(0, 245, 255, 0.2) !important;
    }
    
    .stSlider [role="slider"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Label 스타일 */
    .stTextInput > label,
    .stSelectbox > label,
    .stMultiSelect > label,
    .stSlider > label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e8eaed !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 245, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load state into variables
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# Sidebar (API, URL input)
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")
st.sidebar.info("💡 이 페이지는 **코드의 실행 흐름과 의존성**을 분석합니다!")

api_key = st.sidebar.text_input(
    "🔑 GPT/Gemini API 키", 
    value=options.get("api_key", ""), 
    type="password", 
    disabled=True,
    help="Home 페이지에서 설정한 API 키"
)

repository_url = st.sidebar.text_input(
    "📊 GitHub 저장소 URL", 
    value=options.get("repository_url", ""), 
    disabled=True,
    help="Home 페이지에서 설정한 저장소 주소"
)

# Language selection
language = st.sidebar.selectbox(
    "🌏 응답 언어",
    ["Korean", "English"],
    index=0,
    help="AI가 답변할 언어를 선택하세요"
>>>>>>> Stashed changes
)

st.sidebar.divider()

<<<<<<< Updated upstream
# 레포지토리 정보 표시
if repository_url:
    try:
        owner, repo = repository_url.replace("https://github.com/", "").split("/")[:2]
        st.sidebar.success(f"✅ Repository: `{owner}/{repo}`")
=======
with st.sidebar.expander("❓ 이 페이지는 뭐하는 곳인가요?"):
    st.markdown("""
    ### 🎯 목적
    
    GitHub 저장소의 **코드 흐름**을
    AI가 분석해줍니다!
    
    ### 📚 배울 수 있는 것
    
    1. 코드 실행 흐름은 어떻게 되는지
    2. 모듈 간 의존성은 무엇인지
    3. 데이터는 어떻게 이동하는지
    4. 핵심 함수는 무엇인지
    """)

# Additional info
if repository_url:
    try:
        owner, repo = repository_url.replace("https://github.com/", "").split("/")[:2]
        st.sidebar.success(f"✅ **{repo}** 프로젝트")
>>>>>>> Stashed changes
    except:
        st.sidebar.error("❌ Invalid URL format")

# ---------------------------------------------------
<<<<<<< Updated upstream
# 헬퍼 함수들
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    """GitHub URL에서 owner와 repo 추출"""
=======
# Helper Functions
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    """GitHub URL 파싱"""
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    """GitHub API로 저장소의 파일 트리 가져오기"""
    # GitHub API 엔드포인트
=======
    """
    GitHub API로 저장소 파일 트리 가져오기
    
    Args:
        owner: 저장소 소유자
        repo: 저장소 이름
        branch: 브랜치 (기본값: main)
    
    Returns:
        dict: 파일 트리 구조
    """
    # GitHub API: Get Repository Tree
>>>>>>> Stashed changes
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    
    try:
        response = requests.get(url, timeout=15)
        
<<<<<<< Updated upstream
        # main 브랜치 실패 시 master 시도
=======
        # 401/404 에러 시 master 브랜치 시도
>>>>>>> Stashed changes
        if response.status_code in [401, 404]:
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
<<<<<<< Updated upstream
        # 파일 트리를 계층 구조로 변환
=======
        # Tree 데이터를 계층 구조로 변환
>>>>>>> Stashed changes
        tree = {}
        
        for item in data.get("tree", []):
            path = item["path"]
<<<<<<< Updated upstream
            item_type = item["type"]
            
            # 불필요한 파일/폴더 필터링
=======
            item_type = item["type"]  # blob(file) or tree(directory)
            
            # 무시할 디렉토리/파일
>>>>>>> Stashed changes
            ignore_patterns = ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 
                             '.idea', '.vscode', 'dist', 'build', '.DS_Store']
            
            if any(ignore in path for ignore in ignore_patterns):
                continue
            
            # 경로를 계층 구조로 변환
            parts = path.split("/")
            current = tree
            
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
<<<<<<< Updated upstream
                    # 파일 또는 디렉토리 추가
=======
                    # 마지막 부분 (파일 또는 디렉토리)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
                    # 중간 디렉토리 생성
=======
                    # 중간 디렉토리
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    """GitHub API로 특정 파일의 내용 가져오기"""
=======
    """
    GitHub API로 파일 내용 가져오기
    
    Args:
        owner: 저장소 소유자
        repo: 저장소 이름
        file_path: 파일 경로
        branch: 브랜치
    
    Returns:
        str: 파일 내용
    """
>>>>>>> Stashed changes
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    
    try:
        response = requests.get(url, timeout=10)
        
<<<<<<< Updated upstream
        # main 브랜치 실패 시 master 시도
=======
        # master 브랜치 시도
>>>>>>> Stashed changes
        if response.status_code in [401, 404]:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref=master"
            response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        data = response.json()
        
<<<<<<< Updated upstream
        # Base64 디코딩하여 파일 내용 반환
=======
        # Base64 디코딩
>>>>>>> Stashed changes
        import base64
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content
    
    except Exception as e:
        return f"# Error fetching file: {str(e)}"


def find_source_files(tree: dict, extensions: list, current_path: str = "") -> list:
<<<<<<< Updated upstream
    """파일 트리에서 특정 확장자의 파일 경로 찾기"""
=======
    """
    파일 트리에서 특정 확장자의 파일 찾기
    
    Args:
        tree: 파일 트리
        extensions: 찾을 확장자 리스트
        current_path: 현재 경로 (재귀용)
    
    Returns:
        list: [(파일명, 경로)] 리스트
    """
>>>>>>> Stashed changes
    files = []
    
    for name, value in tree.items():
        if isinstance(value, dict):
            if value.get("type") == "file":
<<<<<<< Updated upstream
                # 확장자 매칭 확인
=======
                # 확장자 확인
>>>>>>> Stashed changes
                if any(name.endswith(ext) for ext in extensions):
                    full_path = f"{current_path}/{name}" if current_path else name
                    files.append((name, value.get("path", full_path)))
            
            elif value.get("type") == "directory":
<<<<<<< Updated upstream
                # 하위 디렉토리 재귀 탐색
=======
                # 재귀적으로 탐색
>>>>>>> Stashed changes
                sub_path = f"{current_path}/{name}" if current_path else name
                files.extend(find_source_files(value.get("contents", {}), extensions, sub_path))
    
    return files


def count_files(tree: dict) -> int:
<<<<<<< Updated upstream
    """파일 트리의 총 파일 개수 계산"""
=======
    """파일 트리에서 총 파일 개수 계산"""
>>>>>>> Stashed changes
    count = 0
    for key, value in tree.items():
        if isinstance(value, dict):
            if value.get("type") == "file":
                count += 1
            elif value.get("type") == "directory":
                count += count_files(value.get("contents", {}))
    return count


# ---------------------------------------------------
<<<<<<< Updated upstream
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
=======
# 시각화 함수들 (6가지 차트)
# ---------------------------------------------------
def create_folder_file_flow(tree: dict) -> go.Figure:
    """🌊 폴더-파일 흐름도: 트리맵으로 변경 (더 명확한 시각화)"""
    labels = []
    parents = []
    values = []
    
    def traverse(node, parent_name, depth=0):
        # 깊이 제한 (3단계까지)
        if depth > 3:
            return
        
        for name, value in node.items():
            if isinstance(value, dict):
                if value.get("type") == "directory":
                    # 숨김 폴더 제외
                    if name.startswith('.') or name in ['__pycache__', 'node_modules', '.git']:
                        continue
                    
                    file_count = count_files({name: value})
                    if file_count > 0:
                        labels.append(name)
                        parents.append(parent_name)
                        values.append(file_count)
                        
                        # 재귀
                        traverse(value.get("contents", {}), name, depth + 1)
    
    # 루트 추가
    total_files = count_files(tree)
    labels.insert(0, "Repository")
    parents.insert(0, "")
    values.insert(0, total_files)
    
    traverse(tree, "Repository", 0)
    
    if len(labels) <= 1:
        fig = go.Figure()
        fig.add_annotation(
            text="폴더 구조를 찾을 수 없습니다",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color='#9aa0a6', family='Plus Jakarta Sans')
        )
    else:
        # Treemap으로 변경 (더 직관적)
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            textfont=dict(size=16, family='Plus Jakarta Sans', color='#ffffff'),
            marker=dict(
                colorscale='Viridis',
                line=dict(color='#1a1f3a', width=2)
            ),
            hovertemplate='<b style="font-size:16px">%{label}</b><br>파일 수: %{value}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': "🌊 폴더-파일 흐름도",
            'font': {'family': 'Plus Jakarta Sans', 'size': 24, 'color': '#e8eaed'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=650,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed', size=14)
    )
    
    return fig


def find_entry_points(tree: dict) -> go.Figure:
    """🚀 시작 파일 찾기"""
    entry_point_patterns = [
        'main.py', 'app.py', '__main__.py', 'run.py', 'start.py',
        'index.js', 'app.js', 'server.js', 'index.ts', 'main.ts',
        'Main.java', 'Application.java', 'index.html', 'main.go',
        'main.rs', 'index.php', '__init__.py', 'setup.py'
    ]
    
    found_files = []
    
    def search(node, path=""):
        for name, value in node.items():
            if isinstance(value, dict):
                current_path = f"{path}/{name}" if path else name
                
                if value.get("type") == "file":
                    if name.lower() in [p.lower() for p in entry_point_patterns]:
                        priority = entry_point_patterns.index(name) if name in entry_point_patterns else 100
                        found_files.append({
                            'name': name,
                            'path': current_path,
                            'priority': priority,
                            'size': value.get('size', 0)
                        })
                
                elif value.get("type") == "directory":
                    search(value.get("contents", {}), current_path)
    
    search(tree)
    
    # 우선순위로 정렬
    found_files.sort(key=lambda x: x['priority'])
    
    if not found_files:
        # 파일이 없으면 빈 차트
        fig = go.Figure()
        fig.add_annotation(
            text="시작 파일을 찾을 수 없습니다",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color='#9aa0a6', family='Plus Jakarta Sans')
        )
    else:
        files_to_show = found_files[:10]
        
        fig = go.Figure(data=[
            go.Bar(
                y=[f['name'] for f in files_to_show],
                x=[f['size'] for f in files_to_show],
                orientation='h',
                marker=dict(
                    color='#667eea',
                    line=dict(color='#764ba2', width=2)
                ),
                text=[f['path'] for f in files_to_show],
                textposition='auto',
                textfont=dict(size=14, family='Plus Jakarta Sans', color='#ffffff'),
                hovertemplate='<b style="font-size:16px">%{y}</b><br>경로: %{text}<br>크기: %{x} bytes<extra></extra>'
            )
        ])
    
    fig.update_layout(
        title={
            'text': "🚀 시작 파일 찾기",
            'font': {'family': 'Plus Jakarta Sans', 'size': 24, 'color': '#e8eaed'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title=dict(
                text="파일 크기 (bytes)",
                font=dict(size=16, family='Plus Jakarta Sans')
            ),
            tickfont=dict(size=14, family='Plus Jakarta Sans'),
            gridcolor='rgba(102, 126, 234, 0.1)'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=14, family='Plus Jakarta Sans'),
            gridcolor='rgba(102, 126, 234, 0.1)'
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed', size=14)
    )
    
    return fig
    """🚀 시작 파일 찾기"""
    entry_point_patterns = [
        'main.py', 'app.py', '__main__.py', 'run.py', 'start.py',
        'index.js', 'app.js', 'server.js', 'index.ts', 'main.ts',
        'Main.java', 'Application.java', 'index.html', 'main.go',
        'main.rs', 'index.php', '__init__.py', 'setup.py'
    ]
    
    found_files = []
    
    def search(node, path=""):
        for name, value in node.items():
            if isinstance(value, dict):
                current_path = f"{path}/{name}" if path else name
                
                if value.get("type") == "file":
                    if name.lower() in [p.lower() for p in entry_point_patterns]:
                        priority = entry_point_patterns.index(name) if name in entry_point_patterns else 100
                        found_files.append({
                            'name': name,
                            'path': current_path,
                            'priority': priority,
                            'size': value.get('size', 0)
                        })
                
                elif value.get("type") == "directory":
                    search(value.get("contents", {}), current_path)
    
    search(tree)
    
    # 우선순위로 정렬
    found_files.sort(key=lambda x: x['priority'])
    
    if not found_files:
        # 파일이 없으면 빈 차트
        fig = go.Figure()
        fig.add_annotation(
            text="시작 파일을 찾을 수 없습니다",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#9aa0a6')
        )
    else:
        files_to_show = found_files[:10]
        
        fig = go.Figure(data=[
            go.Bar(
                y=[f['name'] for f in files_to_show],
                x=[f['size'] for f in files_to_show],
                orientation='h',
                marker=dict(
                    color=[f['priority'] for f in files_to_show],
                    colorscale='Teal',
                    showscale=False
                ),
                text=[f['path'] for f in files_to_show],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>경로: %{text}<br>크기: %{x} bytes<extra></extra>'
            )
        ])
    
    fig.update_layout(
        title={
            'text': "🚀 시작 파일 찾기 (우선순위순)",
            'font': {'family': 'Plus Jakarta Sans', 'size': 20, 'color': '#e8eaed'}
        },
        xaxis_title="파일 크기 (bytes)",
        yaxis_title="",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed'),
        xaxis=dict(gridcolor='rgba(0, 245, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(0, 245, 255, 0.1)')
    )
    
    return fig


def analyze_tech_stack(tree: dict) -> go.Figure:
    """📊 기술 스택 파악: 언어 비율"""
    extensions = {}
    
    def count_extensions(node):
        for name, value in node.items():
            if isinstance(value, dict):
                if value.get("type") == "file":
                    ext = value.get("extension", "")
                    if ext:
                        extensions[ext] = extensions.get(ext, 0) + 1
                elif value.get("type") == "directory":
                    count_extensions(value.get("contents", {}))
    
    count_extensions(tree)
    
    # 언어 매핑
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React (JSX)',
        '.tsx': 'React (TSX)',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.html': 'HTML',
        '.css': 'CSS',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.sh': 'Shell',
        '.sql': 'SQL'
    }
    
    # 언어로 변환
    languages = {}
    for ext, count in extensions.items():
        lang = language_map.get(ext, ext)
        languages[lang] = languages.get(lang, 0) + count
    
    # 상위 10개만
    top_languages = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10])
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(top_languages.keys()),
            values=list(top_languages.values()),
            hole=0.45,
            marker=dict(
                colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', 
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#a8edea'],
                line=dict(color='#1a1f3a', width=3)
            ),
            textfont=dict(size=16, family='Plus Jakarta Sans', color='#ffffff'),
            textposition='inside',
            insidetextorientation='radial',
            hovertemplate='<b style="font-size:16px">%{label}</b><br>파일 수: %{value}<br>비율: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': "📊 기술 스택 파악",
            'font': {'family': 'Plus Jakarta Sans', 'size': 24, 'color': '#e8eaed'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed', size=14),
        showlegend=True,
        legend=dict(
            font=dict(size=14),
            bgcolor='rgba(26, 31, 58, 0.6)',
            bordercolor='rgba(102, 126, 234, 0.3)',
            borderwidth=1
        )
    )
    
    return fig


def file_type_distribution(tree: dict) -> go.Figure:
    """☀️ 파일 종류 분포: Sunburst"""
    extensions = Counter()
    
    def count_extensions(node):
        for name, value in node.items():
            if isinstance(value, dict):
                if value.get("type") == "file":
                    ext = value.get("extension", "")
                    if ext:
                        extensions[ext] += 1
                elif value.get("type") == "directory":
                    count_extensions(value.get("contents", {}))
    
    count_extensions(tree)
    
    # 카테고리화
    categories = {
        'Code': ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php'],
        'Web': ['.html', '.css', '.scss', '.sass', '.less'],
        'Config': ['.json', '.yml', '.yaml', '.toml', '.ini', '.env', '.xml'],
        'Docs': ['.md', '.txt', '.rst', '.pdf'],
        'Data': ['.csv', '.sql', '.db', '.sqlite'],
        'Other': []
    }
    
    labels = ["Files"]
    parents = [""]
    values = [sum(extensions.values())]
    
    # 카테고리별 분류
    for category, exts in categories.items():
        category_count = sum(extensions[ext] for ext in exts if ext in extensions)
        if category_count > 0:
            labels.append(category)
            parents.append("Files")
            values.append(category_count)
            
            # 각 확장자
            for ext in exts:
                if ext in extensions:
                    labels.append(ext)
                    parents.append(category)
                    values.append(extensions[ext])
    
    # Other 카테고리
    other_exts = [ext for ext in extensions if not any(ext in cats for cats in categories.values())]
    if other_exts:
        other_count = sum(extensions[ext] for ext in other_exts)
        labels.append("Other")
        parents.append("Files")
        values.append(other_count)
        
        for ext in other_exts[:5]:  # 상위 5개만
            labels.append(ext)
            parents.append("Other")
            values.append(extensions[ext])
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(
            colorscale='Sunset',
            line=dict(color='#1a1f3a', width=2)
        ),
        textfont=dict(size=16, family='Plus Jakarta Sans', color='#ffffff'),
        hovertemplate='<b style="font-size:16px">%{label}</b><br>파일 수: %{value}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "☀️ 파일 종류 분포",
            'font': {'family': 'Plus Jakarta Sans', 'size': 24, 'color': '#e8eaed'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed', size=14)
    )
    
    return fig


def important_folders(tree: dict) -> go.Figure:
    """📁 중요한 폴더 순위"""
    folder_stats = {}
    
    def analyze_folder(node, path=""):
        for name, value in node.items():
            if isinstance(value, dict) and value.get("type") == "directory":
                current_path = f"{path}/{name}" if path else name
                file_count = count_files({name: value})
                
                folder_stats[current_path] = {
                    'name': name,
                    'files': file_count,
                    'depth': len(current_path.split('/'))
                }
                
                analyze_folder(value.get("contents", {}), current_path)
    
    analyze_folder(tree)
    
    # 파일 수로 정렬
    sorted_folders = sorted(folder_stats.items(), key=lambda x: x[1]['files'], reverse=True)[:15]
    
    if not sorted_folders:
        fig = go.Figure()
        fig.add_annotation(
            text="폴더를 찾을 수 없습니다",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color='#9aa0a6', family='Plus Jakarta Sans')
        )
    else:
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', 
                  '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#a8edea',
                  '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
        
        fig = go.Figure(data=[
            go.Bar(
                x=[f[1]['files'] for f in sorted_folders],
                y=[f[1]['name'] for f in sorted_folders],
                orientation='h',
                marker=dict(
                    color=colors[:len(sorted_folders)],
                    line=dict(color='#1a1f3a', width=2)
                ),
                text=[f[0] for f in sorted_folders],
                textposition='none',
                textfont=dict(size=14, family='Plus Jakarta Sans'),
                hovertemplate='<b style="font-size:16px">%{y}</b><br>경로: %{text}<br>파일 수: %{x}개<extra></extra>'
            )
        ])
    
    fig.update_layout(
        title={
            'text': "📁 중요한 폴더 순위",
            'font': {'family': 'Plus Jakarta Sans', 'size': 24, 'color': '#e8eaed'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title=dict(
                text="파일 수",
                font=dict(size=16, family='Plus Jakarta Sans')
            ),
            tickfont=dict(size=14, family='Plus Jakarta Sans'),
            gridcolor='rgba(102, 126, 234, 0.1)'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=14, family='Plus Jakarta Sans'),
            gridcolor='rgba(102, 126, 234, 0.1)'
        ),
        height=550,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#e8eaed', size=14)
    )
    
    return fig


def create_interaction_diagram(tree: dict, source_code: dict = None) -> str:
    """🔗 상호작용 다이어그램: 테스트 수행"""
    
    # 1단계: 모든 파일 추출
    all_files = []
    
    def extract_files(node, path=""):
        for name, value in node.items():
            if isinstance(value, dict):
                current_path = f"{path}/{name}" if path else name
                
                if value.get("type") == "file":
                    ext = value.get("extension", "")
                    all_files.append({
                        'name': name,
                        'path': current_path,
                        'ext': ext,
                        'size': value.get('size', 0)
                    })
                
                elif value.get("type") == "directory":
                    extract_files(value.get("contents", {}), current_path)
    
    extract_files(tree)
    
    # 2단계: 파일 분류 (실제 저장소 구조 기반)
    entry_files = []      # 진입점 (main.py, app.py, index.js 등)
    ui_files = []         # UI 관련 (streamlit, Home.py, data/*.css 등)
    page_files = []       # pages 폴더
    module_files = []     # module 폴더
    api_files = []        # API 관련
    config_files = []     # 설정 파일
    
    for f in all_files:
        name_lower = f['name'].lower()
        path_lower = f['path'].lower()
        
        # 진입점 파일
        if name_lower in ['main.py', 'app.py', '__main__.py', 'run.py', 'index.js', 'index.html', 'server.js']:
            entry_files.append(f['name'])
        
        # Streamlit UI
        elif 'home.py' in name_lower or 'streamlit' in path_lower:
            ui_files.append(f['name'])
        
        # CSS/데이터 파일
        elif f['ext'] in ['.css', '.scss']:
            ui_files.append(f['path'])
        
        # pages 폴더의 파일
        elif 'pages/' in path_lower or '/pages/' in path_lower:
            # pages/*.py 형태로 저장
            if f['ext'] in ['.py', '.js', '.jsx', '.ts', '.tsx']:
                page_files.append(f['name'])
        
        # module 폴더의 파일
        elif 'module/' in path_lower or 'modules/' in path_lower:
            if f['ext'] in ['.py', '.js', '.jsx', '.ts', '.tsx']:
                module_files.append(f['name'])
        
        # API 파일
        elif 'api' in name_lower or 'client' in name_lower or 'service' in name_lower:
            api_files.append(f['name'])
    
    # 3단계: 외부 API 감지 (소스코드에서)
    external_apis = []
    
    if source_code:
        api_detected = {'openai': False, 'gemini': False, 'github': False}
        
        for code in source_code.values():
            code_lower = code.lower()
            
            if not api_detected['openai'] and ('openai' in code_lower or 'gpt' in code_lower):
                api_detected['openai'] = True
            
            if not api_detected['gemini'] and 'gemini' in code_lower:
                api_detected['gemini'] = True
            
            if not api_detected['github'] and ('github.com/api' in code_lower or 'api.github.com' in code_lower):
                api_detected['github'] = True
        
        # API 이름 생성
        if api_detected['openai'] and api_detected['gemini']:
            external_apis.append('OpenAI / Gemini')
        elif api_detected['openai']:
            external_apis.append('OpenAI API')
        elif api_detected['gemini']:
            external_apis.append('Gemini API')
        
        if api_detected['github']:
            external_apis.append('GitHub API')
    
    # API가 없으면 module 파일에서 추론
    if not external_apis and module_files:
        for mf in module_files:
            if 'gpt' in mf.lower() or 'openai' in mf.lower():
                if 'OpenAI API' not in external_apis:
                    external_apis.append('OpenAI API')
            if 'gemini' in mf.lower():
                if 'Gemini API' not in external_apis:
                    external_apis.append('Gemini API')
            if 'github' in mf.lower():
                if 'GitHub API' not in external_apis:
                    external_apis.append('GitHub API')
    
    # 4단계: 다이어그램 생성
    lines = []
    
    # === Layer 1: User ===
    user_box = [
        "+--------------+",
        "|     User     |",
        "+--------------+"
    ]
    
    # === Layer 2: Streamlit UI / Entry Point ===
    layer2_items = []
    
    # UI 파일 우선
    if ui_files:
        layer2_items.extend(ui_files[:2])
    elif entry_files:
        layer2_items.extend(entry_files[:2])
    else:
        layer2_items = ['Streamlit UI']
    
    # 박스 생성
    max_width = max(len(item) for item in layer2_items) + 4
    max_width = max(max_width, 22)
    
    ui_box = []
    ui_box.append("+" + "-" * max_width + "+")
    ui_box.append("| " + "Streamlit UI".ljust(max_width - 2) + " |")
    for item in layer2_items[:2]:
        display_name = item if len(item) <= max_width - 4 else item[:max_width-7] + "..."
        ui_box.append("| " + display_name.ljust(max_width - 2) + " |")
    ui_box.append("+" + "-" * max_width + "+")
    
    # === Layer 3: Pages ===
    layer3_items = []
    
    if page_files:
        layer3_items = page_files[:2]
        # "각 페이지 주석" 추가
        layer3_formatted = []
        for pf in layer3_items:
            if len(pf) < 12:
                layer3_formatted.append(f"{pf} (각 페이지 주석)")
            else:
                layer3_formatted.append(pf)
        layer3_items = layer3_formatted
    
    page_box = None
    if layer3_items:
        max_width = max(len(item) for item in layer3_items) + 4
        max_width = max(max_width, 25)
        
        page_box = []
        page_box.append("+" + "-" * max_width + "+")
        for item in layer3_items:
            display_name = item if len(item) <= max_width - 4 else item[:max_width-7] + "..."
            page_box.append("| " + display_name.ljust(max_width - 2) + " |")
        page_box.append("+" + "-" * max_width + "+")
    
    # === Layer 4: Modules ===
    layer4_items = []
    
    if module_files:
        layer4_items = module_files[:2]
    elif api_files:
        layer4_items = api_files[:2]
    
    module_box = None
    if layer4_items:
        max_width = max(len(item) for item in layer4_items) + 4
        max_width = max(max_width, 22)
        
        module_box = []
        module_box.append("+" + "-" * max_width + "+")
        for item in layer4_items:
            display_name = item if len(item) <= max_width - 4 else item[:max_width-7] + "..."
            module_box.append("| " + display_name.ljust(max_width - 2) + " |")
        module_box.append("+" + "-" * max_width + "+")
    
    # === Layer 5: External APIs ===
    api_box = None
    if external_apis:
        max_width = max(len(api) for api in external_apis) + 4
        max_width = max(max_width, 22)
        
        api_box = []
        api_box.append("+" + "-" * max_width + "+")
        for api in external_apis:
            api_box.append("| " + api.ljust(max_width - 2) + " |")
        api_box.append("+" + "-" * max_width + "+")
    
    # 5단계: 다이어그램 조립
    lines.append("")
    
    # User <---> UI
    indent = 2
    lines.append(" " * indent + user_box[0] + " " * 10 + ui_box[0])
    lines.append(" " * indent + user_box[1] + "  <--->   " + ui_box[1])
    lines.append(" " * indent + user_box[2] + " " * 10 + ui_box[2])
    
    # UI 박스 나머지 줄
    for i in range(3, len(ui_box)):
        lines.append(" " * 28 + ui_box[i])
    
    # 화살표 (UI -> Pages)
    if page_box:
        lines.append(" " * 28 + "^")
        lines.append(" " * 28 + "|")
        lines.append(" " * 28 + "|")
        lines.append(" " * 28 + "v")
        
        # Pages 박스
        for line in page_box:
            lines.append(" " * 20 + line)
        
        # 화살표 (Pages -> Modules)
        if module_box:
            lines.append(" " * 28 + "^")
            lines.append(" " * 28 + "|")
            lines.append(" " * 28 + "|")
            lines.append(" " * 28 + "v")
    elif module_box:
        # Pages 없이 바로 Modules로
        lines.append(" " * 28 + "^")
        lines.append(" " * 28 + "|")
        lines.append(" " * 28 + "|")
        lines.append(" " * 28 + "v")
    
    # Modules 박스
    if module_box:
        for line in module_box:
            lines.append(" " * 20 + line)
        
        # 화살표 (Modules -> APIs)
        if api_box:
            lines.append(" " * 28 + "^")
            lines.append(" " * 28 + "|")
            
            # API 라벨
            api_label = " OpenAI / Gemini API" if 'OpenAI' in str(external_apis) or 'Gemini' in str(external_apis) else " External API"
            lines.append(" " * 18 + "|" + api_label)
            lines.append(" " * 28 + "v")
    
    # External API 박스
    if api_box:
        for line in api_box:
            lines.append(" " * 20 + line)
    
    lines.append("")
    lines.append("=" * 70)
    
    # 범례
    lines.append("")
    lines.append("범례:")
    lines.append("  <--->  양방향 통신")
    lines.append("  |      데이터 흐름")
    lines.append("  v      방향 표시")
    lines.append("")
    
    # === 자세한 설명 추가 ===
    lines.append("설명:")
    lines.append("")
    
    explanation_num = 1
    
    # 1. 사용자는 Streamlit UI를 통해 애플리케이션과 상호작용합니다.
    lines.append(f"{explanation_num}. 사용자는 Streamlit UI를 통해 애플리케이션과 상호작용합니다.")
    explanation_num += 1
    
    # 2. Streamlit UI는 Home.py와 data/demo.css 등을 통해 초기화되고 스타일링됩니다.
    if ui_files or entry_files:
        ui_examples = []
        for item in layer2_items[:2]:
            name = item.split('/')[-1] if '/' in item else item
            ui_examples.append(f"`{name}`")
        ui_text = "와 ".join(ui_examples) if ui_examples else "`Home.py`"
        lines.append(f"{explanation_num}. Streamlit UI는 {ui_text} 등을 통해 초기화되고 스타일링됩니다.")
    else:
        lines.append(f"{explanation_num}. Streamlit UI는 `Home.py` 등을 통해 초기화되고 스타일링됩니다.")
    explanation_num += 1
    
    # 3. 사용자가 페이지를 선택하면, Streamlit UI는 해당 pages/*.py 파일의 로직을 실행합니다.
    if page_files:
        page_example = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
        lines.append(f"{explanation_num}. 사용자가 페이지를 선택하면, Streamlit UI는 해당 {page_example} 파일의 로직을 실행합니다.")
        explanation_num += 1
    
    # 4. ** pages/*.py **는 사용자 입력을 받아 필요한 경우 ** module/*.py **를 호출합니다.
    if page_files and module_files:
        page_ex = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
        mod_ex = f"`{module_files[0]}`" if module_files else "`module/github.py`"
        lines.append(f"{explanation_num}. ** {page_ex} **는 사용자 입력을 받아 필요한 경우 ** {mod_ex} **를 호출하여 GitHub 데이터를 가져옵니다.")
        explanation_num += 1
    
    # 5. ** module/github.py **는 GitHub API와 통신하여 리포지토리 정보를 가져옵니다.
    if module_files:
        github_module = None
        gemini_module = None
        gpt_module = None
        
        for mf in module_files:
            if 'github' in mf.lower():
                github_module = mf
            elif 'gemini' in mf.lower():
                gemini_module = mf
            elif 'gpt' in mf.lower():
                gpt_module = mf
        
        if github_module:
            page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
            lines.append(f"{explanation_num}. ** `{github_module}` **는 GitHub API와 통신하여 리포지토리 정보를 가져옵니다. ** {page_ref} **로 반환됩니다.")
            explanation_num += 1
        
        # 6. ** pages/*.py **는 가져온 데이터를 ** module/gemini.py **로 전달하여 AI 분석을 요청합니다.
        if page_files and (gemini_module or gpt_module):
            ai_module = gemini_module or gpt_module
            page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
            lines.append(f"{explanation_num}. ** {page_ref} **는 가져온 데이터를 ** `{ai_module}` **로 전달하여 AI 분석을 요청합니다.")
            explanation_num += 1
        
        # 7. ** module/gpt.py / module/gemini.py **는 OpenAI / Gemini API와 통신하여 AI 분석 결과를 가져옵니다.
        if gpt_module and gemini_module:
            page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
            lines.append(f"{explanation_num}. ** `{gpt_module}` / `{gemini_module}` **는 OpenAI / Gemini API와 통신하여 AI 분석 결과를 가져옵니다. ** {page_ref} **로 반환됩니다.")
            explanation_num += 1
        elif gemini_module:
            page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
            lines.append(f"{explanation_num}. ** `{gemini_module}` **는 Gemini API와 통신하여 AI 분석 결과를 가져옵니다. ** {page_ref} **로 반환됩니다.")
            explanation_num += 1
        elif gpt_module:
            page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
            lines.append(f"{explanation_num}. ** `{gpt_module}` **는 OpenAI API와 통신하여 AI 분석 결과를 가져옵니다. ** {page_ref} **로 반환됩니다.")
            explanation_num += 1
    
    # 8. ** pages/*.py **는 최종 결과를 Streamlit UI를 통해 사용자에게 표시합니다.
    if page_files:
        page_ref = f"`{page_files[0]}`" if page_files else "`pages/*.py`"
        lines.append(f"{explanation_num}. ** {page_ref} **는 최종 결과를 Streamlit UI를 통해 사용자에게 표시합니다.")
        explanation_num += 1
    
    lines.append("")
    
    # 분석 요약
    lines.append("분석 결과:")
    lines.append(f"  • 전체 파일: {len(all_files)}개")
    if entry_files or ui_files:
        lines.append(f"  • 진입점/UI: {len(entry_files) + len(ui_files)}개")
    if page_files:
        lines.append(f"  • 페이지: {len(page_files)}개")
    if module_files:
        lines.append(f"  • 모듈: {len(module_files)}개")
    if external_apis:
        lines.append(f"  • 외부 API: {', '.join(external_apis)}")
    
    return "\n".join(lines)


# ---------------------------------------------------
# Check prerequisites
    
    for f in all_files:
        name_lower = f['name'].lower()
        path_lower = f['path'].lower()
        
        # UI/진입점 파일
        if any(p in name_lower for p in ['home.py', 'main.py', 'app.py', 'index.html', '__init__.py', 'streamlit']):
            if 'pages/' not in path_lower:  # pages 폴더 내부는 제외
                ui_files.append(f)
        
        # Pages 폴더
        elif 'pages/' in path_lower or 'page/' in path_lower:
            page_files.append(f)
        
        # Components 폴더
        elif 'component' in path_lower:
            component_files.append(f)
        
        # Module/Src/Lib 폴더
        elif any(p in path_lower for p in ['module/', 'modules/', 'src/', 'lib/']):
            module_files.append(f)
    
    # 외부 API 감지
    external_apis = []
    if source_code:
        api_keywords = {
            'openai': 'OpenAI',
            'gpt': 'GPT API',
            'gemini': 'Gemini',
            'anthropic': 'Claude',
            'github.com/api': 'GitHub API',
            'api.github.com': 'GitHub API'
        }
        
        detected = set()
        for code in source_code.values():
            code_lower = code.lower()
            for keyword, api_name in api_keywords.items():
                if keyword in code_lower and api_name not in detected:
                    detected.add(api_name)
        
        external_apis = list(detected)
    
    # 기본값 설정
    if not external_apis:
        external_apis = ['External APIs']
    
    # ASCII 다이어그램 생성
    lines = []
    lines.append("")
    
    # User 박스
    user_box = [
        "+--------------+",
        "|     User     |",
        "+--------------+"
    ]
    
    # UI 박스 생성
    ui_items = [f['name'] for f in ui_files[:3]] if ui_files else ['Application']
    max_ui_len = max(len(item) for item in ui_items)
    ui_width = max(max_ui_len + 4, 18)
    
    ui_box = []
    ui_box.append("+" + "-" * ui_width + "+")
    for item in ui_items:
        ui_box.append("| " + item.ljust(ui_width - 2) + " |")
    ui_box.append("+" + "-" * ui_width + "+")
    
    # Level 1: User <---> UI
    lines.append("  " + user_box[0] + "        " + ui_box[0])
    lines.append("  " + user_box[1] + " <----> " + ui_box[1])
    lines.append("  " + user_box[2] + "        " + ui_box[2])
    for i in range(3, len(ui_box)):
        lines.append(" " * 25 + ui_box[i])
    
    # 화살표
    lines.append(" " * 25 + "^")
    lines.append(" " * 25 + "|")
    lines.append(" " * 25 + "|")
    lines.append(" " * 25 + "v")
    
    # Level 2: Pages (있으면)
    if page_files:
        page_items = [f['name'] for f in page_files[:3]]
        # (각 페이지 주석) 추가
        page_items_display = [f"{item} (각 페이지 주석)" if i == 0 else item 
                             for i, item in enumerate(page_items)]
        
        max_page_len = max(len(item) for item in page_items_display)
        page_width = max(max_page_len + 4, 20)
        
        page_box = []
        page_box.append("+" + "-" * page_width + "+")
        for item in page_items_display:
            page_box.append("| " + item.ljust(page_width - 2) + " |")
        page_box.append("+" + "-" * page_width + "+")
        
        for line in page_box:
            lines.append(" " * 18 + line)
        
        lines.append(" " * 25 + "^")
        lines.append(" " * 25 + "|")
        lines.append(" " * 25 + "|")
        lines.append(" " * 25 + "v")
    
    # Level 3: Modules (있으면)
    if module_files:
        mod_items = [f['name'] for f in module_files[:3]]
        max_mod_len = max(len(item) for item in mod_items)
        mod_width = max(max_mod_len + 4, 20)
        
        mod_box = []
        mod_box.append("+" + "-" * mod_width + "+")
        for item in mod_items:
            mod_box.append("| " + item.ljust(mod_width - 2) + " |")
        mod_box.append("+" + "-" * mod_width + "+")
        
        for line in mod_box:
            lines.append(" " * 18 + line)
        
        lines.append(" " * 25 + "^")
        lines.append(" " * 25 + "|")
    elif component_files:
        # module이 없으면 component 표시
        comp_items = [f['name'] for f in component_files[:3]]
        max_comp_len = max(len(item) for item in comp_items)
        comp_width = max(max_comp_len + 4, 20)
        
        comp_box = []
        comp_box.append("+" + "-" * comp_width + "+")
        for item in comp_items:
            comp_box.append("| " + item.ljust(comp_width - 2) + " |")
        comp_box.append("+" + "-" * comp_width + "+")
        
        for line in comp_box:
            lines.append(" " * 18 + line)
        
        lines.append(" " * 25 + "^")
        lines.append(" " * 25 + "|")
    
    # External API 레이블
    if external_apis:
        api_label = " | " + " / ".join(external_apis[:2])
        lines.append(" " * 16 + api_label)
        lines.append(" " * 25 + "v")
        lines.append("")
        
        # External API 박스
        max_api_len = max(len(api) for api in external_apis)
        api_width = max(max_api_len + 4, 20)
        
        api_box = []
        api_box.append("+" + "-" * api_width + "+")
        for api in external_apis[:3]:
            api_box.append("| " + api.ljust(api_width - 2) + " |")
        api_box.append("+" + "-" * api_width + "+")
        
        for line in api_box:
            lines.append(" " * 18 + line)
    
    lines.append("")
    lines.append("=" * 60)
    
    # 범례
    lines.append("")
    lines.append("범례:")
    lines.append("  <---->  양방향 통신")
    lines.append("  |       데이터 흐름")
    lines.append("  v       방향 표시")
    lines.append("  ^       역방향")
    lines.append("")
    
    # 분석 결과 요약
    lines.append("분석 결과:")
    lines.append(f"  • 전체 코드 파일: {len(all_files)}개")
    lines.append(f"  • UI/진입점: {len(ui_files)}개")
    if page_files:
        lines.append(f"  • 페이지: {len(page_files)}개")
    if module_files:
        lines.append(f"  • 모듈: {len(module_files)}개")
    if component_files:
        lines.append(f"  • 컴포넌트: {len(component_files)}개")
    if external_apis:
        lines.append(f"  • 외부 API: {', '.join(external_apis)}")
    
    return "\n".join(lines)


# ---------------------------------------------------
# Check prerequisites
# ---------------------------------------------------
# ---------------------------------------------------
if not (options.get("api_key") and options.get("repository_url")):
    st.error("⛔ Home 페이지에서 먼저 설정을 완료해주세요!")
    st.info("""
### 🔰 처음 사용하시나요?

1. 왼쪽 사이드바에서 **Home** 클릭
2. API Token 입력
3. GitHub URL 입력
4. 다시 이 페이지로 오기
    """)
    st.stop()

# API Key validation
with st.spinner("API 키 확인 중..."):
    if not gemini.api_check(api_key):
        st.error("❌ API 키가 올바르지 않아요.")
        st.stop()
>>>>>>> Stashed changes

# Parse GitHub URL
parsed_url = parse_github_url(repository_url)
if not parsed_url:
    st.error("❌ GitHub 주소가 올바르지 않아요.")
    st.stop()

owner = parsed_url["owner"]
repo = parsed_url["repo"]

# ---------------------------------------------------
<<<<<<< Updated upstream
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
=======
# Page Header
# ---------------------------------------------------
st.markdown('<h1 class="main-title">📡 Repository Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.</p>', unsafe_allow_html=True)

st.divider()

st.markdown('<h2 class="section-header">🔍 Code Flow Analysis</h2>', unsafe_allow_html=True)
st.markdown("코드의 실행 흐름, 모듈 간 의존성, 데이터 흐름을 AI가 분석합니다.")

# ---------------------------------------------------
# Repository Info Display
# ---------------------------------------------------
with st.expander("📦 저장소 정보", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**저장소 URL:**")
        st.code(repository_url, language=None)
    with col2:
        st.markdown(f"**소유자:** `{owner}`")
        st.markdown(f"**저장소:** `{repo}`")

st.divider()

# ---------------------------------------------------
# Analysis Options
# ---------------------------------------------------
st.markdown('<h3 class="section-header">⚙️ 분석 옵션</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    analysis_depth = st.selectbox(
        "분석 깊이",
        ["Basic (File Tree Only)", "Detailed (Include Source Code)"],
        help="Basic: 파일 구조만 분석. Detailed: 실제 소스 코드 포함."
    )

with col2:
    max_files = st.slider(
        "최대 분석 파일 수",
        min_value=1,
        max_value=10,
        value=5,
        help="분석할 소스 파일 개수 (Detailed 모드만 해당)"
    )

# File extensions to analyze
file_extensions = st.multiselect(
    "분석할 파일 확장자 (Detailed 모드)",
    [".py", ".js", ".java", ".cpp", ".ts", ".go", ".rs", ".rb", ".php"],
    default=[".py"],
    help="상세 분석에 포함할 파일 타입을 선택하세요"
)

# Branch selection - 동적으로 가져오기
st.markdown("**브랜치 선택**")
col_branch1, col_branch2 = st.columns([3, 1])

with col_branch1:
    # 기본 브랜치 옵션
    available_branches = ["main", "master", "develop", "dev"]
    
    # GitHub API로 실제 브랜치 가져오기 시도
    try:
        branches_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        response = requests.get(branches_url, timeout=5)
        if response.status_code == 200:
            fetched_branches = [b['name'] for b in response.json()]
            if fetched_branches:
                available_branches = fetched_branches[:20]  # 최대 20개
    except:
        pass  # 실패하면 기본값 사용
    
    branch = st.selectbox(
        "브랜치를 선택하세요",
        available_branches,
        help="분석할 브랜치를 선택하세요"
    )

with col_branch2:
    st.markdown("&nbsp;")  # 공백
    if st.button("🔄 새로고침", help="브랜치 목록 새로고침"):
        st.rerun()

st.divider()

# ---------------------------------------------------
# AI Comment (Main Analysis Section)
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🤖 AI 분석</h3>', unsafe_allow_html=True)

# Initialize session state for analysis results
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'file_tree' not in st.session_state:
    st.session_state.file_tree = None
if 'source_code' not in st.session_state:
    st.session_state.source_code = None
if 'analysis_metadata' not in st.session_state:
    st.session_state.analysis_metadata = {}

if st.button("🔍 코드 흐름 분석 시작", type="primary", use_container_width=True):
    
    # Step 1: Fetch File Tree from GitHub
    with st.status("📁 GitHub에서 저장소 구조 가져오는 중...", expanded=True) as status:
        st.write(f"저장소: {owner}/{repo}")
        st.write(f"브랜치: {branch}")
        st.write("GitHub API로 파일 트리 가져오는 중...")
>>>>>>> Stashed changes
        
        try:
            file_tree = fetch_repository_tree(owner, repo, branch)
            
            if not file_tree:
<<<<<<< Updated upstream
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
=======
                st.error("❌ 저장소 구조를 가져오는데 실패했습니다. 저장소가 공개되어 있는지, URL이 올바른지 확인해주세요.")
                st.stop()
            
            file_count = count_files(file_tree)
            st.write(f"✅ {file_count}개 파일 발견")
            
            # Save to session state
            st.session_state.file_tree = file_tree
            
            # Display file tree preview
            with st.expander("📂 파일 트리 미리보기", expanded=False):
                st.json(file_tree)
            
            status.update(label=f"✅ 파일 트리 로드 완료! ({file_count}개 파일)", state="complete")
        
        except Exception as e:
            st.error(f"❌ 파일 트리 로드 중 오류: {str(e)}")
            st.stop()
    
    # Step 2: Get Source Code (if Detailed mode)
    source_code = None
    
    if analysis_depth == "Detailed (Include Source Code)":
        with st.status("💻 GitHub에서 소스 코드 가져오는 중...", expanded=True) as status:
            st.write(f"확장자로 파일 찾는 중: {', '.join(file_extensions)}")
            
            try:
                # 파일 찾기
                source_files = find_source_files(file_tree, file_extensions)
                
                if not source_files:
                    st.warning(f"⚠️ 해당 확장자의 파일을 찾을 수 없습니다: {file_extensions}")
                    st.info("파일 트리 분석만 계속 진행합니다...")
>>>>>>> Stashed changes
                else:
                    source_code = {}
                    files_fetched = 0
                    
<<<<<<< Updated upstream
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
=======
                    for filename, filepath in source_files[:max_files]:
                        st.write(f"📥 가져오는 중: `{filepath}`")
                        
                        # GitHub API로 파일 내용 가져오기
                        content = fetch_file_content(owner, repo, filepath, branch)
                        
                        if content and not content.startswith("# Error"):
                            # 2000자 제한
                            source_code[filepath] = content[:2000]
                            files_fetched += 1
                            st.write(f"✅ 완료: `{filepath}` ({len(content)}자)")
                        else:
                            st.warning(f"⚠️ 가져올 수 없음: `{filepath}`")
>>>>>>> Stashed changes
                        
                        if files_fetched >= max_files:
                            break
                    
                    if source_code:
<<<<<<< Updated upstream
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
=======
                        st.write(f"✅ {len(source_code)}개 파일 가져오기 성공")
                    else:
                        st.warning("⚠️ 소스 파일을 가져올 수 없습니다. 파일 트리만 사용합니다.")
                
                # Save to session state
                st.session_state.source_code = source_code
                
                status.update(label=f"✅ {len(source_code) if source_code else 0}개 소스 파일 가져옴", state="complete")
            
            except Exception as e:
                st.warning(f"⚠️ 소스 코드를 가져올 수 없습니다: {str(e)}")
                st.info("파일 트리 분석만 계속 진행합니다...")
    
    # Step 3: AI Analysis
    with st.status("🤖 Gemini AI로 코드 흐름 분석 중...", expanded=True) as status:
        st.write("Gemini AI로 데이터 전송 중...")
        st.write(f"언어: {language}")
        st.write(f"모드: {analysis_depth}")
        st.write(f"분석 중인 파일: {count_files(file_tree)}개")
        if source_code:
            st.write(f"소스 코드 샘플: {len(source_code)}개")
        
        try:
            # Call Gemini API
            # Gemini의 프롬프트에 이미 "5. Interaction Diagram" 섹션 포함됨
>>>>>>> Stashed changes
            result = gemini.api_code_flow_analysis(
                _key=api_key,
                _file_tree=file_tree,
                _source_code=source_code,
                _language=language
            )
            
            if result.startswith("Error:"):
<<<<<<< Updated upstream
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
=======
                st.error(f"❌ 분석 실패: {result}")
                st.stop()
            
            # 실제 저장소 기반 상호작용 다이어그램 생성
            interaction_diagram = create_interaction_diagram(file_tree, source_code)
            
            # Gemini의 Interaction Diagram 섹션을 실제 다이어그램으로 교체
            # "5." 또는 "**5." 패턴으로 시작하는 섹션 찾기
            import re
            
            # 패턴: "5. Interaction Diagram" 또는 "**5. Interaction Diagram**" 등
            pattern = r'(\*{0,2}5\.\s*(?:Interaction\s*Diagram|상호작용\s*다이어그램).*?)(?=\n\*{0,2}6\.|$)'
            
            if re.search(pattern, result, re.IGNORECASE | re.DOTALL):
                # Gemini가 Interaction Diagram 섹션을 생성했다면 교체
                replacement = f"""**5. 테스트중인 상호작용 다이어그램 (Interaction Diagram)**

시스템의 주요 구성 요소 간 상호작용을 시각화한 실제 다이어그램입니다 다만 아직 작업중이므로 아래 내용은 예시입니다:

```
{interaction_diagram}
```

**다이어그램 설명:**
이 다이어그램은 실제 저장소 구조를 분석하여 자동으로 생성되었습니다:
- **User**: 최종 사용자가 애플리케이션과 상호작용하는 진입점
- **UI/Application**: 사용자 인터페이스 또는 메인 애플리케이션 파일 (Home.py, main.py 등)
- **Pages/Routes**: 개별 페이지 또는 라우트 컴포넌트 (pages 폴더)
- **Modules/Services**: 비즈니스 로직 및 서비스 모듈 (module, src 폴더)
- **External APIs**: 외부 API 서비스 (OpenAI, Gemini, GitHub 등)

화살표 방향은 데이터 흐름 및 호출 관계를 나타내며, 실제 파일 구조와 소스 코드를 분석하여 생성되었습니다."""
                
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE | re.DOTALL)
            else:
                # Gemini가 섹션을 생성하지 않았다면 추가
                result += f"""

---

**5. 테스트중인 상호작용 다이어그램 (Interaction Diagram)**

시스템의 주요 구성 요소 간 상호작용을 시각화한 실제 다이어그램입니다:

```
{interaction_diagram}
```

**다이어그램 설명:**
이 다이어그램은 실제 저장소 구조를 분석하여 자동으로 생성되었습니다:
- **User**: 최종 사용자가 애플리케이션과 상호작용하는 진입점
- **UI/Application**: 사용자 인터페이스 또는 메인 애플리케이션 파일
- **Pages/Routes**: 개별 페이지 또는 라우트 컴포넌트
- **Modules/Services**: 비즈니스 로직 및 서비스 모듈
- **External APIs**: 외부 API 서비스 (OpenAI, Gemini, GitHub 등)

화살표 방향은 데이터 흐름 및 호출 관계를 나타냅니다.
"""
            
            status.update(label="✅ 분석 완료!", state="complete")
        
        except Exception as e:
            st.error(f"❌ AI 분석 오류: {str(e)}")
            st.stop()
    
    # Save results to session state
    st.session_state.analysis_result = result
    st.session_state.analysis_metadata = {
        'repository_url': repository_url,
        'owner': owner,
        'repo': repo,
        'branch': branch,
        'language': language,
        'analysis_depth': analysis_depth,
        'file_count': count_files(file_tree)
    }
    
    # Step 4: Display Results
    st.success("✅ 코드 흐름 분석 완료!")

# Display results if available in session state
if st.session_state.analysis_result:
    st.divider()
    st.markdown('<h3 class="section-header">📊 분석 결과</h3>', unsafe_allow_html=True)
    
    # Get data from session state
    result = st.session_state.analysis_result
    file_tree = st.session_state.file_tree
    source_code = st.session_state.source_code
    metadata = st.session_state.analysis_metadata
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 전체 분석", "📥 다운로드", "📊 시각화"])
    
    with tab1:
        st.markdown("### 📋 완전한 분석 결과")
        st.markdown(result)
    
    with tab2:
        st.markdown("### 📥 분석 보고서 다운로드")
        
        # Create formatted report
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 코드 흐름 분석 보고서

**저장소:** {metadata.get('repository_url', repository_url)}
**소유자:** {metadata.get('owner', owner)}
**저장소 이름:** {metadata.get('repo', repo)}
**브랜치:** {metadata.get('branch', 'main')}
**분석 날짜:** {timestamp}
**언어:** {metadata.get('language', language)}
**분석 모드:** {metadata.get('analysis_depth', analysis_depth)}
**분석된 파일:** {metadata.get('file_count', 0)}개
>>>>>>> Stashed changes

---

{result}

---

<<<<<<< Updated upstream
## File Tree Structure
=======
## 파일 트리 구조
>>>>>>> Stashed changes
```json
{json.dumps(file_tree, indent=2, ensure_ascii=False)}
```

---

<<<<<<< Updated upstream
*Generated by Repository Radar using Gemini AI*
=======
*Repository Radar가 Gemini AI를 사용하여 생성했습니다*
>>>>>>> Stashed changes
"""
        
        col1, col2 = st.columns(2)
        
<<<<<<< Updated upstream
        # 마크다운 파일 다운로드
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=report,
                file_name=f"code_flow_analysis_{owner}_{repo}.md",
=======
        with col1:
            st.download_button(
                label="📥 Markdown으로 다운로드",
                data=report,
                file_name=f"code_flow_analysis_{metadata.get('owner', owner)}_{metadata.get('repo', repo)}.md",
>>>>>>> Stashed changes
                mime="text/markdown",
                use_container_width=True
            )
        
<<<<<<< Updated upstream
        # 텍스트 파일 다운로드
        with col2:
            st.download_button(
                label="📥 Download as Text",
                data=result,
                file_name=f"code_flow_analysis_{owner}_{repo}.txt",
=======
        with col2:
            st.download_button(
                label="📥 텍스트로 다운로드",
                data=result,
                file_name=f"code_flow_analysis_{metadata.get('owner', owner)}_{metadata.get('repo', repo)}.txt",
>>>>>>> Stashed changes
                mime="text/plain",
                use_container_width=True
            )
    
    with tab3:
<<<<<<< Updated upstream
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
=======
        st.markdown("### 📊 6가지 시각화 차트")
        st.info("💡 **순수 코드 구조/흐름 분석**에 집중한 시각화입니다. 설치 관련 정보는 '02_환경 설정 가이드'에서 확인하세요!")
        
        st.markdown("#### 🌊 폴더-파일 흐름도")
        st.info("최상위 폴더부터 파일까지의 흐름을 보여줍니다. 클릭해서 탐색하세요!")
        st.plotly_chart(create_folder_file_flow(file_tree), use_container_width=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚀 시작 파일 찾기")
            st.info("main.py, app.py 같은 시작점을 자동으로 발견합니다")
            st.plotly_chart(find_entry_points(file_tree), use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 기술 스택 파악")
            st.info("사용된 프로그래밍 언어와 파일 비율을 보여줍니다")
            st.plotly_chart(analyze_tech_stack(file_tree), use_container_width=True)
        
        st.divider()
        
        st.markdown("#### ☀️ 파일 종류 분포")
        st.info("파일을 확장자별로 그룹화하여 태양계처럼 보여줍니다")
        st.plotly_chart(file_type_distribution(file_tree), use_container_width=True)
        
        st.divider()
        
        st.markdown("#### 📁 중요한 폴더 순위")
        st.info("코드가 많은 폴더를 찾아 순위를 매깁니다. 핵심 로직 위치 파악에 유용합니다!")
        st.plotly_chart(important_folders(file_tree), use_container_width=True)
        
        st.divider()
        
        st.markdown("#### 🔗 테스트 진행 중인 상호작용 다이어그램")
        st.info("파일 간 import/의존성 관계를 ASCII 다이어그램으로 보여줍니다!")
        
        # source_code가 있으면 실제 import 분석, 없으면 추정
        if source_code:
            st.success(f"✅ {len(source_code)}개 파일의 실제 import 관계를 분석했습니다")
        else:
            st.warning("⚠️ 소스 코드가 없어 파일 구조 기반으로 관계를 추정했습니다. 'Detailed' 모드로 분석하면 더 정확합니다!")
        
        diagram_text = create_interaction_diagram(file_tree, source_code)
        st.code(diagram_text, language=None)

else:
    st.info("👆 버튼을 눌러서 코드 흐름 분석을 시작하세요!")

# ---------------------------------------------------
# Additional Features
# ---------------------------------------------------
st.divider()

with st.expander("💡 더 나은 분석을 위한 팁"):
    st.markdown("""
    **최상의 결과를 위해:**
    
    1. **공개 저장소 사용**: GitHub API는 공개 저장소에서 가장 잘 작동합니다
    2. **브랜치 이름 확인**: 기본값은 'main'이지만, 일부 저장소는 'master'를 사용합니다
    3. **관련 확장자 선택**: 주요 언어 파일에 집중하세요
    4. **파일 수 제한**: Detailed 분석에는 3-5개 파일을 권장합니다
    5. **진입점 포함**: `main.py`, `app.py`, `index.js` 같은 파일을 포함하세요
    
    **분석 대상:**
    
    - 📁 디렉토리 구조 및 구성
    - 🔗 모듈 import 및 의존성
    - 📊 함수 호출 체인
    - 🔄 컴포넌트 간 데이터 흐름
    - ⚡ 성능 중요 경로
    - 🎯 진입점 및 초기화
    
    **GitHub API 제한사항:**
    
    - 요청 제한: 시간당 60개 (인증 없음)
    - 저장소는 공개되어야 함
    - 큰 파일은 잘릴 수 있음
    """)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.divider()

st.markdown("""
<div style="text-align: center; color: #9aa0a6; padding: 1rem 0; font-family: 'Plus Jakarta Sans', sans-serif;">
    <p style="font-size: 0.9rem;">Gemini AI 기반 | 코드 흐름 분석 v2.0 | 저장소: {}/{}</p>
</div>
""".format(owner, repo), unsafe_allow_html=True)
>>>>>>> Stashed changes
