# Linux Agentic CLI (Gemini BYOK)


An autonomous, terminal-based Linux system administration agent powered by Google Gemini. Built with a **Bring Your Own Key (BYOK)** architecture and strict **Human-in-the-Loop** safety controls.

## ✨ Features

- **Autonomous Reasoning:** Translates natural language objectives into multi-step Linux bash workflows.
- **Bring Your Own Key (BYOK):** Zero hardcoded credentials. Supports `.env` files, environment variables, or secure masked CLI input.
- **Human-in-the-Loop Security:** Every shell command proposed by the AI requires explicit `[y/N]` user approval before execution.
- **Lightweight & Portable:** Pure Python implementation relying only on the official `google-genai` SDK.

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com
cd linux-gemini-agent
```

### 2. Set up a virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure your API Key (BYOK)
Get a Gemini API key from [Google AI Studio]. You can provide it in two ways:

* **Option A (Environment / `.env`):**
  ```bash
  cp .env.example .env
  # Edit .env and add your GEMINI_API_KEY
  ```
* **Option B (Interactive Prompt):**
  Simply run the script, and it will securely prompt you for your key at startup.

### 4. Run the Agent
```bash
python3 agent.py
```

## 🛡️ Security Disclaimer

This tool executes real bash commands on your host operating system. Always review the proposed command carefully before typing `y` to approve execution. For untrusted workflows, running this agent inside an isolated Docker container or virtual machine is strongly recommended.
