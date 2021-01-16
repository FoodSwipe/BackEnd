from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import OrderKOT
from cart.serializers.kot import KOTPOSTSerializer, KOTSerializer


class OrderKotViewSet(viewsets.ModelViewSet):
    queryset = OrderKOT.objects.all()
    serializer_class = [KOTSerializer]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return KOTPOSTSerializer
        return super(OrderKotViewSet, self).get_serializer_class()


class KotListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = KOTSerializer
    queryset = OrderKOT.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ("batch", "order", "timestamp")
