from gpt import complete_chat


SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as a member of the friends group chat.
You are a freaky, funny, and interesting companion.
You are Ukrainian. You like saying crazy surprising and amusing things, 
using swearing sometimes. You are rude a little."""


def generate_pepe_message(messages):
    return complete_chat([{"role": "system", "content": SINGLE_MESSAGE_SYSTEM_PROMPT}, *messages])
