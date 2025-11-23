import os
from langchain_openai import ChatOpenAI
from config import CONFIG

model = ChatOpenAI(
    model=CONFIG.llm_model,
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=10,
    max_tokens=CONFIG.max_tokens
)

