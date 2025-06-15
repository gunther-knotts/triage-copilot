import os
from github import Github
import pandas as pd
from dotenv import load_dotenv

# Set up GitHub API
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GitHub token not found. Please create a .env file and set the GITHUB_TOKEN variable.")
g = Github(github_token)

# get example large open source repo
repo = g.get_repo("microsoft/vscode")

# get issues from repo
issues = repo.get_issues(state="closed")
issue_data = []
print("Fetching issues and labels...")
for i, issue in enumerate(issues):
    if i >= 300:
        break
    if issue.labels:
        label_names = [label.name for label in issue.labels]
        issue_data.append({
            "title": issue.title,
            "body": issue.body,
            "url": issue.html_url,
            "labels": ", ".join(label_names) # Join labels into a string
        })

df = pd.DataFrame(issue_data)
df.to_csv("vscode_issues_labeled.csv", index=False)
print("Done. Saved labeled issues to vscode_issues_labeled.csv")