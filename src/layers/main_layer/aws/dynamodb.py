import datetime
import os
from decimal import Decimal

from boto3 import resource

from pepe import PEPE_NAME

table = resource("dynamodb").Table(os.getenv("TABLE_NAME"))


def create_conversation(chat_id, username, text, conversation_type="FUNNY"):
    now = Decimal(datetime.datetime.now().timestamp())
    table.put_item(
        Item={
            "pk": f"CONVERSATION#{chat_id}",
            "sk": f"CONVERSATION#{conversation_type}",
            "chat_id": Decimal(chat_id),
            "messages": [{"username": username, "text": text}],
            "gsi1pk": f"CONVERSATION#{conversation_type}",
            "created_at": now,
            "updated_at": now,
            "expires_at": now,
        },
    )


def get_conversation(chat_id, conversation_type="FUNNY") -> dict:
    item = table.get_item(Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{conversation_type}"})
    return item.get("Item") or {}


def append_conversation_message(chat_id, username, text, conversation_type="FUNNY", pop_old_message=False):
    if pop_old_message:
        table.update_item(
            Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{conversation_type}"},
            UpdateExpression="REMOVE messages[0]",
        )
    print("pop_old_message is ", pop_old_message)
    update_expression = "SET messages = list_append(messages, :new_message), updated_at = :now"
    expression_attribute_values = {
        ":new_message": [{"username": username, "text": text}],
        ":now": Decimal(datetime.datetime.now().timestamp()),
    }
    if username == PEPE_NAME:
        update_expression += ", last_pepe_reply = :now"
    table.update_item(
        Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{conversation_type}"},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
