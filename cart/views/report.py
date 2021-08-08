import itertools
from collections import Counter

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem, MonthlySalesReport, Order
from cart.serializers.report import (RecentLocationsSerializer,
                                     SalesReportSerializer,
                                     UserTopItemsSerializer)
from item.models import MenuItem
from utils.helper import generate_url_for_media_resources


class RecentLocation:
    def __init__(self, location, count):
        self.location = location
        self.count = count


class TopItem:
    def __init__(self, image, count, name):
        self.image = image
        self.count = count
        self.name = name


def get_reverse_sorted_dict(not_sorted_dict):
    """
    :param not_sorted_dict dictionary to sort
    :returns dict sorted dictionary
    """
    return dict(sorted(not_sorted_dict.items(), key=lambda item: item[1], reverse=True))


def get_top_items_from_dict(desc_sorted_dict, top_count):
    """
    :returns top `count` items form the reverse sorted dict
    """
    if len(desc_sorted_dict) <= top_count:
        return desc_sorted_dict
    else:
        return dict(itertools.islice(desc_sorted_dict.items(), top_count))


def get_top_items_of_user(cart_items):
    """:returns top items with from supplied cart items"""
    top_items = []
    item_id_list = []

    for cart_item in cart_items:
        item_id_list.append(cart_item.item.id)

    item_with_count_dict = dict(Counter(item_id_list))
    desc_sorted_dict = get_reverse_sorted_dict(item_with_count_dict)
    top_six_items_dict = get_top_items_from_dict(desc_sorted_dict, 6)

    for itemId, count in top_six_items_dict.items():
        item = MenuItem.objects.get(pk=itemId)
        top_item = TopItem(image=item.image.url, count=count, name=item.name)
        top_items.append(top_item)

    return top_items


def get_most_recent_locations_of_user(completed_orders):
    """:returns top locations with count from supplied orders"""
    # recent order_location calculation
    recent_locations = []
    most_recent_locations = []

    for order in completed_orders:
        recent_locations.append(order.custom_location)

    recent_locations_with_count_dict = dict(Counter(recent_locations))
    desc_sorted_recent_locations_dict = get_reverse_sorted_dict(
        recent_locations_with_count_dict
    )
    most_recent_locations_dict = get_top_items_from_dict(
        desc_sorted_recent_locations_dict, 3
    )

    for location, count in most_recent_locations_dict.items():
        location_obj = RecentLocation(location=location, count=count)
        most_recent_locations.append(location_obj)
    return most_recent_locations


def get_total_transaction_amount_of_a_user(completed_orders):
    """:returns sum of grand total of supplied orders"""
    total_transaction = 0
    for order in completed_orders:
        total_transaction += order.grand_total
    return total_transaction


class StorySummaryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            user = get_user_model().objects.get(pk=pk)
            total_orders = Order.objects.filter(created_by=user).count()
            all_cart_items = CartItem.objects.filter(created_by=user)
            cart_items_count = all_cart_items.count()

            top_items = get_top_items_of_user(all_cart_items)

            top_items = UserTopItemsSerializer(
                instance=top_items,
                many=True,
                read_only=True,
                context={"request": request},
            )
            top_items = generate_url_for_media_resources(top_items)

            completed_orders = Order.objects.filter(created_by=user, is_delivered=True)
            most_recent_locations = get_most_recent_locations_of_user(completed_orders)
            most_recent_locations = RecentLocationsSerializer(
                instance=most_recent_locations, many=True, read_only=True
            ).data

            total_transaction = get_total_transaction_amount_of_a_user(completed_orders)

            return Response(
                {
                    "total_transaction": total_transaction,
                    "total_orders": total_orders,
                    "total_cart_items_count": cart_items_count,
                    "top_items": top_items.data,
                    "most_recent_locations": most_recent_locations,
                },
                status=status.HTTP_200_OK,
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"details": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


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
        desc_sorted_dict = get_reverse_sorted_dict(item_with_count_dict)
        now = timezone.datetime.now()
        for itemId, count in desc_sorted_dict.items():
            item = MenuItem.objects.get(pk=itemId)
            bought_item, created = MonthlySalesReport.objects.get_or_create(
                menu_item=item, date=now.strftime("%Y/%m")
            )
            bought_item.sale_count = count
            bought_item.save()
            bought_items_list.append(bought_item)
        serializer = SalesReportSerializer(
            instance=bought_items_list, many=True, context={"request": request}
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
