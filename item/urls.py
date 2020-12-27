from django.urls import path
from rest_framework.routers import DefaultRouter

from item.views import (ItemTypeViewSet, MenuItemViewSet,
                        OrderNowItemsListView, RecommendedItemsListView,
                        TopItemsListView, TopRecommendedMenuItemViewSet)

router = DefaultRouter()
router.register("item-type", ItemTypeViewSet, basename="menu-item")
router.register("menu-item", MenuItemViewSet, basename="menu-item")
router.register("top-recommended-items", TopRecommendedMenuItemViewSet, basename="menu-item")

urlpatterns = router.urls

app_name = "item"

urlpatterns += [
    path("order-now-list", OrderNowItemsListView.as_view(), name="order-now-list"),
    path("top-items", TopItemsListView.as_view(), name="top-items"),
    path("recommended-items", RecommendedItemsListView.as_view(), name="top-items"),
]
