from unittest.mock import MagicMock

import pytest


@pytest.mark.parametrize(
    ("message_text", "triggered"),
    (
        ("Привіт, пепе. Як твої справи?", True),
        ("PEPE, дурню, шо там?", True),
        ("Пепе!", True),
        ("@pepe_ukrainian_bot ти як там?", True),
        ("Бла-бла, просто балакаємо", False),
        ("jopa popa 123", False),
        ("", False),
    ),
)
def test_trigger_sending_with_mention(message_text, triggered):
    from src.handlers.messages.main import send_message_triggered

    assert send_message_triggered(MagicMock(text=message_text)) == triggered
