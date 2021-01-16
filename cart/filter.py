import django_filters

from cart.models import OrderKOT


class OrderKOTFilter(django_filters.FilterSet):
    batch = django_filters.NumberFilter()

    class Meta:
        model = OrderKOT
        fields = ["batch"]
