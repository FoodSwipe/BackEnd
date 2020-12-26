from rest_framework.routers import DefaultRouter

from homepage_content.views import HomepageContentViewSet

router = DefaultRouter()
router.register(r'homepage-content', HomepageContentViewSet, basename='homepage-content')
urlpatterns = router.urls

app_name = "homepage_content"

urlpatterns += [

]
