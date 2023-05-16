import datetime
import os

from boto3 import resource

table = resource("dynamodb").Table(os.getenv("TABLE_NAME"))


def create_conversation(chat_id, username, text):
    now = datetime.datetime.now()
    table.put_item(
        Item={
            "pk": f"CONVERSATION#{chat_id}",
            "sk": f"CONVERSATION#{chat_id}",
            "chat_id": chat_id,
            "messages": [{"username": username, "text": text}],
            "gsi1pk": "CONVERSATION",
            "created_at": now.isoformat(),
            "expires_at": now.timestamp(),
        },
    )


def get_conversation(chat_id) -> dict:
    return table.get_item(Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{chat_id}"}).get("Item", {})


def append_conversation_message(chat_id, username, text, pop_old_message=False):
    if pop_old_message:
        table.update_item(
            Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{chat_id}"},
            UpdateExpression="REMOVE messages[0]",
        )
    table.update_item(
        Key={"pk": f"CONVERSATION#{chat_id}", "sk": f"CONVERSATION#{chat_id}"},
        UpdateExpression="SET messages = list_append(messages, :new_message)",
        ExpressionAttributeValues={":new_message": [{"username": username, "text": text}]},
    )
