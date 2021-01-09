from rest_framework import serializers

from cart.serializers.order import OrderWithCartListSerializer
from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    order = OrderWithCartListSerializer()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%b %d, %Y %H:%M")

    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 1


class TransactionPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
