from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem, Order, OrderKOT
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
            return Response(
                "Kot is already initialized.", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            cart_items = CartItem.objects.filter(order=order)
            for cart_item in cart_items:
                OrderKOT.objects.create(
                    order=order,
                    cart_item=cart_item,
                    batch=1,
                    quantity_diff=cart_item.quantity,
                )
            return Response(
                "First batch kot initialized.", status=status.HTTP_201_CREATED
            )


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

    @staticmethod
    def get_last_batch(kot_list):
        last_batch = 1
        for item_order_kot in kot_list:
            if item_order_kot.batch > last_batch:
                last_batch = item_order_kot.batch
        return last_batch

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_kots = OrderKOT.objects.filter(order=order).order_by("-timestamp")
        cart_items = CartItem.objects.filter(order=order).order_by("-created_at")

        temp_kot_items = {}
        temp_cart_items = {}

        for cart_item in cart_items:
            temp_cart_items[cart_item.item.id] = cart_item.quantity

        latest_batch = self.get_last_batch(order_kots)

        for order_kot in order_kots:
            try:
                temp_kot_items[order_kot.cart_item.item.id] += order_kot.quantity_diff
            except KeyError:
                temp_kot_items[order_kot.cart_item.item.id] = order_kot.quantity_diff

        print(temp_cart_items)
        print(temp_kot_items)

        for cart_item in cart_items:
            try:
                total_kot_items = temp_kot_items[cart_item.item.id]
                diff = cart_item.quantity - total_kot_items
                if diff == 0:
                    # we have the kot and the diff is zero
                    # take a chill pill and pass out from here
                    pass
                else:
                    # cart item quantity must have been updated
                    # new kot should be created with the diff
                    OrderKOT.objects.create(
                        order=order,
                        cart_item=cart_item,
                        quantity_diff=diff,
                        batch=latest_batch + 1,
                    )
            except KeyError:
                # kot not made yet for the item
                # maybe newly added from admin
                OrderKOT.objects.create(
                    order=order,
                    cart_item=cart_item,
                    quantity_diff=cart_item.quantity,
                    batch=latest_batch + 1,
                )
        return Response(status=status.HTTP_204_NO_CONTENT)
