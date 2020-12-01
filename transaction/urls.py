from rest_framework.routers import DefaultRouter

from transaction.views import TransactionViewSet

router = DefaultRouter()
router.register("transaction", TransactionViewSet, basename="transaction")

urlpatterns = router.urls

app_name = "transaction"

urlpatterns += [
    # TODO add filter apis
]
