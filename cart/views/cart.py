from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem, OrderKOT
from cart.serializers.cart import CartItemPOSTSerializer, CartItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by("created_at")
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.action in ["create", "partial_update", "update"]:
            return CartItemPOSTSerializer
        return super(CartItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.order.total_items -= cart_item.quantity
        cart_item.order.total_price -= cart_item.quantity * cart_item.item.price
        cart_item.order.save()
        cart_item.delete()
        return Response(
            {"message": "Cart order_location removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CartItemQuantityUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_last_batch(kot_list):
        last_batch = 1
        for item_order_kot in kot_list:
            if item_order_kot.batch > last_batch:
                last_batch = item_order_kot.batch
        return last_batch

    @staticmethod
    def get_object(pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
            return cart_item
        except CartItem.DoesNotExist:
            return Response({
                "detail": "Cart item does not exists"
                }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        cart_item_instance = self.get_object(pk=pk)

        quantity_from_request = int(request.data.get("quantity"))
        previous_quantity = cart_item_instance.quantity
        if previous_quantity is quantity_from_request:
            return Response({
                "detail": "Quantity remains unchanged.",
            }, status=status.HTTP_200_OK)
        serializer = CartItemPOSTSerializer(
            instance=cart_item_instance,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            updated_cart_item = serializer.save()
            item_order_kots = OrderKOT.objects.filter(
                order=updated_cart_item.order,
                cart_item__item=updated_cart_item.item
            )
            last_batch = self.get_last_batch(item_order_kots)
            OrderKOT.objects.create(
                order=updated_cart_item.order,
                cart_item=updated_cart_item,
                batch=last_batch+1,
                quantity_diff=(updated_cart_item.quantity - previous_quantity)
            )
            return Response({
                "detail": "Cart item quantity updated successfully.",
                "cart_item": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
