import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince

from app.consts.http import HttpStatusCode
from app.consts.push_notification import Status
from push_notifications import services
from push_notifications.models import PushNotification
from users.models import User


@pytest.fixture
def visitor_notification(visitor_user: User):
    return services.push_notification_create(
        user=visitor_user,
        kind="int_comm",
        title="Hey!",
        description="Hello world",
        data={"foo": "bar"},
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "method_name,url_name,reverse_args",
    [
        ("GET", "api:v1:push_notifications:notifications-list", ()),
        ("PATCH", "api:v1:push_notifications:notifications-read", (1,)),
        ("PATCH", "api:v1:push_notifications:notifications-read-many", ()),
        ("PUT", "api:v1:push_notifications:notifications-token", ()),
        ("DELETE", "api:v1:push_notifications:notifications-token", ()),
    ],
)
def test_pn_endpoints_requires_authentication(client: Client, method_name, url_name, reverse_args):
    url = reverse(url_name, args=reverse_args)
    methods = {"GET": client.get, "PATCH": client.patch, "PUT": client.put, "DELETE": client.delete}
    method = methods[method_name]

    response = method(url)
    assert response.status_code == HttpStatusCode.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_pn_list_returns_expected_output(visitor_notification: PushNotification, client: Client):
    url = reverse("api:v1:push_notifications:notifications-list")
    client.force_login(user=visitor_notification.user)
    response = client.get(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 1
    result = data["results"][0]
    assert result == {
        "id": visitor_notification.id,
        "title": visitor_notification.title,
        "description": visitor_notification.description,
        "read_at": None,
        "kind": {
            "value": visitor_notification.kind,
            "human": visitor_notification.get_kind_display(),
        },
        "status": {
            "value": visitor_notification.status,
            "human": visitor_notification.get_status_display(),
        },
        "data": {
            "id": str(visitor_notification.id),
            "createdAt": visitor_notification.created_at.isoformat(),
            "readAt": None,
            "timeSinceCreated": timesince(visitor_notification.created_at),
            "kind": visitor_notification.kind,
            "meta": visitor_notification.data,
        },
    }


@pytest.mark.django_db
def test_pn_list_query_params_invalid(visitor_notification: PushNotification, client: Client):
    url = reverse("api:v1:push_notifications:notifications-list")
    client.force_login(user=visitor_notification.user)
    response = client.get(url, data={"only_read": "foo"})
    assert response.status_code == HttpStatusCode.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_pn_list_query_params_valid(visitor_notification: PushNotification, client: Client):
    assert visitor_notification.read_at is None

    url = reverse("api:v1:push_notifications:notifications-list")
    client.force_login(user=visitor_notification.user)
    response = client.get(url, data={"only_read": True})
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert len(response.json()["results"]) == 0

    visitor_notification.read_at = timezone.now()
    visitor_notification.save()

    response = client.get(url, data={"only_read": True})
    assert len(response.json()["results"]) == 1

    response = client.get(url, data={"only_read": False})
    assert len(response.json()["results"]) == 0


@pytest.mark.django_db
def test_pn_read_many_all_valid_ids(visitor_notification: PushNotification, client: Client):
    url = reverse("api:v1:push_notifications:notifications-read-many")
    client.force_login(user=visitor_notification.user)
    response = client.patch(
        url, data={"ids": [visitor_notification.id]}, content_type="application/json"
    )
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert response.json()["read"] == 1


@pytest.mark.django_db
def test_pn_read_many_ids_not_set(visitor_notification: PushNotification, client: Client):
    url = reverse("api:v1:push_notifications:notifications-read-many")
    client.force_login(user=visitor_notification.user)
    # We can send None/null to read all notifications
    response = client.patch(url, data={"ids": None}, content_type="application/json")
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert response.json()["read"] == 1

    # reset
    visitor_notification.read_at = None
    visitor_notification.save(force_update=True)

    # We also can send a empty/null data and would read all notifications
    response = client.patch(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert response.json()["read"] == 1


@pytest.mark.django_db
def test_pn_read_many_ids_from_other_user_no_update_happens(
    visitor_notification: PushNotification, admin_client: Client
):
    url = reverse("api:v1:push_notifications:notifications-read-many")
    # We're requesting from a user that has no visibility to the notification
    response = admin_client.patch(
        url, data={"ids": [visitor_notification.id]}, content_type="application/json"
    )
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert response.json()["read"] == 0


@pytest.mark.django_db
def test_pn_read_id_from_other_user_404(
    visitor_notification: PushNotification, admin_client: Client
):
    # We're requesting from a user that has no visibility to the notification
    url = reverse("api:v1:push_notifications:notifications-read", args=(visitor_notification.id,))
    response = admin_client.patch(url)
    assert response.status_code == HttpStatusCode.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_pn_read_id_already_read(visitor_notification: PushNotification, client: Client):
    # if the notification is already read, it should succeed, but no updates should happen
    now = timezone.localtime()
    visitor_notification.read_at = now
    visitor_notification.save()

    url = reverse("api:v1:push_notifications:notifications-read", args=(visitor_notification.id,))
    client.force_login(visitor_notification.user)
    response = client.patch(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    data = response.json()
    assert data["read_at"] == now.isoformat()


@pytest.mark.django_db
def test_pn_read_id_expected_output(visitor_notification: PushNotification, client: Client):
    # if the notification is not read, it should succeed and updates should happen
    assert visitor_notification.read_at is None
    assert visitor_notification.status != Status.READ

    url = reverse("api:v1:push_notifications:notifications-read", args=(visitor_notification.id,))
    client.force_login(visitor_notification.user)
    response = client.patch(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    data = response.json()
    assert data["read_at"] is not None
    assert data["status"]["value"] == Status.READ

    visitor_notification = PushNotification.objects.get(pk=visitor_notification.pk)
    assert visitor_notification.read_at is not None
    assert visitor_notification.status == Status.READ


@pytest.mark.django_db
def test_pn_set_token(client: Client, visitor_user: User):
    assert visitor_user.notification_token is None

    url = reverse("api:v1:push_notifications:notifications-token")
    client.force_login(visitor_user)
    response = client.put(
        url, data={"notification_token": "foobar"}, content_type="application/json"
    )
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    with pytest.raises(TypeError):
        # We don't return any data, so trying to get the json should return an error
        response.json()

    visitor_user = User.objects.get(pk=visitor_user.pk)
    assert visitor_user.notification_token == "foobar"


@pytest.mark.django_db
def test_pn_set_token_invalid(client: Client, visitor_user: User):
    # Someone could try to opt-out of notifications trying to use this endpoint
    # sending a null value, but that's not how we expect it. For that they should
    # send a DELETE request instead
    url = reverse("api:v1:push_notifications:notifications-token")
    client.force_login(visitor_user)
    response = client.put(url, data={"notification_token": None}, content_type="application/json")
    assert response.status_code == HttpStatusCode.HTTP_400_BAD_REQUEST
    assert "notification_token" in response.json()["extra"]["fields"]


@pytest.mark.django_db
def test_pn_delete_token(client: Client, visitor_user: User):
    url = reverse("api:v1:push_notifications:notifications-token")
    client.force_login(visitor_user)
    response = client.delete(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    with pytest.raises(TypeError):
        # We don't return any data, so trying to get the json should return an error
        response.json()
