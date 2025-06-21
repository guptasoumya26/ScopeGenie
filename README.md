---
title: ScopeGenie – AI Test Intelligence Dashboard
emoji: "🧞‍♂️"
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: "1.35.0"
app_file: app.py
pinned: false
---

# 🧞‍♂️ ScopeGenie – AI Test Intelligence Dashboard

Welcome to **ScopeGenie**! This project leverages AI to automate and enhance the process of test planning and test case generation for software projects.

## 🚀 Features

- 🔖 **Jira Integration:** Fetches story details directly from Jira.
- 🔗 **GitHub PR Analysis:** Analyzes pull request diffs to understand code changes.
- 🧠 **AI Test Scope Identification:** Uses AI agents to identify impacted test areas.
- 📋 **Automated Test Plan Generation:** Instantly creates a structured test plan.
- 🧪 **AI-Generated Test Cases:** Produces detailed test cases based on requirements and code changes.
- ⬇️ **Export to DOCX:** Download test scope, plan, and cases as Word documents.

## 🛠️ Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) for the web UI
- [LLM] for AI agents
- [Jira API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [GitHub API](https://docs.github.com/en/rest)

## 📦 Project Structure

```
app.py                # Streamlit app entry point
agents/               # AI agent logic for test area and test case generation
services/             # Integrations for Jira and GitHub
utils/                # Export and parsing utilities
prompts/              # Prompt templates for AI agents
```

## ⚡ Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/scopegenie.git
   cd scopegenie
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys.
4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. Enter a Jira Ticket ID and a GitHub PR link.
2. Click **Analyze** to fetch data and generate test scope, plan, and cases.
3. Review the results and export as needed.

## ☁️ Deploying to Hugging Face Spaces (Manual Upload)

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space (choose Streamlit as the SDK).
2. After creation, open your Space and click the **Files and versions** tab.
3. Click **Upload files** and select all your project files and folders (including `app.py`, `requirements.txt`, and all source folders).
4. Click **Commit changes** to upload.
5. Go to the **Settings** tab and add your secrets (API keys, tokens, etc.) under **Secrets and environment variables** (optional, since users can enter secrets in the sidebar).
6. Your app will automatically build and deploy. If you update your code, repeat the upload process.

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT License

---

Made with ❤️ by Soumya Gupta
