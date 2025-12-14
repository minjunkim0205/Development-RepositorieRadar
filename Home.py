# Home.py (streamlit_app.py)
# ---------------------------------------------------
# 모듈 임포트
# ---------------------------------------------------
import streamlit as st
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# Streamlit 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="Repository Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    /* 메인 헤더 */
    .main-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* 서브타이틀 */
    .subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.25rem;
        text-align: center;
        color: #9aa0a6;
        margin-bottom: 3rem;
        font-weight: 400;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* 기능 카드 - 미니멀하고 세련된 디자인 */
    .feature-card {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4));
    }
    
    .feature-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #e8eaed;
    }
    
    .feature-desc {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #9aa0a6;
    }
    
    .feature-desc ul {
        margin-top: 0.75rem;
        padding-left: 1.25rem;
    }
    
    .feature-desc li {
        margin-bottom: 0.5rem;
        color: #bdc1c6;
    }
    
    .feature-desc strong {
        color: #667eea;
        font-weight: 600;
    }
    
    /* 통계 카드 */
    .stat-card {
        background: rgba(26, 31, 58, 0.4);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .stat-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.9rem;
        color: #9aa0a6;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* CTA 컨테이너 */
    .cta-container {
        text-align: center;
        margin: 3rem 0;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.15);
    }
    
    /* 애니메이션 */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    /* 사용 단계 */
    .step-container {
        background: rgba(26, 31, 58, 0.5);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .step-container:hover {
        border-left-color: #764ba2;
        transform: translateX(4px);
    }
    
    .step-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-right: 1rem;
    }
    
    /* 섹션 타이틀 */
    h2 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e8eaed;
        font-weight: 700;
        margin-top: 2rem;
    }
    
    h3 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #bdc1c6;
        font-weight: 600;
    }
    
    /* 정보 박스 스타일 */
    .stAlert {
        background: rgba(26, 31, 58, 0.6);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 12px;
    }
    
    /* 문제-해결 섹션 */
    .problem-solution-box {
        background: rgba(26, 31, 58, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 245, 255, 0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 세션 상태 초기화
# ---------------------------------------------------
if "options" not in st.session_state:
    st.session_state["options"] = {
        "language": "Korean",
        "api_key": "",
        "api_type": "",
        "repository_url": ""
    }

if "contents" not in st.session_state:
    st.session_state["contents"] = {
        "01": {"File Tree": "", "AI Comment": ""}, 
        "02": {"AI Comment": ""}, 
        "03": {"AI Comment": ""}, 
        "04": {"AI Comment": ""}
    }

options = st.session_state["options"]
contents = st.session_state["contents"]

# ---------------------------------------------------
# 사이드바
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(
    "🔑 GPT/Gemini API 키", 
    value=options["api_key"], 
    type="password",
    help="OpenAI 또는 Google AI Studio에서 발급받은 API 키를 입력하세요"
)

repository_url = st.sidebar.text_input(
    "📊 GitHub 저장소 URL", 
    value=options["repository_url"],
    placeholder="https://github.com/소유자/저장소",
    help="GitHub 저장소의 전체 URL을 입력하세요"
)

st.sidebar.markdown("---")

if st.sidebar.button("💾 저장 및 검증", type="primary", use_container_width=True):
    contents = {
        "01": {"File Tree": "", "AI Comment": ""}, 
        "02": {"AI Comment": ""}, 
        "03": {"AI Comment": ""}, 
        "04": {"AI Comment": ""}
    }
    
    # API 키 확인
    if gpt.api_check(api_key):
        options["api_key"] = api_key
        options["api_type"] = "GPT"
        st.sidebar.success("✅ 유효한 GPT API 키입니다")
    elif gemini.api_check(api_key):
        options["api_key"] = api_key
        options["api_type"] = "GEMINI"
        st.sidebar.success("✅ 유효한 Gemini API 키입니다")
    else:
        options["api_key"] = ""
        options["api_type"] = ""
        st.sidebar.error("❌ 유효하지 않은 API 키입니다")
    
    # 저장소 URL 확인
    if github.url_check(repository_url):
        options["repository_url"] = repository_url
        st.sidebar.success("✅ 유효한 저장소 URL입니다")
    else:
        options["repository_url"] = ""
        st.sidebar.error("❌ 유효하지 않은 저장소 URL입니다")
    
    st.session_state["options"] = options
    st.session_state["contents"] = contents

st.sidebar.markdown("---")
st.sidebar.info("""
💡 **빠른 시작:**
1. [Google AI Studio](https://aistudio.google.com/apikey)에서 API 키 발급
2. GitHub 저장소 URL 입력
3. '저장 및 검증' 클릭
4. 분석 시작!
""")

# ---------------------------------------------------
# 메인 콘텐츠
# ---------------------------------------------------

# 히어로 섹션
st.markdown('<h1 class="main-title">📡 Repository Radar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI 기반 시각적 저장소 인텔리전스 플랫폼</p>', unsafe_allow_html=True)

# 상태 확인
if options["api_key"] and options["repository_url"]:
    st.success("✅ 설정 완료! 사이드바에서 분석 페이지로 이동하세요.")
else:
    st.warning("⚠️ 시작하려면 사이드바에서 API 키와 저장소 URL을 설정해주세요.")

st.markdown("---")

# ---------------------------------------------------
# Repository Radar란?
# ---------------------------------------------------
st.markdown("## 🎯 Repository Radar란?")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="problem-solution-box">
    <h3 style="color: #ff6b6b; margin-top: 0;">문제점 🤔</h3>
    
    새로운 GitHub 저장소를 발견했을 때:
    
    • ❌ <strong>압도적인 코드베이스</strong> - 어디서부터 시작해야 할까?<br>
    • ❌ <strong>불명확한 구조</strong> - 각 폴더는 무슨 역할을 하지?<br>
    • ❌ <strong>복잡한 의존성</strong> - 파일 간 관계는?<br>
    • ❌ <strong>숨겨진 패턴</strong> - 코드 흐름을 어떻게 파악하지?<br>
    • ❌ <strong>시간 소모</strong> - 기본만 이해하는데도 몇 시간
    
    <br><br>
    <strong style="color: #00f5ff;">기존 도구들은 코드만 보여줍니다.</strong><br>
    프로젝트를 <strong>시각적으로 이해</strong>하는 데는 도움이 되지 않습니다.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="problem-solution-box">
    <h3 style="color: #00f5ff; margin-top: 0;">솔루션 ✨</h3>
    
    Repository Radar는 모든 GitHub 저장소를 다음과 같이 변환합니다:
    
    • ✅ <strong>자동 진입점 감지</strong> - 어디서 시작할지 즉시 파악<br>
    • ✅ <strong>시각적 구조 분석</strong> - 전체 프로젝트 흐름을 한눈에<br>
    • ✅ <strong>언어 & 프레임워크 감지</strong> - 기술 스택 자동 파악<br>
    • ✅ <strong>디렉토리 중요도 분석</strong> - 핵심 폴더 우선순위 제공<br>
    • ✅ <strong>의존성 자동 발견</strong> - 설치 파일 즉시 확인
    
    <br><br>
    <strong style="color: #00f5ff;">코드가 아닌 프로젝트를 보여줍니다.</strong><br>
    전문가가 시각적으로 설명해주는 것과 같습니다.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 핵심 기능 (4개 카드)
# ---------------------------------------------------
st.markdown("## 🚀 핵심 기능")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <div class="feature-title">1. 저장소 구조 분석</div>
        <div class="feature-desc">
            <strong>기능:</strong> AI가 전체 저장소 구조를 분석합니다<br><br>
            <strong>제공 내용:</strong>
            <ul>
                <li>📁 진입점 자동 식별 (main.py, app.py, index.js 등)</li>
                <li>🎨 프로그래밍 언어 감지</li>
                <li>📂 디렉토리 목적 설명</li>
                <li>✅ 코드 구성 품질 평가</li>
                <li>🎯 프로젝트 유형 분류</li>
            </ul>
            <strong>적합한 사용자:</strong> 낯선 코드베이스를 즉시 이해하고 싶은 분
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔍</span>
        <div class="feature-title">3. 코드 흐름 시각화</div>
        <div class="feature-desc">
            <strong>기능:</strong> 6가지 인터랙티브 차트로 프로젝트 구조 완벽 이해<br><br>
            <strong>제공 내용:</strong>
            <ul>
                <li>🌊 폴더-파일 흐름도 (어떤 폴더에 무엇이 있는지)</li>
                <li>🚀 시작 파일 찾기 (어디서부터 읽어야 하는지)</li>
                <li>📊 사용 언어 비율 (무슨 언어로 만들어졌는지)</li>
                <li>☀️ 파일 종류 분포 (어떤 파일들이 있는지)</li>
                <li>📁 중요한 폴더 순위 (어느 폴더가 핵심인지)</li>
                <li>🔗 상호작용 다이어그램 (파일 간 의존성 그래프)</li>
            </ul>
            <strong>적합한 사용자:</strong> 프로젝트를 "보고" 싶은 시각적 학습자
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⚙️</span>
        <div class="feature-title">2. 환경 설정 가이드</div>
        <div class="feature-desc">
            <strong>기능:</strong> 완전한 설치 지침을 생성합니다<br><br>
            <strong>제공 내용:</strong>
            <ul>
                <li>💻 시스템 요구사항 (OS, 소프트웨어 버전)</li>
                <li>📋 단계별 설치 명령어</li>
                <li>🔧 구성 파일 설정</li>
                <li>🚀 애플리케이션 실행 방법</li>
                <li>🛠️ 일반적인 문제 및 해결책</li>
            </ul>
            <strong>적합한 사용자:</strong> 프로젝트를 빠르게 실행하고 싶은 분
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📄</span>
        <div class="feature-title">4. 이슈 요약 및 우선순위 지정</div>
        <div class="feature-desc">
            <strong>기능:</strong> AI가 모든 프로젝트 이슈를 분류하고 우선순위를 지정합니다<br><br>
            <strong>제공 내용:</strong>
            <ul>
                <li>🏷️ 이슈 분류 (버그, 기능, 개선사항)</li>
                <li>⚠️ 우선순위 레벨 할당</li>
                <li>📊 통계 및 일반적인 패턴</li>
                <li>✅ 실행 가능한 권장사항</li>
                <li>🚨 중요 이슈 강조</li>
            </ul>
            <strong>적합한 사용자:</strong> 작업을 계획하는 프로젝트 관리자 및 기여자
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 작동 방식
# ---------------------------------------------------
st.markdown("## 🛠️ 작동 방식")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("""
    <div class="step-container">
        <span class="step-number">1️⃣</span>
        <div>
            <strong>URL 입력</strong><br>
            GitHub 저장소 URL을 붙여넣기
        </div>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div class="step-container">
        <span class="step-number">2️⃣</span>
        <div>
            <strong>구조 분석</strong><br>
            자동으로 전체 파일 트리 분석
        </div>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div class="step-container">
        <span class="step-number">3️⃣</span>
        <div>
            <strong>시각화 생성</strong><br>
            6가지 인터랙티브 차트 제공
        </div>
    </div>
    """, unsafe_allow_html=True)

with step4:
    st.markdown("""
    <div class="step-container">
        <span class="step-number">4️⃣</span>
        <div>
            <strong>완전 이해</strong><br>
            5분 안에 프로젝트 완전 파악
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 통계
# ---------------------------------------------------
st.markdown("## 📈 핵심 지표")

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">6개</div>
        <div class="stat-label">한눈에 보는 차트</div>
    </div>
    """, unsafe_allow_html=True)

with stat2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">5분</div>
        <div class="stat-label">평균 분석 시간</div>
    </div>
    """, unsafe_allow_html=True)

with stat3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">자동 진입점 감지</div>
    </div>
    """, unsafe_allow_html=True)

with stat4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">실시간</div>
        <div class="stat-label">구조 분석</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 시각화 기능 상세 설명
# ---------------------------------------------------
st.markdown("## 🎨 한눈에 보는 6가지 차트")

viz1, viz2, viz3 = st.columns(3)

with viz1:
    st.markdown("""
    ### 🌊 폴더-파일 흐름도
    - 최상위 폴더부터 파일까지 흐름
    - 어떤 폴더가 큰지 비교
    - 파일이 어디에 몰려있는지
    """)

with viz2:
    st.markdown("""
    ### 🚀 시작 파일 찾기
    - main.py, app.py 같은 시작점 자동 발견
    - 중요도 순서대로 정렬
    - 여기서부터 읽기 시작!
    """)

with viz3:
    st.markdown("""
    ### 📊 기술 스택 파악
    - Python, JavaScript 등 언어 비율
    - Django, React 같은 프레임워크
    - .py, .js 같은 파일 종류
    """)

viz4, viz5, viz6 = st.columns(3)

with viz4:
    st.markdown("""
    ### ☀️ 파일 종류 분포
    - 파일을 확장자별로 그룹화
    - 어떤 타입이 많은지 한눈에
    - 태양계처럼 펼쳐보기
    """)

with viz5:
    st.markdown("""
    ### 📁 중요한 폴더 순위
    - 코드가 많은 폴더 찾기
    - 핵심 로직이 어디 있는지
    - 어느 폴더부터 볼지 결정
    """)

with viz6:
    st.markdown("""
    ### 🔗 상호작용 다이어그램
    - 파일 간 import/의존성 분석
    - 모듈 연결 구조 시각화
    - 데이터 흐름 파악
    """)

st.markdown("---")

# ---------------------------------------------------
# 사용 사례
# ---------------------------------------------------
st.markdown("## 💼 적합한 사용자")

use_case1, use_case2, use_case3 = st.columns(3)

with use_case1:
    st.markdown("""
    ### 👨‍💻 개발자
    - 새로운 오픈소스 프로젝트 탐색
    - 낯선 코드베이스에 기여
    - 코드 리뷰 준비
    - 리팩토링 계획
    """)

with use_case2:
    st.markdown("""
    ### 👨‍🏫 학생 및 학습자
    - 프로젝트 아키텍처 이해
    - 실제 코드에서 학습
    - 과제 설정
    - 연구 및 분석
    """)

with use_case3:
    st.markdown("""
    ### 👨‍💼 팀 리더
    - 신규 팀원 온보딩
    - 프로젝트 건강도 평가
    - 이슈 우선순위 지정
    - 기술 문서화
    """)

st.markdown("---")

# ---------------------------------------------------
# CTA (행동 유도)
# ---------------------------------------------------
st.markdown('<div class="cta-container">', unsafe_allow_html=True)

if not (options["api_key"] and options["repository_url"]):
    st.markdown("### 🚀 시작할 준비가 되셨나요?")
    st.markdown("👈 **사이드바에서 API 키와 저장소 URL을 설정하세요**")
else:
    st.success("### ✅ 모든 준비 완료!")
    st.markdown("👈 **사이드바에서 분석 페이지로 이동하여 저장소를 탐색하세요**")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 푸터
# ---------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #9aa0a6; padding: 2rem 0;">
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 600; font-size: 1.1rem;">
        <strong style="color: #00f5ff;">Repository Radar</strong> - Gemini AI & Plotly 기반
    </p>
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem;">
        오픈소스 탐색을 쉽게, 시각적으로 🚀
    </p>
</div>
""", unsafe_allow_html=True)