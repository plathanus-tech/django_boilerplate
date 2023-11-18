from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register("", views.AuthenticationViewSet, basename="auth")

urlpatterns = router.urls
