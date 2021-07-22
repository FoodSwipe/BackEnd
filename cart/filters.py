from django_filters import DateTimeFromToRangeFilter, FilterSet

from cart.models import Order


class OrderFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Order
        fields = ["created_at"]
