from pathlib import Path

from app.ext.sms import send_sms


def testSendSmsWontFail():
    send_sms(receiver="+5548912345678", body="Hello World!")


def testSendSmsFileBasedBackendWritesToFile(settings, tmp_path: Path):
    settings.SMS_BACKEND = "app.ext.sms.backends.filebased.FileBasedSmsBackend"
    settings.SMS_FILE_PATH = tmp_path

    send_sms(receiver="+5548912345678", body="Hello World!")

    files = list(tmp_path.iterdir())
    assert files
