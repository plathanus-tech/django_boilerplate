from app.ext.sms import send_sms


def testSendSmsWontFail():
    send_sms(receiver="+5548912345678", body="Hello World!")
