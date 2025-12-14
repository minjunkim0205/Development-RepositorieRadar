<<<<<<< Updated upstream
# pages/04_📄IssueSummary.py
# ---------------------------------------------------
=======
# pages/04_📄IssueSummary.py (최적화 및 간소화 버전)
# ---------------------------------------------------
# GitHub Repository: Development-RepositorieRadar
# Author: minjunkim0205, Assadgang, Gplexs, han183536-ux
# Description: 자동 이슈 요약기
# Version: 1.0.1 
# ---------------------------------------------------
# ---------------------------------------------------
>>>>>>> Stashed changes
# 모듈 임포트
# ---------------------------------------------------
import streamlit as st
import json
import requests
from datetime import datetime
<<<<<<< Updated upstream
=======
from collections import Counter
>>>>>>> Stashed changes
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="Issue Summary",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------
<<<<<<< Updated upstream
# 세션 상태 불러오기
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# 헬퍼 함수들
# ---------------------------------------------------
=======
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
        border-bottom: 2px solid rgba(0, 245, 255, 0.2);
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0, 245, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 245, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #9aa0a6;
        margin-top: 0.5rem;
    }
    
    /* 이슈 카드 */
    .issue-card {
        background: rgba(26, 31, 58, 0.4);
        border-left: 3px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .issue-card:hover {
        background: rgba(26, 31, 58, 0.6);
        border-left-color: #8b5cf6;
        transform: translateX(4px);
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
    
    /* Checkbox */
    .stCheckbox {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* 섹션 타이틀 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e8eaed !important;
    }
    
    /* 일반 텍스트 */
    p, li {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #bdc1c6 !important;
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
        color: #bdc1c6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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
    
    /* 통계 요약 박스 */
    .stats-summary {
        background: rgba(26, 31, 58, 0.4);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 세션 상태 불러오기
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# 헬퍼 함수들
# ---------------------------------------------------
>>>>>>> Stashed changes
def parse_github_url(url: str) -> dict:
    """GitHub URL에서 owner와 repo 추출"""
    if not url:
        return None
    try:
        parts = url.replace("https://github.com/", "").split("/")
        return {"owner": parts[0], "repo": parts[1]}
    except:
        return None


<<<<<<< Updated upstream
def fetch_github_issues(owner: str, repo: str, state: str = "all", per_page: int = 30):
=======
def fetch_github_issues(owner: str, repo: str, state: str = "all", per_page: int = 100):
>>>>>>> Stashed changes
    """GitHub API로 이슈 목록 가져오기"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": per_page,
        "sort": "updated",
        "direction": "desc"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        issues = response.json()
        
        # 이슈 데이터 포맷팅
        formatted_issues = []
        for issue in issues:
            # Pull Request 제외
            if "pull_request" in issue:
                continue
            
            # body가 None인 경우 처리
            body = issue.get("body") or "No description"
            description = body[:500] if body else "No description"
            
            formatted_issues.append({
                "number": issue.get("number", 0),
                "title": issue.get("title", "Untitled"),
                "description": description,
                "labels": [label["name"] for label in issue.get("labels", [])],
                "state": issue.get("state", "open"),
                "created_at": issue.get("created_at", "")[:10],
                "updated_at": issue.get("updated_at", "")[:10],
                "url": issue.get("html_url", ""),
<<<<<<< Updated upstream
                "user": issue.get("user", {}).get("login", "Unknown")
=======
                "user": issue.get("user", {}).get("login", "Unknown"),
                "comments": issue.get("comments", 0)
>>>>>>> Stashed changes
            })
        
        return formatted_issues
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ GitHub API Error: {str(e)}")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        return []


<<<<<<< Updated upstream
# ---------------------------------------------------
# 사이드바 설정
# ---------------------------------------------------
st.sidebar.title("⚙️ Settings")

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

language = st.sidebar.selectbox(
    "Response Language",
    ["English", "Korean"],
    index=1
=======
def categorize_issue(labels: list) -> str:
    """이슈를 라벨 기반으로 카테고리화"""
    labels_lower = [l.lower() for l in labels]
    
    # 우선순위 순서대로 확인
    if any(x in labels_lower for x in ['bug', 'defect', 'error', 'crash']):
        return "🐛 Bug"
    elif any(x in labels_lower for x in ['good first issue', 'good-first-issue']):
        return "🌱 Good First Issue"
    elif any(x in labels_lower for x in ['help wanted', 'help-wanted']):
        return "🆘 Help Wanted"
    elif any(x in labels_lower for x in ['enhancement', 'feature', 'improvement']):
        return "✨ Enhancement"
    elif any(x in labels_lower for x in ['documentation', 'docs']):
        return "📝 Documentation"
    elif any(x in labels_lower for x in ['question', 'support']):
        return "❓ Question"
    elif any(x in labels_lower for x in ['wontfix', 'invalid', 'duplicate']):
        return "🚫 Won't Fix"
    else:
        return "📌 Other"


def get_priority(labels: list) -> str:
    """이슈 우선순위 판단"""
    labels_lower = [l.lower() for l in labels]
    
    if any(x in labels_lower for x in ['critical', 'urgent', 'high priority', 'p0']):
        return "🔴 Critical"
    elif any(x in labels_lower for x in ['high', 'important', 'p1']):
        return "🟠 High"
    elif any(x in labels_lower for x in ['medium', 'p2']):
        return "🟡 Medium"
    elif any(x in labels_lower for x in ['low', 'p3', 'minor']):
        return "🟢 Low"
    else:
        return "⚪ Normal"


# ---------------------------------------------------
# 사이드바 설정
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")
st.sidebar.info("💡 이 페이지는 **GitHub 이슈를 분석하고 요약**해줍니다!")

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
>>>>>>> Stashed changes
)

st.sidebar.divider()

<<<<<<< Updated upstream
=======
with st.sidebar.expander("❓ 이 페이지는 뭐하는 곳인가요?"):
    st.markdown("""
    ### 🎯 목적
    
    GitHub 저장소의 **이슈를 스마트하게 분석**하고
    **AI가 요약**해줍니다!
    
    ### 📚 배울 수 있는 것
    
    1. 어떤 이슈가 있는지
    2. 이슈 우선순위는 무엇인지
    3. 어떤 이슈부터 해결하면 좋을지
    4. 프로젝트의 건강 상태는 어떤지
    """)

>>>>>>> Stashed changes
# 레포지토리 정보 표시
if repository_url:
    parsed = parse_github_url(repository_url)
    if parsed:
<<<<<<< Updated upstream
        st.sidebar.success(f"✅ `{parsed['owner']}/{parsed['repo']}`")

# ---------------------------------------------------
# 사전 조건 확인
# ---------------------------------------------------
if not (options.get("api_key") and options.get("repository_url")):
    st.error("⛔ API Token 과 GitHub URL을 입력해야 이 페이지를 이용할 수 있습니다.")
    st.stop()

# API 키 유효성 검사
with st.spinner("Validating API key..."):
    if not gemini.api_check(api_key):
        st.error("❌ Invalid API Key")
        st.stop()

# GitHub URL 파싱
parsed_url = parse_github_url(repository_url)
if not parsed_url:
    st.error("❌ Invalid GitHub URL")
    st.stop()

owner = parsed_url["owner"]
repo = parsed_url["repo"]

# ---------------------------------------------------
# 페이지 헤더
# ---------------------------------------------------
st.title("📡 Repositorie Radar")
st.write("GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.")
st.divider()

st.title("📄 Issue Summary")
st.markdown(f"**{owner}/{repo}** 저장소의 이슈를 AI가 분석합니다.")

st.markdown(f"🔗 [GitHub에서 보기]({repository_url})")

st.divider()

# ---------------------------------------------------
# 1단계: 이슈 가져오기
# ---------------------------------------------------
st.header("1️⃣ 이슈 가져오기")
=======
        st.sidebar.success(f"✅ **{parsed['repo']}** 프로젝트")

# ---------------------------------------------------
# 사전 조건 확인 (API 호출 최소화)
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

# API 검증 로직 최적화
if "is_api_valid" not in st.session_state or st.session_state.get("last_checked_key") != api_key:
    with st.spinner("API 키 확인 중..."):
        is_valid = gemini.api_check(api_key)
        
        st.session_state["is_api_valid"] = is_valid
        st.session_state["last_checked_key"] = api_key

if not st.session_state["is_api_valid"]:
    st.error("❌ API 키가 올바르지 않아요.")
    st.stop()

parsed_url = parse_github_url(repository_url)
if not parsed_url:
    st.error("❌ GitHub 주소가 올바르지 않아요.")
    st.stop()

owner = parsed_url["owner"]
repo = parsed_url["repo"]

# ---------------------------------------------------
# 페이지 헤더
# ---------------------------------------------------
st.markdown('<h1 class="main-title">📡 Repository Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.</p>', unsafe_allow_html=True)

st.divider()

st.markdown('<h2 class="section-header">📄 Issue Summary</h2>', unsafe_allow_html=True)
st.markdown(f"**{owner}/{repo}** 저장소의 이슈를 스마트하게 분석합니다.")

st.markdown(f"🔗 [GitHub에서 보기]({repository_url})")

st.divider()

# ---------------------------------------------------
# 1단계: 이슈 가져오기 (간소화)
# ---------------------------------------------------
st.markdown('<h3 class="section-header">🔍 이슈 가져오기</h3>', unsafe_allow_html=True)
>>>>>>> Stashed changes

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    issue_state = st.selectbox(
        "이슈 상태",
        ["all", "open", "closed"],
<<<<<<< Updated upstream
        index=0,
=======
        index=1,
>>>>>>> Stashed changes
        help="전체, 열린 이슈, 닫힌 이슈"
    )

with col2:
    max_issues = st.slider(
        "최대 개수",
        min_value=10,
        max_value=100,
<<<<<<< Updated upstream
        value=30,
=======
        value=50,
>>>>>>> Stashed changes
        step=10,
        help="가져올 이슈 개수"
    )

with col3:
    st.write("")
    st.write("")
    fetch_btn = st.button("📥 가져오기", type="primary", use_container_width=True)

# GitHub에서 이슈 가져오기
if fetch_btn or "fetched_issues" not in st.session_state:
    with st.spinner(f"📡 {owner}/{repo} 저장소에서 이슈 가져오는 중..."):
        issues = fetch_github_issues(owner, repo, issue_state, max_issues)
        
        if issues:
            st.session_state["fetched_issues"] = issues
            st.success(f"✅ {len(issues)}개 이슈를 가져왔습니다!")
        else:
            st.warning("⚠️ 이슈를 찾을 수 없습니다.")
            st.session_state["fetched_issues"] = []

# ---------------------------------------------------
<<<<<<< Updated upstream
# 2단계: 분석할 이슈 선택
# ---------------------------------------------------
if "fetched_issues" in st.session_state and st.session_state["fetched_issues"]:
    
    st.divider()
    st.header("2️⃣ 분석할 이슈 선택")
    
    issues = st.session_state["fetched_issues"]
    
    # 전체 선택/해제 버튼
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("✅ 전체 선택", use_container_width=True):
            for issue in issues:
                st.session_state[f"issue_check_{issue['number']}"] = True
            st.rerun()
    
    with col2:
        if st.button("❌ 전체 해제", use_container_width=True):
            for issue in issues:
                st.session_state[f"issue_check_{issue['number']}"] = False
=======
# 이슈 통계 (간소화 - 차트 없이 숫자만)
# ---------------------------------------------------
if "fetched_issues" in st.session_state and st.session_state["fetched_issues"]:
    
    issues = st.session_state["fetched_issues"]
    
    st.divider()
    st.markdown('<h3 class="section-header">📊 이슈 통계</h3>', unsafe_allow_html=True)
    
    # 핵심 지표만 간단하게
    col1, col2, col3, col4 = st.columns(4)
    
    open_count = sum(1 for i in issues if i["state"] == "open")
    closed_count = sum(1 for i in issues if i["state"] == "closed")
    gfi_count = sum(1 for i in issues if any('good first issue' in l.lower() for l in i['labels']))
    bug_count = sum(1 for i in issues if any('bug' in l.lower() for l in i['labels']))
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(issues)}</div>
            <div class="metric-label">📄 Total Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{open_count}</div>
            <div class="metric-label">🟢 Open</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{gfi_count}</div>
            <div class="metric-label">🌱 Good First Issue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{bug_count}</div>
            <div class="metric-label">🐛 Bugs</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 카테고리 통계 (텍스트로만)
    st.markdown("#### 📁 카테고리별 분포")
    categories = [categorize_issue(issue['labels']) for issue in issues]
    category_counts = Counter(categories)
    
    stats_text = " | ".join([f"{cat}: **{count}개**" for cat, count in category_counts.most_common()])
    st.markdown(f"<div class='stats-summary'>{stats_text}</div>", unsafe_allow_html=True)
    
    # ---------------------------------------------------
    # 2단계: 스마트 필터링 (간소화)
    # ---------------------------------------------------
    st.divider()
    st.markdown('<h3 class="section-header">🔍 이슈 필터링 & 선택</h3>', unsafe_allow_html=True)
    
    # 필터 옵션
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.multiselect(
            "📁 카테고리",
            ["🐛 Bug", "🌱 Good First Issue", "🆘 Help Wanted", "✨ Enhancement", 
             "📝 Documentation", "❓ Question", "📌 Other"],
            default=["🐛 Bug", "🌱 Good First Issue", "🆘 Help Wanted"]
        )
    
    with col2:
        filter_priority = st.multiselect(
            "⚡ 우선순위",
            ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low", "⚪ Normal"]
        )
    
    with col3:
        filter_state = st.multiselect(
            "🎯 상태",
            ["open", "closed"],
            default=["open"]
        )
    
    # 검색
    search_keyword = st.text_input(
        "🔍 제목 검색",
        placeholder="검색어 입력...",
        help="이슈 제목에서 검색"
    )
    
    # 빠른 필터 버튼
    st.markdown("#### 🎯 Quick Filters")
    qf_col1, qf_col2, qf_col3, qf_col4 = st.columns(4)
    
    with qf_col1:
        if st.button("🐛 Bugs Only", use_container_width=True):
            filter_category = ["🐛 Bug"]
            st.rerun()
    
    with qf_col2:
        if st.button("🌱 Good First Issues", use_container_width=True):
            filter_category = ["🌱 Good First Issue"]
            st.rerun()
    
    with qf_col3:
        if st.button("🆘 Help Wanted", use_container_width=True):
            filter_category = ["🆘 Help Wanted"]
            st.rerun()
    
    with qf_col4:
        if st.button("🔴 Critical", use_container_width=True):
            filter_priority = ["🔴 Critical"]
>>>>>>> Stashed changes
            st.rerun()
    
    st.divider()
    
<<<<<<< Updated upstream
    st.markdown("### 📋 이슈 목록")
    
    # 이슈 필터링 옵션
    filter_col1, filter_col2 = st.columns([1, 3])
    
    with filter_col1:
        filter_state = st.multiselect(
            "상태 필터",
            ["open", "closed"],
            default=["open", "closed"]
        )
    
    with filter_col2:
        search_keyword = st.text_input(
            "🔍 제목 검색",
            placeholder="검색어 입력...",
            help="이슈 제목에서 검색"
        )
    
    # 필터 적용
    filtered_issues = []
    for issue in issues:
        if issue["state"] not in filter_state:
            continue
        
=======
    # 필터 적용
    filtered_issues = []
    for issue in issues:
        # 카테고리 필터
        if filter_category and categorize_issue(issue['labels']) not in filter_category:
            continue
        
        # 우선순위 필터
        if filter_priority and get_priority(issue['labels']) not in filter_priority:
            continue
        
        # 상태 필터
        if issue["state"] not in filter_state:
            continue
        
        # 검색어 필터
>>>>>>> Stashed changes
        if search_keyword and search_keyword.lower() not in issue["title"].lower():
            continue
        
        filtered_issues.append(issue)
    
<<<<<<< Updated upstream
    st.info(f"📊 총 {len(filtered_issues)}개 이슈 ({len(issues)}개 중)")
    
    # 이슈 목록 표시 및 선택
=======
    st.info(f"📊 필터링된 이슈: **{len(filtered_issues)}개** (전체 {len(issues)}개 중)")
    
    # 전체 선택/해제
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("✅ 전체 선택", use_container_width=True):
            for issue in filtered_issues:
                st.session_state[f"issue_check_{issue['number']}"] = True
            st.rerun()
    
    with col2:
        if st.button("❌ 전체 해제", use_container_width=True):
            for issue in filtered_issues:
                st.session_state[f"issue_check_{issue['number']}"] = False
            st.rerun()
    
    st.divider()
    
    # 이슈 목록 (간소화)
    st.markdown("### 📋 Issue List")
    
>>>>>>> Stashed changes
    selected_issues = []
    
    for issue in filtered_issues:
        check_key = f"issue_check_{issue['number']}"
        
        if check_key not in st.session_state:
            st.session_state[check_key] = True
        
<<<<<<< Updated upstream
=======
        category = categorize_issue(issue['labels'])
        priority = get_priority(issue['labels'])
        
>>>>>>> Stashed changes
        with st.container():
            col1, col2 = st.columns([0.5, 9.5])
            
            with col1:
                is_selected = st.checkbox(
                    "",
                    value=st.session_state[check_key],
                    key=check_key,
                    label_visibility="collapsed"
                )
            
            with col2:
                state_emoji = "🟢" if issue["state"] == "open" else "⚪"
                
<<<<<<< Updated upstream
                # 설명 미리보기 생성
                desc_preview = issue['description'][:100] if issue['description'] else "설명 없음"
                desc_ellipsis = '...' if len(issue['description']) > 100 else ''
                
                st.markdown(f"""
                **{state_emoji} #{issue['number']} - {issue['title']}**
                
                👤 {issue['user']} | 📅 {issue['updated_at']} | 🏷️ {', '.join(issue['labels'][:3]) if issue['labels'] else 'No labels'}
                
                *{desc_preview}{desc_ellipsis}*
                
                [GitHub에서 보기]({issue['url']})
                """)
            
            st.divider()
=======
                # 특별 라벨 하이라이트
                special_badges = ""
                if "🌱" in category:
                    special_badges += "🌱 **GOOD FIRST ISSUE** "
                if "🆘" in category:
                    special_badges += "🆘 **HELP WANTED** "
                if "🔴" in priority:
                    special_badges += "🔴 **CRITICAL** "
                
                # 간소화된 이슈 표시
                st.markdown(f"""
                <div class="issue-card">
                    {special_badges}<br>
                    <strong>{state_emoji} #{issue['number']} - {issue['title']}</strong><br>
                    <small>{category} | {priority} | 👤 {issue['user']} | 📅 {issue['created_at']} | 💬 {issue['comments']} comments</small><br>
                    <small>🏷️ {', '.join(issue['labels'][:5]) if issue['labels'] else 'None'}</small><br>
                    <a href="{issue['url']}" target="_blank">GitHub에서 보기 →</a>
                </div>
                """, unsafe_allow_html=True)
>>>>>>> Stashed changes
            
            if is_selected:
                selected_issues.append(issue)
    
    # ---------------------------------------------------
<<<<<<< Updated upstream
    # 3단계: AI 분석
    # ---------------------------------------------------
    st.divider()
    st.header("🤖 AI Comment")
=======
    # 3단계: AI 분석 (간소화)
    # ---------------------------------------------------
    st.divider()
    st.markdown('<h3 class="section-header">🤖 AI 분석</h3>', unsafe_allow_html=True)
>>>>>>> Stashed changes
    
    if len(selected_issues) == 0:
        st.warning("⚠️ 분석할 이슈를 최소 1개 이상 선택해주세요.")
    else:
        st.success(f"✅ {len(selected_issues)}개 이슈가 선택되었습니다.")
        
<<<<<<< Updated upstream
        # 선택된 이슈 미리보기
        with st.expander(f"📋 선택된 이슈 {len(selected_issues)}개 보기"):
            for issue in selected_issues[:10]:
                st.markdown(f"- #{issue['number']}: {issue['title']}")
            if len(selected_issues) > 10:
                st.info(f"... 외 {len(selected_issues) - 10}개")
        
        if st.button("🤖 AI 분석 시작", type="primary", use_container_width=True):
            
            # Gemini AI로 분석 실행
            with st.status("🤖 Gemini AI로 분석 중...", expanded=True) as status:
=======
        # 선택 요약
        with st.expander(f"📋 선택된 이슈 요약"):
            summary_categories = Counter([categorize_issue(i['labels']) for i in selected_issues])
            for cat, count in summary_categories.most_common():
                st.markdown(f"- **{cat}**: {count}개")
        
        if st.button("🤖 AI 분석 시작", type="primary", use_container_width=True):
            
            with st.status("🤖 Gemini AI로 분석 중...", expanded=False) as status:
>>>>>>> Stashed changes
                st.write(f"선택된 이슈: {len(selected_issues)}개")
                st.write(f"분석 언어: {language}")
                
                try:
                    result = gemini.api_issue_summary(
                        _key=api_key,
                        _issues=selected_issues,
                        _language=language
                    )
                    
                    if result.startswith("Error:"):
                        st.error(f"❌ 분석 실패: {result}")
                        st.stop()
                    
                    status.update(label="✅ 분석 완료!", state="complete")
                
                except Exception as e:
                    st.error(f"❌ 오류: {str(e)}")
                    st.stop()
            
<<<<<<< Updated upstream
            # 분석 결과 표시
            st.success("✅ 이슈 분석이 완료되었습니다!")
            
            st.divider()
            st.markdown("## 📊 분석 결과")
            
            # 결과를 탭으로 구분
            tab1, tab2, tab3 = st.tabs(["📝 AI 분석", "📊 통계", "📥 다운로드"])
=======
            st.success("✅ 이슈 분석이 완료되었습니다!")
            
            st.divider()
            st.markdown('<h3 class="section-header">📊 분석 결과</h3>', unsafe_allow_html=True)
            
            # 결과 탭
            tab1, tab2 = st.tabs(["📝 AI 분석", "📥 다운로드"])
>>>>>>> Stashed changes
            
            with tab1:
                st.markdown(result)
            
            with tab2:
<<<<<<< Updated upstream
                # 이슈 통계 표시
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("총 이슈", len(selected_issues))
                
                with col2:
                    open_count = sum(1 for i in selected_issues if i["state"] == "open")
                    st.metric("열린 이슈", open_count)
                
                with col3:
                    closed_count = sum(1 for i in selected_issues if i["state"] == "closed")
                    st.metric("닫힌 이슈", closed_count)
                
                with col4:
                    all_labels = set()
                    for issue in selected_issues:
                        all_labels.update(issue["labels"])
                    st.metric("고유 라벨", len(all_labels))
                
                st.markdown("#### 🏷️ 라벨 분포")
                
                # 라벨 개수 집계
                label_counts = {}
                for issue in selected_issues:
                    for label in issue["labels"]:
                        label_counts[label] = label_counts.get(label, 0) + 1
                
                if label_counts:
                    sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
                    for label, count in sorted_labels[:10]:
                        st.markdown(f"**{label}**: {count}개")
                else:
                    st.info("라벨이 없습니다.")
            
            with tab3:
                # 분석 보고서 생성
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
=======
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
>>>>>>> Stashed changes
                
                report = f"""# Issue Summary Report

**Repository:** {owner}/{repo}
**Analysis Date:** {timestamp}
<<<<<<< Updated upstream
**Total Issues:** {len(selected_issues)}

---

=======
**Total Issues Analyzed:** {len(selected_issues)}

---

## AI Analysis

>>>>>>> Stashed changes
{result}

---

<<<<<<< Updated upstream
*Generated by Repository Radar using Gemini AI*
"""
                
                # 마크다운 파일 다운로드
                st.download_button(
                    label="📥 Markdown 다운로드",
                    data=report,
                    file_name=f"issue_summary_{owner}_{repo}.md",
=======
## Selected Issues

"""
                
                for issue in selected_issues:
                    cat = categorize_issue(issue['labels'])
                    pri = get_priority(issue['labels'])
                    report += f"""
### #{issue['number']} - {issue['title']}

- **Category:** {cat}
- **Priority:** {pri}
- **State:** {issue['state']}
- **Created:** {issue['created_at']}
- **Author:** {issue['user']}
- **Labels:** {', '.join(issue['labels'])}
- **URL:** {issue['url']}

---
"""
                
                report += "\n*Generated by Repository Radar using Gemini AI*\n"
                
                st.download_button(
                    label="📥 Markdown 파일로 다운로드",
                    data=report,
                    file_name=f"issue_analysis_{owner}_{repo}_{datetime.now().strftime('%Y%m%d')}.md",
>>>>>>> Stashed changes
                    mime="text/markdown",
                    use_container_width=True
                )

else:
    st.info("👆 위의 '📥 가져오기' 버튼을 눌러 이슈를 불러오세요!")

st.divider()
<<<<<<< Updated upstream
st.caption(f"Powered by Gemini AI | {owner}/{repo}")
=======

st.markdown("""
<div style="text-align: center; color: #9aa0a6; padding: 1rem 0; font-family: 'Plus Jakarta Sans', sans-serif;">
    <p style="font-size: 0.9rem;">Powered by Gemini AI | {}/{}</p>
</div>
""".format(owner, repo), unsafe_allow_html=True)
>>>>>>> Stashed changes
