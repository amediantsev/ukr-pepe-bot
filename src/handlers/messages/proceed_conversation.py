from http import HTTPStatus

from aws_lambda_powertools import Logger

from pepe import generate_pepe_message, PEPE_NAME, CONTEXT_LENGTH
from tg import bot
from decorators import handle_errors
import aws.dynamodb as dynamodb_operations
from users import USERNAMES_TO_UKR

logger = Logger()


@handle_errors
def handler(event, _):
    pepe_reply = generate_pepe_message(event["messages"])
    for name, ukr_name in USERNAMES_TO_UKR.items():
        pepe_reply = pepe_reply.replace(name, ukr_name)
    bot.send_message(event["chat_id"], text=pepe_reply)
    dynamodb_operations.append_conversation_message(
        chat_id=event["chat_id"],
        username=PEPE_NAME,
        text=pepe_reply,
        pop_old_message=len(event["messages"]) > CONTEXT_LENGTH,
    )

    return {"statusCode": HTTPStatus.OK}
