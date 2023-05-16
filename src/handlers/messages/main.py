import functools
import json
import os
import random
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update
from telegram.constants import CHAT_GROUP, CHAT_SUPERGROUP

from pepe import generate_pepe_message
from tg import bot
from decorators import handle_errors

logger = Logger()

ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")
# EBOSHIM_MOSHСNO_CHAT_ID = "-1001318344639"
SINGLE_MESSAGE_USER_PROMPT = "Напиши повідомлення довжиною від 5 до 30 слів у продовження до бесіди :\n"
RANDOM_SINGLE_MESSAGE_USER_PROMPT = "Напиши дурне смішне повідомлення довжиною від 5 до 30 слів"

USERNAMES = {
    355526766: "Sashko",
    279746664: "Vladik",
    243907313: "Olegi",
    229665876: "Borys",
    "...": "Pavlo",
}
USERNAMES_TO_UKR = {
    "Sashko": "Сашко",
    "Vladik": "Владік",
    "Olegi": "Олегі",
    "Borys": "Борис",
    "Pavlo": "Павло",
}


@handle_errors
def handler(event, _):
    update = Update.de_json(json.loads(event.get("body")), bot)
    if any(
        (
            not update.message,
            (
                update.message.chat.type not in (CHAT_GROUP, CHAT_SUPERGROUP)
                and str(update.message.chat_id) not in ADMIN_IDS
            ),
        )
    ):
        return {"statusCode": HTTPStatus.OK}
    logger.info(update)
    messages = [
        {
            "role": "user",
            "name": USERNAMES.get(update.message.from_user.id, "Павло"),
            # "content": f"{RANDOM_SINGLE_MESSAGE_USER_PROMPT} у відповідь на `{update.message.text}`",
            "content": update.message.text,
        }
    ]
    if (
        update.message.reply_to_message and update.message.reply_to_message.from_user.id == bot.id
        or random.random() < 0.1
    ):
        pepe_reply = generate_pepe_message(messages)
        for name in USERNAMES.values():
            pepe_reply = pepe_reply.replace(name, USERNAMES_TO_UKR.get(name))
        bot.send_message(update.message.chat_id, text=pepe_reply)

    return {"statusCode": HTTPStatus.OK}
