# Environment Variables Template

Create a `.env` file in the project root with the following configuration:

```env
# LLM Provider Configuration
# Choose provider: openai or huggingface
LLM_PROVIDER=openai

# Model Configuration
# For OpenAI: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
# For HuggingFace: meta-llama/Llama-3.1-70B-Instruct, mistralai/Mixtral-8x7B-Instruct-v0.1, meta-llama/Llama-3.2-11B-Vision-Instruct
LLM_MODEL=gpt-4o-mini

# Optional: Override max tokens (default: 3000)
# MAX_TOKENS=3000

# API Keys
# OpenAI API Key (required if LLM_PROVIDER=openai)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# HuggingFace API Key (required if LLM_PROVIDER=huggingface)
# Get your key from: https://huggingface.co/settings/tokens
# HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
```

## Example Configurations

### OpenAI (default)
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-proj-xxxxx
```

### HuggingFace with Llama-3.1
```env
LLM_PROVIDER=huggingface
LLM_MODEL=meta-llama/Llama-3.1-70B-Instruct
HUGGINGFACE_API_KEY=hf_xxxxx
```

### HuggingFace with Mixtral
```env
LLM_PROVIDER=huggingface
LLM_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
HUGGINGFACE_API_KEY=hf_xxxxx
```

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste into `.env` file

### HuggingFace
1. Visit https://huggingface.co/settings/tokens
2. Create a new access token
3. Copy and paste into `.env` file

