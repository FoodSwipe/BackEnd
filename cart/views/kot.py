from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from cart.models import OrderKOT
from cart.serializers.kot import KotSerializer, OrderKOTPostSerializer


class OrderKotViewSet(viewsets.ModelViewSet):
    queryset = OrderKOT.objects.all()
    serializer_class = [KotSerializer]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return OrderKOTPostSerializer
        return super(OrderKotViewSet, self).get_serializer_class()
