import os
from typing import Any
from langchain_openai import ChatOpenAI
from config import CONFIG


def create_llm_model(provider: str = None) -> Any:
    """
    Factory function to create an LLM model based on the provider.
    
    Args:
        provider: LLM provider name ("openai" or "huggingface")
        
    Returns:
        Configured LLM model instance
        
    Raises:
        ValueError: If provider is unsupported or API key is missing
    """
    provider = provider or CONFIG.llm_provider
    
    if provider == "openai":
        api_key = CONFIG.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        return ChatOpenAI(
            model=CONFIG.llm_model,
            temperature=0,
            api_key=api_key,
            timeout=30,
            max_tokens=CONFIG.max_tokens
        )
    
    elif provider == "huggingface":
        api_key = CONFIG.huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("HuggingFace API key not found. Set HUGGINGFACE_API_KEY environment variable.")
        
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        
        llm = HuggingFaceEndpoint(
            repo_id=CONFIG.llm_model,
            huggingfacehub_api_token=api_key,
            temperature=0,
            max_new_tokens=CONFIG.max_tokens,
            timeout=60,
        )
        
        return ChatHuggingFace(llm=llm)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Choose 'openai' or 'huggingface'.")


def get_raw_client(provider: str = None) -> Any:
    """
    Get the raw client for use with Instructor library.
    
    Args:
        provider: LLM provider name
        
    Returns:
        Raw client instance (OpenAI client or HuggingFace endpoint)
    """
    provider = provider or CONFIG.llm_provider
    
    if provider == "openai":
        from openai import OpenAI
        api_key = CONFIG.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        return OpenAI(api_key=api_key)
    
    elif provider == "huggingface":
        from huggingface_hub import InferenceClient
        api_key = CONFIG.huggingface_api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("HuggingFace API key not found. Set HUGGINGFACE_API_KEY environment variable.")
        return InferenceClient(token=api_key, model=CONFIG.llm_model)
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


# Create default model instance
model = create_llm_model()

