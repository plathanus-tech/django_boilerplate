import json
from django.urls import reverse


def send_auth_post(*, client, payload):
    response = client.post(
        path=reverse("users:auth"),
        data=json.dumps(payload),
        content_type="application/json",
    )
    return response


def assert_good_auth_response(*, response):
    assert response.status_code == 200
    jsn = response.json()
    expected_keys = [
        "user",
        "access_token",
        "token_type",
    ]
    for expected_key in expected_keys:
        assert expected_key in jsn
    assert jsn["token_type"] == "Token"
