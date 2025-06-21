from jira import JIRA
import os

def get_jira_client():
    JIRA_BASE_URL = os.environ["JIRA_BASE_URL"]
    JIRA_EMAIL = os.environ["JIRA_EMAIL"]
    JIRA_API_TOKEN = os.environ["JIRA_API_TOKEN"]
    return JIRA(
        server=JIRA_BASE_URL,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

def fetch_jira_story(jira_id):
    jira = get_jira_client()
    issue = jira.issue(jira_id)
    summary = issue.fields.summary
    description = issue.fields.description
    return {
        "id": jira_id,
        "summary": summary,
        "description": description
    }
