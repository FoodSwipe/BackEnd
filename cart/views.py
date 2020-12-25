import itertools
from collections import Counter

from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Order, CartItem
from cart.serializers import OrderSerializer, OrderPOSTSerializer, CartItemSerializer, CartItemPOSTSerializer, \
    OrderCreateSerializer, OrderWithCartListSerializer, RecentLocationsSerializer, UserTopItemsSerializer
from item.models import MenuItem
from item.serializers import MenuItemSerializer
from utils.helper import generate_url_for_media_resources


class OrderWithCartItemsList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderWithCartListSerializer(instance=orders, many=True, read_only=True)
        return Response({
            "results": serializer.data
        }, status=status.HTTP_200_OK)


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
        if self.action in ["create", "partial_update", "update"]:
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
            "message": "Cart order_location removed successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class UserOrders(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            user = get_user_model().objects.get(pk=pk)
            orders = Order.objects.filter(created_by=user)
            serializer = OrderWithCartListSerializer(instance=orders, read_only=True, many=True)
            return Response({
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({
                "details": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)


class RecentLocation:
    def __init__(self, location, count):
        self.location = location
        self.count = count


class TopItem:
    def __init__(self, image, count):
        self.image = image,
        self.count = count


class StorySummaryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            user = get_user_model().objects.get(pk=pk)
            total_orders = Order.objects.filter(created_by=user).count()
            all_cart_items = CartItem.objects.filter(created_by=user)
            cart_items_count = all_cart_items.count()

            # most ordered items calculation
            top_items = []
            item_id_list = []
            for cart_item in all_cart_items:
                item_id_list.append(cart_item.item.id)
            item_with_count_dict = dict(Counter(item_id_list))
            desc_sorted_dict = dict(sorted(
                item_with_count_dict.items(),
                key=lambda menu_item: menu_item[1],
                reverse=True
            ))
            if len(desc_sorted_dict) <= 6:
                top_six_items_dict = desc_sorted_dict
            else:
                top_six_items_dict = dict(itertools.islice(desc_sorted_dict.items(), 6))
            for itemId, count in top_six_items_dict.items():
                item = MenuItem.objects.get(pk=itemId)
                print(item.image.url)
                top_item = TopItem(image=item.image.url, count=count)
                top_item.image = top_item.image[0]
                top_items.append(top_item)
            top_items = UserTopItemsSerializer(
                instance=top_items,
                many=True,
                read_only=True,
                context={"request": request}
            )
            top_items = generate_url_for_media_resources(top_items)

            # recent order_location calculation
            recent_locations = []
            most_recent_locations = []
            total_transaction = 0
            all_completed_orders = Order.objects.filter(created_by=user, is_delivered=True)
            for order in all_completed_orders:
                total_transaction += order.grand_total
                recent_locations.append(order.custom_location)
            recent_locations_with_count_dict = dict(Counter(recent_locations))
            desc_sorted_recent_locations_dict = dict(sorted(
                recent_locations_with_count_dict.items(),
                key=lambda order_location: order_location[1],
                reverse=True
            ))
            if len(desc_sorted_recent_locations_dict) <= 3:
                most_recent_locations_dict = desc_sorted_recent_locations_dict
            else:
                most_recent_locations_dict = dict(itertools.islice(desc_sorted_dict.items(), 3))
            for location, count in most_recent_locations_dict.items():
                location_obj = RecentLocation(location=location, count=count)
                most_recent_locations.append(location_obj)
            most_recent_locations = RecentLocationsSerializer(
                instance=most_recent_locations,
                many=True,
                read_only=True
            ).data

            return Response({
                "total_transaction": total_transaction,
                "total_orders": total_orders,
                "total_cart_items_count": cart_items_count,
                "top_items": top_items.data,
                "most_recent_locations": most_recent_locations
            }, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({
                "details": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)
