from django.test import Client


def test_admin_is_present(client: Client):
    response = client.get("/admin/login/")
    assert response.status_code == 200
