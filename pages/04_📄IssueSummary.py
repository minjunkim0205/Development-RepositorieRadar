# pages/04_📄IssueSummary.py
# ---------------------------------------------------
# 모듈 임포트
# ---------------------------------------------------
import streamlit as st
import json
import requests
from datetime import datetime
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
# 세션 상태 불러오기
# ---------------------------------------------------
options = st.session_state.get("options", {})
contents = st.session_state.get("contents", {})

# ---------------------------------------------------
# 헬퍼 함수들
# ---------------------------------------------------
def parse_github_url(url: str) -> dict:
    """GitHub URL에서 owner와 repo 추출"""
    if not url:
        return None
    try:
        parts = url.replace("https://github.com/", "").split("/")
        return {"owner": parts[0], "repo": parts[1]}
    except:
        return None


def fetch_github_issues(owner: str, repo: str, state: str = "all", per_page: int = 30):
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
                "user": issue.get("user", {}).get("login", "Unknown")
            })
        
        return formatted_issues
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ GitHub API Error: {str(e)}")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        return []


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
)

st.sidebar.divider()

# 레포지토리 정보 표시
if repository_url:
    parsed = parse_github_url(repository_url)
    if parsed:
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

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    issue_state = st.selectbox(
        "이슈 상태",
        ["all", "open", "closed"],
        index=0,
        help="전체, 열린 이슈, 닫힌 이슈"
    )

with col2:
    max_issues = st.slider(
        "최대 개수",
        min_value=10,
        max_value=100,
        value=30,
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
            st.rerun()
    
    st.divider()
    
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
        
        if search_keyword and search_keyword.lower() not in issue["title"].lower():
            continue
        
        filtered_issues.append(issue)
    
    st.info(f"📊 총 {len(filtered_issues)}개 이슈 ({len(issues)}개 중)")
    
    # 이슈 목록 표시 및 선택
    selected_issues = []
    
    for issue in filtered_issues:
        check_key = f"issue_check_{issue['number']}"
        
        if check_key not in st.session_state:
            st.session_state[check_key] = True
        
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
            
            if is_selected:
                selected_issues.append(issue)
    
    # ---------------------------------------------------
    # 3단계: AI 분석
    # ---------------------------------------------------
    st.divider()
    st.header("🤖 AI Comment")
    
    if len(selected_issues) == 0:
        st.warning("⚠️ 분석할 이슈를 최소 1개 이상 선택해주세요.")
    else:
        st.success(f"✅ {len(selected_issues)}개 이슈가 선택되었습니다.")
        
        # 선택된 이슈 미리보기
        with st.expander(f"📋 선택된 이슈 {len(selected_issues)}개 보기"):
            for issue in selected_issues[:10]:
                st.markdown(f"- #{issue['number']}: {issue['title']}")
            if len(selected_issues) > 10:
                st.info(f"... 외 {len(selected_issues) - 10}개")
        
        if st.button("🤖 AI 분석 시작", type="primary", use_container_width=True):
            
            # Gemini AI로 분석 실행
            with st.status("🤖 Gemini AI로 분석 중...", expanded=True) as status:
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
            
            # 분석 결과 표시
            st.success("✅ 이슈 분석이 완료되었습니다!")
            
            st.divider()
            st.markdown("## 📊 분석 결과")
            
            # 결과를 탭으로 구분
            tab1, tab2, tab3 = st.tabs(["📝 AI 분석", "📊 통계", "📥 다운로드"])
            
            with tab1:
                st.markdown(result)
            
            with tab2:
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
                
                report = f"""# Issue Summary Report

**Repository:** {owner}/{repo}
**Analysis Date:** {timestamp}
**Total Issues:** {len(selected_issues)}

---

{result}

---

*Generated by Repository Radar using Gemini AI*
"""
                
                # 마크다운 파일 다운로드
                st.download_button(
                    label="📥 Markdown 다운로드",
                    data=report,
                    file_name=f"issue_summary_{owner}_{repo}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

else:
    st.info("👆 위의 '📥 가져오기' 버튼을 눌러 이슈를 불러오세요!")

st.divider()
st.caption(f"Powered by Gemini AI | {owner}/{repo}")