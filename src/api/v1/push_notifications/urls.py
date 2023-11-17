from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("", views.PushNotificationViewSet, basename="notifications")

urlpatterns = router.urls
