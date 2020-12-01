from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'cart-item', CartItemViewSet, basename='cart-item')
router.register(r'order', OrderViewSet, basename='order')
urlpatterns = router.urls

app_name = "cart"

urlpatterns += [
    # TODO add filter apis
]
