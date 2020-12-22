from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Order, CartItem
from cart.serializers import OrderSerializer, OrderPOSTSerializer, CartItemSerializer, CartItemPOSTSerializer, \
    OrderCreateSerializer, OrderWithCartListSerializer


class PartialUpdateOrderView(APIView):
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderCreateSerializer(
                instance=order,
                data=request.data,
                partial=True,
                context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Order updated successfully."
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({
                "message": "Order not found."
            }, status=status.HTTP_404_NOT_FOUND)


class OrderWithCartListView(APIView):
    @staticmethod
    def get(request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderWithCartListSerializer(
                instance=order,
                context={"request": request}
            )
            return Response({
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                "message": "Order not found."
            }, status=status.HTTP_404_NOT_FOUND)


class InitializeOrder(APIView):
    @staticmethod
    def post(request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            order = serializer.save()
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            "message": "Cart item removed successfully."
        }, status=status.HTTP_204_NO_CONTENT)
