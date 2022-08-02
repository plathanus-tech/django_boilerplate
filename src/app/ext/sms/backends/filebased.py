from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .base import BaseSmsBackend


class FileBasedSmsBackend(BaseSmsBackend):
    def send(self, *, receiver: str, body: str) -> None:
        with open(self.file_path, "w") as f:
            f.write("SMS\n")
            f.write(f"{receiver=}")
            f.write("-" * 50)
            f.write(body)

    @property
    def file_path(self):
        path: Path = settings.SMS_FILE_PATH
        return path / self.file_name

    @property
    def file_name(self):
        return timezone.now().strftime("%Y-%m-%d %H-%M-%S") + ".log"
