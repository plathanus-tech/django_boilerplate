from dataclasses import dataclass
from io import StringIO
from typing import TYPE_CHECKING, Self, Sequence, Union

from django.conf import settings

from app.ext.abc import ExternalService

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise


@dataclass
class EmbedFile:
    io: StringIO
    filename: str
    content_type: str


class _TextFormat:
    """Base class for formatting text, subclasses may provide the `wrapper_start`
    and `wrapper_end` attributes, that will be used to construct the desired formatting.
    The formatting wrappers don't have any language specific formatting, they need to be
    handled by each messaging service, in order to correctly format the message on that
    platform.
    """

    wrapper_start: str
    wrapper_end: str

    def __init__(self, value: "StrOrPromise"):
        self.value = value

    def __str__(self):
        return "{}{}{}".format(
            self.wrapper_start,
            str(self.value),  # force evaluation
            self.wrapper_end,
        )

    def __add__(self, other: Union["StrOrPromise", Self]) -> str:
        return str(self) + str(other)

    def __radd__(self, other: Union["StrOrPromise", Self]) -> str:
        return str(other) + str(self)


class TextBold(_TextFormat):
    wrapper_start = "<<bold>>"
    wrapper_end = "<</bold>>"


class TextItalic(_TextFormat):
    wrapper_start = "<<italic>>"
    wrapper_end = "<</italic>>"


class TextCodeInline(_TextFormat):
    wrapper_start = "<code>"
    wrapper_end = "</code>"


class TextCodeBlock(_TextFormat):
    wrapper_start = "<<code>>"
    wrapper_end = "<</code>"


class Message:
    """Composable message that can be composable by multiple segments of text formatting.
    The contents of the message will be joined by the given `join_char`.
    """

    def __init__(self, *contents: Union[_TextFormat, "StrOrPromise"], join_char: str = "\n"):
        self.contents = contents
        self.join_char = join_char

    def __str__(self):
        return self.join_char.join(str(c) for c in self.contents)


def messaging_external_service_loader() -> "MessagingExternalService":
    from .backends.discord import DiscordMessagingExternalService
    from .backends.stdout import DevSTDOutMessagingExternalService

    backends = {
        "dev.stdout": DevSTDOutMessagingExternalService,
        "discord": DiscordMessagingExternalService,
    }
    return backends[settings.MESSAGING_EXTERNAL_SERVICE_BACKEND]()


class MessagingExternalService(ExternalService):
    service_loader = messaging_external_service_loader

    def send(self, *, to: str, message: Message, files: Sequence[EmbedFile]) -> None:
        """Sends a message `to` someone or something. Subclasses may handle the `message`
        formatting and the `files` that should be sent with the message."""
        raise NotImplementedError("Missing implementation for method send")
