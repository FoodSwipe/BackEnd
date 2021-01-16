from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet

router = DefaultRouter()
router.register(r"review", ReviewViewSet, basename="order")
urlpatterns = router.urls

app_name = "reviews"

urlpatterns += []
