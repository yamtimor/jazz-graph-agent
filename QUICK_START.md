# Quick Start Guide - Multi-Provider LLM Support

## ✅ Implementation Complete!

Your jazz-graph-agent now supports both OpenAI and HuggingFace models.

## What's New

- **Provider Selection**: Choose between OpenAI or HuggingFace via environment variable
- **Model Flexibility**: Use GPT-4, Llama-3, Mixtral, or any instruction-tuned model
- **Unified Interface**: Same code works with any provider
- **Structured Output**: Pydantic validation across all models via Instructor library

## Getting Started

### Option 1: Use OpenAI (Fastest Setup)

1. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Create `.env` file**:
   ```env
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4o-mini
   OPENAI_API_KEY=your-openai-key
   ```

3. **Run**:
   ```bash
   python main.py
   ```

### Option 2: Use HuggingFace (Open Models)

1. **Install dependencies** (same as above)

2. **Create `.env` file**:
   ```env
   LLM_PROVIDER=huggingface
   LLM_MODEL=meta-llama/Llama-3.1-70B-Instruct
   HUGGINGFACE_API_KEY=your-hf-key
   ```

3. **Run**:
   ```bash
   python main.py
   ```

## Switching Providers

Just change the environment variables! No code changes needed:

```env
# Switch from OpenAI to HuggingFace
LLM_PROVIDER=huggingface
LLM_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
HUGGINGFACE_API_KEY=hf_xxxxx
```

## Recommended Models

### OpenAI
- `gpt-4o-mini` - Best value, fast (default)
- `gpt-4o` - Highest quality
- `gpt-4-turbo` - Good balance

### HuggingFace  
- `meta-llama/Llama-3.1-70B-Instruct` - Best quality
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - Great performance
- `meta-llama/Llama-3.2-11B-Vision-Instruct` - Faster, lighter

## Getting API Keys

**OpenAI**: https://platform.openai.com/api-keys  
**HuggingFace**: https://huggingface.co/settings/tokens

## Troubleshooting

**Dependency conflicts during install?**
→ See `INSTALL.md` for clean installation steps

**Module not found errors?**
→ Make sure you're in the virtual environment: `source .venv/bin/activate`

**API key errors?**
→ Check your `.env` file is in the project root

## Documentation

- `INSTALL.md` - Detailed installation guide
- `docs/ENV_TEMPLATE.md` - Environment variable examples
- `docs/MULTI_PROVIDER_SETUP.md` - Complete setup documentation
- `docs/IMPLEMENTATION_SUMMARY.md` - Technical implementation details

## Example Output

Regardless of provider, you'll get:
- Console logs showing progress
- `data/output/jazz_graph.html` - Interactive network visualization
- Same graph structure and SNA metrics

The output quality may vary slightly between models, but the structure remains consistent.

## Next Steps

1. Install dependencies (if you haven't)
2. Get an API key (OpenAI or HuggingFace)
3. Create your `.env` file
4. Run `python main.py`
5. Open `data/output/jazz_graph.html` in your browser

Enjoy exploring jazz collaboration networks with your choice of LLM! 🎵🎷

