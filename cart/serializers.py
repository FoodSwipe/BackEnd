from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from cart.models import CartItem, Order


class CartItemSerializer(serializers.ModelSerializer):
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
        item_base_order.save()
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.quantity != validated_data["quantity"]:
            instance.order.total_items -= instance.quantity
            instance.order.total_items += validated_data["quantity"]

            instance.order.total_price -= instance.quantity * instance.item.price
            instance.order.total_price += instance.item.price * int(validated_data["quantity"])
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
        fields = ['custom_location', "custom_contact"]

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
        if isinstance(creator, AnonymousUser):
            try:
                order = Order.objects.get(custom_contact=custom_contact, created_by=None)
                raise serializers.ValidationError("Your order has already started at #{}. Please check your cart.".format(order.id))
            except Order.DoesNotExist:
                validated_data["created_by"] = None
        else:
            validated_data["created_by"] = creator
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

    class Meta:
        model = Order
        fields = [
            "custom_location",
            "custom_contact",
            "delivery_started",
            "delivery_started_at",
            "is_delivered",
            "sub_total",
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
