# 01_📊RepositoryStructure.py
# ---------------------------------------------------
# GitHub Repository: Development-RepositorieRadar
# Author: minjunkim0205, Assadgang, Gplexs, han183536-ux
# Description: 저장소 구조 분석기
# Version: 1.0.1 
# ---------------------------------------------------
# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import streamlit as st
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    """GitHub URL에서 owner/repo 추출"""
    if not url:
        return None
    try:
        parts = url.replace("https://github.com/", "").split("/")
        return {"owner": parts[0], "repo": parts[1]}
    except:
        return None

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Repository Structure",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# 세련된 분석 도구 디자인을 위한 커스텀 CSS (EnvironmentSetup과 동일)
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
    
    /* 코드 블록 스타일 */
    .stCodeBlock {
        background: rgba(26, 31, 58, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Code element 자체 */
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
    
    /* Expander content */
    .streamlit-expanderContent {
        background: rgba(26, 31, 58, 0.4) !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* AI 코멘트 박스 */
    .ai-comment-box {
        background: rgba(26, 31, 58, 0.5);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-family: 'Plus Jakarta Sans', sans-serif;
        line-height: 1.8;
        color: #bdc1c6;
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
    
    /* 에러 메시지 */
    .stAlert[data-baseweb="notification"] > div:first-child {
        background: rgba(26, 31, 58, 0.6) !important;
    }
    
    /* 섹션 타이틀 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e8eaed;
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
        color: #e8eaed;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #bdc1c6;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Input 박스 스타일 */
    .stTextInput > div > div > input {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 8px !important;
        color: #e8eaed !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Label 스타일 */
    .stTextInput > label,
    .stSelectbox > label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e8eaed;
        font-weight: 600;
    }
    
    /* Markdown 스타일 */
    .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Divider */
    hr {
        border-color: rgba(102, 126, 234, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load state into variables
# ---------------------------------------------------
options = st.session_state["options"]
contents = st.session_state["contents"]

# ---------------------------------------------------
# Sidebar(API,URL input)
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")
st.sidebar.info("💡 이 페이지는 **저장소의 전체 구조와 파일 트리**를 보여줍니다!")

api_key = st.sidebar.text_input(
    "🔑 GPT/Gemini API 키", 
    value=options["api_key"], 
    type="password", 
    disabled=True,
    help="Home 페이지에서 설정한 API 키"
)

repository_url = st.sidebar.text_input(
    "📊 GitHub 저장소 URL", 
    value=options["repository_url"], 
    disabled=True,
    help="Home 페이지에서 설정한 저장소 주소"
)

st.sidebar.divider()

with st.sidebar.expander("❓ 이 페이지는 뭐하는 곳인가요?"):
    st.markdown("""
    ### 🎯 목적
    
    GitHub 저장소의 **전체 파일 구조**를
    트리 형태로 보여주고,
    AI가 **구조를 분석**해줍니다!
    
    ### 📚 배울 수 있는 것
    
    1. 어떤 폴더가 있는지
    2. 어떤 파일이 있는지
    3. 프로젝트가 어떻게 구성되었는지
    4. 각 폴더의 역할은 무엇인지
    """)

if repository_url:
    parsed = parse_github_url(repository_url)
    if parsed:
        st.sidebar.success(f"✅ **{parsed['repo']}** 프로젝트")

# ---------------------------------------------------
# Page
# ---------------------------------------------------
if not (options["api_key"] and options["repository_url"]):
    st.error("⛔ Home 페이지에서 먼저 설정을 완료해주세요!")
    st.info("""
### 🔰 처음 사용하시나요?

1. 왼쪽 사이드바에서 **Home** 클릭
2. API Token 입력
3. GitHub URL 입력
4. 다시 이 페이지로 오기
    """)
    st.stop()

# 페이지 헤더
st.markdown('<h1 class="main-title">📡 Repository Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.</p>', unsafe_allow_html=True)

st.markdown("---")

st.markdown('<h2 class="section-header">📊 Repository Structure</h2>', unsafe_allow_html=True)

# ---------------------------------------------------
# File Tree
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🗃️ File Tree</h3>', unsafe_allow_html=True)

file_tree = contents["01"]["File Tree"]

with st.spinner("Wait for it...", show_time=True):
    if not file_tree:
        file_tree = github.url_tree_string(repository_url)
        contents["01"]["File Tree"] = file_tree
        st.session_state["contents"] = contents

    with st.expander("📁 파일 트리 보기/접기", expanded=True):
        st.code(file_tree, line_numbers=True)

# ---------------------------------------------------
# AI Comment
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🤖 AI Comment</h3>', unsafe_allow_html=True)

language = options["language"]
api_key = options["api_key"]
api_type = options["api_type"]
repository_url = options["repository_url"]
ai_comment = contents["01"]["AI Comment"]

with st.spinner("Wait for it...", show_time=True):
    if not ai_comment:
        if api_type == "GPT":
            ai_comment = gpt.api_repository_structure(api_key, github.url_tree_dict(repository_url), language)
        elif api_type == "GEMINI":
            ai_comment = gemini.api_repository_structure(api_key, github.url_tree_dict(repository_url), language)

        contents["01"]["AI Comment"] = ai_comment
        st.session_state["contents"] = contents
    
    st.markdown(f'<div class="ai-comment-box">{ai_comment}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9aa0a6; padding: 1rem 0; font-family: 'Plus Jakarta Sans', sans-serif;">
    <p style="font-size: 0.9rem;">Powered by Gemini AI | Repository Structure Analysis</p>
</div>
""", unsafe_allow_html=True)