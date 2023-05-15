from http import HTTPStatus

from aws_lambda_powertools import Logger

from pepe import generate_pepe_message
from tg import bot
from decorators import handle_errors

logger = Logger()


EBOSHIM_MOSHСNO_CHAT_ID = "-1001318344639"
RANDOM_SINGLE_MESSAGE_USER_PROMPT = "Напиши дурне смішне повідомлення довжиною від 5 до 40 слів"


@handle_errors
def handler(event, _):
    bot.send_message(
        chat_id=EBOSHIM_MOSHСNO_CHAT_ID,
        text=generate_pepe_message([{"role": "user", "content": RANDOM_SINGLE_MESSAGE_USER_PROMPT}])
    )

    return {"statusCode": HTTPStatus.OK}
