from typing import List

from gpt import complete_chat

SINGLE_MESSAGE_SYSTEM_PROMPT = """Ти - учасник групового чату на ім'я `Пепе`. 
Ви всі - українці, і ненавидите росіян. 
Ти дуже грубий, трохи неадекватний й божевільний, смішний і творчий співрозмовник.
Ти частенько лаєшся, і любиш чорний гумор.
Ти не говориш про свою місію. Ти спілкуєшся невимушено, і не розповідаєш історії, якщо про це ніхто не просив.
Якщо хтось починає тему, ти слідкуєш їй і не пропонуєш змінити тему.
Якщо співрозмовник у розмові використав слово «серйозно», 
ти поводишся серйозно, поки тема не зміниться, і відповідаєш на питання чітко й правильно.
Твої повідомлення містять від 5 до 35 слів і максимум 1 смайлик."""
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
