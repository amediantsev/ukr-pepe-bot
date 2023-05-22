import json
import traceback
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update
from telegram.error import Unauthorized

from exceptions import ProcessMessageError
from tg import ADMIN_IDS, send_message, bot
from users import USERNAMES

logger = Logger()


def handle_errors(f):
    def wrapper(event, context):
        try:
            return f(event, context)
        except ProcessMessageError as e:
            message = Update.de_json(json.loads(event.get("body") or "{}"), bot).message
            if e.message and message:
                send_message(user_chat_id=message.from_user.id, text=e.message)
        except Unauthorized:
            user_chat_id = event.get("user_chat_id")
            if user_chat_id and user_chat_id not in ADMIN_IDS:
                logger.error(f"user {user_chat_id} has blocked bot")
        except Exception:
            message = Update.de_json(json.loads(event.get("body") or "{}"), bot).message
            if message:
                username = USERNAMES.get(message.from_user.id)
            else:
                username = None
            logger.exception("Unexpected error.")
            for admin_id in ADMIN_IDS:
                send_message(
                    user_chat_id=admin_id,
                    text=f"Error happened for @{username}:\n\n{traceback.format_exc()}",
                    disable_markdown=True,
                )
            send_message(user_chat_id=message.from_user.id, text="Sorry, something went wrong.")

        return {"statusCode": HTTPStatus.OK}

    return wrapper
