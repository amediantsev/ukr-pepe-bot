import json
from http import HTTPStatus

from aws_lambda_powertools import Logger
from telegram import Update

from tg import bot
from decorators import handle_errors

logger = Logger()


@handle_errors
def handler(event, _):
    logger.info(event)
    update = Update.de_json(json.loads(event.get("body")), bot)
    logger.info(update)

    return {"statusCode": HTTPStatus.OK}
