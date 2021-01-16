from rest_framework import serializers

from cart.models import OrderKOT


class KOTSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        return obj.timestamp.strftime("%b %d, %Y %H:%M:%S")

    class Meta:
        model = OrderKOT
        fields = "__all__"
        depth = 2


class KOTPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderKOT
        fields = "__all__"
