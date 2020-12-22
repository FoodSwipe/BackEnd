import decimal

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework import serializers

from backend.settings import DELIVERY_START_PM, DELIVERY_START_AM, DELIVERY_CHARGE, LOYALTY_12_PER_FROM, \
    LOYALTY_10_PER_FROM, LOYALTY_13_PER_FROM, LOYALTY_15_PER_FROM
from cart.models import CartItem, Order


class CartItemSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = CartItem
        fields = "__all__"
        depth = 2


class CartItemPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {"order": {"write_only": True}}

    def create(self, validated_data):
        current_hour = int(timezone.datetime.now().strftime("%H"))

        try:
            check = validated_data["quantity"]
        except KeyError:
            validated_data["quantity"] = 1

        creator = self.context["request"].user
        if isinstance(creator, AnonymousUser):
            validated_data["created_by"] = None
        else:
            validated_data["created_by"] = creator

        item_base_order = validated_data["order"]
        cart_item = validated_data["item"]
        item_base_order.total_items += int(validated_data["quantity"])
        item_base_order.total_price += cart_item.price * int(validated_data["quantity"])

        if current_hour >= DELIVERY_START_PM or current_hour <= DELIVERY_START_AM:
            item_base_order.delivery_charge = DELIVERY_CHARGE

        if LOYALTY_10_PER_FROM <= item_base_order.total_price < LOYALTY_12_PER_FROM:
            item_base_order.loyalty_discount = 10
        elif LOYALTY_12_PER_FROM <= item_base_order.total_price < LOYALTY_13_PER_FROM:
            item_base_order.loyalty_discount = 12
        elif LOYALTY_13_PER_FROM <= item_base_order.total_price < LOYALTY_15_PER_FROM:
            item_base_order.loyalty_discount = 13
        elif item_base_order.total_price >= LOYALTY_15_PER_FROM:
            item_base_order.loyalty_discount = 15

        item_base_order.grand_total = \
            item_base_order.total_price + item_base_order.delivery_charge - \
            decimal.Decimal(item_base_order.loyalty_discount / 100) * item_base_order.total_price

        item_base_order.save()
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        current_hour = int(timezone.datetime.now().strftime("%H"))
        if instance.quantity != validated_data["quantity"]:
            instance.order.total_items -= instance.quantity
            instance.order.total_items += validated_data["quantity"]

            instance.order.total_price -= instance.quantity * instance.item.price
            instance.order.total_price += instance.item.price * int(validated_data["quantity"])

            if current_hour >= DELIVERY_START_PM or current_hour <= DELIVERY_START_AM:
                instance.order.delivery_charge = DELIVERY_CHARGE

            if LOYALTY_10_PER_FROM <= instance.order.total_price < LOYALTY_12_PER_FROM:
                instance.order.loyalty_discount = 10
            elif LOYALTY_12_PER_FROM <= instance.order.total_price < LOYALTY_13_PER_FROM:
                instance.order.loyalty_discount = 12
            elif LOYALTY_13_PER_FROM <= instance.order.total_price < LOYALTY_15_PER_FROM:
                instance.order.loyalty_discount = 13
            elif instance.order.total_price >= LOYALTY_15_PER_FROM:
                instance.order.loyalty_discount = 15

            instance.order.grand_total = \
                instance.order.total_price + instance.order.delivery_charge - \
                decimal.Decimal(instance.order.loyalty_discount / 100) * instance.order.total_price

            instance.order.save()
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['custom_location', "custom_contact", "custom_email", "payment_type", "done_from_customer"]

    def get_fields(self, *args, **kwargs):
        fields = super(OrderCreateSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and isinstance(request.user, AnonymousUser):
            fields['custom_location'].required = True
            fields['custom_contact'].required = True
        return fields

    def create(self, validated_data):
        creator = self.context["request"].user
        custom_contact = validated_data.get("custom_contact")
        # check if pending order exists from customer side
        if isinstance(creator, AnonymousUser):
            try:
                order = Order.objects.get(custom_contact=custom_contact, created_by=None, done_from_customer=False)
                raise serializers.ValidationError(
                    "Ongoing order exists at #{}. Please check your cart.".format(order.id))
            except Order.DoesNotExist:
                validated_data["created_by"] = None
        else:
            try:
                order = Order.objects.get(custom_contact=custom_contact, created_by=creator, done_from_customer=False)
                raise serializers.ValidationError(
                    "Ongoing order exists at #{}. Please check your cart.".format(order.id))
            except Order.DoesNotExist:
                validated_data["created_by"] = creator
                email = validated_data.get("custom_email", None)
                if not email:
                    validated_data["custom_email"] = creator.email
                return Order.objects.create(**validated_data)


class OrderPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Order.objects.create(**validated_data)


class OrderWithCartListSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = Order
        fields = [
            "custom_location",
            "custom_contact",
            "custom_email",
            "delivery_started",
            "delivery_started_at",
            "is_delivered",
            "delivery_charge",
            "loyalty_discount",
            "grand_total",
            "total_price",
            "total_items",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "cart_items"
        ]
