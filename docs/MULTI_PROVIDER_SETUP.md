# Multi-Provider LLM Setup Guide

## Overview

The jazz-graph-agent now supports multiple LLM providers through a unified interface:
- **OpenAI** (GPT-4, GPT-4o, GPT-3.5)
- **HuggingFace** (Llama, Mixtral, and other instruction-tuned models)

## Architecture

### Key Components

1. **Model Factory** (`agent/model.py`)
   - `create_llm_model(provider)` - Creates provider-specific LLM instances
   - `get_raw_client(provider)` - Returns raw API clients for Instructor integration
   - Validates API keys and configuration at runtime

2. **Instructor Integration** (`agent/agent.py`)
   - Uses Instructor library for cross-provider structured output
   - Maintains Pydantic schema validation across all providers
   - Handles provider-specific message formatting

3. **Configuration** (`config.py`)
   - `llm_provider` - Select "openai" or "huggingface"
   - `llm_model` - Provider-specific model name
   - Provider-specific API keys loaded from environment

## Quick Start

### Option 1: OpenAI (Default)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-proj-xxxxx
```

3. Run:
```bash
python main.py
```

### Option 2: HuggingFace

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```env
LLM_PROVIDER=huggingface
LLM_MODEL=meta-llama/Llama-3.1-70B-Instruct
HUGGINGFACE_API_KEY=hf_xxxxx
```

3. Run:
```bash
python main.py
```

## Supported Models

### OpenAI Models

| Model | Context | Speed | Quality | Use Case |
|-------|---------|-------|---------|----------|
| `gpt-4o-mini` | 128K | Fast | Good | Default, cost-effective |
| `gpt-4o` | 128K | Medium | Excellent | Complex networks |
| `gpt-4-turbo` | 128K | Medium | Excellent | Balanced performance |
| `gpt-3.5-turbo` | 16K | Very Fast | Fair | Testing, simple networks |

### HuggingFace Models

| Model | Context | Speed | Quality | Notes |
|-------|---------|-------|---------|-------|
| `meta-llama/Llama-3.1-70B-Instruct` | 128K | Medium | Excellent | Best quality |
| `meta-llama/Llama-3.1-8B-Instruct` | 128K | Fast | Good | Lighter, faster |
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | 32K | Medium | Excellent | Great balance |
| `meta-llama/Llama-3.2-11B-Vision-Instruct` | 128K | Fast | Good | Newer, efficient |

## Testing Your Setup

Run the validation script to check your configuration:

```bash
python test_provider_setup.py
```

This will verify:
- All imports are available
- Configuration is valid
- Provider validation works
- Pydantic models are correct
- Instructor library is installed

## Troubleshooting

### "No module named 'instructor'"
```bash
pip install instructor==1.8.0
```

### "No module named 'langchain_huggingface'"
```bash
pip install langchain-huggingface==0.1.2
```

### "API key not found"
- Check your `.env` file exists in project root
- Verify the key name matches: `OPENAI_API_KEY` or `HUGGINGFACE_API_KEY`
- Ensure no extra spaces or quotes around the key

### "Unsupported LLM provider"
- Verify `LLM_PROVIDER` is either "openai" or "huggingface" (lowercase)
- Check for typos in `.env` file

### HuggingFace model not working
- Verify model name format: `organization/model-name`
- Check model supports Inference API (not all HF models do)
- Try a recommended model from the table above

## How It Works

### Structured Output with Instructor

The agent uses the [Instructor](https://github.com/jxnl/instructor) library to enable Pydantic-based structured output across any LLM provider:

```python
# OpenAI
client = get_raw_client("openai")
instructor_client = instructor.from_openai(client)

# HuggingFace
client = get_raw_client("huggingface")
instructor_client = instructor.from_huggingface(client, mode=Mode.JSON)

# Both use the same Pydantic schema
result = instructor_client.chat.completions.create(
    model=CONFIG.llm_model,
    response_model=JazzNetworkGraph,  # Pydantic model
    messages=[...]
)
```

This ensures consistent data validation regardless of provider.

## Performance Notes

- **OpenAI**: Generally faster and more reliable, especially for structured output
- **HuggingFace**: May have occasional timeouts or formatting issues, but offers access to open models
- **Timeout Settings**: Increased to 30s (OpenAI) and 60s (HuggingFace) to handle larger graphs

## Future Enhancements

- Support for local models via Ollama
- Anthropic Claude integration
- Google Gemini support
- Custom provider plugins
- Model performance benchmarking

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy key to `.env` file

### HuggingFace
1. Visit https://huggingface.co/settings/tokens
2. Sign in or create account
3. Click "New token"
4. Select "read" access level
5. Copy token to `.env` file

Note: HuggingFace Inference API has a free tier, but rate limits apply.

