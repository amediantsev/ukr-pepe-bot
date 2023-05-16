import os
from typing import List

import openai
from aws_lambda_powertools import Logger

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logger = Logger()


def complete_chat(messages: List[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6,
        max_tokens=125,
    )
    return response["choices"][0]["message"]["content"]
