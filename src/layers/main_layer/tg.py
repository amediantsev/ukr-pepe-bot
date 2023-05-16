import os

from telegram import Bot, ParseMode


ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))


def send_message(user_chat_id, text, disable_markdown=False):
    send_message_kwargs = {"chat_id": user_chat_id, "text": text}
    if not disable_markdown:
        send_message_kwargs["parse_mode"] = ParseMode.MARKDOWN
    bot.sendMessage(**send_message_kwargs)
