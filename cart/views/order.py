from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from cart.models import CartItem, Order, OrderKOT
from cart.serializers.order import (OrderCreateSerializer, OrderPOSTSerializer,
                                    OrderSerializer,
                                    OrderWithCartListSerializer)
from log.models import Log


class OrderWithCartItemsList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderWithCartListSerializer(
            instance=orders, many=True, read_only=True
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class PartialUpdateOrderView(APIView):
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderCreateSerializer(
                instance=order,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Order updated successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )


class OrderWithCartListView(APIView):
    @staticmethod
    def get(request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderWithCartListSerializer(
                instance=order, context={"request": request}
            )
            return Response({"results": serializer.data}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )


class InitializeOrder(APIView):
    @staticmethod
    def post(request):
        serializer = OrderCreateSerializer(
            data=request.data, context={"request": request}
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
    filterset_fields = ["delivery_started", "is_delivered", "done_from_customer"]
    search_fields = ["custom_location", "custom_contact", "custom_email", "created_by__username", "updated_at"]

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
            detail="Deleted order #{} of user {}".format(
                order.id, order.custom_contact
            ),
        )
        return Response(
            {"message": "Order deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserOrders(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            user = get_user_model().objects.get(pk=pk)
            orders = Order.objects.filter(created_by=user)
            serializer = OrderWithCartListSerializer(
                instance=orders, read_only=True, many=True
            )
            return Response({"results": serializer.data}, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response(
                {"details": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class DoneFromCustomerView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if order.done_from_customer:
                return Response(
                    {"detail": "Order already set done."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
                            username="{}".format(
                                str(order.custom_contact.national_number)
                            )
                        )
                        if order.custom_email:
                            user.email = order.custom_email
                        user.set_password(str(order.custom_contact.national_number))
                        user.save()

                        user.profile.contact = order.custom_contact
                        user.profile.address = order.custom_location
                        user.save()

                        order.created_by = user
                        order.save()

                order.done_from_customer = True
                order.done_from_customer_at = timezone.datetime.now()
                order.save()

                # create batch one for kot
                cart_items = CartItem.objects.filter(order=order)
                for cart_item in cart_items:
                    OrderKOT.objects.create(
                        order=order,
                        cart_item=cart_item,
                        batch=1,
                        quantity_diff=cart_item.quantity,
                    )
                Log.objects.create(
                    mode="done",
                    actor=order.created_by,
                    detail="Order #{} marked done by customer {} from {}".format(
                        order.id, order.custom_contact, order.custom_location
                    ),
                )
                return Response(
                    {"result": "Order sucessfully set as done."},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
