# pages/02_⚙️EnvironmentSetup.py (최적화 및 간소화 버전)
# ---------------------------------------------------
# GitHub Repository: Development-RepositorieRadar
# Author: minjunkim0205, Assadgang, Gplexs, han183536-ux
# Description: 저장소 구조 분석기
# Version: 1.0.1 자동환경설정 가이드
# ---------------------------------------------------
# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import streamlit as st
import json
import requests
from pathlib import Path
import time
import re
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Environment Setup",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------
# 세련된 분석 도구 디자인을 위한 커스텀 CSS
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
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    /* 정보 카드 */
    .info-card {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .info-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    /* 코드 블록 스타일 */
    .stCodeBlock {
        background: rgba(26, 31, 58, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    code {
        background: rgba(26, 31, 58, 0.6) !important;
        color: #e8eaed !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Expander 스타일 */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 58, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #e8eaed !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(102, 126, 234, 0.3) !important;
        background: rgba(26, 31, 58, 0.8) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 31, 58, 0.4) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
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
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* 정보 박스 스타일 */
    .stAlert {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        color: #e8eaed !important;
    }
    
    /* Alert 내부 텍스트만 폰트 적용 */
    .stAlert > div {
        font-family: 'Plus Jakarta Sans', sans-serif;
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
        background: rgba(102, 126, 234, 0.1) !important;
        color: #667eea !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #0a0e27 !important;
    }
    
    /* Download 버튼 */
    .stDownloadButton > button {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        color: #667eea !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: rgba(102, 126, 234, 0.5) !important;
        background: rgba(26, 31, 58, 0.8) !important;
        transform: translateY(-2px);
    }
    
    /* Status 컨테이너 */
    .stStatus {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
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
    .stSelectbox > div > div > div {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 8px !important;
        color: #e8eaed !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Label 스타일 */
    .stTextInput > label,
    .stSelectbox > label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e8eaed !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* 프로세스 단계 스타일 */
    .process-step {
        background: rgba(26, 31, 58, 0.4);
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load state
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# 토큰 최적화 함수
# ---------------------------------------------------
def summarize_file_tree(tree: dict, max_files: int = 80) -> dict:
    """
    파일 트리를 요약해서 토큰 사용량 90% 감소
    
    전략:
    1. 중요한 파일만 선택 (설정 파일, 메인 파일)
    2. 깊이 제한 (3단계까지만)
    3. 파일 개수 제한 (80개까지)
    """
    
    # 중요한 파일 확장자
    important_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx',
        '.java', '.go', '.rs', '.cpp', '.c',
        '.json', '.yaml', '.yml', '.toml',
        '.md', '.txt', '.sh', '.bat'
    }
    
    # 중요한 파일명
    important_files = {
        'README.md', 'package.json', 'requirements.txt',
        'Dockerfile', 'docker-compose.yml', 'Makefile',
        'setup.py', 'pyproject.toml', 'pom.xml',
        'build.gradle', '.env.example', 'main.py',
        'app.py', 'index.js', 'main.go', 'manage.py',
        'settings.py', 'config.py', 'webpack.config.js'
    }
    
    summary = {
        "important_files": [],
        "directory_structure": {},
        "file_stats": {
            "total_files": 0,
            "by_extension": {}
        }
    }
    
    def extract_files(node, current_path="", depth=0, file_list=[]):
        """재귀적으로 중요한 파일만 추출"""
        if depth > 3:  # 깊이 제한
            return file_list
        
        for name, value in node.items():
            if not isinstance(value, dict):
                continue
            
            full_path = f"{current_path}/{name}" if current_path else name
            
            if value.get("type") == "file":
                ext = value.get("extension", "")
                size = value.get("size", 0)
                
                # 통계
                summary["file_stats"]["total_files"] += 1
                summary["file_stats"]["by_extension"][ext] = \
                    summary["file_stats"]["by_extension"].get(ext, 0) + 1
                
                # 중요한 파일만 포함
                if name in important_files or ext in important_extensions:
                    if len(file_list) < max_files:
                        file_list.append({
                            "path": full_path,
                            "name": name,
                            "extension": ext,
                            "size": size
                        })
            
            elif value.get("type") == "directory":
                # 1단계 디렉토리 구조만 저장
                if depth == 0:
                    summary["directory_structure"][name] = "directory"
                
                extract_files(
                    value.get("contents", {}),
                    full_path,
                    depth + 1,
                    file_list
                )
        
        return file_list
    
    summary["important_files"] = extract_files(tree)
    
    return summary

def api_call_with_retry(api_func, max_retries=3, **kwargs):
    """
    429 에러 발생 시 자동 재시도
    """
    for attempt in range(max_retries):
        try:
            result = api_func(**kwargs)
            
            # 에러 체크
            if isinstance(result, str) and "Error: 429" in result:
                error_msg = result
                
                # 재시도 시간 추출
                match = re.search(r'retry in ([\d.]+)s', error_msg)
                if match:
                    wait_time = float(match.group(1))
                else:
                    wait_time = 40.0 * (2 ** attempt)
                
                if attempt < max_retries - 1:
                    st.warning(f"⏳ API 사용량 제한! {wait_time:.1f}초 후 재시도... (시도 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    return result
            
            return result
        
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = 40.0 * (2 ** attempt)
                
                if attempt < max_retries - 1:
                    st.warning(f"⏳ API 제한! {wait_time:.1f}초 후 재시도...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise
    
    return None

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    if not url:
        return None
    try:
        parts = url.replace("https://github.com/", "").split("/")
        return {"owner": parts[0], "repo": parts[1]}
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_readme(owner: str, repo: str) -> str:
    readme_names = ["README.md", "README.txt", "README", "readme.md"]
    for name in readme_names:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{name}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                import base64
                content = base64.b64decode(response.json()["content"]).decode("utf-8")
                return content
        except:
            continue
    return ""

@st.cache_data(ttl=3600)
def fetch_repository_tree(owner: str, repo: str, branch: str = "main") -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code in [401, 404]:
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
            response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        tree = {}
        for item in data.get("tree", []):
            path = item["path"]
            item_type = item["type"]
            ignore = ['.git', '__pycache__', 'node_modules', '.venv']
            if any(ig in path for ig in ignore):
                continue
            
            parts = path.split("/")
            current = tree
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    if item_type == "blob":
                        current[part] = {
                            "type": "file",
                            "size": item.get("size", 0),
                            "extension": Path(part).suffix,
                            "path": path
                        }
                else:
                    if part not in current:
                        current[part] = {"type": "directory", "contents": {}}
                    current = current[part].get("contents", current[part])
        return tree
    except:
        return {}

def detect_project_type(tree: dict) -> dict:
    indicators = {
        "Python": [".py", "requirements.txt", "setup.py", "pyproject.toml"],
        "Node.js": ["package.json", "package-lock.json", "yarn.lock"],
        "Java": [".java", "pom.xml", "build.gradle"],
        "React": ["package.json", ".jsx", ".tsx"],
        "Django": ["manage.py", "settings.py"],
        "Flask": ["app.py", "wsgi.py"],
        "Spring": ["pom.xml", "application.properties"]
    }
    
    detected = {}
    
    def check_files(node):
        files = []
        for name, value in node.items():
            if isinstance(value, dict):
                if value.get("type") == "file":
                    files.append(name)
                    files.append(value.get("extension", ""))
                elif value.get("type") == "directory":
                    files.extend(check_files(value.get("contents", {})))
        return files
    
    all_files = check_files(tree)
    all_files_str = " ".join(all_files)
    
    for tech, patterns in indicators.items():
        count = sum(1 for p in patterns if p in all_files_str)
        if count > 0:
            detected[tech] = count
    
    return detected

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")
st.sidebar.info("💡 이 페이지는 **프로젝트를 설치하고 실행하는 방법**을 알려줍니다!")

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

language = st.sidebar.selectbox(
    "🌏 응답 언어",
    ["Korean", "English"],
    index=0,
    help="AI가 답변할 언어를 선택하세요"
)

st.sidebar.divider()

with st.sidebar.expander("❓ 이 페이지는 뭐하는 곳인가요?"):
    st.markdown("""
    ### 🎯 목적
    
    GitHub에서 다운받은 프로젝트를
    **내 컴퓨터에서 실행하는 방법**을
    단계별로 알려드립니다!
    
    ### 📚 배울 수 있는 것
    
    1. 어떤 프로그램을 설치해야 하는지
    2. 어떤 명령어를 입력해야 하는지
    3. 어떻게 실행하는지
    4. 문제가 생기면 어떻게 해결하는지
    """)

if repository_url:
    parsed = parse_github_url(repository_url)
    if parsed:
        st.sidebar.success(f"✅ **{parsed['repo']}** 프로젝트")

# ---------------------------------------------------
# Check Prerequisites
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

with st.spinner("API 키 확인 중..."):
    if not gemini.api_check(api_key):
        st.error("❌ API 키가 올바르지 않아요.")
        st.stop()

parsed_url = parse_github_url(repository_url)
if not parsed_url:
    st.error("❌ GitHub 주소가 올바르지 않아요.")
    st.stop()

owner = parsed_url["owner"]
repo = parsed_url["repo"]

# ---------------------------------------------------
# Page Header
# ---------------------------------------------------
st.markdown('<h1 class="main-title">📡 Repository Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">누구나 쉽게 GitHub 프로젝트를 이해하고 실행할 수 있어요!</p>', unsafe_allow_html=True)

st.divider()

st.markdown('<h2 class="section-header">⚙️ 환경 설정 가이드</h2>', unsafe_allow_html=True)

st.markdown(f"""
### 👋 안녕하세요! 

**{repo}** 프로젝트를 여러분의 컴퓨터에서 실행하는 방법을 알려드릴게요!
""")

# ---------------------------------------------------
# 간결한 정보 카드
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>📚 배울 내용</h4>
        <p>• 필요한 프로그램<br>
        • 설치 명령어<br>
        • 실행 방법</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>⏱️ 소요 시간</h4>
        <p>• 5-10분 정도<br>
        • 천천히 따라하세요!<br>
        • 단계별로 진행</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>💡 준비물</h4>
        <p>• 컴퓨터<br>
        • 인터넷 연결<br>
        • 텍스트 에디터</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# 프로젝트 분석 (간소화)
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🔍 프로젝트 파악하기</h3>', unsafe_allow_html=True)

with st.spinner("프로젝트 분석 중..."):
    file_tree = fetch_repository_tree(owner, repo)
    
    if file_tree:
        detected_types = detect_project_type(file_tree)
        
        if detected_types:
            primary_tech = max(detected_types, key=detected_types.get)
            
            tech_explanations = {
                "Python": "🐍 Python",
                "Node.js": "🟢 Node.js",
                "Java": "☕ Java",
                "React": "⚛️ React",
                "Django": "🎸 Django",
                "Flask": "🌶️ Flask",
            }
            
            tech_display = ", ".join([tech_explanations.get(t, t) for t in list(detected_types.keys())[:3]])
            st.success(f"✅ 프로젝트 타입: {tech_display}")
        else:
            st.info("📊 프로젝트 구조 분석 완료")

st.divider()

# ---------------------------------------------------
# AI 가이드 생성 (깔끔하게 정리)
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🤖 AI 설치 가이드 생성</h3>', unsafe_allow_html=True)

# 프로세스 단계를 깔끔하게 표시
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.5rem; margin-bottom: 1.5rem;">
    <div class="process-step">1️⃣ README 찾기</div>
    <div class="process-step">2️⃣ 파일 구조 분석</div>
    <div class="process-step">3️⃣ AI 가이드 작성</div>
    <div class="process-step">4️⃣ 결과 확인</div>
    <div class="process-step">5️⃣ 다운로드</div>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 설치 가이드 만들기", type="primary", use_container_width=True):
    
    # 1단계: README
    with st.status("📄 README 파일 찾는 중...", expanded=False) as status:
        readme_content = fetch_readme(owner, repo)
        
        if readme_content:
            st.write(f"✅ README 발견! ({len(readme_content)}자)")
            readme_content = readme_content[:5000]
        else:
            st.write("⚠️ README 없음. 파일 구조로 분석할게요.")
        
        status.update(label="✅ README 완료", state="complete")
    
    # 2단계: 파일 구조
    with st.status("📦 파일 구조 요약 중...", expanded=False) as status:
        if not file_tree:
            file_tree = fetch_repository_tree(owner, repo)
        
        summarized_tree = summarize_file_tree(file_tree, max_files=80)
        
        st.write(f"✅ {len(summarized_tree['important_files'])}개 주요 파일 선택")
        
        status.update(label="✅ 파일 구조 완료", state="complete")
    
    # 3단계: AI 분석
    with st.status("🤖 AI가 가이드 작성 중...", expanded=False) as status:
        try:
            result = api_call_with_retry(
                api_func=gemini.api_environment_setup,
                max_retries=3,
                _key=api_key,
                _file_tree=summarized_tree,
                _readme=readme_content,
                _language=language
            )
            
            if result and result.startswith("Error:"):
                st.error(f"❌ 오류: {result}")
                st.info("""
                **💡 해결 방법:**
                1. 1-2분 후 다시 시도
                2. 더 작은 프로젝트로 테스트
                3. API 사용량 확인
                """)
                st.stop()
            
            status.update(label="✅ AI 분석 완료", state="complete")
        
        except Exception as e:
            st.error(f"❌ 에러: {str(e)}")
            st.stop()
    
    st.success("✅ 설치 가이드 생성 완료!")
    
    st.divider()
    
    # ---------------------------------------------------
    # 결과 표시 (깔끔하게)
    # ---------------------------------------------------
    st.markdown('<h3 class="section-header">📖 설치 가이드</h3>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 전체 가이드", "💾 다운로드"])
    
    with tab1:
        st.markdown(result)
    
    with tab2:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        
        report = f"""# {repo} 설치 가이드

**생성 날짜:** {timestamp}
**저장소:** {repository_url}

---

{result}
"""
        
        st.download_button(
            "📥 Markdown 파일로 다운로드",
            report,
            f"{repo}_가이드_{timestamp}.md",
            "text/markdown",
            use_container_width=True
        )

else:
    st.info("👆 버튼을 눌러서 가이드를 만들어보세요!")

st.divider()

st.markdown("""
<div style="text-align: center; color: #9aa0a6; padding: 1rem 0; font-family: 'Plus Jakarta Sans', sans-serif;">
    <p style="font-size: 0.9rem;">Made with ❤️ by Repository Radar | {}/{}</p>
</div>
""".format(owner, repo), unsafe_allow_html=True)