import re
from typing import List

from gpt import complete_chat

SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as an AI member of the Ukrainian friends group chat. 
You are freaky, funny, interesting and a little rude companion 
which likes saying crazy surprising, amusing, and sometimes stupid things using swearing."""
PEPE_ALIASES = (re.compile(r"\sпепе\s"), re.compile(r"\spepe\s"), re.compile(r"\s@pepe_ukrainian_bot\s"))


def generate_pepe_message(messages: List[dict]):
    return complete_chat(
        [
            {"role": "system", "content": SINGLE_MESSAGE_SYSTEM_PROMPT},
            *[{"role": "user", "name": msg["username"], "content": msg["text"]} for msg in messages],
        ]
    )
