# 02_⚙️EnvironmentSetup.py

# ---------------------------------------------------
# Import module
# ---------------------------------------------------
import streamlit as st
import module.github as github
import module.gpt as gpt
import module.gemini as gemini

# ---------------------------------------------------
# Load state into variables
# ---------------------------------------------------
options = st.session_state["options"]
contents = st.session_state["contents"]

# ---------------------------------------------------
# Sidebar(API,URL input)
# ---------------------------------------------------
st.sidebar.title("Input")
api_key = st.sidebar.text_input("GPT/Gemini API token", value=options["api_key"], type="password", disabled=True)
repository_url = st.sidebar.text_input("Github repository url", value=options["repository_url"], disabled=True)

# ---------------------------------------------------
# Page
# ---------------------------------------------------
if not (options["api_key"] and options["repository_url"]):
    st.error("API Token 과 GitHub URL를 입력해야 이 페이지를 이용할 수 있습니다.")
    st.stop()

st.title("Repositorie Radar")
st.write("GitHub 저장소를 자동 분석하는 웹 기반 오픈소스 탐색 도구입니다.")

st.title("⚙️Environment Setup")

# ---------------------------------------------------
# AI Comment
# ---------------------------------------------------
st.header("AI Comment")

language = options["language"]
api_key = options["api_key"]
api_type = options["api_type"]
repository_url = options["repository_url"]
ai_comment = contents["02"]["AI Comment"]

with st.spinner("Wait for it...", show_time=True):
    if not ai_comment:
        if api_type == "GPT":
            ai_comment = gpt.api_environment_setup(api_key, github.url_tree_dict(repository_url), github.url_readme_string(repository_url), language)
        elif api_type == "GEMINI":
            ai_comment = gemini.api_environment_setup(api_key, github.url_tree_dict(repository_url), github.url_readme_string(repository_url), language)

        contents["02"]["AI Comment"] = ai_comment
        st.session_state["contents"] = contents
    st.write(ai_comment)
