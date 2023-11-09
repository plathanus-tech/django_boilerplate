from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("notifications", views.PushNotificationViewSet, basename="push_notifications")

urlpatterns = router.urls
