import pytest

from app import consts
from push_notifications import services
from users.models import User


@pytest.mark.django_db
def test_push_notification_create_status_is_failed_when_user_has_no_notification_token(
    visitor_user: User,
):
    if visitor_user.notification_token is not None:
        visitor_user.notification_token = None
        visitor_user.save()

    push_notification = services.push_notification_create(
        user=visitor_user,
        kind=consts.push_notification.Kind.INTERNAL_COMMUNICATION,
        title="Hey you, yes you!",
        description="We have a new vaccine available",
        data={"foo": "bar"},
    )
    assert push_notification.status == consts.push_notification.Status.FAILED
    assert push_notification.failure_kind == consts.push_notification.FailureKind.NOT_OPTED_IN


@pytest.mark.django_db
def test_push_notification_create_succeeds(
    visitor_user: User,
):
    visitor_user.notification_token = "foo"
    visitor_user.save()

    push_notification = services.push_notification_create(
        user=visitor_user,
        kind=consts.push_notification.Kind.INTERNAL_COMMUNICATION,
        title="Hey you, yes you!",
        description="We have a new vaccine available",
        data={"foo": "bar"},
    )
    assert push_notification.status == consts.push_notification.Status.CREATED
    assert push_notification.title == "Hey you, yes you!"
    assert push_notification.description == "We have a new vaccine available"
    assert push_notification.data == {"foo": "bar"}
