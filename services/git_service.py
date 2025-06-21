from github import Github
from urllib.parse import urlparse
import os

def get_github_client():
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    return Github(GITHUB_TOKEN)

def parse_pr_url(pr_url):
    parsed = urlparse(pr_url)
    path_parts = parsed.path.strip("/").split("/")
    owner, repo, _, pr_number = path_parts
    return owner, repo, int(pr_number)

def fetch_pr_diff(pr_url):
    gh = get_github_client()
    owner, repo_name, pr_number = parse_pr_url(pr_url)
    repo = gh.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    changed_files = []
    for file in pr.get_files():
        changed_files.append({
            "filename": file.filename,
            "status": file.status,
            "patch": getattr(file, "patch", None)
        })

    return {
        "title": pr.title,
        "body": pr.body,
        "files": changed_files
    }
