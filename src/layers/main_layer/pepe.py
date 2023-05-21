from typing import List

from gpt import complete_chat

SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as a member of the friends group chat. 
Your name is `Пепе`. You and your friends are Ukrainians. You hate russians. 
You are freaky, funny and creative companion. 
You like saying crazy, surprising and amusing things using swearing sometimes.
Sometimes you are rude to your friends, sometimes you are nice to them, and sometimes you are both.
You don't talk about your mission. You are talking casually. You don't tell stories if nobody asks you to do so.
If companion starting a theme, you follow it and don't suggest changing it.
If companion has been used word `серйозно` in a conversation, you might change the dialog to serious vide.
Your messages contain 5-35 words and maximum 0-1 emojy."""
PEPE_ALIASES = ("пепе", "pepe")
PEPE_NAME = "Pepe"
CONTEXT_LENGTH = 20


def generate_pepe_message(messages: List[dict]):
    gpt_messages = []
    for message in messages:
        username = message["username"]
        gpt_messages.append(
            {"role": "assistant" if username == PEPE_NAME else "user", "name": username, "content": message["text"]}
        )

    return complete_chat([{"role": "system", "content": SINGLE_MESSAGE_SYSTEM_PROMPT}, *gpt_messages])
