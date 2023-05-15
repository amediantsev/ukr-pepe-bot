import json
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update

from tg import bot
from decorators import handle_errors

logger = Logger()


SINGLE_MESSAGE_SYSTEM_PROMPT = """Act as a member of the friends group chat.
You are a freaky, funny, and interesting companion.
You are Ukrainian. You like saying crazy surprising and amusing things, 
using swearing sometimes. You are rude a little."""
SINGLE_MESSAGE_USER_PROMPT = "Напиши повідомлення довжиною від 5 до 40 слів у продовження до бесіди :\n"


def generate_single_message_user_prompt(messages):
    return SINGLE_MESSAGE_USER_PROMPT + "\n\n".join(f"{username}:\n{text}" for username, text in messages)


@handle_errors
def handler(event, _):
    update = Update.de_json(json.loads(event.get("body")), bot)

    logger.info(update)

    return {"statusCode": HTTPStatus.OK}
