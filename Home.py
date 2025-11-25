# streamlit_app.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import streamlit as st

# ---------------------------------------------------
# Streamlit config
# ---------------------------------------------------
st.set_page_config(
    page_title="Repositorie Radar",
    page_icon=":shark:",
    layout="wide",
)

# ---------------------------------------------------
# Sidebar(API,URL input)
# ---------------------------------------------------
if "api_token" not in st.session_state:
    st.session_state["api_token"] = ""
if "repository_url" not in st.session_state:
    st.session_state["repository_url"] = ""

st.sidebar.title("Input")
api_token = st.sidebar.text_input("GPT/Gemini API token", value=st.session_state["api_token"], type="password")
repository_url = st.sidebar.text_input("Github repository url", value=st.session_state["repository_url"])

if st.sidebar.button("Save"):
    st.session_state["api_token"] = api_token
    st.session_state["repository_url"] = repository_url

# ---------------------------------------------------
# Home Page
# ---------------------------------------------------
st.title("Repositorie Radar")
st.write("GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.")

st.header(" Home")
api_token = st.session_state.get("api_token", "")
repository_url = st.session_state.get("repository_url", "")

# ---------------------------------------------------
# Check input
# ---------------------------------------------------
if api_token and repository_url:
    st.success("GitHub URL과 API Token이 확인되었습니다. 왼쪽 메뉴에서 분석 페이지로 이동하세요!")
else:
    st.error("API Token 과 GitHub URL를 입력해야 합니다.")
