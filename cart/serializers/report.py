from rest_framework import serializers

from cart.models import MonthlySalesReport


class RecentLocationsSerializer(serializers.Serializer):
    location = serializers.CharField()
    count = serializers.IntegerField()


class UserTopItemsSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=None)
    count = serializers.IntegerField()


class SalesReportSerializer(serializers.ModelSerializer):
    menu_item = serializers.SerializerMethodField()

    @staticmethod
    def get_menu_item(obj):
        return obj.menu_item.name

    class Meta:
        model = MonthlySalesReport
        fields = "__all__"
