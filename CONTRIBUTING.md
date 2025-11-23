# Contributing to Jazz Graph Agent

Thank you for your interest in contributing!  
Jazz Graph Agent is an LLM-powered tool for mapping jazz musicians as a
collaboration network using SNA and interactive visualizations.  
Contributions of all kinds are welcome — code, issues, ideas, fixes, docs,
or even jazz knowledge.

---

## 🧭 Ways to Contribute

### ✔️ Report Bugs
Found a crash? Incorrect graph behavior? Malformed JSON from the LLM?  
Please open an issue with:

- What happened  
- Expected behavior  
- Steps to reproduce  
- Logs or traceback (if any)  

You can use the **Bug Report** issue template.

---

### ✔️ Suggest Features
Want support for more models (Ollama/HF)?  
More jazz metadata?  
Better visualizations?

Open a **Feature Request** issue with clear motivation.

---

### ✔️ Work on Open Issues
The repository maintains organized issues labeled as:

- `good first issue`
- `help wanted`
- `enhancement`
- `bug`
- `refactor`
- `agent`
- `sna`

Browse the issue tracker and pick something you like.  
Comment on the issue to get assigned before starting work.

---

## 🚀 Development Setup

### 1. Clone the repo
```bash
git clone https://github.com/yamtimor/jazz-graph-agent
cd jazz-graph-agent
```
### 2. Install dependencies
`pip install -r requirements.txt`

### 3. Set up environment variables
Create a .env file:
```
OPENAI_API_KEY=your-key-here
LLM_PROVIDER=openai  # or 'ollama' / 'hf-local'
```
(If you don’t want to use OpenAI, see Issue: “Add multi-model support.”)

### 🧪 Running the Project
`python main.py`
This will:
1. Run the LLM-powered agent
2. Parse musician collaborations
3. Build a NetworkX graph
4. Compute SNA metrics
5. Generate an interactive HTML graph
6. (Optional) Generate an SNA jazz analysis report

Outputs appear in data/output/.

### 🛠 Code Style & Standards
- Follow Python conventions (PEP8)
- Keep functions small and modular
- Add docstrings for new functions/classes
- Prefer pure/deterministic logic inside pipeline/
- Keep LLM logic inside the agent/ directory

### 🔀 Pull Requests
Before opening a PR:
1. Make sure an issue exists (or create one)
2. Comment “I’d like to take this”
3. Wait for confirmation before starting

### PR Requirements
- Clear title using Conventional Commits:
```
feat(...): <description>
fix(...): <description>
refactor(...): <description>
docs(...): <description>
```
- Describe what you changed
- Reference the issue (e.g., “Closes #12”)
- Include tests if applicable
- Keep PRs small and focused

### 🧪 Testing
Tests are gradually being added.
If you contribute new logic, please add a simple test using pytest.

### 🤝 Code of Conduct
Be respectful, collaborative, and constructive.

### 🎺 Thank You
Your contributions help the project grow and improve.
Whether you’re a jazz lover, graph wizard, or agentic AI builder — welcome aboard!
