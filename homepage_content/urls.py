from django.urls import path
from rest_framework.routers import DefaultRouter

from homepage_content.views import (HomePageContentListView,
                                    HomepageContentViewSet)

router = DefaultRouter()
router.register(r'homepage-content', HomepageContentViewSet, basename='homepage-content')
urlpatterns = router.urls

app_name = "homepage_content"

urlpatterns += [
    path("home-page-contents", HomePageContentListView.as_view(), name="homepage-list"),
]
