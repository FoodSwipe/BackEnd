from rest_framework import serializers

from cart.models import OrderKOT


class KotSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderKOT
        depth = 1


class OrderKOTPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderKOT
