# Installation Guide

## Clean Installation (Recommended)

If you encounter dependency conflicts, use this fresh installation method:

### 1. Remove old virtual environment
```bash
rm -rf .venv
```

### 2. Create new virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### 4. Install core dependencies first
```bash
pip install pydantic==2.12.4 pydantic-core==2.41.5
pip install openai>=2.0.0
```

### 5. Install langchain packages
```bash
pip install langchain langchain-core langchain-openai
```

### 6. Install instructor (for structured output)
```bash
pip install "instructor>=1.5.0"
```

### 7. Install HuggingFace support
```bash
pip install huggingface-hub langchain-huggingface
```

### 8. Install remaining dependencies
```bash
pip install -r requirements.txt
```

## Quick Test

After installation, verify everything works:

```bash
python -c "from agent.model import create_llm_model; from config import CONFIG; print('✓ Setup successful!')"
```

## Troubleshooting

### Dependency Conflicts

If you still see conflicts, try installing with flexible versions:

```bash
# Remove problematic packages
pip uninstall -y langchain langchain-core langchain-openai langchain-huggingface instructor

# Reinstall without version pins
pip install langchain langchain-core langchain-openai langchain-huggingface "instructor>=1.5.0"
```

### Missing Packages

If you get "ModuleNotFoundError", install the missing package:

```bash
pip install <package-name>
```

## Environment Setup

Create `.env` file (see `docs/ENV_TEMPLATE.md` for details):

```env
# For OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key-here

# OR for HuggingFace
# LLM_PROVIDER=huggingface
# LLM_MODEL=meta-llama/Llama-3.1-70B-Instruct
# HUGGINGFACE_API_KEY=your-key-here
```

## Run the Agent

```bash
python main.py
```

## Windows-Specific Notes

If using Windows with WSL:

1. Create venv in WSL (not Windows)
2. Install in WSL environment
3. Run from WSL

```bash
wsl
cd /mnt/c/Users/YOUR_USERNAME/jazz-graph-agent
python3 -m venv .venv
source .venv/bin/activate
# Follow installation steps above
```

