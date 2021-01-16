from django.urls import path
from rest_framework.routers import DefaultRouter

from item_group.views import MenuItemGroupsWithItemListView, MenuItemGroupViewSet

router = DefaultRouter()
router.register("menu-item-group", MenuItemGroupViewSet, basename="menu-item-group")

urlpatterns = router.urls

app_name = "item_group"

urlpatterns += [
    path(
        "item-group-with-items",
        MenuItemGroupsWithItemListView.as_view(),
        name="groups-with-items",
    )
]
