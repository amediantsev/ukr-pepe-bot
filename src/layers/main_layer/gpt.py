import os
from typing import List

import backoff
import openai

from exceptions import GptResponseFormatError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


@backoff.on_exception(backoff.expo, GptResponseFormatError, max_tries=3)
def complete_chat(messages: List[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.75,
    )
    # print(response)
    return response["choices"][0]["message"]["content"]
