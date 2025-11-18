from langchain.agents import create_agent
from model import model
from prompts import SYSTEM_PROMPT, ResponseFormat
from tools import Tools, Context

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=Tools,
    context_schema=Context,
    response_format=ResponseFormat,
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "a placeholder message"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])