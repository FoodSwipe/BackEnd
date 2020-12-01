from rest_framework.routers import DefaultRouter

from item_group.views import MenuItemGroupViewSet, MenuItemGroupImageViewSet

router = DefaultRouter()
router.register("menu-item-group", MenuItemGroupViewSet, basename="menu-item-group")
router.register("menu-item-group-image", MenuItemGroupImageViewSet, basename="menu-item-group-image")

urlpatterns = router.urls

app_name = "item_group"

urlpatterns += [
    # TODO add filter apis
]
