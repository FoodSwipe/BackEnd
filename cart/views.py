from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Order, CartItem
from cart.serializers import OrderSerializer, OrderPOSTSerializer, CartItemSerializer, CartItemPOSTSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderPOSTSerializer
        return super(OrderViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({
            "message": "Order deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CartItemPOSTSerializer
        return super(CartItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({
            "message": "Cart item removed successfully."
        }, status=status.HTTP_204_NO_CONTENT)
