import json
from io import StringIO
from typing import Any, Sequence

import requests
from django.conf import settings

from app.ext.messaging.abc import (
    EmbedFile,
    Message,
    MessagingExternalService,
    TextBold,
    TextCodeBlock,
    TextCodeInline,
    TextItalic,
)

format_replacers = {
    TextBold.wrapper_start: "**",
    TextBold.wrapper_end: "**",
    TextCodeInline.wrapper_start: "`",
    TextCodeInline.wrapper_end: "`",
    TextCodeBlock.wrapper_start: "```python\n",
    TextCodeBlock.wrapper_end: "```",
    TextItalic.wrapper_start: "*",
    TextItalic.wrapper_end: "*",
}


class DevSTDOutMessagingExternalService(MessagingExternalService):
    suitable_for_production = False

    def send(self, *, to: str, message: Message, files: Sequence[EmbedFile]):
        formatted_message = str(message)
        for to_replace, replaced in format_replacers.items():
            formatted_message = formatted_message.replace(to_replace, replaced)

        print("Received messaging send request")
        print("To:", to)
        print("Message:", formatted_message)
        print("Files:", files)
