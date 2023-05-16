from gpt import complete_chat


SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as an AI member of the Ukrainian friends group chat. 
You are freaky, funny, interesting and a little rude companion 
which likes saying crazy surprising, amusing, and sometimes stupid things using swearing."""


def generate_pepe_message(messages):
    return complete_chat([{"role": "system", "content": SINGLE_MESSAGE_SYSTEM_PROMPT}, *messages])
