import json
import os
import random
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update, Message
from telegram.constants import CHAT_GROUP, CHAT_SUPERGROUP

from pepe import PEPE_ALIASES, CONTEXT_LENGTH
from tg import bot
from decorators import handle_errors
import aws.dynamodb as dynamodb_operations
from aws.aws_lambda import invoke as invoke_lambda
from users import USERNAMES

logger = Logger()

TWO_MINUTES = 2 * 60
SIX_HOURS = 6 * 60 * 60
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")
PROCEED_CONVERSATION_ARN = os.getenv("PROCEED_CONVERSATION_ARN", "")
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
            update.message.text and len(update.message.text) > 200,
        )
    )


def sending_message_triggered(message: Message, last_pepe_reply=None):
    message_text = message.text.lower()
    return any(
        (
            message.reply_to_message and message.reply_to_message.from_user.id == bot.id,
            any(filter(lambda pepe_alias: pepe_alias in message_text, PEPE_ALIASES)),
            last_pepe_reply and (message.date.timestamp() - float(last_pepe_reply)) < TWO_MINUTES,
            random.random() < 0.07,
        )
    )


@handle_errors
def handler(event, _):
    update = Update.de_json(json.loads(event.get("body") or "{}"), bot)
    if skip_update(update):
        return {"statusCode": HTTPStatus.OK}
    # logger.info(update)
    message = dict(username=USERNAMES.get(update.message.from_user.id, "Павло"), text=update.message.text)
    conversation = dynamodb_operations.get_conversation(update.message.chat_id)
    if not conversation or update.message.date.timestamp() - float(conversation["updated_at"]) > SIX_HOURS:
        dynamodb_operations.create_conversation(chat_id=update.message.chat_id, **message)
    else:
        dynamodb_operations.append_conversation_message(
            chat_id=update.message.chat_id,
            **message,
            pop_old_message=len(conversation.get("messages", [])) >= CONTEXT_LENGTH
        )

    if sending_message_triggered(update.message, last_pepe_reply=conversation.get("last_pepe_reply")):
        invoke_lambda(
            func_identifier=PROCEED_CONVERSATION_ARN,
            event={"messages": conversation.get("messages", []) + [message], "chat_id": update.message.chat_id},
        )

    return {"statusCode": HTTPStatus.OK}
