from rest_framework.routers import DefaultRouter

from item.views import ItemTypeViewSet, MenuItemViewSet, MenuItemTypeViewSet, MenuItemImageViewSet

router = DefaultRouter()
router.register("item-type", ItemTypeViewSet, basename="menu-item")
router.register("menu-item", MenuItemViewSet, basename="menu-item")
router.register("menu-item-type", MenuItemTypeViewSet, basename="menu-item")
router.register("menu-item-image", MenuItemImageViewSet, basename="menu-item")

urlpatterns = router.urls

app_name = "item"

urlpatterns += [
    # TODO add filter apis
]
