from django.urls import path
from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet, OrderViewSet, InitializeOrder, OrderWithCartListView

router = DefaultRouter()
router.register(r'cart-item', CartItemViewSet, basename='cart-item')
router.register(r'order', OrderViewSet, basename='order')
urlpatterns = router.urls

app_name = "cart"

urlpatterns += [
    path('init-order', InitializeOrder.as_view(), name='initialize-order'),
    path('order/<int:pk>/cart', OrderWithCartListView.as_view(), name='initialize-order')
]
