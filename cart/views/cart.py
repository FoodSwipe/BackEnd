from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import CartItem
from cart.serializers.cart import CartItemSerializer, CartItemPOSTSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by('created_at')
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial_update":
            return CartItemPOSTSerializer
        return super(CartItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.order.total_items -= cart_item.quantity
        cart_item.order.total_price -= cart_item.quantity * cart_item.item.price
        cart_item.order.save()
        cart_item.delete()
        return Response({
            "message": "Cart order_location removed successfully."
        }, status=status.HTTP_204_NO_CONTENT)
