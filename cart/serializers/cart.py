import decimal

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from cart.models import CartItem
from utils.helper import get_delivery_charge, get_loyalty_discount


class CartItemSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%b %d, %Y %H:%M")

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
            validated_data["quantity"]
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

        item_base_order.delivery_charge = get_delivery_charge()

        item_base_order.loyalty_discount = get_loyalty_discount(
            item_base_order.total_price
        )

        item_base_order.grand_total = (
            item_base_order.total_price
            + item_base_order.delivery_charge
            - decimal.Decimal(item_base_order.loyalty_discount / 100)
            * item_base_order.total_price
        )

        item_base_order.save()

        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.quantity != validated_data["quantity"]:
            instance.order.total_items -= instance.quantity
            instance.order.total_items += validated_data["quantity"]

            instance.order.total_price -= instance.quantity * instance.item.price
            instance.order.total_price += instance.item.price * int(
                validated_data["quantity"]
            )

            instance.order.delivery_charge = get_delivery_charge()

            instance.order.loyalty_discount = get_loyalty_discount(
                instance.order.total_price
            )

            instance.order.grand_total = (
                instance.order.total_price
                + instance.order.delivery_charge
                - decimal.Decimal(instance.order.loyalty_discount / 100)
                * instance.order.total_price
            )

            instance.order.save()
        return super().update(instance, validated_data)
