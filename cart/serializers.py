from rest_framework import serializers

from cart.models import CartItem, Order


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        depth = 1


class CartItemPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {"order": {"write_only": True}}

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        item_base_order = validated_data["order"]
        cart_item = validated_data["item"]
        item_base_order.total_price = cart_item.price * int(validated_data["quantity"])
        item_base_order.save()
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.quantity != validated_data["quantity"]:
            instance.order.total_price -= instance.quantity * instance.item.price
            instance.order.total_price += instance.item.price * int(validated_data["quantity"])
            instance.order.save()
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class OrderPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Order.objects.create(**validated_data)
