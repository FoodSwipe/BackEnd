from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Order, OrderKOT, CartItem
from cart.serializers.kot import KOTPOSTSerializer, KOTSerializer


class OrderKotViewSet(viewsets.ModelViewSet):
    queryset = OrderKOT.objects.all()
    serializer_class = KOTSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return KOTPOSTSerializer
        return super(OrderKotViewSet, self).get_serializer_class()


class InitFirstBatchKot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_kots = OrderKOT.objects.filter(order=order)
        if len(order_kots) > 0:
            return Response("Kot is already initialized.", status=status.HTTP_400_BAD_REQUEST)
        else:
            cart_items = CartItem.objects.filter(order=order)
            for cart_item in cart_items:
                OrderKOT.objects.create(
                    order=order,
                    cart_item=cart_item,
                    batch=1,
                    quantity_diff=cart_item.quantity,
                )
            return Response("First batch kot initialized.", status=status.HTTP_201_CREATED)


class KotListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = KOTSerializer
    queryset = OrderKOT.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ("batch", "order", "timestamp")


class GeneratePostKotView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order_kots = OrderKOT.objects.filter(order=order)
            have_more_batches = False
            for kot in order_kots:
                if kot.batch > 1:
                    have_more_batches = True
                    break
            if not have_more_batches:
                return Response(
                    {
                        "detail": "Order has not been updated from previous generated KOT."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                pass
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order does not exists."}, status=status.HTTP_400_BAD_REQUEST
            )
