from django.urls import path
from rest_framework.routers import DefaultRouter

from cart.views.cart import CartItemQuantityUpdateView, CartItemViewSet
from cart.views.kot import GeneratePostKotView, KotListView, OrderKotViewSet, InitFirstBatchKot
from cart.views.order import (DoneFromCustomerView, InitializeOrder,
                              OrderViewSet, OrderWithCartItemsList,
                              OrderWithCartListView, PartialUpdateOrderView,
                              UserOrders)
from cart.views.report import SalesReportListView, StorySummaryDetailView

router = DefaultRouter()
router.register(r"cart", CartItemViewSet, basename="cart-item")
router.register(r"order", OrderViewSet, basename="order")
router.register(r"order-kot", OrderKotViewSet, basename="order-kot")
urlpatterns = router.urls

app_name = "cart"

urlpatterns += [
    path("orders", OrderWithCartItemsList.as_view(), name="orders-list"),
    path("init-order", InitializeOrder.as_view(), name="initialize-order"),
    path(
        "order/<int:pk>/cart", OrderWithCartListView.as_view(), name="initialize-order"
    ),
    path(
        "update-order/<int:pk>", PartialUpdateOrderView.as_view(), name="update-order"
    ),
    path("user/<int:pk>/orders", UserOrders.as_view(), name="user_orders"),
    path(
        "user/<int:pk>/store-summary",
        StorySummaryDetailView.as_view(),
        name="user-store-summary",
    ),
    path("sales-report", SalesReportListView.as_view(), name="sales-report"),
    path(
        "done-from-customer/<int:pk>",
        DoneFromCustomerView.as_view(),
        name="done-from-customer",
    ),
    path("kot", KotListView.as_view(), name="kot-filter"),
    path("init-fist-batch/<int:pk>", InitFirstBatchKot.as_view(), name="init-first-batch-kot"),
    path(
        "generate-post-kot/<int:pk>",
        GeneratePostKotView.as_view(),
        name="generate-post-kot",
    ),
    path(
        "cart-item/<int:pk>/quantity-update",
        CartItemQuantityUpdateView.as_view(),
        name="kot-quantity-update",
    ),
]
