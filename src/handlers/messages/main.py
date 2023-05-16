import json
import os
import random
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update, Message
from telegram.constants import CHAT_GROUP, CHAT_SUPERGROUP

from pepe import generate_pepe_message, PEPE_ALIASES
from tg import bot
from decorators import handle_errors
import aws.dynamodb as dynamodb_operations
from users import USERNAMES, USERNAMES_TO_UKR

logger = Logger()

GPT_CONTEXT_LENGTH = 6
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")
# EBOSHIM_MOSHСNO_CHAT_ID = "-1001318344639"
SINGLE_MESSAGE_USER_PROMPT = "Напиши повідомлення довжиною від 5 до 30 слів у продовження до бесіди :\n"
RANDOM_SINGLE_MESSAGE_USER_PROMPT = "Напиши дурне смішне повідомлення довжиною від 5 до 30 слів"


def skip_update(update: Update) -> bool:
    return any(
        (
            not update.message,
            (
                update.message.chat.type not in (CHAT_GROUP, CHAT_SUPERGROUP)
                and str(update.message.chat_id) not in ADMIN_IDS
            ),
            len(update.message.text) > 200,
        )
    )


def send_message_triggered(message: Message):
    message_text = message.text.lower()
    return any(
        (
            message.reply_to_message and message.reply_to_message.from_user.id == bot.id,
            any(filter(lambda pepe_alias: pepe_alias.match(message_text), PEPE_ALIASES)),
            random.random() < 0.07,
        )
    )


@handle_errors
def handler(event, _):
    update = Update.de_json(json.loads(event.get("body") or "{}"), bot)
    if skip_update(update):
        return {"statusCode": HTTPStatus.OK}
    logger.info(update)
    # messages = [
    #     {
    #         "role": "user",
    #         "name": USERNAMES.get(update.message.from_user.id, "Павло"),
    #         # "content": f"{RANDOM_SINGLE_MESSAGE_USER_PROMPT} у відповідь на `{update.message.text}`",
    #         "content": update.message.text,
    #     }
    # ]
    # message = dict(
    #     username=USERNAMES.get(update.message.from_user.id, "Павло"),
    #     text=f"{RANDOM_SINGLE_MESSAGE_USER_PROMPT} у відповідь на `{update.message.text}`",
    # )
    message = dict(username=USERNAMES.get(update.message.from_user.id, "Павло"), text=update.message.text)
    conversation = dynamodb_operations.get_conversation(update.message.chat_id)
    if not conversation:
        dynamodb_operations.create_conversation(chat_id=update.message.chat_id, **message)
    else:
        dynamodb_operations.append_conversation_message(
            chat_id=update.message.chat_id,
            **message,
            pop_old_message=len(conversation.get("messages", [])) > GPT_CONTEXT_LENGTH
        )

    if send_message_triggered(update.message):
        pepe_reply = generate_pepe_message(conversation.get("messages", []) + [message])
        for name, ukr_name in USERNAMES_TO_UKR.items():
            pepe_reply = pepe_reply.replace(name, ukr_name)
        bot.send_message(update.message.chat_id, text=pepe_reply)

    return {"statusCode": HTTPStatus.OK}
