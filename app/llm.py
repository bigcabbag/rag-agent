from functools import lru_cache

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.config import get_settings


@lru_cache
def get_llm() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings["model"],
        api_key=SecretStr(settings["api_key"]),
        base_url=settings["base_url"],
        temperature=0.7,
    )


async def chat(message: str, system_prompt: str | None = None) -> str:
    llm = get_llm()
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    response = await llm.ainvoke(messages)
    content = response.content
    if isinstance(content, str):
        return content
    return str(content)


async def chat_stream(message: str, system_prompt: str | None = None):
    """逐 token 生成，供 SSE 流式接口使用。"""
    llm = get_llm()
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    async for chunk in llm.astream(messages):
        content = chunk.content
        if not content:
            continue
        if isinstance(content, str):
            yield content
        else:
            yield str(content)
