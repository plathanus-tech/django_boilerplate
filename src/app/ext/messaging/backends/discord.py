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


class DiscordMessagingExternalService(MessagingExternalService):
    suitable_for_production = True

    def __init__(self):
        self.oauth_token = settings.MESSAGING_EXTERNAL_SERVICE_DISCORD_OAUTH_TOKEN

    def send(self, *, to: str, message: Message, files: Sequence[EmbedFile]):
        formatted_message = str(message)
        for to_replace, replaced in format_replacers.items():
            formatted_message = formatted_message.replace(to_replace, replaced)

        embed_files: list[tuple[str, tuple[str, StringIO, str]]] = []
        attachments = []
        for n, file in enumerate(files):
            file.io.seek(0)
            embed_files.append(
                (
                    f"files[{n}]",
                    (file.filename, file.io, file.content_type),
                )
            )
            attachments.append({"id": n, "filename": file.filename})

        DISCORD_MESSAGE_LIMIT = 2000
        if len(formatted_message) > DISCORD_MESSAGE_LIMIT:
            formatted_message = formatted_message[:DISCORD_MESSAGE_LIMIT]
        json_payload: dict[str, Any] = {"content": formatted_message}
        if attachments:
            json_payload["attachments"] = attachments

        try:
            response = requests.post(
                url=f"https://discord.com/api/channels/{to}/messages",
                headers={"Authorization": f"Bot {self.oauth_token}"},
                data={"payload_json": json.dumps(json_payload)},
                files=embed_files or None,
                timeout=5,
            )
            response.raise_for_status()
        except (requests.Timeout, requests.HTTPError) as e:
            print("Failed to send message", e)
            return
