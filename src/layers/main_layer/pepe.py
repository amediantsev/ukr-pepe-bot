from typing import List

from gpt import complete_chat

SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as an AI member of the Ukrainian friends group chat. 
You are freaky, funny, interesting and a little rude companion 
which likes saying crazy surprising, amusing things using swearing. 
Your messages takes 5-30 words with maximum 1 emojy."""
PEPE_ALIASES = ("пепе", "pepe")
PEPE_NAME = "Pepe"


def generate_pepe_message(messages: List[dict]):
    gpt_messages = []
    for message in messages:
        username = message["username"]
        gpt_messages.append(
            {"role": "assistant" if username == PEPE_NAME else "user", "name": username, "content": message["text"]}
        )
    return complete_chat([{"role": "system", "content": SINGLE_MESSAGE_SYSTEM_PROMPT}, *gpt_messages])
