import functools
import json
import random
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update

from pepe import generate_pepe_message
from tg import bot
from decorators import handle_errors

logger = Logger()


# EBOSHIM_MOSHСNO_CHAT_ID = "-1001318344639"
SINGLE_MESSAGE_USER_PROMPT = "Напиши повідомлення довжиною від 5 до 30 слів у продовження до бесіди :\n"
RANDOM_SINGLE_MESSAGE_USER_PROMPT = "Напиши дурне смішне повідомлення довжиною від 5 до 30 слів"


def generate_single_message_user_prompt(messages):
    return SINGLE_MESSAGE_USER_PROMPT + "\n\n".join(f"{username}:\n{text}" for username, text in messages)


@handle_errors
def handler(event, _):
    update = Update.de_json(json.loads(event.get("body")), bot)
    # logger.info(update)
    funny_reply = functools.partial(
        bot.send_message,
        chat_id=update.message.chat_id,
        text=generate_pepe_message(
            [
                {
                    "role": "user",
                    "content": f"{RANDOM_SINGLE_MESSAGE_USER_PROMPT} у відповідь на `{update.message.text}`",
                }
            ]
        ),
        reply_to_message_id=update.message.message_id,
    )
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == bot.id:
        funny_reply()
        return {"statusCode": HTTPStatus.OK}

    if random.random() < 0.05:
        funny_reply()
    return {"statusCode": HTTPStatus.OK}
