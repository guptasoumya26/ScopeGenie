from openai import OpenAI
import os

def generate_test_cases(jira_story: dict, pr_diff: dict) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = build_test_case_prompt(jira_story, pr_diff)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a QA engineer skilled in writing test cases based on code diffs and user stories."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

def build_test_case_prompt(jira: dict, pr: dict) -> str:
    prompt = f"""Write QA test cases based on the following:

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
            prompt += f"\n  Diff (truncated):\n  {f['patch'][:1000]}\n"

    prompt += """

Provide detailed test cases with:
- Input conditions
- Expected outcomes
- Negative test cases (if applicable)
Use Markdown bullet points or numbered list.
"""
    return prompt
