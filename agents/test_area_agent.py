from openai import OpenAI
import os

def identify_test_areas(jira_story: dict, pr_diff: dict) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = build_test_scope_prompt(jira_story, pr_diff)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a QA expert helping identify test scope from code changes and user stories."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

def build_test_scope_prompt(jira: dict, pr: dict) -> str:
    prompt = f"""You are given a Jira story and a pull request.

Jira Story:
Title: {jira['summary']}
Description: {jira['description']}

Pull Request:
Title: {pr['title']}
Description: {pr['body']}
Files Changed:"""

    for f in pr['files']:
        prompt += f"\n- {f['filename']} ({f['status']})"
        if f.get('patch'):
            prompt += f"\n  Diff:\n  {f['patch'][:1000]}\n"

    prompt += "\n\nIdentify impacted modules, features, and test areas that should be covered."

    return prompt
