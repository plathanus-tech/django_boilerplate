from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("me", views.CurrentUserViewSet, basename="me")

urlpatterns = router.urls
