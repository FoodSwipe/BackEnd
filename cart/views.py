import itertools
from collections import Counter

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from cart.models import CartItem, MonthlySalesReport, Order
from cart.serializers import (CartItemPOSTSerializer, CartItemSerializer,
                              OrderCreateSerializer, OrderPOSTSerializer,
                              OrderSerializer, OrderWithCartListSerializer,
                              RecentLocationsSerializer, SalesReportSerializer,
                              UserTopItemsSerializer)
from item.models import MenuItem
from log.models import Log
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
        Log.objects.create(
            mode="delete",
            actor=request.user,
            detail="Deleted order #{} of user {}".format(order.id, order.custom_contact)
        )
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


class SalesReportListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        # most ordered items calculation
        bought_items_list = []
        item_id_list = []
        all_cart_items = CartItem.objects.all()
        for cart_item in all_cart_items:
            item_id_list.append(cart_item.item.id)
        item_with_count_dict = dict(Counter(item_id_list))
        desc_sorted_dict = dict(sorted(
            item_with_count_dict.items(),
            key=lambda menu_item: menu_item[1],
            reverse=True
        ))
        now = timezone.datetime.now()
        print(desc_sorted_dict)
        for itemId, count in desc_sorted_dict.items():
            item = MenuItem.objects.get(pk=itemId)
            bought_item, created = MonthlySalesReport.objects.get_or_create(menu_item=item, date=now.strftime("%Y/%m"))
            bought_item.sale_count = count
            bought_item.save()
            bought_items_list.append(bought_item)
        serializer = SalesReportSerializer(
            instance=bought_items_list,
            many=True,
            context={"request": request}
        )
        return Response({
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class DoneFromCustomerView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if order.done_from_customer:
                return Response({
                    "detail": "Order already set done."
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                if isinstance(request.user, get_user_model()):
                    """
                    If request user is already registered user
                    then set order author as the request user
                    """
                    order.created_by = request.user
                    order.save()
                else:
                    try:
                        """
                        If request user is anonymous and order custom_contact belongs
                        to some user, then assign order to user found. 
                        """
                        profile = Profile.objects.get(contact=order.custom_contact)
                        order.created_by = profile.user
                        order.save()
                    except Profile.DoesNotExist:
                        """
                        If request user is anonymous and order custom_contact is totally unique,
                        then create a new user with the custom_contact and assign order author
                        """
                        user = get_user_model().objects.create(
                            username="{}".format(str(order.custom_contact.national_number))
                        )
                        if order.custom_email:
                            user.email = order.custom_email
                        user.set_password(str(order.custom_contact.national_number))
                        user.save()

                        user.profile.contact = order.custom_contact
                        user.save()

                        order.created_by = user
                        order.save()

                order.done_from_customer = True
                order.save()
                Log.objects.create(
                    mode="done",
                    actor=order.created_by,
                    detail="Order #{} marked done from customer {} at {}".format(
                        order.id, order.custom_contact, order.custom_location
                    ))
                return Response({
                    "result": "Order sucessfully set to done."
                }, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({
                "detail": "Order does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
