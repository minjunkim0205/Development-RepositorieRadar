# 01_📊RepositoryStructure.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import streamlit as st
import module.github as github
import module.gpt as gpt

# ---------------------------------------------------
# Get session state
# ---------------------------------------------------
api_token = st.session_state.get("api_token", "")
repository_url = st.session_state.get("repository_url", "")

# ---------------------------------------------------
# Sidebar(API,URL input)
# ---------------------------------------------------
st.sidebar.title("Input")
api_token = st.sidebar.text_input("GPT/Gemini API token", value=api_token, type="password", disabled=True)
repository_url = st.sidebar.text_input("Github repository url", value=repository_url, disabled=True)

# ---------------------------------------------------
# Page
# ---------------------------------------------------
if not (api_token and repository_url):
    st.error("API Token 과 GitHub URL를 입력해야 이 페이지를 이용할 수 있습니다.")
    st.stop()

st.title("Repositorie Radar")
st.write("GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.")

st.header("📊Repository Structure")
st.code(github.url_tree_string(repository_url)) 

st.header("AI Comment")
st.write(gpt.api_repository_structure(api_token, github.url_tree_dict(repository_url)))
