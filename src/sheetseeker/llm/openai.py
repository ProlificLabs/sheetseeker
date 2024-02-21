import os
import asyncio
from typing import List, Dict
from openai import OpenAI, AsyncOpenAI, ChatCompletion

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
DEFAULT_MODEL = "gpt-4-1106-preview"

def call_openai(system_prompt: str, user_prompt: str|None=None, model: str=DEFAULT_MODEL) -> str:
    messages = prepare_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0,
    )
    return message_from_completion(response)

async def acall_openai(system_prompt: str, user_prompt: str|None=None, model: str=DEFAULT_MODEL) -> str:
    messages = prepare_messages(system_prompt, user_prompt)
    response = await async_client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0,
    )
    return message_from_completion(response)

def prepare_messages(system_prompt: str, user_prompt: str|None=None) -> List[Dict[str,str]]:
    messages = [ {
        "role": "system",
        "content": system_prompt,
    }, ]
    if user_prompt:
        messages.append({
            "role": "user",
            "content": user_prompt
        })

    return messages

def message_from_completion(response: ChatCompletion) -> str:
    return response.choices[0].message.content
