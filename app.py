import streamlit as st
from dotenv import load_dotenv
import os
import time
from services.jira_service import fetch_jira_story
from services.git_service import fetch_pr_diff
from agents.test_area_agent import identify_test_areas
from agents.test_generator_agent import generate_test_cases
from utils.exporter import download_docx_button

def get_env_or_sidebar(key, label, type_="text"):
    value = st.session_state.get(key, "")
    with st.sidebar:
        if type_ == "password":
            value = st.text_input(label, type="password", key=key, value=value)
        else:
            value = st.text_input(label, key=key, value=value)
    return value

with st.sidebar:
    st.header("🔐 API & Integration Secrets")
openai_api_key = get_env_or_sidebar("OPENAI_API_KEY", "🔑 OpenAI API Key", type_="password")
github_token = get_env_or_sidebar("GITHUB_TOKEN", "🔑 GitHub Token", type_="password")
jira_base_url = get_env_or_sidebar("JIRA_BASE_URL", "🌐 Jira Base URL")
jira_email = get_env_or_sidebar("JIRA_EMAIL", "📧 Jira Email")
jira_api_token = get_env_or_sidebar("JIRA_API_TOKEN", "🔑 Jira API Token", type_="password")

# Set secrets in os.environ for downstream code
if openai_api_key: os.environ["OPENAI_API_KEY"] = openai_api_key
if github_token: os.environ["GITHUB_TOKEN"] = github_token
if jira_base_url: os.environ["JIRA_BASE_URL"] = jira_base_url
if jira_email: os.environ["JIRA_EMAIL"] = jira_email
if jira_api_token: os.environ["JIRA_API_TOKEN"] = jira_api_token

load_dotenv()
st.set_page_config(page_title="ScopeGenie", page_icon="🧞‍♂️", layout="wide")
st.title("🧞 ScopeGenie – AI Test Intelligence Dashboard")

jira_data = st.session_state.get("jira_data", {})
pr_data = st.session_state.get("pr_data", {})
test_scope = st.session_state.get("test_scope", "")
test_plan = st.session_state.get("test_plan", "")
test_cases = st.session_state.get("test_cases", "")

with st.form("scope_form"):
    jira_id = st.text_input("🔖 Jira Ticket ID")
    pr_link = st.text_input("🔗 GitHub PR Link")
    submitted = st.form_submit_button("🧠 Analyze")

missing_secrets = not all([openai_api_key, github_token, jira_base_url, jira_email, jira_api_token])

if submitted:
    if missing_secrets:
        st.warning("All API keys and credentials are mandatory. Please fill in all fields in the sidebar.")
    else:
        with st.spinner("⏳ Fetching data from Jira and GitHub..."):
            try:
                jira_data = fetch_jira_story(jira_id)
                pr_data = fetch_pr_diff(pr_link)
                test_scope = identify_test_areas(jira_data, pr_data)
                test_plan = f"""Test Plan for {jira_data['summary']}

Objective:
Ensure correctness of the implementation described in the Jira story and corresponding code changes.

Test Scope:
{test_scope}

Entry Criteria:
- Code pushed and PR created
- Story approved

Exit Criteria:
- All test cases pass
- No critical bugs remain

Test Types:
- Functional
- Negative
- Regression
"""
                test_cases = generate_test_cases(jira_data, pr_data)
                st.session_state.jira_data = jira_data
                st.session_state.pr_data = pr_data
                st.session_state.test_scope = test_scope
                st.session_state.test_plan = test_plan
                st.session_state.test_cases = test_cases
            except Exception as e:
                st.error(f"❌ Failed to process: {e}")

if jira_data:
    with st.expander("📌 Jira Story", expanded=True):
        st.markdown(f"**Title:** {jira_data['summary']}")
        st.markdown(jira_data['description'])

if pr_data:
    with st.expander("🔁 GitHub PR", expanded=True):
        st.markdown(f"**Title:** {pr_data['title']}")
        st.markdown(pr_data['body'])
        st.markdown("### 🔧 Changed Files:")
        for f in pr_data["files"]:
            st.code(f"{f['filename']} ({f['status']})")
            if f.get("patch"):
                with st.expander(f"🔍 Diff: {f['filename']}"):
                    st.code(f["patch"], language="diff")

if test_scope:
    st.markdown("---")
    st.subheader("🔬 AI-Identified Test Scope")
    st.markdown(test_scope)
    download_docx_button("⬇️ Export Test Scope (.docx)", "test_scope.docx", test_scope)

if test_plan:
    st.markdown("---")
    st.subheader("📋 Test Plan")
    st.markdown(test_plan)
    download_docx_button("⬇️ Export Test Plan (.docx)", "test_plan.docx", test_plan)

if test_cases:
    st.markdown("---")
    st.subheader("🧪 AI-Generated Test Cases")
    st.markdown(test_cases)
    download_docx_button("⬇️ Export Test Cases (.docx)", "test_cases.docx", test_cases)

